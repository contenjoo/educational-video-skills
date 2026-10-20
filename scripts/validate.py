#!/usr/bin/env python3
"""Validate portable skill structure, YAML, references, and public content."""
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("Install validation dependencies: python3 -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("remotion-lesson-video", "canva-video-maker")


def check():
    errors = []
    for name in NAMES:
        skill = ROOT / "skills" / name
        entry = skill / "SKILL.md"
        text = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{name}: missing YAML frontmatter")
            continue
        meta = yaml.safe_load(match.group(1))
        if not isinstance(meta, dict):
            errors.append(f"{name}: frontmatter must be a mapping")
            continue
        if meta.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"{name}: invalid name")
        description = meta.get("description")
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            errors.append(f"{name}: invalid description")
        if set(meta) - {"name", "description", "license", "metadata"}:
            errors.append(f"{name}: unexpected frontmatter fields")
        if meta.get("license") != "MIT":
            errors.append(f"{name}: missing license")
        ui = yaml.safe_load((skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        interface = ui.get("interface", {})
        if "$" + name not in interface.get("default_prompt", ""):
            errors.append(f"{name}: default prompt must mention the skill")
        if not 25 <= len(interface.get("short_description", "")) <= 64:
            errors.append(f"{name}: short description must have 25-64 characters")
        for path in skill.rglob("*.md"):
            body = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", body):
                if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                dest = (path.parent / target.split("#", 1)[0]).resolve()
                if not dest.is_relative_to(skill.resolve()) or not dest.exists():
                    errors.append(f"{path.relative_to(ROOT)}: broken/nonportable reference {target}")
    # New distribution sources only: no original user captures or state files.
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(p in {".git", "dist", "__pycache__"} for p in path.relative_to(ROOT).parts):
            continue
        if path.suffix in {".png", ".mp4", ".mp3", ".wav"} or path.name.startswith(".env"):
            errors.append(f"Unexpected private-media/config candidate: {path.relative_to(ROOT)}")
        if path.suffix not in {".md", ".yaml", ".yml", ".txt"}:
            continue
        body = path.read_text(encoding="utf-8")
        for pattern in (r"/Users/", r"/private/", r"gh[pousr]_[A-Za-z0-9]{20,}", r"sk-[A-Za-z0-9]{20,}", r"DAH[A-Za-z0-9_-]{7,}"):
            if re.search(pattern, body):
                errors.append(f"Possible personal path/secret/design ID: {path.relative_to(ROOT)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: both skills, UI metadata, relative references, and public-content checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
