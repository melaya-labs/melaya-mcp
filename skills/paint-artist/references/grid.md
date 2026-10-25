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

```bash
cd "SKILL_DIR/scripts"; J=$(cygpath -m "$HOME/paint-jobs/boxes_ermine")
python -m paint_artist prepare SRC.jpg --boxes 2x2 --styles master,pop-art,pixel-art,stained-glass --job "$J" --name ermine \
       [--crop 509,120,1781,2020] [--split-at 1145,1070] [--focus 0.48,0.30,0.16,0.12 ...] [--cell-override overrides.json]
python -m paint_artist plan --job "$J" [--seconds 480] [--box-detail 1.2,,,] [--box-seconds 400,0,0,0] [--only 0]
# open the 4 canvases in Paint, pre-flight, then locate ONCE on the first one (all boxes share the position):
python -m paint_artist locate --job "$J/box0_master" --take --write-ui && cp "$J/box0_master/ui.json" "$J/ui.json"
python -m paint_artist emit --job "$J" --name ermine --title "Lady with an Ermine" --artist "Leonardo da Vinci" \
       --year "c. 1489-1491" --source-url "https://..." --labels "Leonardo,Pop art,Pixel art,Stained glass"
# per box, in order: bring "pa_ermine_<style>.png - Paint" to the front, one batch call with plan pa_ermine_<style>.json, Ctrl+S
python -m paint_artist assemble --job "$J"        # assembled.png + assembled_nodividers.png
```

**Names.** `--name ermine` (on `prepare`, or later on `emit`, which wins) names every file `pa_ermine_<style>`: plans `~/.melaya/plans/pa_ermine_<style>.json`, canvases `JOB/pa_ermine_<style>.png`, Paint titles `pa_ermine_<style>.png - Paint`. A style used twice gets the box index: `pa_ermine_master_0`, `pa_ermine_master_2`. A leading `pa_` in the name is dropped (`--name pa_ermine` is the same). Without a name the prefix is `box` (`pa_box_<style>`). Give every painting its own name: all plans live in ONE folder, so two paintings with the same names overwrite each other's plans.

**Source window: crop, fit, split.** The boxes paint one window of the source with the assembled aspect (C*450 : R*672, so 450:672 for 2x2):

- `--crop x0,y0,x1,y1` (source px) uses only that region of the source.
- `--fit crop` (default) takes the largest window of that aspect inside the region, centred. `--fit stretch` uses the whole region, stretched.
- `--split-at x,y` (source px; either may be empty, e.g. `--split-at 1145,`) places that source point EXACTLY on the middle vertical and/or horizontal divider: the face centre on the split, the hook of a split-face painting. The window shrinks as needed, and `prepare` prints `split_at_window_frac` (0.5, 0.5 for 2x2) to confirm. Find the point on the source: between the eyes and through the mouth for the vertical split, just under the chin for the horizontal one.
- `boxes.json` records `window_src_px`, `crop_src_px` and `split_at_src_px`. The source keeps its full resolution: each box is cut from it and resized to its 450x672 drawing area.

**Focus.** `--focus cx,cy,rx,ry` is in fractions of the window (the assembled picture), as in the single mode; the bundled subject's focus is converted from the whole image. Every focus ellipse goes into EVERY box it overlaps, in box coordinates, so ONE face ellipse centred on the split gives both halves of the face the finest detail. The first focus in a box is that box's face (finest detail, glaze protection, score box, clamped to the box).

**Bleed.** Each box gets `--bleed` (8) drawing px of the neighbouring area on every interior side. The planner paints past the box edge, so the tile edges are fully painted and seamless. No frame and no dividers on the boxes.

**Per-box detail and time cap.** Each box is planned like a normal job, capped at `--seconds` (480 s, recorded profile). A plan over the cap triggers a detail search that lands just under it (94-100 % of the cap, a few plans), never above the box's detail. The stroke seed grid follows detail continuously, so the time follows it smoothly too. Per box, in priority order:

- `--box-detail 1.2,,,` and `--box-seconds 400,0,0,0` on `plan`, in box order; empty or 0 = the global `--detail` / `--seconds`.
- `"plan": {"detail": 1.2, "seconds": 400}` inside that box's entry of the overrides file (`--cell-override`, inline JSON or a file path; the other keys are merged into the box's style).
- `plan --only 0,2` re-plans only those boxes; the others keep their plans and the assembled preview is rebuilt.

**Coverage guard (cells styles).** After a `cells` layer (pixel art, stained glass, Mondrian), the simulation must leave no bare canvas pixel where the cell colour is not white. Any such pixel (a gap between fill lines, a missed bucket fill, a skipped tiny region) gets 1 px Pencil runs (`<layer>-cover`); `plan` prints `uncovered_px` (0 after the guard) and `cover_patch_px` (pixels it had to patch). The rectangle fill keeps its line pitch at least 1.2 px under the line width, overlap included, so neighbouring lines still overlap once rounded (before the fix it left 1 px white rows). Live pixel-art boxes fill their cells grouped by colour, dark to light, so the lightest cells stay white until the last seconds of the box: that is the run in progress, not a defect, and the saved canvas matches the simulation.

**emit** writes one plan per box, a canvas copy per box (never over a saved one; `--recopy` forces it), `JOB/boxes.json` (per box: style, sub-job, plan and canvas file and path, window title, tile rectangle in drawing px, focus, batch steps, strokes, detail, estimates, canvas origin) and `JOB/job_card.json`. It prints, for each box in order, the canvas to open, the window title and the plan to call.

**assemble --job JOB** reads the SAVED canvases (`JOB/<canvas_file>`, or `--file INDEX=path`). It crops each drawing area, removes the bleed, resizes each tile to the exact box size, tiles them and draws 5 px dark dividers and the frame, writing `assembled.png` and `assembled_nodividers.png`. `assemble --sim` does the same from the simulations (`*_sim.png`); `plan` writes those automatically.

### JOB/job_card.json (written by emit)

One canonical card per boxes job, read by the video script and the batch tooling. Values not passed to `emit` are kept from the previous card (older hand-written cards included), so re-emitting after `locate` keeps the title and labels.

| Key | Value |
|---|---|
| `version` | 1 |
| `slug` | the name prefix (`ermine`) |
| `title`, `artist`, `year`, `source_url` | from `emit --title --artist --year --source-url` |
| `mode`, `rows`, `cols` | `"boxes 2x2"`, 2, 2 |
| `source`, `window_src_px` | the source file and the painted window (source px) |
| `boxes[]` | `{index, row, col, style, label, plan_file, canvas_file, window_title, est_seconds, est_seconds_unrecorded, strokes, steps, detail}` in box (reading) order. `label` comes from `--labels` (comma separated, box order), else the previous card, else the style (`master` = the artist) |
| `est_total_seconds`, `est_total_seconds_unrecorded` | sums over the boxes |
| `total_strokes`, `total_steps` | sums over the boxes |
| `timing_profile`, `canvas_origin`, `plans_dir` | as emitted |
| `preview`, `preview_nodividers` | `JOB/assembled_sim.png`, `JOB/assembled_nodividers_sim.png` |
| `notes` | kept from the previous card (free text: crop, hook, overrides, rejected variants) |

### Batch of paintings

Many paintings, one live Paint at a time. Everything except the live run can happen in parallel.

1. **Prepare in parallel**, one job folder and one `--name` per painting (`~/paint-jobs/boxes_<slug>`, `--name <slug>`): source, `--crop` / `--split-at`, `prepare`, `plan`, `emit --title ... --labels ...`. Check each `assembled_sim.png` and adjust the overrides before going live. Several agents can do this at once: unique names mean no plan overwrites another.
2. **One live runner at a time.** A single agent owns the screen, because Paint, the mouse and the keyboard are one resource. It paints the paintings one after another, the boxes of each in order: one `melaya_computer_batch` per box, the right window title in front, Ctrl+S right after each box.
3. **Per painting: its own recorder and stopwatch.** Start a fresh recording and stopwatch before the first box of each painting and stop them after its last save ([recording.md](recording.md)), so each painting has its own `raw/<slug>_recording.mp4`. The stopwatch also counts the switching and saving between boxes (10-13 min against 4.5-8.5 min of batch time in the 2026-10-24 batch); the batch summaries hold the real painting times.
4. **Assemble between paintings.** Run `assemble --job JOB` after the last save. Keep one `runs.json` entry per painting: live seconds per box (from the batch summaries), strokes, estimates and any issue.

The 2026-10-24 batch: 10 paintings, 4 boxes each, every box in ONE call; 4,444 s of painting and 165,824 strokes in total. Live runs took 65-75 % of the recorded-profile estimates for most paintings (57-77 % across all ten).

### The 2x2 Mona Lisa boxes

```bash
python -m paint_artist prepare --subject mona_lisa --boxes 2x2 --styles master,pop-art,pointillism,cubism --job "$J" \
       --name mona --cell-override ../assets/subjects/mona_boxes.json
```

Planned 2026-10-24 with the recorded profile. Box 2 (pointillism) and box 3 (cubism) use the cell overrides in `assets/subjects/mona_boxes.json`:

| Box | Style | Strokes | Steps | Detail | Estimate |
|---|---|---|---|---|---|
| 0 | master | 12,529 | 1683 | 1.00 | 410 s (unrecorded about 331 s) |
| 1 | pop-art | 1,229 | 89 | 1.00 | 73 s (unrecorded about 50 s) |
| 2 | pointillism | 12,229 | 251 | 0.52 | 458 s (unrecorded about 186 s) |
| 3 | cubism | 3,818 | 271 | 1.00 | 145 s (unrecorded about 82 s) |

Total about 1086 s in 4 calls (recorded). Preview: `JOB/assembled_sim.png`.
