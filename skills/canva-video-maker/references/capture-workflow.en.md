# Running and lesson.json

[한국어](capture-workflow.md) · English · [日本語](capture-workflow.ja.md)

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
    "preview_review": {
      "approved": false,
      "reviewed_by": "Actual final-card reviewer",
      "reviewed_at": "Actual review timestamp",
      "sha256": "Exact reviewed PNG SHA-256 from preview.json"
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

The final render.json status is `rendered_pending_playback_review`. Do not mark unperformed full listening as approved. Default subtitle times are estimated within each scene's actual speech; refine using verified timing or forced alignment.


## v3 preview review and subtitles

`--frames` writes final card PNGs and preview.json with their hashes. Inspect every card for target meaning/position, language, clipping, whitespace and privacy. Only after inspection set each scene's `preview_review.approved`, actual reviewer/time and exact PNG SHA. This is a review record, not a command to approve automatically. `--validate` now generates cards in memory and rejects missing/stale preview review or invalid crop/highlight geometry. Changing title, caption, source, font, order or highlights changes the rendered card hash and requires review. This new required field is the migration from v2; do not copy old approval without viewing the new frame.

The renderer now writes short SRT phrases plus narration.txt and checks that all approved narration text survives. Default phrase times are estimated within measured scene audio and explicitly marked as estimates. For actual aligned timing, provide each scene's optional `subtitles` list, e.g. `[{"start": 0.0, "end": 1.4, "text": "Open the text menu."}, {"start": 1.4, "end": 3.2, "text": "Select Add a text box."}]`. Text must cover that scene's entire approved display narration, with positive increasing non-overlapping times within speech duration. Do not fabricate alignment times. `subtitle_max_chars` defaults to 42, accepts 10–120 and controls automatic phrase length; adapt to the language/layout.

The final render runs the bundled media/subtitle checker once and embeds its result in render.json. Silence/empty audio fails; word omissions, zero/overlapping cue intervals and truncated subtitles fail. Readability warnings still need review. It never modifies speech speed or inserts pauses inside narration. See [production checks](production-checks.en.md) for remaining manual checks and destination verification.
