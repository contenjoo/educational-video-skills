#!/usr/bin/env python3
"""Build independent Claude-compatible ZIPs from a fixed file allowlist."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("remotion-lesson-video", "canva-video-maker")


def main():
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    for name in SKILLS:
        skill = ROOT / "skills" / name
        files = [skill / "SKILL.md", skill / "agents" / "openai.yaml"]
        files += [skill / "SKILL.en.md"]
        files += sorted((skill / "references").glob("*.md"))
        files += sorted((skill / "scripts").glob("*.py"))
        destination = output / f"{name}.zip"
        with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, f"{name}/{path.relative_to(skill).as_posix()}")
            archive.write(ROOT / "LICENSE", f"{name}/LICENSE")
        with ZipFile(destination) as archive:
            assert archive.testzip() is None
            assert f"{name}/SKILL.md" in archive.namelist()
            assert all(item.startswith(name + "/") for item in archive.namelist())
        print(destination)


if __name__ == "__main__":
    main()
