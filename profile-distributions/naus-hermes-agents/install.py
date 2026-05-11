#!/usr/bin/env python3
"""Install the Naus/NOUS Hermes Agent profile fleet.

This installer is intentionally conservative: it overlays distribution-owned
profile files and skills, but never deletes local memories, sessions, state
databases, auth files, logs, or other runtime artifacts.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


BUNDLE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BUNDLE_ROOT.parents[1]
PROFILES_ROOT = BUNDLE_ROOT / "profiles"
DEFAULT_TARGET = Path.home() / ".hermes" / "profiles"
PROFILE_FILES = (
    "NAUS_AGENT_CORE.md",
    "SOUL.md",
    "IDENTITY.md",
    "TOOLS.md",
    "LETTA_PERSONA.md",
    "LETTA_TOOLS.md",
    "distribution.yaml",
)
RUNTIME_NAMES = {
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


def profile_names() -> list[str]:
    return sorted(path.name for path in PROFILES_ROOT.iterdir() if path.is_dir())


def copy_file(src: Path, dst: Path, *, dry_run: bool) -> None:
    if src.name in RUNTIME_NAMES:
        raise RuntimeError(f"refusing to copy runtime-owned file: {src}")
    if dry_run:
        print(f"would copy {src} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_contents(src: Path, dst: Path, *, dry_run: bool) -> None:
    if not src.exists():
        return
    for item in sorted(src.iterdir()):
        if item.name in RUNTIME_NAMES or item.name.startswith("."):
            continue
        target = dst / item.name
        if dry_run:
            print(f"would copy {item} -> {target}")
            continue
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def install_profile(name: str, target_root: Path, *, force_config: bool, skip_bundled_skills: bool, dry_run: bool) -> None:
    source = PROFILES_ROOT / name
    if not source.exists():
        raise SystemExit(f"unknown profile: {name}")
    target = target_root / name
    if dry_run:
        print(f"would ensure {target}")
    else:
        target.mkdir(parents=True, exist_ok=True)

    for filename in PROFILE_FILES:
        src = source / filename
        if src.exists():
            copy_file(src, target / filename, dry_run=dry_run)

    config_src = source / "config.yaml"
    config_dst = target / "config.yaml"
    if config_src.exists() and (force_config or not config_dst.exists()):
        copy_file(config_src, config_dst, dry_run=dry_run)
    elif config_src.exists():
        print(f"preserved existing {config_dst}; pass --force-config to overwrite")

    skills_dst = target / "skills"
    if not skip_bundled_skills:
        copy_tree_contents(REPO_ROOT / "skills", skills_dst, dry_run=dry_run)
    copy_tree_contents(source / "skills", skills_dst, dry_run=dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Hermes profiles directory")
    parser.add_argument("--profile", action="append", choices=profile_names(), help="Install only one profile; repeatable")
    parser.add_argument("--force-config", action="store_true", help="Overwrite existing profile config.yaml files")
    parser.add_argument("--skip-bundled-skills", action="store_true", help="Only install Naus custom skills")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without copying files")
    args = parser.parse_args()

    selected = args.profile or profile_names()
    for name in selected:
        install_profile(
            name,
            args.target.expanduser(),
            force_config=args.force_config,
            skip_bundled_skills=args.skip_bundled_skills,
            dry_run=args.dry_run,
        )
    print(f"installed {len(selected)} Naus Hermes profile(s) into {args.target.expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
