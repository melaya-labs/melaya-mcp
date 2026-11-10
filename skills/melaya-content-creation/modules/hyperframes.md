# HyperFrames composition

> **Use when:** building, checking or rendering the video as a HyperFrames composition (HTML, CSS and a paused GSAP timeline rendered frame by frame in headless Chrome), adding registry blocks, or deciding what to hand to an installed HyperFrames skill.
> **Inputs:** `storyboard.md`, `design.md`, `timeline.json`, assets and audio in `assets/`, motion, transition and morph plans.
> **Outputs:** `composition-brief.md` and `composition/` (a valid project that passes check), then a render ([render-qa.md](render-qa.md)).
> **Next:** [render-qa.md](render-qa.md); [remotion.md](remotion.md) if Remotion is required instead.

## Who owns what

The plan (brief, script, storyboard, design, audio direction) owns what the piece says and shows. HyperFrames owns how: composition structure, animation mechanics, lint and render. When the HyperFrames agent skills are installed (`hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-audio`, `hyperframes-registry`, `hyperframes-cli`, `media-use`), load the domain skills you need and follow their current rules over this page; skip their intent interview, because the brief already exists. When they are not installed, this page is enough to build a valid project.

Write `composition-brief.md` first: objective, output paths, format and duration, source material and copy that must appear verbatim, tone and angle, visual identity, the scene summary, audio role and cue guidance, and the requirements (show real UI, readable text, duration, audio layer, check passes). It is the handoff boundary: product decisions in the brief, implementation in the composition.

## Project layout

```text
composition/
  index.html          root composition and its one paused timeline
  compositions/       sub-compositions (one per scene in larger pieces)
  assets/             images, logos, fonts (static woff2 per weight), music, sfx, voice, footage
  vendor/             gsap.min.js and any plugin or runtime, local copies
  hyperframes.json    registry config (created by init or add)
  meta.json           name, duration, fps, width, height
```

Every asset lives inside the project and is referenced by a relative path; absolute paths and remote URLs fail in the headless render. Vendor every library locally: a CDN script that fails to load leaves a black video with no error. Start from [../templates/composition-skeleton.html](../templates/composition-skeleton.html) or from the CLI's `init`.

## The contract

- **Root:** a `div` with `data-composition-id`, `data-width`, `data-height`, `data-start="0"` and `data-duration` (seconds), placed directly in `body` (a sub-composition file instead wraps everything, styles and scripts included, in a `template`). Root CSS: position relative, 100% size, overflow hidden.
- **Clips:** any element with `data-start` is a clip, visible in `[start, start + duration)`; divs need `data-duration`; images default to 3 s, media to their own length. Keep `class="clip"` on timed visual elements. `data-track-index` is a timeline lane for the editor; stacking order comes from CSS `z-index`.
- **Sub-compositions:** a host element with `data-composition-src="compositions/scene.html"`, its own `data-composition-id`, `data-start` and `data-duration`; the same id on the host, the inner root and the timeline key. The runtime nests child timelines itself.
- **One timeline per composition:** `gsap.timeline({ paused: true })`, built synchronously, registered as `window.__timelines["<composition id>"] = tl`. Never play it. Give every tween an explicit position; never rely on chained sequencing.
- **The render length is the root `data-duration`.** Keep it, `meta.json` and the timeline length equal; a mismatch cuts the video early or overruns the audio.
- **Media:** video is muted and inline; its sound is a separate audio element. Every audio element has an `id` (the mixer skips one without), a `data-start` and a `data-volume` (0 to about 4, 1 = unity). No `crossorigin`. Never call play, pause or seek. Animate a wrapper, not the media element.
- **Determinism bans:** `Date.now`, `performance.now`, unseeded `Math.random` (use a seeded generator), `requestAnimationFrame` or intervals outside the timeline, `repeat: -1` (compute a finite count), CSS `transition` on animated elements, network fetches at render time, layout measured during tweens, two timelines on one property.
- **Positioning:** do not combine a CSS `translate(-50%, -50%)` with GSAP x/y on the same element; bake `xPercent`/`yPercent: -50` with `gsap.set` at t = 0 or centre with flex. Transforms and opacity only; never animate width, height, top or left.
- **Callbacks fire during discovery and seeks:** never change visible state inside a timeline callback; pre-build the states and toggle them with opacity tweens.
- **Fonts:** a bundled family, or your own `@font-face` with a local file per weight, declared on every scene root. Text inside an SVG used as an image needs its own embedded font. Rasterise SVG images to PNG if they render empty.
- **Variables:** declare on the `html` element (`data-composition-variables`), bind with `data-var-text` or `data-var-src`, override per render; use them for per-language or per-variant text.

## Captions, audio and layout in the timeline

- All captions on one track: a single caption sub-composition carrying every group in order, one group visible at a time, each group hard-killed at its end ([captions.md](captions.md)).
- Every scene is a sub-composition in larger pieces; one element kind per track (video, graphics, captions, audio).
- Fades, ducking and voiceover carve are audio attributes on the bed, not GSAP volume tweens ([audio.md](audio.md)).
- Layout-audit escape hatches for intentional cases: `data-layout-allow-overflow` (push-ins, light), `data-layout-allow-overlap` (stacked titles, text inside a transition window), `data-layout-ignore` (decorative layers, duplicated morph layers).

## Registry first

Before hand-building any named visual (a glitch, film grain, a chart, a terminal window, a map, a caption style, a shader transition), search the registry: about 400 blocks and components, searched locally. Blocks are standalone sub-compositions installed into `compositions/`; components are snippets pasted into the host. Use them as installed, or read them for technique and rebuild inside your world: splicing a separately rendered block reintroduces a cut.

## The CLI loop

Commands, in order: `init` (scaffold; `--resolution landscape|portrait|square`), `add` and `catalog` (registry), `lint` while authoring, `check` (the single gate: lint, runtime, layout, motion and WCAG contrast; zero errors), `snapshot` (PNG stills at chosen times), `preview` (studio with hot reload; give the user the local URL), `render`, plus `tts`, `transcribe`, `beats`, `keyframes`, `remove-background`, `doctor`.

```bash
npx hyperframes@latest doctor --json            # Node 22+, ffmpeg, Chrome; gate on .ok
npx hyperframes init my-video --resolution landscape --non-interactive
npx hyperframes catalog --query "film grain" --json
npx hyperframes add <block-name>
npx hyperframes lint
npx hyperframes check --timeout 60000           # 0 errors before any render
npx hyperframes snapshot --at 1.2,3.9,7.7
npx hyperframes preview
npx hyperframes render --quality draft --output ../draft.mp4
npx hyperframes render --quality high --output ../final.mp4
```

Version notes: `check`, `beats`, `keyframes`, `timeline` and the `looks` and `delivery` quality presets exist in 0.8 and later; older 0.6 releases have `lint`, `validate` and qualities `draft`, `standard`, `high`. Pin the version a project was built with in its package scripts so every machine renders with the same engine. Behind a certificate-intercepting proxy the package runner may fail to reach the registry: run the cached CLI directly. When several renders run in parallel, use 2 workers each and raise the page navigation timeout (`PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS=120000`).

## Self-review before render

- [ ] `composition-brief.md` exists and names the exact product moments.
- [ ] At least one real UI, copy or visual element from the source is on screen.
- [ ] Duration equals the storyboard; root, meta and timeline agree.
- [ ] Music and SFX are wired as planned (or the silence is documented); 1-3 major reveals locked to strong cues within 0.15 s; sequential accents on the beat grid within 0.10 s, or natural timing chosen for readability (mark the locks in comments).
- [ ] At most one subtle audio-reactive element per scene, or a note why none.
- [ ] Check passes with zero errors; every warning read.
