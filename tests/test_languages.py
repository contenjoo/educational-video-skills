"""Protect multilingual ZIP distribution and lossless Korean/English/Japanese subtitles."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/canva-video-maker/scripts/render_lesson.py'
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location('language_renderer', SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class LanguageDistribution(unittest.TestCase):
    def test_release_archives_include_each_language_and_its_references(self):
        subprocess.run([sys.executable, str(ROOT/'scripts/package.py')], check=True, capture_output=True)
        for skill in ('canva-video-maker', 'remotion-lesson-video'):
            with self.subTest(skill=skill), ZipFile(ROOT/'dist'/f'{skill}.zip') as archive:
                self.assertIsNone(archive.testzip())
                for suffix in ('', '.en', '.ja'):
                    path=f'{skill}/SKILL{suffix}.md'
                    self.assertGreater(len(archive.read(path).decode('utf-8')), 300)
                for source in (ROOT/'skills'/skill/'references').glob('*.md'):
                    self.assertEqual(archive.read(f'{skill}/references/{source.name}'),source.read_bytes())
                self.assertIn(b'SKILL.ja.md', archive.read(f'{skill}/SKILL.md'))

    def test_subtitles_preserve_all_three_languages(self):
        for language, narration in {
            'ko':'텍스트 메뉴를 열고 텍스트 상자를 추가하세요. 결과를 확인하세요.',
            'en':'Open the text menu and add a text box. Check the result.',
            'ja':'テキストメニューを開き、テキストボックスを追加してください。結果を確認しましょう。',
        }.items():
            with self.subTest(language=language):
                cues=renderer.timed_subtitles(narration,12,max_chars=14)
                self.assertGreater(len(cues),1)
                self.assertEqual(renderer.canonical(''.join(c['text'] for c in cues)),renderer.canonical(narration))
                self.assertTrue(all(0<=c['start']<c['end']<=12 and len(c['text'])<=14 for c in cues))
                self.assertTrue(all(a['end']<=b['start'] for a,b in zip(cues,cues[1:])))

if __name__=='__main__':
    unittest.main()
