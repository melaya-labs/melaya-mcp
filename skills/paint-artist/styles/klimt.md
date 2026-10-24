# klimt: the golden phase

Preset: [klimt.json](klimt.json). The Kiss, Portrait of Adele Bloch-Bauer I.

## What defines it

- The face, neckline and hands are painted naturally and softly. Their edge is the real contour of the skin, with no frame or oval around it.
- Everything else is gold:
  - the dress and hair become a field of mosaic tesserae and rings in black, bronze, teal and cream;
  - the background becomes a gold mosaic with spirals;
  - gold dots form a halo where the skin meets the ornament.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| gold ground | Brush 64 | `#c9a23a` |
| gold mosaic | Pencil 2 | small squares in three golds, background (`light:42&~skin+5`), density 0.55 |
| dress tesserae | Pencil 3 | 9 px squares every 11 px, coloured by value (black, bronze, teal, ochre, cream from dark to light), dark areas (`dark:42&~skin+5`) |
| spirals, rings, dots | Pencil 2, Brush 4 | bronze spirals in the background; cream, black and teal rings and gold dots on the dress |
| skin | Brush 12, 6; Pencil 3; Pencil 2 on the face | `strokes` clipped to the `skin` mask, grown 1 to 3 px. The mask is the face and hands as the picture draws them: light warm pixels touching the focus ellipses |
| halo | Brush 3 | gold dots in the ring between `skin+3` and `skin+9`: the soft transition into the ornament |

Palette: 16 k-means colours (focus weighted 6x, for the skin) plus gold, light gold, ochre, bronze, black, teal, cream, deep red.

## Do / don't

- Do give the face and hands as `--focus`: the `skin` mask grows from them.
- Do raise `skin.min_L` in the preset if the skin mask spills into a light background.
- Don't use the focus ellipses themselves as the naturalistic area: that is what made the hard oval.

About 12,000 strokes, about 5.5 minutes.
