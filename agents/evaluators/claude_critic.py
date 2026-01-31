"""
Claude Opus Evaluator - Deep Reasoning Critic

Uses Anthropic's Claude API for deep, rigorous evaluation
of business model nuance, ethical risks, and long-term viability.
"""

import os
import json
import httpx
from typing import List, Dict
from agents.base_evaluator import BaseEvaluator
from models.evaluation import ModelEvaluation
from prompts.evaluator_prompts import CLAUDE_OPUS_PROMPT


class ClaudeEvaluator(BaseEvaluator):
    """
    Claude Opus evaluator using Anthropic API
    
    Role: Deep Reasoning Critic
    Focus: Business model nuance, ethical risks, long-term viability
    """
    
    def __init__(self):
        super().__init__(
            model_name="claude_opus",
            role="deep_reasoning_critic",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-opus-4-5-20251101"
        self.timeout = 30.0
    
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        """
        Evaluate concept using Claude Opus
        
        Args:
            concept: Startup concept to evaluate
            dimensions: List of dimensions to score
            
        Returns:
            ModelEvaluation with Claude's analysis
        """
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set. Cannot use Claude evaluator.")
        
        try:
            # Prepare the prompt
            user_message = f"""Evaluate this startup concept:

"{concept}"

{CLAUDE_OPUS_PROMPT}

Provide your evaluation in JSON format as specified in the prompt."""

            # Call Anthropic API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 2048,
                        "messages": [
                            {
                                "role": "user",
                                "content": user_message
                            }
                        ]
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Extract content from response
                content = result["content"][0]["text"]
                
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
            raise RuntimeError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Claude evaluation failed: {str(e)}")
