# NERV · AP80 Pro Max

**A cyan, pink and purple Rockbox theme for the Hidizs AP80 Pro Max.**

Built for the **360 × 640 portrait touchscreen**: large cover art, scrolling track details, live stereo LED meters, touch controls, and a dedicated USB power dashboard.

[**Download theme 1.0.0**](https://github.com/mr-f0xx/NERV-AP80-Pro-Max/releases/tag/theme-v1.0.0) · [Installation](#installation) · [Controls](#controls) · [Compatibility](#compatibility)

## Preview

| Main menu | Now playing | USB / charging |
|:---:|:---:|:---:|
| <a href="screenshots/menu.png"><img src="screenshots/menu.png" width="240" alt="NERV main menu, 360 by 640 pixels"></a> | <a href="screenshots/now_playing.png"><img src="screenshots/now_playing.png" width="240" alt="NERV now-playing screen with stereo LED meters, 360 by 640 pixels"></a> | <a href="screenshots/charging.png"><img src="screenshots/charging.png" width="240" alt="NERV USB charging dashboard, 360 by 640 pixels"></a> |

Actual, unretouched **Rockbox AP80 Pro Max simulator captures**, each at the device's native **360 × 640 / 9:16** screen format. No stretched screenshots or device-photo mockups. The demo track/artwork and battery/clock readings are simulated—not measurements from a physical player. [Capture and validation details →](docs/VALIDATION.md)

## Features

- **Portrait now-playing layout** with a 320 × 320 cover-art area, title, artist, album, year and file information.
- **Live stereo LED meters** in cyan → purple → pink. Two independent audio-level towers, without labels or separator lines. These are peak meters, not a frequency spectrum or an EQ control.
- **Tap or drag to seek**, with a larger invisible target around the progress bar.
- **Tap the bottom playback icon to play/pause**, without changing its appearance.
- **USB power dashboard** with battery percentage, segmented battery gauge, charging/power status, battery voltage, clock/date and a safe-eject reminder.
- **Matching menu/browser and Hold layout**, plus bundled Kode Mono / MPLUS2 fonts with kana support.

## Installation

This is a **theme-only package**. Rockbox must already be installed; the download does not include firmware or a bootloader.

1. Download **`NERV-AP80-Pro-Max-theme-v1.0.0.zip`** from the [theme release](https://github.com/mr-f0xx/NERV-AP80-Pro-Max/releases/tag/theme-v1.0.0).
2. Extract it to the root of your player's storage, **merging** its `.rockbox` folder with the existing one. Do not delete or replace your entire Rockbox installation.
3. Eject the player safely.
4. Open **Settings → Theme Settings → Browse Theme Files** and select **`NERV_AP80.cfg`**. Menu wording may vary by build.
5. For touch controls, select **Point** under **Settings → General Settings → Display → Touchscreen Settings**.

**Updating an existing installation?** Back up your current theme, merge the new package, and reselect `NERV_AP80.cfg` to reload it. The required fonts, icons and bitmaps are included.

To install from the source repository instead, copy the contents of its `.rockbox/` folder to the matching folder on the player. Developer files and screenshots are not required on the device.

## Controls

| Area | Action |
|---|---|
| Progress bar | Tap to seek; drag and release to choose a position |
| Bottom playback icon | Tap to pause; tap again to resume |
| Stereo LED meters | Display only; left and right audio levels |
| USB dashboard | Display only; eject from your computer before unplugging |

The seek and play/pause targets do not overlap. They are disabled when the theme's Hold view is active. Rockbox's own lock and Party Mode restrictions still apply. The theme does not change your touchscreen-mode preference.

## Compatibility

- Designed specifically for the **Hidizs AP80 Pro Max, 360 × 640**. This is not the layout for the older AP80 / AP80 Pro / AP80 Pro-X.
- Validated with the target-specific Rockbox skin parser and AP80 Pro Max simulator. **Physical-device verification is still needed**, especially with third-party firmware builds.
- The visualizer requires native `%pL` / `%pR` peak-meter bar support. Live meters add redraw work and may affect battery life; performance varies by firmware.
- The USB dashboard replaces the skin-controlled USB page, **not** a bootloader/offline charging screen. Some firmware builds handle USB differently.
- `CHARGING` appears only when Rockbox reports active charging. A USB connection alone does not imply charging; `BATTERY FULL` requires a reported 100%.
- Unknown battery/voltage readings remain unknown. No time-to-full, charging wattage, battery-health estimate or file-transfer progress is invented.

If fonts or graphics are missing, check that the folder structure was preserved and reload the theme. For rendering or touch problems, include your firmware version and a photo/screenshot in an [issue](https://github.com/mr-f0xx/NERV-AP80-Pro-Max/issues).

## Source layout

```text
.rockbox/      Installable theme, fonts, icons and artwork
screenshots/  Native-resolution simulator captures
LICENSES/     Upstream theme notice and font licences
docs/         Validation and development notes
tools/        Asset generators, demo media and release packaging
tests/        Layout, asset and packaging regression checks
```

Run `python3 -m unittest discover -s tests -v` for the regression checks. See [development notes](docs/DEVELOPMENT.md) for asset generation and packaging.

## Credits & licensing

Adapted from **NERV by EppsNL**, originally for the Innioasis Y1. The upstream theme declares **CC-BY-SA**; the original notice is preserved without inventing a licence version. The merged font sources use the **SIL Open Font License**.

Thanks to EppsNL, the original Snarty/SPAZZ/SNAZZ theme authors, the Kode Mono and MPLUS font projects, and the Rockbox contributors. Full attribution and licence details: [CREDITS.md](CREDITS.md).
