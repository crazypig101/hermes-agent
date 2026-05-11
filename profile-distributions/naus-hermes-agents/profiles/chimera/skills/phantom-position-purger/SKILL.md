---
name: phantom-position-purger
description: Diffs portfolio JSON files against oracle truth and proposes epigenome rules to purge any 'ghost' symbol from the system.
---

# phantom-position-purger

## When to use
Each pulse, as part of the cross-hemisphere review.

## How
For each portfolio JSON (hermes/trading-portfolio.json, tyche/coinbase-paper-portfolio.json): diff against truth_oracle.alpaca_held() / coinbase_held(). Any ghost symbol (in JSON, not at broker) generates an epigenome proposal: purge_phantom:<SYMBOL>.

## Why this matters
Stale JSON portfolio files were a contributing source for the LLY-class drift. Treating them as cache (not source of truth) prevents recurrence.

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
