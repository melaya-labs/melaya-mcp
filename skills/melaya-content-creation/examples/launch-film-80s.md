# Worked example: 80 s launch film (fictional brand "Brightfold Suite")

Brightfold Suite is a fictional automation suite with four products: browser automation, phone automation, a chat-app integration and a search-ranking assistant. The film is built as units in parallel and assembled on one master track. All names are invented.

## Structure (30 fps)

Intro 8 s + 4 x (bridge 4 s + product unit 12.5 s) + outro 9 s = 83 s (2490 frames). For about 77 s, trim each unit to 11 s; for about 67 s, drop the bridges.

| Unit | Global (s) | Content |
|---|---|---|
| Intro (4 scenes) | 0-8 | dark ground, one light that only grows; a slot swaps "old tool" logos on an accelerating grid (beat, half beat, quarter beat); the tools lock into a still orbit; **morph:** the slot becomes the brand mark on a strong downbeat; 0.5 s held breath with no text; join: zoom-flash on the music drop |
| Bridge 1 | 8-12 | the product wheel turns, glyph 1 drops into the hub, the hub becomes the mark, a title card: wordmark, two-line product name (accent on line 2), one line; voice at bridge + 1.4 s: "Brightfold Browse is..." |
| Unit 1: browser automation | 12-24.5 | near-black, one accent; trailer camera with whip pans; **morph:** the agent's cursor puck becomes the "Take over" control and back; proof: "Completed: 14 actions"; exit join: iris |
| Bridge 2 + Unit 2: phone automation | 24.5-41 | light ground (alternation); a phone object orbiting, waking on the downbeat; **morphs:** a row becomes the approval card, the card flips, the screen breaks out to full frame; exit: diagonal split |
| Bridge 3 + Unit 3: chat-app integration | 41-57.5 | warm white with the chat app's UI recreated faithfully, its mark unaltered; **morph:** a mention chip becomes "thinking...", which grows into the answer card; approval in the thread; exit: blinds |
| Bridge 4 + Unit 4: search-ranking assistant | 57.5-74 | warm amber; 2D overhead crane only; **morph carried across a shader:** a search row becomes a gauge ring at a shared camera lock point; five workers start together and finish one per beat; ends calm; exit: card-fall into the light outro |
| Outro (one continuous shot) | 74-83 | four product glyphs morph into the mark's facets, real-logo hand-off, the mark glides into the lockup, three tagline lines build in that frame as spoken (earlier lines stay small), URL types at 45 ms per character, 1 s hold; the only music fade in the film |

## Production

- Orchestrator first: segment table in `timeline.json`, one master track (extended on bar lines, sliced per unit on whole frames with a beats file each), the signature matrix (no shared ground, camera verb, transition family or morph type), the source map of real UI files, `FILM_BRIEF.md`.
- One builder per unit in parallel, each in its own folder, rendering an exact frame count with no baked poster and its own SFX cue list.
- Assembly: a CSS-only composition plays the units back to back with freeze-frame joins (0.45 s), the narrated mix underneath (bed 0.30 ducked by the voice), SFX cue lists shifted onto the master.
- QA: joins grabbed at J-0.1, +0.12, +0.30, +0.6 s; a 2.5 s contact sheet; caption band checked on the units before the single film render; a review copy with unit-local and global counters at the top.
- Revisions in a copy of the approved version; notes by unit and local time.

## Deliverables

The film 16:9 with burned captions and a captionless master, SRT and VTT, a 4K YouTube upload, a 45 s vertical cut rebuilt from two units (not cropped), thumbnail, YouTube chapters (Intro 0:00, Browse 0:12, Phone 0:24, Chat 0:41, Rank 0:57, each at least 10 s), share copy and the publishing package.
