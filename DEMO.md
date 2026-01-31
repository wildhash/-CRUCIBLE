# CRUCIBLE Demo Concepts

Test these concepts to see CRUCIBLE in action:

## 1. STRONG CONCEPT (Should get PROCEED or STRONG_PROCEED)
```bash
python3 crucible.py "Enterprise SaaS platform for automated accounting with $100K MRR, 200 paying customers, subscription model, proprietary AI with patent pending, deep QuickBooks integration creating high switching costs, and automated workflows enabling global scale"
```

## 2. WEAK CONCEPT (Should get KILL)  
```bash
python3 crucible.py "Free mobile game with ad revenue"
```

## 3. MODERATE CONCEPT (Should get PROCEED_WITH_CAUTION)
```bash
python3 crucible.py "B2B marketplace connecting freelance designers with startups"
```

## 4. RISKY CONCEPT (Should get KILL or PROCEED_WITH_CAUTION)
```bash
python3 crucible.py "Blockchain-powered decentralized social network with NFT integration"
```

## 5. SIMPLE CONCEPT (Needs more detail)
```bash
python3 crucible.py "Todo list app"
```

## Running All Examples

To see evaluations across multiple concept types:
```bash
python3 examples.py
```

## Running Tests

To verify CRUCIBLE works correctly:
```bash
python3 test_crucible.py
```

All 22 tests should pass.
