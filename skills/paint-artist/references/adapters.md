# Adapters: other apps and operating systems

The planner and simulator never know about Paint. The contract between them and an app adapter:

| Piece | Format | Owner |
|---|---|---|
| `plan.json` | `{W, H, palette: [[r,g,b] 0..1], layers: [{name, tool, width, opacity, strokes: [[k, [[x, y], ...]]], speed?, stepPx?}], sim_score, stats}` in drawing-area pixels (the frame layers may have negative coordinates: they live in the margins) | planner |
| tool model | `{tool: {alpha, aa, soft, bristles, opacity_setting, stepPx, measured}}` (`paint_tools.json`) | adapter (measured on the app) |
| layout | `meta.json` `layout`: canvas size, drawing origin, palette strip geometry | prepare (shared) |
| UI map | `ui.json`: where the tools, colour source and sliders are, waits, timing model | adapter |

`emit_paint.py` is the Paint adapter: tool switch (Pencil button or Brushes popup), opacity and size sliders, colour by eyedropper from the strip, `path` steps, clamping away from the strip and the canvas edges.

## Writing another adapter (not built)

For any app driven through Melaya Computer Control (`melaya_computer_batch` works on Windows, macOS and Linux, including a headless Linux VM through the runner with `--computer`), an adapter needs:

1. **Tool selection**: a click sequence per tool name the presets use (`brush`, `oil`, `watercolour`, `pencil`), or a mapping to the closest tools the app has. Measure each tool's alpha and texture with the calibration recipe and write a tool model.
2. **Colour input**: the most reliable path is the same palette strip in the canvas plus the app's eyedropper (Krita `P`, GIMP `O`, Pinta's color picker, macOS Preview has none). A hex field typed per colour also works where the app has one (Krita, GIMP, Photopea in a browser) but costs more steps; never rely on a modal dialog that can hang.
3. **Size and opacity**: a slider or field per tool, and the px mapping (verify by painting a test stroke).
4. **Canvas geometry**: zoom 100 %, canvas origin from `locate` (works on any grab), forbidden zones (resize handles, rulers, the strip).
5. **Screen grab for scoring**: macOS `screencapture -x grab.png`, Linux X11 `import -window root grab.png` or `ffmpeg -f x11grab -i :0.0 -frames:v 1 grab.png`, Wayland `grim grab.png`; then `score --grab grab.png`.
6. **Timing model**: fit `per_stroke_s` on one real run.
7. Emit the same Melaya step kinds (`click`, `wait`, `mouse`, `move`, `set_value`, `press` for shortcuts, `path` with camelCase keys) and keep the one-call stored-plan rule.

Candidates: Krita (Windows, macOS, Linux; real brush engines, eyedropper `P`), GIMP, Pinta (Linux), Paintbrush or Pixelmator (macOS), Photopea or Excalidraw in a browser window.
