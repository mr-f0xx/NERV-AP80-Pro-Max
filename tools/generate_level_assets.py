"""Rebuild the segmented stereo-meter bitmaps. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / '.rockbox/wps/NERV_AP80'


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def generate():
    cyan, purple, pink = (0, 229, 255), (148, 60, 255), (255, 60, 220)
    lit = Image.new('RGB', (24, 78), 'black')
    dark = lit.copy()
    draw, dim = ImageDraw.Draw(lit), ImageDraw.Draw(dark)
    for row in range(13):
        t = row / 12
        color = mix(pink, purple, t * 2) if t <= .5 else mix(purple, cyan, (t - .5) * 2)
        low = tuple(round(c * .14) for c in color)
        for x in (0, 9, 18):
            rect = (x, row * 6 + 2, x + 5, row * 6 + 5)
            draw.rectangle(rect, fill=color)
            dim.rectangle(rect, fill=low)
    ASSETS.mkdir(parents=True, exist_ok=True)
    lit.save(ASSETS / 'eq_led_fill.bmp')
    dark.save(ASSETS / 'eq_led_back.bmp')


if __name__ == '__main__':
    generate()
