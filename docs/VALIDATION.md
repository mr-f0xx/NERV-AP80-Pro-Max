# Validation & preview provenance

## Environment

- Date: 2026-09-28.
- Rockbox source: https://github.com/Rockbox/rockbox
- Revision: `e9a6b58870e799e508260d2b63f9b036dc2e2fd1`.
- Target: **`hidizsap80max`**, model 125, 360 × 640, RGB565.
- Target-specific `checkwps` and SDL2 simulator built on Linux.
- Parser result: `NERV_AP80.wps` and `NERV_AP80.sbs` both **parsed OK** with the bundled assets/fonts present.
- The simulator used for the final captures has no source modifications. A temporary diagnostic edit used while troubleshooting was reverted before the final run.

## Screenshots

| File | Captured state |
|---|---|
| `screenshots/menu.png` | Actual root menu, Files selected, playback stopped |
| `screenshots/now_playing.png` | Children of Zeus — Good Light metadata and official album art loaded; generated stereo test-tone FLAC drives the live meters |
| `screenshots/charging.png` | Actual USB screen while the simulator's native battery model reports charging and external power |

All three were produced using the simulator's **F5 framebuffer dump**, then converted losslessly from BMP to PNG. Each image is **360 × 640 pixels**. No pixels, telemetry, menu items or text were painted over; there is no device frame or synthetic UI layer. The README displays them at 240 pixels wide while retaining the 9:16 aspect ratio.

Battery voltage/percentage, charging state and clock/date are the simulator's values. They are not hardware measurements. In particular, the simulator cycles its battery independently of USB connection. It was allowed to enter its charging state naturally for the USB capture.

The current Now Playing capture uses the artwork and track metadata for **Good Light — Children of Zeus**, from **As The World Burns**. The artist's [official Bandcamp album page](https://childrenofzeus.bandcamp.com/album/as-the-world-burns) lists a release date of **4 September 2026**, track **4**, and duration **3:40**. Artwork source: `https://f4.bcbits.com/img/a1141388720_5.jpg`.

This is a metadata/artwork preview, not a capture of the commercial recording. `tools/create_good_light_preview.py` accepts a separately obtained cover file and creates a 220-second synthetic stereo test-tone FLAC with those tags. The file format, bitrate, sample rate and level-meter activity shown are those of this fixture, not claimed properties of the artist's master/download. The footer's 1/1 is the actual one-item preview playlist position, not the album track number.

The screenshot was freshly captured through the same unmodified AP80 simulator's F5 dump. The cover is loaded through Rockbox's actual album-art path. The raw cover and audio fixture are not distributed in the theme package. Artwork rights remain with their respective owners; inclusion in the screenshot does not relicense the cover as theme artwork.

The original procedural demo generator remains available as `tools/create_preview_media.py` for artwork-independent testing.

## Runtime checks completed in the simulator

The original release checks below used the 3:00 procedural demo fixture; the updated screenshot uses the 3:40 Good Light metadata fixture.

- Loaded the theme's menu/browser, Now Playing and USB dashboard.
- Connected/disconnected simulated USB and confirmed the menu returns.
- Observed native stereo peak-meter animation during playback.
- Tapped the footer playback region: playback paused and the LED towers went dark.
- Tapped the progress-bar midpoint while paused: elapsed time changed to 1:30 of a 3:00 track and remained paused.
- Tapped the footer again: playback resumed and the live towers returned.
- Confirmed the compact elapsed/total and playlist-position footer replaces the inherited malformed footer string.

## Static regression checks

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

These cover touch geometry, separation of controls, conditional visibility, visualizer channels/assets, text viewport widths, USB routing/fallbacks, bundled-font fit, screenshot dimensions, asset references and release-file hygiene. Static tests do not emulate touch gestures or hardware.

## Still requires a physical player

No AP80 Pro Max was available for hardware testing. Verify firmware-specific USB behavior, lock handling, long press/drag edge cases, unknown telemetry, battery-full transitions, next-track text, long metadata and long FLAC playback. Monitor battery life/performance with the peak meters enabled. Older/custom ports may differ from the tested source revision.

Do not treat these simulator checks as hardware certification.
