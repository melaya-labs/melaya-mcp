# Remotion alternative

> **Use when:** the user asks for Remotion, the team already has a Remotion project or React components to reuse pixel for pixel, or a long episodic series shares bookends and a primitives library.
> **Inputs:** the same plan as for HyperFrames: brief, storyboard, design, `timeline.json`, assets, audio.
> **Outputs:** a Remotion project (`src/`, `public/`, `remotion.config.ts`) and its render.
> **Next:** [render-qa.md](render-qa.md).

Everything before the build (brief, script, storyboard, design, audio plan) is identical. Only the composition layer changes.

## Choosing

| HyperFrames | Remotion |
|---|---|
| HTML, CSS and one paused GSAP timeline; fast iteration (stills in seconds, a 20 s render in under a minute) | React components and props; reuse of real product components; typed props for variants |
| one-shot camera worlds, shader transitions, registry blocks, vertical pieces | long series with shared bookends and a shared library of primitives |
| audio mix and voiceover carve inside the composition | audio placed with sequences; mixing usually done in ffmpeg |

Remotion renders slower (about 3 fps at 1080p with concurrency 2: a 60 s body takes about 10 min). Porting an existing Remotion composition to HyperFrames is its own job (an installed `remotion-to-hyperframes` skill does it, refusing patterns such as component state and effects that do not translate).

## Setup

- Pin `remotion` and `@remotion/cli` to one exact version; a minor update can break video components. Node 18 or newer, ffmpeg on the path, fonts installed or loaded explicitly (Remotion does not embed system fonts).
- Config: JPEG intermediates at quality 95 (about twice as fast as PNG, no visible difference), concurrency 2 (4 oversaturates a typical laptop), pixel format `yuv420p` (other formats show blue frames on Apple devices), codec h264, CRF 17.
- Layout: `src/index.ts` registers the root, `Root.tsx` declares compositions, `scenes/*.tsx`, `styles.ts` holds the tokens, one primitives file, `public/` for every asset.

```ts
// remotion.config.ts
import { Config } from "@remotion/cli/config";
Config.setVideoImageFormat("jpeg"); Config.setJpegQuality(95); Config.setConcurrency(2);
Config.setPixelFormat("yuv420p"); Config.setCodec("h264"); Config.setCrf(17);
```

```bash
npx remotion studio                                   # scrub and preview
npx remotion render src/index.ts Main out/main.mp4
npx remotion render src/index.ts Intro out/intro.mp4 --props='{"subtitle":"..."}' --overwrite
```

## Composition patterns

- Declare `<Composition id="Main" durationInFrames={seconds * 30} fps={30} width={1920} height={1080} />`; derive the duration from data (`timeline.json`) so the render always matches the plan.
- A schedule array of `{ start, duration, label }` dispatches scenes; each scene is a `<Sequence from durationInFrames>`.
- **Inside a Sequence, `useCurrentFrame()` is already local.** Subtracting the sequence start again gives negative frames and a black scene.
- `interpolate(frame, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing })` with a strictly increasing input range; `Easing.out(Easing.cubic)` for entrances, `Easing.bezier(0.2, 0.7, 0.2, 1)` for appear; `spring({ frame, fps, config: { damping: 14, stiffness: 120, mass: 0.9 } })` for a bouncy settle.
- Everything is derived from the frame: no mutable state, seeded randomness (or `Math.sin(frame * 13.7)`), no effects with side effects.
- `const SEC = (s) => Math.round(s * 30)`; a single speed constant that divides it retimes a whole composition uniformly.
- Footage with `OffthreadVideo`, assets with `staticFile()` from `public/` only (anything else is a 404 at frame 0).
- Layer order: backdrop, footage, dynamic layers, brand overlays (a top strip and captions over a 0.72-0.86 dark scrim with a 14-22 px backdrop blur), vignette.
- Dark-background loops can be keyed cheaply with `mixBlendMode: "screen"`; inside a backdrop-filter context, pre-key them to RGBA PNGs with ffmpeg `colorkey` instead.

## Audio and assembly

- Studio preview adds audio latency: an offset tuned by ear in Studio is about 0.58 s later than the same offset in an ffmpeg mix. Re-validate with an A/B render; the value is version-specific.
- Concatenate bookends with the ffmpeg concat demuxer and stream copy only when codec, resolution, frame rate and pixel format are identical; otherwise re-render the odd one.
- Mixing, ducking and loudness are the same ffmpeg recipes as any piece ([audio.md](audio.md)).

## Gate

The project renders at the planned frame count, `yuv420p`, with the plan's durations; then the same QA as any piece ([render-qa.md](render-qa.md)).
