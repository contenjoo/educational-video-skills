# v3 regression validation · 2026-10-21

[한국어](VALIDATION.md) · English

This update converts observed production failures into workflow decisions and technical checks. Private transcripts, voices and screenshots are not distributed.

- Twelve unit/installation regressions passed: full text preservation when splitting long narration, rejected zero/overlapping/missing/out-of-range subtitles, BOM/CRLF SRT, invalid geometry, stale preview reviews and existing-output/installation preservation.
- Actual negative fixtures were executed: a caption changed after review, an out-of-bounds crop and a genuinely silent WAV each failed --validate; valid inputs passed.
- Claude Code actually read both installed skills and production-checks guidance, generated screenshot previews, visually inspected them, recorded truthful AI review hashes, validated and rendered. It caught a clipped menu label and a rectangle crossing resize controls, corrected them and reviewed a new preview.
- Codex desktop executed the installed screenshot workflow and incorporated the visual corrections found during the Claude run, then re-reviewed and re-rendered. Both used the same three existing actual capture frames and supplied narration. They did not independently generate fresh capture/audio.
- Both new screenshot outputs are 17.788s, 1920×1080 H.264/AAC with four SRT cues. Full decode, complete display-transcript preservation and audio checks passed without errors/warnings. Both hosts also executed the new shared MP4/SRT checker on the existing 50.112s Remotion output; it passed. No fresh Remotion render was produced in this regression run.
- This added validation did not include full player playback, human full-length listening, pronunciation approval or public replacement. Keep the earlier 20 October playback evidence separate from this code regression run. Preview SHA validation detects changed files; it cannot externally certify reviewer judgment or semantic correctness.

New screenshot MP4 SHA-256:
- Claude Code: `0bfb4298fb79832878cbb88c9f7c43c1d17ab85488c2241b6830e76779eda4a7`
- Codex desktop: `0bfb4298fb79832878cbb88c9f7c43c1d17ab85488c2241b6830e76779eda4a7`

The same inputs and corrected frame compositions produced the same final hash. These are not counted as independent fresh captures. Both standalone ZIPs are checked for Korean/English instructions, bundled tools and Claude/Codex installation.

---

# Usage validation · 2026-10-20

[한국어](VALIDATION.md) · English

These are short real-screen educational video samples tested on one macOS environment. They do not guarantee error-free operation for every OS, account or app. Human full-length listening and pronunciation approval were not performed.

| Host | Workflow | Actual output | Execution scope |
| --- | --- | --- | --- |
| Claude Code 2.1.296 | Remotion | 50.112s MP4, SRT, script and sources | Actual CLI production and rendering |
| Codex desktop | Remotion | 32.043s MP4, SRT, script and sources | Initial CLI limitations; desktop completed TTS, npm and rendering through individually approved commands |
| Claude Code 2.1.296 | Python/Pillow/FFmpeg screenshots | 21.688s MP4, SRT, script, inputs and receipt | CLI read the skill, authored inputs, corrected crop/highlights and rendered |
| Codex desktop | Python/Pillow/FFmpeg screenshots | 17.788s MP4, SRT, script, inputs and receipt | Used the installed skill and bundled renderer |

## Shared inputs and checks

Recorded actual actions adding a text box, entering fictional classroom news and changing text size. Remotion used the recording; the screenshot workflow used three frames extracted from it. The test coordinator generated Korean system-voice scene audio in advance and supplied the same inputs to both screenshot runs. This was not independent end-to-end fresh capture and TTS generation in each host.

All four outputs had video/audio stream checks, full decoding and actual player playback. All screenshot output frames were visually inspected by AI for text rendering, crop, highlight positions and source agreement. Playback completion, unmuted output and no player errors are not human full-length listening. Subtitles follow speech but complete word-level alignment is not guaranteed. Wrapped text was not described as a successful single-line result. Short execution tests do not establish full-length course readiness.

## Findings incorporated

- Version 1 misinterpreted the second workflow as editor-based video editing. That work stopped and was replaced with screenshot/Python/FFmpeg production. Private test drafts were preserved and excluded from the result matrix.
- The Codex CLI had an unsupported host-specific model alias and restricted npm DNS/system-voice execution. Global settings were preserved; individual commands ran through normal approval. This is not counted as a fully independent CLI success.
- Claude required normal authentication refresh before actual production.
- The renderer rejected an out-of-bounds crop in Claude's first preview. Only affected coordinates were fixed; later highlight overlap and bottom clipping were corrected by viewing actual frames.
- Installation now refuses collisions by default and provides backup-based `--update`; user-file preservation was tested.
- Preflight checks actual audio duration rather than trusting a successful system-voice exit code.

## Distribution checks

Checked both skill entry points, UI metadata, relative references and public content. Built standalone ZIPs and tested installation/backups, invalid crop/highlight rectangles, stale image-review hashes and existing-output protection. CI reproduces structure and unit checks, not login, recording, TTS or playback.

Original screen media, account details, authentication logs and test videos are excluded from the public repository and ZIPs. Final-file SHA-256 identifiers follow.

- Claude Code · Remotion: `8d7dfd0ec9f665e9ea5ebe9262f55cf10a37f62f92306dbbe3e37f4be28e6123`
- Codex 데스크톱 · Remotion: `87be7f791583528038182d7d307dd8bb22f0cde84990339c5e716ee0a06bfad1`
- Claude Code · 캡처 기반: `513d437b890ec2d14077bb63c8f66f8c11b5115aa27b9d17da772e1748e48731`
- Codex 데스크톱 · 캡처 기반: `ad8f7f52f8a28d40733e78bcc2e041d018d20f8db161777ab388d13fad4e9483`
