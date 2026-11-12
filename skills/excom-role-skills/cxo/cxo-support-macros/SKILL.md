---
name: cxo-support-macros
description: Builds and maintains a small library of vetted support answers (macros) for the questions users ask most, each checked against the public docs and the live product, and uses them to draft fast, consistent replies. Use when the same support question repeats, when a known issue is fixed or changes, when a reply needs a vetted answer, for the monthly macro review, or when someone asks "do we have a standard answer for this".
version: 2.0.0
---

# Support macros from the answer library

Quick, correct, consistent answers keep trials alive long enough to convert, and a macro checked against the docs never promises what the product does not do.

## Look up first

- The documented answers: `excom_knowledge_search` "troubleshooting", "error messages", "FAQ", "getting help", then `excom_knowledge_read`. No documented answer: open a docs gap (cxo-help-docs-gaps) instead of inventing one.
- Reply structure and voice: search "support reply structure", "brand voice", and the interface languages.
- Which support channels and mailboxes are bound (connector settings); whether a help desk such as Intercom is granted.
- Routing rules for billing, security and upgrade questions: search "support escalation".

## Steps

1. Collect repeats from the sweep: `zoho_email_list`, `gmail_list_threads`, `discord_get_messages`, `reddit_search_posts`; with Intercom, `intercom_search_conversations` and `intercom_list_tags`. Without a help desk, count by hand in your notes.
2. Pick questions asked twice or more this month, starting with those that block first success.
3. Write each macro in four parts: the fix first, the reason in one line, the doc link, what to include if it persists. Variables in braces. Plain text, under 90 words.
4. Review every macro with references/macro-checklist.md before first use, because a wrong macro repeats the mistake to every user.
5. Store macros: propose the library note (`excom_propose_task` with the draft), and in Intercom when granted (`intercom_list_macros` to read; creating or editing help-desk content asks). Want a help desk and none is connected: `excom_request_setup` with service id "intercom".
6. Draft replies from macros: adapt the first line to the user's words, read their run first when they shared one (run diagnosis through `melaya_tools`), save as a draft (`gmail_create_draft`), ask for the send.
7. Route what a macro must not answer: billing and refunds to the CFO, security reports privately to the CISO, upgrade intent to the CRO, new failure kinds to the CTO and CQO (`excom_send_handoff`).
8. When a fix ships, update every macro naming that issue the same day. Record macro coverage with `excom_record_measurement`.

## Output

```text
Macro: <name> | Trigger phrases: <how users ask>
Fix: <steps> | Why: <one line> | Doc: <public note title>
If it persists, send: error code and message, the goal in one sentence, page and time with timezone, provider and model, screenshot or run id
Owner: CXO | Verified on: <date> | Linked issue: <id or none> | Languages: <list>
```

Monthly: macro, times used, last verified, issue status, change needed.

## Approvals

- Every reply sent to a user, on any channel: send class.
- Creating or editing help-desk macros or articles, or editing a public note: asks.
- Deleting macros, messages or tags: delete, always asks.

## Example

"I clicked run and nothing happened" asked 6 times. Macro: "Your run is waiting for your approval. Open Approvals and accept or reject the step. Why: actions that send or change data wait for you. Doc: Approvals. If it persists, send the run id."

## References

- references/macro-checklist.md: the review checklist for accuracy, voice, safety, languages and versioning. Read at step 4; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/technical-writing/skills/quality-review-checklist/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
