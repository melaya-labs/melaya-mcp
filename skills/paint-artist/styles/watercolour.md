# watercolour: wet washes on white paper

Preset: [watercolour.json](watercolour.json).

## What defines it

Transparency: light washes laid first, darker ones glazed over them, each one darkening what is below; soft, bleeding edges; the white of the paper is the only white (never painted); the picture dissolves into bare paper toward the borders.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| wash | Watercolour 44 | thresh 18, `max_len` 3, `grid` 1.5, `seed_jitter` 0.5 (gaps stay paper) |
| wash | Watercolour 24 | thresh 15, `grid` 1.4 |
| wash | Watercolour 12 | thresh 13, `grid` 1.3 |
| detail | Watercolour 5 | `detail` only, thresh 13 |

Everything is the Watercolour tool (live: a wet-edge ramp across each stroke with hair streaks and paper showing; the model is fitted on a live painting of this preset, so the simulation now looks as streaky as Paint's result; expect live_vs_sim around 10 from the streak placement alone): the planner picks each paint for how it lands over what is already there, so it chooses darker paints than the target colour. Prefilter: gamma 0.62 (much lighter), contrast 0.9, saturation 1.2, `fade_edges` 0.11 (soft rounded-rectangle vignette of bare paper with a slightly irregular edge). Palette k 20, saturation x1.1. No ground.

## Do / don't

- Do keep thresholds high: leaving paper is the style.
- Do keep the big washes first; fine strokes only on `detail`.
- Don't use Brush, Oil or Pencil; don't add a ground or a dark outline.
- Don't expect a low dE against the source: it is lighter by design.

About 2,400 to 3,200 strokes, under 2 minutes at 450x600: a good live demo.
