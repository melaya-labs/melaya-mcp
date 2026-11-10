---
type: meta
description: How the {{vault}} vault is organised and written, which zone is public and which is internal, and the rules that keep the graph clean and safe to share.
tags:
  - area/meta
aliases:
  - Conventions
  - How this vault works
related:
  - "[[{{home}}]]"
  - "[[Tag Taxonomy]]"
  - "[[Editing Protocol]]"
  - "[[Vault Changelog]]"
audience: everyone
owner: {{owner}}
status: current
updated: {{date}}
reviewed: {{date}}
review_every: 180d
---

# Vault Conventions

The rules every person and agent follows when reading or writing this vault. The checker enforces most of them.

## At a glance

- Start at [[{{home}}]]. Every note is at most {{max_hops}} links away from it.
- One fact lives in one note. Other notes link to it instead of copying it.
- Every note starts with properties, a one-sentence `description`, a lead and `## At a glance`.
- Every fact carries a source and a date. Unknowns are open questions, never guesses.
- Internal notes never get a link from a public note. See [[#Zones]].

## Folder map

{{sections_table}}

Hubs (maps of content) are named after their section without the number. Link to them by that name.

## Note names

- Title Case, unique across the whole vault, no dates, emojis or version numbers (meetings and logs excepted: `2026-03-14 Pricing Review`).
- Never a bare `Overview`, `Index`, `Setup` or `FAQ`: qualify it (`Billing FAQ`).
- Search before creating. If the note exists, link or extend it.

## Properties

| Key | Required | Holds |
|---|---|---|
| `type` | yes | `moc`, `concept`, `process`, `reference`, `decision`, `person`, `team`, `project`, `glossary`, `term`, `faq`, `meeting`, `source`, `log`, `meta` |
| `description` | yes | One sentence, at most 200 characters: the question the note answers |
| `tags` | yes | A list, from [[Tag Taxonomy]] only |
| `updated` | yes | Date of the last real change, `YYYY-MM-DD` |
| `aliases` | when useful | Other names people search for |
| `related` | when useful | Quoted wikilinks: `"[[Note]]"` |
| `audience` | yes for shared vaults | Who it is written for |
| `owner` | internal notes | Who keeps it true |
| `status` | internal notes | `draft`, `current`, `stale`, `superseded`, `archived` |
| `source_of_truth` | when facts come from elsewhere | List of sources with dates |
| `reviewed`, `review_every` | internal notes | Last check, and how often (`30d`, `6w`, `3m`, `1y`) |
| `publish`, `superseded_by`, `open_questions` | when they apply | Zone flag, replacement note, open questions flag |

## Body

1. `# Title`, then a one to three sentence lead.
2. `## At a glance`: 3 to 7 bullets that answer the note on their own.
3. `## Contents` for notes over 8 KB, linking every H2.
4. The sections of the note type (see the templates in `_Templates/`).
5. `## Related`, then `## Changelog` last when the note keeps one.

## Links

- Every note links up to its hub and to at least three related notes.
- The first mention of a concept, person, project or term links to its note.
- Deep links point at headings or blocks: `[[Note#Heading]]`, `[[Note#^block-id]]`.
- Reuse a definition with an embed (`![[Term#^definition]]`) instead of rewriting it.
- Links inside properties are quoted. Never link to a note that does not exist.

## Zones

- Public notes may be shared outside the team. Internal notes carry `publish: false` and a non-public `audience`, and their paths are in `_Meta/.publishignore`.
- A public note never links to, embeds or lists an internal note. The only exception is [[{{home}}]], between `%% private:start %%` and `%% private:end %%`, which exports drop.
- Never write credentials, and never personal data about people outside the team.

## Style

- {{languages}}
- Plain words, short sentences, present tense, concrete numbers with their source and date.
- No em dashes, no marketing superlatives, no emojis.

## Checking

Run `python3 check_vault.py --vault .` (from the skill's scripts) after every editing session and fix every error.

## Related

- [[{{home}}]]
- [[Tag Taxonomy]]
- [[Editing Protocol]]
- [[Vault Changelog]]
