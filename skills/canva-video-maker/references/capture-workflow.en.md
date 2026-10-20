# Running and lesson.json

[한국어](capture-workflow.md) · English

A lightweight implementation of an existing capture → script → narration → Pillow → FFmpeg production workflow. It excludes private branding, course lists, publication permissions and fixed-voice rules.

## Setup and run

Set `SKILL_DIR` to the installed skill's absolute path and work in a new project folder. Adapt paths directly in Windows PowerShell.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
python3 "$SKILL_DIR/scripts/preflight.py" --mode canva
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --frames --output preview
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --validate
.venv/bin/python "$SKILL_DIR/scripts/render_lesson.py" lesson.json --output output
```

Install FFmpeg/FFprobe through a system package manager. Set `font` to your own font supporting the production language. Fonts and Pillow are neither bundled nor automatically downloaded. Windows venv Python is `.venv/Scripts/python.exe`. Use the same Python that has Pillow installed, including for preflight.

`--frames` permits previews without audio/review approval but does not produce a final video. `--validate` checks actual images, review records, SHA and audio provenance without output. If an output directory exists, choose a new path. Default output is 1920×1080, 30fps, H.264/AAC. Split long scenes rather than accelerating speech.

## Input

This is a format example, not review or generation evidence. Replace every placeholder with actual files and records. Paths are relative to lesson.json. Compute SHA-256, for example with `hashlib.sha256(Path(...).read_bytes()).hexdigest()`.

```json
{
  "schema_version": 1,
  "title": "Add a text box",
  "font": "fonts/YourFont.ttf",
  "scenes": [{
    "image": "images/01.png",
    "caption": "Add a text box.",
    "narration": "Open the text menu and select Add a text box.",
    "audio": "audio/01.wav",
    "hold_seconds": 1.2,
    "capture": {
      "kind": "actual_screen_capture",
      "source": "Actual capture tool or source file and time range",
      "captured_at": "Actual capture timestamp"
    },
    "image_review": {
      "approved": false,
      "reviewed_by": "Actual reviewer",
      "reviewed_at": "Actual review timestamp",
      "sha256": "Reviewed image SHA-256"
    },
    "audio_provenance": {
      "provider": "Own recording or actual TTS provider",
      "generation_id": "Actual recording session or generation job ID",
      "sha256": "Actual audio SHA-256"
    },
    "crop": [0, 0, 1280, 720],
    "highlights": [[75, 180, 200, 55]]
  }]
}
```

`crop` and `highlights` are optional x/y/width/height pixel rectangles. Crop uses original-image coordinates; highlights use the **cropped image**. Out-of-bounds rectangles are rejected. The renderer preserves aspect ratio, places a short caption below the image and writes full narration to SRT and script. Add highlights only to verified actual targets.

Use `actual_screen_capture` for direct screenshots or `actual_recording_frame` for real recording frames. Provenance is a supplied source statement, not remote authentication by the renderer.

The final render.json status is `rendered_pending_playback_review`. Do not mark unperformed full listening as approved. Subtitle times span each scene's actual speech; split long narration into sentence scenes or refine using forced alignment.
