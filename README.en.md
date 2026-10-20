# Educational Video Skills

**[한국어](README.md) · [English](README.en.md)**

Two skills for Claude and Codex that turn real screen media, scripts and narration into educational videos.

| Workflow | Best for | Deliverables |
| --- | --- | --- |
| [Remotion lessons](skills/remotion-lesson-video/SKILL.en.md) | Editing actual screen recordings, zoom and motion, multiple lessons and languages | MP4, SRT, script, editable project and review records |
| [Screenshot lessons](skills/canva-video-maker/SKILL.en.md) | Explanations using real screenshots, highlights and scene narration | MP4, SRT, script, inputs and render receipt |

Free to use, modify and redistribute under MIT. No personal accounts, API keys, fixed voices or existing course originals are included. These are independent production workflows.

## v3: incorporating production failures

Both skills now include Korean and English guidance based on observed method misunderstandings, empty number slots, misplaced highlights, audio/subtitle omissions, optimistic estimates, incomplete localization/folders and unverified public replacements. Inspect the original project, finish a short complete sample plus a difficult representative scene, then scale and verify each requested destination.

Both ZIPs bundle `scripts/check_media.py` for final decoding, audio, subtitle intervals and approved transcript preservation. Human listening, semantic agreement and published-version verification remain unverified. These checks cannot prevent every failure or guarantee 100% completion.

**Upgrading from v2:** the screenshot renderer now requires a per-scene `preview_review`. Inspect the actual `--frames` PNGs before recording their hashes from preview.json. Changed text, highlights or layout invalidate old preview approval. Long narration is split into readable SRT phrases; default phrase times are explicitly estimated. See [input/migration instructions](skills/canva-video-maker/references/capture-workflow.en.md) and [production checks](skills/remotion-lesson-video/references/production-checks.en.md). Existing identifiers and Claude/Codex installation paths are preserved.

## Requirements

- Both: real source media, your own recordings or available TTS, and the necessary file, terminal and browser tools.
- Remotion: Node.js, npm, a working render browser, FFmpeg and FFprobe.
- Screenshots: Python 3.9+, Pillow, FFmpeg/FFprobe and a font supporting the production language.

Installing a skill does not grant tools or account permissions. Without execution tools, the assistant prepares scripts and scene plans and reports unfinished work. Check the terms and costs of services, media and fonts you use.

## Install in Claude Code and Codex

Use Python 3.9+ and Git. By default, installation refuses to overwrite existing skills with the same identifiers.

```bash
git clone https://github.com/contenjoo/educational-video-skills.git
cd educational-video-skills
python3 scripts/install.py --target both --dry-run
python3 scripts/install.py --target both
```

For one host, select `--target claude` or `--target codex`. On Windows, use `python` if `python3` is unavailable.

| Host | User install | Project install |
| --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |

For project-only installation, specify the project's absolute path.

```bash
python3 scripts/install.py --target both --scope project --project /path/to/your-project
```

Updates back up existing skills to the host's `skill-backups/` before installing. Backups are not automatically deleted.

```bash
git pull --ff-only
python3 scripts/install.py --target both --update
```

Start a new conversation after installation. Check other skill search paths for duplicate identifiers. Official instructions: [Codex](https://developers.openai.com/codex/skills/), [Claude Code](https://code.claude.com/docs/en/skills).

## Install in Claude web or desktop

1. Get the two individual skill ZIPs from the [latest release](https://github.com/contenjoo/educational-video-skills/releases/latest).
2. Upload and enable each ZIP in the custom skills interface. See the [official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
3. Check available terminal, file and browser tools, then request a video.

Use individual skill ZIPs rather than the full repository ZIP. Each contains a top-level skill folder, `SKILL.md`, and Korean and English instructions. Actual rendering depends on app and organization capabilities.

## Check prerequisites

For Remotion:

```bash
python3 skills/remotion-lesson-video/scripts/preflight.py --mode remotion --network
```

For screenshots, install Pillow in a virtual environment and run the check with that same Python:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "Pillow>=10,<13"
.venv/bin/python skills/canva-video-maker/scripts/preflight.py --mode canva
```

On Windows, the virtual environment interpreter is `.venv/Scripts/python.exe`. Add `--tts` only when testing the macOS Korean system voice. Passing prerequisites does not prove login, production or playback success.

## Use

In Codex:

```text
$remotion-lesson-video
Create a beginner lesson from my real screen recording.
Include English narration, subtitles and time to practice.
```

```text
$canva-video-maker
Explain how to add a text box using my actual screenshots.
Use Python/Pillow and FFmpeg, narration, subtitles and rectangular click highlights.
```

In Claude Code, invoke `/remotion-lesson-video` or `/canva-video-maker`. In web or desktop apps, enable the skill and describe your goal. Published command and folder identifiers are retained for installation compatibility.

## Validation and production principles

Distinguish actual recordings from still screenshots. No fixed voice service is required. In the screenshot workflow, confirm the screen before finalizing narration and reuse the bundled renderer. Record automated checks, actual playback and human full-length listening separately. Publishing, sharing and replacing existing courses require the corresponding user request.

Both workflows produced real MP4s in Claude Code and Codex desktop. See the [usage validation record](VALIDATION.en.md) for assisted steps and review limits. Not every OS, account or app combination was tested; human full-length listening was not performed. Version 2 corrected the second workflow from an earlier mistaken editor-based interpretation to screenshot-based production.

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

These commands check structure, relative links, public content, installation backups and input protection, and build two ZIPs in `dist/`. They do not certify login, TTS, capture, rendering or playback.

Report problems through [Issues](https://github.com/contenjoo/educational-video-skills/issues). Do not include passwords, API keys or student personal information.

## License

[MIT](LICENSE) applies to the skills, documentation and tools in this repository. External services, recordings, fonts, visuals and voices remain subject to their owners' rights and terms.
