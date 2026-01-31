"""
GPT-o3 Evaluator - VC Skeptic

Uses OpenAI's GPT-o3 API to attack concepts from a
battle-hardened VC perspective, finding fatal flaws.
"""

import os
import json
import httpx
from typing import List, Dict
from agents.base_evaluator import BaseEvaluator
from models.evaluation import ModelEvaluation
from prompts.evaluator_prompts import GPT_O3_PROMPT


class GPTEvaluator(BaseEvaluator):
    """
    GPT-o3 evaluator using OpenAI API
    
    Role: VC Skeptic
    Focus: Market size validation, competitive threats, exit strategy
    """
    
    def __init__(self):
        super().__init__(
            model_name="gpt_o3",
            role="vc_skeptic",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4"  # Using GPT-4 as o3 may not be available yet
        self.timeout = 30.0
    
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Evaluate concept using GPT-o3/GPT-4
        
        Args:
            concept: Startup concept to evaluate
            dimensions: List of dimensions to score
            
        Returns:
            ModelEvaluation with GPT's analysis
        """
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Cannot use GPT evaluator.")
        
        try:
            # Prepare the messages
            messages = [
                {
                    "role": "system",
                    "content": GPT_O3_PROMPT
                },
                {
                    "role": "user",
                    "content": f'Evaluate this startup concept:\n\n"{concept}"\n\nProvide your evaluation in the JSON format specified.'
                }
            ]
            
            # Call OpenAI API
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
                        "temperature": 0.7,
                        "max_tokens": 2048,
                        "response_format": {"type": "json_object"}
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
                    confidence=parsed.get("confidence", 0.85),
                    dissenting_opinion=parsed.get("dissenting_opinion"),
                    reasoning=parsed.get("reasoning", "")[:500]
                )
                
        except httpx.HTTPError as e:
            raise RuntimeError(f"GPT API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"GPT evaluation failed: {str(e)}")
