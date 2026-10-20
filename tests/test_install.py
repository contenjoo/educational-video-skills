"""Exercise user-content preservation in both supported hosts."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("canva-video-maker", "remotion-lesson-video")


class InstallTests(unittest.TestCase):
    def test_install_dry_run_collision_and_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            command = [sys.executable, str(ROOT / "scripts/install.py"), "--target", "both",
                       "--scope", "project", "--project", str(base)]
            subprocess.run(command + ["--dry-run"], check=True, capture_output=True)
            self.assertFalse((base / ".agents").exists())
            self.assertFalse((base / ".claude").exists())
            subprocess.run(command, check=True, capture_output=True)
            for host in (".agents", ".claude"):
                for name in NAMES:
                    installed = base / host / "skills" / name
                    self.assertEqual((installed / "SKILL.md").read_bytes(),
                                     (ROOT / "skills" / name / "SKILL.md").read_bytes())
                    self.assertEqual((installed / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
                    self.assertTrue((installed / "scripts/preflight.py").exists())
            old = base / ".claude/skills/canva-video-maker/SKILL.md"
            old.write_text("user customization", encoding="utf-8")
            before = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob("*") if p.is_file()}
            rejected = subprocess.run(command, capture_output=True)
            self.assertEqual(rejected.returncode, 1)
            after = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            subprocess.run(command + ["--update", "--dry-run"], check=True, capture_output=True)
            self.assertEqual(old.read_text(encoding="utf-8"), "user customization")
            subprocess.run(command + ["--update"], check=True, capture_output=True)
            backups = list((base / ".claude/skill-backups").glob("*/canva-video-maker/SKILL.md"))
            self.assertTrue(any(p.read_text(encoding="utf-8") == "user customization" for p in backups))
            self.assertEqual(old.read_bytes(), (ROOT / "skills/canva-video-maker/SKILL.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
