---
name: proprioceptive_reflex
description: Pre-order phantom check — refuses sells for symbols not held at broker, emits pain signal.
---

# proprioceptive_reflex

## When to use
MUST be called before submitting any SELL or REDUCE order to Alpaca. This is a code-level reflex, not a discretionary check.

## How (concrete API)

The concrete implementation lives at:
  `~/.openclaw/workspace/organism/oracle_immune.py`

Library API you can call directly from Python:
```python
from oracle_immune import assert_position_for_sell
if not assert_position_for_sell(symbol, agent='hermes_trader'):
    return  # phantom blocked; pain signal already emitted
```

CLI entry point:
```
python3 ~/.openclaw/workspace/organism/oracle_immune.py (library only)
```

## Why this matters
Sending sells for symbols you don't hold burns API calls, wakes the broker's risk system, and — worst — proves the agent's worldview has decoupled from reality. Block early, then send a pain signal so alfred can defund the lobe.

## Self-evolution hook
Every blocked order appends a phantom-limb event to oracle_immune_phantom_limbs.jsonl + Redis list. epistemological_budgeting weights phantom-limbs at 8× drift events, so repeated phantoms cause near-immediate budget cut.

## Wiring status
Library function only. Hermes must call it before every sell. Fail-OPEN on oracle unavailable (returns True) so transient infra issues don't lock the agent out.
