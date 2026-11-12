---
name: cqo-docs-accuracy-check
description: Verifies public and in-app documentation against what the product actually does today, claim by claim, with a live read for each count, step, limit, capability and safety statement, and routes fixes to the CPO. Use when a release changed behaviour or counts, for the weekly docs sample, when a ticket says "the docs say X but the app does Y", or before docs are quoted in a listing or a sales answer.
version: 2.0.0
---
# Docs accuracy check

Make what the documentation says match what the product does, because customers, partners and AI assistants quote the docs, and a wrong count or a vanished step costs trust and support time.

## Look up first

- Where the docs live: `excom_knowledge_search` for "public docs", "in-app documentation", "help center". If you hold a docs app (`notion_search`, `intercom_list_articles`), read there too.
- The canonical numbers the company publishes (tool, template, provider, language counts) and where they come from: `excom_knowledge_search` for "headline numbers" or "product facts". If there is no canonical source, propose one to the CPO with `excom_send_handoff` (kind request).
- House rules for public claims (certifications not held, platform limits, hidden integrations never named): `excom_knowledge_search` for "brand voice" or "public claims".
- The supported locales, if the in-app docs are translated: `excom_knowledge_search` for "locales".

## Steps

1. Find the pages: `excom_knowledge_search` for the feature in the docs; `melaya_docs_search` for what the in-app docs and assistant corpus return. List every claim the pages make about the change.
2. Classify each claim: count, step, limit, capability, or safety statement.
3. Verify each claim against a live read, never memory, using references/claim-checks.md. If the product and the page disagree, the product is right and the page is wrong; if the canonical numbers source is stale, flag it to the CPO.
4. For translated docs, check every locale carries the fix: a fix in the source language only leaves the other pages wrong (hand the keys to skill cqo-locale-qa).
5. Check the house rules on each page.
6. Write the verdict per claim (true, false, unverifiable). "Unverifiable" is valid and names what would verify it.
7. Send fixes to the CPO with `excom_send_handoff` (kind request): the CPO patches the notes or codes the in-app change in a coding session. Third-party listings go to the CXO or CMO.
8. Re-check the fixed pages after publish and record the share of verified claims with `excom_record_measurement` (record write).

## Output

```text
Docs accuracy YYYY-MM-DD: <feature>
| page or section | claim | type | source of truth | verified by (tool, read time) | true / false / unverifiable | fix proposed |
Locales affected; owners: CPO (docs, in-app), CXO or CMO (third-party listings)
```

Saved with `excom_save_draft`.

## Approvals

- Editing a public docs note or knowledge note (record write, done by the CPO).
- Changing a third-party listing or store description (send).
- Running a flow that could send or write outside the validation rule.
- Deploying in-app documentation strings (production, CTO).

## Example

Acme's setup guide says "connect in 3 steps" and "over 200 integrations". A live read of `melaya_connector_list` shows 214 integrations (true). Following the guide in a validation run needs 4 steps because a consent screen was added (false). Fix proposed: add step 3 "approve the consent screen", owner CPO, all locales.

## References

- references/claim-checks.md: which live read verifies each claim type. Read it at step 3; load with `excom_skill_load` (section) or by paging.
