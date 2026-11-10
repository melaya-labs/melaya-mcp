# Content creation skill

An agent skill that makes launch, promo, explainer, ad and social videos, films, carousels, thumbnails, product shots, captions and share copy for any brand or product, end to end: brief, brand kit, script, storyboard, design, composition, audio, captions, render, QA and publishing package. It builds with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML, CSS and GSAP rendered frame by frame), offers Remotion as an alternative, and hands off a ready-to-render package when no renderer is available.

It is generic: no house style is assumed. Brand, tone and look come from the source (a website, a code repository, an asset folder) and from presets stored as data.

## How it is organised

`SKILL.md` is a short router: ten rules that always apply and an intent table. Everything else loads on demand, so an agent reads one to three modules per task instead of the whole skill.

```text
SKILL.md                 router: rules, intent table, typical flows
modules/INDEX.md         the graph: every module's inputs, outputs and next steps; standard flows
modules/                 brief, brand-kit, narrative, storyboard, design-system, motion, transitions,
                         morphs, product-ui, hyperframes, remotion, audio, captions, assets, platforms,
                         stills, render-qa, publishing, multilingual, films, review, tooling, troubleshooting
styles/                  tone presets (tone-*.md) and visual looks (look-*.md) as YAML data
templates/               brief, script, storyboard, shot list, render checklist, publishing package,
                         voice card, a HyperFrames composition skeleton
examples/                worked examples for fictional brands: 15 s social clip, 40 s narrated explainer,
                         80 s launch film, carousel and thumbnail
scripts/                 detect_tools.sh, beatgrid.py, audio_reactive.py, captions.py, qa_frames.sh,
                         poster.sh, duck_mix.sh
```

Every module opens with the same front block (Use when, Inputs, Outputs, Next), so the graph is explicit and an agent can follow it without loading the rest.

## Install

**Claude Code:** copy the folder into your skills directory and restart; it loads when you ask for a video, a carousel, captions or any other content piece.

```bash
cp -r melaya-content-creation ~/.claude/skills/
```

**Codex CLI:** copy the folder into `~/.codex/skills/` (or reference `SKILL.md` from your `AGENTS.md`).

**Gemini CLI:** reference the skill from your `GEMINI.md` (`@path/to/melaya-content-creation/SKILL.md`), or copy the folder into your project and point the context file at it.

**Any other agent or a hosted assistant:** add `SKILL.md` as an instruction or rules file and attach the `modules/` files as knowledge. Without a shell the skill still plans, writes and authors the composition, and delivers a render handoff (see `modules/tooling.md`).

## Requirements (for rendering)

Node.js 22 or newer for the HyperFrames CLI, ffmpeg and ffprobe (a build with libass for caption burn-in), Chrome or Chromium (the CLI can download one), and Python 3 with NumPy for the helper scripts. `scripts/detect_tools.sh` reports what is present. The installed HyperFrames agent skills (`hyperframes`, `hyperframes-core`, `media-use` and the others) are used when present and are not required.

## Credits and licences

This skill is released under the Apache License 2.0 with the repository that contains it.

- **brag** by Shunit Haviv Hakimi ([latent-spaces/brag](https://github.com/latent-spaces/brag), MIT License). The launch-video method is adapted from brag: the four gated steps (inspect, plan, compose, deliver), the planning rubric, the seven tone presets and their share-copy shapes, the creative laws (short, readable, specific, show the thing, the hook first), the reading-time floors, the music cue-locking tolerances, the poster frame baked as frame 0, and the boundary between the creative plan and the composition. The text here is rewritten and extended; no brag code, music or sound files are included. brag's licence notice:

  > MIT License. Copyright (c) 2026 Shunit Haviv Hakimi. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

- **HyperFrames** by HeyGen, Inc. ([heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), Apache License 2.0, Copyright 2026 HeyGen, Inc.). The composition contract (data attributes, the paused timeline registry, determinism rules), the CLI commands, the registry, caption-track and audio conventions and the shader-transition names described in `modules/hyperframes.md`, `modules/transitions.md`, `modules/audio.md` and `modules/captions.md` follow the HyperFrames documentation and agent skills; `templates/composition-skeleton.html` follows its documented minimal composition. No HyperFrames source files are copied. HyperFrames and HeyGen are names of their owner.
- The production method (pacing, typography, motion, transitions, morphs, captions, mixing and ducking numbers, multi-clip assembly, review loops, multilingual delivery) is distilled from the maintainers' own production notes, written for this skill.
- Fictional brands in `examples/` and `styles/` are invented for illustration.
