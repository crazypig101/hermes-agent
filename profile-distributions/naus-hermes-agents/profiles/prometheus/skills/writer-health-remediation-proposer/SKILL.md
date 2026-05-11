---
name: writer-health-remediation-proposer
description: Reads truth_oracle_writer_health.json and converts unhealthy writers into actionable Tier-2 proposals for the adaptation_engine.
---

# writer-health-remediation-proposer

## When to use
Each adaptation cycle, BEFORE scoring fitness.

## How
Parse ~/.openclaw/workspace/organism/data/truth_oracle_writer_health.json. For each writer with score >= 30, emit a Tier-2 proposal: type='writer_remediation', details={writer, symbol, last_recurrence, suggested_restart_cmd}.

## Why this matters
Halts evolution-on-bad-data. Turns the oracle's diagnostic output into actionable directives — the missing link between detection and remediation.

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
