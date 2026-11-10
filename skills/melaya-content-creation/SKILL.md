---
name: melaya-content-creation
description: Use for any content-creation request for a brand, product or feature - launch, promo, explainer, demo, ad and social videos (YouTube, Shorts, TikTok, Reels, LinkedIn, X, Product Hunt), carousels, thumbnails, posters and product shots, captions and subtitles, voiceover, scripts and storyboards, localised versions and brand-consistent asset sets. Plans like a creative director, builds with HyperFrames (HTML video; Remotion as an alternative) and delivers render, poster and share copy, or a ready-to-render handoff when no renderer is available. Load this first, then open only the modules the task needs.
version: 1.0.0
---

# Content creation

Turn a brief, a website, a code repository or a folder of brand assets into finished content: short videos, films, carousels, thumbnails, captions and the copy that ships with them, at a consistent professional standard for any brand, style or product. This file is the router: the rules that always apply, then which module to open. Open a module only when the task needs it; most tasks need one to three.

## Rules that always apply

1. **Brief first.** Write a one-page brief before any asset ([modules/brief.md](modules/brief.md)). Ask at most three questions; default the rest and say which defaults you took.
2. **Show the real thing.** Recreate the product's real UI, copy and assets from its source. Never invent metrics, testimonials, customers or claims; stand-in data is fictional (`.example` domains). Nothing secret or personal goes on screen.
3. **The brand comes from the source.** Extract colours, fonts, logo and voice ([modules/brand-kit.md](modules/brand-kit.md)); never guess them. Never redraw or recolour a logo.
4. **Readable beats fast.** Pace comes from motion and cuts, never from pulling text early: a 1-3 word line holds about 0.8 s settled, a sentence 0.3 s per word (1.2 s minimum). Keep essentials inside the platform's safe zones.
5. **Rebuild per format.** A vertical or square version is re-laid-out, never a crop of the landscape render.
6. **Deterministic frames.** Every frame is a pure function of time: one paused timeline, no wall clock, no unseeded randomness, no network at render time, every asset local.
7. **Gate before you ship.** Lint or check with zero errors, look at stills from every reveal and every mid-transition, confirm duration and frame count, listen to every boundary ([modules/render-qa.md](modules/render-qa.md)).
8. **Licensed media only.** Owned, licensed, public-domain or generated assets; record the source and licence of each in the asset ledger.
9. **Ask before anything outward.** Publishing, posting, uploading, paid generation or anything that spends money waits for the user's yes.
10. **No renderer, no pretence.** Without a shell or a renderer (a chat, a hosted agent, a pipeline step), deliver the brief, script, storyboard and composition source plus the exact render handoff ([modules/tooling.md](modules/tooling.md)). Never report a render you did not make.

## Intent table

| The task is about | Open |
|---|---|
| Unclear request, new piece, what to make, for whom, how long | [modules/brief.md](modules/brief.md) |
| Colours, fonts, logo, voice, UI from a site, repo or asset folder | [modules/brand-kit.md](modules/brand-kit.md) |
| Hook, script, voiceover text, on-screen copy, story shape by length | [modules/narrative.md](modules/narrative.md) |
| Scenes, beats, durations, timeline, shot list | [modules/storyboard.md](modules/storyboard.md) |
| Type scale, colour roles, grounds, easing, layout, what looks AI-made | [modules/design-system.md](modules/design-system.md) |
| Camera moves, kinetic type, counters, glows, audio-reactive light | [modules/motion.md](modules/motion.md) |
| Scene transitions, joins between clips, shader cuts | [modules/transitions.md](modules/transitions.md) |
| One element becoming the next (true morphs), logo hand-offs | [modules/morphs.md](modules/morphs.md) |
| Recreating product UI, cursors, typing, taps, approvals, mock data | [modules/product-ui.md](modules/product-ui.md) |
| Building the HyperFrames composition, CLI, registry blocks, render | [modules/hyperframes.md](modules/hyperframes.md) |
| Building in Remotion instead | [modules/remotion.md](modules/remotion.md) |
| Music, beat grid, SFX, voiceover, ducking, loudness | [modules/audio.md](modules/audio.md) |
| Captions and subtitles: timing, styles, burn-in, SRT and VTT | [modules/captions.md](modules/captions.md) |
| Images, icons, logos, stock, generated media, screen capture | [modules/assets.md](modules/assets.md) |
| Specs per platform: sizes, durations, safe zones, caption rules | [modules/platforms.md](modules/platforms.md) |
| Carousels, thumbnails, posters, product shots, social cards | [modules/stills.md](modules/stills.md) |
| Render settings, QA, lint, frame checks, poster, delivery encodes | [modules/render-qa.md](modules/render-qa.md) |
| Share copy, titles, descriptions, chapters, publishing package | [modules/publishing.md](modules/publishing.md) |
| Other languages: translation, voice, captions, delivery matrix | [modules/multilingual.md](modules/multilingual.md) |
| Films over 25 s, several clips, parallel builds, joins, assembly | [modules/films.md](modules/films.md) |
| Review rounds, notes, revisions, refining a look, crew roles | [modules/review.md](modules/review.md) |
| Which tools exist here, installing them, no-shell handoff, hosts | [modules/tooling.md](modules/tooling.md) |
| Something broke: black frames, wrong fonts, desync, cut-off audio | [modules/troubleshooting.md](modules/troubleshooting.md) |

The full graph (every module's inputs, outputs and next steps, plus the standard flows) is [modules/INDEX.md](modules/INDEX.md). Style presets are data in [styles/](styles/), fill-in templates in [templates/](templates/), worked examples for fictional brands in [examples/](examples/), helper scripts in [scripts/](scripts/).

## Typical flows

- **Launch or promo video (15-25 s):** brief, brand-kit, narrative, storyboard, then design-system with motion or product-ui, hyperframes, audio, render-qa, publishing.
- **Narrated explainer or launch film (30-120 s):** the same, plus captions, and films for anything built from several clips.
- **Social cut of an existing piece:** platforms, then storyboard again for the new format (rebuild, never crop), render-qa.
- **Carousel, thumbnail or product shot:** brief, brand-kit, stills, publishing.
- **Localised versions:** multilingual (it routes to audio and captions).

## Output folder

Write each piece into its own folder: `content-output/<slug>/` (timestamped `-YYYY-MM-DD-HHmmss` if it exists). Keep `brief.md`, `script.md`, `storyboard.md`, `composition/`, the render, `poster.jpg`, `share-copy.txt`, `assets/ledger.md` and `qa/` there; intermediate files go in `work/`.
