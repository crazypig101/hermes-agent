#!/usr/bin/env python3
"""postmortem-ingest — daily cron skill that feeds new postmortems into a Hermes session.

Reads ~/.openclaw/postmortems/*.md, parses frontmatter, composes a 1-line
summary per postmortem, POSTs to the 'trading-postmortems' Hermes session
via Hermes Gateway HTTP API. Honcho's sync_turn ingests them into the
user model.

Idempotent via cursor file ~/.openclaw/state/hermes-ingest-cursor.json.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

POSTMORTEM_DIR = Path("/home/ericm1883/.openclaw/postmortems")
CURSOR = Path("/home/ericm1883/.openclaw/state/hermes-ingest-cursor.json")
HERMES_API_URL = os.environ.get("HERMES_API_URL", "http://127.0.0.1:8642")
HERMES_API_TOKEN = os.environ.get("HERMES_API_TOKEN", "local-hermes-token")
SESSION_ID = "trading-postmortems"  # /append auto-creates if missing
HTTP_TIMEOUT = 15

# Endpoints — verified by plan Task 1 (~/.openclaw/docs/hermes_api_contract.md)
ENDPOINT_APPEND = "/api/sessions/{session_id}/append"

log = logging.getLogger("postmortem_ingest")


def _auth_headers() -> dict:
    return {
        "Authorization": f"Bearer {HERMES_API_TOKEN}",
        "Content-Type": "application/json",
    }


def _http_post(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        method="POST", headers=_auth_headers(),
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
        return json.loads(r.read())


def load_cursor() -> dict:
    if CURSOR.exists():
        try:
            return json.loads(CURSOR.read_text())
        except (OSError, json.JSONDecodeError):
            pass
    return {"last_seen_filename": ""}


def save_cursor(state: dict) -> None:
    CURSOR.parent.mkdir(parents=True, exist_ok=True)
    CURSOR.write_text(json.dumps(state, indent=2))


def parse_frontmatter(path: Path) -> dict | None:
    """Return parsed JSON frontmatter, or None if missing/malformed."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 4)
    if end <= 0:
        return None
    try:
        return json.loads(text[4:end])
    except json.JSONDecodeError:
        return None


def make_summary(front: dict) -> str:
    """Compose 1-line summary suitable for a Hermes session user_message."""
    sym = front.get("symbol") or "?"
    side = front.get("side") or "?"
    pnl = front.get("realized_pnl_pct")
    pnl_s = f"{pnl:+.2f}%" if pnl is not None else "?"
    setup = front.get("setup_family") or "?"
    exit_codes = ",".join(front.get("exit_reason_codes") or []) or "none"
    duration_h = (front.get("duration_seconds") or 0) / 3600.0
    closed = (front.get("closed_at") or "")[:10] or "?"
    if pnl is None:
        verdict = "?"
    elif pnl > 0:
        verdict = "WINNER"
    elif pnl < 0:
        verdict = "LOSER"
    else:
        verdict = "FLAT"
    return (f"Closed trade {closed}: {sym} {side} {verdict} {pnl_s} "
            f"setup={setup} exit={exit_codes} held={duration_h:.1f}h")


def post_to_session(content: str) -> None:
    """POST a user_message into the postmortem session.

    Auto-creates the session if missing (verified API behavior — see
    ~/.openclaw/docs/hermes_api_contract.md).

    Swallows network errors so a transient gateway hiccup doesn't crash the
    cron tick; the cursor isn't advanced on error so a retry next cycle picks
    up the missed file.
    """
    url = f"{HERMES_API_URL}{ENDPOINT_APPEND.format(session_id=SESSION_ID)}"
    try:
        _http_post(url, {"role": "user", "content": content})
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        log.warning("post_to_session failed: %s", e)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cursor = load_cursor()
    last_seen = cursor.get("last_seen_filename", "")
    if not POSTMORTEM_DIR.exists():
        print(json.dumps({"status": "ok", "new_postmortems": 0,
                          "reason": f"{POSTMORTEM_DIR} missing"}))
        return 0

    md_files = sorted(POSTMORTEM_DIR.glob("*.md"))
    new_files = [f for f in md_files if f.name > last_seen]
    if not new_files:
        print(json.dumps({"status": "ok", "new_postmortems": 0}))
        return 0

    posted = 0
    skipped = 0
    for f in new_files:
        front = parse_frontmatter(f)
        if not front:
            skipped += 1
            continue
        try:
            post_to_session(make_summary(front))
            posted += 1
        except Exception as e:
            log.warning("post failed for %s: %s", f.name, e)
            skipped += 1

    cursor["last_seen_filename"] = new_files[-1].name
    cursor["last_run_at"] = datetime.now(timezone.utc).isoformat()
    save_cursor(cursor)
    print(json.dumps({
        "status": "ok",
        "session": SESSION_ID,
        "new_postmortems": len(new_files),
        "posted": posted,
        "skipped": skipped,
        "cursor": new_files[-1].name,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
