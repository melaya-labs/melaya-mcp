# impressionist: Monet

Preset: [impressionist.json](impressionist.json).

## What defines it

Light and atmosphere over contour. Broken colour: short separate dabs of fairly pure paint laid side by side and left unblended, so the eye mixes them. A high-key palette with no black (shadows are blue and violet), a warm toned ground glimpsing between dabs, strokes mostly horizontal (water, sky) with lively angle variation, detail suggested rather than drawn.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| ground | Brush 64 | warm ochre `#c9a978` |
| dabs | Oil 18 | `direction: angle` 0 deg +-30, `max_len` 2, `color_jitter` 7, `seed_jitter` 0.5 |
| dabs | Brush 11 | angle -8 deg +-40, thresh 5 |
| dabs | Brush 7 | along contours, thresh 6 |
| accents | Brush 4 | `detail` only, thresh 9 |

Palette: k 26, saturation x1.3, value +4, `min_L` 24 (no black), plus cream, cobalt, cadmium yellow, rose. Prefilter saturation 1.25, gamma 0.9 (lighter).

## Do / don't

- Do keep strokes short (1 to 3 widths) and let the ground show.
- Do raise `color_jitter` for more vibration, lower it for calmer surfaces.
- Don't use the Pencil or outlines; don't let darks go to black.
- Don't go below width 4: fine strokes turn it into a photo.

About 13,000 strokes, 6 minutes at 450x600.
