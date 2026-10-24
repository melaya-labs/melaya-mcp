# pencil-sketch: graphite hatching

Preset: [pencil-sketch.json](pencil-sketch.json).

## What defines it

Values made only by lines: hatching density and the number of crossing directions (one direction for light greys, two for mid tones, three to five crossings for darks), a few confident contour lines on the strongest edges, graphite grey rather than black, paper left white in the lights and around the border.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| hatch | Pencil 1 at 55 % | 5 value levels: L < 78 at 45 deg every 6 px, < 62 at -45 deg / 5 px, < 46 at 0 deg / 4 px, < 32 at 90 deg / 3 px, < 20 at 30 deg / 3 px; 0.6 px endpoint jitter |
| contours | Pencil 1 at 85 % | boundaries of 5 luminance levels on strong edges (`edge_pct` 75), chains of 14 px or more, not along the faded border (`~paper`) |

Palette: 3 fixed graphite greys. Prefilter: saturation 0, contrast 1.3, gamma 0.85, `fade_edges` 0.08.

## Do / don't

- Do keep the Pencil's partial opacity: crossings darken like real graphite (true alpha in Paint).
- Do change the angles for a different hand (for example 60 / -30 / 15).
- Don't use the Brush (its soft edge reads as charcoal, not pencil); don't fill areas.

About 1,500 to 1,700 strokes, about 1 minute: the fastest style, a good live demo.
