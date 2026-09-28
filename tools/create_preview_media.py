"""Create original demo cover and test-tone track for simulator screenshots.
Not part of the install ZIP. Requires Pillow and ffmpeg; no downloaded music/art.
Usage: python3 tools/create_preview_media.py /path/to/simdisk
"""
from pathlib import Path
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageFont


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('simdisk',type=Path)
    args=parser.parse_args()
    folder=args.simdisk/'Music/NERV'
    folder.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(320,320),'#02070B')
    d=ImageDraw.Draw(im)
    for y in range(320):
        d.line((0,y,319,y),fill=(3+int(y/50),6,int(12+y/12)))
    for x in range(-300,650,35):
        d.line((160,175,x,320),fill='#123345')
    for y in (195,208,225,247,276,316):
        d.line((0,y,319,y),fill='#173449')
    for r in range(67,42,-1):
        t=(67-r)/25
        c=(round(8+125*t),round(40+50*t),round(65+150*t))
        d.ellipse((160-r,143-r,160+r,143+r),outline=c,width=1)
    d.ellipse((114,97,206,189),fill='#040911',outline='#00E5FF',width=2)
    d.arc((108,91,212,195),20,160,fill='#FF3CDC',width=3)
    for x,y in [(24,94),(287,101),(260,69),(58,155),(282,181),(34,191)]:
        d.rectangle((x,y,x+1,y+1),fill='#00E5FF')
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    small=ImageFont.truetype(fontpath,11)
    title=ImageFont.truetype(fontpath,25)
    d.text((20,20),'NERV AUDIO LAB',font=small,fill='#00E5FF')
    d.text((20,43),'AFTER HOURS',font=title,fill='#FF3CDC')
    d.text((20,288),'NEON SIGNAL  /  01',font=small,fill='#00E5FF')
    im.save(folder/'cover.bmp')
    subprocess.run(['ffmpeg','-nostdin','-v','error','-f','lavfi','-i',
        'aevalsrc=0.32*(0.5+0.5*sin(2*PI*0.63*t))*sin(2*PI*220*t)|0.38*(0.5+0.5*sin(2*PI*0.79*t))*sin(2*PI*330*t):s=44100:d=180',
        '-c:a','flac','-sample_fmt','s16','-metadata','title=Neon Signal',
        '-metadata','artist=NERV Audio Lab','-metadata','album=After Hours',
        '-metadata','date=2026','-y',str(folder/'01-Neon-Signal.flac')],check=True)
    print('Demo fixture created. Preview audio is a generated test tone, not music.')


if __name__=='__main__':
    main()
