---
name: cpo-docs-upkeep
description: Keeps public and in-app documentation true after a product change: finds every doc that states the behaviour, confirms the truth with a live read, patches knowledge notes and in-app doc strings in every supported language, and keeps headline counts in one canonical place. Use when a release changed behaviour, a limit or a setting name, when a doc is reported wrong, when support answers contradict the docs, or on the weekly docs pass.
version: 2.0.0
---
# Keep public and in-app docs true

Make the documentation say what the product does today, everywhere it is said. Wrong docs cost signups and support time, and AI answers repeat them.

## Look up first

- Where docs live: `excom_knowledge_search` "documentation", "public docs", "in-app docs", "docs corpus". If unknown, ask the owner with `excom_propose_task` (needs decision).
- Supported languages and the translation procedure: `excom_knowledge_search` "locales", "translation pipeline". If missing, ask the owner; never guess the list.
- Canonical headline numbers and product names: `excom_knowledge_search` "products", "headline numbers".
- The house style and banned characters: `excom_knowledge_search` "brand voice", "style guide". Default: no em or en dashes.

## Steps

1. Find every place the behaviour is documented: `obsidian_search` in the docs vault, `melaya_docs_search` for in-app and assistant docs, and the in-app doc strings in the site code. If the vault app is not granted, `excom_request_setup`.
2. Confirm the truth with a read made now: `melaya_connector_tools`, `melaya_pipeline_templates`, `melaya_model_list`, `melaya_run_diagnosis` on a real run. If doc and product disagree, the product wins unless the CTO says the code is the bug.
3. Patch the knowledge note and bump its updated date with `obsidian_patch` (record write, asks outside your own folder). Keep its structure and links.
4. Patch in-app doc strings in a coding session (skill cpo-code-session-handoff): source language first, then every supported language through the translation procedure. Lock human corrections the way the procedure says, so the next machine run does not overwrite them.
5. Apply house rules to every string: banned characters, brand names untranslated, no certification or compliance claim the company does not hold.
6. Counts: link to the canonical note instead of restating a number. Where a number must appear, it comes from a generator or the canonical note, never a typed figure.
7. If the docs feed an assistant corpus, ask the CTO with `excom_send_handoff` (kind request) to rebuild it after deploy.
8. Copy on third-party sites (directories, store listings) is send class: draft it and hand it to the marketing or support executive.
9. Record each change with `excom_record_fact` (doc, old claim, new claim) and close the task with `excom_update_task`.

## Output

```text
Docs patch <date>: change that triggered it
| surface | note or file | old claim | new claim | languages done | verified by | status |
Handoffs: coding session id, corpus rebuild, third-party copy drafts
```

Saved with `excom_save_draft`.

## Approvals

- Patching a shared knowledge note (record write).
- A paid translation run (asks with the cost).
- Push and deploy of the in-app change: the CTO only (production).
- Changing copy on third-party sites (send).

## Example

A release renamed the setting "Auto-run" to "Run within rules". Search finds it in 3 public notes, 1 in-app card and a store description. Live read confirms the new name. The notes are patched, the card ships in all supported languages in one session, the store copy goes to marketing as a draft.
