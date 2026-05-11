---
name: exit-signal-acknowledgment
description: Closes the loop on whether execution lobes actually applied kairos's exit levels.
---

# exit-signal-acknowledgment

## When to use
After writing signals/kairos_exits each pulse.

## How
Diff truth_oracle.held_anywhere() across pulses. If a position persists past its stop-loss threshold for >2 pulses, escalate to signals/kairos_exit_unacked with a WRITER_HEALTH finding pointing at the responsible execution lobe.

## Why this matters
Kairos's postmortem says 'exit signals never triggered in 37 Letta-era trades'. Verifying acknowledgment turns a fire-and-forget broadcast into a closed loop.

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
