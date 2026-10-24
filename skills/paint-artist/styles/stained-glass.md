# stained-glass: leaded glass window

Preset: [stained-glass.json](stained-glass.json). Gothic cathedral windows, Tiffany.

## What defines it

- The picture is cut into panes of saturated, jewel-coloured glass, in light and dark versions (ruby, sapphire, emerald, amber, amethyst, turquoise, rose, pale gold).
- Panes are small where there is detail, and their edges follow the figure's contours, the way a glazier cuts glass along the drawing.
- Each pane is slightly graded.
- Thick black lead lines run around every pane.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| panes | Brush 30 / 14 / 6 / 2 (region fill) | `cells`: voronoi, 300 seeds following detail (`edge_bias` 0.4, `density_gamma` 0.8, 5x on the focus). Each cell is split by its own value threshold, so pieces follow the contour (`split: value`, min 9 L). Then `color: shade`: 2 bands 6 L apart, light from the upper left. Jewel colours only, matched with `value_weight` 1.5, no jitter |
| leading | Brush 3 | `outline` on every pane boundary, black |

Palette: 21 jewel colours plus lead black. Prefilter: saturation 1.7, contrast 1.1, gamma 0.9.

## Do / don't

- Do keep the value-weighted colour match: the face must stay light and the hair and dress dark.
- Do keep the lead lines unbroken (`min_len` 3).
- Don't add random colour jitter (the figure dissolves); don't use black glass.

About 3,100 strokes, under 2 minutes.
