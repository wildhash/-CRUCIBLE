# 🔥 CRUCIBLE

**Multi-model adversarial refinement engine that stress-tests startup concepts through collaborative AI debate until they're investor-ready.**

> *Weak ideas die here so strong ones survive.*

## What is CRUCIBLE?

CRUCIBLE is an **adversarial evaluation agent** that challenges startup concepts across 5 critical dimensions using **7 specialized AI models** working in parallel to provide comprehensive, multi-perspective analysis.

### The 5 Dimensions

1. **Market Viability** - Is there a real market? Will customers pay?
2. **Technical Feasibility** - Can it actually be built? What are the risks?
3. **Unit Economics** - Do the numbers work? Can it be profitable?
4. **Competitive Moats** - What prevents competitors from crushing you?
5. **Scaling Bottlenecks** - What breaks when you try to grow?

## 🆕 Multi-Model Architecture

CRUCIBLE v2.0 orchestrates **7 specialized AI models**, each attacking from a unique adversarial perspective:

- 🧠 **Claude Opus** (Deep Reasoning Critic) - Senior partner conducting deep diligence on business model nuance, ethical risks, and long-term viability
- 💰 **GPT-o3** (VC Skeptic) - Battle-hardened VC finding fatal flaws in market size, competitive threats, and exit strategy
- ⚡ **Gemini Flash** (Speed Analyst) - Fast market analyst providing broad market research and competitive landscape
- 🔧 **DeepSeek R1** (Technical Auditor) - Principal engineer auditing architecture feasibility and scaling bottlenecks
- 🎲 **Grok** (Contrarian) - Contrarian thinker finding unconventional angles and black swan risks
- 🌏 **Kimi** (APAC Expansion) - APAC market specialist for China market and regulatory compliance
- 💸 **Qwen** (Cost Optimizer) - Unit economics expert optimizing burn rate and capital efficiency

### How Multi-Model Evaluation Works

1. **Phase 1: Parallel Evaluation** - All 7 models evaluate independently in parallel
2. **Phase 2: Cross-Model Debate** - System identifies where models disagree (>3 point spread)
3. **Phase 3: Consensus Synthesis** - Weighted consensus with minority reports for dissenting opinions

After the gauntlet, CRUCIBLE synthesizes:

- ✅ **Consensus Decision** - KILL, PROCEED_WITH_CAUTION, PROCEED, or STRONG_PROCEED
- 🤖 **Model-by-Model Breakdown** - See how each model evaluated your concept
- ⚔️ **Key Debates** - Where models disagreed significantly
- 🎯 **Refined Concept** - Your idea, battle-tested and improved
- 🔄 **Unified Pivots** - Synthesized from all models' recommendations
- 🧪 **3 Validation Experiments** - Concrete tests to validate assumptions
- ⚠️ **Minority Report** - Dissenting model's case (when models disagree >3 points)

## Installation

No installation required! Just Python 3.7+

```bash
# Clone the repository
git clone https://github.com/wildhash/-CRUCIBLE.git
cd -CRUCIBLE

# Make it executable
chmod +x crucible.py
```

## Usage

### Multi-Model Mode (Default)

Run your concept through the **7-model adversarial gauntlet**:

```bash
python3 crucible.py "Your startup concept here"
# OR explicitly
python3 crucible.py "Your startup concept here" --mode=multi
```

### Legacy Mode

Use the original rule-based single-agent evaluation:

```bash
python3 crucible.py "Your startup concept here" --mode=legacy
```

### Example

```bash
python3 crucible.py "AI-powered fitness app that creates personalized workout plans using machine learning to analyze user performance and adapt in real-time"
```

## Configuration

### API Keys (Optional)

By default, CRUCIBLE uses **mock evaluators** (rule-based scoring) when API keys are not configured. This allows you to use CRUCIBLE immediately without any setup.

To enable **real AI model evaluations** with actual LLM APIs:

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Set API Keys

Configure API keys in `config/models.yaml`:

```yaml
models:
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    enabled: true
    
  openai:
    api_key: ${OPENAI_API_KEY}
    enabled: true
    
  google:
    api_key: ${GOOGLE_API_KEY}
    enabled: true
    
  deepseek:
    api_key: ${DEEPSEEK_API_KEY}
    enabled: true
    
  xai:
    api_key: ${XAI_API_KEY}
    enabled: true
```

Or set environment variables:

```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
export DEEPSEEK_API_KEY="your-key-here"
export XAI_API_KEY="your-key-here"
```

#### 3. Enable Real API Mode

Modify `crucible.py` to use real APIs:

```python
# In crucible.py, change:
orchestrator = CrucibleOrchestrator(use_mock=False)  # Enable real APIs
```

**See [docs/API_USAGE.md](docs/API_USAGE.md) for detailed API setup guide.**
```

**Note**: Even without API keys, CRUCIBLE provides valuable analysis using sophisticated rule-based mock evaluators that simulate each model's perspective.

## Example Output

### Multi-Model Output

```
🔥 CRUCIBLE MULTI-MODEL EVALUATION REPORT
======================================================================

Original Concept:
B2B SaaS platform with proven revenue

----------------------------------------------------------------------
🤖 MODEL EVALUATIONS (7 models)
----------------------------------------------------------------------

claude_opus (deep_reasoning_critic)
  Average Score: 7.2/10 | Confidence: 85.0%
  Scores: Market Viability: 8, Technical Feasibility: 7, Unit Economics: 8, 
          Competitive Moats: 6, Scaling Bottlenecks: 7

gpt_o3 (vc_skeptic)
  Average Score: 6.8/10 | Confidence: 90.0%
  Scores: Market Viability: 7, Technical Feasibility: 6, Unit Economics: 8,
          Competitive Moats: 5, Scaling Bottlenecks: 8

[... 5 more models ...]

----------------------------------------------------------------------
⚔️  KEY DEBATES (Model Disagreements)
----------------------------------------------------------------------
  • Technical Feasibility: Models disagree (range 4-8, avg 6.3) - requires deeper analysis
  • Competitive Moats: Models disagree (range 3-7, avg 5.1) - requires deeper analysis

----------------------------------------------------------------------
📊 CONSENSUS DIMENSION SCORES
----------------------------------------------------------------------

Market Viability: 8/10 [vc_skeptic]
  Consensus Reasoning: Strong market indicators with proven revenue...
  Failure Modes:
    - Market saturation in enterprise space
    - Customer acquisition costs may exceed projections
    
[Additional dimensions...]

======================================================================
Consensus Score: 7.1/10

✓ DECISION: PROCEED
======================================================================

⚠️  MINORITY REPORT:
grok (contrarian) strongly disagrees: Scored 5.2 vs consensus 7.1. 
Black swan risk: Market paradigm shift to AI agents could make SaaS obsolete.

🎯 REFINED CONCEPT:
B2B SaaS platform with proven revenue PIVOTS: Build defensible moat through 
data network effects AND Prepare for AI agent integration strategy

----------------------------------------------------------------------
🔄 UNIFIED PIVOTS (From All Models)
----------------------------------------------------------------------
1. Build defensible moat through data network effects and customer lock-in
2. Develop AI agent integration strategy to future-proof against disruption
3. Accelerate international expansion to diversify market risk

----------------------------------------------------------------------
🧪 VALIDATION EXPERIMENTS (Top 3)
----------------------------------------------------------------------

[Experiments...]
```

### Legacy Output Example

```
🔥 CRUCIBLE: Adversarial Evaluation Initiated
======================================================================

Concept: AI-powered fitness app that creates personalized workout plans...

======================================================================
📊 DIMENSION SCORES (with Adversarial Perspectives)
======================================================================

Market Viability: 6/10 [VC Skeptic]
  Reasoning: From VC Skeptic view: Market viability is questionable...
  Failure Modes:
    - Market size smaller than anticipated
    - Customer acquisition costs exceed projections

Technical Feasibility: 5/10 [Domain Expert]
  Reasoning: From Domain Expert view: Technical execution has moderate risk...
  Failure Modes:
    - Technology doesn't perform as expected in production
    - Development timeline exceeds estimates by 2-3x

[Additional dimensions...]

======================================================================
Overall Score: 5.4/10

⚠️ DECISION: PROCEED_WITH_CAUTION
======================================================================

🎯 REFINED CONCEPT:
AI-powered fitness app... PIVOT: Start with MVP using existing tools/APIs 
to reduce technical risk AND Build network effects or data moat from day 
one as core strategy

----------------------------------------------------------------------
🔄 KEY PIVOTS RECOMMENDED
----------------------------------------------------------------------
1. Start with MVP using existing tools/APIs to reduce technical risk
2. Build network effects or data moat from day one as core strategy
3. De-risk before significant investment by validating key assumptions

----------------------------------------------------------------------
🧪 VALIDATION EXPERIMENTS (Top 3)
----------------------------------------------------------------------

Experiment 1: Technical Proof of Concept
  Hypothesis: Core technology can deliver promised value at acceptable cost...
  Method: Build minimal prototype of hardest technical component...
  Success Criteria: Prototype achieves 80%+ of promised capability...
  Cost: $2000-10000 (developer time)
  Time: 2-4 weeks

[Additional experiments...]
```

## Output Files

CRUCIBLE generates two outputs:

1. **Console Output** - Human-readable evaluation report
2. **crucible_evaluation.json** - Machine-readable JSON for programmatic use

## Exit Codes

CRUCIBLE uses exit codes to indicate the decision:

- `0` - PROCEED or STRONG_PROCEED
- `1` - KILL
- `2` - PROCEED_WITH_CAUTION

This allows integration into CI/CD pipelines or automated workflows.

## Use Cases

- **Entrepreneurs** - Validate your startup idea before investing time/money
- **Investors** - Quick due diligence framework for early-stage concepts
- **Accelerators** - Standard evaluation framework for applicants
- **Product Teams** - Stress-test new product concepts before development
- **Students** - Learn to think critically about business ideas

## Evaluation Dimensions Explained

### 1. Market Viability (VC Skeptic Perspective)
Questions:
- Is there a large enough market?
- Will customers actually pay?
- Is the timing right?
- Can you acquire customers economically?

### 2. Technical Feasibility (Domain Expert Perspective)
Questions:
- Can this actually be built with current technology?
- What are the technical risks?
- Does the team have the skills?
- What could go wrong technically?

### 3. Unit Economics (VC Skeptic Perspective)
Questions:
- What's the LTV/CAC ratio?
- Can this be profitable per customer?
- What are the margins?
- How long is the payback period?

### 4. Competitive Moats (Competitor Perspective)
Questions:
- What prevents me from copying this?
- Are there network effects?
- Is there IP protection?
- Why won't incumbents crush this?

### 5. Scaling Bottlenecks (Domain Expert Perspective)
Questions:
- What breaks at 10x? 100x?
- Are there operational constraints?
- Can quality be maintained at scale?
- What are the hard limits?

## Limitations

CRUCIBLE is a rule-based evaluation system designed to simulate adversarial thinking. While it provides valuable insights, it:

- Cannot replace human judgment and domain expertise
- Works best as a starting framework for critical thinking
- May miss context-specific nuances
- Should be supplemented with real customer research

For production use, consider integrating with LLM APIs for deeper analysis.

## Contributing

Contributions welcome! Areas for improvement:

- Integration with LLM APIs (OpenAI, Anthropic, etc.) for deeper analysis
- Additional evaluation dimensions
- Industry-specific evaluation templates
- Historical case study validation

## License

MIT License - See LICENSE file for details

## Authors

Created for adversarial evaluation of startup concepts. Inspired by the need to kill weak ideas early so strong ones can thrive.

---

**Remember: Weak ideas die here so strong ones survive. 🔥**
