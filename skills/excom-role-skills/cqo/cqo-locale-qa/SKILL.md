---
name: cqo-locale-qa
description: Checks translations and locale behaviour before release: key parity across every supported locale, placeholders, plural forms, banned characters, the translation audit trail, and live language tags and hreflang on public pages. Use when strings change in a coding session or release, when a language is added, when a translation wave finishes, or when someone reports a wrong or untranslated text.
version: 2.0.0
---
# Translation and locale QA

Make every surface read correctly in every supported language before it ships, because a missing key falls back to the source language silently and a broken page loses trust in that market.

## Look up first

- The supported locales and the source locale: `excom_knowledge_search` for "locales" or "supported languages". If you cannot find them, ask the owner with `excom_propose_task` (needs decision true); never assume a list.
- The add-a-language runbook and the translation pipeline runbook: `excom_knowledge_search` for "add a new language", "translation pipeline". They name the quality gates and their commands, the sanitizer, the audit file and its confidence threshold, the allow-list of untranslated words, and the paid run costs.
- The house style for copy (banned characters, names kept in Latin script): `excom_knowledge_search` for "brand voice".
- The last verdict for the same namespace: `excom_recall`.

## Steps

1. Read the diff: `excom_code_status` for a session, or `gitea_commit_diff` or `github_list_commits` for commits. List every new or changed source-locale key and every locale file touched.
2. Run the checks in references/locale-checks.md against the files (read with `gitea_repo_file` or `github_get_file`): key parity, placeholders, plurals, banned content, audit trail.
3. Read the quality gate output from the session checks with `excom_code_status`. If the gates were not run, the row is "not verified" and the CPO is asked to run them in a coding session.
4. After deploy, run the live checks on a sample of public pages per locale with `web_fetch`: html lang, a localized title, one self canonical, a full reciprocal hreflang set with x-default, structured data language. Spot check indexing with `gsc_url_inspect`; if Search Console is not assigned, `excom_request_setup`.
5. Never machine-translate to make a check pass: a gap is marked for a translator. Send findings to the CPO (owner of translation keys) with `excom_send_handoff` (kind request).
6. Save the verdict with `excom_save_draft` and record the blocking count with `excom_record_measurement` (record write).

## Output

```text
Scope: namespaces, keys, locales, session or commits
| locale | missing keys | placeholder breaks | plural errors | banned chars | low-confidence entries | lang/hreflang live | status |
Blocking: file, key, locale
Translator queue: keys needing a human, per locale
```

## Approvals

- A paid translation run (spend, state the cost from the runbook).
- Any deploy or app release that ships the strings (production, CTO).
- Sitemap or IndexNow submission after a new language (send).
- A native-speaker reviewer contract (spend).

## Example

A session adds 12 keys to the checkout namespace. In the Russian file 2 keys are missing and one plural copies the English two forms (Russian needs few and many). In the French file a placeholder was renamed. Verdict: blocking, 3 findings with file and key, handed to the CPO; the session cannot be pushed until fixed.

## References

- references/locale-checks.md: the per-file and live checks with what blocks and what warns. Read it at step 2; load with `excom_skill_load` (section) or by paging.

Adapted from alirezarezvani/claude-skills (engineering/skills/i18n-localization), MIT. Modified: rewritten generic for EXCOM.
