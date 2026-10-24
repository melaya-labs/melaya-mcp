# pixel-art: 8-bit

Preset: [pixel-art.json](pixel-art.json).

## What defines it

A coarse grid of square, flat blocks (here 36 across, 54 down at 450x672) and a small limited palette (14 colours). In-between tones come from ordered dithering (a regular checker of two colours). Edges are crisp, with no antialiasing.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| blocks | Pencil 4 (`fill: rects`) | `cells`: grid, 36 columns, square blocks. Then `color: dither`: 4x4 Bayer threshold on the block grid, spread 7 L. Rows of same-colour blocks merged, each filled with overlapping horizontal Pencil lines, ends inset by half the width |

Palette: 14 k-means colours (saturation x1.25, focus weighted 3x). Prefilter: saturation 1.2, contrast 1.1.

## Do / don't

- Do use the Pencil (aliased): the Brush softens block edges.
- Do change `cols` for resolution (24 for chunky, 48 for detailed); `dither: 0` for flat blocks.
- Don't exceed 16 colours.

About 4,200 strokes, about 2 minutes.
