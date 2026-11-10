# Graph quality

> **Use when:** after each batch of notes, before a review or a handover, or when the graph looks like a hairball or a set of islands.
> **Inputs:** the vault; `scripts/graph_report.py` output; `scripts/check_vault.py` findings.
> **Outputs:** every note reachable from Home within three hops, no orphans, no dead links, hubs that list their notes, deliberate cross-links between sections, a glossary that links itself in.
> **Next:** [validation.md](validation.md).

A good vault graph is hub and spoke plus cross-links: Home to hubs, hubs to notes, notes to their neighbours across sections. Links are written for a reader's next question, not for density.

## Rules

| Rule | Why | Enforced by |
|---|---|---|
| Every note links up to its hub | a reader can always climb back | `graph_report.py` (missing up-link); templates put the hub in Related |
| Every hub lists every note in its folder | nothing is hidden | `build_moc.py` generated list, `graph_report.py` |
| Home links every hub | one entry point | scaffold, checker hops |
| Max 3 hops from Home | anything is found in three clicks, agents expand few hops | `check_vault.py` (configurable `max_hops`) |
| No orphans (nothing links in) | an orphan is invisible to browsing and to link-following agents | `check_vault.py` |
| No dead links or anchors | trust | `check_vault.py` |
| At least 3 related notes per note | context and cross-section paths | `graph_report.py` weakly linked |
| First mention links | the reader can jump at the point of need | `autolink.py` |
| Public never links to internal | zones | `check_vault.py` |

## Building the links deliberately

1. **Spine first:** Home, hubs, sub-hubs (scaffold, then `build_moc.py --all --apply` after every batch).
2. **Up-links:** each note's Related starts with its hub.
3. **Concept links:** the first mention of every concept, term, person, team, project and system links to its note. Run `autolink.py` (dry run, review, then `--apply`); add `--exclude` for common words used as titles.
4. **Cross-links:** for each note ask "what would the reader need next?": the process that uses this concept, the decision behind this rule, the team that owns this system, the project that changed it. Two to five such links per note.
5. **Deep links:** point at the heading or block that answers (`[[Returns Policy#Refund window]]`), not at the top of a long note.
6. **Backlinks review:** for each hub and key concept, open its backlinks (Obsidian's panel, `obsidian_backlinks`): unexpected sources reveal missing hubs; many unlinked mentions reveal missing links.
7. **Glossary:** one `term` note per term that needs more than a line, a `Glossary` note with every term in a table, and aliases on each term (abbreviations, plurals, other languages) so `autolink.py` catches them.

## Generating hubs

`build_moc.py --moc "20 Product/Product.md"` (or `--all`) writes the list between `%% moc:start %%` and `%% moc:end %%`: one line per note with its description, grouped by type, sub-hubs first, `order` property respected. Hand-written text around the markers (lead, Start here, editorial grouping) is kept. A public hub never lists internal notes. Re-run after every batch; it is idempotent.

## Metrics to watch

`python3 scripts/graph_report.py --vault V` prints:

| Metric | Healthy |
|---|---|
| Links per note (average out-degree) | 4 to 12 |
| Components | 1 (one connected graph) |
| Hops from Home | most notes at 1 or 2, none over 3 |
| Orphans, dead ends, unresolved links | 0 |
| Weakly linked (fewer than 3 links in and out) | under about 10 percent, all leaves like terms or meetings |
| Notes missing an up-link, hubs missing a note | 0 |
| Sections that never link to each other | few; each pair is a question (should Product link to Customers?) |
| Top hubs by inbound links | the hubs and core concepts, not a random note |

Use `--json` to compare runs and `--md` to save the report outside the vault (or in `_Meta/` as an internal note).

## Fixing

| Finding | Fix |
|---|---|
| Orphan | add it to its hub (`build_moc.py`) and link it from 2 notes that mention its subject; if nothing should link to it, it may not belong |
| Over 3 hops | link it from its section hub or a sub-hub that Home reaches; add a sub-hub when a section is deep |
| Dead link | create the note (if in scope and sourced), fix the name, or remove the link |
| Dead anchor | the heading was renamed: update the link to the new heading or add a block id |
| Ambiguous link (two notes, one name) | rename one note (in Obsidian or `obsidian_rename`, which updates links); never find-and-replace |
| Dead end (links to nothing) | add Related with the hub and neighbours |
| Hairball (a note with 100+ links) | it is a hub in disguise: turn it into a hub, or split it |
| Islands (components over 1) | link each island's hub from Home or from the hub it belongs under |

Run [validation.md](validation.md) after every fix round.
