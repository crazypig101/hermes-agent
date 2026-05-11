---
name: entry-score-post-audit
description: Reconciles GO/WAIT/ABORT scoring against actual fill outcomes via oracle, so calibration learns from real broker reality.
---

# entry-score-post-audit

## When to use
When a trade closes, before writing the postmortem.

## How
Fetch truth_oracle.held_anywhere() at-close. Reconcile against the GO/WAIT signal that originated the trade. Write outcome to episodic memory with held_at_close=bool.

## Why this matters
Calibration currently learns from assumed fills. The oracle gives ground truth. Better calibration = better entry scores over time.

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
