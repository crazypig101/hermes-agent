---
name: regime-position-sympathy-check
description: Cross-references current regime against actually-held positions to surface regime/holding conflicts (e.g. CRISIS regime + leveraged longs still open).
---

# regime-position-sympathy-check

## When to use
After classifying the regime each pulse.

## How
Compare ares_regime against truth_oracle.held_anywhere(). If CRISIS while high-beta names held, emit signals/regime_position_conflict with the conflicting tickers. Hermes/Tyche listen for this and trim.

## Why this matters
Without this, regime detection is informational. With this, it's actionable: the regime call drives concrete exits.

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
