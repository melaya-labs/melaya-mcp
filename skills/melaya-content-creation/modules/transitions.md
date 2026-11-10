# Transitions

> **Use when:** choosing or building the change between two scenes, or the join between two rendered clips; fixing a transition that flickers, goes black or looks the same everywhere.
> **Inputs:** `storyboard.md` (transition mood per cut, the clip's family), `beats.json` for timing.
> **Outputs:** one named transition per cut with duration, ease and beat placement.
> **Next:** [hyperframes.md](hyperframes.md) to build; [films.md](films.md) for joins between clips.

A transition says how two scenes relate: continue, contrast, jump in time, zoom into detail, converge. It is the exit of the outgoing scene: no separate exit animation before it (the final scene of a piece is the exception).

## Rules

- **One primary family per clip** (60-70% of its cuts) plus one or two accents; a different primary in each clip of a film.
- **Place by narrative position:** the most distinctive at the opening, the primary between related points, a different one at a topic change, the boldest on the hero reveal, gentle for the wind-down, the simplest for the outro.
- **On the beat:** centre burns, flashes and warps on the downbeat (start = beat - duration / 2); land zooms and whips that reveal content on it (start = beat - duration).
- **Energy sets duration:** calm 0.5-0.8 s `sine.inOut`; medium 0.3-0.5 s `power2`/`power3`; high 0.15-0.3 s `power4`/`expo`. Blur by energy: calm 20-30 px, medium 8-15 px, high 3-6 px.
- **Never mix two scene-switching systems** (CSS visibility and a shader engine) in one composition.
- A plain crossfade between two busy layouts makes a muddy double exposure: stagger it (old out, new in) or dip through the ground.
- Avoid: star iris (polygon interpolation breaks), tilt-shift, lens flare, door or hinge, and any visible repeating pattern (tiles, hex cells).

## CSS and timeline transitions

| Name | Build | Duration and ease | Meaning |
|---|---|---|---|
| Zoom-through | camera wrapper scales into an origin point (scale 5, blur 14 px), the next scene takes over | 0.42 s `power3.in` | dive into detail |
| Flash pop | a white layer opacity 0.85 to 0 (never a `brightness()` filter: it reads grey) | 0.28 s `expo.out` | payoff, drop |
| Horizontal blinds | N full-width strips alternate in from left and right, cut under the cover, mirror out; 4 strips calm, 6-8 medium, 12-16 high | 0.22-0.24 s each, stagger 0.018 s, `power3.inOut` | tech, energy |
| Staggered blocks | three full-frame blocks in brand colours sweep in (stagger 0.06 s), swap under cover, sweep out | 0.25 s each | brand moment |
| Clock wipe | conic mask driven by a CSS variable from 360 to 0; or a 9-point polygon advancing one quadrant per 0.11 s for a mechanical feel | 0.45 s `power2.inOut` | time passing |
| Diagonal split | the outgoing layer on top, its 4-point polygon collapses to a corner; the seam becomes the next layout | 0.55 s `power3.inOut` | reveal behind |
| Iris from a point | a scaled disc (200 px, scale 0 to 15) or a circle clip driven by a CSS variable; a GSAP tween of a `circle()` string does not render | 0.45-0.48 s `power3.in` | open onto |
| Focus pull | blur and dim all but the subject while the dolly leans in (scale 1.1) | 0.5-0.6 s | attention shift |
| Whip push | x -2100 with blur 18 px | 0.38 s `power4.in` | jump |
| Card-fall | the outgoing frame shrinks to a card (scale 0.55, radius 48, y 80, 0.25 s `power3.out`) then drops (y 1300, rotation 8, 0.2 s `power3.in`) | 0.45 s | ending, dark to light |
| Chromatic aberration | two coloured drop-shadows offset by plus and minus 30 px times k (k 0 to 1 in 0.2 s, decays 0.42 s), lateral shake 40, -30, 18, 0; overlays in normal blend about 35% (multiply is invisible on dark) | 0.6 s total | glitch, tension |

Shape tweens need structurally identical strings at both ends: same `inset()` radius count, same polygon vertex count (pad with repeated points). CSS variables inside `clip-path` or `mask` animate reliably when no shader engine captures the element.

```css
/* circle iris and conic clock driven by custom properties */
.iris { clip-path: circle(calc(var(--r, 75) * 1%) at 50% 50%); }
.clock { mask-image: conic-gradient(from 0deg at 50% 50%, #000 0deg, #000 calc(var(--a, 360) * 1deg),
  rgba(0,0,0,0) calc(var(--a, 360) * 1deg)); }
```

A radius of 75% covers the corners in any aspect ratio (a circle percentage is relative to the diagonal divided by the square root of 2).

## Shader transitions

HyperFrames ships a shader-transitions package (search the registry first: [hyperframes.md](hyperframes.md)). Shaders capture whole scenes to textures, so they impose rules.

| Shader | Look | Use when | Watch for |
|---|---|---|---|
| cinematic-zoom | radial zoom blur | into light or detail, drops | needs colour contrast between scenes; at most half the clips of a film |
| whip-pan | lateral smear | time jump, topic change | midpoint can be an empty frame: keep strong content near the travel edges |
| sdf-iris | circle opening | open onto | always opens from frame centre: centre the subject |
| cross-warp-morph | organic flow | calm, premium | warps type while running: start text after it |
| gravitational-lens | inward pull | before a convergence | |
| domain-warp | noise burn tinted by the accent | change, tech, warm grounds | |
| flash-through-white | overexposure | payoff on a beat | centre the peak on the beat |
| light-leak | warm bleed | only under a musical swell | greys light grounds, turns warm grounds olive |
| glitch, chromatic-split, ridged-burn, ripple, swirl, thermal | stylised | tech, playful, warm | test a mid-transition still on your ground first |

Shader-safe checklist: every scene full-frame with an explicit background colour equal to the shader's background; scenes after the first start hidden in CSS; no `transparent` in gradients and no `var()` on captured elements; glow layers excluded from capture; fonts and images embedded as data URIs; all DOM built synchronously before the shader init; anything continuous across a cut duplicated in both scenes; something always moving while a shader runs (a static swapped element renders black).

To get a CSS-style change inside a shader composition: a plain scene switch timed under a full CSS cover (0.06-0.08 s), sub-layers revealed by CSS inside one shader scene, or a state swap under a cover with no scene switch at all.

## Choosing

| Mood | Primary | Accent |
|---|---|---|
| Calm, premium | cross-warp, focus pull, soft crossfade | iris on a centred subject, card-fall |
| Product walkthrough | whip, cinematic zoom, blocks, push | clock wipe, diagonal split |
| Launch, hero | cinematic zoom, flash-through-white, zoom-through with flash, blinds 12-16 | chromatic aberration |
| Tech, developer | domain-warp, chromatic split, blinds | scaled-disc iris |
| Light or warm grounds | domain-warp, flash, clock wipe | card-fall (avoid light-leak) |
| Time jump, replay | whip | playhead rewind |
| Many into one | gravitational-lens, scaled-disc iris | a morph into the target |

## Gate

Each cut has a named transition, the clip's families are recorded, nothing mixes scene-switching systems, and a mid-transition still of every cut has been looked at ([render-qa.md](render-qa.md)).
