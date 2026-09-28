"""Source/package hygiene and lossless screenshot shape checks."""
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseHygiene(unittest.TestCase):
    def test_native_portrait_previews(self):
        paths = sorted((ROOT/'screenshots').glob('*.png'))
        self.assertEqual([p.name for p in paths], ['charging.png','menu.png','now_playing.png'])
        for p in paths:
            data = p.read_bytes()
            self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack_from('>II',data,16),(360,640),p.name)
            self.assertGreater(len(data),1000)

    def test_bitmap_preloads_have_no_orphans(self):
        expected=set()
        for suffix in ('wps','sbs'):
            text=(ROOT/f'.rockbox/wps/NERV_AP80.{suffix}').read_text()
            expected.update(re.findall(r'%xl\([^,]+,([^,()]+\.bmp)[,)]',text))
        actual={p.name for p in (ROOT/'.rockbox/wps/NERV_AP80').glob('*.bmp')}
        self.assertEqual(actual,expected)

    def test_no_credentials_or_machine_paths_in_source_text(self):
        for folder in (ROOT/'.rockbox',ROOT/'docs',ROOT/'tools',ROOT/'tests'):
            for p in folder.rglob('*'):
                if p.suffix in ('.py','.md','.txt','.cfg','.wps','.sbs'):
                    text=p.read_text()
                    self.assertIsNone(re.search(r'gh[pousr]_[A-Za-z0-9]{30,}',text),str(p))
                    self.assertIsNone(re.search(r'/home/[a-z]+/',text),str(p))

    def test_readme_uses_real_captures_and_theme_release(self):
        text=(ROOT/'README.md').read_text()
        for name in ('menu','now_playing','charging'):
            self.assertIn(f'screenshots/{name}.png',text)
        self.assertIn('simulator captures',text)
        self.assertIn('theme-v1.0.0',text)
        self.assertNotIn('_mockup.png',text)


if __name__=='__main__':
    unittest.main()
