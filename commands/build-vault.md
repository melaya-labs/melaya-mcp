---
description: Build, extend, migrate or refresh an Obsidian vault of your knowledge from your documents, wikis, mail, chats, tickets and files, end to end
---

Build the Obsidian vault the user describes, using the `melaya-obsidian-vault` skill.

1. Load the skill's `SKILL.md`, follow its rules, and open only the modules the task needs.
2. Detect the tools on this host (`modules/tools.md`): the Melaya connectors and vault tools if present, a shell and Python for the scripts, or chat-only mode.
3. Write the vault charter first (`modules/intake.md`): ask at most three questions, state the defaults you took, and get the user's yes before reading any source.
4. Inventory every source with its sensitivity (`modules/sources.md`) and get a yes for anything personal or confidential. Sources are read-only.
5. Follow the scenario's path from `modules/scenarios.md`: skeleton, then batches of about 25 items with the ledger, notes with sources and dates, hubs and links, and `check_vault.py` at zero errors after each batch.
6. Finish with the report from `modules/scenarios.md` (notes, sources, checker result, open questions, exclusions, how to refresh). Never publish, share, push or overwrite existing notes without the user's explicit yes.

If the user gave input with the command (a vault path, sources, a scenario, languages, a public zone), use it as the charter's starting point: $ARGUMENTS
