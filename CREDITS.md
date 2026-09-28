# Credits & licensing

## Theme

- **NERV** by **EppsNL** (Epps.nl / eppsnl@gmail.com), originally designed for the Innioasis Y1 at 480 × 360.
  - Source: https://github.com/EppsNL/Innioasis-y1-rockbox-themes/tree/main/NERV
  - Upstream notice: [LICENSES/NERV-upstream.txt](LICENSES/NERV-upstream.txt), preserved verbatim.
  - Upstream declares **CC-BY-SA**, but does not identify a version in the supplied notice. This adaptation retains that declaration; no particular CC licence version is asserted here.
- Based on **Snarty** by **Simon Andén**, in turn based on **SPAZZ** by **Chuck Lardo**, **SNAZZ/SNAZZ2** by **Jihoon Kim**, and **SNAZZY** by **Phil Graves**.
- **AP80 Pro Max adaptation and cyberpunk variant:** mr-f0xx's NERV-AP80-Pro-Max project, with agent-assisted implementation.
  - Adaptations include the portrait layout, recoloured graphics, stereo LED meters, touch seek/playback controls, and USB power dashboard.
  - Source: https://github.com/mr-f0xx/NERV-AP80-Pro-Max

The inherited theme notice is not a grant of rights to third-party names, logos or trademarks. This is an unofficial fan theme, not an affiliated Hidizs or Evangelion product.

## Fonts

The bundled `KodeMonoMPlus2-SemiBold` bitmap fonts derive from the Kode Mono / MPLUS2 combination credited by EppsNL, with sizes adapted for this layout.

- **Kode Mono** — https://github.com/isaozler/kode-mono
- **MPLUS fonts / MPLUS2** — https://github.com/coz-m/MPLUS_FONTS

The corresponding SIL Open Font License 1.1 notices are included in:

- [LICENSES/KodeMono-OFL.txt](LICENSES/KodeMono-OFL.txt)
- [LICENSES/MPLUS2-OFL.txt](LICENSES/MPLUS2-OFL.txt)

Font licences apply separately from the theme artwork/layout notice. The notices were obtained from the respective font-family directories in the Google Fonts repository.

## Previews and Rockbox

Screenshots are unretouched captures from the Rockbox AP80 Pro Max simulator. The current Now Playing screenshot features **Good Light — Children of Zeus**, with cover art for **As The World Burns**, sourced from the [artist's official Bandcamp page](https://childrenofzeus.bandcamp.com/album/as-the-world-burns). Album art remains the property of its respective rights holders and is not relicensed under the theme or font licences.

Only the artwork and metadata identify the song. The screenshot's audio-level meters are driven by a generated stereo test tone, not the commercial recording. `tools/create_good_light_preview.py` reproduces the fixture from a separately supplied cover. Neither the raw cover nor any song audio is installed by the theme ZIP.

The separate `Neon Signal` test fixture created by `tools/create_preview_media.py` uses original procedural artwork and generated audio. It remains available for tests but is no longer the README's Now Playing preview.

Rockbox provides the firmware, simulator, skin parser, audio metering and touch actions: https://www.rockbox.org/ · https://github.com/Rockbox/rockbox

Rockbox is a separate project and is not bundled in the theme release. See [docs/VALIDATION.md](docs/VALIDATION.md) for the exact source revision used.
