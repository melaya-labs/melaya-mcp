# Properties and the tag taxonomy

> **Use when:** writing the frontmatter of any note, choosing or adding tags, or configuring what the checker requires.
> **Inputs:** the note type and zone ([architecture.md](architecture.md)); `_Meta/Tag Taxonomy.md`; `_Meta/vault-config.json`.
> **Outputs:** a valid properties block on every note; taxonomy and config kept in step.
> **Next:** [writing.md](writing.md).

## The schema

```yaml
---
type: concept                 # one value from the types list
description: One sentence, at most 200 characters, saying which question the note answers.
tags:                         # always a list, from the taxonomy only
  - area/product
  - topic/refill-kit
aliases:                      # other names readers search for
  - Kit
related:                      # quoted wikilinks
  - "[[Product]]"
  - "[[Refill Process]]"
audience: everyone            # everyone | team | internal | private (configurable)
owner: product-lead           # a role or person who keeps it true
status: current               # draft | current | stale | superseded | archived
source_of_truth:              # where the facts come from, with dates
  - "Product spec (Drive), read 2026-11-02"
  - "[[Pricing Facts]]"
updated: 2026-11-02           # last real change, YYYY-MM-DD
reviewed: 2026-11-02          # last time someone checked it is still true
review_every: 90d             # 14d, 6w, 3m, 1y
---
```

| Key | Required | Notes |
|---|---|---|
| `type`, `description`, `tags`, `updated` | every note | the checker's `required_properties` |
| `audience` | shared vaults | values in `audiences` |
| `owner`, `status`, `reviewed`, `review_every` | internal notes (and all notes in a team vault, if wanted) | `required_by_zone` |
| `source_of_truth` | notes whose facts come from elsewhere | list; system, document, URL or note, with date read |
| `aliases`, `related` | when useful | `related` duplicates key links for Bases and graph filters |
| `publish: false` | internal notes | with an internal `audience`; see [zones.md](zones.md) |
| `superseded_by` | when `status: superseded` | quoted wikilink to the replacement |
| `open_questions: true` | when the note has `## Open questions` | makes a review queue possible |
| `lang`, `translation_of` | multilingual vaults | [multilingual.md](multilingual.md) |
| type-specific | as the template shows | `decided` (decision), `phase`, `start`, `due` (project), `date`, `attendees` (meeting), `role`, `team` (person), `system`, `scope`, `last_read` (source) |

## Property rules (Obsidian and machine readers)

- One property name means one type across the vault: Obsidian stores the type per name (text, list, number, checkbox, date, date and time, tags). Never mix `updated: 2026-11-02` and `updated: last week`.
- Lists are YAML lists, even with one item. `tags` and `aliases` are always lists.
- Links inside properties are quoted: `"[[Note]]"`. Unquoted, YAML breaks.
- Dates are `YYYY-MM-DD`; date and time `YYYY-MM-DDTHH:MM`.
- No Markdown, no nested maps (Obsidian does not show them), no multi-line values except when unavoidable.
- Property names are lowercase snake_case and in the primary language, even in multilingual vaults.
- `description` is one sentence: it is what Bases, search results and agents show first.

## The tag taxonomy

Tags answer "where" and "about what"; properties answer "what kind", "who", "when". Keep the tree small and closed: the taxonomy note lists every allowed tag in backticks, and `check_vault.py` rejects anything else.

| Family | Count per note | Examples |
|---|---|---|
| `area/*` | exactly one | `area/product`, `area/people`, `area/reference`, `area/internal` |
| `topic/*` | one to three | `topic/refill-kit`, `topic/decision`, `topic/onboarding` |
| `source/*` | when imported | `source/notion`, `source/google-drive`, `source/slack` |
| `lang/*` | multilingual vaults | `lang/en`, `lang/fr` |
| `zone/internal` | internal notes | with `publish: false` |
| `level/*` (optional) | one | `level/beginner`, `level/advanced` for docs vaults |

Rules:
- Lowercase, hyphens, nested with `/`. No spaces, no plurals mixed with singulars (`topic/customer`, never also `topic/customers`).
- A family listed with a star (`source/*`) accepts any value; everything else is listed tag by tag.
- Tags live in the `tags` property, not inline in the body (inline tags are still read by the checker).
- New tag: add it to the taxonomy first, with a one-line meaning, then use it. Prefer an existing tag to a near-duplicate.
- About 20 to 60 topic tags is healthy for a few hundred notes. More means tags are doing the job of links or folders.

## Configuring the checker

`_Meta/vault-config.json` (created by `scripts/scaffold.py`, template [../templates/meta/vault-config.json](../templates/meta/vault-config.json)) sets: `home`, `max_hops`, `types`, `statuses`, `audiences`, `required_properties`, `required_by_zone`, `sections` (required H2 per type), `glance_bullets`, `description_max`, `size_budget_kb`, `taxonomy_note`, `tag_patterns` (regular expressions accepted besides the taxonomy), `banned` punctuation, `zones`, `pii`, `denylist`, `denylist_public`, `orphan_exempt`, `attachments_folder`, `attachment_max_mb`. Every key is optional; defaults are in `scripts/vaultlib.py`.
