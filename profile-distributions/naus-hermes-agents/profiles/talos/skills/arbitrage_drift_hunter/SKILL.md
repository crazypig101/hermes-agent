---
name: arbitrage_drift_hunter
description: Detects systemic bias between internal worldview and broker truth, drafts mean-reversion skill proposals.
---

# arbitrage_drift_hunter

## When to use
Fires every 5 min via oracle-immune.timer. Talos may also invoke manually when researching a hypothesis.

## How (concrete API)

The concrete implementation lives at:
  `~/.openclaw/workspace/organism/oracle_immune.py`

Library API you can call directly from Python:
```python
from oracle_immune import arbitrage_drift_hunter
result = arbitrage_drift_hunter()
for proposal in result['proposals']:
    # proposal contains: surface, agent, draft_skill, rationale
    review_or_implement(proposal)
```

CLI entry point:
```
python3 ~/.openclaw/workspace/organism/oracle_immune.py arbitrage
```

## Why this matters
If an internal model consistently publishes signals that the oracle has to correct, that's not random noise — it's a structural bias. Trading AGAINST the organism's own false assumptions captures alpha while the structural fix is pending.

## Self-evolution hook
Proposals are appended to oracle_immune_bias_proposals.jsonl. Talos's research lobe consumes them, ranks by potential edge, and drafts a fade-{agent}-on-{surface} skill for prometheus to review and merge.

## Wiring status
Live; writing proposals to ~/.openclaw/workspace/organism/data/oracle_immune_bias_proposals.jsonl.
