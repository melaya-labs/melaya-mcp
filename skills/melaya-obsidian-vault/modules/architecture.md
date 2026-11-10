# Information architecture

> **Use when:** deciding the folders, hubs and note types of a vault, where a new note goes, whether to split or merge, how to name it, and where files live.
> **Inputs:** the charter; the inventory; candidate notes from extraction.
> **Outputs:** the section list (for `scripts/scaffold.py --sections`), hub notes, a note type per note, its path and name, the attachments policy.
> **Next:** [properties.md](properties.md), then [writing.md](writing.md).

## Numbered top-level sections

Use 5 to 10 numbered folders so the file tree reads in order and every hub has a home. Leave gaps of 10 for later sections.

| Vault | Typical sections |
|---|---|
| Company or founder | 00 Home, 10 Company, 20 Product, 30 Customers and Market, 40 Sales and Marketing, 50 Operations, 60 People, 70 Finance and Legal (internal), 90 Reference |
| Team wiki | 00 Home, 10 Team, 20 Projects, 30 Processes, 40 Systems, 50 Decisions, 90 Reference |
| Handbook | 00 Home, 10 About Us, 20 How We Work, 30 Policies, 40 Benefits and Tools, 50 Onboarding, 90 Reference |
| Research | 00 Home, 10 Questions, 20 Concepts, 30 Literature, 40 Methods, 50 Data, 60 Findings, 70 Writing, 90 Reference |
| Client project | 00 Home, 10 Client, 20 Scope and Contract (internal), 30 Deliverables, 40 Meetings, 50 Decisions, 60 Risks, 90 Reference |
| Personal | 00 Home, 10 Areas, 20 Projects, 30 Resources, 40 Journal, 90 Reference |

Plus `_Meta/` (charter, conventions, taxonomy, protocol, changelog, ledger), `_Templates/`, `Bases/`, `Canvas/`, `Attachments/`.

## Hubs (maps of content)

- Home (`00 Home.md`) links every section hub, the views and the rules; internal links only inside the private strip markers ([zones.md](zones.md)).
- One hub per section, named like the section without its number (`20 Product/Product.md`). It links every note in the section, grouped by type, with the generated list from `scripts/build_moc.py`, plus a hand-written "Start here".
- Sub-hubs when a section passes about 40 notes: one subfolder per feature, client, project or topic, each with a hub named after it.
- Hubs carry `type: moc` and stay short: a lead, At a glance, Start here, the list, Related.

## Note types

| Type | Holds | Sections beyond the defaults |
|---|---|---|
| `concept` | what something is and why it matters | How it works, Examples |
| `process` (and runbooks) | how to do a job, step by step | Before you start, Steps, Troubleshooting, Rollback (runbooks) |
| `reference` | canonical facts, settings, lists, fact sheets | Facts (table with source and date) |
| `decision` | one decision record | Context, Options considered, Decision, Consequences |
| `person`, `team` | roles, ownership, who to ask (work facts only) | Responsibilities, Members, Owns |
| `project` | goal, scope, milestones, status | Scope, Milestones, Decisions, Open questions |
| `glossary`, `term` | the shared vocabulary; one term per note when it needs explaining | Terms (glossary) |
| `faq` | questions as people ask them | Questions (folded callouts) |
| `meeting` | one meeting | Notes, Decisions, Actions |
| `source` | one source system and what was taken | What was taken, What was left out |
| `moc`, `log`, `meta` | hubs, the changelog, rules about the vault | |

Templates for each: [../templates/notes/](../templates/notes/). Research vaults add `literature` (one source, its claims and your reading) and `claim` or `finding` (one atomic statement with its evidence); add them to `types` in `_Meta/vault-config.json`.

## Atomic or long

- **Atomic** (one idea, 100 to 600 words): concepts, terms, decisions, claims. Easy to link, easy to cite, easy to keep current.
- **Long** (a guide, a handbook chapter, a runbook): fine when readers follow it top to bottom; over 8 KB it gets `## Contents` (`scripts/add_contents.py`), and its parts get stable headings and block ids so other notes can deep-link.
- Split when a note answers two questions, when one section is linked from elsewhere far more than the rest, or when two owners edit different halves. Merge when several notes are stubs on one subject or always read together. Procedure: [maintenance.md](maintenance.md).

## Naming

- Title Case, the words people search for, unique across the whole vault (wikilinks resolve by name).
- No bare `Overview`, `Index`, `Setup`, `FAQ`, `Notes`: qualify (`Billing FAQ`, `CRM Setup`).
- No dates, versions or emojis in names, except dated kinds: meetings and logs as `YYYY-MM-DD Subject`.
- Prefix internal notes with their area when names would clash (`Ops Escalation Policy`).
- Other names go in `aliases`; never create a near-duplicate note for a synonym.
- Avoid characters Obsidian links handle badly: `# ^ [ ] | \ :` and leading dots.

## Attachments policy

- One `Attachments/` folder (or `Attachments/<section>/` past a few hundred files), set as Obsidian's attachment folder.
- Import a file only when a note embeds or links it. Otherwise link to it in its source system.
- Prefer text over files: a table over a screenshot of a table, Mermaid over a diagram image.
- Names: `<note-name> - <what>.png`, lowercase extensions, no spaces at the ends.
- Size: images resized to at most about 2000 px wide; files over 20 MB stay in their source; video and audio are linked, not stored.
- Personal photos, scans of ids and signed contracts never go into a shared vault.
- The checker reports unused attachments, files outside the folder and oversized files.

## Placing a new note

1. Search the vault for the subject and its synonyms. Extend an existing note when it covers the subject.
2. Pick the type, then the section whose hub a reader would open first.
3. Name it, copy the template, fill the properties ([properties.md](properties.md)).
4. Link it up to its hub (the generated list does this on the next `build_moc.py`) and to three related notes.
