# Source inventory, permissions and personal data

> **Use when:** the charter is agreed and you need the full list of sources before reading any content, or a new source is added later.
> **Inputs:** the charter; connected services ([tools.md](tools.md)); folders or exports the user provides.
> **Outputs:** the Sources table in `_Meta/Source Ledger.md`, one `type: source` note per large source (template [../templates/notes/source.md](../templates/notes/source.md)), a listing file per source for `ledger.py plan`, and the owner's yes per sensitive source.
> **Next:** [extraction.md](extraction.md).

Inventory first, content second. Listing is cheap and reveals scope, sensitivity and size before a single document is read.

## 1. Enumerate every source

Walk every place knowledge lives, not only the one the user named. Ask once: "Anything else: shared drives, old wikis, a personal folder, a mailbox label, a Slack channel, a repository README?"

| Family | Enumerate with | List entry |
|---|---|---|
| Drive or shared drives | search by folder, then by type (Docs, Sheets, Slides, PDF, Office) | id, title, type, folder path, modified, owner role, size |
| Notion | search pages and databases the integration was granted | id, title, parent, last edited, database or page |
| Confluence | spaces, then the page tree per space | id, title, ancestors, version, labels, attachments count |
| OneNote, Evernote | notebooks, sections, pages (or the export file) | id, title, section, modified |
| Mail | labels or folders and a date range, as a thread list | thread id, subject, participants count, date range, attachment names |
| Chat | channels (public first), date range, pinned items | channel id, name, message count estimate, member count |
| Tickets | projects and a JQL or filter; issue types | key, type, status, updated, links |
| Repositories | repos, then docs paths (README, docs/, ADRs, CHANGELOG, wiki) | repo, path, ref, size |
| Local folders and exports | a file tree | path, extension, size, modified |
| Web | sitemap or a page list the user approves | URL, title, last modified |
| Media | recordings with or without transcripts | file, duration, language, transcript available |

Write each listing as JSON Lines (`{"id", "title", "rev" or "modified", "url" or "path", ...}`) and record it with `scripts/ledger.py plan --source <name> --listing <file>`. The ledger then knows what exists before anything is read.

## 2. Check permission and scope

- Read only what the connector or export already allows. A 403, a missing space or a private channel is reported, not worked around.
- Confirm the account: one read-only call per service that returns the account or workspace name, shown to the user in one line.
- Note the permission owner per source (who could revoke it) in its source note.
- Scope down to the charter: date ranges for mail and chat, specific spaces and folders, issue types.

## 3. Triage sensitivity before reading

Mark every source and every sub-scope with one level. Ask the owner for anything above "internal".

| Level | Examples | Default handling |
|---|---|---|
| public | published docs, website, public repos | import, public zone allowed |
| internal | team wikis, project docs, public channels, tickets | import, internal zone |
| confidential | contracts, pricing internals, client deliverables under NDA, board material | only with a yes; internal zone, summary over copy, no attachments by default |
| personal | mailboxes, DMs, HR, health, payroll, performance reviews, personal journals | excluded unless the owner asks, and then a private vault |
| secret | credential stores, `.env` files, key files, password exports | never imported |

Signals that a folder needs a second look: names like HR, payroll, legal, contracts, personal, private, salaries, medical, passwords, keys, backup; spreadsheets with columns like email, phone, address, date of birth, IBAN; mail threads with external personal addresses.

## 4. Personal data rules

- **Minimise.** Keep roles over names for people outside the team ("the supplier's account manager"). Team members may be named by role and name in internal notes when the owner agrees.
- **Never copy** personal contact details, government ids, bank or card numbers, health data, home addresses or private messages into the vault. Link to the system of record instead.
- **Customers and third parties** appear as organisations, not as individuals, unless the vault is a CRM-like internal vault the owner asked for.
- **Record exclusions**: every excluded source or pattern gets a row in the Source Ledger's Excluded table with the reason.
- The checker flags emails, phone numbers, IBANs, card numbers, national id patterns, IP addresses and credential-like strings; add organisation-specific terms (client code names, project names under NDA) to `denylist` or `denylist_public` in `_Meta/vault-config.json`.

## 5. Size and order

Sum the counts per source and pick an order: the canonical, curated sources first (handbook, wiki, specs), then working documents, then tickets, then mail and chat (which mostly confirm, date and add decisions). Big sources go in batches of about 25 items. Put the plan in the Source Ledger's At a glance: sources, counts, order, expected notes.

## 6. Present the inventory

Show the owner a table: source, scope, item count, sensitivity, proposed handling. Get a yes (or edits) before extraction. Record the answer in the charter's Sources table.
