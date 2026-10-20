# First run and recovery

[한국어](first-run.md) · English

1. Verify that the host discovers and reads the skill. Produce one short lesson in a new folder and preserve existing courses.
2. Inspect source duration, video stream and actual actions. If footage is missing, request the required capture rather than inventing it.
3. Check required tools and networking before rendering. Do not repeatedly attempt unavailable package installations.
4. Test one spoken sentence, verifying audio stream, real duration and level. File existence alone does not prove audio generation.
5. Render a short segment containing real footage and audio before completing the whole lesson.

| Observed failure | Recovery |
| --- | --- |
| Logged in but OAuth expired during inference | Use normal host login/refresh, then verify an actual model call; never extract or publish tokens |
| Configured model unsupported by account | Choose a supported model for that run; do not overwrite global settings |
| Registry DNS/network failure | Separate DNS, proxy and host policy; use normal approval rather than disabling protection |
| macOS say denied or producing an approximately 4KB empty file | Check actual FFprobe duration; use approved execution, supplied audio or available TTS |
| Read-only state folder or app-server permission failure | Check required writable host state; do not copy authentication/configuration elsewhere as a bypass |
| Korean keyboard input produces spaces | Use the supported UTF-8 editor input and read back the saved result instead of repeating the same keystrokes |

Preserve partial scripts, sources or silent previews when useful, but explicitly report missing narration or Remotion rendering. An MP4 created with another workflow is not a successful Remotion render.
