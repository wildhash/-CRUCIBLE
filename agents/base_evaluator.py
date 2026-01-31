"""
Base evaluator interface for all AI model evaluators
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from models.evaluation import ModelEvaluation


class BaseEvaluator(ABC):
    """
    Base class for all model evaluators
    Each model implements this interface to evaluate startup concepts
    """
    
    def __init__(self, model_name: str, role: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.role = role
        self.api_key = api_key or os.getenv(f"{api_key}_API_KEY")
        
    @abstractmethod
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Evaluate a startup concept
        
        Args:
            concept: The startup concept description
            dimensions: List of dimensions to evaluate
            
        Returns:
            ModelEvaluation with scores and analysis
        """
        pass
    
    def _parse_model_response(self, response: str) -> Dict:
        """
        Parse JSON response from model
        
        Args:
            response: Raw response from model
            
        Returns:
            Parsed dictionary
        """
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                response = response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                response = response[start:end].strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Return default structure if parsing fails
            return {
                "scores": {},
                "failure_modes": ["Failed to parse model response"],
                "pivots": [],
                "confidence": 0.5,
                "reasoning": f"Error parsing response: {str(e)}"
            }
    
    def _validate_scores(self, scores: Dict[str, int]) -> Dict[str, int]:
        """Ensure all scores are in valid range 1-10"""
        return {
            dim: max(1, min(10, score))
            for dim, score in scores.items()
        }


class MockEvaluator(BaseEvaluator):
    """
    Mock evaluator for testing and fallback when APIs are unavailable
    Uses rule-based scoring similar to original CRUCIBLE
    """
    
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Provide mock evaluation based on keyword analysis
        """
        concept_lower = concept.lower()
        
        scores = {}
        for dim in dimensions:
            # Simple rule-based scoring
            score = 5  # baseline
            
            if "Market Viability" in dim:
                if any(w in concept_lower for w in ["revenue", "customers", "validated"]):
                    score += 2
                if any(w in concept_lower for w in ["enterprise", "global", "platform"]):
                    score += 1
                if "niche" in concept_lower or "small" in concept_lower:
                    score -= 2
                    
            elif "Technical Feasibility" in dim:
                if any(w in concept_lower for w in ["proven", "existing", "simple"]):
                    score += 2
                if any(w in concept_lower for w in ["ai", "blockchain", "quantum"]):
                    score -= 2
                    
            elif "Unit Economics" in dim:
                if any(w in concept_lower for w in ["saas", "subscription", "recurring"]):
                    score += 2
                if any(w in concept_lower for w in ["free", "ad-supported"]):
                    score -= 2
                    
            elif "Competitive Moats" in dim:
                if any(w in concept_lower for w in ["network", "proprietary", "patent"]):
                    score += 2
                if "commodity" in concept_lower:
                    score -= 2
                    
            elif "Scaling Bottlenecks" in dim:
                if any(w in concept_lower for w in ["automated", "platform", "cloud"]):
                    score += 2
                if any(w in concept_lower for w in ["manual", "custom"]):
                    score -= 2
            
            scores[dim] = max(1, min(10, score))
        
        return ModelEvaluation(
            model_name=self.model_name,
            role=self.role,
            scores=scores,
            failure_modes=[
                f"Mock evaluation - API not available for {self.model_name}",
                "Scores based on keyword analysis only"
            ],
            pivots_suggested=[
                "Enable API access for deeper multi-model analysis",
                "Provide more details in concept description"
            ],
            confidence=0.3,  # Low confidence for mock
            reasoning=f"Mock {self.role} evaluation using rule-based analysis (API unavailable)"
        )
