# cubism: analytic cubism

Preset: [cubism.json](cubism.json). Picasso and Braque, 1909 to 1912.

## What defines it

- The subject is broken into small angular planes, seen from several angles at once.
- Each facet is graded light to dark, so the planes seem to tilt.
- Facets are small and dense where the form has detail (face, hands, folds) and large in quiet areas.
- The facet edges follow the real contours, so the figure stays readable.
- A muted, nearly monochrome palette of ochre, umber, grey, slate and cream, with dark facet edges.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| facets | Brush 30 / 14 / 6 / 2 (region fill) | `cells`: voronoi, 300 seeds. 50 % sit on strong structure; the rest follow local detail (`density_gamma` 0.9), 5x denser on the focus. Each cell is cut twice with a straight line placed where the value changes most (`split: edge_line`, `split_depth` 2, cells under 7 L of contrast stay whole). Then `color: shade`: 3 bands 7 L apart, across the facet's edge. Colour match weighted on value (`value_weight` 1.6), restricted to the cubist palette |
| facet edges | Pencil 2 | `outline` on every cell boundary, umber-black |

Palette: 12 fixed muted colours, including a near-black. Prefilter: saturation 0.75, contrast 1.2, gamma 0.85.

## Do / don't

- Do keep `value_weight` above 1 and the splits on: they are what keeps the face and silhouette readable.
- Do lower `n` for synthetic-cubism-like big planes, or raise it for finer fragmentation.
- Don't use saturated colour (that turns it into stained glass); don't blend across facets.

About 4,900 strokes, about 2.5 minutes at 450x672.
