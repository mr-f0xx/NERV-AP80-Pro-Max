"""Create a simulator-only metadata/cover fixture (NOT the song recording).
Usage: python3 tools/create_good_light_preview.py /path/to/simdisk /path/to/cover.jpg
Requires Pillow and ffmpeg. Obtain the cover separately from the artist.
"""
import argparse
from pathlib import Path
import subprocess
from PIL import Image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('simdisk',type=Path)
    parser.add_argument('cover',type=Path)
    args=parser.parse_args()
    folder=args.simdisk/'Music/Children-of-Zeus'
    folder.mkdir(parents=True,exist_ok=True)
    Image.open(args.cover).convert('RGB').save(folder/'cover.bmp')
    subprocess.run(['ffmpeg','-nostdin','-v','error','-f','lavfi','-i',
        'aevalsrc=0.32*(0.5+0.5*sin(2*PI*0.63*t))*sin(2*PI*220*t)|0.38*(0.5+0.5*sin(2*PI*0.79*t))*sin(2*PI*330*t):s=44100:d=220',
        '-c:a','flac','-sample_fmt','s16','-metadata','title=Good Light',
        '-metadata','artist=Children of Zeus','-metadata','album=As The World Burns',
        '-metadata','date=2026','-metadata','track=4/16','-y',str(folder/'04-Good-Light.flac')],check=True)
    print('Created a 3:40 test-tone fixture with supplied artwork. This is not the song audio.')


if __name__=='__main__':
    main()
