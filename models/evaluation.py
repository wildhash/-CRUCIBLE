"""
Enhanced evaluation data models for multi-model CRUCIBLE
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from enum import Enum


class Decision(Enum):
    """Kill or proceed decision for a startup concept"""
    KILL = "KILL"
    PROCEED_WITH_CAUTION = "PROCEED_WITH_CAUTION"
    PROCEED = "PROCEED"
    STRONG_PROCEED = "STRONG_PROCEED"


@dataclass
class ModelEvaluation:
    """Evaluation from a single AI model"""
    model_name: str
    role: str
    scores: Dict[str, int]  # dimension -> 1-10
    failure_modes: List[str]
    pivots_suggested: List[str]
    confidence: float  # 0.0-1.0
    dissenting_opinion: Optional[str] = None
    reasoning: str = ""


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension"""
    dimension: str
    score: int  # 1-10
    reasoning: str
    failure_modes: List[str]
    perspective: str
    model_evaluations: List[ModelEvaluation] = field(default_factory=list)


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
class CrucibleVerdict:
    """
    Complete multi-model evaluation verdict
    Combines consensus from all models with dissenting opinions
    """
    original_concept: str
    consensus_score: float
    decision: Decision
    model_evaluations: List[ModelEvaluation]
    dimension_scores: List[DimensionScore]
    key_debates: List[str]  # Where models disagreed
    unified_pivots: List[str]
    validation_experiments: List[Experiment]
    critical_risks: List[str]
    minority_report: Optional[str] = None  # Dissenting model's case
    refined_concept: str = ""
    
    def to_legacy_result(self):
        """Convert to legacy EvaluationResult format for backwards compatibility"""
        # Import here to avoid circular dependency
        from crucible import EvaluationResult
        
        return EvaluationResult(
            original_concept=self.original_concept,
            dimension_scores=self.dimension_scores,
            overall_score=self.consensus_score,
            decision=self.decision,
            refined_concept=self.refined_concept,
            key_pivots=self.unified_pivots,
            validation_experiments=self.validation_experiments,
            critical_risks=self.critical_risks
        )
