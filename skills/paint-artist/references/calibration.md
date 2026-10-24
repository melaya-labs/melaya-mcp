# Calibration: ui.json and tool darkness

The defaults (`scripts/paint_artist/ui.default.json`) are for Paint on Windows 11 at 1920x1080 and 100 % display scale. Re-derive whenever the resolution, the display scale, the Paint version or the ribbon layout differs, and every time you are unsure: one wrong coordinate paints 17,000 strokes in the wrong place.

## 1. Canvas origin and scale (every run)

With the canvas open, maximised, zoom 100 % and Paint in front:

```
python -m paint_artist locate --job JOB --take --write-ui
```

`--take` grabs the desktop with ffmpeg (`ffmpeg -f gdigrab -i desktop -frames:v 1 grab.png`, option order matters). The locator finds the largest near-white region with the canvas aspect, returns `origin` (screen x, y of the canvas top-left), `scale` (screen pixels per image pixel at 100 % zoom, which equals the display scale) and `swatch_err` (mean RGB error at every swatch centre; under 3 means every pick will land). `--write-ui` saves `JOB/ui.json` with `canvas_origin` and `scale`; `emit` then uses them. Also look at the screenshot yourself (`melaya_computer_screenshot`): canvas fully visible, nothing over it, status bar at 100 %.

If `swatch_err` is high: the canvas is scrolled or zoomed, a dialog covers it, or the wrong window is in front. Fix, then locate again.

## 2. Ribbon controls (new resolution, DPI or Paint version)

Find each control and write its centre into `JOB/ui.json` (copy `ui.default.json` first):

| Key | How to find it |
|---|---|
| `pencil` | `melaya_computer_find` `query: "Pencil"` -> bounds centre |
| `picker` | `melaya_computer_find` `query: "Color picker"` (or "Colour picker") |
| `brushes` | `melaya_computer_find` `query: "Brushes"` |
| `brush_items` | click Brushes, then `melaya_computer_screenshot` (the popup is its own window: `scope: "display"`) or `melaya_computer_find` per item name; record each item centre; press Escape |
| `size_slider`, `opacity_slider` | `melaya_computer_find` `query: "Size"` / `"Opacity"`, `role: "slider"`; keep `{label, role}` targets |
| `canvas_center`, `viewport` | from `locate` on a canvas you opened: `origin + scale * canvas_size / 2`; viewport = the empty workspace box |

Verify the size mapping once: set the Size slider to 43 with `melaya_computer_set_value` and paint one test stroke; it should be 64 px wide at 100 % zoom. If not, update `size_map` and `emit_paint.size_value`.

At a display scale other than 100 %, keep zoom at 100 %: `locate` reports the scale (for example 1.25) and the emitter multiplies canvas coordinates by it. Ribbon positions must then be measured, not scaled.

## 3. Tool darkness, thickness and nib (new Paint build, or a tool still `measured: false`)

One short batch (about 10 s, 142 steps) paints 16 px black strokes on a white calibration canvas: Brush, Oil brush, Watercolour once and twice, Pencil at 35 % and 100 %, Calligraphy, Airbrush, Crayon, Marker and Natural pencil horizontally, and the Calligraphy brush again vertically and on both diagonals.

```bash
cd "SKILL_DIR/scripts"; C="$HOME/paint-jobs/calib_tools"
python -m paint_artist calib-plan --job "$C" --name pa_calib_tools        # canvas.png + ~/.melaya/plans/pa_calib_tools.json
cp "$C/canvas.png" "$C/pa_calib_tools.png"
powershell -NoProfile -Command "Start-Process mspaint -ArgumentList '\"$(cygpath -w "$C/pa_calib_tools.png")\"'"
# pre-flight (SKILL.md): other Paint windows minimised, this one focused + maximised, zoom 100 %, screenshot check
python -m paint_artist locate --job "$C" --take --write-ui                  # expect origin [685, 335], swatch_err < 2.5
python -m paint_artist calib-plan --job "$C" --name pa_calib_tools          # re-emit with the measured origin
# melaya_computer_batch {"steps": [], "plan": {"file": "pa_calib_tools.json"}}   (no window_id)
python -m paint_artist calib-measure --job "$C" --take --install            # measure, write paint_tools.json
```

`calib-measure` samples the darkness profile across each stroke. It reports per stroke:
- `alpha`: mean darkness of the stroke core (profile at 75 % of its peak or more), which is the coverage of one pass;
- `peak`;
- `thickness_px`: ink area / alpha;

and for the Calligraphy brush the nib angle and nib length, fitted on the four directions (thickness = nib x |sin(direction - angle)| + pen).

`--install` writes `alpha`, `width_scale` (thickness / 16), the nib and `measured: true` into `scripts/paint_artist/paint_tools.json`; without it the result goes to `JOB/tools.json` only, which you copy into a job folder to use for that job. After installing, re-run `plan` for the styles that use the re-measured tools (sumi-e uses Calligraphy), and keep the skill's installed copy in sync.

Reference values (live, Windows 11 Paint, 2026-10-24): Brush 1.00, Oil 0.81, Watercolour 0.70 one pass / 0.89 two passes (12 px wide at size 16), Pencil at 35 % = 0.349, Calligraphy 1.00 with a 14 px nib at 135 deg, Airbrush 0.11, Crayon 0.70, Marker 0.75 (18.5 px wide), Natural pencil 0.34. Full table: [paint-win11.md](paint-win11.md). `calib-measure` also writes `calib_live.png` (the painted strokes) and `calib_measured.json` (all numbers).

## 4. Speed calibration (fastest safe pointer settings, Fill connectivity)

```bash
cd "SKILL_DIR/scripts"; C=$(cygpath -m "$HOME/paint-jobs/speed_calib")
python -m paint_artist speed-calib --job "$C"                # canvas + 6 plans: pa_speed_setup, pa_speed_s0 .. s4
cp "$C/canvas.png" "$C/pa_speed.png"; powershell -NoProfile -Command "Start-Process mspaint -ArgumentList '\"$(cygpath -w "$C/pa_speed.png")\"'"
# pre-flight, then:
python -m paint_artist locate --job "$C" --take --write-ui && python -m paint_artist speed-calib --job "$C"   # re-emit at the real origin
# 6 batch calls in order, Paint in front, no window_id: pa_speed_setup.json, pa_speed_s0.json ... pa_speed_s4.json; note each duration
python -m paint_artist speed-measure --job "$C" --take --times T0,T1,T2,T3,T4 [--install]
```

- **Setup plan** (slow reference): closed boxes around every test cell, so a leaking fill stays contained; the 1 px rings to be filled; and a 1 px diagonal diamond probe.
- **Rows s0..s4:** the same Brush (6 px) and Pencil (2 px) pattern (zigzag, short strokes, dots) and three Fill clicks, at increasing settings: (speed, stepPx, strokeGapMs) = (1500, 2, 10), (8000, 16, 2), (12000, 16, 1), (16000, 16, 0), (20000, 16, 0).
- **speed-measure** compares every row with the slow s0 row (missing pixels with a 1 px tolerance) and counts the filled rings. It reads the probe: an 8-connected bucket leaks out of the diagonal diamond, a 4-connected one stays inside. It recommends, per tool, the fastest setting (by your measured durations) with under 1 % missing pixels and all fills done.
- **`--install`** writes `speed`, `stepPx`, `strokeGapMs` for brush and pencil, the fill `strokeGapMs`, and the fill `connectivity` / `fill_conn` into `paint_tools.json`. The emitter uses per-tool settings from there.
- **Timing:** re-fit the timing profile when the settings change: the durations of the rows are in `speed_measured.json`.
