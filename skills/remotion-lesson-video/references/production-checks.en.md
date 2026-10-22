# Production checks drawn from actual failures

[한국어](production-checks.md) · English · [日本語](production-checks.ja.md)

These rules translate observed production and conversation failures into decisions and checks. No private accounts, voices, paths or course originals are required.

| Failure | Apply during this task | Limit of automation |
| --- | --- | --- |
| Misreading an existing project as another production method | Read its actual README, current inputs and render commands. State the chosen method and deliverables in one sentence; do not infer an editor workflow from a product name. | Method selection depends on the request and actual media. |
| Scaling and estimating from an easy pilot | Finish a short complete lesson and a representative scene involving menus, permissions or multiple clicks before a batch. Continue already authorized batch work after incorporating necessary fixes. | A single render time is not the total capture, narration, review and publishing estimate. |
| Empty number slots, marks beside controls or on vanished controls | Keep clean sources and overlays separate. Preserve before-click and result states. Use numberless rectangles around the actual control at the explained moment; reflow cards and whitespace after removing numbers. | Geometry and preview hashes cannot certify that a box identifies the semantically correct control. Inspect the actual screen. |
| Portrait crops hiding menus or overlapping explanations | Inspect every distinct marked state and its transitions at real output size. Keep zoom/masking from obscuring needed controls or speech context. | A few sampled frames do not establish review of every state. |
| Translated video but untranslated documents, menus or folders | Define video, SRT, display/pronunciation scripts, documents, folders and actual menu wording as one localized delivery package. | A valid font path does not prove correct glyphs, wrapping or Arabic/other RTL shaping and reading order. Inspect rendered output. |
| Keeping identical audio but overlooking original speech defects | Verify a short voice sample, then check the final MP4 as well as source audio for omissions, repetition, cuts, silence and pronunciation. Use manageable scenes/batches for unreliable long generation; inspect existing results before retrying failed pieces. | Hash equality, signal/transcription checks and loudness are not natural pronunciation or full-listening approval. |
| Arbitrary pauses inside speech or a vanished zero-duration subtitle phrase | Do not cut speech or alter playback speed to fit time. Add needed holds only at measured silence or sentence ends. Compare the approved display transcript with all final subtitle text and intervals. | Automatic timing estimates are not forced alignment. Check preservation of every phrase and actual playback separately. |
| Wrong course title, count or next-lesson announcement | Derive cover, introduction, conclusion and next lesson from one confirmed curriculum and compare speech meaning with the actual screen. | A valid media container can teach the wrong thing. |
| Unicode-name mismatch or FFmpeg consuming batch input | Normalize names to NFC for comparison while preserving originals. Use FFmpeg -nostdin and subprocess DEVNULL for batch operations. | Matching names prove neither file content nor upload/playback. |
| Confusing authentication/model/network/environment failures with skill failures | Separate inference, account access, Python/Pillow, npm connectivity, TTS and rendering. Use normal approval without silently changing global/security settings. | Successful process exit does not prove usable media. |
| Confusing a local repair or upload with the learner-facing version | For each requested destination, preserve IDs, URLs and learner progress, read back the replacement and play the relevant individual course, integrated site, Drive or mobile page. Retire old assets only after replacement verification and within authorized scope. | Re-encoded hosted media may have another hash. Record local SHA plus destination asset/version, duration and the corrected visible scene. |
| Paperwork and repeated checks overtaking production | Add only necessary facts to existing input, render and review records. Reuse shared tools; rerun checks only after relevant changes or new findings. | Do not multiply per-lesson scripts, duplicate evidence files or unnecessary cross-approval rituals. |

## Check final media

Both skills bundle the standalone `scripts/check_media.py`. It needs Python's standard library and FFmpeg/FFprobe.

```bash
python3 "$SKILL_DIR/scripts/check_media.py" output/lesson.mp4 --srt output/lesson.srt --expected-text output/narration.txt --output qa/media.json
```

`--expected-text` is the **approved full display transcript**, without headings, lesson numbers, timestamps or Markdown. If pronunciation text differs, use the written subtitle form. Extract the actual narration from a headed script first. The screenshot renderer exports this file and runs the same check during rendering; do not repeat unchanged checks. For Remotion, provide the existing project's exported MP4, SRT and approved transcript.

Checks include full decode, video/audio streams, valid duration, effectively empty audio and missing/repeated/overlapping/zero-length/out-of-range subtitles. Long lines or intervals are **warnings** requiring language/layout review; adjust the line-length warning with `--max-line-chars`. Even success is `technical_checks_passed_pending_review`. Pronunciation, semantic screen/speech agreement, human full-length listening and published-version verification are never automatically passed.

## Report results

Consolidate source inputs and supplied intermediate media, actual commands, final SHA, checks/warnings, observed playback ranges, unperformed reviews and destination-specific state into the existing completion report. Distinguish local render, upload, destination replacement and public playback. Do not label assisted execution as independent end-to-end success. Estimate capture, voice, render, review and publishing separately from external waiting; do not guarantee uncertain timing.

A failure report must distinguish a user-reported symptom, a locally reproduced defect, a recorded repair and a verified live replacement. Use actual logs/files before attributing a cause. Unresolved warnings are not a completed quality review; record why an inspected warning is acceptable.
