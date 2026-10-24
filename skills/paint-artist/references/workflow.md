# Workflow: commands, job folder, options

All commands: `cd SKILL_DIR/scripts && python -m paint_artist <command> ...` (Python 3.10+, numpy, scipy, Pillow; ffmpeg on PATH for `--take`). `python -m paint_artist -h` lists everything. Stdout is JSON only (hints go to stderr). Paths may be Windows (`C:/...`) or Git Bash (`/c/...`) style; in Bash build job paths with `cygpath -m` so other tools see Windows paths too.

## Job folder

| File | Written by | What it is |
|---|---|---|
| `source.*` | prepare | copy of the source image |
| `target_raw.png` | prepare | source fitted to the drawing size (the honest scoring reference) |
| `target.png` | prepare | target after the style prefilter (saturation, contrast, vignette, paper fade); what the planner aims at |
| `fade.png` | prepare | paper mask when the style fades into bare paper |
| `canvas.png` | prepare | the image to open in Paint: white, palette strip at x 10..40, drawing area at (60, 9) |
| `meta.json` | prepare | size, layout (canvas, draw origin, strip, swatch height), palette, frame colour indices, focus, face box |
| `preset.json` | prepare | resolved copy of the style preset (edit it, then re-run `plan`) |
| `ui.json` | locate --write-ui | measured canvas origin and DPI scale on top of `ui.default.json` |
| `tools.json` | calib-measure | measured tool darkness (optional; default `paint_tools.json`) |
| `plan.json` | plan | the app-agnostic plan: layers of strokes in drawing coordinates, sim score, stats |
| `sim.png`, `sim_canvas.png`, `preview.png` | plan | simulated drawing area, full simulated canvas, side-by-side preview |
| `emit.json` | emit | the emit summary (also printed): plan file path, step counts by kind, strokes, picks, tool switches, canvas origin used, bytes, est_seconds |
| `grab_locate.png`, `grab_score.png` | locate, score --take | screen grabs |
| `live.png`, `live_canvas.png`, `compare.png`, `score.json` | score | live drawing area; the canvas without the palette strip, frame included (gallery crop); target / sim / live strip; the numbers |

## Commands

| Command | Use |
|---|---|
| `compose SCENE --out ref.png [--width --height]` | Fresh composition (built-in `landscape`, `still_life`, `portrait`, or a scene JSON). See [style-transfer.md](style-transfer.md). |
| `analyse REF --out style.json [--base STYLE]` | Measure a reference painting, pick a base style, tune it. See [style-transfer.md](style-transfer.md). |
| `prepare SRC --job JOB --style STYLE` | `--height` (default 672), `--width` (default from aspect), `--fit crop|stretch`, `--focus cx,cy,rx,ry` (repeatable, fractions; the first is the face: finest detail, glaze protection, score box), `--face-box x0,y0,x1,y1`, `--reference REF [--transfer]`, `--no-frame`. |
| `plan --job JOB` | `--detail` (1.0; lower = fewer strokes), `--budget N` strokes, `--seconds S` (default 480 with the timing profile; 0 = no cap), `--profile recorded|unrecorded`, `--seed`. Retries with less detail until strokes, time and the 4900-step margin fit. Prints `sim_vs_target` (simulation vs the style-filtered target). |
| `preview --job JOB [--ui]` | Estimate and preview without writing a Melaya plan. |
| `emit --job JOB --name NAME [--ui] [--plans DIR]` | Writes `~/.melaya/plans/NAME.json` (or DIR) and prints the call to make. |
| `locate --job JOB --take|--grab G [--write-ui]` | Finds the canvas on screen, prints origin, scale, swatch error; writes `JOB/ui.json`. |
| `score --job JOB --file SAVED.png|--take|--grab G [--vs raw|target]` | `live_vs_sim` (execution fidelity) and live / sim vs the source (`raw`, default) or the filtered target. `--file` scores the saved canvas (exact pixels, preferred); grabs show Paint's resize-handle dots. |
| `calib-plan --job CJ --name N` / `calib-measure --job CJ --take` | Tool darkness calibration. See [calibration.md](calibration.md). |
| `prepare ... --grid RxC --styles a,b,... [--split-x] [--split-y] [--order] [--divider-width] [--inset] [--cell-override]` | Grid composite job; `plan` then writes the combined `canvas.png`, `emit` writes `cells.json`. See [grid.md](grid.md). |
| `prepare --boxes RxC --styles a,b,... [--bleed 8] [--cell-override]`, `plan`, `emit`, `assemble --job JOB [--sim] [--file I=png]` | Boxes: each part as its own full painting, then tiled. See [grid.md](grid.md). |
| `speed-calib --job CJ`, `speed-measure --job CJ --take --times t0,..,t4 [--install]` | Fastest safe pointer settings per tool and the Fill tool's connectivity. See [calibration.md](calibration.md). |
| `make SRC --job JOB --style STYLE --name NAME` | prepare + plan + emit (run `locate` before trusting the origin). |
| `contact JOB... --out sheet.png [--cols --tile --drawing]` | Contact sheet of simulations. |

## Opening the canvas in Paint

On the painting computer (normally the same machine as Claude Code), copy `canvas.png` to a name the user will recognise, for example `C:\Users\<user>\Pictures\<name>_live.png`, and open it: PowerShell `Start-Process mspaint -ArgumentList '"C:\...\<name>_live.png"'`. The window title becomes `<name>_live.png - Paint`, which is how you find it in `melaya_computer_list_windows`. Save right after the run returns: check the window TITLE with `melaya_computer_current_app` (a window id survives File > New), then `melaya_computer_press` `Ctrl+S`. In the live runs Ctrl+S saved at once, with no approval prompt. If the title changed, someone else is using Paint: send no keys, stop and report. Then `score --file` the saved image.

## Time model

Two timing profiles in `ui.default.json` (`timing_profiles`); `--profile` on plan / preview / emit picks one.

| Profile | Fitted on | Long stroke | Short stroke or dot (< 4 px) | Colour pick | Ink (stepPx 16) | Fill click |
|---|---|---|---|---|---|---|
| `recorded` (default) | recorded runs: the split-face grid (593 s) and the 17,386-stroke master run (512 s), max error 11 % | 0.016 s | 0.036 s | 0.28 s | 0.55 s / 1000 px | 0.10 s (placeholder) |
| `unrecorded` | 9 unrecorded live runs, max error 17 % | 0.012 s + 0.0011 s per point | same | 0.33 s | 0.13 s / 1000 px | 0.10 s |

A screen recorder (ffmpeg gdigrab at 30 fps) slows Paint, dots most. The grid estimate with the old model was 324 s and the run took 593 s; the recorded profile predicts 587 s. Every wait step is added. `plan` lowers detail until the estimate is under `--seconds` (480 by default) and refuses if it cannot. `emit` refuses a single plan above the cap (`--force` overrides), and a grid splits into one plan per cell instead. Add about 3 s of call latency per batch call.

Simulated numbers for the bundled Mona Lisa (`--subject mona_lisa`, 450x672, frame on):

| Style | Strokes | Steps | Picks | Est. time (recorded profile) |
|---|---|---|---|---|
| master | 15,499 | 1,670 | 267 | 476 s |
| impressionist | 16,790 | 797 | 122 | 428 s |
| van-gogh | 14,441 | 654 | 98 | 280 s |
| pointillism | 12,468 | 340 | 46 | 473 s |
| watercolour | 5,591 | 491 | 77 | 118 s |
| pencil-sketch | 1,907 | 49 | 5 | 140 s |
| ukiyo-e | 1,032 | 236 | 36 | 95 s |
| pop-art | 1,406 | 113 | 15 | 92 s |
| chiaroscuro | 7,193 | 946 | 151 | 247 s |
| cubism | 4,851 | 324 | 43 | 211 s |
| fauvism | 3,960 | 248 | 37 | 128 s |
| expressionism | 9,723 | 307 | 43 | 448 s |
| klimt | 11,959 | 397 | 52 | 294 s |
| stained-glass | 1,957 | 195 | 28 | 114 s |
| mondrian | 273 | 134 | 19 | 37 s |
| pixel-art | 1,080 | 223 | 35 | 104 s |
| sumi-e | 590 | 146 | 21 | 23 s |

Grid composite, split face (`--grid 2x2 --styles master,pop-art,pointillism,cubism --split-x 0.45 --split-y 0.37` with the bundled cell overrides, [grid.md](grid.md)): 14,531 strokes, 1,728 steps, 262 picks, about 324 s in one plan.

## Deliverables

Report: the style and mode, canvas size, strokes, colour picks, batch steps, the real duration (from the batch summary), Lab dE live vs target (all / face / rest) and sim vs target, and attach `compare.png` (or `live.png`). If a recording was made, its path and the stopwatch caveat in [recording.md](recording.md).

Boxes, 2x2 Mona Lisa (recorded profile): master 410 s, pop-art 73 s, pointillism 458 s, cubism 145 s; one batch call each.
