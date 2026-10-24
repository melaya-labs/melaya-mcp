# Modes 2 and 4: style from a reference, fresh compositions

## Mode 2: paint subject X in the style of painting Y

1. Get Y as a file (the user's image, or a public-domain painting: Wikimedia Commons thumbnails such as `https://upload.wikimedia.org/wikipedia/commons/thumb/.../960px-<file>.jpg` download with a descriptive User-Agent; never fetch the full-resolution original, some are 700 MB).
2. Measure it: `python -m paint_artist analyse Y.jpg --out JOBS/style_y.json`. It reports:

| Feature | Meaning | Drives |
|---|---|---|
| `palette_k` | fewest k-means colours within 6 dE | palette size (mode `reference`: colours taken from Y) |
| `chroma`, `L_mean`, `L_p5`, `L_p95` | saturation, value key and range | prefilter saturation, chiaroscuro vs watercolour |
| `coherence` | structure-tensor coherence at 2 px | directional strokes vs dots / meshes |
| `swirl` | coherence at 2 px minus at 12 px | swirling flow (Van Gogh) |
| `flatness` | share of near-uniform pixels | flat fills (ukiyo-e, pop) vs broken colour |
| `outline` | share of edges that are thin dark lines | contour drawing |
| `texture` | high-pass std | impasto, dots, broken colour |
| `stroke_len_px`, `stroke_w_px` | autocorrelation along / across the local stroke direction | stroke length scale of the base style |

3. It picks a base style by rules (calibrated: Starry Night -> van-gogh, The Great Wave -> ukiyo-e, A Sunday on La Grande Jatte -> pointillism, the Mona Lisa -> chiaroscuro) and tunes palette size, saturation and stroke length. The rules are a first guess: LOOK at Y yourself, then override with `--base STYLE` or edit the JSON (layers, widths, directions, outline on/off, ground colour). Describe to the user what defines Y in a sentence before painting.
4. Paint X with it: `prepare X --job JOB --style JOBS/style_y.json --reference Y.jpg --transfer` (`--transfer` moves X's Lab mean and spread to Y's colour mood; drop it to keep X's own colours), then plan, preview, paint as usual.

Example in [../assets/examples/contact_sheet.png](../assets/examples/contact_sheet.png): the composed still life in the style of Starry Night (analysed, base van-gogh, palette from Starry Night), and the Mona Lisa in the style of The Great Wave (analysed, base ukiyo-e).

## Mode 4: a fresh painting with no source

Either fetch a public-domain reference photo or painting of the subject, or compose one:

```
python -m paint_artist compose landscape --out ref.png          # also: still_life, portrait
python -m paint_artist compose scene.json --out ref.png --height 600
```

Scene JSON (fractions of the canvas, painted in order):

```json
{"size": [450, 600],
 "background": {"stops": [[0, "#24315e"], [0.5, "#f2a65a"], [1, "#2c4a5a"]]},
 "shapes": [
  {"type": "ellipse", "box": [0.56, 0.40, 0.76, 0.55], "fill": "#fff1c4", "glow": 0.06},
  {"type": "polygon", "points": [[0, 0.6], [0.36, 0.36], [1, 0.6]], "fill": "#4a4f7a", "to": "#2e3352", "dir": [0, 1]},
  {"type": "reflection", "y": 0.62, "strength": 0.85, "ripple": 4, "water_mix": 0.25},
  {"type": "ellipse", "box": [0.3, 0.2, 0.6, 0.7], "fill": "#3d6e9e", "sphere": {"light": [-0.6, -0.5, 0.6], "ambient": 0.25, "spec": 0.6}},
  {"type": "noise", "amount": 0.02, "scale": 1.5}
 ],
 "focus": [[0.5, 0.4, 0.17, 0.19]]}
```

Shapes: `ellipse`, `rect` (`box`), `polygon` (`points`); `fill`, optional linear gradient `to` + `dir`, `sphere` lighting (volume, diffuse + specular), `glow`, `blur`, `alpha`; `reflection` mirrors everything above a waterline with ripples and a water tint; `noise` adds texture so painterly layers have something to follow. Compose like a painter: a clear focal point (put it in `focus` and pass it to `prepare --focus`), a light direction, big value masses, then details. Look at `ref.png` before planning, then pick a style (mode 3) or a reference style (mode 2).
