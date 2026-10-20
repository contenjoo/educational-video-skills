#!/usr/bin/env python3
"""Check video-production prerequisites without changing user settings."""
import argparse
import json
import platform
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.request import urlopen


def run(args, timeout=12):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, "", type(exc).__name__


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("remotion", "canva"), required=True)
    parser.add_argument("--network", action="store_true", help="Check public npm registry reachability")
    parser.add_argument("--tts", action="store_true", help="Test macOS Korean system voice using synthetic text")
    parser.add_argument("--output", type=Path, help="Write a local JSON report")
    args = parser.parse_args()
    report = {"mode": args.mode, "os": platform.system(), "checks": {}, "actions": [],
              "scope": "Prerequisites only; browser login, model inference and final video are not verified."}
    required = ("node", "npm", "ffmpeg", "ffprobe") if args.mode == "remotion" else ("ffmpeg", "ffprobe")
    missing = []
    if args.mode == "canva":
        try:
            import PIL
            report["checks"]["Pillow"] = {"present": True, "version": PIL.__version__}
        except ImportError:
            report["checks"]["Pillow"] = {"present": False}
            missing.append("Pillow")
    for tool in ("node", "npm", "ffmpeg", "ffprobe", "claude", "codex"):
        present = shutil.which(tool) is not None
        item = {"present": present, "required": tool in required}
        if present:
            flag = "-version" if tool in ("ffmpeg", "ffprobe") else "--version"
            rc, out, err = run([tool, flag])
            item.update({"command_ok": rc == 0, "version": out.splitlines()[0] if out else None})
        if tool in required and (not present or not item.get("command_ok")):
            missing.append(tool)
        report["checks"][tool] = item
    if missing:
        report["actions"].append("Install or repair required tools: " + ", ".join(missing))
    if not any(report["checks"][x]["present"] for x in ("claude", "codex")):
        report["actions"].append("Use a skill-capable Claude/Codex app, or install its official CLI. CLI is optional for app users.")
    if args.network:
        try:
            with urlopen("https://registry.npmjs.org/remotion/latest", timeout=10) as response:
                package = json.load(response)
            report["checks"]["npm_network"] = {"ok": True, "remotion_version": package.get("version")}
        except Exception as exc:
            report["checks"]["npm_network"] = {"ok": False, "error_type": type(exc).__name__}
            report["actions"].append("Check DNS/proxy and host-approved network access; do not disable security settings.")
    if args.tts:
        if platform.system() != "Darwin" or not shutil.which("say"):
            report["checks"]["system_korean_tts"] = {"status": "not_available", "optional": True}
            report["actions"].append("Provide a Korean recording or choose an available TTS provider; macOS say is optional.")
        else:
            rc, out, err = run(["say", "-v", "?"])
            voices = [m.group(1).strip() for line in out.splitlines()
                      if (m := re.match(r"^(.*?)\s+ko_KR\b", line))]
            voice = next((v for v in voices if v.startswith("Yuna")), voices[0] if voices else None)
            ok, duration = False, 0
            if voice and shutil.which("ffprobe"):
                with tempfile.TemporaryDirectory(prefix="video-skill-tts-") as tmp:
                    audio = Path(tmp) / "check.aiff"
                    rc, _, _ = run(["say", "-v", voice, "-o", str(audio), "안녕하세요. 영상 제작 준비를 확인합니다."], 20)
                    if rc == 0 and audio.exists() and audio.stat().st_size > 4096:
                        prc, probe, _ = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(audio)])
                        try:
                            duration = float(json.loads(probe)["format"]["duration"])
                            ok = prc == 0 and duration > 0.2
                        except (ValueError, KeyError, TypeError):
                            pass
            report["checks"]["system_korean_tts"] = {"ok": ok, "voice": voice, "duration_seconds": duration, "optional": True}
            if not ok:
                report["actions"].append("System voice is unavailable or returned empty audio. Use host-approved execution or provide another voice; do not treat an existing file as successful speech.")
    report["manual_checks"] = ["Confirm actual source recording exists and has no unwanted personal information.",
                               "Confirm the selected host can invoke its model; login-status alone does not prove it."]
    if args.mode == "canva":
        report["manual_checks"] += ["Confirm actual capture provenance and a Korean font file.",
                                    "Review capture images, scene audio, and final MP4 playback."]
    report["status"] = "missing_required_tools" if missing else ("prerequisites_need_attention" if report["actions"] else "prerequisites_checked_runtime_not_verified")
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
