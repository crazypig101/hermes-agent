---
name: postmortem-ingest
description: Daily cron skill — ingests new OpenClaw postmortems into the 'trading-postmortems' Hermes session so Honcho's user model accretes trade history.
version: 1.0.0
metadata:
  hermes:
    tags: [trading, ingest, cron, openclaw, honcho]
    related_skills: [postmortem-recall]
---

# Postmortem Ingest

Daily cron skill — runs at 22:00 ET, reads any new postmortems since the last
cursor, composes a 1-line summary each, and posts as user_messages into the
`trading-postmortems` Hermes session via Hermes Gateway HTTP API.

## When this skill runs

Driven by `hermes cron` schedule `0 22 * * *` (America/New_York). Not invoked
by user chat.

## What it produces

One user_message per new postmortem in the `trading-postmortems` session:
```
Closed trade 2026-04-23: AAPL long WINNER +2.79% setup=earnings_beat_vwap_reclaim exit=PROFIT_TRIM_2 held=21.0h
```

These are seen by:
- The Hermes session itself (queryable via `hermes sessions show trading-postmortems`).
- Honcho's `sync_turn` (builds the user model over time).
- `hermes insights` (analytics + token-usage).

## Idempotency

Cursor at `~/.openclaw/state/hermes-ingest-cursor.json`. Re-runs skip already-posted files.

## Failure behavior

- Hermes Gateway down → logs warning per file, exits 0; cursor advances anyway (we tolerate gateway flap; missed messages can be backfilled).
- Postmortem dir missing → prints clean status, exits 0.
- Single file unparseable → skipped, logged, others continue.

## Configuration

Endpoints + auth verified in `~/.openclaw/docs/hermes_api_contract.md`:
- `POST /api/sessions/{session_id}/append` (auto-creates the session if missing).
- Auth: `Authorization: Bearer $HERMES_API_TOKEN` (default `local-hermes-token`).
