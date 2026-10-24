# pop-art: Warhol and Lichtenstein

Preset: [pop-art.json](pop-art.json).

## What defines it

The subject reduced to a screen print: 4 or 5 luminance bands, each a bold flat colour unrelated to the real one (black shadows, then blue, red, pink, yellow lights), Ben-Day dots over one band, thick black outlines on every band boundary.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| flat | Brush 30 / 14 / 6 / 2 | `labels: bands`: 5 quantile bands of luminance mapped to the 5 colours in order (dark to light), smoothed, specks under 30 cells removed |
| Ben-Day dots | Brush 4 | red dots every 8 px on a square grid over band 3 (pink) |
| outlines | Brush 4 | black on every band boundary, chains of 12 px or more, 2 Chaikin passes |

Palette (`mode: bands`): `#111111`, `#1f4fbf`, `#e8202a`, `#f7a1c4`, `#ffe01a`. Prefilter contrast 1.2.

## Do / don't

- Do swap the 5 colours for another colourway (Warhol's Marilyn: black, turquoise, orange, pink, yellow); order = dark to light.
- Do put the dots on the band that holds the skin or the sky.
- Don't keep realistic colours; don't use translucent tools.

About 2,200 to 2,400 strokes, about 80 s: a good live demo.
