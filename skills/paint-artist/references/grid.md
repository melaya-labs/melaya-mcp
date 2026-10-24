# Grid composite: one picture, several styles

One image split into R x C cells by straight dark dividers, each cell painted in its own style, cell by cell (a cell is finished before the next starts, so a recording can zoom into each in turn), then the dividers, then the frame.

## Commands

```bash
cd "SKILL_DIR/scripts"
J=$(cygpath -m "$HOME/paint-jobs/grid_mona"); N="pa_grid_mona"
python -m paint_artist prepare --subject mona_lisa --grid 2x2 --styles master,pop-art,pointillism,cubism --job "$J" \
       [--split-x 0.45] [--split-y 0.37] [--order 0,1,2,3] [--divider-width 5] [--inset 2] [--divider-color "#1a1a1a"] \
       [--cell-override '{"2": {...}}']
python -m paint_artist plan --job "$J"        # plans every style on the whole image, clips, writes canvas.png + preview.png
cp "$J/canvas.png" "$J/$N.png"                # open THIS in Paint (canvas.png is written by plan, not prepare)
# pre-flight + locate --write-ui as in SKILL.md, then:
python -m paint_artist emit --job "$J" --name "$N"   # ONE plan if the estimate fits 480 s (recorded profile), else N_cell<i>.json per cell
# melaya_computer_batch {"steps": [], "plan": {"file": "<N>.json"}}  (one call per plan file, in order; no window_id)
# save (title check + Ctrl+S), then:
python -m paint_artist score --job "$J" --file "$J/$N.png"   # overall and per-cell live_vs_sim
```

- `--styles` takes style names or preset files, in reading order (left to right, top to bottom).
- `--order` sets the paint order (cell indexes).
- `--split-x` / `--split-y` place the dividers as fractions of the drawing area: `cols - 1` and `rows - 1` increasing values, for example `--split-x 0.33,0.7` for 3 columns. The default is uniform.
- `--cell-override` merges preset keys into one cell's style. `layers` replaces the whole layer list, so copy the style's layers and edit them. Pass the JSON inline, or with `"$(cat file.json)"`.

## How it works

- **Each style sees the whole image.** Each cell gets a sub-job in `JOB/cells/<i>_<style>/`, prepared and planned on the whole picture, so its palette, masks and stroke field are the same as for a full painting of that style.
- **Clipping.** Each stroke is clipped to its cell, so that its painted footprint (centreline +- half the width) stays `inset` px from every internal divider centre line. Outer edges follow the usual canvas rules. Pieces shorter than 2 px are dropped; dots are kept when inside.
- **Grounds per cell.** Ground fills (the wide serpentines) are re-laid inside each cell, plus an 8 px loop of the same colour along the cell's inner edges, because a clipped whole-image serpentine leaves bands and round-cap corners.
- **Divider and inset.** Keep `inset` at or below divider width / 2 (defaults 2 and 5 px): then no stroke crosses a divider's centre line (no bleed), and the divider covers the clipped edge (no white seam).
- **Palette.** Only the colours each cell really uses go into ONE combined palette strip; exact duplicates are merged and the strip is sorted dark to light. Swatches shrink to fit, down to 6 px: the strip holds at most (canvas height - 10) / 6 colours, 113 on the 690 px Mona Lisa canvas. The 2x2 Mona Lisa uses 70 colours in 9 px swatches. The locator matches this strip as usual.
- **Order and simulation.** Layers go cell by cell in `--order`, then the dividers (Pencil, divider colour, full length), then the frame. The whole grid is simulated (`sim_canvas.png`, `preview.png`).
- **Plan files.** `emit` writes one plan when the estimate is at most `--seconds` (480, recorded profile), else one per cell; the dividers and frame go with the last.

## JOB/cells.json (for the video edit)

- `canvas_origin_screen` and `scale`: where the canvas was when emitting (re-run `emit` after `locate` to refresh).
- `plans`: plan files with step counts and estimates.
- `cells[]`, in paint order:
  - `index`, `style`;
  - `rect_drawing_px`, `rect_canvas_px`, `rect_screen_px` (x0, y0, x1, y1);
  - `paint_order`;
  - `segments`: one entry per plan file the cell occupies, with `plan`, `steps` (0-based first and last step index in that file), `est_start_s` and `est_end_s` from the batch start.
- `finish`: the same for the dividers and frame.

Times are estimates from the calibrated time model (about 7 % on recent runs). Add about 3 s of call latency at the start; the batch summary gives the real total.

## Recipe: the split face (half Leonardo, half Warhol)

The hook: the vertical divider runs down the middle of the face, so the top-left master and the top-right pop-art each get HALF of it. The horizontal divider runs just under the chin. Bottom-left pointillism gets the left hand and sleeve, bottom-right cubism the right hand and the dress.

```bash
python -m paint_artist prepare --subject mona_lisa --grid 2x2 --styles master,pop-art,pointillism,cubism \
       --split-x 0.45 --split-y 0.37 --job "$J" --cell-override "$(cat ../assets/subjects/mona_grid_split_face.json)"
```

- **Where to cut:** find the line on the source, not from the face box. The Mona Lisa's face is turned, so the line between the eyes, through the philtrum and the mouth, is at x 0.45, while the face box centre is 0.47. The chin ends at y 0.355, so the horizontal divider is at 0.37. Check by drawing candidate lines on `assets/subjects/mona_lisa.jpg` before planning.
- **Cell overrides** (`assets/subjects/mona_grid_split_face.json`):
  - Pop-art adds fine black face lines (Pencil 3, 6 luminance levels, face only), so its half reads clearly as a face: eye, half mouth, hair outline.
  - Pointillism, for a small cell: a pale ground, dots 9, 6 and 4 px every 7, 5 and 4 px, saturation 1.5, gamma 0.8.
  - Cubism: a light sand, ochre, grey and slate palette without near-black, gamma 0.5, contrast 1.25, facets graded 18 L apart. It reads lighter, with strong per-facet contrast, instead of a murky brown.

Planned 2026-10-24 as ONE plan `pa_grid_mona.json`, 1,728 steps, 14,531 strokes, 262 picks, estimated 324 s with the old time model. Painted live (recorded) it took 593 s; the recorded timing profile now predicts 587 s, so `emit` splits it into `pa_grid_mona_cell0..3.json` (116 / 37 / 348 / 87 s). The pointillism cell's 9,196 dots cost 345 s by themselves. Old-model estimates per cell:

| Cell | Style | Canvas rect (px) | Strokes | Est. start - end |
|---|---|---|---|---|
| 0 top left | master (left half of the face) | 60, 9 - 262.5, 257.6 | 2,664 | 0 - 105 s |
| 1 top right | pop-art (right half of the face) | 262.5, 9 - 510, 257.6 | 667 | 105 - 128 s |
| 2 bottom left | pointillism (left hand, sleeve) | 60, 257.6 - 262.5, 681 | 9,196 | 128 - 273 s |
| 3 bottom right | cubism (right hand, dress) | 262.5, 257.6 - 510, 681 | 1,985 | 273 - 321 s |
| dividers + frame | | | 19 | 321 - 324 s |

## The uniform 2x2 Mona Lisa (planned 2026-10-24, before the split-face recipe)

| Cell | Style | Strokes in the cell | Est. start - end |
|---|---|---|---|
| 0 top left | master | 5,038 | 0 - 162 s |
| 1 top right | pop-art | 845 | 162 - 188 s |
| 2 bottom left | pointillism (cell override: pale ground, dots 9 / 6 / 4 px every 7 / 5 / 4 px, saturation 1.5, gamma 0.8) | 8,060 | 188 - 314 s |
| 3 bottom right | cubism | 926 | 314 - 341 s |
| dividers + frame | | 15 | 341 - 344 s |

Total 14,888 strokes, 1,840 steps, 285 colour picks, about 344 s in ONE plan (`pa_grid_mona.json`).

## Boxes: each part as its own painting (zoomed in, ultra detailed when assembled)

Instead of one canvas with cells, `--boxes RxC` paints every part as a FULL painting on its own standard canvas (540x690, drawing area 450x672, the same screen position for every box), then `assemble` tiles the saved boxes into one big picture. A 2x2 Mona Lisa from the bundled 900x1344 source is painted at 1:1 per box, so assembled at 900x1344 it is four times as detailed as a single run.

- Each box is prepared from its quarter of the high-resolution source, plus `--bleed` (8) source px of the neighbouring area on every interior side, resized to the drawing area. The planner paints past the box edge, so the tile edges are fully painted and seamless. No frame and no dividers on the boxes.
- Each box is planned like a normal job, at the corrected time cap (480 s per box, recorded profile). Detail is lowered only where needed (`detail` in `boxes.json`).
- `emit` writes one plan per box (`pa_box_<style>.json`), a canvas copy per box to open in Paint (`JOB/pa_box_<style>.png`), and updates `JOB/boxes.json`. That file holds, per box: style, sub-job, plan file and path, canvas file and path, tile rectangle in drawing px, batch steps, estimates and canvas origin.
- `assemble --job JOB` reads the four SAVED canvases (`JOB/pa_box_<style>.png`, or `--file INDEX=path`). It crops each drawing area, removes the bleed, resizes each tile to the exact box size, tiles them and draws 5 px dark dividers and the frame, writing `assembled.png` and `assembled_nodividers.png`. `assemble --sim` does the same from the simulations (`*_sim.png`); `plan` writes those automatically.

```bash
cd "SKILL_DIR/scripts"; J=$(cygpath -m "$HOME/paint-jobs/boxes_mona")
python -m paint_artist prepare --subject mona_lisa --boxes 2x2 --styles master,pop-art,pointillism,cubism --job "$J" \
       --cell-override "$(cat ../assets/subjects/mona_boxes.json)"
python -m paint_artist plan --job "$J"            # plans the 4 boxes + assembled_sim.png
# open the 4 canvases in Paint, pre-flight, then locate ONCE on the first one (all boxes share the position):
python -m paint_artist locate --job "$J/box0_master" --take --write-ui && cp "$J/box0_master/ui.json" "$J/ui.json"
python -m paint_artist emit --job "$J" --name pa_box  # 4 plans, boxes.json (copies JOB/ui.json into every box)
# for each box in order: bring its Paint window to the front (title pa_box_<style>.png - Paint), batch call, save (Ctrl+S)
python -m paint_artist assemble --job "$J"        # assembled.png + assembled_nodividers.png
```

The 2x2 Mona Lisa boxes (planned 2026-10-24, recorded profile; box 2 pointillism and box 3 cubism use the cell overrides in `assets/subjects/mona_boxes.json`):

| Box | Style | Strokes | Steps | Detail | Estimate |
|---|---|---|---|---|---|
| 0 | master | 12,529 | 1683 | 1.00 | 410 s (unrecorded about 331 s) |
| 1 | pop-art | 1,229 | 89 | 1.00 | 73 s (unrecorded about 50 s) |
| 2 | pointillism | 12,229 | 251 | 0.52 | 458 s (unrecorded about 186 s) |
| 3 | cubism | 3,818 | 271 | 1.00 | 145 s (unrecorded about 82 s) |

Total about 1086 s in 4 calls (recorded). Preview: `JOB/assembled_sim.png`.
