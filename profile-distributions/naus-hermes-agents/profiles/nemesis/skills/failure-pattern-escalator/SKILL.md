---
name: failure-pattern-escalator
description: Implements the SOUL.md promise of escalating after 3+ recurrences of the same failure pattern.
---

# failure-pattern-escalator

## When to use
After every postmortem write.

## How
Hash failure mode = (hemisphere, exit_type, regime, symbol_class). Increment per occurrence. At >=3, emit signals/nemesis_escalation with concrete remediation (kill-switch / quarantine action) and notify Prometheus + responsible lobe.

## Why this matters
SOUL.md claims escalation but the agent has no codified mechanism. Closing the loop means recurring bugs (e.g. LLY-loop class) get hard-stopped, not just logged.

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
