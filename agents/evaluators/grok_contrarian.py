"""
Grok Evaluator - Contrarian

Uses xAI's Grok API to find unconventional risks,
black swan events, and paradigm shifts.
"""

import os
import json
import httpx
from typing import List, Dict
from agents.base_evaluator import BaseEvaluator
from models.evaluation import ModelEvaluation
from prompts.evaluator_prompts import GROK_PROMPT


class GrokEvaluator(BaseEvaluator):
    """
    Grok evaluator using xAI API
    
    Role: Contrarian
    Focus: Unconventional angles, black swan risks, paradigm shifts
    """
    
    def __init__(self):
        super().__init__(
            model_name="grok",
            role="contrarian",
            api_key=os.getenv("XAI_API_KEY")
        )
        self.api_url = "https://api.x.ai/v1/chat/completions"
        self.model = "grok-beta"
        self.timeout = 30.0
    
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Evaluate concept using Grok
        
        Args:
            concept: Startup concept to evaluate
            dimensions: List of dimensions to score
            
        Returns:
            ModelEvaluation with Grok's contrarian analysis
        """
        if not self.api_key:
            raise ValueError("XAI_API_KEY not set. Cannot use Grok evaluator.")
        
        try:
            # Prepare the messages
            messages = [
                {
                    "role": "system",
                    "content": GROK_PROMPT
                },
                {
                    "role": "user",
                    "content": f'Evaluate this startup concept from a contrarian perspective:\n\n"{concept}"\n\nProvide your evaluation in JSON format as specified.'
                }
            ]
            
            # Call xAI API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.8,
                        "max_tokens": 2048
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Extract content from response
                content = result["choices"][0]["message"]["content"]
                
                # Parse the JSON response
                parsed = self._parse_model_response(content)
                
                return ModelEvaluation(
                    model_name=self.model_name,
                    role=self.role,
                    scores=self._validate_scores(parsed.get("scores", {})),
                    failure_modes=parsed.get("failure_modes", [])[:5],
                    pivots_suggested=parsed.get("pivots", [])[:3],
                    confidence=parsed.get("confidence", 0.75),
                    dissenting_opinion=parsed.get("dissenting_opinion"),
                    reasoning=parsed.get("reasoning", "")[:500]
                )
                
        except httpx.HTTPError as e:
            raise RuntimeError(f"Grok API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Grok evaluation failed: {str(e)}")
