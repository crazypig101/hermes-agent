#!/usr/bin/env python3
"""Stage a sanitized Hermes skill proposal."""

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


def assert_clean(value: str, field: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(value or ""):
            raise SystemExit(f"refusing to write secret-like value in {field}")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip().lower()).strip("-")
    return cleaned or "proposal"


def render_skill(name: str, description: str, trigger: str, workflow: str, validation: str, safety: str) -> str:
    skill_name = slug(name)
    return f"""---
name: {skill_name}
description: {description}
metadata:
  short-description: Proposed Naus Hermes skill
---

# {name}

## Trigger

{trigger}

## Workflow

{workflow}

## Validation

{validation}

## Safety

{safety or "Do not use secrets, private memory snapshots, runtime databases, or unverifiable claims."}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--safety", default="")
    parser.add_argument("--root", type=Path, default=Path.home() / ".hermes" / "learning")
    args = parser.parse_args()

    for field in ("agent", "name", "description", "trigger", "workflow", "validation", "safety"):
        assert_clean(str(getattr(args, field)), field)

    agent = slug(args.agent)
    proposal = slug(args.name)
    out_dir = args.root.expanduser() / agent / "skill_proposals" / proposal
    out_dir.mkdir(parents=True, exist_ok=True)

    skill_text = render_skill(args.name, args.description, args.trigger, args.workflow, args.validation, args.safety)
    (out_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")

    metadata = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "name": proposal,
        "status": "proposal",
        "description": args.description,
        "trigger": args.trigger,
        "validation": args.validation,
    }
    (out_dir / "proposal.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
