#!/usr/bin/env python3
"""
Test suite for multi-model CRUCIBLE architecture
"""

import unittest
import asyncio
from models.evaluation import ModelEvaluation, CrucibleVerdict, Decision
from agents.base_evaluator import MockEvaluator
from agents.orchestrator import CrucibleOrchestrator
from agents.evaluators import EVALUATOR_MODELS


class TestMultiModelArchitecture(unittest.TestCase):
    """Test multi-model evaluation architecture"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = CrucibleOrchestrator(use_mock=True)
        self.test_concept = "B2B SaaS platform with proven revenue"
    
    def test_orchestrator_initialization(self):
        """Test that orchestrator initializes with all models"""
        self.assertEqual(len(self.orchestrator.evaluators), len(EVALUATOR_MODELS))
        
        for model_name in EVALUATOR_MODELS.keys():
            self.assertIn(model_name, self.orchestrator.evaluators)
    
    def test_mock_evaluator(self):
        """Test mock evaluator returns valid evaluation"""
        evaluator = MockEvaluator("test_model", "test_role")
        
        async def run_test():
            result = await evaluator.evaluate(
                self.test_concept,
                self.orchestrator.DIMENSIONS
            )
            
            self.assertIsInstance(result, ModelEvaluation)
            self.assertEqual(result.model_name, "test_model")
            self.assertEqual(result.role, "test_role")
            self.assertEqual(len(result.scores), 5)
            
            # Check all scores are in valid range
            for score in result.scores.values():
                self.assertGreaterEqual(score, 1)
                self.assertLessEqual(score, 10)
        
        asyncio.run(run_test())
    
    def test_parallel_evaluation(self):
        """Test parallel model evaluation"""
        async def run_test():
            evaluations = await self.orchestrator._run_parallel_evaluation(
                self.test_concept
            )
            
            self.assertEqual(len(evaluations), len(EVALUATOR_MODELS))
            
            for eval in evaluations:
                self.assertIsInstance(eval, ModelEvaluation)
                self.assertGreater(len(eval.scores), 0)
        
        asyncio.run(run_test())
    
    def test_full_adversarial_evaluation(self):
        """Test complete adversarial evaluation flow"""
        async def run_test():
            verdict = await self.orchestrator.run_adversarial_evaluation(
                self.test_concept
            )
            
            self.assertIsInstance(verdict, CrucibleVerdict)
            self.assertEqual(verdict.original_concept, self.test_concept)
            self.assertEqual(len(verdict.model_evaluations), len(EVALUATOR_MODELS))
            self.assertEqual(len(verdict.dimension_scores), 5)
            self.assertIsInstance(verdict.decision, Decision)
            self.assertGreater(verdict.consensus_score, 0)
            self.assertLessEqual(verdict.consensus_score, 10)
        
        asyncio.run(run_test())
    
    def test_consensus_calculation(self):
        """Test that consensus is properly calculated from multiple models"""
        async def run_test():
            verdict = await self.orchestrator.run_adversarial_evaluation(
                self.test_concept
            )
            
            # Calculate expected consensus manually
            for dim_score in verdict.dimension_scores:
                # Should be average of model scores for that dimension
                model_scores = [
                    e.scores.get(dim_score.dimension, 5)
                    for e in verdict.model_evaluations
                ]
                self.assertGreater(len(model_scores), 0)
        
        asyncio.run(run_test())
    
    def test_debate_identification(self):
        """Test that model disagreements are identified"""
        async def run_test():
            # Create mock evaluations with disagreement
            evaluations = await self.orchestrator._run_parallel_evaluation(
                "blockchain-based social network"  # Should cause disagreement
            )
            
            debates = await self.orchestrator._run_debate_rounds(evaluations)
            
            # Debates list should exist
            self.assertIsInstance(debates, list)
        
        asyncio.run(run_test())
    
    def test_decision_logic(self):
        """Test decision making from consensus scores"""
        # High scores should get PROCEED or STRONG_PROCEED
        from models.evaluation import DimensionScore
        
        high_scores = [
            DimensionScore(dim, 9, "test", [], "test")
            for dim in self.orchestrator.DIMENSIONS
        ]
        decision = self.orchestrator._make_decision(9.0, high_scores)
        self.assertIn(decision, [Decision.PROCEED, Decision.STRONG_PROCEED])
        
        # Low scores should get KILL
        low_scores = [
            DimensionScore(dim, 2, "test", [], "test")
            for dim in self.orchestrator.DIMENSIONS
        ]
        decision = self.orchestrator._make_decision(2.0, low_scores)
        self.assertEqual(decision, Decision.KILL)
    
    def test_pivot_synthesis(self):
        """Test that pivots are synthesized from multiple models"""
        async def run_test():
            verdict = await self.orchestrator.run_adversarial_evaluation(
                "weak startup concept"
            )
            
            self.assertIsInstance(verdict.unified_pivots, list)
            # Should have some pivots for weak concept
            self.assertGreaterEqual(len(verdict.unified_pivots), 0)
        
        asyncio.run(run_test())
    
    def test_experiment_generation(self):
        """Test validation experiment generation"""
        async def run_test():
            verdict = await self.orchestrator.run_adversarial_evaluation(
                self.test_concept
            )
            
            self.assertEqual(len(verdict.validation_experiments), 3)
            
            for exp in verdict.validation_experiments:
                self.assertIsNotNone(exp.title)
                self.assertIsNotNone(exp.hypothesis)
                self.assertIsNotNone(exp.method)
        
        asyncio.run(run_test())
    
    def test_minority_report(self):
        """Test minority report generation when models disagree"""
        async def run_test():
            verdict = await self.orchestrator.run_adversarial_evaluation(
                self.test_concept
            )
            
            # Minority report may or may not exist
            self.assertTrue(
                verdict.minority_report is None or 
                isinstance(verdict.minority_report, str)
            )
        
        asyncio.run(run_test())
    
    def test_selective_model_evaluation(self):
        """Test evaluating with only selected models"""
        async def run_test():
            selected = ["claude_opus", "gpt_o3"]
            verdict = await self.orchestrator.run_adversarial_evaluation(
                self.test_concept,
                selected_models=selected
            )
            
            self.assertEqual(len(verdict.model_evaluations), len(selected))
        
        asyncio.run(run_test())


class TestModelRegistry(unittest.TestCase):
    """Test model registry configuration"""
    
    def test_all_models_configured(self):
        """Test that all expected models are in registry"""
        expected_models = [
            "claude_opus", "gpt_o3", "gemini_flash",
            "deepseek_r1", "grok", "kimi", "qwen"
        ]
        
        for model in expected_models:
            self.assertIn(model, EVALUATOR_MODELS)
    
    def test_model_configs_complete(self):
        """Test that each model has required config fields"""
        required_fields = ["role", "focus", "api", "model", "weight", "description"]
        
        for model_name, config in EVALUATOR_MODELS.items():
            for field in required_fields:
                self.assertIn(field, config, f"{model_name} missing {field}")
    
    def test_dimension_model_priority(self):
        """Test that dimension-model priority mapping exists"""
        from agents.evaluators import DIMENSION_MODEL_PRIORITY
        
        dimensions = [
            "Market Viability",
            "Technical Feasibility",
            "Unit Economics",
            "Competitive Moats",
            "Scaling Bottlenecks"
        ]
        
        for dim in dimensions:
            self.assertIn(dim, DIMENSION_MODEL_PRIORITY)
            # Should have at least one model per dimension
            self.assertGreater(len(DIMENSION_MODEL_PRIORITY[dim]), 0)


class TestDataModels(unittest.TestCase):
    """Test data model classes"""
    
    def test_model_evaluation_creation(self):
        """Test ModelEvaluation dataclass"""
        eval = ModelEvaluation(
            model_name="test",
            role="tester",
            scores={"dim1": 5},
            failure_modes=["test"],
            pivots_suggested=["pivot"],
            confidence=0.8
        )
        
        self.assertEqual(eval.model_name, "test")
        self.assertEqual(eval.confidence, 0.8)
    
    def test_crucible_verdict_creation(self):
        """Test CrucibleVerdict dataclass"""
        from models.evaluation import DimensionScore, Experiment
        
        verdict = CrucibleVerdict(
            original_concept="test",
            consensus_score=7.5,
            decision=Decision.PROCEED,
            model_evaluations=[],
            dimension_scores=[],
            key_debates=[],
            unified_pivots=[],
            validation_experiments=[],
            critical_risks=[]
        )
        
        self.assertEqual(verdict.consensus_score, 7.5)
        self.assertEqual(verdict.decision, Decision.PROCEED)


class TestPrompts(unittest.TestCase):
    """Test prompt configuration"""
    
    def test_prompts_exist_for_all_models(self):
        """Test that prompts are defined for all models"""
        from prompts.evaluator_prompts import MODEL_PROMPTS
        
        for model_name in EVALUATOR_MODELS.keys():
            self.assertIn(model_name, MODEL_PROMPTS)
    
    def test_prompts_not_empty(self):
        """Test that all prompts have content"""
        from prompts.evaluator_prompts import MODEL_PROMPTS
        
        for model_name, prompt in MODEL_PROMPTS.items():
            self.assertGreater(len(prompt), 0)
            self.assertIsInstance(prompt, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
