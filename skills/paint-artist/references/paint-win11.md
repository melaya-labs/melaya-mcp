# Microsoft Paint (Windows 11): verified facts

Measured live at 1920x1080, display scale 100 %, Paint maximised, zoom 100 %. These are the defaults in `scripts/paint_artist/ui.default.json`; re-derive them elsewhere with [calibration.md](calibration.md).

## UI map (screen pixels)

| Control | Position | Notes |
|---|---|---|
| Pencil button | (262, 88) | Tools group |
| Fill (bucket) | (302, 88) | Tools group, top row middle (verified on screenshots; confirm with `melaya_computer_find` `query: "Fill"` on another build). One click floods the connected area of exactly the clicked colour; no tolerance setting |
| Colour picker (eyedropper) | (302, 127) | Returns to the previous tool after one pick |
| Brushes dropdown | (405, 127) | Opens a SEPARATE popup window: never pin `window_id` |
| Brushes popup items, x = 500 | Brush 165, Calligraphy 211, Airbrush 303, Oil brush 349, Crayon 395, Marker 441, Natural pencil 487, Watercolour 533 | Click the dropdown (foreground), wait 450 ms, click the item, wait 300 ms |
| Size slider | left side panel, `{"label": "Size", "role": "slider"}` | Set with `set_value` |
| Opacity slider | left side panel, `{"label": "Opacity", "role": "slider"}` | Pencil and Brush only |
| Zoom | status bar, bottom right | Must read 100 % |

## Size slider mapping

Slider value v for a brush of px pixels: `v = px - 1` when px <= 22, else `v = (px + 1 + 22) // 2` (64 px -> 43). The emitter caps widths at 64 px.

## Tools as the simulator models them

Measured live on 2026-10-24 with the calibration run ([calibration.md](calibration.md) step 3): a 16 px black stroke on white with each tool. Darkness = mean darkness of the stroke core, thickness = ink area / peak darkness.

| Tool | Darkness, one pass | Thickness at size 16 | Character | stepPx |
|---|---|---|---|---|
| Brush | 1.00 (antialiased edge) | 15.0 px | soft-edged, opaque | 16 |
| Oil brush | 0.81 core (peak 0.89) | 15.4 px | streaky bristle tracks | 4 |
| Watercolour | 0.70 core (two passes 0.89) | 12.0 px area-width | a wet-edge ramp across the stroke (transparent on one side, darkest on the other), hair streaks, bare paper inside wide strokes; modelled as `side_ramp` 0.8, streaks 0.8 to 1.0, alpha 0.75, mean coverage 0.55 (fitted on the live watercolour and sumi-e crops) | 4 |
| Pencil | true alpha = Opacity (0.349 at 35 %, 1.00 at 100 %) | 16.0 px | hard, aliased pixels | 16 |
| Calligraphy | 1.00 | nib 14 px at 135 deg (screen y down), hairline 1.5 px | thick-thin: hairline along the nib (down-left / up-right), full width across it | 4 |
| Airbrush | 0.11 (peak 0.12) | 12.1 px | faint speckle spray, needs many passes | 4 |
| Crayon | 0.70 (peak 0.77) | 10.6 px | grainy, tapered profile | 4 |
| Marker | 0.75, flat | 18.5 px | flat, wider than its size, translucent | 4 |
| Natural pencil | 0.34 (peak 0.38) | 12.6 px | light grainy graphite | 4 |

`paint_tools.json` holds these as `alpha`, `width_scale` (thickness / 16) and `nib`, with `measured: true`. Earlier figures (Brush 0.90, Watercolour 0.57 and 0.78) were band averages that included the soft edges; the core values above replace them.

Paint renders a stroke as one unit (it does not darken where it crosses itself). Opacity applies to Pencil and Brush; the emitter sets it after every switch to those tools.

## Colours: the palette strip

The Edit Colours dialog hangs Paint: never open it. Colours come from a palette strip painted into the canvas image itself (`prepare` writes it): up to 40 swatches at canvas x 10..40, `swh` px high (17 for 40 colours on a 690 px canvas), 1 px white gap, starting at y 9. A pick = mouse down/up on the colour picker, move to the swatch centre, mouse down/up. Consequences: no stroke may ever cross canvas x < 44 (the emitter clamps by half the brush width), and the frame starts at x 46.

## Canvas geometry

- `prepare` builds a canvas of (60 + W + 30) x (9 + H + 9): drawing area at (60, 9). The Mona Lisa: 540 x 690, drawing 450 x 672.
- Opened maximised at 100 %, the canvas is centred in the workspace: centre (960, 583.5) at 1920x1080 (the half pixel goes down), so a 540x690 canvas has its origin at (690, 239) and the drawing box at X0 = 750, Y0 = 248, 450 x 672; a 450x498 canvas sits at (735, 335). The reference Mona Lisa plan assumed (690, 238), one pixel high, which was harmless; `locate` measures it exactly. Height up to about 790 px fits the workspace (y 176..990).
- The canvas resize handles sit ON the canvas edges (x 690 / 960 / 1230, y 239 / 584 / 929 for the Mona Lisa). A stroke starting there drags the canvas: a frame stroke once shrank it to 541x1 (Ctrl+Z restored it). The emitter keeps every point 5 px inside the canvas.

## Behaviour to plan around

- The first click after a ribbon click and very fast consecutive actions are handled by the Melaya helper; tool-switch clicks are still `onError: "continue"` with waits.
- Brushes popup: if a tool switch is missed, the next strokes are painted with the previous tool. Raise `waits_ms` in `ui.json` on a slow machine.
- After the run Paint shows the result unsaved. Save at once: check the window title first (`melaya_computer_current_app`), then Ctrl+S; in the live runs it saved without an approval prompt. Never send keys to a Paint window whose title changed.

## Tools considered for speed and not used

- **Shapes (Rectangle, Ellipse with a solid fill):** reachable without a dialog: the Shapes gallery, the Fill dropdown set to Solid colour, and the fill colour is Colour 2 (set by right-clicking with the colour picker). Not used. Each shape stays a selected, editable object until the next action commits it, needs a separate drag and colour-2 handling, and is not faster than a Pencil ring plus one bucket click for flat regions, nor than a Brush dab for dots. Not measured live; add it to speed-calib before relying on it.
- **Ribbon colour slots:** the 20 fixed colours could set black or white in one click instead of a 5-step pick. The custom slots can only be filled through Edit Colours, which hangs Paint, so the palette strip stays the colour source.
