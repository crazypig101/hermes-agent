---
name: narrative-heartbeat-publisher
description: Guarantees pheme publishes at least a heartbeat every pulse, even when no fresh narrative news exists.
---

# narrative-heartbeat-publisher

## When to use
End of every pulse, unconditionally.

## How
Write signals/pheme_heartbeat = {ts, themes_scanned, items_seen, top3_themes}. Then write per-theme heat hash openclaw:pheme:heat:<theme> keyed against truth_oracle.held_or_universe(). Held = 1.0x weight, in-universe = 0.7x, neither = drop.

## Why this matters
Pheme has been silent for 1h45m+ — no heat keys at all. Downstream consumers (athena, hermes) starve. A heartbeat surface fixes this categorically.

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
