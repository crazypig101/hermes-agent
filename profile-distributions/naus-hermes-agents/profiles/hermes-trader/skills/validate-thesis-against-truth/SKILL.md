---
name: validate-thesis-against-truth
description: Pre-flight broker-truth check before any BUY/SELL on equities. Prevents phantom-position orders.
---

# validate-thesis-against-truth

## When to use
Before calling fsm_execute_cycle. Every entry, every exit. Non-negotiable.

## How
Snapshot truth_oracle.alpaca_held(). REJECT a SELL when ticker not in held set (no inventory). WARN on a BUY when ticker already held (doubling down without fresh thesis). Proceed only when oracle confidence >= 0.8.

## Why this matters
The LLY infinite-loop came from selling a phantom position the LLM 'remembered' from stale MEMORY. The oracle is broker truth — trust it over memory.

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
