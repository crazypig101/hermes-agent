---
name: held-set-garbage-collector
description: Sweeps stale openclaw:sentinel:health:* keys for symbols not held at the broker. Belongs to the somatic_sentinel domain but lives under prometheus's improvement skills.
---

# held-set-garbage-collector

## When to use
Run on a periodic timer (already wired via truth-oracle.timer).

## How
Scan openclaw:sentinel:health:*. For each key, if the symbol is not in truth_oracle.held_anywhere(), DELETE it. Log to signals/sentinel_purged.

## Why this matters
Prevents the LLY-loop pathology categorically: no health state exists for non-held symbols, so no decay can produce a phantom SELL signal.

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
