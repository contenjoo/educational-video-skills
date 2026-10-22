# First run and recovery

[한국어](first-run.md) · English · [日本語](first-run.ja.md)

1. Verify that the host discovers and reads the skill. Produce one short lesson in a new folder and preserve existing courses.
2. Inspect source duration, video stream and actual actions. If footage is missing, request the required capture rather than inventing it.
3. Check required tools and networking before rendering. Do not repeatedly attempt unavailable package installations.
4. For narrated lessons, test one spoken sentence, verifying audio stream, real duration and level. File existence alone does not prove audio generation.
5. Render a short segment containing real footage and the requested captions/audio before completing the whole lesson.

| Observed failure | Recovery |
| --- | --- |
| Logged in but OAuth expired during inference | Use normal host login/refresh, then verify an actual model call; never extract or publish tokens |
| Configured model unsupported by account | Choose a supported model for that run; do not overwrite global settings |
| Registry DNS/network failure | Separate DNS, proxy and host policy; use normal approval rather than disabling protection |
| macOS say denied or producing an approximately 4KB empty file | Check actual FFprobe duration; use approved execution, supplied audio or available TTS |
| Read-only state folder or app-server permission failure | Check required writable host state; do not copy authentication/configuration elsewhere as a bypass |
| Korean keyboard input produces spaces | Use the supported UTF-8 editor input and read back the saved result instead of repeating the same keystrokes |

Preserve partial scripts, sources or silent previews when useful, but explicitly report missing narration or Remotion rendering. An MP4 created with another workflow is not a successful Remotion render.

## Recording blocked while verifying the browser URL

- A readable window title does not establish a verified current URL. Report `capture blocked before start / Remotion render not attempted`, rather than concluding that Remotion is unavailable. Without diagnostic logs, leave the internal cause unknown.
- Preserve the tool's URL trust checks and security settings. Stop automatic capture when the same error repeats. Do not repeatedly request reopened windows, a single remaining tab, or app updates without evidence. Retry only when a meaningful diagnostic change supports it.
- If the user supplies recorded footage, inspect its duration, video stream, required real actions and private information, then edit it locally without browser control. Chrome or the recorded site need not remain open. If footage is missing, request a short recording of the required actions and report capture as pending until it exists.
- Respect an explicit silent, captioned-video request: do not require TTS or supplied narration. Check a Remotion result with `python scripts/check_media.py lesson.mp4 --silent --srt lesson.srt --expected-text captions.txt`, where `captions.txt` contains the approved full display text. This option must not bypass audio checks for a narrated lesson. The screenshot-only `render_lesson.py` still requires narration inputs; do not claim that it supports silent production.
- When asked to repair the host tool, collect product/tool versions, the exact error and whether recording began. A successful test on another computer does not prove that the affected Windows host has recovered.
