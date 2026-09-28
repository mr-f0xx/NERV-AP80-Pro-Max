# Development

The installable theme lives in `.rockbox/`. Keep generated builds, simulator disks, archives, credentials and captured raw BMPs out of the repository.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

The test suite uses Python's standard library. Asset/preview-media generation additionally needs Pillow; the demo audio generator needs ffmpeg.

```sh
python3 tools/generate_level_assets.py
python3 tools/generate_charge_assets.py
python3 tools/create_preview_media.py /path/to/rockbox-sim/simdisk
# Current README preview: supply the artist's cover separately.
python3 tools/create_good_light_preview.py /path/to/rockbox-sim/simdisk /path/to/cover.jpg
```

## Rockbox parser and simulator

Use the source revision recorded in [VALIDATION.md](VALIDATION.md). From separate build directories:

```sh
/path/to/rockbox/tools/configure --target=hidizsap80max --type=c
make -j8
```

Run the resulting `checkwps.hidizsap80max` from this theme's repository root so it can find the fonts:

```sh
/path/to/checkwps.hidizsap80max .rockbox/wps/NERV_AP80.wps .rockbox/wps/NERV_AP80.sbs
```

For the simulator (SDL2 development libraries required):

```sh
/path/to/rockbox/tools/configure --target=hidizsap80max --type=s
make -j8
make install
cp -a /path/to/NERV-AP80-Pro-Max/.rockbox/. simdisk/.rockbox/
cp simdisk/.rockbox/themes/NERV_AP80.cfg simdisk/.rockbox/config.cfg
```

Append these **simulator-only** settings to `config.cfg`; they are deliberately not forced by the distributed theme:

```text
start in screen: root
backlight timeout: on
backlight timeout plugged: on
touchscreen mode: point
```

Run `./rockboxui --nobackground` with an available graphical display (Xvfb also works). `SDL_AUDIODRIVER=dummy` allows silent playback during capture.

For this simulator target:

- Up/Down: scroll; Return: select/play; Left: back in lists; Escape: menu from WPS.
- Mouse: touchscreen in Point mode. Use a normal-duration press/release; an instantaneous synthetic click can be missed.
- `c`: toggle USB. The native battery simulation cycles independently of this switch.
- F5: dump the 360 × 640 framebuffer to the simulator disk.

Convert the F5 BMPs losslessly to PNG. Do not repaint readouts or use a hand-drawn UI as a release screenshot. Capture charging when the native simulator battery model reports that state. The README must continue to identify simulator output as such.

## Packaging

```sh
python3 tools/package_release.py --output /path/outside/the/repository
```

This creates a theme-only ZIP and `SHA256SUMS`. The ZIP contains `.rockbox/`, installation instructions and licence notices—not test tracks, screenshots, scripts, Rockbox firmware, caches or Git metadata.

The release uses the tag `theme-v1.0.0` to distinguish the theme package from the repository's existing `1.2` firmware release. Publishing this theme does not require deleting earlier releases or rewriting repository history.
