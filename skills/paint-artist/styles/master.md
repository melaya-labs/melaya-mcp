# master: faithful 1:1 reproduction

Preset: [master.json](master.json). The exact recipe of the Mona Lisa run (live dE 6.30, face 5.36, 512 s).

## What defines it

Fidelity, not a look: as many colours as the strip holds (40, k-means in Lab weighted 4x on the focus), detail spent where the image has structure, soft where it is smooth, the face finished with the finest tools and protected from the final glaze.

## Recipe

| # | Layer | Tool, width | Rule |
|---|---|---|---|
| 0 | ground | Brush 64 | one serpentine in the mean colour |
| 1-2 | strokes | Brush 32, 16 | contour strokes, up to 12 steps, thresh 0 / 6 |
| 3 | strokes | Oil 8 | off the focus (texture where it reads as paint), thresh 7 |
| 4 | strokes | Brush 8 | on the focus, short (5), thresh 6 |
| 5 | strokes | Brush 4 | smooth areas only (`~detail`), thresh 8 |
| 6 | strokes | Pencil 4 | structure everywhere (`detail`: hair, veil, folds, rocks), thresh 6.5 |
| 7 | strokes | Pencil 2 | finest structure + face (`finest`), thresh 7.5 |
| 8 | glaze | Watercolour 8 px cells | sfumato where it gains > 3 dE, never over the face |
| 9 | frame | Pencil 11 / 3 / 2 | walnut bands, gold fillet, dark line |

## Use

`prepare SRC --style master --focus <face ellipse> [--focus <hands ellipse>] --height 672`. Always give the face as the first `--focus`: it gets the finest strokes, the glaze protection and the face score. For the Mona Lisa: `--focus 0.47,0.27,0.13,0.14 --focus 0.47,0.79,0.26,0.09 --face-box 0.32,0.12,0.62,0.42`.

## Do / don't

- Do keep the estimate under 480 s (recorded profile; the plan default trims detail automatically).
- Do score with `score` (identical crops) and report live and sim.
- Don't add outlines or colour jitter: they cost fidelity.
- Don't lower the palette below 32 colours for a photo-real subject.
