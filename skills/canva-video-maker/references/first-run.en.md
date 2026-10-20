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
