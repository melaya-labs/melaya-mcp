# mondrian: De Stijl portrait

Preset: [mondrian.json](mondrian.json). Piet Mondrian's grid language, applied so that the portrait still reads.

## What defines it

- Only horizontal and vertical black lines and flat rectangles.
- Paint only in primary red, blue and yellow, black, grey, light grey and white.
- No curves, gradients or brushwork.
- In this portrait version the rectangles are small where the picture has detail (face, hands, the edge of the silhouette) and large in quiet areas, and every colour stands for a part of the image:

| Paint | Stands for |
|---|---|
| yellow | light skin |
| red | warm mid tones |
| blue and black | the darks |
| white and greys | the light background |

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| rectangles | Pencil 8 (`fill: rects`, crisp corners) | `cells`: mondrian partition, 170 cells. The cell with the most value variation is split next (`detail_power` 1), along its strongest straight edge, never closer than 20 % / 9 px to a side. `color: nearest` through proxy colours (`match`: each paint is chosen where the image looks like its proxy), `value_weight` 1.5, `jitter` 5 (blue and black alternate in the darks) |
| lines | Brush 3, Brush 6 for the first two split levels | the split lines, straight and full length, black |

Palette: black, grey, light grey, white, red, blue, yellow (fixed; the colour match is restricted to these).

## Do / don't

- Do adapt the `match` proxies to the subject: pick the image colours that each paint should stand for.
- Do lower `n` (20 to 40) and set `detail_power` 0 for a classic, sparse Mondrian that does not trace the subject.
- Don't add curves or outlines; don't use the Brush for the fill (it leaves stripes).

About 1,300 strokes, under 1 minute: a quick live demo.
