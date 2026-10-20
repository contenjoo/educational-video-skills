# Project setup and rendering

[한국어](production.md) · English

## Environment

Confirm a terminal, Node.js, package manager and working browser renderer. Check current OS/Node support in the [official docs](https://www.remotion.dev/docs/). Preserve an existing lockfile and keep `remotion` and all `@remotion/*` packages on compatible matching versions. Do not install globally or upgrade an existing project without reason.

For a new project, use the official generator, such as `npx create-video@latest` when supported by current documentation, under the host's execution/network policy. Choose a new writable folder, inspect existing files and generator questions, and select only what the lesson needs. The [official Remotion skill](https://www.remotion.dev/docs/ai/skills) may help with code but is not mandatory.

## Structure and timing

```text
lesson-project/
  src/               compositions, scenes, subtitles and zoom
  public/media/      actual footage, audio and licensed visuals
  content/           objectives, script, timeline and provenance
  output/            final MP4 and SRT
  qa/                hashes, technical checks and playback records
```

Preserve original media. Record each capture's screen, date, language, actual actions and used ranges. Never store signed media URLs or credentials in sources.

Record scene IDs, source ranges, start/end frames, audio files, speech/subtitle timing, zoom and practice holds. Specify time units and fps, accounting for different trim offsets. Avoid overlapping narration or cutting speech at scene ends.

## Run

Prefer project scripts. A typical new-project invocation is below; replace entry point and composition ID with actual values.

```bash
npx remotion studio src/index.ts
npx remotion render src/index.ts Lesson output/lesson.mp4
```

Check arguments and media components against [current documentation](https://www.remotion.dev/docs/). Render a short real-content segment before a long render. Do not fabricate operations when actual footage is missing.

Diagnose the logged cause. Reduce concurrency for CPU/memory pressure; investigate a writable project cache or supported cache-disable option for cache permission failures. Do not default to removing sandbox protections or changing permissions.

Record package versions, install/render commands and input/output paths so another user can replace media and narration and reproduce the workflow.
