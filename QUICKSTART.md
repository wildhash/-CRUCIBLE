# CRUCIBLE Quick Start Guide

## Installation

No installation needed! Just Python 3.7+

```bash
git clone https://github.com/wildhash/-CRUCIBLE.git
cd -CRUCIBLE
```

## 🆕 Multi-Model Mode (Default)

Run your concept through the **7-model adversarial gauntlet**:

```bash
python3 crucible.py "Your startup concept here"
```

This orchestrates 7 specialized AI models in parallel:
- 🧠 Claude Opus (Deep Reasoning Critic)
- 💰 GPT-o3 (VC Skeptic)
- ⚡ Gemini Flash (Speed Analyst)
- 🔧 DeepSeek R1 (Technical Auditor)
- 🎲 Grok (Contrarian)
- 🌏 Kimi (APAC Expansion)
- 💸 Qwen (Cost Optimizer)

**Note**: By default, uses mock evaluators (rule-based). Configure API keys in `config/models.yaml` for real AI evaluations.

## Legacy Mode

Use the original single-agent evaluation:

```bash
python3 crucible.py "Your startup concept" --mode=legacy
```

## Example Evaluations

Try these examples to see CRUCIBLE in action:

### Strong Concept (Should get PROCEED)
```bash
python3 crucible.py "B2B SaaS platform with recurring revenue, validated enterprise customers, automated workflows, network effects, and proven profitability"
```

### Weak Concept (Should get KILL)
```bash
python3 crucible.py "Free mobile app for niche hobby with ad-supported model"
```

### Moderate Concept (Should get PROCEED_WITH_CAUTION)
```bash
python3 crucible.py "AI-powered productivity tool for remote teams"
```

### Compare Multi-Model vs Legacy

```bash
# Multi-model (default)
python3 crucible.py "B2B marketplace for freelancers"

# Legacy mode
python3 crucible.py "B2B marketplace for freelancers" --mode=legacy
```

## Run Multiple Examples

```bash
python3 examples.py
```

This will walk you through 5 different startup concept evaluations.

## Run Tests

```bash
# Original tests
python3 test_crucible.py

# Multi-model architecture tests (18 new tests)
python3 test_multimodel.py

All 22 tests should pass, demonstrating that CRUCIBLE works correctly.

## Understanding the Output

CRUCIBLE provides:

1. **Dimension Scores (1-10)** - How your concept performs on each of 5 critical dimensions
2. **Adversarial Perspectives** - Each dimension evaluated by a different skeptical viewpoint
3. **Overall Score** - Average across all dimensions
4. **Decision** - KILL, PROCEED_WITH_CAUTION, PROCEED, or STRONG_PROCEED
5. **Refined Concept** - Your idea improved based on the critique
6. **Key Pivots** - Specific changes to make your concept stronger
7. **3 Validation Experiments** - Concrete tests to validate your assumptions
8. **Critical Risks** - Top failure modes to watch out for

## Exit Codes

CRUCIBLE returns different exit codes for automation:

- `0` - PROCEED or STRONG_PROCEED
- `1` - KILL  
- `2` - PROCEED_WITH_CAUTION

Use in scripts:
```bash
if python3 crucible.py "My concept"; then
    echo "Concept approved!"
else
    echo "Concept needs work or should be killed"
fi
```

## Output Files

- **Console** - Human-readable formatted report
- **crucible_evaluation.json** - Machine-readable JSON for programmatic use

## Tips for Best Results

1. **Be Specific** - Include details about your market, technology, business model, and competitive advantage
2. **Include Evidence** - Mention validation, customers, revenue, or other proof points
3. **Describe Scale** - Mention if it's automated, platform-based, or has network effects
4. **Note Defensibility** - Highlight patents, proprietary data, or other moats

### Good Example
```
"B2B SaaS platform for accounting automation targeting mid-market companies.
Subscription model at $500/month, 50 paying customers with $25K MRR.
Proprietary AI algorithms with patent pending. Integration with QuickBooks
creates high switching costs. Automated workflows enable global scale."
```

### Bad Example  
```
"App for better productivity"
```

## What CRUCIBLE Evaluates

### 1. Market Viability (VC Skeptic)
- Market size and growth
- Customer validation and willingness to pay
- Timing and adoption readiness
- Customer acquisition economics

### 2. Technical Feasibility (Domain Expert)
- Technology complexity and risk
- Team capability
- Dependencies on external systems
- Development timeline realism

### 3. Unit Economics (VC Skeptic)
- Revenue model and margins
- LTV/CAC ratio potential
- Scalability of economics
- Path to profitability

### 4. Competitive Moats (Competitor)
- Defensibility against replication
- Switching costs and lock-in
- Network effects potential
- Market position advantages

### 5. Scaling Bottlenecks (Domain Expert)
- Operational complexity
- Resource constraints
- Geographic/regulatory barriers
- Quality maintenance at scale

## Limitations

CRUCIBLE is a rule-based system that simulates adversarial thinking. It:

- Provides a framework for critical evaluation
- Cannot replace human judgment
- Works best as a starting point for analysis
- Should be supplemented with real customer research

## Next Steps After Evaluation

1. **If KILL** - Seriously consider pivoting or abandoning the concept
2. **If PROCEED_WITH_CAUTION** - Focus on de-risking the weakest dimensions
3. **If PROCEED** - Execute the recommended validation experiments
4. **If STRONG_PROCEED** - Move forward but stay vigilant for the identified risks

## Contributing

Found a bug or have an improvement? Contributions welcome!

## Support

For questions or issues, please open a GitHub issue.

---

**Remember: Weak ideas die here so strong ones survive. 🔥**
