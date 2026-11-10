# Motion language

> **Use when:** choosing camera moves, kinetic typography, beat-stepped reveals, counters, glows and audio-reactive light for a scene, or when a piece feels static, mechanical or "like slides".
> **Inputs:** `storyboard.md` (motion verbs, signature), `design.md` (eases), `beats.json` if music is used.
> **Outputs:** a motion plan per scene: camera verb with values, entrance per read, accents on the grid, the audio-reactive target.
> **Next:** [transitions.md](transitions.md) and [morphs.md](morphs.md) for scene changes; [hyperframes.md](hyperframes.md) to build.

Cards sliding in is not motion design. Energy comes from camera language, real morphs, one idea per beat and reveals locked to the music or the voice.

## Principles

- **One camera verb per clip,** applied to a camera wrapper; pan and zoom live on nested wrappers, never on the same element.
- **Never fully freeze.** After every hit, a slow drift: scale +1.8-5% over 1.3-3.3 s, `sine.inOut`. No run of more than 24 frames (0.8 s) without movement.
- **Land on the beat.** An entrance starts on the beat; an arrival ends on it (start = beat - duration). Slams start 30-60 ms early, presses 30 ms early, impact sounds 20 ms ahead of the visual.
- **Build tension by rate, not by adding elements:** repeat one gesture every beat, then every half beat, then every quarter beat, shortening each step (0.3, 0.18, 0.1 s).
- **Texture tells the story:** faint payload text, tool ids, logs or real data drifting behind, never decorative particles.
- **Seek-safe always:** one paused timeline, explicit positions on every tween, `fromTo` with explicit start states, `immediateRender: false` on a later `fromTo` of the same property, finite repeats, state changes as stacked elements toggled by opacity, DOM measured once at setup.

## Camera moves

| Move | Recipe | Use |
|---|---|---|
| Lens punch on frame 0 | hero from z 520, rotationY -8 to its pose in 0.55 s `expo.out` (perspective 1400), then a 1.2 s drift | open on a full frame and a hit |
| 3D fly-in with parallax | world from z -1600, rotationX 50 to z 340, rotationX 22 over 1.9 s `power3.out`; parallax layers drift independently; an oversized grid pans slowly | hook, context reveal |
| Slow dolly with rack focus | dolly scale 1.0 to 1.07 over 3.3 s; blur and dim every group but the subject (blur 9 px, opacity 0.55, 0.5 s) | premium, calm |
| Vertical push in a tall world | pan wrapper y -1080 to 0 in 0.62 s `power3.inOut` inside a zoom wrapper; foreground racks out (blur to 22-30 px) | vertical formats |
| Whip pan | rig x/y/scale over 0.75 s `power4.inOut` plus blur 0 to 9 px and back | topic change, time jump |
| Orthographic schematic | paper ground, 60 px grid at 0.07 opacity, lines that draw themselves (dash offset 1 to 0, 0.7 s, stagger 0.12), junction dots `back.out(3)` | architecture, data flow |
| 2D crane (instead of 3D on a whole scene) | scale 1.34 and rotation -5 to flat over 2.4 s `power2.inOut`, with a growing drop shadow as the height cue | overhead reveal |
| Hero device orbit | layered divs for thickness and glass, rotY -34 to -22 over 3.6 s, macro push on a downbeat, a glare sweep | phone or hardware |
| Push-in and hold | scale 1 to 1.05 over 1.45 s after a resolve; a final lockup drifts 1.8% | after every payoff |

CSS 3D on a single element is fine; 3D on a whole scene can lower capture fidelity in some renderers, so crane in 2D.

## Kinetic type: a different entrance per read

| Treatment | Recipe | Best for |
|---|---|---|
| Scale slam | scale 1.7 and blur 18 px to 1 and 0, 0.42 s `expo.out`, origin left, start 0.06 s early | the first read, a strong downbeat |
| Mask rise per line | each line in an overflow-hidden box, text yPercent 105 to 0, 0.55 s `power4.out`, stagger 0.1 | two or three line reads |
| Tracking collapse | letter-spacing 0.35em to -0.01em with a fade, 0.5 s `power3.out` | a light answer line under a heavy one |
| Blur resolve | blur 24 px and scale 1.06 to sharp, 0.55 s `power2.out` | focus-pull camera language |
| Skew slide | x -140, skewX 14 to 0, 0.4 s `power4.out` | action verbs |
| Clip wipe with underline | `inset(0 100% 0 0)` to `inset(0)`, 0.65 s, underline scaleX 0 to 1 on the next beat | the moral of the clip |
| Word-by-word build | one word per beat, each word triggering a micro-animation on the UI element it names | listing capabilities without chips |
| Demote, don't delete | the previous read shrinks to opacity 0.16, scale 0.8 while the next enters | sequential reads in one scene |
| Persistence | earlier lines stay small as a top row while the last enters large | three-part taglines |

## Reveals on the grid

- **Beat helper:** `B(i) = firstBeat + beatLength * i`, plus named strong downbeats (`D1`, `D2`...). Measure them from the actual track ([audio.md](audio.md)).
- **Cause and effect on every other beat:** a row arrives on the beat, its result 0.35 s later, a fact card 0.4 s later.
- **Parallel start, sequential finish:** several workers start together and one finishes per following beat while a counter ticks 1/N to N/N.
- **Slot-machine reel:** logos stacked in one reel inside a clipping window; a swap is a y translate (0.6 of the step, `expo.out`), never a `src` change; keep the window moving between swaps.
- **Satellites into a fixed orbit:** items fly from the hub to trigonometric positions with `back.out(1.6)`, stagger 0.05, then never move: stillness carries the idea.

## Rings, lines, counters

- Shock ring on an event: scale 0.6 to 7, opacity 0.95 to 0, 0.8 s `power2.out` (small: 0.55 to 3.4 in 0.42 s). It also hides a swap underneath.
- A light that only grows: `expo.out` pops on strong downbeats, slow creep between them.
- Self-drawing paths: `pathLength="1"` and dash offset 1 to 0; flowing dashes move their offset by whole periods with linear ease so loops are seamless.
- Gauge: circumference `C = 2 pi r`; offset `C * (1 - pct)`; a stepped gauge fills one Nth per event.
- **Counters are computed from time** (count the events whose time has passed) so any seek shows the right number; never increment in a callback.

## Audio-reactive light (subtle)

Extract per-frame loudness (RMS) and frequency bands at the video frame rate ([../scripts/audio_reactive.py](../scripts/audio_reactive.py)), embed the arrays, and sample them by frame index on the timeline. Bass drives large light surfaces (glow opacity `0.72 + 0.28 * min(1, 1.4 * bass)`, shadow blur `40 + 70 * bass` px); RMS drives thin lines (stroke opacity `0.4 + 0.6 * rms`). Text moves at most 3-6%, backgrounds 10-30%. Gate each glow to its window with a ramp so it fades in. Drive a real product affordance (a "working" border), never waveforms, equaliser bars or pulsing orbs. As the music fades, the light dims with it.

```js
// sample a baked per-frame array on the one paused timeline (seek-safe)
var glow = { k: 0 };
tl.to(glow, { k: 1, duration: CLIP, ease: "none", onUpdate: function () {
  var b = BASS[Math.min(BASS.length - 1, Math.round(this.time() * FPS))] || 0;
  halo.style.opacity = (0.72 + 0.28 * Math.min(1, 1.4 * b)).toFixed(3);
} }, 0);
```

## Gate

Each scene has its camera verb with values, a distinct entrance per read, accents on named beats, no frozen run over 0.8 s, and at most one audio-reactive element per scene.
