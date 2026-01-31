#!/usr/bin/env python3
"""
Demo: Using Real LLM API Evaluators

This script demonstrates how to use CRUCIBLE with real LLM APIs.

Prerequisites:
1. pip install -r requirements.txt
2. Set API keys as environment variables

Usage:
    python3 demos/real_api_demo.py
"""

import os
import asyncio
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import CrucibleOrchestrator


async def demo_real_apis():
    """Demonstrate real API evaluation"""
    
    print("=" * 70)
    print("🔥 CRUCIBLE - Real LLM API Demo")
    print("=" * 70)
    
    # Check which API keys are available
    api_keys = {
        "ANTHROPIC_API_KEY": "Claude Opus",
        "OPENAI_API_KEY": "GPT-4",
        "GOOGLE_API_KEY": "Gemini Flash",
        "DEEPSEEK_API_KEY": "DeepSeek R1",
        "XAI_API_KEY": "Grok"
    }
    
    print("\n📋 Checking API Keys:")
    available_models = []
    for key, model in api_keys.items():
        if os.getenv(key):
            print(f"  ✓ {model:15} - API key found")
            available_models.append(model)
        else:
            print(f"  ✗ {model:15} - API key missing (will use mock)")
    
    if not available_models:
        print("\n⚠️  No API keys found! Running in mock mode.")
        print("Set API keys to enable real AI evaluations:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        use_real = False
    else:
        print(f"\n✓ Found {len(available_models)} API key(s)")
        use_real = True
    
    # Initialize orchestrator
    print(f"\nInitializing {'REAL API' if use_real else 'MOCK'} mode...")
    orchestrator = CrucibleOrchestrator(use_mock=not use_real)
    
    # Concept to evaluate
    concept = "B2B SaaS platform for AI-powered code review at $99/month per dev"
    
    print(f"\nEvaluating: {concept}\n")
    
    # Run evaluation
    verdict = await orchestrator.run_adversarial_evaluation(concept)
    
    print(f"\n📊 Results: {verdict.consensus_score:.1f}/10 - {verdict.decision.value}")


if __name__ == "__main__":
    asyncio.run(demo_real_apis())
