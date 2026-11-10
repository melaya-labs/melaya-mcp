# Multilingual adaptation

> **Use when:** making a piece in other languages: translating or transcreating the script and on-screen text, voicing it per language, fitting it to the locked picture, captioning each language, and delivering the set.
> **Inputs:** the approved source piece (captionless master, voice script with sentence start times, word timings verified), the voice card per language ([../templates/voice-card.md](../templates/voice-card.md)).
> **Outputs:** per language: script, voice takes, mix, SRT and VTT, a burned render; a delivery matrix; fit and back-check reports.
> **Next:** [audio.md](audio.md), [captions.md](captions.md), [render-qa.md](render-qa.md).

## The contract: the picture is locked

Never re-time the film per language. Each translated sentence plays over the scene that shows its source sentence. Build `SOURCE.json` with one entry per source sentence: the text, its global start, its spoken length and its slot (`max_seconds = next_start - start - 0.25`; the last sentence ends 1.2 s before the end). Leave slack in the source edit: slots with at least 13% more time than the source take absorb most text expansion.

## Translation or transcreation

- **One target sentence per source sentence,** same order of ideas, written as spoken narration, not as UI copy.
- **Transcreate** taglines, hooks and wordplay: keep their structure and rhythm, change the words. Never cut a tagline's rhythm to save time.
- Keep numbers, brand and product names, protocol terms (API, URL), code and placeholders. Use the product's own localised UI strings first, then its localisation files, then earlier scripts in that language.
- Same style bans as the source (no hype words; the brand's punctuation rules).
- One translator pass per language, in parallel, each reading that language's voice card; ask for a complete file early, then refine.

## Voice cards (one per language)

Each card fixes: the locale variant and why; the register (informal or formal address) and its exceptions (legal is usually formal); three or four tone adjectives in the target language; banned constructions; the brand-name rule (Latin script, untranslated); the jargon policy (an English allow-list, or local terms with a canonical table); the call-to-action verb form; number formatting; and seven to ten sample lines that prove the tone survives. Use the card as the translator's instructions, as the rubric of a reviewer or judge pass (score, hard-rule rejections, one-line rationale), and for a native review. Re-run a language after its card changes.

## Craft per language (planning defaults)

| Language | Register and CTA | Typography and length |
|---|---|---|
| French | `tu` for consumer and developer tools, `vous` for enterprise and legal; imperative CTAs ("Commence"); avoid "N'hesitez pas", "Decouvrez" | narrow no-break space before `! ? : ;` and inside guillemets; about +15-30% length |
| Spanish | neutral Latin American (`es-419`) for reach; `tu` and `ustedes`, never `vosotros`; buttons in the infinitive ("Empezar") | `.` as thousands separator; +15-30% |
| Portuguese | Brazilian neutral; `voce`; buttons in the infinitive ("Comecar") | +15-30% |
| German | `du` for consumer and developer, `Sie` for enterprise; infinitive buttons ("Jetzt starten"); prefer verbs to noun stacks | compounds run long (+20-35%): no fixed-width buttons, soft hyphens in headlines; decimal comma |
| Chinese (Simplified) | `ni` (not the honorific) in tech marketing; bare-verb CTAs; avoid corporate jargon | full-width punctuation, half-width spaces around Latin terms and numbers; measure words with counts; Traditional is a separate locale |
| Japanese | polite desu/masu forms by default | no spaces between words; break lines at phrase boundaries; katakana for loanwords; 13-16 characters per caption line |
| Russian | `ty` for playful builder tone, `vy` for legal; avoid bureaucratic passive | established Cyrillic tech loanwords; space as thousands separator |
| Hindi | `aap` even in marketing; Devanagari only; established loanwords over coinages | Indian digit grouping (lakh, crore) |
| Arabic, Hebrew | per brand | right-to-left layout and captions; numbers and Latin names stay left-to-right; mirror directional motion only when meaning depends on it |

Expansion is a planning number, not a promise: German and Romance languages often run 15-35% longer in characters; CJK uses 30-50% fewer characters but similar spoken time.

## Voice and fit loop

1. One take per sentence (local engines: [audio.md](audio.md); respell brand names in the target script in the `tts` field only; the caption keeps the Latin name).
2. A take longer than its slot is re-voiced faster in proportion, up to the language's ceiling (about 1.1x English, up to about 1.18x for other engines), three tries at most.
3. Place each take at its source sentence start. If one overruns the next start, delay the next to 0.12 s after it and record the shift; never let two voices overlap. A shift over 0.3 s is a translation problem: rewrite it.
4. For each over-budget sentence, a rewrite brief: source, current text, spoken seconds, slot, and the share of syllables to cut, `1 - 0.92 * slot / (seconds * speed / base_speed)`. Iterate until nothing is over by more than 0.3 s.
5. **Back-check:** transcribe each take and compare it with both the caption text and the respelled `tts` text (keep the better ratio). Review every sentence under 0.75; typical medians are 0.91-1.00. Real faults are misreads, drones and dead air; homophone spellings are not.
6. Cache each take with a fingerprint of its text, so a changed sentence is never shipped with old audio.
7. Gain-match the voice track to the source voice's integrated loudness; mix with the same music, SFX and duck chain.

Some engines have no punctuation in their vocabulary: voice each sentence whole (voicing comma pieces separately leaves 0.4-0.8 s gaps) and test wordings for trailing drones.

## Delivery matrix

| Asset | Per language | Spec |
|---|---|---|
| Captionless master video | no | the source-language mix, plus a video-only copy for adaptive streaming |
| Audio mix | yes | WAV (lossless source) and MP3 or AAC |
| `captions.<lang>.srt` and `.vtt` | yes | timed to that language's voice |
| Burned render `<slug>_<lang>.mp4` | yes | every cue burned, including taglines |
| Poster | no | text-free, or one per language when it carries words |
| `film.json` | no | duration, frames, chapters, languages with native names |

Order of work: source approved and word times verified; `SOURCE.json`; translation passes in parallel; per-language voice as each script lands; reports (over-budget, shifts, back-check) and the fix loop; captionless master once; caption band render or burn per language; one caption frame spot-checked per language; frame count equal to the source in every file.

## Gate

Every language has its card, script, takes that fit without overlaps, a back-check report, captions and a render with the source's frame count.
