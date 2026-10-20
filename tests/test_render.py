"""Reject stale evidence and preserve existing outputs; no network or paid TTS."""
import importlib.util
import json
from pathlib import Path
import tempfile
import sys
import unittest
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1]/'skills/canva-video-maker/scripts/render_lesson.py'
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location('renderer', SCRIPT)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class InputSafety(unittest.TestCase):
    def test_crop_and_highlight_reject_outside_actual_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); image=p/'capture.png'; Image.new('RGB',(20,20)).save(image)
            # Font is never used before the invalid crop, so isolate the crop boundary.
            from unittest.mock import patch
            for scene in ({'_image':image,'crop':[0,0,30,20]}, {'_image':image,'highlights':[[0,0,30,20]]}):
                with patch.object(r,'text'), self.assertRaisesRegex(ValueError,'outside'):
                    r.frame({'_font':None,'title':'test','scenes':[scene]},scene,0,p/'out.png')

    def test_existing_output_is_never_overwritten(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); out=p/'output';out.mkdir(); marker=out/'keep.txt';marker.write_text('keep')
            with patch.object(r,'load',return_value={'scenes':[]}), self.assertRaises(FileExistsError):
                r.render(p/'lesson.json',out,frames=True)
            self.assertEqual(marker.read_text(),'keep')

    def test_final_rejects_unreviewed_changed_and_synthetic_images(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);Image.new('RGB',(20,20)).save(p/'capture.png');(p/'font.ttf').write_text('fixture')
            scene={'image':'capture.png','caption':'caption','narration':'words',
                   'capture':{'kind':'actual_screen_capture','source':'test','captured_at':'actual date'}}
            data={'schema_version':1,'title':'test','font':'font.ttf','scenes':[scene]}
            path=p/'lesson.json'
            with patch.object(r.ImageFont,'truetype'):
                for review in ({}, {'approved':True,'reviewed_by':'reviewer','reviewed_at':'date','sha256':'wrong'}):
                    scene['image_review']=review;path.write_text(json.dumps(data))
                    with self.assertRaisesRegex(ValueError,'review'):
                        r.load(path,final=True)
                scene['capture']['kind']='synthetic_test';path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError,'actual captures'):
                    r.load(path,final=True)


if __name__=='__main__':
    unittest.main()
