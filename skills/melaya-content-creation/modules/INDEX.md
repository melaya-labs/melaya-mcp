# Module graph

Every module is a node with typed inputs and outputs; an edge means "the output of A is the input of B". Load the node you need and follow its Next line; never load the whole graph of modules. The artifacts named here are files in the piece's output folder.

## Nodes

| Module | Inputs | Outputs | Next |
|---|---|---|---|
| [brief](brief.md) | request, source (site, repo, assets) | `brief.md` | brand-kit, narrative |
| [brand-kit](brand-kit.md) | source | `brand-kit.md` (tokens, fonts, logo, voice, UI inventory) | design-system, narrative |
| [narrative](narrative.md) | brief, brand-kit | `script.md` (hook, reads, voiceover) | storyboard |
| [storyboard](storyboard.md) | script, style preset | `storyboard.md`, `timeline.json`, shot list | design-system, hyperframes |
| [design-system](design-system.md) | brand-kit, platform | `design.md` (type scale, colour roles, motion language) | motion, product-ui, stills |
| [motion](motion.md) | storyboard, design | motion plan per scene | transitions, morphs, hyperframes |
| [transitions](transitions.md) | storyboard | transition per cut | hyperframes |
| [morphs](morphs.md) | storyboard | morph recipe per scene | hyperframes |
| [product-ui](product-ui.md) | repo or site, storyboard | recreated UI scenes, mock data | hyperframes |
| [assets](assets.md) | storyboard | `assets/` + `assets/ledger.md` | hyperframes, audio, stills |
| [audio](audio.md) | storyboard, script | music slice, `beats.json`, SFX plan, voiceover, mix | captions, hyperframes |
| [captions](captions.md) | voiceover or script | `captions.srt`, `.vtt`, `.ass` or caption track | render-qa |
| [hyperframes](hyperframes.md) | everything above | `composition/` | render-qa |
| [remotion](remotion.md) | everything above | Remotion project | render-qa |
| [platforms](platforms.md) | target platforms | sizes, durations, safe zones | storyboard, render-qa, publishing |
| [stills](stills.md) | brief, design | carousel slides, thumbnails, posters, product shots | render-qa, publishing |
| [render-qa](render-qa.md) | composition | render, `poster.jpg`, `qa/` report | publishing |
| [publishing](publishing.md) | render, brief | `share-copy.txt`, publishing package | done |
| [multilingual](multilingual.md) | approved source piece | per-language voice, captions, renders | audio, captions, render-qa |
| [films](films.md) | storyboard over 25 s | segment table, clips, assembled film | render-qa, review |
| [review](review.md) | any draft | notes table, revision plan, crew briefs | the module that owns the fix |
| [tooling](tooling.md) | the host | tool status, install steps, handoff package | hyperframes or handoff |
| [troubleshooting](troubleshooting.md) | a symptom | cause and fix | the module that owns the fix |

## Standard flows

| Deliverable | Path through the graph |
|---|---|
| 15-25 s launch or promo clip | tooling, brief, brand-kit, narrative, storyboard, design-system, (product-ui, motion, transitions, morphs as the storyboard needs), assets, audio, hyperframes, render-qa, publishing |
| 30-120 s narrated explainer or film | the clip path, plus captions; films when built from several clips; review after the first cut |
| Vertical or square version | platforms, storyboard (re-layout), hyperframes, render-qa |
| Carousel, thumbnail, poster, product shot | brief, brand-kit, design-system, stills, render-qa, publishing |
| Localised versions | multilingual, audio, captions, render-qa |
| Revision of a delivered piece | review, then the owning module, then render-qa |

## Resources

| Folder | What is there | When to read it |
|---|---|---|
| [../styles/](../styles/) | Tone presets (`tone-*.md`: pacing, scenes, transitions, copy, audio) and visual looks (`look-*.md`: type, palette approach, grounds, motion) as data | storyboard and design-system pick one tone and one look |
| [../templates/](../templates/) | brief, script, storyboard, shot list, render checklist, publishing package, voice card; a composition skeleton | copy the one you are filling |
| [../examples/](../examples/) | Worked examples for fictional brands: social clip, narrated explainer, launch film, carousel and thumbnail | when you want a finished reference of the same kind |
| [../scripts/](../scripts/) | Tool detection, beat grid, audio-reactive data, caption files, frame QA, poster bake, ducked mix | when a shell is available ([tooling.md](tooling.md)) |

## Adding a node

A new module is one file in `modules/` that opens with a title and the four-line front block (Use when, Inputs, Outputs, Next), plus one row in the router's intent table and one in the node table above. Keep modules generic: no brand, product or person names, plain ASCII, numbers over adjectives.
