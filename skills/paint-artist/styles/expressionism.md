# expressionism: Munch and Kirchner

Preset: [expressionism.json](expressionism.json).

## What defines it

Emotion over appearance:
- the forms are distorted, as if seen through anxiety;
- long wavy strokes swirl through sky, water and figure alike (The Scream);
- intense, clashing colour: blood orange against acid green and Prussian blue;
- heavy dark outlines hold the figure.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| ground | Brush 64 | orange `#e8641c` |
| swirls | Brush 13 | `direction: flow`, `flow_sigma` 12, `swirl` 0.85 (7 vortices), `fixed_len` 16 steps of 0.55 width, `color_jitter` 26 (neighbouring strokes clash) |
| swirls | Brush 7 | `swirl` 0.6, 14 steps, thresh 6 |
| accents | Brush 4 | `finest` only |
| outlines | Brush 5 | black on 4-level luminance boundaries, chains of 30 px or more |

Palette: 12 fixed (cadmium red, orange, chrome yellow, cream, acid green, emerald, Prussian blue, cobalt, violet, pink, black, burnt sienna). Prefilter: saturation 1.8, contrast 1.25, `warp` (smooth waves, 12 px amplitude, 150 px wavelength: the distortion).

## Do / don't

- Do keep `color_jitter` high: the clash between neighbouring strokes is the style.
- Do keep the outlines heavy (width 5 or more).
- Don't use soft glazes or naturalistic colour.

About 11,700 strokes, about 6 minutes.
