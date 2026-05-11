#!/usr/bin/env python3
"""Create or repair Hermes Desktop DGX connections for the Naus profile fleet."""

from __future__ import annotations

import argparse
import json
import shutil
import time
import uuid
from pathlib import Path


PROFILE_NAMES = [
    "alfred",
    "ares",
    "athena",
    "chimera",
    "gungnir",
    "hephaestus",
    "hermes-trader",
    "iris",
    "kairos",
    "mnemosyne",
    "nemesis",
    "pheme",
    "prometheus",
    "talos",
    "themis",
    "tyche",
    "zhuge_liang",
]
DEFAULT_CONNECTIONS = Path.home() / "Library/Application Support/HermesDesktop/connections.json"
MAC_EPOCH_OFFSET = 978307200


def now_cocoa() -> float:
    return time.time() - MAC_EPOCH_OFFSET


def load_connections(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"expected {path} to contain a JSON array")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connections", type=Path, default=DEFAULT_CONNECTIONS)
    parser.add_argument("--label-prefix", default="DGX")
    parser.add_argument("--ssh-alias", default="dgx")
    parser.add_argument("--host", default="", help="Optional explicit SSH host if Hermes Desktop should not rely on sshAlias")
    parser.add_argument("--user", default="", help="Optional SSH user for explicit host connections")
    parser.add_argument("--port", type=int, default=22)
    args = parser.parse_args()

    path = args.connections.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    connections = load_connections(path)
    if path.exists():
        backup = path.with_name(f"{path.name}.bak.pre-naus-connect-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(path, backup)
        print(f"backup: {backup}")

    by_profile = {c.get("hermesProfile"): c for c in connections if c.get("hermesProfile")}
    changed: list[str] = []
    timestamp = now_cocoa()
    for profile in PROFILE_NAMES:
        label = f"{args.label_prefix} · {profile}"
        conn = by_profile.get(profile)
        if conn is None:
            conn = {
                "id": str(uuid.uuid4()).upper(),
                "label": label,
                "sshAlias": args.ssh_alias,
                "hermesProfile": profile,
                "createdAt": timestamp,
                "updatedAt": timestamp,
            }
            connections.append(conn)
            changed.append(f"added {label}")
        if conn.get("label") != label or conn.get("hermesProfile") != profile or conn.get("sshAlias") != args.ssh_alias:
            conn["label"] = label
            conn["hermesProfile"] = profile
            conn["sshAlias"] = args.ssh_alias
            conn["updatedAt"] = timestamp
            changed.append(f"repaired {label}")
        if args.host:
            conn["host"] = args.host
        if args.user:
            conn["user"] = args.user
        if args.port:
            conn["port"] = args.port

    path.write_text(json.dumps(connections, indent=2) + "\n", encoding="utf-8")
    print(f"connections: {len(connections)}")
    for item in changed:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
