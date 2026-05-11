---
name: concentration-aware-thesis
description: Wraps autonomous thesis generation with concentration accounting so Tyche stops re-buying the same coin every pulse.
---

# concentration-aware-thesis

## When to use
Inside Step 2 of the autonomous-thesis path, before emitting confidence.

## How
Snapshot truth_oracle.coinbase_held(). If candidate ticker > 30% of crypto NAV OR appeared in last 3 thesis writes, downweight confidence by 0.2 and prefer an under-represented universe member. Reject any candidate outside [BTC,ETH,SOL].

## Why this matters
MEMORY documents 37 consecutive buys / 0 sells / SOL 14x overconcentration. The oracle prevents repeating that pattern.

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
