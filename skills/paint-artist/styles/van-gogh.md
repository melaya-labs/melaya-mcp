# van-gogh: post-impressionist swirls

Preset: [van-gogh.json](van-gogh.json). Analysing Starry Night with `analyse` selects this base.

## What defines it

Every surface is made of long, curved, parallel strokes that flow: along the forms where the image has structure, in vortices where it is flat (skies, fields). Thick paint (impasto, visible bristle tracks), high saturation and complementary contrasts (cobalt against chrome yellow, viridian against orange), dark blue contour accents.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| ground | Brush 64 | mean colour |
| flow | Oil 14 | `direction: flow`, `flow_sigma` 9, `swirl` 0.65 (6 vortices), `fixed_len` 9 steps of 0.6 width, `fc` 0.85, `color_jitter` 7 |
| flow | Oil 8 | `swirl` 0.5, 12 steps, thresh 5 |
| flow | Oil 5 | `detail` only, `swirl` 0.3 |
| contours | Brush 3 | `#2a3f8f` on the strongest luminance boundaries (`edge_pct` 85, chains of 30 px or more) |

Palette: k 24, saturation x1.45 plus cobalt, chrome yellow, viridian, cream, violet, orange. Prefilter saturation 1.5, contrast 1.15.

## Do / don't

- Do keep `fixed_len`: strokes must flow past edges, not stop at them.
- Do use the Oil brush for every paint layer (its streaks are the impasto).
- Do change `swirl_seed` to move the vortices if one lands on the face.
- Don't use short strokes or flat fills; don't drop saturation.

About 12,000 to 13,000 strokes, 7 to 8 minutes at 450x600.
