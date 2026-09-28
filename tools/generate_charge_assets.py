"""Generate NERV USB battery-gauge assets. Development dependency: Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / '.rockbox/wps/NERV_AP80'


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def generate():
    cyan, purple, pink = (0,229,255), (148,60,255), (255,60,220)
    lit = Image.new('RGB', (272,60), 'black')
    dark = lit.copy()
    bright, dim = ImageDraw.Draw(lit), ImageDraw.Draw(dark)
    for col in range(17):
        t = col / 16
        color = mix(cyan,purple,t*2) if t <= .5 else mix(purple,pink,(t-.5)*2)
        low = tuple(round(c*.16) for c in color)
        for row in range(6):
            rect = (col*16+2,row*10+1,col*16+13,row*10+8)
            bright.rectangle(rect, fill=color)
            dim.rectangle(rect, fill=low)
    lit.save(ASSETS / 'charge_fill.bmp')
    dark.save(ASSETS / 'charge_back.bmp')


if __name__ == '__main__':
    generate()
