# Extraction: batches, ledger, paging, dedupe and conflicts

> **Use when:** reading content out of the sources, resuming an interrupted import, or refreshing from sources.
> **Inputs:** the approved inventory; the ledger at `_Meta/sources/ledger.jsonl` with pending items ([sources.md](sources.md)).
> **Outputs:** per batch, normalised text in a work folder outside the vault, ledger records (read, written, skipped, duplicate, failed), and the facts and notes for [writing.md](writing.md).
> **Next:** [extract-types.md](extract-types.md) for the source type, then [architecture.md](architecture.md) and [writing.md](writing.md).

## The batch loop

1. `python3 scripts/ledger.py next --vault V --source S --batch 25` prints the next pending items.
2. For each item: read it fully (all pages), normalise to Markdown text, save to `work/<source>/<id>.md` outside the vault, and hash it: `ledger.py mark --source S --id ID --state read --rev REV --text-file work/S/ID.md`.
3. Extract: facts with their location, decisions, definitions, procedures, people and roles, dates, links to other items. Keep the item's URL and heading path for citations.
4. Write or update notes ([writing.md](writing.md)), then `ledger.py mark ... --state written --notes "path/a.md,path/b.md"`. Items with nothing to keep get `--state skipped --reason "..."`.
5. After the batch: `scripts/build_moc.py --all --apply`, `scripts/check_vault.py`, one line in `_Meta/Vault Changelog.md`, and a progress line to the user ("Notion: 75 of 210 read, 31 notes written, 4 skipped, 0 failed").

An interrupted run resumes with `ledger.py next`: written items are never re-read; `read` items are re-processed from the work folder without calling the source again.

## The ledger record

| Field | Holds |
|---|---|
| `source`, `id` | the system and its stable id (page id, file id, thread id, issue key, path) |
| `title`, `url` | for citations and for people |
| `rev` | revision, version number, etag or modified time: what decides "changed" on refresh |
| `hash` | `sha256` of the whitespace-normalised text, for duplicates across sources |
| `state` | pending, read, written, skipped, duplicate, failed, gone |
| `notes` | the vault notes this item fed (provenance; `ledger.py where --note`) |
| `reason`, `batch` | why skipped or failed; which batch |

The ledger stays in the internal zone (it lists source titles). Its human view is `_Meta/Source Ledger.md`, refreshed with `ledger.py status --md`.

## Paging and rate limits

- Always follow cursors to the end (`cursor`, `next_page_token`, `offset`, `page_token`, `start`); a first page is not the source.
- Long bodies come in windows (`offset` and `max_chars`, or a cursor): read until the reply says there is no more.
- On a rate-limit or 429 reply: wait, then retry with backoff (2 s, 4 s, 8 s, up to 60 s), at most 5 tries, then mark `failed` with the reason and continue. Never hammer.
- Spread large sources across sessions; the ledger makes that safe.
- Prefer one export call over many small reads when the source offers it (a Drive export of a Doc to text, a Confluence space export, a Notion workspace export).

## Normalisation

- Convert to Markdown: headings kept, tables as Markdown tables (or CSV attachments when wider than about 8 columns), lists, links rewritten to their final form later.
- Remove boilerplate: navigation, footers, signatures, quoted reply chains in mail, "Sent from my phone", tracking links.
- Keep dates absolute (`2026-03-14`), never "yesterday".
- Keep the original language; translation happens at writing time ([multilingual.md](multilingual.md)).
- Redact on the way in: secrets and personal data never reach the work folder in clear when avoidable ([zones.md](zones.md)).

## Duplicates

Detect at three levels:

| Level | How | Action |
|---|---|---|
| Same content | `ledger.py dupes` (equal normalised hash) | keep the canonical copy (curated system, newest, owner's), mark others `duplicate` |
| Near copy | same title or first heading, or most of the text equal | read both; merge into one note; cite both sources |
| Same fact | one value stated in several items | one canonical note holds it; see conflicts |

## Conflicts between sources

1. Same fact, different values: keep the newest dated value that cites a primary source (the system of record beats a slide; a signed decision beats a chat message; a later version beats an earlier one).
2. Write the value with its source and date; mention the other value in the note's Changelog line or a `> [!note] Conflicting sources` callout with both citations.
3. Equal dates, no primary source, or a contradiction that matters: write neither as fact. Add a row under `## Open questions` (question, owner, why open), set `open_questions: true`, and report it.
4. Never average, never pick silently, never resolve by guessing.

## Failure handling

- A source that returns nothing is an error, not an empty success: report it, keep its items pending.
- A lost permission mid-run: stop that source, keep its ledger records, tell the owner. Never treat lost access as deletion.
- A file that cannot be parsed (encrypted PDF, corrupt export): `failed` with the reason; list it in the report.
