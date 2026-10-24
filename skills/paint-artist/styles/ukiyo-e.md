# ukiyo-e: Japanese woodblock print

Preset: [ukiyo-e.json](ukiyo-e.json). Analysing The Great Wave selects this base.

## What defines it

A print, not a painting: a few flat colour areas, each printed from one block with no shading inside, a restricted period palette (Prussian blue, indigo, vermilion, ochre, sage, pine, rose, paper cream), crisp dark sumi key lines on every boundary, and the bokashi gradient (typically the top of the sky) as the only modulation.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| flat | Brush 30 / 14 / 6 / 2 | 12 k-means colours snapped 75 % to the period palette, mode filter 2, specks under 30 cells removed, biggest area as ground, others filled inside their region (tip cascade) |
| bokashi | Watercolour 20 | Prussian blue over the top 16 %, 3 overlapping passes |
| key lines | Pencil 2 | sumi black `#1a1a1a` on every region boundary, chains of 12 px or more, 2 Chaikin passes (flowing, not staircase) |
| face lines | Pencil 1 | fine lines on 6-level luminance boundaries inside the face only (eyes, brows, nose, mouth), like a woodblock bijin face |

Palette also includes sumi black and paper cream.

## Do / don't

- Do keep regions big (`smooth`, `minsize`): fragmented regions read as posterised photos.
- Do put the bokashi where the sky is; move it with `y0` / `y1`.
- Don't shade inside regions; don't use Oil or soft outlines.

About 1,100 to 1,700 strokes, 70 to 85 s: a good live demo.
