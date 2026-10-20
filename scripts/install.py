#!/usr/bin/env python3
"""Install both instruction-only skills without overwriting existing folders."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("remotion-lesson-video", "canva-video-maker")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude", "both"), required=True)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--dry-run", action="store_true")
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
    if collisions:
        print("No files changed. Existing skills must be reviewed first:", file=sys.stderr)
        print("\n".join(collisions), file=sys.stderr)
        return 1
    if args.dry_run:
        for source, dest in plans:
            print(f"Would install {source.name} -> {dest}")
        return 0
    for source, dest in plans:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, dest)
        shutil.copy2(ROOT / "LICENSE", dest / "LICENSE")
        print(f"Installed {source.name} -> {dest}")
    print("Open a new conversation to discover the skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
