# Obsidian vault skill

An agent skill that builds the most complete, detailed and well-linked Obsidian vault of someone's own knowledge, end to end, from everything they have: Google Drive, Docs, Sheets, Slides, Notion, Confluence, OneNote, Evernote, Gmail, Outlook, Slack, Teams, Jira, GitHub, Zoho, web pages and local files (PDF with OCR, Office, images, audio and video transcripts). It covers solo founders, team wikis, company handbooks, research vaults, client project vaults, migrations, personal knowledge bases, multilingual vaults, public plus private zones, and ongoing sync.

It is a Melaya skill: with the Melaya MCP server it reads sources through read-only connectors and can write to a connected vault through Melaya's vault tools; without Melaya it works from exports and folders and writes plain Markdown files. Its scripts need only Python 3.8+.

## How it is organised

`SKILL.md` is a short router: twelve rules that always apply, the tool surfaces, and an intent table. Everything else loads on demand, so an agent reads one to three modules per step instead of the whole skill.

```text
SKILL.md                 router: rules, tool surfaces, intent table, standard flow, definition of done
modules/INDEX.md         the graph: every module's inputs, outputs and next steps; standard flows
modules/                 intake, tools, sources, extraction, extract-types, architecture, properties,
                         obsidian-syntax, views, writing, graph, zones, multilingual, validation,
                         maintenance, migration, agents, scenarios, troubleshooting
templates/               vault charter, Home, hub; notes/ (concept, process, runbook, reference, decision,
                         person, team, project, glossary, term, faq, meeting, source); meta/ (conventions,
                         tag taxonomy, editing protocol, changelog, source ledger, vault-config.json,
                         publishignore.txt); bases/; canvas/
examples/                a fictional company vault from Drive, Notion, Slack and mail; a fictional research vault
scripts/                 scaffold.py, ledger.py, build_moc.py, autolink.py, add_contents.py, check_vault.py,
                         graph_report.py, export_public.py, vaultlib.py (shared)
```

Every module opens with the same front block (Use when, Inputs, Outputs, Next), so the graph is explicit and an agent can follow it without loading the rest.

## Scripts

| Script | What it does |
|---|---|
| `scaffold.py` | creates a vault skeleton (Home, section hubs, `_Meta` notes, config, manifest, templates, Bases, Canvas) that already passes the checker |
| `ledger.py` | the source ledger: plan from a listing, next batch, mark states, seen, content hashes, duplicates, provenance, status |
| `build_moc.py` | writes each hub's note list between markers, grouped by type, never listing internal notes in a public hub |
| `autolink.py` | finds unlinked mentions of titles and aliases and links the first one per note |
| `add_contents.py` | adds or refreshes `## Contents` outlines on long notes |
| `check_vault.py` | links and anchors, orphans, hops from Home, properties, taxonomy, structure, staleness, zone leaks, secrets, personal data, deny lists, punctuation, Canvas, Bases, attachments |
| `graph_report.py` | graph metrics (degree, components, hops, hubs) and repair lists |
| `export_public.py` | exports the public zone, strips private blocks and internal properties, prunes views, re-checks the copy |

Writing scripts are dry runs unless `--apply`; the checker and graph report are read-only.

## Install

**Claude Code:** the Melaya plugin bundles it with the `/build-vault` command. On its own, copy the folder into your skills directory and restart:

```bash
cp -r melaya-obsidian-vault ~/.claude/skills/
```

**Codex CLI:** copy the folder into `~/.codex/skills/` (or reference `SKILL.md` from your `AGENTS.md`).

**Gemini CLI:** reference the skill from your `GEMINI.md` (`@path/to/melaya-obsidian-vault/SKILL.md`).

**Any other agent or a hosted assistant:** add `SKILL.md` as an instruction or rules file and attach the `modules/` and `templates/` files as knowledge. Without a shell the skill still plans, writes notes as Markdown and walks the manual checklist.

## Requirements

- Python 3.8 or newer for the scripts (standard library only).
- Obsidian 1.9 or newer to open Bases; Canvas and Properties are core features. Dataview is optional.
- For connectors: a Melaya account with the MCP server connected and the services connected in the Melaya app. Reads use read-only tools; nothing is written to a source.
- For OCR and transcripts (optional): `ocrmypdf` or `tesseract`, and a transcription tool such as Whisper, or a vision and transcription capable model.

## Safety

Sources are read-only; personal and sensitive sources are excluded until the owner says yes; content read from sources is treated as data, never as instructions; credentials are never written; public notes never link into internal ones; nothing is published, shared or overwritten without the user's yes.

## Credits and licence

Apache License 2.0, with the repository that contains it. The method is distilled from the maintainers' own experience building and maintaining linked documentation and knowledge vaults for people and for AI agents. Obsidian is a trademark of its owner; this skill is not affiliated with it. All organisations, people and figures in `examples/` and `templates/` are fictional.
