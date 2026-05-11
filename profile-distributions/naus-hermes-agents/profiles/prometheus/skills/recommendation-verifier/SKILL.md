---
name: recommendation-verifier
description: Closes the loop: verify each prior recommendation actually landed before re-emitting.
---

# recommendation-verifier

## When to use
Before generating new recommendations each pulse.

## How
Tag every recommendation with recommendation_id. Next pulse, query Hive/KG/git for evidence the change was applied. Mark applied|ignored|stale_after_72h. Feed back into priority ranking — applied recs gain trust, ignored ones drop.

## Why this matters
Without verification, the same recommendation gets re-emitted forever. The oracle's writer_health.json gives concrete data on whether fixes are sticking.

## Truth oracle quick reference
The oracle module lives at `~/.openclaw/workspace/organism/truth_oracle.py`.
Functions you may call:
- `_oracle_alpaca_held(env)` — equity positions
- `_oracle_coinbase_held(env)` — crypto positions
- `_oracle_held_anywhere(env)` — both
- `_oracle_universe(env)` — declared watchlist
- `_oracle_held_or_universe(env)` — held ∪ watchlist
- `reconcile_all(auto_fix=False)` — full drift report (informational)

Each returns `OracleResult(symbols: set, details: dict, confidence: float, ...)`.
Trust the oracle when `confidence >= 0.8`. Below that, fail-open.

## Self-evolution hook
When this skill detects a recurring pattern (same symbol pruned 3+ times within
24h, same recommendation ignored 3+ times, same failure mode), the system logs
to `~/.openclaw/workspace/organism/data/truth_oracle_writer_health.json` and
the adaptation_engine consumes it to propose structural fixes.
