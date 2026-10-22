# First-run troubleshooting

[한국어](first-run.md) · English

- `No module named PIL`: install Pillow into the exact Python used to run the renderer, including the selected virtual environment.
- Missing FFmpeg/FFprobe: install through a system package manager and check PATH. This workflow does not require Node.js.
- Font errors or missing-glyph boxes: choose a font supporting the production language and visually inspect `--frames`.
- Review SHA mismatch: an image or audio file changed. Inspect the actual revision and update the real record; do not remove validation.
- Successful system voice command but empty audio: restricted macOS execution may produce an empty file. Check actual FFprobe duration and stream; use normal required approval or supplied narration.
- Claude/Codex authentication or model errors: use normal login and a supported model without silently changing global or security settings.
- Connector account differs from browser account: verify the source account. This workflow needs no editor timeline or media upload.
- Text does not fit: split scenes and shorten summary captions. Preserve full narration in subtitles and script.

## Recording blocked while verifying the browser URL

- A readable window title does not establish a verified current URL. Report `capture blocked before start / Remotion render not attempted`, rather than concluding that Remotion is unavailable. Without diagnostic logs, leave the internal cause unknown.
- Preserve the tool's URL trust checks and security settings. Stop automatic capture when the same error repeats. Do not repeatedly request reopened windows, a single remaining tab, or app updates without evidence. Retry only when a meaningful diagnostic change supports it.
- If the user supplies recorded footage, inspect its duration, video stream, required real actions and private information, then edit it locally without browser control. Chrome or the recorded site need not remain open. If footage is missing, request a short recording of the required actions and report capture as pending until it exists.
- Respect an explicit silent, captioned-video request: do not require TTS or supplied narration. Check a Remotion result with `python scripts/check_media.py lesson.mp4 --silent --srt lesson.srt --expected-text captions.txt`, where `captions.txt` contains the approved full display text. This option must not bypass audio checks for a narrated lesson. The screenshot-only `render_lesson.py` still requires narration inputs; do not claim that it supports silent production.
- When asked to repair the host tool, collect product/tool versions, the exact error and whether recording began. A successful test on another computer does not prove that the affected Windows host has recovered.
