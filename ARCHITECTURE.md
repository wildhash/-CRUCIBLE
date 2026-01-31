# CRUCIBLE Multi-Model Architecture

## Overview

CRUCIBLE v2.0 transforms startup concept evaluation from a single-agent rule-based system into a **multi-model adversarial refinement engine** where 7 specialized AI models work in parallel to stress-test ideas from different perspectives.

## Architecture Layers

### 1. Orchestration Layer (`agents/orchestrator.py`)

The `CrucibleOrchestrator` coordinates the three-phase evaluation process:

**Phase 1: Parallel Model Evaluation**
- Launches all 7 models simultaneously
- Each model independently evaluates the concept across 5 dimensions
- Returns `ModelEvaluation` objects with scores, failure modes, and pivots

**Phase 2: Cross-Model Debate**
- Analyzes score divergence across models
- Identifies dimensions where models disagree (>3 point spread)
- Generates debate points highlighting disagreements

**Phase 3: Consensus Synthesis**
- Calculates weighted consensus scores (models have different weights)
- Generates unified pivots from all models' suggestions
- Creates validation experiments based on weakest dimensions
- Identifies minority reports when models strongly disagree

### 2. Model Layer

#### Base Evaluator (`agents/base_evaluator.py`)

Abstract base class defining the evaluator interface:

```python
class BaseEvaluator(ABC):
    @abstractmethod
    async def evaluate(self, concept: str, dimensions: List[str]) -> ModelEvaluation:
        pass
```

#### Mock Evaluator (Fallback)

When API keys are not configured, mock evaluators use sophisticated rule-based analysis:

- Keyword-based scoring across dimensions
- Simulates each model's perspective (VC skeptic, domain expert, etc.)
- Low confidence scores (30%) to indicate mock evaluation
- Still provides valuable analysis without API costs

#### Real Model Evaluators (Future)

Planned implementations for each AI provider:
- `ClaudeEvaluator` - Anthropic Claude API
- `GPTEvaluator` - OpenAI GPT API
- `GeminiEvaluator` - Google Gemini API
- `DeepSeekEvaluator` - DeepSeek API
- `GrokEvaluator` - xAI Grok API
- `KimiEvaluator` - Moonshot Kimi API
- `QwenEvaluator` - Alibaba Qwen API

### 3. Model Registry (`agents/evaluators/__init__.py`)

Centralized configuration for all models:

```python
EVALUATOR_MODELS = {
    "claude_opus": {
        "role": "deep_reasoning_critic",
        "focus": ["business_model_nuance", "ethical_risks", "long_term_viability"],
        "api": "anthropic",
        "model": "claude-opus-4-5-20251101",
        "weight": 1.5,  # Trusted model gets higher weight
        "description": "Senior partner conducting deep diligence"
    },
    # ... 6 more models
}
```

**Model Weights**:
- Claude Opus: 1.5 (highest trust)
- GPT-o3: 1.3
- DeepSeek R1: 1.2
- Grok: 1.1
- Gemini Flash: 1.0
- Qwen: 1.0
- Kimi: 0.8 (specialized APAC focus)

**Dimension-Model Priority Mapping**:

Maps each dimension to models best suited for that evaluation:

```python
DIMENSION_MODEL_PRIORITY = {
    "Market Viability": ["gpt_o3", "gemini_flash", "claude_opus"],
    "Technical Feasibility": ["deepseek_r1", "claude_opus", "grok"],
    "Unit Economics": ["qwen", "gpt_o3", "claude_opus"],
    "Competitive Moats": ["gpt_o3", "grok", "claude_opus"],
    "Scaling Bottlenecks": ["deepseek_r1", "kimi", "claude_opus"]
}
```

### 4. Prompt Layer (`prompts/evaluator_prompts.py`)

Each model has a specialized system prompt:

**Claude Opus** (Deep Reasoning Critic):
- Focus: Business model nuance, ethical risks, long-term viability
- Tone: Intellectually rigorous but fair
- Approach: Second and third-order consequences

**GPT-o3** (VC Skeptic):
- Focus: TAM validation, competitive threats, exit strategy
- Tone: Aggressive skepticism
- Approach: Find the fatal flaw

**DeepSeek R1** (Technical Auditor):
- Focus: Architecture feasibility, scaling bottlenecks, tech debt
- Tone: Demand specificity
- Approach: No hand-waving about "AI" or "blockchain"

**Grok** (Contrarian):
- Focus: Black swan risks, unconventional angles, paradigm shifts
- Tone: Provocative but substantive
- Approach: Challenge consensus wisdom

**Gemini Flash** (Speed Analyst):
- Focus: Market research, competitive landscape, trends
- Tone: Data-driven, rapid
- Approach: Broad market intelligence

**Qwen** (Cost Optimizer):
- Focus: Unit economics, burn rate, capital efficiency
- Tone: Ruthless about financials
- Approach: Demand realistic numbers

**Kimi** (APAC Expansion):
- Focus: China market, regulatory landscape, localization
- Tone: Regional specialist
- Approach: Cross-border challenges

### 5. Data Models (`models/evaluation.py`)

Enhanced data structures for multi-model evaluation:

```python
@dataclass
class ModelEvaluation:
    """Single model's evaluation"""
    model_name: str
    role: str
    scores: Dict[str, int]  # dimension -> 1-10
    failure_modes: List[str]
    pivots_suggested: List[str]
    confidence: float  # 0.0-1.0
    dissenting_opinion: Optional[str]
    reasoning: str

@dataclass
class CrucibleVerdict:
    """Complete multi-model verdict"""
    consensus_score: float
    decision: Decision
    model_evaluations: List[ModelEvaluation]
    dimension_scores: List[DimensionScore]
    key_debates: List[str]
    unified_pivots: List[str]
    validation_experiments: List[Experiment]
    critical_risks: List[str]
    minority_report: Optional[str]
    refined_concept: str
```

## Consensus Algorithm

### Weighted Consensus Scoring

For each dimension:

1. Collect scores from all models that evaluated the dimension
2. Weight each score by: `model_weight × model_confidence`
3. Calculate weighted average: `Σ(score × weight) / Σ(weights)`
4. Round to nearest integer (1-10)

Example:
```
Dimension: Market Viability
- claude_opus: 8 × (1.5 × 0.85) = 10.2
- gpt_o3: 7 × (1.3 × 0.90) = 8.19
- gemini_flash: 8 × (1.0 × 0.75) = 6.0

Weighted Average = (10.2 + 8.19 + 6.0) / (1.275 + 1.17 + 0.75) = 7.6
Consensus Score: 8/10
```

### Debate Detection

Models are considered to be in "debate" when:

1. Score spread ≥ 3 points for a dimension
2. Example: Model A scores 8, Model B scores 4 → spread of 4
3. Flagged as: "Market Viability: Models disagree (range 4-8, avg 6.0)"

### Minority Report Generation

When a model's average score differs from consensus by ≥3 points:

1. Identify the dissenting model
2. Extract its reasoning and dissenting opinion
3. Include in verdict as: "Model X (role) strongly disagrees: Scored Y vs consensus Z"

### Decision Logic

```python
if consensus_score >= 8 and min_dimension >= 6:
    return STRONG_PROCEED
elif consensus_score >= 7 and min_dimension >= 4:
    return PROCEED
elif consensus_score >= 6 and min_dimension >= 3:
    return PROCEED_WITH_CAUTION
elif consensus_score >= 5 and critically_low_dimensions <= 1:
    return PROCEED_WITH_CAUTION
else:
    return KILL
```

## Dual-Mode Operation

### Multi-Model Mode (Default)

```bash
python3 crucible.py "concept" --mode=multi
```

1. Initialize `CrucibleOrchestrator`
2. Run async parallel evaluation
3. Synthesize consensus
4. Output multi-model report
5. Save JSON with model-by-model breakdown

### Legacy Mode

```bash
python3 crucible.py "concept" --mode=legacy
```

1. Initialize `CrucibleEvaluator` (original)
2. Run rule-based evaluation
3. Output single-agent report
4. Maintains backwards compatibility

### Automatic Fallback

If multi-model mode fails (missing dependencies, etc.):
- Automatically falls back to legacy mode
- User sees: "Multi-model evaluation failed... Falling back to legacy mode"

## Configuration (`config/models.yaml`)

```yaml
models:
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-opus-4-5-20251101
    enabled: false  # Set to true when API key available
    
orchestrator:
  use_mock: true  # Use mock evaluators by default
  max_parallel: 7
  timeout: 30
  min_confidence: 0.3
  
output:
  show_model_details: true
  show_debates: true
  show_minority_report: true
```

## Testing

### Test Coverage

18 new tests in `test_multimodel.py`:

**Multi-Model Architecture Tests**:
- Orchestrator initialization
- Mock evaluator functionality
- Parallel evaluation execution
- Full adversarial evaluation flow
- Consensus calculation
- Debate identification
- Decision logic
- Pivot synthesis
- Experiment generation
- Minority report generation
- Selective model evaluation

**Model Registry Tests**:
- All models configured
- Model configs complete
- Dimension-model priority mapping

**Data Model Tests**:
- ModelEvaluation creation
- CrucibleVerdict creation

**Prompt Tests**:
- Prompts exist for all models
- Prompts are not empty

### Running Tests

```bash
# Run multi-model tests
python3 test_multimodel.py

# Run all tests
python3 test_crucible.py
python3 test_multimodel.py
```

## Future Enhancements

### Phase 1: Real API Integrations
- Implement actual API calls to Claude, GPT, Gemini, etc.
- Add retry logic and error handling
- Implement rate limiting and cost controls

### Phase 2: Advanced Debate
- Actual cross-model debate rounds
- Models critique each other's evaluations
- Iterative refinement through debate

### Phase 3: Learning System
- Track historical evaluations
- Learn which models are most accurate over time
- Auto-adjust model weights based on performance

### Phase 4: Specialized Evaluators
- Industry-specific model configurations
- Custom prompts for different domains
- Fine-tuned models on historical startup data

## File Structure

```
-CRUCIBLE/
├── crucible.py              # Main CLI (dual-mode support)
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py      # Multi-model orchestration
│   ├── base_evaluator.py    # Base class + MockEvaluator
│   └── evaluators/
│       └── __init__.py      # Model registry
├── prompts/
│   ├── __init__.py
│   └── evaluator_prompts.py # Model-specific prompts
├── models/
│   ├── __init__.py
│   └── evaluation.py        # Enhanced data models
├── config/
│   └── models.yaml          # Configuration
└── test_multimodel.py       # Multi-model tests
```

## Performance Characteristics

### Mock Evaluator Mode (Default)
- **Latency**: ~5ms per model (35ms total for 7 models in parallel)
- **Cost**: $0
- **Quality**: Rule-based, consistent, no API failures
- **Confidence**: 30% (explicitly marked as mock)

### Real API Mode (When Configured)
- **Latency**: ~2-5s per model (parallel, so ~5s total)
- **Cost**: ~$0.10-0.50 per evaluation (varies by model)
- **Quality**: High, leverages actual AI reasoning
- **Confidence**: 70-95% (model-dependent)

## Summary

CRUCIBLE v2.0's multi-model architecture provides:

✅ **Comprehensive Evaluation**: 7 specialized models attack from different angles  
✅ **Parallel Processing**: Fast evaluation through async execution  
✅ **Consensus + Dissent**: Weighted consensus with minority reports  
✅ **Zero Setup**: Works immediately with mock evaluators  
✅ **Flexible Configuration**: Easy API key setup when ready  
✅ **Backwards Compatible**: Legacy mode preserved  
✅ **Well Tested**: 18 new tests covering all components  

The architecture balances immediate usability (mock mode) with future scalability (real API mode) while maintaining the core CRUCIBLE mission: **Weak ideas die here so strong ones survive. 🔥**
