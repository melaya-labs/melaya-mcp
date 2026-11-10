# True morphs

> **Use when:** one element must become the next (a row becomes a card, a cursor becomes a button, shapes become the logo, a device screen becomes the world), or a morph looks like a blob, stretches text or loses the logo.
> **Inputs:** `storyboard.md` (the named morph per scene), the source and target elements, the strong downbeat to land on.
> **Outputs:** a morph recipe per scene: technique, duration, ease, lock time, hand-off.
> **Next:** [hyperframes.md](hyperframes.md).

A true morph changes shape and identity (size, colour, content, role) while the viewer tracks one object through the change. Fades, slides and goo blobs are not morphs. Give every clip at least one, from a different family than its neighbours.

## Rules for every morph

1. **Content out before, content in after.** The inner text fades out in the first 0.2 s, the container changes, the new content lands after the lock, label last. Text is never visibly clipped or stretched.
2. **Short.** 0.3 s is ideal, 0.45-0.62 s for containers, never over about 1 s: overlapping intermediates read as a soft blob. Punch right after (a ring, a settle).
3. **Lock on a strong downbeat:** start = beat - duration, impact sound 20 ms ahead.
4. **Move the camera with it:** pull back on a split, push in on a container morph.
5. **End on the real artwork.** A morph into the logo ends on a vector stand-in of identical geometry; the real bitmap fades in over 0.1-0.2 s, the vector fades 0.1 s later, hidden under a shock ring or a 1.05 overshoot that settles with `back.out(2)`. Never redraw the logo in the final frame.
6. **Seek-safe:** drive the morph from a proxy value `p` from 0 to 1 and compute the shape from `p`; `immediateRender: false` on every `fromTo` after another tween of the same property.

## Chooser

| You want | Technique | Duration, ease |
|---|---|---|
| A shape to become the logo | point-resampled path morph: both shapes resampled to the same N = 96 points starting at the top, lerped by `p`; or a path-morph plugin with both paths baked into one coordinate space | 0.3 s `power3.inOut` (resampled), 0.57 s `power2.inOut` (plugin) |
| Many marks to become one line | swap raster logos for disc paths of the same centre and radius, morph all to one capsule; stagger starts 0.08 s and shorten durations (1.0, 0.92, 0.84 s) so they arrive together; hide trailing discs once the lead has arrived | about 1 s `power3.inOut` |
| One to become many | shared-box split: lay items at their final slots, set them all onto the first item's box, then FLIP each home with a small rotation kick while the camera pulls back | 0.7-0.8 s `expo.out`, stagger 0.04 s |
| A list row to become a card or modal | rect-to-rect FLIP: show the card inverted over the row (offset and scale from the two rects) and tween to identity; recolour 0.04 s in; content in at +0.22 s | 0.45 s `power3.inOut` |
| A container to become another container (input to message, chip to card) | one element whose `clip-path: inset(... round r)` tweens between two rects; a ring 3 px larger behind it recolours; a gradient fades in as an overlay layer (gradients do not tween) | 0.62 s `power3.inOut` |
| An actor to become a control and back | author the element at the final button size; scaled down with an elliptical radius it renders as a cursor puck; lift, travel, land as the button | lift 0.16 s, land 0.26 s `back.out(1.3)` |
| A row to become a circle, pill or gauge | SVG rect attributes (`rx = ry = w / 2` makes a circle) while a duplicate of the content slides away | 0.6 s `power3.inOut` |
| An object to survive a shader cut | camera lock point: end on an object at a known position; the next scene's camera starts at scale 2 on that point with a pixel-identical object, then cranes out | crane 2 to 1 over 1.15 s |
| A device screen to become the full frame | a full-frame layer revealed by a clip that starts exactly on the screen rect at the device's current scale and opens to the frame; a scaled copy of the screen content hides the swap | 0.63 s `power3.inOut` |
| A request to become its answer | 3D card flip (perspective 1100 px, back face rotated 180, `backface-visibility: hidden`) with a z lift of 60 that yoyos | 0.65 s `power2.inOut` |
| A picked item to become the brand | the drop layer starts on the exact pixels of the picked glyph; lift (-16 px, 1.14, 0.07 s), dive (1.3, 0.19 s `power3.in`) while the path morphs to the logo silhouette (0.26 s); real artwork under a shock ring | under 0.3 s |
| The hero to become part of the lockup | glide FLIP: author the final lockup in CSS, animate from the inverted offset in one move; the wordmark wipes out from behind it; tagline lines enter around it with different entrances | 1.6 s `power3.inOut` |

## Recipes in code

```js
// point-resampled morph: A and B are arrays of N [x, y] points, same start point
function pathAt(p) { var d = "";
  for (var i = 0; i < N; i++) { var x = A[i][0] + (B[i][0] - A[i][0]) * p, y = A[i][1] + (B[i][1] - A[i][1]) * p;
    d += (i ? "L" : "M") + x.toFixed(2) + " " + y.toFixed(2); }
  return d + "Z"; }
tl.fromTo(content, { opacity: 1 }, { opacity: 0, duration: 0.24, ease: "power2.in", immediateRender: false }, T);
tl.fromTo(m, { p: 0 }, { p: 1, duration: 0.3, ease: "power3.inOut", immediateRender: false,
  onUpdate: function () { path.setAttribute("d", pathAt(m.p)); } }, T);
tl.fromTo(logoPng, { opacity: 0, scale: 0.96 }, { opacity: 1, scale: 1, duration: 0.1 }, T + 0.22);  // hand-off
tl.fromTo(vector, { opacity: 1 }, { opacity: 0, duration: 0.1 }, T + 0.28);
tl.fromTo(ring, { opacity: 0.9, scale: 1 }, { opacity: 0, scale: 1.35, duration: 0.55, ease: "power2.out" }, T + 0.3);

// rect-to-rect FLIP: the card sits at its final rect
tl.fromTo(card, { x: src.cx - dst.cx, y: src.cy - dst.cy, scaleX: src.w / dst.w, scaleY: src.h / dst.h },
  { x: 0, y: 0, scaleX: 1, scaleY: 1, duration: 0.45, ease: "power3.inOut", immediateRender: false }, T);
```

Trace the target polygon from the real logo outline, scaled into place, so the vector lands exactly on the bitmap.

## Failure modes

| Symptom | Fix |
|---|---|
| Soft blob for about 0.5 s | shorten under 0.3-0.5 s; hide trailing shapes once the lead has arrived |
| Text stretches or clips | fade content out first, change the container, content in after the lock |
| Logo looks off at the end | hand off to the real bitmap under a ring or overshoot |
| Object jumps across a shader cut | camera lock point with a pixel-identical object in the next scene |
| Shape tween does nothing | identical structure at both ends; for circles use a scaled element or a CSS variable |
| Wrong start state when scrubbing | `immediateRender: false` on the later `fromTo` |

## Gate

Each named morph has its technique, duration under 1 s, lock time on a strong cue, and (for any logo) a real-artwork hand-off; a mid-morph still has been looked at.
