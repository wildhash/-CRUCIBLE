"""
Model registry and configuration for CRUCIBLE evaluators
"""

EVALUATOR_MODELS = {
    "claude_opus": {
        "role": "deep_reasoning_critic",
        "focus": ["business_model_nuance", "ethical_risks", "long_term_viability"],
        "api": "anthropic",
        "model": "claude-opus-4-5-20251101",
        "weight": 1.5,  # Higher weight for more trusted models
        "description": "Senior partner conducting deep diligence"
    },
    "gpt_o3": {
        "role": "vc_skeptic", 
        "focus": ["market_size_validation", "competitive_threats", "exit_strategy"],
        "api": "openai",
        "model": "o3",
        "weight": 1.3,
        "description": "Battle-hardened VC who has seen 10,000 pitches"
    },
    "gemini_flash": {
        "role": "speed_analyst",
        "focus": ["market_research", "competitive_landscape", "trend_analysis"],
        "api": "google",
        "model": "gemini-2.5-flash",
        "weight": 1.0,
        "description": "Fast market analyst with broad knowledge"
    },
    "deepseek_r1": {
        "role": "technical_auditor",
        "focus": ["architecture_feasibility", "scaling_bottlenecks", "tech_debt"],
        "api": "deepseek",
        "model": "deepseek-r1",
        "weight": 1.2,
        "description": "Principal engineer auditing technical feasibility"
    },
    "grok": {
        "role": "contrarian",
        "focus": ["unconventional_angles", "black_swan_risks", "paradigm_shifts"],
        "api": "xai",
        "model": "grok-3",
        "weight": 1.1,
        "description": "Contrarian thinker finding unconventional risks"
    },
    "kimi": {
        "role": "apac_expansion",
        "focus": ["china_market", "regulatory_compliance", "localization"],
        "api": "moonshot",
        "model": "kimi",
        "weight": 0.8,
        "description": "APAC market specialist"
    },
    "qwen": {
        "role": "cost_optimizer",
        "focus": ["unit_economics", "burn_rate", "capital_efficiency"],
        "api": "alibaba",
        "model": "qwen",
        "weight": 1.0,
        "description": "Cost optimization specialist"
    }
}

# Dimension to model mapping - which models are best for each dimension
DIMENSION_MODEL_PRIORITY = {
    "Market Viability": ["gpt_o3", "gemini_flash", "claude_opus"],
    "Technical Feasibility": ["deepseek_r1", "claude_opus", "grok"],
    "Unit Economics": ["qwen", "gpt_o3", "claude_opus"],
    "Competitive Moats": ["gpt_o3", "grok", "claude_opus"],
    "Scaling Bottlenecks": ["deepseek_r1", "kimi", "claude_opus"]
}
