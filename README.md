# 🔥 CRUCIBLE

**Multi-model adversarial refinement engine that stress-tests startup concepts through collaborative AI debate until they're investor-ready.**

> *Weak ideas die here so strong ones survive.*

## What is CRUCIBLE?

CRUCIBLE is an adversarial evaluation agent that challenges startup concepts across 5 critical dimensions:

1. **Market Viability** - Is there a real market? Will customers pay?
2. **Technical Feasibility** - Can it actually be built? What are the risks?
3. **Unit Economics** - Do the numbers work? Can it be profitable?
4. **Competitive Moats** - What prevents competitors from crushing you?
5. **Scaling Bottlenecks** - What breaks when you try to grow?

## How It Works

CRUCIBLE adopts three adversarial perspectives to stress-test your idea:

- 🎯 **VC Skeptic** - "Show me the money and the moat"
- 🔬 **Domain Expert** - "Here's why the tech won't work as planned"
- ⚔️ **Competitor** - "Here's how I'd crush your business"

Each dimension is scored 1-10 with specific failure modes identified. After the critique, CRUCIBLE synthesizes:

- ✅ **Kill/Proceed Decision** - Should you continue or pivot?
- 🎯 **Refined Concept** - Your idea, battle-tested and improved
- 🔄 **Key Pivots** - Specific changes to make your concept stronger
- 🧪 **3 Validation Experiments** - Concrete tests to validate your assumptions

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

### Basic Usage

```bash
python crucible.py "Your startup concept here"
```

### Example

```bash
python crucible.py "AI-powered fitness app that creates personalized workout plans using machine learning to analyze user performance and adapt in real-time"
```

### Example Output

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
