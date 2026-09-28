"""Static checks for the native footer play/pause touch action."""
import unittest
from test_touch_seek import WPS, layout


def region(vp, tag):
    x, y, w, h = map(int, tag[3:-1].split(',')[:4])
    return vp[1] + x, vp[2] + y, w, h


def overlaps(a, b):
    x, y, w, h = a
    xx, yy, ww, hh = b
    return x < xx + ww and xx < x + w and y < yy + hh and yy < y + h


class TouchPlayLayout(unittest.TestCase):
    def test_two_explicit_touch_controls(self):
        touches = [(v, t) for v, t in layout() if t.startswith('%T(')]
        self.assertEqual(touches, [
            (('MainDisplay', 16, 584, 328, 20), '%T(0,0,328,20,progressbar)'),
            (('MainDisplay', 24, 604, 64, 32), '%T(0,0,64,32,play)'),
        ])

    def test_play_target_contains_icon_and_stays_in_viewport(self):
        vp, tag = next((v, t) for v, t in layout() if t.endswith(',play)'))
        self.assertEqual(tag, '%T(0,0,64,32,play)')
        x, y, w, h = region(vp, tag)
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, 0)
        self.assertLessEqual(x + w, 360)
        self.assertLessEqual(y + h, 640)
        self.assertEqual((w, h), vp[3:])
        self.assertLessEqual(x, 40)
        self.assertLessEqual(y, 608)
        self.assertGreaterEqual(x + w, 40 + 31)
        self.assertGreaterEqual(y + h, 608 + 16)

    def test_no_overlap_with_seek_or_footer_text(self):
        regions = [region(v, t) for v, t in layout() if t.startswith('%T(')]
        self.assertFalse(overlaps(*regions))
        play = regions[1]
        for text in [(98,604,222,26), (98,604,24,26), (124,604,196,26)]:
            self.assertFalse(overlaps(play, text))

    def test_unchanged_icon_and_hold_protection(self):
        text = WPS.read_text()
        self.assertIn('%V(40,608,31,16,-)\n%?mp<%xd(PBI,1)|%xd(PBI,2)|%xd(PBI,3)|%xd(PBI,4)|%xd(PBI,5)>', text)
        self.assertLess(text.index('%T(0,0,64,32,play)'), text.index('%V(40,608,31,16,-)'))
        self.assertNotIn('%T(', text.split('#-------- Lock Screen Layer -------#')[1])
        self.assertNotIn('allow_while_locked', text)
        self.assertIn('%?mh<%Vd(LockScreen)%?C<%Vd(LockScreenA)|%Vd(LockScreenB)>|%Vd(MainDisplay)', text)


if __name__ == '__main__':
    unittest.main()
