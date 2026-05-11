---
name: proprioceptive_reflex
description: Pre-order phantom check for crypto — refuses sells for symbols not held at Coinbase.
---

# proprioceptive_reflex

## When to use
MUST be called before submitting any SELL or REDUCE order to Coinbase (or paper-coinbase). Same reflex pattern as hermes-trader.

## How (concrete API)

The concrete implementation lives at:
  `~/.openclaw/workspace/organism/oracle_immune.py`

Library API you can call directly from Python:
```python
from oracle_immune import assert_position_for_sell
if not assert_position_for_sell(symbol, agent='tyche'):
    return  # phantom blocked
```

CLI entry point:
```
python3 ~/.openclaw/workspace/organism/oracle_immune.py (library only)
```

## Why this matters
Crypto venues are less forgiving of phantom-position attempts: rate limits bite faster, and the paper portfolio includes symbols Tyche shouldn't actively manage. The reflex protects both the live and paper sides.

## Self-evolution hook
Same accumulation as hermes-trader: phantom events feed epistemological_budgeting and trigger source attribution.

## Wiring status
Library function. Tyche must call it before every sell. Fail-open on oracle unavailable.
