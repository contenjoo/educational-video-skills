#!/usr/bin/env python3
"""Install both skills; preserve existing folders unless backup-update is requested."""
import argparse
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("remotion-lesson-video", "canva-video-maker")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude", "both"), required=True)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update", action="store_true", help="Back up existing skills before installing the new copy")
    args = parser.parse_args()
    if args.scope == "project" and args.project is None:
        parser.error("--scope project requires --project PATH")
    if args.scope == "user" and args.project is not None:
        parser.error("--project is only valid with --scope project")
    base = Path.home() if args.scope == "user" else args.project.expanduser().resolve()
    if not base.is_dir():
        parser.error(f"Destination base directory does not exist: {base}")
    targets = ("codex", "claude") if args.target == "both" else (args.target,)
    plans = []
    for target in targets:
        folder = ".agents" if target == "codex" else ".claude"
        for skill in SKILLS:
            source = ROOT / "skills" / skill
            dest = base / folder / "skills" / skill
            if not (source / "SKILL.md").is_file():
                parser.error(f"Missing source skill: {source}")
            plans.append((source, dest))
    # Check the entire batch before changing any files.
    collisions = [str(dest) for _, dest in plans if dest.exists() or dest.is_symlink()]
    if collisions and not args.update:
        print("No files changed. Existing skills must be reviewed first:", file=sys.stderr)
        print("\n".join(collisions), file=sys.stderr)
        return 1
    if args.dry_run:
        for source, dest in plans:
            print(f"Would install {source.name} -> {dest}")
        return 0
    for source, dest in plans:
        dest.parent.mkdir(parents=True, exist_ok=True)
        staging = dest.parent / ("." + source.name + ".install-" + uuid4().hex[:8])
        backup = None
        try:
            shutil.copytree(source, staging, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copy2(ROOT / "LICENSE", staging / "LICENSE")
            if dest.exists() or dest.is_symlink():
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
                backup = dest.parent.parent / "skill-backups" / stamp / source.name
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), str(backup))
                print(f"Backed up existing skill -> {backup}")
            staging.rename(dest)
        except Exception:
            if staging.exists():
                shutil.rmtree(staging)
            if backup is not None and not dest.exists() and not dest.is_symlink():
                shutil.move(str(backup), str(dest))
            raise
        print(f"Installed {source.name} -> {dest}")
    print("Open a new conversation to discover the skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
