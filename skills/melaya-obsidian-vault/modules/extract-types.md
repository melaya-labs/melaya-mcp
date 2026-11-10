# Extraction by source type

> **Use when:** you are about to read one kind of source and need the recipe: what to read, what to keep, what it becomes in the vault.
> **Inputs:** a batch of ledger items of one type ([extraction.md](extraction.md)).
> **Outputs:** normalised text per item and a list of candidate notes (type, title, facts with citations).
> **Next:** [architecture.md](architecture.md) to place the notes, [writing.md](writing.md) to write them.

Every recipe keeps the same three things: the text, where each fact came from (URL or path#heading), and the date the fact was true.

## Documents and wikis (Docs, Word, Notion pages, Confluence pages, OneNote, Markdown)

- Read the whole body (all windows), the title chain (parents or ancestors), labels or tags, last editor role and modified date, comments only when they hold decisions.
- Keep the heading structure: it becomes the note's sections and the citation anchors.
- One page usually becomes one note; split a page that covers several subjects; merge many thin pages on one subject ([architecture.md](architecture.md)).
- Page trees and databases become folders or hubs; database properties become note properties.
- Embedded files and images: list them; import only those a note needs ([architecture.md](architecture.md), attachments policy).

## Mail threads (Gmail, Outlook, Zoho Mail)

- Read whole threads, oldest first; drop quoted replies and signatures.
- Keep: decisions ("we agreed", "approved"), commitments with dates, facts (prices, volumes, terms), answers to recurring questions.
- Mail becomes decision records, facts in reference notes, FAQ entries and meeting-like summaries, almost never one note per thread.
- People outside the team appear as roles and organisations; no addresses or phone numbers.
- Attachments: treat as documents, with the thread as their citation context.

## Chats (Slack, Teams, Discord)

- Read public channels in scope, pinned items and threads first; a date range; skip join messages and bots unless they post facts.
- Keep: decisions, how-to answers that recur, links to canonical documents, incident timelines.
- Chats become FAQ entries, decisions, runbook steps and glossary terms. Cite as `channel, date` (and a permalink when the tool gives one).
- Private channels and DMs only with the owner's explicit yes, and then summarised, never pasted.

## Tickets (Jira, Linear, GitHub issues)

- Query with filters (JQL or labels), not one by one: epics, decisions, known issues, resolved incidents with a root cause.
- Keep: the problem, the decision or fix, the date, the key (as citation).
- Tickets become decision records, known-issue entries in a troubleshooting note, project milestones. Status that changes daily stays in the tracker; link it.

## Repositories (GitHub, GitLab, local code)

- Read README, docs folders, architecture decision records, CHANGELOG, CONTRIBUTING, runbooks and config documentation, not source code line by line.
- Keep: what each component does, how to run and deploy (as processes), decisions (ADRs map one to one to decision records), glossary terms.
- Cite as `repo/path#heading @ ref`. Never copy secrets, `.env` values, keys or internal hostnames.

## Spreadsheets (Sheets, Excel, CSV)

- Read the tab list, then each tab's header row and a sample before reading all rows; record the range read.
- Small reference tables (under about 50 rows and 8 columns) become Markdown tables in a reference note.
- Large or changing data stays in the sheet: the note describes it (columns, meaning, owner, refresh) and links to it, or a CSV goes to attachments with a Base or Dataview view when the vault must hold it.
- Personal-data columns (emails, phones, addresses, ids) are never imported.

## Slides (Google Slides, PowerPoint, Keynote exports)

- Read slide text and speaker notes slide by slide; tables included.
- Decks are summaries: extract the claims with the slide number as citation (`Deck name, slide 7, 2026-03-02`), and check each claim against a primary source before it becomes a fact.

## PDFs and scanned documents

- Text PDFs: extract text with page numbers; cite `file.pdf p. 12`.
- Scanned PDFs and images of text: OCR first (Tesseract `ocrmypdf` or `tesseract`, a vision-capable model, or the platform's OCR), then proofread numbers and names against the image. Mark OCR-derived facts `(OCR, verify)` until checked.
- Forms and invoices: keep only the fields the charter needs.

## Images and diagrams

- Describe what the image shows in the note (alt text and a sentence), keep the file in attachments only when a note embeds it.
- Diagrams that matter are redrawn as Mermaid or Canvas so they are searchable and editable ([obsidian-syntax.md](obsidian-syntax.md), [views.md](views.md)).

## Audio and video

- Use an existing transcript when the platform has one; otherwise transcribe (Whisper or the platform's transcription), keeping timestamps.
- Keep: decisions, explanations, answers; cite as `Recording name, 00:14:32`.
- Meetings become meeting notes (template [../templates/notes/meeting.md](../templates/notes/meeting.md)) with Decisions and Actions; lectures and talks become literature or concept notes.
- Recordings of people need the owner's yes; never store raw recordings of third parties in a shared vault.

## Web pages

- Only pages in the charter's scope (the user's own site, public docs, sources they named). Respect robots and terms; no logins.
- Extract the main content (drop navigation), keep the canonical URL and the date read: `(example.com/pricing, read 2026-11-10)`.
- Web clippings become literature notes (research) or reference notes; quote briefly, summarise the rest.

## Exports and dumps

Notion, Confluence, Evernote, OneNote and Drive exports are covered step by step in [migration.md](migration.md).
