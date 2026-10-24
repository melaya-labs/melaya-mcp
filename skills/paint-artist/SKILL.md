---
name: paint-artist
description: Paint or draw a picture in Microsoft Paint (Windows 11) through Melaya Computer Control in ONE melaya_computer_batch call driven by a stored plan. Use when asked to paint or draw something in Paint, to reproduce an image or a painting stroke by stroke, to paint a subject in the style of a painter or of a reference painting (impressionist, Van Gogh, pointillism, watercolour, pencil sketch, ukiyo-e, pop art, chiaroscuro, cubism, fauvism, expressionism, Klimt, stained glass, Mondrian, pixel art, sumi-e), to compose and paint a new scene, or for a computer-control art demo (with optional recording and stopwatch). Plans palette and painterly strokes in Python, simulates Paint's real tools, previews time and result, paints, then scores the live canvas against the simulation and the target. Bundled subject: the Mona Lisa.
version: 1.2.0
---

# Paint Artist

Plan a painting as strokes (app-agnostic), simulate it with Paint's measured tools, emit it as one stored Melaya batch plan, paint it in Paint in a single `melaya_computer_batch` call, then score the live canvas. Reference runs: Mona Lisa (master): 1786 steps, 17,386 strokes, 288 colour picks, 512 s, Lab dE 6.30 vs the original (face 5.36). Nine styles painted live on the Mona Lisa by an agent using only this file: live vs simulation dE 1.7 (mondrian) to 4.1 (pop-art) for flat and opaque styles; see [references/scoring.md](references/scoring.md).

`SKILL_DIR` = the folder of this file. Every command runs in `SKILL_DIR/scripts`: `python -m paint_artist <command>` (numpy, scipy, Pillow; ffmpeg for grabs). Load the `melaya` skill for Melaya rules (status first, never widen access, never approve for the user).

## Pick the mode

| The user wants | Mode | Start with |
|---|---|---|
| This PNG/JPG painted as faithfully as possible | 1. Reproduce 1:1 | `prepare SRC --style master` (+ `--focus` on the face) |
| Subject X painted like reference painting Y | 2. Style from a reference | `analyse Y --out style.json`, look at Y, fix the JSON, `prepare X --style style.json --reference Y --transfer` |
| Subject X "as Monet / Van Gogh / Seurat / Picasso / Matisse / Munch / Klimt / Mondrian / watercolour / sketch / woodblock / stained glass / pixel art / ink wash / pop art / old master" | 3. Named style | `prepare X --style <style>`; see [styles/](styles/) |
| One picture split into cells, each in another style (a style grid, e.g. half Leonardo half Warhol through the face) | 5. Grid composite | `prepare --subject mona_lisa --grid 2x2 --styles master,pop-art,pointillism,cubism [--split-x 0.45 --split-y 0.37]`, then plan, open `canvas.png` (written by plan), locate, emit, one batch call; see [references/grid.md](references/grid.md) |
| Each part painted as its own full painting, assembled into one ultra-detailed picture (zoomed boxes) | 6. Boxes | `prepare --subject mona_lisa --boxes 2x2 --styles ...`, plan, open the box canvases, locate once, emit, one batch call per box, save each, `assemble`; see [references/grid.md](references/grid.md) |
| A new picture with no source image | 4. Fresh composition | `compose landscape|still_life|portrait|scene.json --out ref.png`, then mode 1 or 3 |

Styles (17): [master](styles/master.md), [impressionist](styles/impressionist.md), [van-gogh](styles/van-gogh.md), [pointillism](styles/pointillism.md), [watercolour](styles/watercolour.md), [pencil-sketch](styles/pencil-sketch.md), [ukiyo-e](styles/ukiyo-e.md), [pop-art](styles/pop-art.md), [chiaroscuro](styles/chiaroscuro.md), [cubism](styles/cubism.md), [fauvism](styles/fauvism.md), [expressionism](styles/expressionism.md), [klimt](styles/klimt.md), [stained-glass](styles/stained-glass.md), [mondrian](styles/mondrian.md), [pixel-art](styles/pixel-art.md), [sumi-e](styles/sumi-e.md). All of them on the Mona Lisa: [assets/examples/contact_sheet.png](assets/examples/contact_sheet.png).

## Recipe: one style, live, in one call (copy exactly)

Bash (Git Bash on Windows). Replace `STYLE` with a style name from the list above. The bundled subject `mona_lisa` (`assets/subjects/`) brings its own size and focus ellipses; for your own image use `prepare SRC --focus cx,cy,rx,ry ...` instead. Every command prints JSON on stdout (hints go to stderr); paths may be Windows or Git Bash style.

```bash
cd "SKILL_DIR/scripts"
J=$(cygpath -m "$HOME/paint-jobs/mona_STYLE"); N="pa_mona_STYLE"
python -m paint_artist prepare --subject mona_lisa --style STYLE --job "$J"     # target, palette, canvas.png
python -m paint_artist plan --job "$J"            # plan + simulation; prints est_seconds and sim_vs_target
cp "$J/canvas.png" "$J/$N.png"
powershell -NoProfile -Command "Start-Process mspaint -ArgumentList '\"$(cygpath -w "$J/$N.png")\"'"
```

Then the pre-flight below, with the Melaya tools (the window title is `<N>.png - Paint`). Then:

```bash
python -m paint_artist locate --job "$J" --take --write-ui   # expect origin [690, 239], scale 1.0, swatch_err < 2.5
python -m paint_artist emit --job "$J" --name "$N"           # writes ~/.melaya/plans/<N>.json; summary also in $J/emit.json
```

1. **Paint:** `melaya_computer_batch` with `{"steps": [], "plan": {"file": "<N>.json"}}` and NO `window_id`. While the result is `{status: "running", run_id}`, call it again with `{"steps": [], "run_id": "<run_id>"}` until the summary arrives (it states the run's own duration).
2. **Save at once**, before anything else: `melaya_computer_current_app` must show the TITLE `<N>.png - Paint` (a window id survives File > New, so the id alone proves nothing). Then `melaya_computer_press` with `keys: "Ctrl+S"` (it saves without a prompt). If the title is different, someone else is using Paint: do not press anything in that window (no Ctrl+Z or other "recovery" keys), stop and report.
3. **Score:**

```bash
python -m paint_artist score --job "$J" --file "$J/$N.png"   # from the saved file: exact pixels (preferred)
# or, if it could not be saved: python -m paint_artist score --job "$J" --take   (screen grab; Paint must still be in front)
```

`score` writes `live.png` (drawing area), `live_canvas.png` (the canvas without the palette strip, frame included, 499x690 for the Mona Lisa: the gallery crop), `compare.png` (target | sim | live) and `score.json`. Screen-grab crops show Paint's small resize-handle dots on the canvas corners and edge midpoints; the saved file does not.

The three numbers, all mean Lab dE (CIE76) over the drawing area inset 16 px:

| Number | Where | Meaning |
|---|---|---|
| `sim_vs_target` | `plan` | simulation vs the STYLE-FILTERED target (`target.png`): how well the plan reaches its own stylised goal |
| `live_vs_sim` | `score` | live painting vs simulation: execution fidelity, the number to report for every style (2 to 5 = faithful; textured tools such as Watercolour score higher, about 8 to 11, because their streaks land in different places) |
| `live_vs_raw`, `sim_vs_raw` | `score` | live and simulation vs the UNFILTERED source: only meaningful for `master` (stylised versions are meant to differ) |

Report strokes, picks, batch steps, the run's duration from the batch summary, `live_vs_sim`, and show `compare.png`.

## The flow, step by step

1. **Prepare.** `prepare SRC|--subject NAME --job JOB --style STYLE [--height 672] [--focus cx,cy,rx,ry] [--no-frame]` writes `target.png`, the palette, `canvas.png` (white drawing area + palette strip at the left) and `meta.json`. Canvas height up to about 790 px fits Paint at 1920x1080.
2. **Plan.** `plan --job JOB [--detail 1.0] [--seconds 500] [--budget N]` plans and simulates every layer, retrying with less detail until it fits the time cap and the 5000-step batch limit. Writes `plan.json`, `sim.png`, `sim_canvas.png`, `preview.png`.
3. **Preview.** `preview --job JOB` prints strokes, picks, batch steps, the time estimate (about 34 strokes/s). Show `preview.png`. Preview-only requests stop here.
4. **Calibrate the position.** Open `canvas.png` in Paint (copy it to a recognisable name first), run the pre-flight, then `locate --job JOB --take --write-ui`. Other resolution, DPI or Paint version, or an unmeasured tool: [references/calibration.md](references/calibration.md).
5. **Paint in ONE call.** `emit --job JOB --name NAME`, then `melaya_computer_batch` with the stored plan as in the recipe. Details: [references/melaya-batch.md](references/melaya-batch.md).
6. **Save, score and deliver.** Verify the title and Ctrl+S right after the run, then `score --job JOB --file SAVED.png` (or `--take`): identical crops of live, simulation and target (16 px inset), Lab dE all / face / rest. [references/scoring.md](references/scoring.md).

Options: canvas size (`--height`, `--width`), detail (`--detail`, `--budget` strokes, `--seconds`), frame (`--no-frame`), recording and stopwatch ([references/recording.md](references/recording.md)), preview only (stop after step 3).

## Pre-flight (every run, in this order)

- [ ] `melaya_computer_status`: computer online, `running` false (no other task holds it), Paint allowed at Full control (sliders and drags need it). If the user is actively using the computer, wait and ask: never take the screen over them.
- [ ] The user agreed that the run takes over the mouse now. Tell them not to touch the mouse or keyboard until the painting is SAVED (a touch pauses the run, which re-checks the window and resumes); Ctrl+Alt+End stops it.
- [ ] Canvas opened in Paint; `melaya_computer_list_windows`: every OTHER Paint window minimised (a pause once sent strokes into another maximised Paint window).
- [ ] Target Paint window focused and maximised, zoom 100 % (status bar), in front: `melaya_computer_current_app` shows the title `<N>.png - Paint`.
- [ ] `melaya_computer_screenshot` (scope display): the canvas is fully visible with its palette strip, nothing over it. Then `locate --take --write-ui`: origin (690, 239 for a 540x690 canvas at 1920x1080), scale 1.0, `swatch_err` under 2.5. Emit AFTER this, so the plan uses the measured origin.
- [ ] `plan` estimate under 480 s (the `recorded` timing profile, default: recording slows Paint, dots most) and under 5000 steps; `emit` refuses a plan above the cap. Without a recorder, `--profile unrecorded`.
- [ ] New machine, Paint build or speed settings: run `speed-calib` once ([references/calibration.md](references/calibration.md)) to find the fastest safe pointer settings and the Fill tool's connectivity.
- [ ] Recording wanted: recorder and stopwatch started, start flag touched right before the call ([references/recording.md](references/recording.md)).

## Failure table

| Symptom | Cause | Fix |
|---|---|---|
| Brush strokes come out as Pencil, Brushes menu never opens | `window_id` passed: the Brushes dropdown is a separate popup window | Never pass `window_id` for Paint runs |
| Strokes land in another Paint window | Another Paint window was maximised and came forward after a pause | Minimise all other Paint windows, verify the front window, rerun |
| Canvas suddenly 541x1 or resized | A stroke started on a canvas edge resize handle (handles sit ON the edges) | Ctrl+Z restores; keep 5 px clear of edges (the emitter clamps) |
| Paint hangs | Edit Colours dialog opened | Never use it; colours come only from the palette strip + colour picker |
| Wrong colours everywhere | Swatches moved: zoom not 100 %, canvas scrolled, origin changed, or strip painted over | `locate` again, re-emit; strokes never cross canvas x < 44 |
| `path` step rejected | snake_case keys | Batch path steps use `stepPx`, `strokeGapMs`, `speed` |
| Call slow to start | Plan inlined in the call | Always `plan: {"file": ...}` (or `{id}` via `melaya_computer_plan save`, or `{url}`) |
| Result `{status: "running"}` | Long run | Collect with `steps: []` + `run_id`, repeat until the summary |
| Run stops near 10 min or refused | Over the batch limits | `plan --seconds 540` or lower `--detail`; worst case split into two plans |
| Run paused mid-way | User touched mouse or keyboard | It resumes by itself after re-checking the window; ask them to keep off |
| Live much lighter or darker than the sim | Tool darkness differs (other Paint build), or the tool is still `measured: false` in `paint_tools.json` | Calibration run ([references/calibration.md](references/calibration.md)), `calib-measure --install` |
| A tool switch or size change ignored | First click after a ribbon click, very fast actions | Already `onError: "continue"` + waits; raise `waits_ms` in `ui.json` |
| `not_allowed` / `tier_denied` | Paint not allowed, or below Full control | The user changes it on the Computer Control page |
| Score looks far worse than it should | Misaligned crop (whole source resized to the crop size) | Use `score`: identical crop of live and full-size target |
| `canvas not found on screen` | Paint no longer in front (the user took the screen back), or something covers the strip | Save right after the run and score with `--file`; never bring Paint forward over the user |
| Paint's title changed after the run (another document, `Untitled`) | Someone used File > New or opened another file in that window | Stop: send no keys to it (no Ctrl+Z), report; score from a grab only if one was taken before |
| Stopwatch never freezes in the video | Recorder hard-killed (last fragment lost) or stop flag touched late | `record.ps1` + stop flag right after the run returns |

## References

- [references/workflow.md](references/workflow.md): job folder, every command and option, time model, deliverables.
- [references/melaya-batch.md](references/melaya-batch.md): the one-call contract, step schema, limits, pause and resume.
- [references/paint-win11.md](references/paint-win11.md): Paint UI map, tools, sliders, palette strip, canvas handles.
- [references/calibration.md](references/calibration.md): re-deriving `ui.json` and the tool darkness on any screen.
- [references/planner.md](references/planner.md): the planner, layer types, masks, preset JSON schema.
- [references/style-transfer.md](references/style-transfer.md): modes 2 and 4 (analyse a reference, compose a scene).
- [references/scoring.md](references/scoring.md) and [references/recording.md](references/recording.md).
- [references/grid.md](references/grid.md): grid composites (several styles in one picture), `cells.json` for the video edit.
- [references/adapters.md](references/adapters.md): the app-agnostic plan and what a macOS or Linux adapter needs.
