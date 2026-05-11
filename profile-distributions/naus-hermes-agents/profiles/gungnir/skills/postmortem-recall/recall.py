#!/usr/bin/env python3
"""postmortem-recall — Hermes skill wrapper around find_similar_setup.py.

Calls the existing CLI and formats top-K JSON hits as chat-friendly markdown
for delivery via Telegram / Discord / CLI.

Reads OPENCLAW_LESSONS_DSN from env or strike-team/.env (mode 600).
Never bakes a literal password into source.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

WRAPPED = Path("/home/ericm1883/workspace/scripts/find_similar_setup.py")
VENV_PY = Path("/home/ericm1883/workspace/.venv-organism/bin/python")

# Ticker extraction — uppercase 1-5 letter standalone words.
_TICKER_RE = re.compile(r"\b([A-Z]{1,5}(?:-[A-Z]{1,4})?)\b")
_TICKER_BLOCKLIST = {
    # English / direction words that look like tickers
    "I", "A", "AN", "AND", "OR", "THE", "IS", "IT", "BE", "DO", "TO", "OF",
    "ON", "IN", "AT", "AS", "BY", "GO", "WE", "ME", "MY", "MR", "MS",
    # Trading direction / outcome words
    "LONG", "SHORT", "WINNER", "LOSER", "BUY", "SELL", "STOP", "LOSS",
    "PROFIT", "FEE", "PNL", "RR", "TP", "SL",
    # OpenClaw markers / conventions
    "MARK", "USD", "ETF", "VWAP", "VIX",
    # Reason codes
    "FLAT", "OK", "RUN", "END", "NEW", "OLD",
}


def _extract_ticker(query: str) -> str | None:
    """If query mentions a likely ticker, return it. Else None.

    Heuristic: 1-5 char uppercase tokens not in the blocklist.
    """
    for match in _TICKER_RE.finditer(query):
        cand = match.group(1)
        if cand not in _TICKER_BLOCKLIST and len(cand) >= 1:
            return cand
    return None


def _resolve_dsn() -> str:
    dsn = os.environ.get("OPENCLAW_LESSONS_DSN") or ""
    if dsn:
        return dsn
    env_path = Path("/home/ericm1883/workspace/strike-team/.env")
    if env_path.is_file():
        try:
            for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("OPENCLAW_LESSONS_DSN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        except OSError:
            pass
    # Final fallback: password-less DSN (will fail fast with clear error)
    return "postgresql://stash@127.0.0.1:5433/stash"


def run_query(query: str, k: int = 5) -> list[dict]:
    """Invoke find_similar_setup.py and return top-K hits, or [] on failure.

    Extracts a likely ticker from the query and passes it as --symbol so symbol
    filtering happens server-side. Direction is auto-inferred by find().
    """
    if not WRAPPED.is_file():
        return []
    cmd = [
        str(VENV_PY), str(WRAPPED), query,
        "--backend", "hybrid", "-k", str(k),
        "--format", "json", "--dsn", _resolve_dsn(),
    ]
    ticker = _extract_ticker(query)
    if ticker:
        cmd.extend(["--symbol", ticker])
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except (subprocess.SubprocessError, OSError):
        return []
    if proc.returncode != 0:
        return []
    try:
        return json.loads(proc.stdout).get("results", [])
    except json.JSONDecodeError:
        return []


def format_chat(query: str, hits: list[dict]) -> str:
    """Format hits as chat markdown. Pattern summary if 3+ share a symbol or outcome."""
    if not hits:
        return f"No similar prior setups found for: {query!r}"

    lines = [f"Top {len(hits)} similar prior setups for {query!r}:"]
    for i, h in enumerate(hits, 1):
        sym = h.get("symbol") or "(general)"
        outcome = h.get("outcome_label") or "?"
        pnl = h.get("outcome_pnl_pct")
        pnl_s = f"{pnl:+.2f}%" if pnl is not None else "?"
        title = h.get("title") or "(untitled)"
        date = (h.get("occurred_at") or "")[:10] or "?"
        excerpt = (h.get("excerpt") or "")[:200].replace("\n", " ")
        lines.append("")
        lines.append(f"{i}. {sym} — {outcome} {pnl_s} on {date}")
        lines.append(f"   {title}")
        if excerpt:
            lines.append(f"   {excerpt}")

    # Pattern detection: 3+ hits sharing symbol or outcome label
    if len(hits) >= 3:
        sym_counter = Counter(h.get("symbol") for h in hits if h.get("symbol"))
        out_counter = Counter(h.get("outcome_label") for h in hits if h.get("outcome_label"))
        for counter, label in ((sym_counter, "on"), (out_counter, "are")):
            if counter:
                top_value, top_n = counter.most_common(1)[0]
                if top_n >= 3:
                    lines.append("")
                    lines.append(f"Pattern: {top_n}/{len(hits)} hits {label} {top_value}.")
                    break  # one pattern line is enough
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Recall similar prior trades/lessons")
    parser.add_argument("query", help="Free-form query (ticker, direction, regime, setup family)")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()
    hits = run_query(args.query, args.k)
    print(format_chat(args.query, hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
