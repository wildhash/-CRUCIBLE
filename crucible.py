#!/usr/bin/env python3
"""
CRUCIBLE - Adversarial Startup Evaluation Agent

Multi-model adversarial refinement engine that stress-tests startup concepts 
through collaborative AI debate until they're investor-ready.

Weak ideas die here so strong ones survive.
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from enum import Enum


class Decision(Enum):
    """Kill or proceed decision for a startup concept"""
    KILL = "KILL"
    PROCEED_WITH_CAUTION = "PROCEED_WITH_CAUTION"
    PROCEED = "PROCEED"
    STRONG_PROCEED = "STRONG_PROCEED"


class Perspective(Enum):
    """Adversarial perspectives for evaluation"""
    VC_SKEPTIC = "VC Skeptic"
    DOMAIN_EXPERT = "Domain Expert"
    COMPETITOR = "Competitor"


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension"""
    dimension: str
    score: int  # 1-10
    reasoning: str
    failure_modes: List[str]
    perspective: str


@dataclass
class Experiment:
    """Validation experiment to test assumptions"""
    title: str
    hypothesis: str
    method: str
    success_criteria: str
    estimated_cost: str
    estimated_time: str


@dataclass
class EvaluationResult:
    """Complete evaluation result for a startup concept"""
    original_concept: str
    dimension_scores: List[DimensionScore]
    overall_score: float
    decision: Decision
    refined_concept: str
    key_pivots: List[str]
    validation_experiments: List[Experiment]
    critical_risks: List[str]


class CrucibleEvaluator:
    """
    CRUCIBLE Adversarial Evaluation Engine
    
    Evaluates startup concepts across 5 critical dimensions using 
    contrarian perspectives to identify weaknesses and opportunities.
    """
    
    DIMENSIONS = [
        "Market Viability",
        "Technical Feasibility", 
        "Unit Economics",
        "Competitive Moats",
        "Scaling Bottlenecks"
    ]
    
    def __init__(self):
        self.perspectives = [
            Perspective.VC_SKEPTIC,
            Perspective.DOMAIN_EXPERT,
            Perspective.COMPETITOR
        ]
    
    def evaluate(self, concept: str) -> EvaluationResult:
        """
        Evaluate a startup concept through adversarial analysis
        
        Args:
            concept: The startup concept description
            
        Returns:
            EvaluationResult with scores, decision, and recommendations
        """
        print("🔥 CRUCIBLE: Adversarial Evaluation Initiated")
        print("=" * 70)
        print(f"\nConcept: {concept}\n")
        
        # Evaluate each dimension from multiple perspectives
        dimension_scores = []
        for dimension in self.DIMENSIONS:
            score = self._evaluate_dimension(concept, dimension)
            dimension_scores.append(score)
        
        # Calculate overall score
        overall_score = sum(s.score for s in dimension_scores) / len(dimension_scores)
        
        # Make kill/proceed decision
        decision = self._make_decision(overall_score, dimension_scores)
        
        # Generate refined concept and pivots
        refined_concept, pivots = self._synthesize_refinements(
            concept, dimension_scores, decision
        )
        
        # Generate validation experiments
        experiments = self._generate_experiments(concept, dimension_scores)
        
        # Identify critical risks
        risks = self._identify_critical_risks(dimension_scores)
        
        return EvaluationResult(
            original_concept=concept,
            dimension_scores=dimension_scores,
            overall_score=overall_score,
            decision=decision,
            refined_concept=refined_concept,
            key_pivots=pivots,
            validation_experiments=experiments,
            critical_risks=risks
        )
    
    def _evaluate_dimension(self, concept: str, dimension: str) -> DimensionScore:
        """Evaluate a single dimension with adversarial perspective"""
        
        # This is a rule-based implementation that simulates adversarial thinking
        # In a production system, this would interface with LLMs for deeper analysis
        
        perspective = self._select_perspective(dimension)
        score, reasoning, failure_modes = self._analyze_dimension(
            concept, dimension, perspective
        )
        
        return DimensionScore(
            dimension=dimension,
            score=score,
            reasoning=reasoning,
            failure_modes=failure_modes,
            perspective=perspective.value
        )
    
    def _select_perspective(self, dimension: str) -> Perspective:
        """Select most relevant adversarial perspective for dimension"""
        perspective_map = {
            "Market Viability": Perspective.VC_SKEPTIC,
            "Technical Feasibility": Perspective.DOMAIN_EXPERT,
            "Unit Economics": Perspective.VC_SKEPTIC,
            "Competitive Moats": Perspective.COMPETITOR,
            "Scaling Bottlenecks": Perspective.DOMAIN_EXPERT
        }
        return perspective_map.get(dimension, Perspective.VC_SKEPTIC)
    
    def _analyze_dimension(
        self, concept: str, dimension: str, perspective: Perspective
    ) -> Tuple[int, str, List[str]]:
        """
        Analyze a dimension from an adversarial perspective
        
        Returns: (score, reasoning, failure_modes)
        """
        concept_lower = concept.lower()
        
        if dimension == "Market Viability":
            return self._analyze_market_viability(concept_lower, perspective)
        elif dimension == "Technical Feasibility":
            return self._analyze_technical_feasibility(concept_lower, perspective)
        elif dimension == "Unit Economics":
            return self._analyze_unit_economics(concept_lower, perspective)
        elif dimension == "Competitive Moats":
            return self._analyze_competitive_moats(concept_lower, perspective)
        elif dimension == "Scaling Bottlenecks":
            return self._analyze_scaling_bottlenecks(concept_lower, perspective)
        else:
            return 5, "Unknown dimension", []
    
    def _analyze_market_viability(
        self, concept: str, perspective: Perspective
    ) -> Tuple[int, str, List[str]]:
        """Analyze market viability from VC skeptic perspective"""
        
        # Check for red flags
        red_flags = []
        green_flags = []
        
        # Market size indicators
        if any(word in concept for word in ["niche", "small market", "limited audience"]):
            red_flags.append("Limited addressable market")
        if any(word in concept for word in ["billion", "enterprise", "global", "platform"]):
            green_flags.append("Large market opportunity")
        
        # Timing and adoption
        if any(word in concept for word in ["new technology", "bleeding edge", "revolutionary"]):
            red_flags.append("Market may not be ready for adoption")
        if any(word in concept for word in ["proven demand", "existing market", "growing need"]):
            green_flags.append("Market timing appears favorable")
        
        # Customer validation
        if any(word in concept for word in ["validated", "customers", "paying users", "revenue"]):
            green_flags.append("Evidence of customer demand")
        else:
            red_flags.append("Lack of customer validation mentioned")
        
        # Calculate score
        score = 5
        score += len(green_flags) * 2
        score -= len(red_flags) * 2
        score = max(1, min(10, score))
        
        reasoning = f"From {perspective.value} view: "
        if score >= 7:
            reasoning += "Market shows promise but needs validation. "
        elif score >= 5:
            reasoning += "Market viability is questionable. "
        else:
            reasoning += "Significant market concerns identified. "
        
        if green_flags:
            reasoning += f"Strengths: {', '.join(green_flags)}. "
        if red_flags:
            reasoning += f"Concerns: {', '.join(red_flags)}."
        
        failure_modes = [
            "Market size smaller than anticipated",
            "Customer acquisition costs exceed projections",
            "Market timing misalignment with technology adoption curve",
            "Regulatory barriers to market entry"
        ]
        
        return score, reasoning, failure_modes[:2]
    
    def _analyze_technical_feasibility(
        self, concept: str, perspective: Perspective
    ) -> Tuple[int, str, List[str]]:
        """Analyze technical feasibility from domain expert perspective"""
        
        red_flags = []
        green_flags = []
        
        # Complexity indicators
        if any(word in concept for word in ["ai", "machine learning", "blockchain", "quantum"]):
            red_flags.append("High technical complexity and risk")
        if any(word in concept for word in ["simple", "existing technology", "proven stack"]):
            green_flags.append("Leverages proven technology")
        
        # Team capability
        if any(word in concept for word in ["experienced", "technical team", "built before"]):
            green_flags.append("Team appears technically capable")
        else:
            red_flags.append("Team technical capability unclear")
        
        # Dependencies
        if any(word in concept for word in ["api", "integration", "dependent on"]):
            red_flags.append("Reliant on external dependencies")
        
        score = 6
        score += len(green_flags) * 2
        score -= len(red_flags) * 1.5
        score = max(1, min(10, score))
        
        reasoning = f"From {perspective.value} view: "
        if score >= 7:
            reasoning += "Technical approach appears feasible. "
        elif score >= 5:
            reasoning += "Technical execution has moderate risk. "
        else:
            reasoning += "Significant technical challenges identified. "
        
        if green_flags:
            reasoning += f"Advantages: {', '.join(green_flags)}. "
        if red_flags:
            reasoning += f"Risks: {', '.join(red_flags)}."
        
        failure_modes = [
            "Technology doesn't perform as expected in production",
            "Development timeline exceeds estimates by 2-3x",
            "Key technical assumptions prove incorrect",
            "Inability to hire specialized talent needed"
        ]
        
        return score, reasoning, failure_modes[:2]
    
    def _analyze_unit_economics(
        self, concept: str, perspective: Perspective
    ) -> Tuple[int, str, List[str]]:
        """Analyze unit economics from VC skeptic perspective"""
        
        red_flags = []
        green_flags = []
        
        # Revenue model
        if any(word in concept for word in ["subscription", "recurring", "saas", "mrr"]):
            green_flags.append("Recurring revenue model")
        if any(word in concept for word in ["free", "freemium", "ad-supported"]):
            red_flags.append("Monetization path unclear or challenging")
        
        # Margin profile
        if any(word in concept for word in ["software", "digital", "platform", "marketplace"]):
            green_flags.append("High-margin business model potential")
        if any(word in concept for word in ["hardware", "physical", "inventory", "logistics"]):
            red_flags.append("Low-margin operations with high overhead")
        
        # Scalability
        if any(word in concept for word in ["manual", "human-intensive", "service"]):
            red_flags.append("Unit economics may not improve with scale")
        if any(word in concept for word in ["automated", "self-service", "viral"]):
            green_flags.append("Economics improve with scale")
        
        score = 5
        score += len(green_flags) * 2
        score -= len(red_flags) * 2
        score = max(1, min(10, score))
        
        reasoning = f"From {perspective.value} view: "
        if score >= 7:
            reasoning += "Unit economics show promise for profitability. "
        elif score >= 5:
            reasoning += "Unit economics need significant improvement. "
        else:
            reasoning += "Fundamental unit economics concerns. "
        
        if green_flags:
            reasoning += f"Positive indicators: {', '.join(green_flags)}. "
        if red_flags:
            reasoning += f"Warning signs: {', '.join(red_flags)}."
        
        failure_modes = [
            "CAC never achieves acceptable payback period",
            "Gross margins compressed by competition",
            "Hidden costs emerge that destroy unit economics",
            "Churn rates higher than sustainable threshold"
        ]
        
        return score, reasoning, failure_modes[:2]
    
    def _analyze_competitive_moats(
        self, concept: str, perspective: Perspective
    ) -> Tuple[int, str, List[str]]:
        """Analyze competitive moats from competitor perspective"""
        
        red_flags = []
        green_flags = []
        
        # Defensibility
        if any(word in concept for word in ["patent", "proprietary", "network effect", "brand"]):
            green_flags.append("Defensible competitive advantages")
        else:
            red_flags.append("No clear defensible moats identified")
        
        # Switching costs
        if any(word in concept for word in ["integration", "migration", "embedded", "workflow"]):
            green_flags.append("High customer switching costs")
        if any(word in concept for word in ["easy to switch", "commodity"]):
            red_flags.append("Low switching costs enable competition")
        
        # Market position
        if any(word in concept for word in ["first mover", "only", "unique"]):
            green_flags.append("Early market position")
        if any(word in concept for word in ["crowded", "competitive", "many players"]):
            red_flags.append("Intensely competitive landscape")
        
        # Data/scale advantages
        if any(word in concept for word in ["data", "network", "marketplace", "platform"]):
            green_flags.append("Potential for scale-based advantages")
        
        score = 4  # Default skeptical on moats
        score += len(green_flags) * 2.5
        score -= len(red_flags) * 2
        score = max(1, min(10, score))
        
        reasoning = f"From {perspective.value} view: "
        if score >= 7:
            reasoning += "Defensible moats identified, but must be proven. "
        elif score >= 5:
            reasoning += "Moats are weak and easily replicated. "
        else:
            reasoning += "No sustainable competitive advantages. "
        
        if green_flags:
            reasoning += f"Potential moats: {', '.join(green_flags)}. "
        if red_flags:
            reasoning += f"Vulnerabilities: {', '.join(red_flags)}."
        
        failure_modes = [
            "Well-funded competitor copies and outspends you",
            "Incumbent leverages existing customer base to enter market",
            "Technology advantage proves temporary and easily replicated",
            "Network effects fail to materialize at scale"
        ]
        
        return score, reasoning, failure_modes[:2]
    
    def _analyze_scaling_bottlenecks(
        self, concept: str, perspective: Perspective
    ) -> Tuple[int, str, List[str]]:
        """Analyze scaling bottlenecks from domain expert perspective"""
        
        red_flags = []
        green_flags = []
        
        # Operational complexity
        if any(word in concept for word in ["complex", "custom", "bespoke", "manual"]):
            red_flags.append("High operational complexity limits scale")
        if any(word in concept for word in ["automated", "standardized", "self-service"]):
            green_flags.append("Operations designed for scale")
        
        # Resource constraints
        if any(word in concept for word in ["specialized", "expert", "consultant"]):
            red_flags.append("Dependent on scarce specialized resources")
        if any(word in concept for word in ["platform", "tools", "enabling"]):
            green_flags.append("Enables scale through platform approach")
        
        # Geographic/regulatory
        if any(word in concept for word in ["local", "regulated", "licensed", "compliance"]):
            red_flags.append("Geographic or regulatory barriers to scale")
        if any(word in concept for word in ["global", "cloud", "distributed"]):
            green_flags.append("Geographic expansion potential")
        
        score = 5
        score += len(green_flags) * 2
        score -= len(red_flags) * 2
        score = max(1, min(10, score))
        
        reasoning = f"From {perspective.value} view: "
        if score >= 7:
            reasoning += "Scaling path appears relatively clear. "
        elif score >= 5:
            reasoning += "Significant scaling challenges ahead. "
        else:
            reasoning += "Fundamental scaling limitations. "
        
        if green_flags:
            reasoning += f"Scale enablers: {', '.join(green_flags)}. "
        if red_flags:
            reasoning += f"Bottlenecks: {', '.join(red_flags)}."
        
        failure_modes = [
            "Quality degradation as company scales",
            "Infrastructure costs grow faster than revenue",
            "Unable to maintain culture and execution quality",
            "Supply chain or operational constraints hit hard limits"
        ]
        
        return score, reasoning, failure_modes[:2]
    
    def _make_decision(
        self, overall_score: float, dimension_scores: List[DimensionScore]
    ) -> Decision:
        """Make kill/proceed decision based on scores"""
        
        # Check for any dimension with critically low score
        min_score = min(s.score for s in dimension_scores)
        critically_low = [s for s in dimension_scores if s.score <= 3]
        
        # Strong proceed: high overall, no major weaknesses
        if overall_score >= 8 and min_score >= 6:
            return Decision.STRONG_PROCEED
        
        # Proceed: good overall, acceptable minimum
        if overall_score >= 7 and min_score >= 4:
            return Decision.PROCEED
        
        # Proceed with caution: moderate scores or one weak dimension
        if overall_score >= 6 and min_score >= 3:
            return Decision.PROCEED_WITH_CAUTION
        
        # Proceed with caution: decent overall but needs work
        if overall_score >= 5 and len(critically_low) <= 1:
            return Decision.PROCEED_WITH_CAUTION
        
        # Kill: multiple critical failures or very low overall
        return Decision.KILL
    
    def _synthesize_refinements(
        self, 
        concept: str, 
        dimension_scores: List[DimensionScore],
        decision: Decision
    ) -> Tuple[str, List[str]]:
        """Synthesize refined concept and key pivots based on evaluation"""
        
        pivots = []
        
        # Identify weakest dimensions
        weak_dimensions = [s for s in dimension_scores if s.score < 6]
        
        for dim_score in weak_dimensions:
            if "Market Viability" in dim_score.dimension:
                pivots.append(
                    "Narrow focus to specific high-value customer segment to prove market fit"
                )
            elif "Technical Feasibility" in dim_score.dimension:
                pivots.append(
                    "Start with MVP using existing tools/APIs to reduce technical risk"
                )
            elif "Unit Economics" in dim_score.dimension:
                pivots.append(
                    "Restructure pricing model to improve margins and customer LTV"
                )
            elif "Competitive Moats" in dim_score.dimension:
                pivots.append(
                    "Build network effects or data moat from day one as core strategy"
                )
            elif "Scaling Bottlenecks" in dim_score.dimension:
                pivots.append(
                    "Redesign operations for automation and standardization before scaling"
                )
        
        # Add general pivots based on decision
        if decision == Decision.KILL:
            pivots.append("Consider fundamental pivot to different problem or market")
        elif decision == Decision.PROCEED_WITH_CAUTION:
            pivots.append("De-risk before significant investment by validating key assumptions")
        
        # Generate refined concept
        if decision == Decision.KILL:
            refined = f"KILL: {concept} - Fundamental issues require complete rethink."
        else:
            refined = concept
            if pivots:
                refined += " PIVOT: " + " AND ".join(pivots[:2])
        
        return refined, pivots[:3] if pivots else ["Continue current approach with vigilant monitoring"]
    
    def _generate_experiments(
        self, concept: str, dimension_scores: List[DimensionScore]
    ) -> List[Experiment]:
        """Generate 3 validation experiments to test critical assumptions"""
        
        experiments = []
        weak_dimensions = sorted(dimension_scores, key=lambda x: x.score)[:3]
        
        for dim_score in weak_dimensions:
            if "Market Viability" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Customer Discovery Sprint",
                    hypothesis="Target customers have urgent need and willingness to pay",
                    method="Interview 20-30 target customers, present concept, measure genuine interest and ask for prepayment/LOI",
                    success_criteria="50%+ express strong interest, 20%+ willing to prepay or sign LOI",
                    estimated_cost="$500-2000 (time + incentives)",
                    estimated_time="2-3 weeks"
                ))
            elif "Technical Feasibility" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Technical Proof of Concept",
                    hypothesis="Core technology can deliver promised value at acceptable cost/performance",
                    method="Build minimal prototype of hardest technical component, measure performance and cost",
                    success_criteria="Prototype achieves 80%+ of promised capability within 2x cost budget",
                    estimated_cost="$2000-10000 (developer time)",
                    estimated_time="2-4 weeks"
                ))
            elif "Unit Economics" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Economics Model Stress Test",
                    hypothesis="Unit economics are profitable at scale with realistic assumptions",
                    method="Build detailed financial model with conservative assumptions, test sensitivity to key variables",
                    success_criteria="Positive unit economics within 12 months, LTV/CAC > 3, payback < 18 months",
                    estimated_cost="$500-1000 (analysis time)",
                    estimated_time="1 week"
                ))
            elif "Competitive Moats" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Competitive Differentiation Test",
                    hypothesis="Our unique value proposition is defensible and meaningful to customers",
                    method="A/B test our pitch vs competitor alternatives with target customers",
                    success_criteria="60%+ choose our approach when presented with alternatives",
                    estimated_cost="$1000-3000 (testing + tools)",
                    estimated_time="2 weeks"
                ))
            elif "Scaling Bottlenecks" in dim_score.dimension:
                experiments.append(Experiment(
                    title="Scaling Simulation",
                    hypothesis="Operations and costs scale sub-linearly with customer growth",
                    method="Model operational requirements at 10x and 100x current/projected scale",
                    success_criteria="Variable costs < 30% of revenue at scale, no hard bottlenecks identified",
                    estimated_cost="$500-2000 (planning time)",
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
    
    def _identify_critical_risks(
        self, dimension_scores: List[DimensionScore]
    ) -> List[str]:
        """Identify top critical risks from failure modes"""
        
        risks = []
        for dim_score in dimension_scores:
            if dim_score.score < 6:
                risks.extend([
                    f"[{dim_score.dimension}] {fm}" 
                    for fm in dim_score.failure_modes
                ])
        
        return risks[:5] if risks else ["No critical risks identified"]


def format_output(result: EvaluationResult) -> str:
    """Format evaluation result for display"""
    
    output = []
    output.append("\n" + "=" * 70)
    output.append("🔥 CRUCIBLE EVALUATION REPORT")
    output.append("=" * 70)
    output.append(f"\nOriginal Concept:\n{result.original_concept}\n")
    
    output.append("\n" + "-" * 70)
    output.append("📊 DIMENSION SCORES (with Adversarial Perspectives)")
    output.append("-" * 70)
    
    for score in result.dimension_scores:
        output.append(f"\n{score.dimension}: {score.score}/10 [{score.perspective}]")
        output.append(f"  Reasoning: {score.reasoning}")
        output.append(f"  Failure Modes:")
        for fm in score.failure_modes:
            output.append(f"    - {fm}")
    
    output.append(f"\n{'=' * 70}")
    output.append(f"Overall Score: {result.overall_score:.1f}/10")
    
    # Decision with visual indicator
    decision_icons = {
        Decision.KILL: "❌",
        Decision.PROCEED_WITH_CAUTION: "⚠️",
        Decision.PROCEED: "✓",
        Decision.STRONG_PROCEED: "✓✓"
    }
    icon = decision_icons.get(result.decision, "?")
    output.append(f"\n{icon} DECISION: {result.decision.value}")
    output.append("=" * 70)
    
    output.append(f"\n\n🎯 REFINED CONCEPT:\n{result.refined_concept}\n")
    
    output.append("\n" + "-" * 70)
    output.append("🔄 KEY PIVOTS RECOMMENDED")
    output.append("-" * 70)
    for i, pivot in enumerate(result.key_pivots, 1):
        output.append(f"{i}. {pivot}")
    
    output.append("\n" + "-" * 70)
    output.append("🧪 VALIDATION EXPERIMENTS (Top 3)")
    output.append("-" * 70)
    
    for i, exp in enumerate(result.validation_experiments, 1):
        output.append(f"\nExperiment {i}: {exp.title}")
        output.append(f"  Hypothesis: {exp.hypothesis}")
        output.append(f"  Method: {exp.method}")
        output.append(f"  Success Criteria: {exp.success_criteria}")
        output.append(f"  Cost: {exp.estimated_cost}")
        output.append(f"  Time: {exp.estimated_time}")
    
    output.append("\n" + "-" * 70)
    output.append("⚠️  CRITICAL RISKS")
    output.append("-" * 70)
    for risk in result.critical_risks:
        output.append(f"  - {risk}")
    
    output.append("\n" + "=" * 70)
    output.append("Weak ideas die here so strong ones survive. 🔥")
    output.append("=" * 70 + "\n")
    
    return "\n".join(output)


def main():
    """Main entry point for CRUCIBLE CLI"""
    
    if len(sys.argv) < 2:
        print("Usage: python crucible.py <startup_concept>")
        print("\nExample:")
        print('  python crucible.py "AI-powered fitness app that creates personalized workout plans"')
        sys.exit(1)
    
    concept = " ".join(sys.argv[1:])
    
    evaluator = CrucibleEvaluator()
    result = evaluator.evaluate(concept)
    
    print(format_output(result))
    
    # Also save to JSON for programmatic use
    output_file = "crucible_evaluation.json"
    with open(output_file, 'w') as f:
        # Convert dataclasses to dict
        result_dict = asdict(result)
        result_dict['decision'] = result.decision.value
        json.dump(result_dict, f, indent=2)
    
    print(f"📄 Detailed results saved to: {output_file}")
    
    # Exit code based on decision
    if result.decision == Decision.KILL:
        sys.exit(1)
    elif result.decision == Decision.PROCEED_WITH_CAUTION:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
