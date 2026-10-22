#!/usr/bin/env python3
"""Check final media and subtitle integrity; never certify teaching quality or listening."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import unicodedata


def canonical(text):
    return ''.join(c for c in unicodedata.normalize('NFC', text).casefold() if c.isalnum())


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def command(argv):
    return subprocess.run([str(x) for x in argv], stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True)


def probe(path):
    return json.loads(command(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]).stdout)


def audio_peak(path):
    result = command(['ffmpeg', '-v', 'info', '-nostdin', '-i', path, '-vn', '-af', 'volumedetect', '-f', 'null', '-'])
    match = re.search(r'max_volume:\s*(-?inf|[-+\d.]+) dB', result.stderr)
    if not match:
        raise ValueError('Could not measure audio peak')
    return float(match.group(1))


def seconds(value):
    h, m, tail = value.replace('.', ',').split(':')
    s, ms = tail.split(',')
    if int(m) >= 60 or int(s) >= 60:
        raise ValueError('Invalid SRT timestamp')
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000


def parse_srt(body):
    cues = []
    body = body.lstrip('\ufeff').replace('\r\n', '\n').strip()
    for index, block in enumerate(re.split(r'\n\s*\n', body), 1):
        lines = block.splitlines()
        if len(lines) < 3 or lines[0].strip() != str(index):
            raise ValueError('SRT cue indices must be contiguous and contain text')
        match = re.fullmatch(r'(\d{2,}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(\d{2,}:\d{2}:\d{2}[,.]\d{3})', lines[1].strip())
        if not match:
            raise ValueError('Invalid SRT timing line')
        text = '\n'.join(lines[2:]).strip()
        if not text:
            raise ValueError('Empty SRT cue')
        cues.append({'start': seconds(match[1]), 'end': seconds(match[2]), 'text': text})
    if not cues:
        raise ValueError('No SRT cues')
    return cues


def check_subtitles(cues, duration, expected_text=None, max_chars=42):
    errors, warnings, previous = [], [], 0.0
    for i, cue in enumerate(cues, 1):
        start, end = cue['start'], cue['end']
        if not all(math.isfinite(t) for t in (start, end)) or start < 0 or end <= start:
            errors.append(f'Cue {i}: non-positive or invalid interval')
        if start < previous - .001:
            errors.append(f'Cue {i}: overlaps or moves backwards')
        if end > duration + .1:
            errors.append(f'Cue {i}: extends past video/audio duration')
        if any(len(line) > max_chars for line in cue['text'].splitlines()):
            warnings.append(f'Cue {i}: long line; inspect reading fit')
        if end-start > 8:
            warnings.append(f'Cue {i}: long display interval; inspect speech alignment')
        previous = end
    if expected_text is not None and canonical(' '.join(c['text'] for c in cues)) != canonical(expected_text):
        errors.append('Subtitle text differs from the approved display transcript (missing, repeated or changed words)')
    return errors, warnings


def inspect(media, srt=None, expected_text=None, max_chars=42, silent=False):
    metadata = probe(media)
    duration = float(metadata['format']['duration'])
    if not math.isfinite(duration) or duration <= .2:
        raise ValueError('Empty or invalid media duration')
    streams = metadata['streams']
    if not any(s['codec_type'] == 'video' for s in streams):
        raise ValueError('Video stream missing')
    has_audio = any(s['codec_type'] == 'audio' for s in streams)
    if not has_audio and not silent:
        raise ValueError('Audio stream missing')
    errors, warnings = [], []
    peak = audio_peak(media) if has_audio else None
    if silent:
        if peak is not None and peak > -80:
            errors.append('Audible audio found in an explicitly silent deliverable')
    elif peak <= -80:
        errors.append('Audio is silent or effectively empty')
    command(['ffmpeg', '-v', 'error', '-xerror', '-nostdin', '-i', media, '-f', 'null', '-'])
    count = None
    if srt:
        cues = parse_srt(srt.read_text(encoding='utf-8-sig'))
        expected = expected_text.read_text(encoding='utf-8') if expected_text else None
        more_errors, more_warnings = check_subtitles(cues, duration, expected, max_chars)
        errors.extend(more_errors)
        warnings.extend(more_warnings)
        count = len(cues)
    return {'status': 'failed' if errors else 'technical_checks_passed_pending_review',
            'mp4_sha256': sha(media), 'duration': duration, 'audio_peak_dbfs': peak if peak is not None and math.isfinite(peak) else None,
            'full_decode': 'passed', 'subtitle_cues': count,
            'subtitle_text_checked': bool(srt and expected_text), 'errors': errors, 'warnings': warnings,
            'streams': streams, 'human_full_listening': 'not_applicable_silent' if silent else 'not_verified',
            'audio_requirement': 'explicit_silent' if silent else 'narration_required',
            'semantic_screen_speech_agreement': 'not_verified', 'published_version': 'not_verified'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('media', type=Path)
    p.add_argument('--srt', type=Path)
    p.add_argument('--silent', action='store_true', help='Only for explicitly requested silent output; reject audible audio')
    p.add_argument('--expected-text', type=Path, help='Plain approved display transcript, no headings or timestamps')
    p.add_argument('--max-line-chars', type=int, default=42, help='Warning threshold, adapt to language/layout')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if args.expected_text and not args.srt:
        p.error('--expected-text requires --srt')
    try:
        result = inspect(args.media.resolve(), args.srt, args.expected_text, args.max_line_chars, args.silent)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        result = {'status': 'failed', 'errors': [str(exc)], 'human_full_listening': 'not_verified'}
    body = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding='utf-8')
    print(body)
    return 1 if result['status'] == 'failed' else 0


if __name__ == '__main__':
    raise SystemExit(main())
