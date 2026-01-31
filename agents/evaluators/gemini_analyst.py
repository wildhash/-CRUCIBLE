"""
Gemini Flash Evaluator - Speed Analyst

Uses Google's Gemini API for fast market research,
competitive landscape analysis, and trend validation.
"""

import os
import json
import httpx
from typing import List, Dict
from agents.base_evaluator import BaseEvaluator
from models.evaluation import ModelEvaluation
from prompts.evaluator_prompts import GEMINI_FLASH_PROMPT


class GeminiEvaluator(BaseEvaluator):
    """
    Gemini Flash evaluator using Google API
    
    Role: Speed Analyst
    Focus: Market research, competitive landscape, trend analysis
    """
    
    def __init__(self):
        super().__init__(
            model_name="gemini_flash",
            role="speed_analyst",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.model = "gemini-2.0-flash-exp"
        self.timeout = 30.0
    
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Evaluate concept using Gemini Flash
        
        Args:
            concept: Startup concept to evaluate
            dimensions: List of dimensions to score
            
        Returns:
            ModelEvaluation with Gemini's analysis
        """
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set. Cannot use Gemini evaluator.")
        
        try:
            # Prepare the prompt
            prompt = f"""{GEMINI_FLASH_PROMPT}

Evaluate this startup concept:

"{concept}"

Provide your evaluation in JSON format as specified in the system prompt."""

            # Call Gemini API
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    api_url,
                    headers={
                        "Content-Type": "application/json",
                    },
                    json={
                        "contents": [{
                            "parts": [{
                                "text": prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 2048,
                        }
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Extract content from response
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                
                # Parse the JSON response
                parsed = self._parse_model_response(content)
                
                return ModelEvaluation(
                    model_name=self.model_name,
                    role=self.role,
                    scores=self._validate_scores(parsed.get("scores", {})),
                    failure_modes=parsed.get("failure_modes", [])[:5],
                    pivots_suggested=parsed.get("pivots", [])[:3],
                    confidence=parsed.get("confidence", 0.8),
                    dissenting_opinion=parsed.get("dissenting_opinion"),
                    reasoning=parsed.get("reasoning", "")[:500]
                )
                
        except httpx.HTTPError as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Gemini evaluation failed: {str(e)}")
