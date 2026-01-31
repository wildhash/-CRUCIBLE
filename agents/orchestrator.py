"""
CRUCIBLE Orchestrator - Coordinates multi-model adversarial evaluation

Runs concept through adversarial model gauntlet.
Each model attacks from its specialized angle.
Synthesizes consensus score + divergent opinions.
"""

import asyncio
import os
from typing import List, Dict, Optional
from models.evaluation import ModelEvaluation, CrucibleVerdict, Decision, DimensionScore, Experiment
from agents.base_evaluator import BaseEvaluator, MockEvaluator
from agents.evaluators import EVALUATOR_MODELS, DIMENSION_MODEL_PRIORITY


class CrucibleOrchestrator:
    """
    Orchestrates multi-model adversarial evaluation
    
    Three-phase process:
    1. Parallel model evaluation - each model evaluates independently
    2. Cross-model debate - models critique each other (future enhancement)
    3. Consensus synthesis - combine into unified verdict
    """
    
    DIMENSIONS = [
        "Market Viability",
        "Technical Feasibility", 
        "Unit Economics",
        "Competitive Moats",
        "Scaling Bottlenecks"
    ]
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize orchestrator
        
        Args:
            use_mock: If True, use mock evaluators (for testing/no API keys)
                     If False, attempt to use real API evaluators
        """
        self.use_mock = use_mock
        self.evaluators: Dict[str, BaseEvaluator] = {}
        self._initialize_evaluators()
    
    def _initialize_evaluators(self):
        """Initialize all model evaluators - real API or mock fallback"""
        import os
        
        # Try to import real evaluators
        try:
            from agents.evaluators.claude_critic import ClaudeEvaluator
            from agents.evaluators.gpt_skeptic import GPTEvaluator
            from agents.evaluators.deepseek_tech import DeepSeekEvaluator
            from agents.evaluators.grok_contrarian import GrokEvaluator
            from agents.evaluators.gemini_analyst import GeminiEvaluator
        except ImportError:
            # If imports fail, use mock for all
            for model_name, config in EVALUATOR_MODELS.items():
                self.evaluators[model_name] = MockEvaluator(
                    model_name=model_name,
                    role=config["role"]
                )
            return
        
        # Map model names to evaluator classes
        evaluator_classes = {
            "claude_opus": ClaudeEvaluator,
            "gpt_o3": GPTEvaluator,
            "deepseek_r1": DeepSeekEvaluator,
            "grok": GrokEvaluator,
            "gemini_flash": GeminiEvaluator,
        }
        
        for model_name, config in EVALUATOR_MODELS.items():
            # Check if we should use real API evaluator
            if not self.use_mock and model_name in evaluator_classes:
                # Check if API key is available
                api_env_var = {
                    "claude_opus": "ANTHROPIC_API_KEY",
                    "gpt_o3": "OPENAI_API_KEY",
                    "deepseek_r1": "DEEPSEEK_API_KEY",
                    "grok": "XAI_API_KEY",
                    "gemini_flash": "GOOGLE_API_KEY",
                }.get(model_name)
                
                if api_env_var and os.getenv(api_env_var):
                    try:
                        # Try to instantiate real evaluator
                        evaluator_class = evaluator_classes[model_name]
                        self.evaluators[model_name] = evaluator_class()
                        print(f"  ✓ Initialized real API evaluator: {model_name}")
                        continue
                    except Exception as e:
                        print(f"  ⚠ Failed to init {model_name} API evaluator: {e}")
            
            # Fallback to mock evaluator
            self.evaluators[model_name] = MockEvaluator(
                model_name=model_name,
                role=config["role"]
            )
    
    async def run_adversarial_evaluation(
        self, 
        concept: str,
        selected_models: Optional[List[str]] = None
    ) -> CrucibleVerdict:
        """
        Run complete adversarial evaluation through model gauntlet
        
        Args:
            concept: The startup concept to evaluate
            selected_models: Optional list of model names to use (uses all if None)
            
        Returns:
            CrucibleVerdict with consensus and model-specific evaluations
        """
        print("\n🔥 Multi-Model CRUCIBLE: Adversarial Evaluation Gauntlet")
        print("=" * 70)
        
        # Phase 1: Parallel model evaluation
        print(f"\n📡 Phase 1: Parallel Model Evaluation ({len(self.evaluators)} models)")
        evaluations = await self._run_parallel_evaluation(concept, selected_models)
        
        # Phase 2: Cross-model debate (simplified for now)
        print("\n💬 Phase 2: Cross-Model Debate & Critique")
        debates = await self._run_debate_rounds(evaluations)
        
        # Phase 3: Consensus synthesis
        print("\n🎯 Phase 3: Consensus Synthesis")
        verdict = await self._synthesize_verdict(concept, evaluations, debates)
        
        return verdict
    
    async def _run_parallel_evaluation(
        self, 
        concept: str,
        selected_models: Optional[List[str]] = None
    ) -> List[ModelEvaluation]:
        """
        Run all models in parallel to evaluate the concept
        
        Args:
            concept: Startup concept to evaluate
            selected_models: Optional list of specific models to use
            
        Returns:
            List of ModelEvaluation results
        """
        models_to_use = selected_models or list(self.evaluators.keys())
        
        # Create evaluation tasks for all models
        tasks = []
        for model_name in models_to_use:
            if model_name in self.evaluators:
                evaluator = self.evaluators[model_name]
                task = evaluator.evaluate(concept, self.DIMENSIONS)
                tasks.append(task)
                print(f"  ⚡ Launching {model_name} ({EVALUATOR_MODELS[model_name]['role']})")
        
        # Run all evaluations in parallel
        evaluations = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out any exceptions
        valid_evaluations = []
        for i, result in enumerate(evaluations):
            if isinstance(result, Exception):
                print(f"  ❌ Model {models_to_use[i]} failed: {str(result)}")
            else:
                print(f"  ✓ {result.model_name} complete (confidence: {result.confidence:.1%})")
                valid_evaluations.append(result)
        
        return valid_evaluations
    
    async def _run_debate_rounds(
        self, 
        evaluations: List[ModelEvaluation]
    ) -> List[str]:
        """
        Run cross-model debate rounds (simplified version)
        
        In full implementation, models would critique each other's evaluations.
        For now, we identify where models disagree significantly.
        
        Args:
            evaluations: List of model evaluations
            
        Returns:
            List of debate points (where models disagreed)
        """
        debates = []
        
        # Find dimensions where models disagree significantly
        for dimension in self.DIMENSIONS:
            scores = []
            for eval in evaluations:
                if dimension in eval.scores:
                    scores.append(eval.scores[dimension])
            
            if scores:
                min_score = min(scores)
                max_score = max(scores)
                
                if max_score - min_score >= 3:  # Significant disagreement
                    avg_score = sum(scores) / len(scores)
                    debates.append(
                        f"{dimension}: Models disagree (range {min_score}-{max_score}, "
                        f"avg {avg_score:.1f}) - requires deeper analysis"
                    )
                    print(f"  ⚔️ Debate: {dimension} scores range from {min_score} to {max_score}")
        
        if not debates:
            print("  ✓ Models generally agree on scores")
        
        return debates
    
    async def _synthesize_verdict(
        self,
        concept: str,
        evaluations: List[ModelEvaluation],
        debates: List[str]
    ) -> CrucibleVerdict:
        """
        Synthesize final verdict from all model evaluations
        
        Args:
            concept: Original concept
            evaluations: All model evaluations
            debates: List of debate points
            
        Returns:
            CrucibleVerdict with consensus
        """
        # Calculate consensus scores for each dimension
        dimension_scores = []
        for dimension in self.DIMENSIONS:
            scores = []
            weights = []
            all_failure_modes = []
            model_evals = []
            
            for eval in evaluations:
                if dimension in eval.scores:
                    scores.append(eval.scores[dimension])
                    # Weight by model weight and confidence
                    model_weight = EVALUATOR_MODELS[eval.model_name]["weight"]
                    weights.append(model_weight * eval.confidence)
                    all_failure_modes.extend(eval.failure_modes)
                    model_evals.append(eval)
            
            if scores:
                # Weighted average
                weighted_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
                consensus_score = round(weighted_score)
                
                # Get perspective from highest priority model for this dimension
                perspective = self._get_dimension_perspective(dimension, model_evals)
                
                dimension_scores.append(DimensionScore(
                    dimension=dimension,
                    score=consensus_score,
                    reasoning=self._synthesize_reasoning(dimension, model_evals),
                    failure_modes=list(set(all_failure_modes))[:3],  # Top 3 unique
                    perspective=perspective,
                    model_evaluations=model_evals
                ))
        
        # Calculate overall consensus score
        overall_score = sum(ds.score for ds in dimension_scores) / len(dimension_scores)
        
        # Make decision
        decision = self._make_decision(overall_score, dimension_scores)
        
        # Synthesize unified pivots
        unified_pivots = self._synthesize_pivots(evaluations)
        
        # Generate validation experiments
        experiments = self._generate_experiments(dimension_scores)
        
        # Identify critical risks
        critical_risks = self._identify_risks(dimension_scores)
        
        # Check for minority reports (models that strongly disagree)
        minority_report = self._find_minority_report(evaluations, overall_score)
        
        # Generate refined concept
        refined_concept = self._refine_concept(concept, unified_pivots, decision)
        
        print(f"\n  📊 Consensus Score: {overall_score:.1f}/10")
        print(f"  ⚖️ Decision: {decision.value}")
        
        return CrucibleVerdict(
            original_concept=concept,
            consensus_score=overall_score,
            decision=decision,
            model_evaluations=evaluations,
            dimension_scores=dimension_scores,
            key_debates=debates,
            unified_pivots=unified_pivots,
            validation_experiments=experiments,
            critical_risks=critical_risks,
            minority_report=minority_report,
            refined_concept=refined_concept
        )
    
    def _get_dimension_perspective(
        self, 
        dimension: str, 
        model_evals: List[ModelEvaluation]
    ) -> str:
        """Get the perspective for a dimension from highest priority model"""
        priority_models = DIMENSION_MODEL_PRIORITY.get(dimension, [])
        
        for model_name in priority_models:
            for eval in model_evals:
                if eval.model_name == model_name:
                    return f"{EVALUATOR_MODELS[model_name]['role']}"
        
        # Fallback to first model
        if model_evals:
            return model_evals[0].role
        return "consensus"
    
    def _synthesize_reasoning(
        self, 
        dimension: str, 
        model_evals: List[ModelEvaluation]
    ) -> str:
        """Synthesize reasoning from multiple models"""
        if not model_evals:
            return "No evaluations available"
        
        # Get reasoning from highest priority model for this dimension
        priority_models = DIMENSION_MODEL_PRIORITY.get(dimension, [])
        
        for model_name in priority_models:
            for eval in model_evals:
                if eval.model_name == model_name and eval.reasoning:
                    return eval.reasoning[:200]  # First 200 chars
        
        # Fallback to first model's reasoning
        return model_evals[0].reasoning[:200] if model_evals[0].reasoning else "See model evaluations"
    
    def _make_decision(
        self, 
        overall_score: float, 
        dimension_scores: List[DimensionScore]
    ) -> Decision:
        """Make kill/proceed decision based on consensus"""
        min_score = min(ds.score for ds in dimension_scores)
        critically_low = [ds for ds in dimension_scores if ds.score <= 3]
        
        if overall_score >= 8 and min_score >= 6:
            return Decision.STRONG_PROCEED
        elif overall_score >= 7 and min_score >= 4:
            return Decision.PROCEED
        elif overall_score >= 6 and min_score >= 3:
            return Decision.PROCEED_WITH_CAUTION
        elif overall_score >= 5 and len(critically_low) <= 1:
            return Decision.PROCEED_WITH_CAUTION
        else:
            return Decision.KILL
    
    def _synthesize_pivots(self, evaluations: List[ModelEvaluation]) -> List[str]:
        """Synthesize unified pivots from all models"""
        all_pivots = []
        for eval in evaluations:
            all_pivots.extend(eval.pivots_suggested)
        
        # Deduplicate and return top 3
        unique_pivots = list(dict.fromkeys(all_pivots))  # Preserve order
        return unique_pivots[:3]
    
    def _generate_experiments(self, dimension_scores: List[DimensionScore]) -> List[Experiment]:
        """Generate validation experiments for weak dimensions"""
        experiments = []
        weak_dims = sorted(dimension_scores, key=lambda x: x.score)[:3]
        
        for dim_score in weak_dims:
            if "Market" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Customer Discovery Sprint",
                    hypothesis="Target customers have urgent need and willingness to pay",
                    method="Interview 20-30 target customers, measure genuine interest and LOI commitment",
                    success_criteria="50%+ express strong interest, 20%+ willing to prepay or sign LOI",
                    estimated_cost="$500-2000",
                    estimated_time="2-3 weeks"
                ))
            elif "Technical" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Technical Proof of Concept",
                    hypothesis="Core technology delivers promised value at acceptable cost/performance",
                    method="Build minimal prototype of hardest component, measure performance",
                    success_criteria="Achieves 80%+ of promised capability within 2x cost budget",
                    estimated_cost="$2000-10000",
                    estimated_time="2-4 weeks"
                ))
            elif "Economics" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Unit Economics Stress Test",
                    hypothesis="Unit economics are profitable at scale with conservative assumptions",
                    method="Build detailed financial model, stress test key variables",
                    success_criteria="LTV/CAC > 3, payback < 18 months, positive unit economics by month 12",
                    estimated_cost="$500-1000",
                    estimated_time="1 week"
                ))
            elif "Moats" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Competitive Differentiation Test",
                    hypothesis="Our unique value proposition is defensible and meaningful",
                    method="A/B test our pitch vs competitor alternatives with target customers",
                    success_criteria="60%+ choose our approach when presented with alternatives",
                    estimated_cost="$1000-3000",
                    estimated_time="2 weeks"
                ))
            elif "Scaling" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Scaling Simulation",
                    hypothesis="Operations and costs scale sub-linearly with growth",
                    method="Model operational requirements at 10x and 100x scale",
                    success_criteria="Variable costs < 30% of revenue at scale",
                    estimated_cost="$500-2000",
                    estimated_time="1-2 weeks"
                ))
        
        # Ensure we have exactly 3 experiments
        while len(experiments) < 3:
            experiments.append(Experiment(
                title="Assumption Validation",
                hypothesis="Critical business assumptions hold under scrutiny",
                method="Identify and systematically test top 3 riskiest assumptions",
                success_criteria="All critical assumptions validated or alternative paths identified",
                estimated_cost="$1000-5000",
                estimated_time="2-4 weeks"
            ))
        
        return experiments[:3]
    
    def _identify_risks(self, dimension_scores: List[DimensionScore]) -> List[str]:
        """Identify critical risks from dimension scores"""
        risks = []
        for ds in dimension_scores:
            if ds.score < 6:
                for fm in ds.failure_modes[:2]:
                    risks.append(f"[{ds.dimension}] {fm}")
        return risks[:5]
    
    def _find_minority_report(
        self, 
        evaluations: List[ModelEvaluation], 
        consensus_score: float
    ) -> Optional[str]:
        """Find if any model strongly disagrees with consensus"""
        for eval in evaluations:
            avg_model_score = sum(eval.scores.values()) / len(eval.scores) if eval.scores else 0
            
            if abs(avg_model_score - consensus_score) >= 3:
                return (
                    f"{eval.model_name} ({eval.role}) strongly disagrees: "
                    f"Scored {avg_model_score:.1f} vs consensus {consensus_score:.1f}. "
                    f"{eval.dissenting_opinion or 'See detailed evaluation for reasoning.'}"
                )
        
        return None
    
    def _refine_concept(
        self, 
        concept: str, 
        pivots: List[str], 
        decision: Decision
    ) -> str:
        """Generate refined concept incorporating pivots"""
        if decision == Decision.KILL:
            return f"KILL: {concept} - Fundamental issues require complete rethink."
        elif pivots:
            return f"{concept} PIVOTS: {' AND '.join(pivots[:2])}"
        else:
            return concept
