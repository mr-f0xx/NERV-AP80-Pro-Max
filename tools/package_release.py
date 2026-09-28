"""Build a theme-only install ZIP and SHA256SUMS using the Python standard library.
Usage: python3 tools/package_release.py --output /path/to/releases
"""
from pathlib import Path
import argparse
import hashlib
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.0.0'
NAME = f'NERV-AP80-Pro-Max-theme-v{VERSION}.zip'
INSTALL = '''NERV — AP80 Pro Max | Theme 1.0.0
360 x 640 portrait | Rockbox theme only (no firmware/bootloader)

1. Back up your existing theme.
2. Extract this ZIP to your player's storage root, merging .rockbox with
   the existing .rockbox folder. Do not delete the existing folder.
3. Eject safely. In Rockbox select Settings > Theme Settings > Browse
   Theme Files > NERV_AP80.cfg (wording may vary by firmware).
4. Enable Point touchscreen mode for tap/drag seeking and tap play/pause.

For updates, merge the package and reselect the theme.
Fonts, images and icons are included. The USB screen is theme-controlled;
bootloader/offline charging screens are not modified. Peak meters show
left/right audio levels, not a frequency spectrum. Hardware testing is
still needed; custom firmware may differ from the tested simulator.

Source, screenshots and compatibility notes:
https://github.com/mr-f0xx/NERV-AP80-Pro-Max

Theme attribution and licence information: CREDITS.md and LICENSES/.
'''


def release_files():
    paths = [p for p in (ROOT/'.rockbox').rglob('*') if p.is_file()]
    paths += [ROOT/'CREDITS.md']
    paths += [p for p in (ROOT/'LICENSES').iterdir() if p.is_file()]
    return sorted(paths)


def build(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    archive = output/NAME
    with ZipFile(archive, 'w', ZIP_DEFLATED, compresslevel=9) as z:
        for path in release_files():
            z.write(path, path.relative_to(ROOT).as_posix())
        z.writestr('INSTALL.txt', INSTALL)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output/'SHA256SUMS').write_text(f'{digest}  {NAME}\n')
    print(f'{archive} ({archive.stat().st_size:,} bytes)')
    return archive


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    build(parser.parse_args().output)
