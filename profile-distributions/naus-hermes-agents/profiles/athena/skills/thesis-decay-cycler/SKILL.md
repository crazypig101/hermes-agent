---
name: thesis-decay-cycler
description: Walks all theses each pulse, applies age-based decay, and retires defeated theses against current broker truth.
---

# thesis-decay-cycler

## When to use
At top of every pulse, before writing new theses.

## How
For each thesis in theses/*: apply daily decay (-0.2/day). Mark RESOLVED if its ticker no longer in truth_oracle.held_or_universe() for the relevant hemisphere. Mark EXPIRED if confidence < 0.3. Append to theses_retired ledger.

## Why this matters
Without this, athena writes new theses without retiring stale ones. Confidence inflates and 'we still hold the LLY thesis' zombies persist forever.

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
