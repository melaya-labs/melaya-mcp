# sumi-e: Japanese ink wash

Preset: [sumi-e.json](sumi-e.json). Sesshu Toyo, Hasegawa Tohaku.

## What defines it

Ink only, in a few dilutions, from pale grey washes to black. A few expressive brush lines carry the form, thick and thin as the brush turns. Most of the paper is left untouched, since the emptiness is part of the picture. A small red seal stamp signs it.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| washes | Watercolour 36, 18, 8 | `grid` 1.8 / 1.6 / 1.2 with `seed_jitter`, high thresholds (28 / 24 / 22): few strokes, lots of paper; the planner picks among the ink dilutions for how each lands over what is there |
| brush lines | Calligraphy 5 | `outline` on 4-level luminance boundaries (`edge_pct` 80, chains of 25 px or more), not along the faded border; the flat nib (measured: 135 deg, hairline along it) gives thick-thin lines |
| seal | Pencil 5 | `ornament` seal, 22 px red square at the lower right |

Palette: black, dark, mid and light ink, pale wash, seal red (fixed). Prefilter: saturation 0, gamma 0.6, contrast 1.35, `fade_edges` 0.18.

## Do / don't

- Do leave paper: raise thresholds rather than adding layers.
- Do keep the line work sparse (`min_len`, `edge_pct`).
- Don't add colour (except the seal); don't fill backgrounds.

Calligraphy and Watercolour are measured live (Calligraphy opaque, 14 px nib at 135 deg; Watercolour wet-edge ramp with hair streaks, fitted on the live sumi-e and watercolour crops). The washes use longer curving strokes (`max_len` 7 / 6, `step` 0.5) so the side-loaded ramp reads as brush washes. About 575 strokes, under 30 s; expect live_vs_sim around 8.
