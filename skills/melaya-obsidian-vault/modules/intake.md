# Intake and the vault charter

> **Use when:** a vault is about to be built, extended or migrated and its purpose, readers, zones, languages or sources are not written down yet.
> **Inputs:** the user's request; any existing vault; the list of tools available ([tools.md](tools.md)).
> **Outputs:** `_Meta/Vault Charter.md` from [../templates/vault-charter.md](../templates/vault-charter.md), with test questions, zones, languages, sources in scope and the defaults taken.
> **Next:** [sources.md](sources.md) to inventory the sources, then `scripts/scaffold.py` and [architecture.md](architecture.md).

The charter is the contract every later step is checked against. One page. It says what the vault must let a reader (or an agent) answer, not how notes are formatted.

## Ask little, default the rest

Ask at most three questions, only those whose answer changes the build. State every default in the charter; people correct defaults faster than they fill questionnaires.

| Decision | Ask when | Default |
|---|---|---|
| Purpose and readers | always unless obvious | the owner and their team; agents as a second reader |
| Scenario | it is ambiguous | from the request: see the table below |
| Zones | anything may be shared outside the team | one vault, everything `internal`; a public zone only when asked |
| Personal or sensitive sources (mail, DMs, HR, finance, legal, health) | they would be read | excluded until the owner says yes, per source |
| Languages | sources mix languages or readers do | the language most sources use; others summarised in it, originals linked |
| Existing vault | one exists | adopt its conventions; add, never restructure without a yes |
| Refresh | the sources keep changing | one import now, then a monthly refresh with the ledger |
| Size | always estimate, never ask | see "Estimate the size" |

## Recognise the scenario

| The request sounds like | Scenario in [scenarios.md](scenarios.md) |
|---|---|
| "Everything I know about my startup in one place" | Solo founder |
| "Our team wiki is a mess", "one place for the team" | Team wiki |
| "Employee handbook", "how we work", policies | Company handbook |
| Papers, notes, highlights, a thesis, a literature review | Research vault |
| One customer engagement, a deal room, a client delivery | Client project vault |
| "Move us off Notion / Confluence / Drive / OneNote / Evernote" | Migration |
| Journals, reading notes, life admin, second brain | Personal knowledge base |
| Teams in several languages, docs in several languages | Multilingual |
| A public docs site plus internal notes | Public and private zones |
| "Keep it in sync", "refresh weekly" | Ongoing sync (added to any scenario) |

## Test questions

Write 5 to 15 questions the vault must answer, phrased the way readers ask them ("What is our refund rule for annual plans?", "Who approves a new supplier?", "Which papers measured the effect in winter?"). They are the acceptance test: at the end, answer each from the vault alone, with a citation. A question no source can answer stays in the charter as an open question and is reported, never filled in.

## Zones

| Zone | Who reads | Mechanism |
|---|---|---|
| public | anyone, including outside the organisation | default zone of an export; checked for leaks |
| internal | the team or company | `publish: false`, internal `audience`, path in `_Meta/.publishignore` |
| private | the owner only | a separate vault; never mixed with shared notes |

Rule of thumb: if a leak of a note would harm a person or break a promise (HR files, health, legal disputes, client contracts under NDA, credentials), it does not belong in a shared vault at all. Put it in a private vault or leave it in its source. Details: [zones.md](zones.md).

## Languages

Pick one primary language for structure (hub names, properties, tags). Decide per other language: translate, summarise with a link to the original, or keep originals in a per-language folder. Details: [multilingual.md](multilingual.md).

## Estimate the size

Count the sources first ([sources.md](sources.md)), then estimate. Typical ratios after consolidation: wiki and doc pages map one to one or several to one (0.5 to 1 note per page); mail and chat produce few notes (decisions, facts, FAQs: about 1 note per 20 to 50 threads); tickets give decision records and known issues, not one note per ticket; papers give one literature note each plus concept notes. Plan about 25 items per batch and report after each.

## Existing vault

Read before planning: its top folders, Home or index notes, a conventions note if any, tags and property names in use (`obsidian_overview`, `obsidian_tags`, `obsidian_properties` through the vault tools, or a file listing and a quick `scripts/graph_report.py` on a copy). Record in the charter what you keep (names, folders, tags) and what you add. Run `scripts/check_vault.py` once to get a baseline before changing anything.

## Write the charter

Copy [../templates/vault-charter.md](../templates/vault-charter.md) to `_Meta/Vault Charter.md` (or let `scripts/scaffold.py` create it), fill every table, and list the defaults taken. Show it to the owner and get a yes before reading any source.
