# Scoring: the honest metric

```
python -m paint_artist score --job JOB --file SAVED.png   # preferred: the saved canvas, exact pixels
python -m paint_artist score --job JOB --take             # or a screen grab (Paint in front), or --grab grab.png
```

1. Right after the run returns, while Paint is still in front, grab the screen: `ffmpeg -f gdigrab -draw_mouse 0 -i desktop -frames:v 1 grab.png` (Windows; the option order matters: `-f` and `-draw_mouse` are input options and go before `-i`, `-frames:v` after; `-draw_mouse 0` keeps the cursor out of the painting).
2. Locate the canvas on the grab by matching the palette strip (never painted over; any display scale), with a fallback to the white canvas region, crop the drawing area at `origin + draw_origin x scale`, size W x H (resampled if the display scale is not 1).
3. Compare with the FULL-SIZE target cropped IDENTICALLY: both images are the W x H drawing area, then both are cut 16 px inside the edge (the frame's gold and dark lines sit at 14 and 17 px, so the dark line is inside the scored area, as it was in the reference run). Never resize the whole source to the size of a crop: that shifts every pixel by the crop offset and inflates dE by several points.
4. Report mean CIE76 Lab dE: `all`, `face` (inside `face_box`, default the first focus ellipse box x 1.15) and `rest`. Also `sim_vs_raw` (what the plan predicted) and `live_vs_sim` (how faithfully Paint executed it).

`--vs raw` (default) compares with the unfiltered source, the right metric for mode 1. For stylised modes the dE against the source is not a quality measure (a pop-art version is meant to differ): report `live_vs_sim` and show `compare.png`.

Reference numbers (Mona Lisa, 450x672 drawing, inset 16): live 6.30 all, 5.36 face; old sim 5.29; this package's sim with the default tool model 5.98 with frame. Live test (composed landscape, ukiyo-e, 360x480): live vs sim 4.55, live vs source 14.84, sim vs source 14.62.

If `score` says `canvas not found on screen`, Paint is no longer in front (the user took the screen back) or something covers the strip: nothing is written; ask the user before bringing Paint forward.

Files written: `live.png` (the drawing area), `live_canvas.png` (the canvas without the palette strip, frame included: the gallery crop, canvas x 41 to the right edge, full height), `compare.png` (target, simulation, live), `score.json`, plus `grab_score.png` for `--take`. Crops from a screen grab show Paint's small resize-handle dots at the canvas corners and edge midpoints; crops from the saved file do not.

Live results (nine styles painted by a fresh agent from SKILL.md, live_vs_sim): mondrian 1.7, pixel-art 2.1, ukiyo-e 2.7, fauvism 3.1, stained-glass 3.5, pop-art 4.1, pencil-sketch 12.6 (one-pixel misregistration of 1 px hatching inflates dE on line art; visually identical), sumi-e 12.1 and watercolour 14.8 with the old Watercolour model (refitted on those crops: about 8 and 11 now).
