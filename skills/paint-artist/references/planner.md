# The planner and the preset schema

`scripts/paint_artist/planner.py` turns a prepared job and a preset into layers of strokes. It is app-agnostic: a stroke is `[palette index, [[x, y], ...]]` in drawing-area pixels, a layer is `{name, tool, width, opacity, strokes}`. After planning each layer it simulates it (`simulate.py`, tool model from the adapter), so the next layer sees the real canvas, translucent tools included.

## Pipeline

1. **Palette** (`prepare`): k-means in CIELAB (numpy, k-means++ init, optional weight on the focus ellipses), cluster means in RGB, sorted dark to light into the swatch strip. Modes: `kmeans` (from the target), `reference` (from a reference painting), `fixed` (preset colours), `bands` (luminance bands mapped to fixed colours). Options: `k`, `focus_weight`, `include` (always-present colours), `snap` (pull toward a period palette), `saturation`, `value`, `min_L` (no black: darks become deep blue-violet). Frame colours (walnut, gold, dark) are reused when a palette colour is within 6 dE, else appended. At most 40 swatches.
2. **Prefilter** (`prepare`), in this order:
   - `saturation`, `contrast`, `gamma`, `brightness` in Lab;
   - `complement_shadows` {`L`, `strength`, `soft`, `warm_to`, `cool_to`}: below `L`, warm shadows go green and cool ones violet, keeping the value (Fauve);
   - `warp` {`amp`, `wavelength`, `seed`}: smooth wave distortion (Expressionist);
   - `vignette` {`strength`, `inner`, `outer`}: tenebrism around the first focus;
   - `fade_edges` {`width`, `noise`, `noise_scale`, `roundness`}: dissolve into bare paper toward a rounded-rectangle border, slightly irregular; writes `fade.png`, the `paper` mask.

   Reinhard colour transfer comes first, with `--reference --transfer`.
3. **Masks**: `struct` = gaussian(Sobel(gaussian(L, 1)), 3). `detail` = top 50 % of `struct` (dilated) plus the focus; `finest` = top 15 % plus the dilated first focus; `focus`, `primary` (first focus only), `fine` (focus dilated 6 px), `skin` (the face and hands as the picture draws them: light warm pixels touching the focus ellipses; `skin.min_L` in the preset), `paper` (faded border), `band:<i>` (after a `flat` layer), `dark:<L>`, `light:<L>`. Grow a mask with `+N` (`skin+3`), negate with `~`, intersect with `&`. Percentiles: `masks.detail_pct`, `masks.finest_pct`.
4. **Layers** in preset order, then the frame.

## Layer types and parameters

| Type | Parameters (defaults) | What it does |
|---|---|---|
| `ground` | `color` (`mean`, `darkest`, `#hex`, index, `none`), `width` 64, `spacing` 0.75 | One serpentine stroke covering the drawing area edge to edge (rows evenly spaced, the first and last touching the edges), kept width/2 inside |
| `strokes` | `tool`, `width`, `thresh` 0, `max_len` 10, `min_len` 2, `fc` 0.6, `mask`, `fine_len` 3, `fine_scale` 0.6, `use_fine` true, `direction` (`contour`, `flow`, `angle`, `gradient`), `angle`, `angle_jitter`, `flow_sigma` 6, `swirl` 0, `swirl_n` 5, `swirl_seed` 7, `fixed_len` false, `step` 1.0, `grid` 1.0, `seed_jitter` 0, `len_jitter` 0, `color_jitter` 0, `blur` 0.5, `opacity` 1, `color_order` (`index`, `dark_first`, `light_first`), `clip_mask` false | Hertzmann-style: on a grid of `width x grid`, where the mean Lab error between canvas and the target blurred at `width x blur` exceeds `thresh` (x `fine_scale` in `fine`), seed at the worst pixel, pick the palette colour whose blend at the tool's alpha over the current canvas lands closest (random among those within `color_jitter`), trace along the direction field in steps of `width x step` with inertia `fc`, stop after `min_len` once the canvas is closer than the stroke colour (unless `fixed_len`), at most `max_len` steps (`fine_len` in `fine`). Strokes are grouped by colour (one pick per colour per layer). |
| `glaze` | `tool` watercolour, `cell` 8, `gain` 3.0, `protect` `primary`, `mask` | Per cell, the palette colour whose translucent blend lowers the error most; cells gaining more than `gain` become row runs. Never over the protected (finished) face. |
| `bokashi` | `color`, `y0`, `y1` (fractions), `passes` 3, `width` 16, `spacing` 0.45 | Woodblock gradient: overlapping translucent horizontal passes, each shorter |
| `hatch` | `tool` pencil, `width` 1, `opacity`, `color`, `levels` [{`L`, `angle`, `spacing`}], `min_run` 4, `jitter` 0.5, `blur` 1.5, `mask` | For each value level, parallel lines at `angle` every `spacing` px wherever the smoothed L is below `L` |
| `dots` | `tool`, `width` 6, `spacing` 6, `grid` (`hex`, `square`), `jitter` 0.3, `color` (`fs` or a colour), `complement` 0, `thresh` 0, `mask` | Dots on a grid; `fs` = Floyd-Steinberg error diffusion in linear RGB over the dot grid (optical mixing), `complement` = share of complementary dots; `thresh` skips dots where the canvas is already close |
| `flat` | `tool` brush, `labels` (`nearest`, `bands`), `band_edges`, `scale` 2, `tips` [15, 7, 3, 1], `smooth` 2, `minsize` 20, `blur` 1.5, `first_is_ground` true, `ground_width` 64 | Posterised regions (mode filter + despeckle), the biggest laid as a ground, the others filled with serpentine strokes kept inside each region (tip cascade, coarse first). Sets the label map used by `outline` and `band:<i>` |
| `outline` | `tool`, `width` 2, `color` `darkest`, `source` (`labels`, `luminance:<n>`), `min_len` 8, `simplify` 0.9, `smooth` 0, `edge_pct`, `mask`, `blur` 2 | Boundary chains of the label map (or of n luminance levels), traced, simplified (RDP), `smooth` Chaikin passes (staircase chains become flowing key lines), kept if long enough and on strong structure (`edge_pct`). With `source: labels` after a `cells` layer it draws every cell boundary (leading, facet edges) |
| `cells` | `partition` (`voronoi`: `n`, `edge_bias`, `density_gamma` (cells follow local detail), `focus_density`, `split` (`edge_line`: straight cut where the value changes most; `value`: split by the cell's own value threshold), `split_depth`, `split_min_dL`; `grid`: `cols`, `rows`; `mondrian`: `n`, `min_px`, `min_frac`, `detail_power`), `color` (`nearest`, `shade`: `bands`, `shade_step`, `shade_dir` deg / `edge` / `random`; `mondrian`: `primary_share`, `black_share`, `grey_below`; `dither`: `dither`), `colors` (restrict to these), `match` ({paint: proxy}: choose each paint where the image looks like its proxy), `value_weight` (weight of L in the colour match: keeps the subject readable in a stylised palette), `jitter` (dE window, random pick per cell), `fill` (`regions` with `scale`/`tips`, or `rects` with `rect_width`), `lines` {`color`, `width`, `thick_width`, `thick_levels`} | Partition into cells, colour each, fill with paintable strokes; `rects` = overlapping horizontal lines with ends inset by half the width (crisp corners; adjacent same-colour grid blocks merged); `lines` = mondrian split lines drawn straight. Sets the cell-id map for `outline`. Code and full doc: `cells.py` |
| `ornament` | `motif` (`squares`, `spirals`, `rings`, `dots`, `seal`), `size`, `spacing`, `width` (line width), `grid` (`square`, `hex`), `jitter`, `size_jitter`, `density`, `colors` (dark to light), `color_by` (`luminance`, `random`), `turns`, `mask`, `at` (seal position) | Decorative motifs on a grid inside a mask (Klimt tesserae and spirals, a hanko seal); squares are built from overlapping short lines |

The simulator models every tool from `paint_tools.json`: `alpha` (coverage of one pass), `width_scale` (measured ink thickness / nominal size), `bristles` (streaks), `soft` (blurred edge), `nib` (Calligraphy: a flat nib at that angle, strokes thick or thin with direction). `measured: true` marks values taken from a live calibration run.

Keeping the subject recognisable in abstract styles: let cells follow detail (`density_gamma`, `focus_density`, `detail_power`), split cells on edges (`split`), and match colours on value (`value_weight`, `match`). Without these, Voronoi, Mondrian and mosaic styles turn the picture into random pattern.

`frame` (preset key, used when the job has a frame): `inset` 14, `band_width` 11. Walnut bands with the Pencil in the margins, a gold fillet at the inset, a dark line 3 px inside it; everything 5 px clear of the canvas edges.

`detail` (CLI) divides every `thresh`, `gain` and the grid density by itself (lower = fewer strokes); `plan --seconds/--budget` adjusts it automatically.

## Preset file

```json
{
 "name": "my-style",
 "description": "what defines the style, in one or two sentences",
 "palette": {"mode": "kmeans", "k": 24, "saturation": 1.2, "include": ["#1d3fa0"]},
 "prefilter": {"saturation": 1.2, "contrast": 1.1, "gamma": 1.0, "vignette": null, "fade_edges": null},
 "masks": {"detail_pct": 50, "finest_pct": 85},
 "layers": [
  {"type": "ground", "color": "mean", "width": 64},
  {"type": "strokes", "tool": "oil", "width": 14, "thresh": 0, "max_len": 8, "direction": "flow"},
  {"type": "strokes", "tool": "brush", "width": 6, "thresh": 6, "max_len": 5, "mask": "detail"}
 ],
 "frame": {"inset": 14, "band_width": 11}
}
```

Edit `JOB/preset.json` and re-run `plan` to iterate without re-preparing (palette and prefilter changes need `prepare`).

## Accuracy notes

- With the old sim assumptions (opaque brush, antialiased pencil, flat mean ground, the original palette) the package reproduces the original Mona Lisa plan: sim dE 5.28 inset 16 (original 5.29). The default tool model uses the live-measured tools (Brush 1.00 with its measured width, Oil 0.81, Watercolour 0.70 and narrower, aliased Pencil, the real ground stroke) and gives 5.61 for the bundled subject with the frame lines that fall inside the 16 px inset; the reference live run scored 6.30 on the same crop.
- `strokes` colour choice is translucency-aware: with the Watercolour (0.70) it picks a darker paint so the blend lands right.

## Fast rendering (scripts/paint_artist/fastpaint.py)

Every layer goes through a stroke optimiser before it is simulated, so the simulation shows exactly what will be painted:

- **Colour merge:** colours of one layer closer than `colour_merge_dE` (preset key, default 2.0 Lab) become the most used of them, so there are fewer picks.
- **Collinear pruning:** exactly collinear points are dropped, with no change to the pixels.
- **Chaining:** strokes whose ends touch (within 0.6 px) are joined, which paints the same pixels with fewer presses.
- **Ordering:** within each colour, strokes are ordered by nearest neighbour, then 2-opt on the pen-up travel. Strokes are reversed only for direction-free tools (never Watercolour with its wet-edge ramp, nor the Calligraphy nib).

Preset key `optimise: false` turns it off.

`render` on `flat` and `cells` layers chooses how the flat regions are painted:

| `render` | How |
|---|---|
| `strokes` | serpentine region fills (tip cascade) or rectangle lines, as before |
| `fill` | outline + bucket fill: each connected region of one colour gets a 1 px Pencil ring in its own colour along its inner border, then ONE click of Paint's Fill tool inside each interior part |
| `auto` | plan both, price both with the timing model, keep the cheaper (set on pop-art, stained-glass, cubism, ukiyo-e, mondrian, pixel-art) |

**Fill safety.** The Fill tool's connectivity (`fill_conn` in `paint_tools.json`) decides the ring:
- `both` (default, safe for either kind of bucket): the 8-neighbour border is ringed (no leak even for an 8-connected bucket), and every 4-connected interior part gets its own seed (full coverage even for a 4-connected one).
- `4` or `8`, once `speed-measure` has read Paint's real connectivity; 4 is the leanest.

Every fill is verified in the simulator (pencil rasterisation plus flood). A region that would leak, or a tiny one, is painted with 1 px Pencil rows instead, and the simulator models the bucket exactly (`simulate.flood_fill`).

Measured on the Mona Lisa (recorded profile, same detail): pop-art 156 -> 73 s (box), 141 -> 92 s (full canvas); ukiyo-e 155 -> 95 s; stained-glass 151 -> 114 s; mondrian 62 -> 37 s; pixel-art 123 -> 104 s. Cubism keeps strokes: its banded facets make too many tiny regions. Painterly styles gain only a few percent from ordering: their cost is the number of presses, and dots are the slowest (about 36 ms each when recorded).
