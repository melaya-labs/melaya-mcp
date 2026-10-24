# chiaroscuro: old-master light and dark

Preset: [chiaroscuro.json](chiaroscuro.json).

## What defines it

Caravaggio, Rembrandt, Georges de La Tour: a dark umber ground laid first and left as the shadows, the lights built up over it from dark to light, a strong spotlight on the focus with everything else falling into darkness (tenebrism), warm earth palette, a unifying warm glaze at the end.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| ground | Brush 64 | `#1b120c` dark umber |
| lights | Brush 24 | thresh 8, `color_order: dark_first` |
| lights | Oil 12 | thresh 7 |
| modelling | Brush 6 | `detail` only |
| accents | Pencil 3 | `finest` only |
| glaze | Watercolour 10 px cells | gain 2.5, never over the face |

Palette: k 28 (focus weight 3) plus the umber. Prefilter: contrast 1.4, gamma 1.3 (darker), saturation 0.9, `vignette` strength 0.75 around the first focus (inner 0.16, outer 0.6).

## Do / don't

- Do give the lit face as `--focus`: the vignette centres on it.
- Do paint dark to light inside each layer, so highlights land last.
- Don't paint the shadows: the ground is the shadow.
- Don't use a light ground or saturated colours.

About 4,600 to 6,400 strokes, 3 to 4 minutes at 450x600.
