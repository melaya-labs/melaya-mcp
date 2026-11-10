# Maintenance: refresh, staleness, changelog, split and merge

> **Use when:** sources changed since the import, notes are due for review, the vault grew unevenly, or notes need splitting, merging, renaming or retiring.
> **Inputs:** the vault; the ledger; fresh listings from the sources; the review queue.
> **Outputs:** updated notes with Changelog lines, a refreshed ledger, a review pass, a refresh report.
> **Next:** [validation.md](validation.md).

## Incremental refresh from sources

1. Re-list each source as JSON Lines with revisions (same as [sources.md](sources.md)); for chats and mail, list only since the last read date.
2. `ledger.py plan --source S --listing new.jsonl --mark-gone` records new and changed items as pending and reports items gone from the source with the notes they fed.
3. Process pending items with the batch loop in [extraction.md](extraction.md). For a changed item, diff the new normalised text against the work copy, and update only the facts that changed, in their canonical notes.
4. For a gone item: check whether the source deleted, moved or restricted it (a permission change is not a deletion). If the knowledge is obsolete, mark the notes it fed `status: stale` or superseded; never delete silently.
5. One line per source in `_Meta/Vault Changelog.md`, the Source Ledger table refreshed (`ledger.py status --md`), `check_vault.py` at zero errors.

Cadence by source: wikis and docs monthly, tickets and chats weekly or monthly, mail by label on demand, websites quarterly. A Melaya pipeline can run the refresh on a schedule ([agents.md](agents.md)).

## Staleness and reviews

- `reviewed` + `review_every` passed and `status: current`: the checker warns; `Bases/Review Queue.base` lists them oldest first, by owner.
- Review: re-read the sources in `source_of_truth`. Still true: set `reviewed` to today. Changed: update, Changelog line. Unsure: `status: stale` plus an open question.
- Suggested `review_every`: prices, plans, people, projects 14 to 30 days; processes and references 90 days; concepts and decisions 180 to 365 days; meetings 365 days.
- A vault-wide review each quarter: stale notes, open questions, unused tags, weakly linked notes, attachments unused.

## The changelog

- `_Meta/Vault Changelog.md` (`type: log`) is append-only: `- YYYY-MM-DD who | [[Note]] | what changed (source)`.
- Each note with a `## Changelog` gets its own dated line; `updated` is never older than its newest line (the checker enforces).
- Imports and refreshes log per batch, not per note.

## Deduplicating notes

1. Find candidates: same or similar titles, shared aliases, `ledger.py dupes`, notes with the same `source_of_truth`, Obsidian's search for a key sentence.
2. Choose the survivor: the better-linked, better-sourced, correctly placed note.
3. Merge (below).

## Merging notes

1. Move the facts, with their citations, into the survivor; resolve conflicts with the rule in [extraction.md](extraction.md).
2. Add the retired note's name to the survivor's `aliases`.
3. Retire the other: `status: superseded`, `superseded_by: "[[Survivor]]"`, a `> [!warning] Superseded by [[Survivor]]` line under the title, body reduced to that pointer. Or, in a vault where history does not matter, rename it to the survivor in Obsidian (which merges links) and delete after a backlinks check.
4. Point links at the survivor (Obsidian's rename, `obsidian_rename`, or editing each backlink), rebuild hubs, run the checker.

## Splitting a note

1. Pick the cut: one question per note; a section linked from elsewhere more than the rest; different owners or review cycles.
2. Create the new note from its template with the moved sections, their citations and block ids.
3. In the original, replace the moved text with a one-line summary and a link (or an embed `![[New Note#Section]]` where readers need it inline).
4. Retarget links that pointed at the moved headings (`[[Old#Heading]]` to `[[New#Heading]]`): the checker lists the dead anchors.
5. Changelog lines in both notes.

## Renaming and moving

Rename in Obsidian, or with `obsidian_rename` / `obsidian_move`, which update every link. Never rename with find and replace across files. Keep the old name as an alias. Moving between folders needs no link change (links resolve by name) but rebuild the hubs.

## Growing sections

Past about 40 notes, add sub-hubs (a subfolder per feature, client or topic, each with a hub) and re-run `build_moc.py --all --recursive --apply`. Past about 10 sections, merge the thin ones; Home should fit on one screen.
