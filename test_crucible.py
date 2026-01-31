#!/usr/bin/env python3
"""
Test suite for CRUCIBLE evaluation engine
"""

import unittest
import json
import os
from crucible import (
    CrucibleEvaluator, 
    Decision, 
    Perspective,
    DimensionScore,
    Experiment,
    EvaluationResult
)


class TestCrucibleEvaluator(unittest.TestCase):
    """Test cases for CRUCIBLE evaluator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.evaluator = CrucibleEvaluator()
    
    def test_evaluator_initialization(self):
        """Test that evaluator initializes correctly"""
        self.assertEqual(len(self.evaluator.DIMENSIONS), 5)
        self.assertEqual(len(self.evaluator.perspectives), 3)
    
    def test_dimension_scoring(self):
        """Test that all dimensions are evaluated"""
        concept = "SaaS platform for enterprise customers with proven revenue"
        result = self.evaluator.evaluate(concept)
        
        self.assertEqual(len(result.dimension_scores), 5)
        for score in result.dimension_scores:
            self.assertGreaterEqual(score.score, 1)
            self.assertLessEqual(score.score, 10)
            self.assertIsNotNone(score.reasoning)
            self.assertGreater(len(score.failure_modes), 0)
    
    def test_strong_concept_gets_proceed(self):
        """Test that strong concepts get positive decision"""
        strong_concept = (
            "Proven SaaS platform with recurring revenue, "
            "validated customers, high margins, network effects, "
            "and automated operations serving global enterprise market"
        )
        result = self.evaluator.evaluate(strong_concept)
        
        self.assertIn(result.decision, [
            Decision.PROCEED, 
            Decision.STRONG_PROCEED
        ])
        self.assertGreater(result.overall_score, 6.0)
    
    def test_weak_concept_gets_caution_or_kill(self):
        """Test that weak concepts get cautionary decision"""
        weak_concept = (
            "Complex blockchain solution requiring new technology "
            "for small niche market with manual operations"
        )
        result = self.evaluator.evaluate(weak_concept)
        
        self.assertIn(result.decision, [
            Decision.KILL,
            Decision.PROCEED_WITH_CAUTION
        ])
        self.assertLess(result.overall_score, 7.0)
    
    def test_market_viability_analysis(self):
        """Test market viability scoring logic"""
        good_market = "platform serving billion dollar global enterprise market with validated customers"
        bad_market = "niche solution for small market with limited audience"
        
        good_result = self.evaluator.evaluate(good_market)
        bad_result = self.evaluator.evaluate(bad_market)
        
        good_market_score = [s for s in good_result.dimension_scores if "Market" in s.dimension][0]
        bad_market_score = [s for s in bad_result.dimension_scores if "Market" in s.dimension][0]
        
        self.assertGreater(good_market_score.score, bad_market_score.score)
    
    def test_technical_feasibility_analysis(self):
        """Test technical feasibility scoring logic"""
        simple_tech = "simple solution using proven stack and existing technology"
        complex_tech = "revolutionary quantum AI blockchain requiring bleeding edge technology"
        
        simple_result = self.evaluator.evaluate(simple_tech)
        complex_result = self.evaluator.evaluate(complex_tech)
        
        simple_tech_score = [s for s in simple_result.dimension_scores if "Technical" in s.dimension][0]
        complex_tech_score = [s for s in complex_result.dimension_scores if "Technical" in s.dimension][0]
        
        self.assertGreater(simple_tech_score.score, complex_tech_score.score)
    
    def test_unit_economics_analysis(self):
        """Test unit economics scoring logic"""
        good_economics = "SaaS subscription platform with recurring revenue and high margins"
        bad_economics = "free ad-supported service with low margins and manual operations"
        
        good_result = self.evaluator.evaluate(good_economics)
        bad_result = self.evaluator.evaluate(bad_economics)
        
        good_econ_score = [s for s in good_result.dimension_scores if "Economics" in s.dimension][0]
        bad_econ_score = [s for s in bad_result.dimension_scores if "Economics" in s.dimension][0]
        
        self.assertGreater(good_econ_score.score, bad_econ_score.score)
    
    def test_competitive_moats_analysis(self):
        """Test competitive moats scoring logic"""
        strong_moats = "platform with network effects, proprietary data, and high switching costs"
        weak_moats = "commodity service in crowded competitive market easy to switch"
        
        strong_result = self.evaluator.evaluate(strong_moats)
        weak_result = self.evaluator.evaluate(weak_moats)
        
        strong_moat_score = [s for s in strong_result.dimension_scores if "Moat" in s.dimension][0]
        weak_moat_score = [s for s in weak_result.dimension_scores if "Moat" in s.dimension][0]
        
        self.assertGreater(strong_moat_score.score, weak_moat_score.score)
    
    def test_scaling_analysis(self):
        """Test scaling bottlenecks scoring logic"""
        scalable = "automated platform with self-service and global cloud distribution"
        not_scalable = "manual custom service requiring specialized experts and local compliance"
        
        scalable_result = self.evaluator.evaluate(scalable)
        not_scalable_result = self.evaluator.evaluate(not_scalable)
        
        scalable_score = [s for s in scalable_result.dimension_scores if "Scaling" in s.dimension][0]
        not_scalable_score = [s for s in not_scalable_result.dimension_scores if "Scaling" in s.dimension][0]
        
        self.assertGreater(scalable_score.score, not_scalable_score.score)
    
    def test_generates_three_experiments(self):
        """Test that exactly 3 validation experiments are generated"""
        concept = "New marketplace platform"
        result = self.evaluator.evaluate(concept)
        
        self.assertEqual(len(result.validation_experiments), 3)
        for exp in result.validation_experiments:
            self.assertIsNotNone(exp.title)
            self.assertIsNotNone(exp.hypothesis)
            self.assertIsNotNone(exp.method)
            self.assertIsNotNone(exp.success_criteria)
    
    def test_generates_pivots_for_weak_dimensions(self):
        """Test that pivots are generated for weak dimensions"""
        weak_concept = "manual niche service with free model"
        result = self.evaluator.evaluate(weak_concept)
        
        self.assertGreater(len(result.key_pivots), 0)
        self.assertIsNotNone(result.refined_concept)
    
    def test_identifies_critical_risks(self):
        """Test that critical risks are identified"""
        risky_concept = "complex new technology for small market"
        result = self.evaluator.evaluate(risky_concept)
        
        self.assertGreater(len(result.critical_risks), 0)
    
    def test_perspective_assignment(self):
        """Test that perspectives are assigned to dimensions"""
        concept = "test concept"
        result = self.evaluator.evaluate(concept)
        
        perspectives_used = set()
        for score in result.dimension_scores:
            perspectives_used.add(score.perspective)
        
        # Should use multiple perspectives
        self.assertGreater(len(perspectives_used), 1)
    
    def test_overall_score_calculation(self):
        """Test that overall score is average of dimension scores"""
        concept = "test concept"
        result = self.evaluator.evaluate(concept)
        
        expected_avg = sum(s.score for s in result.dimension_scores) / len(result.dimension_scores)
        self.assertAlmostEqual(result.overall_score, expected_avg, places=2)
    
    def test_decision_thresholds(self):
        """Test decision making thresholds"""
        # Mock high scores
        high_scores = [DimensionScore(d, 9, "test", [], "test") for d in self.evaluator.DIMENSIONS]
        decision = self.evaluator._make_decision(9.0, high_scores)
        self.assertEqual(decision, Decision.STRONG_PROCEED)
        
        # Mock low scores
        low_scores = [DimensionScore(d, 3, "test", [], "test") for d in self.evaluator.DIMENSIONS]
        decision = self.evaluator._make_decision(3.0, low_scores)
        self.assertEqual(decision, Decision.KILL)
    
    def test_result_serialization(self):
        """Test that results can be serialized to JSON"""
        concept = "test concept"
        result = self.evaluator.evaluate(concept)
        
        # Should be able to convert to dict
        from dataclasses import asdict
        result_dict = asdict(result)
        result_dict['decision'] = result.decision.value
        
        # Should be able to serialize to JSON
        json_str = json.dumps(result_dict)
        self.assertIsNotNone(json_str)
        
        # Should be able to deserialize
        parsed = json.loads(json_str)
        self.assertEqual(parsed['original_concept'], concept)


class TestExampleConcepts(unittest.TestCase):
    """Test CRUCIBLE with real-world example concepts"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.evaluator = CrucibleEvaluator()
    
    def test_saas_platform_example(self):
        """Test evaluation of SaaS platform concept"""
        concept = (
            "B2B SaaS platform for marketing automation with "
            "subscription model, proven customers, and automated workflows"
        )
        result = self.evaluator.evaluate(concept)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result.dimension_scores), 5)
        self.assertEqual(len(result.validation_experiments), 3)
        
    def test_marketplace_example(self):
        """Test evaluation of marketplace concept"""
        concept = (
            "Two-sided marketplace connecting freelancers with enterprise clients, "
            "building network effects through platform integration"
        )
        result = self.evaluator.evaluate(concept)
        
        self.assertIsNotNone(result)
        # Marketplace should have decent competitive moat score due to network effects
        moat_score = [s for s in result.dimension_scores if "Moat" in s.dimension][0]
        self.assertGreaterEqual(moat_score.score, 5)
    
    def test_ai_product_example(self):
        """Test evaluation of AI product concept"""
        concept = (
            "AI-powered analytics tool using machine learning "
            "to predict customer churn for SaaS companies"
        )
        result = self.evaluator.evaluate(concept)
        
        self.assertIsNotNone(result)
        # AI should flag technical complexity
        tech_score = [s for s in result.dimension_scores if "Technical" in s.dimension][0]
        self.assertLessEqual(tech_score.score, 7)  # Should show some concern
    
    def test_hardware_product_example(self):
        """Test evaluation of hardware product concept"""
        concept = (
            "Hardware device with physical inventory and logistics requirements"
        )
        result = self.evaluator.evaluate(concept)
        
        self.assertIsNotNone(result)
        # Hardware should flag unit economics concerns
        econ_score = [s for s in result.dimension_scores if "Economics" in s.dimension][0]
        self.assertLessEqual(econ_score.score, 6)  # Should show margin concerns


class TestOutputFormatting(unittest.TestCase):
    """Test output formatting functions"""
    
    def test_format_output_completeness(self):
        """Test that formatted output includes all key sections"""
        from crucible import format_output
        
        evaluator = CrucibleEvaluator()
        concept = "Test concept"
        result = evaluator.evaluate(concept)
        
        output = format_output(result)
        
        # Check for key sections
        self.assertIn("CRUCIBLE EVALUATION REPORT", output)
        self.assertIn("DIMENSION SCORES", output)
        self.assertIn("DECISION:", output)
        self.assertIn("REFINED CONCEPT", output)
        self.assertIn("KEY PIVOTS", output)
        self.assertIn("VALIDATION EXPERIMENTS", output)
        self.assertIn("CRITICAL RISKS", output)
        self.assertIn("Weak ideas die here", output)
    
    def test_format_output_includes_all_dimensions(self):
        """Test that output includes all 5 dimensions"""
        from crucible import format_output
        
        evaluator = CrucibleEvaluator()
        result = evaluator.evaluate("Test concept")
        output = format_output(result)
        
        for dimension in CrucibleEvaluator.DIMENSIONS:
            self.assertIn(dimension, output)


def run_example_evaluation():
    """Run an example evaluation for manual testing"""
    print("\n" + "=" * 70)
    print("Running Example Evaluation")
    print("=" * 70 + "\n")
    
    evaluator = CrucibleEvaluator()
    concept = (
        "AI-powered fitness app that creates personalized workout plans "
        "using machine learning to analyze user performance and adapt in real-time"
    )
    
    result = evaluator.evaluate(concept)
    
    from crucible import format_output
    print(format_output(result))


if __name__ == "__main__":
    # Run tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run example
    run_example_evaluation()
