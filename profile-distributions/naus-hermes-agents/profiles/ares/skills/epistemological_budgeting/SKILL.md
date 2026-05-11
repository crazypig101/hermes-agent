---
name: epistemological_budgeting
description: Reads per-hemisphere drift scores and routes capital away from hallucinating lobes.
---

# epistemological_budgeting

## When to use
Before allocating any daily_buy_budget. Fires automatically every 5 min and publishes openclaw:budget:scale:{hemisphere} Redis keys.

## How (concrete API)

The concrete implementation lives at:
  `~/.openclaw/workspace/organism/oracle_immune.py`

Library API you can call directly from Python:
```python
from oracle_immune import budget_scale, epistemological_budgeting
scale = budget_scale('equity')          # 0.0–1.0 multiplier
alloc = base_budget * scale             # apply
report = epistemological_budgeting()    # full per-hemisphere report
```

CLI entry point:
```
python3 ~/.openclaw/workspace/organism/oracle_immune.py budget
```

## Why this matters
Hallucinating lobes (high drift score) signal model mismatch with reality — sending more capital there compounds the error. Budget routing is the cheapest, fastest defense against a drifting agent.

## Self-evolution hook
Score bands map to budget multipliers (1.0 → 0.75 → 0.5 → 0.25 → 0.0). Phantom-limb signals from motor cortices add weight, so the budget responds within minutes of a phantom sell attempt.

## Wiring status
Live; published at openclaw:budget:scale:<hemisphere> and openclaw:immune:score:<hemisphere>. Alfred reads these on every allocation decision.
