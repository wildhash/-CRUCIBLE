# Using Real LLM API Evaluators

CRUCIBLE v2.0 supports both mock evaluators (rule-based, zero-setup) and real LLM API evaluators for production use.

## Quick Start

### Option 1: Mock Mode (Default - No Setup)

Works immediately without any API keys:

```bash
python3 crucible.py "Your startup concept"
```

### Option 2: Real LLM APIs (Production)

Enable real AI model evaluations by configuring API keys.

## Setup API Keys

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Keys (Environment Variables)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."
export DEEPSEEK_API_KEY="..."
export XAI_API_KEY="..."
```

### 3. Enable Real API Mode

Modify orchestrator initialization in `crucible.py` to use `use_mock=False`.

## Supported Models

| Model | Provider | Role | API Key Env Var |
|-------|----------|------|-----------------|
| Claude Opus | Anthropic | Deep Reasoning Critic | `ANTHROPIC_API_KEY` |
| GPT-4 | OpenAI | VC Skeptic | `OPENAI_API_KEY` |
| DeepSeek R1 | DeepSeek | Technical Auditor | `DEEPSEEK_API_KEY` |
| Grok | xAI | Contrarian | `XAI_API_KEY` |
| Gemini Flash | Google | Speed Analyst | `GOOGLE_API_KEY` |

## Cost Estimation

| Models Enabled | Estimated Cost | Latency |
|----------------|----------------|---------|
| Mock only | $0 | 5ms |
| 1-2 models | $0.01-0.05 | 2-5s |
| All 5 models | $0.30-0.80 | 5-8s |

## Error Handling

CRUCIBLE automatically falls back to mock evaluators when API keys are missing or errors occur.
