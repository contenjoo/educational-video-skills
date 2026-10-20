#!/usr/bin/env python3
"""Portable capture -> Pillow cards -> FFmpeg video, SRT and script renderer."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageOps


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(f.read()).hexdigest()


def run(argv):
    return subprocess.run([str(x) for x in argv], check=True, capture_output=True, text=True).stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]))


def local(base, value):
    path = (base / value).resolve()
    if not path.is_file():
        raise ValueError('Missing local input: ' + str(path))
    return path


def load(path, final=False):
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema_version') != 1:
        raise ValueError('schema_version must be 1')
    if not data.get('title') or not data.get('scenes') or len(data['scenes']) > 60:
        raise ValueError('A title and 1-60 scenes are required')
    font = local(path.parent, data['font'])
    ImageFont.truetype(str(font), 30)
    for scene in data['scenes']:
        if not scene.get('caption') or not scene.get('narration'):
            raise ValueError('Each scene needs caption and narration')
        image = local(path.parent, scene['image'])
        with Image.open(image) as im:
            im.verify()
        scene['_image'] = image
        if final:
            capture, review = scene.get('capture', {}), scene.get('image_review', {})
            if capture.get('kind') not in ('actual_screen_capture', 'actual_recording_frame'):
                raise ValueError('Final output requires actual captures, not synthetic test images')
            if not capture.get('captured_at') or not capture.get('source'):
                raise ValueError('Missing real capture date/source')
            if review.get('approved') is not True or not review.get('reviewed_by') or not review.get('reviewed_at') or review.get('sha256') != sha(image):
                raise ValueError('Image review missing or stale; review this exact image')
            audio = local(path.parent, scene['audio'])
            provenance = scene.get('audio_provenance', {})
            if provenance.get('sha256') != sha(audio) or not provenance.get('provider') or not provenance.get('generation_id'):
                raise ValueError('Missing/mismatched audio provenance')
            metadata = probe(audio)
            if not any(s['codec_type'] == 'audio' for s in metadata['streams']):
                raise ValueError('Audio stream missing')
            duration = float(metadata['format']['duration'])
            if not math.isfinite(duration) or duration <= .2:
                raise ValueError('Audio is empty or too short')
            hold = float(scene.get('hold_seconds', 1.2))
            if not math.isfinite(hold) or not 0 <= hold <= 60:
                raise ValueError('hold_seconds must be between 0 and 60')
            scene.update(_audio=audio, _speech=duration, _duration=math.ceil((duration + hold) * 30) / 30)
    data['_font'] = font
    return data


def wrap(draw, text, font, width):
    # Character wrapping also handles Korean and long English words.
    lines, line = [], ''
    for char in text:
        if char == '\n' or (line and draw.textlength(line + char, font=font) > width):
            lines.append(line.rstrip())
            line = '' if char == '\n' else char
        else:
            line += char
    if line:
        lines.append(line.rstrip())
    return lines


def text(draw, value, fontpath, box, size, fill):
    x, y, width, height = box
    while size >= 18:
        font = ImageFont.truetype(str(fontpath), size)
        lines = wrap(draw, value, font, width)
        if len(lines) * (size * 1.5) <= height:
            break
        size -= 2
    else:
        raise ValueError('Text is too long for the card; split the scene')
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += size * 1.5


def frame(data, scene, index, dest):
    canvas = Image.new('RGB', (1920, 1080), '#f7f8fc')
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1920, 12), fill='#00aeb7')
    text(draw, data['title'], data['_font'], (70, 35, 1780, 100), 48, '#172033')
    with Image.open(scene['_image']) as original:
        original = original.convert('RGB')
        if scene.get('crop'):
            x, y, w, h = scene['crop']
            if min(x, y) < 0 or min(w, h) <= 0 or x+w > original.width or y+h > original.height:
                raise ValueError('Crop is outside the actual image')
            original = original.crop((x, y, x+w, y+h))
        for mark in scene.get('highlights', []):
            x, y, w, h = mark
            if min(x, y) < 0 or min(w, h) <= 0 or x+w > original.width or y+h > original.height:
                raise ValueError('Highlight is outside the cropped image')
            ImageDraw.Draw(original).rounded_rectangle((x, y, x+w, y+h), 6, outline='#00aeb7', width=5)
        shot = ImageOps.contain(original, (1780, 720), Image.Resampling.LANCZOS)
        canvas.paste(shot, ((1920-shot.width)//2, 145+(720-shot.height)//2))
    draw.rounded_rectangle((60, 900, 1860, 1050), 24, fill='#172033')
    text(draw, scene['caption'], data['_font'], (95, 922, 1730, 112), 42, 'white')
    draw.rectangle((0, 1070, round(1920 * (index+1)/len(data['scenes'])), 1080), fill='#00aeb7')
    canvas.save(dest)


def stamp(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'


def render(path, output, frames=False, validate=False):
    data = load(path, final=not frames)
    if validate:
        return {'status': 'inputs_validated', 'scenes': len(data['scenes'])}
    # Never replace existing output, including a failed prior attempt.
    output.mkdir(parents=True, exist_ok=False)
    folder = output / 'frames'
    folder.mkdir()
    for i, scene in enumerate(data['scenes']):
        frame(data, scene, i, folder / f'{i+1:03}.png')
    if frames:
        return {'status': 'preview_only', 'frames': len(data['scenes'])}
    timeline, subtitles, script, elapsed = [], [], [], 0
    with tempfile.TemporaryDirectory(prefix='render-', dir=output) as work:
        work = Path(work)
        for i, scene in enumerate(data['scenes']):
            clip = work / f'{i:03}.mp4'
            run(['ffmpeg', '-v', 'error', '-nostdin', '-loop', '1', '-framerate', '30', '-i', folder/f'{i+1:03}.png',
                 '-i', scene['_audio'], '-map', '0:v:0', '-map', '1:a:0', '-t', f"{scene['_duration']:.8f}",
                 '-af', 'apad', '-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '192k', '-c:v', 'libx264',
                 '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', clip])
            timeline.append({'scene': i+1, 'start': elapsed, 'speech_end': elapsed+scene['_speech'], 'end': elapsed+scene['_duration'],
                             'image_sha256': sha(scene['_image']), 'audio_sha256': sha(scene['_audio'])})
            subtitles.append(f"{i+1}\n{stamp(elapsed)} --> {stamp(elapsed+scene['_speech'])}\n{scene['narration']}\n")
            script.append(f"{i+1}. {scene['narration']}")
            elapsed += scene['_duration']
        (work/'concat.txt').write_text(''.join(f"file '{i:03}.mp4'\n" for i in range(len(timeline))), encoding='utf-8')
        run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'concat', '-safe', '1', '-i', work/'concat.txt', '-c', 'copy', '-movflags', '+faststart', output/'lesson.mp4'])
    (output/'lesson.srt').write_text('\n'.join(subtitles), encoding='utf-8')
    (output/'script.md').write_text(data['title']+'\n\n'+'\n\n'.join(script)+'\n', encoding='utf-8')
    run(['ffmpeg', '-v', 'error', '-nostdin', '-i', output/'lesson.mp4', '-f', 'null', '-'])
    info = probe(output/'lesson.mp4')
    receipt = {'status': 'rendered_pending_playback_review', 'input_sha256': sha(path), 'mp4_sha256': sha(output/'lesson.mp4'),
               'duration': float(info['format']['duration']), 'scenes': timeline, 'decode': 'passed',
               'subtitle_alignment': 'scene audio boundaries; word timing not verified',
               'human_listening': 'not_verified', 'media': info['streams']}
    (output/'render.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--frames', action='store_true')
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            parser.error(tool+' is required')
    if not args.output and not args.validate:
        parser.error('--output is required unless --validate is selected')
    try:
        result = render(args.lesson.resolve(), args.output, args.frames, args.validate)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError):
            print(exc.stderr, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
