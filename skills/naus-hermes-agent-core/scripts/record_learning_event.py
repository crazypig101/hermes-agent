#!/usr/bin/env python3
"""Append a sanitized Naus Hermes learning event."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]+"),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
]

ALLOWED_KINDS = {
    "observation",
    "defect",
    "postmortem",
    "research_brief",
    "skill_proposal",
    "validation",
    "promotion",
    "rollback",
}


def assert_clean(value: str, field: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(value or ""):
            raise SystemExit(f"refusing to write secret-like value in {field}")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip().lower()).strip("-")
    return cleaned or "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--kind", required=True, choices=sorted(ALLOWED_KINDS))
    parser.add_argument("--summary", required=True)
    parser.add_argument("--evidence", default="")
    parser.add_argument("--status", default="observed")
    parser.add_argument("--proposal", default="")
    parser.add_argument("--metric", action="append", default=[], help="key=value metric; repeatable")
    parser.add_argument("--root", type=Path, default=Path.home() / ".hermes" / "learning")
    args = parser.parse_args()

    for field in ("agent", "kind", "summary", "evidence", "status", "proposal"):
        assert_clean(str(getattr(args, field)), field)
    for metric in args.metric:
        assert_clean(metric, "metric")

    metrics: dict[str, str] = {}
    for item in args.metric:
        if "=" not in item:
            raise SystemExit(f"bad --metric value, expected key=value: {item}")
        key, value = item.split("=", 1)
        metrics[key.strip()] = value.strip()

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": slug(args.agent),
        "kind": args.kind,
        "summary": args.summary.strip(),
        "evidence": args.evidence.strip(),
        "status": args.status.strip(),
        "proposal": args.proposal.strip(),
        "metrics": metrics,
    }

    out_dir = args.root.expanduser() / slug(args.agent)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "events.jsonl"
    with out_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
