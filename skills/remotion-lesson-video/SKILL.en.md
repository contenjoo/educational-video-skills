# Remotion lesson videos

[한국어](SKILL.md) · English

Create educational videos that let learners complete a real task from actual screen recordings. Use the same workflow in Claude and Codex without assuming a specific OS, account, voice, recorder or personal path.

## Start and resume

- Run `python3 scripts/preflight.py --mode remotion --network` from this skill folder. Add `--tts` only for the macOS Korean system voice; other systems do not require `say`. A prerequisite check is not production success.
- Identify the audience, task, outcome, language, duration, source media and requested deliverables. Prioritize the task over a fixed runtime. Ask only about consequential missing information and state reasonable assumptions.
- Read existing files and progress records. Reuse recordings, audio and subtitles that do not need changes.
- Confirm terminal/file access, supported recording tools, audio sources and a working Remotion environment. Without execution tools, prepare scripts and scene plans and identify missing inputs. Skill installation grants no tools or account access.
- For setup/rendering, read [production](references/production.en.md). Preserve existing package versions and commands.
- On failure, use [first-run troubleshooting](references/first-run.en.md). Identify whether authentication, networking, audio or rendering is blocked; do not repeat the same failure or deliver a silent substitute as a finished lesson.

## Real screen media and lesson design

1. Perform the actual task and verify its saved result. Record differences caused by menu names, permissions or plan tiers. Do not invent account-specific features.
2. Use actual recordings of input, clicks, menus, dragging and cursor movement. Still images with simulated cursors are not recordings. Preserve an explicitly requested slideshow format and label it accurately.
3. Capture only needed windows/tabs using fictional practice data without personal information. If capture tools or permissions are missing, use supplied footage or list required clips.
4. Structure scenes as task → actual operation → result check → practice time. Remove dead time and mistakes while preserving cause and effect.
5. Zoom only as needed for legibility. Prefer the recorded cursor. Confirm requested highlight rectangles against the same frame, resolution and zoom; remove them at screen transitions.

## Narration, captions and editing

- Use the user's recording or available TTS. Do not require a particular paid provider or personal voice. Voice cloning requires authorization to use that voice.
- Separate pronunciation text from display text where helpful. Remove production notes from learner-facing content.
- Align scenes and short meaningful subtitle segments to the actual audio, not character-count estimates. Correct menu names, proper nouns and line breaks.
- Use Remotion frame time for recordings, audio, captions and zoom. Verify components against documentation for the installed version. Calculate animation from frames rather than CSS time or uncontrolled randomness.
- Localized versions retain learning objectives and task order while aligning localized menus, narration and subtitles. Subtitle translation alone is not complete localization.

## Review and delivery

Review representative scenes before a long render. This does not require routine user approval; continue within the authorized request.

Use [quality checks](references/quality.en.md). Record technical tests, automated audio comparisons and human playback/listening separately. Never mark an unperformed check as passed. After edits, review the exact final file identified by its hash.

Deliver requested MP4, subtitles, script, project sources and reproduction commands; add thumbnails/chapters when needed. File generation, uploads, publication and course replacement are distinct actions within the user's requested scope, each requiring verification of the actual result.
