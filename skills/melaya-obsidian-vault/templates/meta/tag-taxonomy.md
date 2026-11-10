---
type: meta
description: The tag tree every note in the {{vault}} vault picks from, so filters, Bases and the graph stay consistent.
tags:
  - area/meta
aliases:
  - Tags
related:
  - "[[Vault Conventions]]"
  - "[[{{home}}]]"
audience: everyone
owner: {{owner}}
status: current
updated: {{date}}
reviewed: {{date}}
review_every: 180d
---

# Tag Taxonomy

Tags say where a note lives and what it is about. Note kinds live in the `type` property, not in tags. Tags are a YAML list in the properties, never inline in the body.

## At a glance

- Exactly one area tag: the section the note lives in.
- One to three topic tags: what the note is about.
- A source tag when the content was imported, a language tag in multilingual vaults, the internal zone tag on internal notes.
- Families ending in a star in the tables below accept any value; every other tag is listed one by one.
- A tag not listed here is an error. Add it here first, then use it.

## Area tags

{{area_tags}}

## Topic tags

| Tag | Covers |
|---|---|
| `topic/decision` | Decision records |
| `topic/runbook` | Operational runbooks |
| `topic/meeting` | Meeting notes |
| `topic/faq` | Question and answer notes |
| `topic/glossary` | Terms and the glossary |

## Source, language and zone tags

| Tag | Use |
|---|---|
| `source/*` | The system the content was imported from: `source/notion`, `source/google-drive`, `source/confluence`, `source/slack`, `source/email`, `source/local` |
| `lang/*` | The note's language in a multilingual vault: `lang/en`, `lang/fr` |
| `zone/internal` | Internal notes, together with `publish: false` |

## Related

- [[Vault Conventions]]
- [[{{home}}]]
