# Review loops, revisions and crew roles

> **Use when:** a draft comes back with notes, a look is "almost right", a reviewer rejected a direction, several revisions must be managed, or a large piece needs specialist pre-production (strategy, copy, brand, growth) before building.
> **Inputs:** the current version, the reviewer's words verbatim, the plan files.
> **Outputs:** a notes table, a revision plan, a new version folder, crew briefs and their synthesis when used.
> **Next:** the module that owns each fix; then [render-qa.md](render-qa.md).

## Version discipline

- Every revision works in a **copy** (`v2/` from `v1/`); the approved version stays as the shippable backup. Never overwrite a version a reviewer called "closest".
- State the runtime and the changes at every version.
- When a revision changes the identity (a font, the palette), update the plan's identity section, not just a note at the end.
- Ship v1, collect the review, then refine. Do not over-polish bookends before the first review.

## Reading a note

| The reviewer says | It means | Do |
|---|---|---|
| "They're all ugly", "boring", "AI-looking" | the direction is wrong | stop; delete the branch; new direction (often: real UI, camera language, true morphs, beat-locked reveals; see the banned list in [design-system.md](design-system.md)) |
| "Good, but X is off" | an execution problem | the refinement loop below |
| "Pick B" | a choice | patch B and ship |
| "This moment is the best" | promote it | record its exact CSS and timing and make it a reusable template (a title card, a transition) |
| "It must explain the product" | missing narration or reads | add voiceover and captions; reads in narration order |
| "Feels like slides" | static holds, hard cuts from blank, one ease | match-cut bridges, a camera move in every scene, 5-7 eases, scenes overlapping 0.4-0.9 s |

## Notes table and surgical edits

One line per change, with a unit and a time range from the review copy's counters: `UNIT 01.5-03.8 s: change`, `UNIT f210-f240: change`, `JOIN A to B: change`. A note spanning two units becomes two notes; a note in a unit's first 0.45 s may really be about the join.

1. Locate the composition and the tweens active in that window.
2. Edit only that unit; keep its frame count, its locks, its signature and its edges free.
3. Check (zero errors); grab the noted frames plus the mid-transition frames around them and look.
4. Re-render the unit; confirm its frame count.
5. Rebuild and render the film; regenerate the review copy. Join-only changes need only the rebuild.
6. Notes on different units are independent: fix them in parallel, then rebuild once.

## Refinement loop (for "almost right")

1. **Triangulate:** restate the complaint as concrete CSS and quote the line causing it ("fat and blurry" = stacked 40 px and 80 px text-shadows, a gradient fill at 148 px, heavy weight with tight tracking).
2. **Diagnose from several angles in parallel** (brand and type; pacing and motion; copy if words are involved), each with the verbatim complaint, the source files and the brand context, returning numbered diagnoses and three to five alternatives.
3. **Build one preview board** (a single HTML page): a tile per variant labelled `A - CURRENT` and the likely best clearly marked, each with the exact parameters that differ; a reply format at the bottom (`words: F, wordmark: C, backdrop: B`). Six variants for small pairwise studies, three for direction swaps, never more than eight.
4. **Wait for the pick;** never render on speculation (a render costs minutes). Add two or three blend tiles if asked.
5. **Patch surgically** (a few values, one swapped gradient), re-render, check, ship; log the complaint, the fix and the files in a pattern table for next time.

## What a reviewer checks

- Exact frame counts and durations; check passed; no baked poster at joins.
- Stills at every reveal and mid-transition; joins at J-0.1, +0.12, +0.30, +0.6 s; a contact sheet every 2.5 s.
- Each on-screen word on its spoken word; nothing essential under the caption band.
- Loudness about -14 LUFS, true peak about -1.5 dBTP, no clipping, audio as long as picture.
- Typography crisp (single shadows, no blur on entry), captions large enough on a phone, content clear of overlays, the canvas used, real data only, the thumbnail readable small.

Frequent rejection reasons, worth checking before the first review: generic components and pill rows; a reference video's fonts copied; music with the wrong energy; screenshots instead of recreated UI; no dedicated visual per product; the same transition everywhere; no real morphs; narration and on-screen text fighting.

## Crew pre-production (large pieces)

Decide the spine first (story, proof point, length, platform), then brief three to five specialists in parallel, each with product facts, the spine, numbered asks, an output format and a word cap. Log their answers verbatim, resolve conflicts explicitly, and show the synthesis before building: skipping this step is the most expensive mistake on large pieces.

| Role | Standards | Asks | Cap |
|---|---|---|---|
| Content strategist | never static; movement every 2-3 s; hook in 1.5 s; CTA in the last 3 s | hook, per-scene duration, key visual, what moves, transitions, closing beat (vertical: the camera path) | 500 words |
| Copywriter (never skip) | every word earns its place | headline under 70 characters plus two variants; post body; 5 in-video lines under 55 characters (38 vertical); closing line under 40; narration under 50 words for a short | 400 words |
| Brand lead | hierarchy, two accents per scene at most, motion continuity | per-scene accents, density rules, three brand-breakers to pre-empt | 500 words |
| Growth lead (when there is a conversion goal) | distribution and loops | sharper hook, closing CTA, a loop built into the video, the distribution sequence, the pinned comment | 350 words |
| Optional | platform cuts, motion audit, UX copy, performance (first 3 s, drop-off) | as needed | |

For any reference video, run a visual analysis first (rhythm, entrance and transition grammar, camera, type emphasis, palette, five signature moves, what it avoids), timestamped, and borrow principles, never its fonts or assets.

## Gate

Every note is resolved or answered; the approved version is preserved; the new version passes [render-qa.md](render-qa.md); the plan reflects any identity change.
