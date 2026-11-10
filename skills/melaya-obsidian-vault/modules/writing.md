# Writing standards

> **Use when:** writing or rewriting any note from extracted material.
> **Inputs:** extracted facts with their citations ([extraction.md](extraction.md)); the note type, path and properties ([architecture.md](architecture.md), [properties.md](properties.md)); the voice for the language.
> **Outputs:** notes that answer in their first lines, cite every fact, mark unknowns, and log their changes.
> **Next:** [graph.md](graph.md), then [validation.md](validation.md).

## The shape of every note

1. Properties ([properties.md](properties.md)).
2. `# Title` matching the file name.
3. A lead of one to three sentences: what it is and why a reader is here.
4. `## At a glance`: 3 to 7 bullets that answer the note on their own. A reader (or an agent) who stops here is right.
5. `## Contents` when the note is over 8 KB: one `[[#Heading]]` per H2 (`scripts/add_contents.py`).
6. The sections of the type (templates in [../templates/notes/](../templates/notes/)).
7. `## Open questions` when anything is unknown or disputed.
8. `## Related`: the hub and at least three related notes.
9. `## Changelog` last, for notes that change over time (processes, references, decisions, projects).

## Facts with source and date

Every fact a reader could act on carries where it came from and when it was true:

- Inline: `Twelve pouches per box (product spec, Drive, 2026-10-01).`
- To a vault note: `See [[Pricing Facts#Plans]]` (the fact lives there, with its own source).
- To a heading in a source: `(Onboarding Guide, Confluence > People > Onboarding#First week, read 2026-11-03)`.
- To a URL: `([pricing page](https://example.com/pricing), read 2026-11-10)`.
- To a ticket, thread or recording: `(PROJ-142, 2026-05-20)`, `(sales channel, 2026-09-03)`, `(All-hands recording, 00:14:32)`.
- In tables: a Source column and an As of column.
- Collect every source in `source_of_truth` too.

Numbers keep units and their period (`2,400 orders per month, average of 2026-Q3`). Relative words ("recently", "soon", "most") are replaced by dates and numbers or removed.

## Never invent

- What no source says is not written as fact. It becomes a row under `## Open questions` (question, who could answer, why open) and `open_questions: true`.
- Disputed facts follow the conflict rule in [extraction.md](extraction.md).
- Inferences are labelled: `> [!info] Inference` with the reasoning and the facts it rests on.
- Quotes are verbatim, short, in a `> [!quote]` callout with the citation; paraphrase is the default.
- Never fill a template placeholder with plausible text. Leave it, or remove the section.

## Changelog lines

- In the note: `- 2026-11-10 ines: refill time updated to under one minute (product spec v3, 2026-11-05).`
- In `_Meta/Vault Changelog.md`: `- 2026-11-10 ines | [[Refill Kit]] | refill time updated (product spec v3)`.
- Bump `updated` (and `reviewed` when you re-checked the sources). Imports log one line per batch, not per note: `- 2026-11-10 import | Notion batch b003 | 25 read, 9 notes written, 2 skipped`.

## Voice and style

- Write for the reader in the charter, in the vault's primary language unless the note is a translation ([multilingual.md](multilingual.md)).
- Plain words, short sentences, active voice, present tense. Second person for processes ("Open the returns form").
- Concrete over vague: real names of screens, systems, roles, numbers.
- One idea per paragraph; lists for parallel items; tables for comparisons; numbered steps for sequences.
- No marketing superlatives, no filler ("It is important to note that"), no emojis.
- Configurable bans (`banned` in `vault-config.json`): em dashes and en-dash separators by default; semicolons and exclamation marks when the voice card says so.
- A per-language voice card (tone, address form, number and date formats, terms never translated) lives in `_Meta/` and is linked from the conventions.

## Chunk-friendly for agents

- Headings say what the section answers ("Refund rule for annual plans", not "Details").
- The first paragraph under each heading stands alone: an agent may read only that chunk.
- Repeat the subject in the section instead of "it" or "this" across headings.
- Short sections (under about 400 words) with stable headings and block ids on rules others cite.
- More in [agents.md](agents.md).

## Rewriting imported text

Imported pages are raw material, not notes. Keep the facts and the structure that helps; rewrite the prose into the note shape above; drop history that no longer applies (keep it in the Changelog or a superseded note); keep the original's URL in `source_of_truth`. Never paste a whole source page as a note body.

## Checklist before saving

- [ ] Lead and At a glance answer the note alone.
- [ ] Every fact has a source and a date; unknowns are open questions.
- [ ] First mentions link to their notes; the hub and three related notes are linked.
- [ ] No personal data or secret; zone properties right.
- [ ] `updated` bumped; Changelog line added where the note keeps one.
