---
name: ceo-company-knowledge-vault
description: Guides the owner, working with their own local AI assistant, to build an Obsidian company vault and attach it to the team so every executive indexes it. It covers the founder interview, gathering existing documents, the folder structure, note conventions, privacy, sync, then attach and verify. Use when the team has no knowledge vault bound (propose it first), when company knowledge is scattered or lives only in the founder's head, or when someone asks to "set up the knowledge base".
version: 2.0.0
---

# Build your company knowledge vault

Executives can only act on what they can read. Without a company vault, every brief rests on guesses. When no vault is bound, propose this before any other plan.

## Look up first

- Whether a vault is bound: run `excom_knowledge_search` for a company hub, products, pricing and team. If none of them comes back, start at step 1. The owner can list the bound sources with `melaya_excom_knowledge_read` (action sources).
- Which apps hold existing documents (Drive, Notion, mail): your granted connectors. Ask the owner which folders may be read.

## Steps

1. Propose the task "Build the company knowledge vault" for the owner with `excom_propose_task`, and say why: every executive works better once it exists.
2. Draft the brief for the owner's local assistant (Claude Code or similar) with `excom_save_draft`. It holds steps 3 to 8 and the two reference files. The owner pastes it in. The assistant works on the owner's computer, not through EXCOM.
3. Interview the founder, one question at a time. Each answer becomes a note. Cover: what the company sells and to whom, the plans and prices, the outcomes for the next horizon and how each is measured (with exact definitions), the team and who owns what, the customer channels, partners and suppliers, the systems in use, what always needs the founder, open decisions, and known risks.
4. Gather only the documents the founder names. Extract facts into notes with their source and date, link the originals, and summarise rather than copy.
5. Create the folders and notes per references/vault-structure.md, and apply the conventions in references/note-conventions.md: one fact per note, owners, review dates, links.
6. Keep private things out. Never write passwords, keys, tokens, bank details, personal data of customers or staff, or material under NDA. If the vault also holds public notes, put internal notes in one folder marked publish: false, exclude that folder from publishing, and never link into it from public notes.
7. Choose one sync method:
   - A folder on the owner's computer, read in place through the Melaya runner. Works with Obsidian Sync, iCloud, Dropbox or Git.
   - A Git repository over HTTPS, with a token limited to that repository.
   - An uploaded zip snapshot. Re-upload it to refresh.
   Back up before the first sync, and never run two sync tools on one vault on one device. Switch off cloud AI models in the vault's privacy settings for notes that must stay on local models.
8. Attach the vault. In the app: Connectors, Obsidian, Connect a vault, Read only. Then add it in each executive's Knowledge tab. Or from the owner's assistant through the Melaya MCP server: `melaya_excom_knowledge_manage` with action bind, kind obsidian, the team, and the connected vault and folders as the reference (omit the executive to bind it for the whole team). Then run action sync.
9. Verify. Run `excom_knowledge_search` for three facts from the interview. Record that the vault is live with `excom_record_fact`. Then tell every executive with `excom_send_handoff` (kind request) to read the company hub before their next brief.

## Output

```text
Task: Build the company knowledge vault (owner, due this week)
Brief: interview questions | documents to gather | folder tree | note template | privacy rules | sync choice | attach steps
After attach: source bound (obsidian, read only) | sync state | 3 facts found | executives notified
```

## Approvals

- Binding, removing or syncing a team source is a record write. The owner confirms it.
- Edit rights for executives on the vault are the owner's decision. Edits then follow the approval settings.
- A paid sync or hosting plan is spend, and the owner decides with the cost.

## Example

Acme has no vault. The CEO proposes the task. The founder spends 45 minutes with their assistant and gets 40 notes across ten folders. They sync through Git, bind the vault read only to the whole team, and search finds the price list, the goal definitions and the partner list.

## References

- references/vault-structure.md: the folder tree and the first notes to write. It loads with `excom_skill_load`.
- references/note-conventions.md: the frontmatter, names, links, one-fact rule, review dates and editing rules.

Adapted from kepano/obsidian-skills (plugins/obsidian/skills/obsidian-markdown/SKILL.md, plugins/obsidian/skills/obsidian-headless/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
