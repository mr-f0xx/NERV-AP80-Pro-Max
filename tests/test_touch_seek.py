"""Static layout checks, not a Rockbox parser or hardware simulation."""
from pathlib import Path
import re
import unittest

WPS = Path(__file__).resolve().parents[1] / '.rockbox/wps/NERV_AP80.wps'


def layout():
    viewport = None
    tags = []
    for line in WPS.read_text().splitlines():
        match = re.fullmatch(r'%Vl\((\w+),(\d+),(\d+),(\d+),(\d+),[^)]+\)', line)
        if match:
            viewport = (match[1], *map(int, match.groups()[1:]))
        elif line.startswith('%V('):
            viewport = None
        if line.startswith(('%T(', '%pb(', '%dr(')):
            tags.append((viewport, line))
    return tags


class TouchSeekLayout(unittest.TestCase):
    def test_single_seek_region_in_main_display(self):
        touches = [(v, tag) for v, tag in layout() if tag.startswith('%T(') and tag.endswith(',progressbar)')]
        self.assertEqual(touches, [
            (('MainDisplay', 16, 584, 328, 20), '%T(0,0,328,20,progressbar)')
        ])

    def test_target_between_file_info_and_footer(self):
        vp, tag = next((v, t) for v, t in layout() if t.startswith('%T('))
        x, y, w, h = map(int, tag[3:-1].split(',')[:4])
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLessEqual(x + w, vp[3])
        self.assertLessEqual(y + h, vp[4])
        self.assertEqual((vp[1] + x, w), (16, 328))
        self.assertGreaterEqual(vp[2] + y, 560 + 24)
        self.assertLessEqual(vp[2] + y + h, 604)
        self.assertLessEqual(vp[1] + x + w, 360)
        self.assertLessEqual(vp[2] + y + h, 640)
        self.assertLessEqual(vp[2] + y, 588)
        self.assertGreaterEqual(vp[2] + y + h, 598)

    def test_visual_bars_unchanged_and_no_automatic_touch(self):
        bars = [(v, t) for v, t in layout() if t.startswith('%pb(')]
        self.assertEqual(bars, [
            ((name, 16, 589, 328, 7), '%pb(0,0,328,7,PBB,slider,PB,notouch)')
            for name in ('MainDisplay', 'LockScreen')
        ])

    def test_original_main_borders(self):
        borders = [(v, t) for v, t in layout()
                   if v and v[0] == 'MainDisplay' and v[2] in (588, 597)]
        self.assertEqual(borders, [
            (('MainDisplay', 16, y, 328, 1), '%dr(0,0,328,1,FF3CDC)')
            for y in (588, 597)
        ])

    def test_lock_visibility_and_touch_paint_order(self):
        text = WPS.read_text()
        self.assertIn('%?mh<%Vd(LockScreen)%?C<%Vd(LockScreenA)|%Vd(LockScreenB)>|%Vd(MainDisplay)', text)
        self.assertNotIn('allow_while_locked', text)
        self.assertLess(text.index('%T('), text.index('%Vl(MainDisplay,16,588,'))


if __name__ == '__main__':
    unittest.main()
