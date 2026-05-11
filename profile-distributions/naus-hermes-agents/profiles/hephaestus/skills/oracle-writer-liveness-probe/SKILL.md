---
name: oracle-writer-liveness-probe
description: Treats truth_oracle as a monitored service and probes upstream broker writers (alpaca cache, coinbase cache, universe loader) for liveness.
---

# oracle-writer-liveness-probe

## When to use
Every pulse, alongside the standard MCP health checks.

## How
Verify ~/.openclaw/workspace/organism/data/truth_oracle_meta.json mtime < 600s. Verify each oracle returns confidence >= 0.8. Any stale writer triggers a systemctl restart of its source service before drift propagates.

## Why this matters
Oracle quality is upstream of every other agent's correctness. Treating it as infra-tier means drift is caught before it reaches decision lobes.

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
