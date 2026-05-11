#!/usr/bin/env python3
"""Validate that the public Naus Hermes profile bundle is portable and sanitized."""

from __future__ import annotations

import re
import sys
from pathlib import Path


BUNDLE_ROOT = Path(__file__).resolve().parent
PROFILES_ROOT = BUNDLE_ROOT / "profiles"
REQUIRED_FILES = {"SOUL.md", "config.yaml", "distribution.yaml"}
FORBIDDEN_NAMES = {
    ".env",
    "auth.json",
    "auth.lock",
    "state.db",
    "state.db-shm",
    "state.db-wal",
    "LETTA_MEMORY.md",
    "logs",
    "sessions",
    "backups",
    "cache",
}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"https://discord(?:app)?\\.com/api/webhooks/\\d+/[A-Za-z0-9_-]+"),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
]


def main() -> int:
    errors: list[str] = []
    profiles = sorted(path for path in PROFILES_ROOT.iterdir() if path.is_dir())
    if len(profiles) != 17:
        errors.append(f"expected 17 profiles, found {len(profiles)}")

    for profile in profiles:
        names = {path.name for path in profile.iterdir()}
        missing = REQUIRED_FILES - names
        if missing:
            errors.append(f"{profile.name}: missing {sorted(missing)}")
        for path in profile.rglob("*"):
            if path.name in FORBIDDEN_NAMES:
                errors.append(f"{profile.name}: forbidden runtime artifact {path.relative_to(BUNDLE_ROOT)}")
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{profile.name}: secret-like value in {path.relative_to(BUNDLE_ROOT)}")

    if errors:
        print("Naus Hermes profile bundle validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validated {len(profiles)} Naus Hermes profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
