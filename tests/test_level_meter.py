"""Static regression checks; does not emulate Rockbox's audio/render loop."""
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / '.rockbox/wps/NERV_AP80.wps').read_text()
ASSETS = ROOT / '.rockbox/wps/NERV_AP80'
MAIN, LOCK = TEXT.split('#-------- Lock Screen Layer -------#')


class StereoLevelMeter(unittest.TestCase):
    def test_metadata_reserves_panel_and_keeps_scrolling(self):
        for y, h, f in [(432,34,5), (468,28,4), (500,28,4), (532,26,4)]:
            match = re.search(rf'%Vl\(MainDisplay,16,{y},236,{h},{f}\)\n(?:%Vf\([^\n]+\)\n)?(%al%s[^\n]+)', MAIN)
            self.assertIsNotNone(match)
        self.assertLess(16 + 236, 264)
        self.assertIn('%Vl(MainDisplay,16,560,328,24,3)', MAIN)
        self.assertIn('%Vl(MainDisplay,20,102,320,320,-)', MAIN)

    def test_panel_inside_screen_and_above_file_info(self):
        block = MAIN.split('#__Stereo LED Levels')[1].split('#__File Info')[0]
        viewports = re.findall(r'%Vl\(MainDisplay,(\d+),(\d+),(\d+),(\d+),[^)]+\)', block)
        self.assertEqual(len(viewports), 2)
        for x, y, w, h in (map(int, v) for v in viewports):
            self.assertGreaterEqual(x, 264)
            self.assertLessEqual(x + w, 344)
            self.assertGreaterEqual(y, 432)
            self.assertLessEqual(y + h, 558)
        self.assertNotIn('%T(', block)
        self.assertNotIn('allow_while_locked', block)

    def test_bars_only_without_labels_or_separators(self):
        block = MAIN.split('#__Stereo LED Levels')[1].split('#__File Info')[0]
        self.assertNotIn('%dr(', block)
        self.assertNotIn('%ac', block)
        self.assertNotIn('%al', block)
        lines = [line for line in block.splitlines()[1:] if line and not line.startswith('#')]
        self.assertEqual(len(lines), 4)
        for line in lines:
            self.assertTrue(line.startswith(('%Vl(', '%?mp<')))

    def test_native_channels_vertical_noninteractive(self):
        for channel in ('L', 'R'):
            bars = re.findall(rf'%p{channel}\(([^)]+)\)', MAIN)
            self.assertEqual(bars, ['0,0,24,78,EQLit,backdrop,EQDark,vertical,notouch'] * 3)
            self.assertNotIn(f'%p{channel}', LOCK)
        self.assertNotIn('EQDark', LOCK)

    def test_stopped_and_paused_use_unlit_bitmap(self):
        lines = [line for line in MAIN.splitlines() if line.startswith('%?mp<%xd(EQDark)')]
        self.assertEqual(len(lines), 2)
        for line in lines:
            states = line[len('%?mp<'):-1].split('|')
            self.assertEqual(len(states), 5)
            self.assertEqual(states[0], '%xd(EQDark)')
            self.assertEqual(states[2], '%xd(EQDark)')

    def test_bitmap_headers_and_theme_colours(self):
        for name, label in [('eq_led_fill.bmp', 'EQLit'), ('eq_led_back.bmp', 'EQDark')]:
            raw = (ASSETS / name).read_bytes()
            self.assertEqual(raw[:2], b'BM')
            self.assertEqual(struct.unpack_from('<ii', raw, 18), (24, 78))
            self.assertEqual(struct.unpack_from('<H', raw, 28)[0], 24)
            self.assertIn(f'%xl({label},{name},0,0)', MAIN)
        lit = (ASSETS / 'eq_led_fill.bmp').read_bytes()
        # 24-bit BMP stores BGR; assert all three palette anchors are present.
        pixels = lit[struct.unpack_from('<I', lit, 10)[0]:]
        for rgb in [(0,229,255), (148,60,255), (255,60,220)]:
            self.assertIn(bytes(reversed(rgb)), pixels)


if __name__ == '__main__':
    unittest.main()
