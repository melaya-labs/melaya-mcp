# The one-call contract (Melaya Computer Control)

## The call

1. `emit` writes the plan to `~/.melaya/plans/<name>.json` on the user's computer (the runner or desktop app reads that folder).
2. Call `melaya_computer_batch` with `steps: []` and `plan: {"file": "<name>.json"}`. Equivalent sources: `{"id": "pl_..."}` after `melaya_computer_plan` `action: "save"`, `source: {"file": "<name>.json"}`, `kind: "batch"` (reusable for 7 days), or `{"url": "https://..."}` (JSON, at most 2 MB).
3. Do NOT pass `window_id`: Paint's Brushes dropdown is a separate popup window, and a pinned window makes the tool-switch clicks miss it. The batch acts in the focused allowed window, which the pre-flight made the right Paint.
4. Never inline a large plan in the call: writing thousands of steps into the call is slow to start (the user complained). The stored plan starts at once.
5. Long runs return `{"status": "running", "run_id": "cr_..."}` after about 50 s. Call `melaya_computer_batch` again with `steps: []` and `run_id` (nothing else); each collect call waits about 50 s. Repeat until the result is the summary (step counts by kind, first failure if any, final pointer, observed change, a screenshot).

## Limits

| Limit | Value | What the skill does |
|---|---|---|
| Steps per batch | 5000 | `plan` keeps a 4900-step margin |
| Run time | up to 10 minutes | `plan --seconds 500` default (margin for the time model) |
| Stored plan size | 2 MB (id / url) | the Mona Lisa plan is about 0.95 MB |
| Strokes per path step | 200 worked well | the emitter chunks at 200 |

## Step schema (what the emitter writes)

Plan file: `{"surface": "computer", "kind": "batch", "steps": [...]}`.

| Kind | Shape | Used for |
|---|---|---|
| `set_value` | `{"target": {"label": "Size", "role": "slider"}, "value": "43", "onError": "continue"}` | Size and Opacity sliders |
| `click` | `{"target": {"x": 405, "y": 127}, "delivery": "foreground", "onError": "continue"}` | Brushes dropdown (foreground), its item, the Pencil button |
| `wait` | `{"ms": 450}` | after ribbon clicks |
| `mouse` | `{"target": {"x": 302, "y": 127}, "state": "down"}` then `"up"` | colour picker press, swatch press |
| `move` | `{"x": 715, "y": 527}` | travel to the swatch |
| `path` | `{"strokes": [[[x, y], ...], ...], "speed": 8000, "stepPx": 16, "strokeGapMs": 2}` | painting; camelCase keys only (`step_px` / `stroke_gap_ms` are rejected inside a batch) |

Values: `stepPx` 16 for Pencil and Brush, 4 for Oil brush and Watercolour (their texture needs dense events); `strokeGapMs` 2; `speed` 8000 (6000 for the ground serpentine, 4000 for frame lines). Every tool-switch click and slider set is `onError: "continue"`: the helper handles the first click after a ribbon click and very fast consecutive actions, and a missed size change must not abort a 9-minute run. A stroke has at least 2 distinct integer points (a dot is `[[x, y], [x + 1, y]]`).

A colour pick is 5 steps: mouse down/up on the colour picker (302, 127), move to the swatch centre, mouse down/up on the swatch. The picker returns to the previous tool by itself.

## Pause, resume, stop

- If the user moves the mouse or types, the run pauses, re-checks the window and resumes where it stopped (runner 1.1.75+). Tell the user before the call not to touch the computer.
- `melaya_computer_stop` halts everything (the user can also press Ctrl+Alt+End on Windows, Control+Command+Esc on a Mac, or stop from Melaya). A `stopped` result means do not retry; ask.
- If a run ended early, read the summary's first failure. Re-running the same plan repaints from the start over what is there (harmless for opaque layers, but darker for watercolour); for a clean retry, reopen the canvas. Runner 1.1.75 also accepts `resume_from` on batch (check the tool schema before relying on it).
