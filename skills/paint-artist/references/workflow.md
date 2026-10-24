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
| `plan --job JOB` | `--detail` (1.0; lower = fewer strokes), `--budget N` strokes, `--seconds S` (default 500; 0 = no cap), `--seed`. Retries with less detail until strokes, time and the 4900-step margin fit. Prints `sim_vs_target` (simulation vs the style-filtered target). |
| `preview --job JOB [--ui]` | Estimate and preview without writing a Melaya plan. |
| `emit --job JOB --name NAME [--ui] [--plans DIR]` | Writes `~/.melaya/plans/NAME.json` (or DIR) and prints the call to make. |
| `locate --job JOB --take|--grab G [--write-ui]` | Finds the canvas on screen, prints origin, scale, swatch error; writes `JOB/ui.json`. |
| `score --job JOB --file SAVED.png|--take|--grab G [--vs raw|target]` | `live_vs_sim` (execution fidelity) and live / sim vs the source (`raw`, default) or the filtered target. `--file` scores the saved canvas (exact pixels, preferred); grabs show Paint's resize-handle dots. |
| `calib-plan --job CJ --name N` / `calib-measure --job CJ --take` | Tool darkness calibration. See [calibration.md](calibration.md). |
| `make SRC --job JOB --style STYLE --name NAME` | prepare + plan + emit (run `locate` before trusting the origin). |
| `contact JOB... --out sheet.png [--cols --tile --drawing]` | Contact sheet of simulations. |

## Opening the canvas in Paint

On the painting computer (normally the same machine as Claude Code), copy `canvas.png` to a name the user will recognise, for example `C:\Users\<user>\Pictures\<name>_live.png`, and open it: PowerShell `Start-Process mspaint -ArgumentList '"C:\...\<name>_live.png"'`. The window title becomes `<name>_live.png - Paint`, which is how you find it in `melaya_computer_list_windows`. Save right after the run returns: check the window TITLE with `melaya_computer_current_app` (a window id survives File > New), then `melaya_computer_press` `Ctrl+S`. In the live runs Ctrl+S saved at once, with no approval prompt. If the title changed, someone else is using Paint: send no keys, stop and report. Then `score --file` the saved image.

## Time model

Fitted on nine live Mona Lisa runs (2026-10-24, tool-reported seconds; mean error 5 %, worst 17 %, the estimates for those plans within 7 %):

`0.0119 s x strokes + 0.0011 s x points + 0.334 s x colour picks + 0.131 s per 1000 px of ink at stepPx > 4 + every wait step`

(`timing_model` in `ui.default.json`; a job's `ui.json` only overrides the canvas position.) Pencil and fill-heavy plans are about a third faster than the old one-run model said. The 17,386-stroke reference run took 17 % longer than this predicts (an older runner), so `plan` caps the estimate at 500 s by default to stay inside the batch's 10 minutes. Add about 3 s of MCP latency before the first step and the time to collect with `run_id`.

Simulated numbers for the bundled Mona Lisa (`--subject mona_lisa`, 450x672, frame on):

| Style | Strokes | Steps | Picks | Est. time |
|---|---|---|---|---|
| master | 18,056 | 1,701 | 271 | 429 s |
| impressionist | 16,849 | 799 | 122 | 316 s |
| van-gogh | 14,649 | 655 | 98 | 378 s |
| pointillism | 30,487 | 463 | 52 | 454 s |
| watercolour | 5,564 | 491 | 77 | 120 s |
| pencil-sketch | 1,911 | 49 | 5 | 55 s |
| ukiyo-e | 2,819 | 415 | 57 | 93 s |
| pop-art | 2,667 | 172 | 22 | 73 s |
| chiaroscuro | 7,312 | 946 | 151 | 195 s |
| cubism | 4,851 | 324 | 43 | 110 s |
| fauvism | 4,005 | 250 | 37 | 85 s |
| expressionism | 11,623 | 309 | 42 | 377 s |
| klimt | 12,050 | 398 | 52 | 211 s |
| stained-glass | 3,073 | 316 | 43 | 80 s |
| mondrian | 1,264 | 91 | 12 | 32 s |
| pixel-art | 3,913 | 134 | 19 | 75 s |
| sumi-e | 575 | 146 | 21 | 20 s |

## Deliverables

Report: the style and mode, canvas size, strokes, colour picks, batch steps, the real duration (from the batch summary), Lab dE live vs target (all / face / rest) and sim vs target, and attach `compare.png` (or `live.png`). If a recording was made, its path and the stopwatch caveat in [recording.md](recording.md).
