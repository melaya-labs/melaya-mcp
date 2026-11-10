# Narrative and script frameworks

> **Use when:** writing the hook, the on-screen reads, the voiceover or the story shape of any piece, from a 6 s bumper to a 3 min film.
> **Inputs:** `brief.md`, the voice card in `brand-kit.md`, a tone preset from [../styles/](../styles/).
> **Outputs:** `script.md` (template: [../templates/script.md](../templates/script.md)): angle, hook, beats with reads and voiceover lines, CTA.
> **Next:** [storyboard.md](storyboard.md) turns the script into timed scenes.

## The spine: Hook, Problem, Reveal, Proof, CTA

Every format is this spine, compressed or stretched. The product in use is the centre of it; the stat-card row and the landing-page hero are at most a frame around it.

| Beat | Job | Rule |
|---|---|---|
| **Hook** | earn the next seconds | lands in the first 1.5-2 s (vertical: the first second); the frame is already full at frame 0 |
| **Problem** | name the pain the audience has | one claim, often a number or an absence; at most 17% of the runtime |
| **Reveal** | the product appears doing the job | its name is said or shown while the product is on screen |
| **Proof** | the concrete result | a real UI state, a real output in the place it is received (an inbox, a posted message, a filled sheet), approved facts only |
| **CTA** | what to do now | one canonical URL or "available now"; never promise access, keys or anything not offered at publish time |

## Shapes by length

| Length | Shape | Reads on screen |
|---|---|---|
| 6 s bumper | hook claim, product glimpse, logo | 1-2 |
| 15 s clip or ad | hook (0-2), problem or claim (2-4), product in use (4-10), proof (10-13), lockup (13-15) | 3-4 |
| 18-25 s launch clip | hook (2-3), reveal (2-4), 2-3 highlights (5-12), punchline or outro (2-4) | 4 at most |
| 30-45 s feature explainer (narrated) | hook, setup, product in use, trust or control moment, proof, CTA | headline-only, in narration order |
| 60-90 s launch film | intro (7-8 s), one 12-16 s unit per product or feature, outro (8-10 s) | see [films.md](films.md) |
| 2-3 min tutorial or overview | chapters of at least 10 s each, one task per chapter | captions carry the detail |

One run tells one story in 15-25 s. A story that needs more than about four reads or more than one product becomes several units joined into a film, never one stretched clip.

## Hook formulas

| Formula | Pattern |
|---|---|
| Number first | "{N} tools. {N} tabs. 1 person." |
| Benchmark contrast | "{familiar slow thing}: {big number}. {product}: {small number}." |
| Provocation | "Your next {role} isn't a {person}. Watch." |
| Inverted value | "{Something usually bad}. That's the feature." |
| Behaviour reframe | "Stop doing the {task}. Start approving it." |
| Literal anxiety | the audience's own pain shown as a message bubble: "{500} cold emails. {2} replies." |
| The result first | the finished output on screen with a two-line claim ("Made by {product}. In {time}.") |
| A question they are about to ask | asked, then answered in the reveal |

Write the hook first and the rest after. For variants, change only the hook beat and the first line, then re-render.

## On-screen reads

- **Readable floor:** a 1-3 word line stays fully visible and settled about 0.8 s; a sentence 0.3 s per word, at least 1.2 s; labels the viewer must read at least 1.5 s. Text that is only texture (scrolling logs) needs no floor.
- **At most about four reads per 15 s.** A 4 s scene carries two or three short reads. Too much text for the time: cut copy or split the scene, never speed it up.
- **One idea per read.** Verbs first, numbers over adjectives. Hero lines are broken by hand, about 10 characters per line in vertical.
- **No generic SaaS language** ("streamline your workflow" is banned). Use the product's own words.
- **Humour earns its place** from the product's own absurdity, never from trying.
- **Copy hygiene:** no em-dashes or exclamation marks on screen unless the brand uses them; replace with a colon, a period, a middle dot or parentheses. Plain ASCII on screen when fonts are uncertain.

## Voiceover script

- Narration explains in full sentences; on-screen text stays headline-only and complements it. Never read the screen aloud.
- **Narration order equals on-screen read order.** Reorder sentences or reads until they match; the eye and the ear meet the same word at the same time.
- Open each section by naming what is on screen ("{Product} is...", "{Feature} lets you...") so the name is spoken while its title is up.
- Rate: about 2.8-3.1 words per second for an English neural voice at speed 1.05, pauses included. A 15 s clip carries about 35-45 words; a short vertical at most 50 words in 8 lines.
- Keep two fields per sentence: `caption` (what is read) and `tts` (numbers as words, acronyms as spoken, respellings). Same punctuation in both so pauses match the captions. Commas at breath points.
- Too long for its slot: shorten the sentence. Never push the voice past about 1.1x speed in English.

## The angle

One sentence above the script that makes the piece specific to this product: the creative premise, the joke or the claim. If the same script could advertise a competitor, the angle is missing.

## Gate

`script.md` has the angle, the hook, every beat with its reads (counted against the floor) and its voiceover line, and the CTA. Every claim is in the source or the approved facts.
