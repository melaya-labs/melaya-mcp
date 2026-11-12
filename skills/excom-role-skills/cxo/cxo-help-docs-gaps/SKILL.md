---
name: cxo-help-docs-gaps
description: Keeps a scored backlog of missing or wrong help docs fed by real support questions, known issues and product changes, and drafts the customer-facing version of each fix for review. Use when a support reply had no documented answer, when a fixed issue has no customer note, when a product change makes a page stale, on the weekly docs block, or when someone asks "what's missing from our help center".
version: 2.0.0
---

# Help-docs gaps

Every question the docs answer is a stalled trial that never stalls, so gaps are logged from real questions, ranked by impact and turned into reviewed drafts.

## Look up first

- The public docs and their structure: `excom_knowledge_search` "troubleshooting", "FAQ", "getting started", "error messages"; the help desk articles when Intercom is granted.
- The known-issues list and which issues are fixed: search "known issues".
- Docs ownership and how public notes are edited and published (who approves, whether an assistant corpus must be rebuilt): search "documentation process". Missing: ask the CPO with `excom_send_handoff` kind question.
- Supported languages and the translation process: search "translation".

## Steps

1. Intake each gap: the question in the user's words, source and count, audience, product, the note that should hold it, linked issue or release, date found.
2. Check the docs before logging: `excom_knowledge_search` and `excom_knowledge_read`; `intercom_search_articles` when granted; `web_fetch` on the public page. Merge duplicates and add to their count.
3. Score with references/gap-scoring.md and rank.
4. Note dependencies: the CPO or CTO for facts on new features, screenshots, translations, the CMO for positioning wording.
5. Draft the customer version: the symptom as the user sees it, the cause in one line, the fix or workaround, the fixed date if fixed, related links. Follow the existing notes' structure and the brand voice. Save with `excom_save_draft`.
6. Propose the edit with `excom_propose_task` (draft and target note), because public notes change only with approval. When an assistant docs corpus must be rebuilt, ask the CTO (`excom_send_handoff` kind request).
7. Track status: backlog, drafting, in review, published, refresh queued. Re-verify published fixes against the live product monthly.
8. Weekly: open gaps, published this week, oldest open gap. Record gaps closed with `excom_record_measurement`.

## Output

```text
| Gap (user words) | Product | Target note | Source and count | Score | Dependencies | Status | Owner |
```

Plus each drafted section ready for review.

## Approvals

- Editing or publishing any public note, article or help-desk content: asks.
- Rebuilding a docs corpus or any deploy: production, CTO.
- Deleting notes or articles: delete, always asks.

## Example

Gap: "where do I find my API key?", asked 5 times, no doc. Score 19 of 25 (blocks developer activation). Draft: "Settings, Developer, Create key" with the screen names as shown; target: the developer quickstart note; dependency: CTO confirms the screen names.

## References

- references/gap-scoring.md: scoring criteria and the customer-version template. Read at steps 3 and 5; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/technical-writing/skills/doc-requirements-matrix/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
