# fauvism: Matisse and Derain

Preset: [fauvism.json](fauvism.json).

## What defines it

Colour is freed from nature: pure, saturated paint straight from the tube, and shadows in complementary colours (green or violet in skin, for example Matisse's "Green Stripe"). Strokes are broad, flat and quick, with the light ground left showing between them. A few loose cobalt contours.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| ground | Brush 64 | cream `#fdf5e6` |
| strokes | Brush 26 | short (up to 3 steps), `grid` 1.45 + `seed_jitter` 0.45 so the ground shows between strokes |
| strokes | Brush 14 | thresh 9, `grid` 1.35 |
| strokes | Brush 7 | `detail` only |
| contours | Brush 3 | cobalt on strong luminance boundaries |

Palette: 14 fixed pure colours (vermilion, orange, yellow, yellow-green, emerald, viridian, turquoise, cobalt, ultramarine, violet, pink, white, red, night blue). Prefilter: saturation 1.9, contrast 1.1, gamma 0.85, `complement_shadows` (below L 78, warm shadows pushed toward green and cool ones toward violet, strength 0.85).

## Do / don't

- Do keep the strokes broad and separate.
- Do let the complementary shadows read; raise `complement_shadows.L` for more of them.
- Don't use the Oil brush (Fauve paint is thin and flat); don't use earth colours or black.

About 4,000 strokes, about 2 minutes.
