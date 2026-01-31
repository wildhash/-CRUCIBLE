"""
DeepSeek R1 Evaluator - Technical Auditor

Uses DeepSeek API to audit technical feasibility,
architecture scalability, and engineering complexity.
"""

import os
import json
import httpx
from typing import List, Dict
from agents.base_evaluator import BaseEvaluator
from models.evaluation import ModelEvaluation
from prompts.evaluator_prompts import DEEPSEEK_PROMPT


class DeepSeekEvaluator(BaseEvaluator):
    """
    DeepSeek R1 evaluator using DeepSeek API
    
    Role: Technical Auditor
    Focus: Architecture feasibility, scaling bottlenecks, tech debt
    """
    
    def __init__(self):
        super().__init__(
            model_name="deepseek_r1",
            role="technical_auditor",
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        self.timeout = 30.0
    
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Evaluate concept using DeepSeek R1
        
        Args:
            concept: Startup concept to evaluate
            dimensions: List of dimensions to score
            
        Returns:
            ModelEvaluation with DeepSeek's analysis
        """
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not set. Cannot use DeepSeek evaluator.")
        
        try:
            # Prepare the messages
            messages = [
                {
                    "role": "system",
                    "content": DEEPSEEK_PROMPT
                },
                {
                    "role": "user",
                    "content": f'Evaluate this startup concept from a technical perspective:\n\n"{concept}"\n\nProvide your evaluation in JSON format as specified.'
                }
            ]
            
            # Call DeepSeek API
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
                    confidence=parsed.get("confidence", 0.8),
                    dissenting_opinion=parsed.get("dissenting_opinion"),
                    reasoning=parsed.get("reasoning", "")[:500]
                )
                
        except httpx.HTTPError as e:
            raise RuntimeError(f"DeepSeek API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"DeepSeek evaluation failed: {str(e)}")
