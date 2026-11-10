# Multilingual vaults

> **Use when:** sources, readers or the published output use more than one language.
> **Inputs:** the charter's languages; source items in several languages.
> **Outputs:** one chosen layout, `lang` and `translation_of` properties, language tags, translation links, a voice card per language.
> **Next:** [writing.md](writing.md), [graph.md](graph.md).

## Pick a layout

| Layout | When | Shape |
|---|---|---|
| A. One language, others summarised | most readers share one language; sources are mixed | notes in the primary language; originals cited by URL; foreign terms as aliases |
| B. Parallel notes, same folders | a few key notes need full translations (handbook, policies) | `Refund Policy.md` and `Refund Policy (FR).md` side by side, linked both ways |
| C. Per-language trees | a full translated docs set, often published per language | `en/10 Product/...`, `fr/10 Produit/...`, one Home per language plus a language picker Home |
| D. Mixed by audience | regional teams write in their own language | notes in their author's language, hubs and properties in the primary language, summaries in the primary language at the top |

Default to A. Choose C only when every page is translated and published per language.

## Properties and tags

```yaml
lang: fr
translation_of: "[[Refund Policy]]"   # on every translation, pointing at the source-language note
translations:                          # on the source note, optional
  - "[[Refund Policy (FR)]]"
tags:
  - lang/fr
```

- Property names, tag names, types and statuses stay in the primary language in every note, so Bases, the checker and agents work across languages.
- Note names must stay unique vault-wide: suffix translations (`(FR)`) in layout B; in layout C, translated titles are usually unique already; when not, suffix.
- Aliases carry the other languages' names for the same thing, so search and `autolink.py` find it.

## Links across languages

- A translation links to its source note and to the translations of its neighbours, not to source-language neighbours, so a reader stays in one language.
- Each language's hub links its notes; Home (or a language picker Home) links each language's hub.
- The checker's hop rule applies per language tree: each language Home within three hops of the root Home.

## Translating

- Translate from the canonical source-language note, not from the original source document, so facts stay single.
- Keep numbers, dates, product names, code, UI labels in the form the reader sees in their product (often not translated).
- A glossary table per language (term, translation, never translate) lives in the Glossary or a voice card.
- After a source-language change, mark translations `status: stale` until updated; a Base view "translations older than their source" compares `updated`.
- Machine translation is a draft: a fluent reader reviews before `status: current`.

## Voice per language

A voice card per language in `_Meta/` (`Voice EN.md`, `Voice FR.md`): register (formal or informal address), sentence length, date and number formats, quotation marks, terms that stay in the primary language, punctuation bans. Link them from the conventions note. Agents writing in a language read its card first.

## Extraction from mixed-language sources

Keep each item's original language in the ledger (`lang` field in the listing) and cite originals in their language; write the note in the layout's language; quote short original passages with a translation when the wording matters (legal, policy).
