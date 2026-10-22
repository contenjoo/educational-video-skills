"""Regressions drawn from subtitle omissions and stale layout reviews."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'skills/canva-video-maker/scripts'
sys.path.insert(0, str(SCRIPTS))
import check_media as media
spec = importlib.util.spec_from_file_location('review_renderer', SCRIPTS/'render_lesson.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class SubtitleIntegrity(unittest.TestCase):
    def test_long_narration_is_split_without_losing_words_or_zero_length_cues(self):
        text = '선생님, 먼저 실제 텍스트 메뉴를 눌러 주세요. ' * 8
        cues = r.timed_subtitles(text, 24.9)
        self.assertGreater(len(cues), 2)
        self.assertTrue(all(len(c['text']) <= 42 and c['end']-c['start'] >= .079 for c in cues))
        errors, _ = media.check_subtitles(cues, 24.9, text)
        self.assertEqual(errors, [])
        self.assertEqual(cues[-1]['end'], 24.9)

    def test_explicit_timing_rejects_omission_overlap_and_end_after_speech(self):
        cases = [
            [{'start':0,'end':1,'text':'first'}],
            [{'start':0,'end':1.5,'text':'first'},{'start':1,'end':2,'text':'second'}],
            [{'start':0,'end':1,'text':'first'},{'start':1,'end':3,'text':'second'}],
            [{'start':0,'end':0,'text':'first second'}]]
        for cues in cases:
            with self.subTest(cues=cues), self.assertRaises(ValueError):
                r.timed_subtitles('first second', 2, cues)

    def test_very_short_scene_does_not_silently_drop_subtitles(self):
        with self.assertRaisesRegex(ValueError, 'Too much'):
            r.timed_subtitles(' '.join(['word']*200), .21)

    def test_srt_parses_bom_and_crlf_and_detects_missing_text(self):
        cues=media.parse_srt('\ufeff1\r\n00:00:00,000 --> 00:00:01,000\r\nHello\r\n\r\n2\r\n00:00:01,000 --> 00:00:02,000\r\nworld\r\n')
        self.assertEqual(media.check_subtitles(cues, 2, 'Hello world')[0], [])
        self.assertTrue(media.check_subtitles(cues[:1], 2, 'Hello world')[0])

    def test_long_cue_warns_without_claiming_linguistic_alignment(self):
        errors,warnings=media.check_subtitles([{'start':0,'end':10,'text':'x'*90}],10)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 2)


class PreviewIntegrity(unittest.TestCase):
    def test_missing_and_modified_previews_require_new_review(self):
        scene={};data={'scenes':[scene]};png=b'exact reviewed final composition'
        with self.assertRaisesRegex(ValueError,'missing or stale'):
            r.preview_reviews(data,[png])
        scene['preview_review']={'approved':True,'reviewed_by':'test fixture reviewer','reviewed_at':'test timestamp','sha256':hashlib.sha256(png).hexdigest()}
        r.preview_reviews(data,[png])
        with self.assertRaisesRegex(ValueError,'missing or stale'):
            r.preview_reviews(data,[png+b'changed target or caption'])

    def test_invalid_coordinates_are_rejected_during_layout_generation(self):
        for rect in ([0,0,float('nan'),10],[0,0,float('inf'),10],[0,0,10],[-1,0,3,3],[0,0,101,2]):
            with self.subTest(rect=rect), self.assertRaises(ValueError):
                r.rectangle(rect,100,100,'Crop')

    def test_each_package_has_the_same_standalone_checker(self):
        other=ROOT/'skills/remotion-lesson-video/scripts/check_media.py'
        self.assertEqual(other.read_bytes(),(SCRIPTS/'check_media.py').read_bytes())


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class SilentDeliverable(unittest.TestCase):
    def test_silence_is_explicit_and_cannot_hide_missing_narration_or_audible_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            video = folder/'silent.mp4'
            base = ['ffmpeg', '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
                    'color=c=blue:s=64x64:r=10:d=1']
            subprocess.run(base + ['-an', '-c:v', 'mpeg4', str(video)], check=True,
                           stdin=subprocess.DEVNULL, capture_output=True)
            srt = folder/'lesson.srt'
            srt.write_text('1\n00:00:00,000 --> 00:00:00,900\nHello\n')
            expected = folder/'captions.txt'
            expected.write_text('Hello')
            result = media.inspect(video, srt, expected, silent=True)
            self.assertEqual(result['errors'], [])
            self.assertEqual(result['audio_requirement'], 'explicit_silent')
            self.assertTrue(result['subtitle_text_checked'])
            with self.assertRaisesRegex(ValueError, 'Audio stream missing'):
                media.inspect(video)
            for source, should_pass in [('anullsrc=r=44100:cl=mono', True),
                                        ('sine=frequency=440:duration=1', False)]:
                output = folder/('empty-audio.mp4' if should_pass else 'audible.mp4')
                subprocess.run(base + ['-f', 'lavfi', '-i', source, '-t', '1',
                               '-c:v', 'mpeg4', '-c:a', 'aac', str(output)], check=True,
                               stdin=subprocess.DEVNULL, capture_output=True)
                result = media.inspect(output, silent=True)
                self.assertEqual(not result['errors'], should_pass)
                self.assertEqual(not media.inspect(output)['errors'], not should_pass)
            expected.write_text('Hello missing words')
            self.assertTrue(media.inspect(video, srt, expected, silent=True)['errors'])


if __name__=='__main__':
    unittest.main()
