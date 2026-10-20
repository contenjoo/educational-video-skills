# Final video review

[한국어](quality.md) · English

Evaluate file integrity and the learner's ability to complete the task separately.

| Check | Inspect | Limit |
| --- | --- | --- |
| Task | Actual actions and saved outcome | Menu presence alone is not task success |
| File | SHA, duration, resolution, fps, video/audio streams | A valid container does not prove correct teaching |
| Full decode | Decode video/audio through the end | Not human full-length viewing |
| Visuals | Click targets, zoom, cursor, text size, overlaps and result | Distinguish sampled frames from full viewing |
| Audio | Missing/repeated/cut speech, silence, loudness and peaks | ASR does not certify natural pronunciation |
| Subtitles | Audio alignment, menu names, omissions, breaks and scene bounds | Summary cards are not full speech captions |
| Human playback | Actual intervals and listening performed | Mark unperformed full listening/device review as unperformed |

```bash
ffprobe -v error -show_format -show_streams -of json output/lesson.mp4
ffmpeg -v error -i output/lesson.mp4 -f null -
```

Adapt paths to actual files. Without these tools, report available player/metadata checks rather than guessing results. Use EBU R128 or another suitable measure for loudness; average dB is not LUFS. Set targets for the destination and voice. Black/silent segments may be intentional and require interpretation.

Record final SHA-256, check time, commands/tools, scope, findings and unperformed checks. Compute hashes with tools such as Python hashlib. A changed video needs review tied to its new hash.

For the shared final-file/SRT/transcript checker, warning handling and destination-specific readback, follow [production checks](production-checks.en.md). These technical checks never certify pronunciation or a published replacement.
