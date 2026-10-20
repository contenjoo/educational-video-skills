# Screenshot lesson videos

[한국어](SKILL.md) · English

Use real screen captures → confirm the screen and finalize the script → scene narration → Pillow cards → FFmpeg encoding → playback review. This is a portable version of an existing educational production workflow, not a copy of private course assets or course-specific rules. Use the bundled Python renderer locally.

## Start

- Confirm audience, learning outcome, duration, language and source media. Explain only verified features and preserve existing user work.
- Require Python 3.9+, Pillow, FFmpeg/FFprobe and a font supporting the production language. Run `scripts/preflight.py --mode canva` from the skill folder; this mode name is retained for compatibility. Read [workflow and schema](references/capture-workflow.en.md).
- Apps without a working terminal can prepare inputs but cannot claim a rendered result. Do not assume specific connector names, personal paths or voices.

## Screens and script

1. Use actual screenshots/recordings supplied by the user or obtained through supported browser tools. Record the source and time range when extracting recording frames. Label a still-image sequence as screenshot-based video.
2. Mask personal information and crop for legibility. Mark actual click targets with numberless rectangles. Do not describe obscured menus, failed operations or wrapped text as successful results.
3. Approve `image_review` only after inspecting the exact image and recording its SHA-256. Never invent reviewers, timestamps or capture evidence.
4. Explain one task per scene using short, natural sentences. Include checks, practice time and result verification. Remove irrelevant production notes and tooling remnants from learner-facing screens.

## Audio and render

- Use the user's recording or selected TTS. If using a provider, verify available models/voices and retain actual generation records. Do not require a private paid voice or account.
- Prepare scene audio with file hashes and real provenance. Check missing speech, silence, misread words and spoken control tags. Preserve playback speed; add practice holds after speech instead.
- Reuse `scripts/render_lesson.py` rather than writing a renderer for each lesson. Run `--frames`, inspect images, then `--validate` and final render. Existing outputs are never overwritten.
- The bundled renderer produces still-image scenes, highlights, narration, summary cards and separate full-narration SRT. If continuous recording edits or complex movement are essential, suggest the Remotion workflow. Respect an explicit request to keep this workflow.

## Review and delivery

Use [quality checks](references/quality.en.md) for decoding, dimensions, audio, subtitle bounds and beginning/middle/end playback. SRT uses scene audio boundaries rather than word-level alignment. Refine with transcription/forced alignment where available, otherwise report the limitation. Separate automated checks, AI visual inspection and human full-length listening.

Deliver MP4, SRT, script, lesson.json, capture/audio inputs and the render receipt. Local production is the default completion scope. Uploading, publishing and replacing courses require the corresponding request. Troubleshoot specific failures using [first-run guidance](references/first-run.en.md).
