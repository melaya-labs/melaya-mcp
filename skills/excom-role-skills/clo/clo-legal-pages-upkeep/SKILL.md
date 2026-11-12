---
name: clo-legal-pages-upkeep
description: Keeps the public legal pages (terms, privacy policy, security overview, subprocessor list, DPA, usage policy) true to what the product enforces, drafts changes as redlines, and checks parity across every site language before release. Use when a product surface ships or changes, when a counsel item, store or marketplace requirement or regulation needs a clause, for the weekly legal change log, or when a translation may promise more or less than the source.
version: 2.0.0
---
# Terms and legal pages upkeep

Keeps legal pages accurate in every language. A page that promises more than the code does is a liability; a page that lags a launch blocks listings and deals.

## Look up first

- Which legal pages exist, their routes, languages and section structure: `excom_knowledge_search` "legal pages", "terms of service", "privacy policy and DPA". If missing, ask the owner with `excom_propose_task` (needs_decision true).
- How legal acceptance is recorded and when re-acceptance is needed: `excom_knowledge_search` "legal acceptance". If missing, ask the CTO.
- The translation process and brand voice per language: `excom_knowledge_search` "translation process", "brand voice".
- The change: what the product does now, from the CTO or CPO (`excom_send_handoff`, kind question).

## Steps

1. Get the current text: `melaya_browser_read` or `web_fetch` on each live page, or source strings with `github_get_file` or `gitea_repo_file`. Keep the previous public version as evidence with `wayback_history`.
2. Confirm enforcement before wording: ask the CTO which gate, setting or job enforces the claim. No enforcement, no clause; use honest status words (live, live with counsel review pending, operational gap, target).
3. Draft the source-language change as a redline (section, current, proposed, reason, enforcing control) with `excom_save_draft` or `docs_create` (record write). Mark AI transparency, dispute, privacy label and regulated-activity clauses for counsel via the owner.
4. Request translations of the approved text through the team's translation process, following the brand voice per language; never a machine-only pass. The CMO reviews tone.
5. Run the parity check in `references/parity-checklist.md` across every language.
6. If terms, usage policy or privacy changed, flag the acceptance version bump so sign-in paths re-collect acknowledgement (production change with the CTO).
7. Release with the CTO as an engineering release; propose it with `excom_propose_task`. After deploy, verify each language with `melaya_browser_read` and record languages verified with `excom_record_measurement`.
8. Log the change: date, sections, languages, acceptance version, reason.

## Output

```text
Legal page change: <page>  sections  trigger (product / counsel / regulation)
Redline: section | current | proposed | reason | enforcing control
Counsel questions
Parity: language | sections | numbers | processors | contacts | status
Release: acceptance bump yes/no | ticket | verified n of N languages | date
```

## Approvals

- Publishing or deploying a legal page or acceptance version: production, the owner with the CTO.
- Regional blocks or regulated-feature flags: production, counsel required.
- Sending counsel questions: the owner sends.
- Paid translation or counsel: spend, with the cost.

## Example

Acme ships a feature that lets agents operate a user's browser. The privacy page gains a section on what is captured and where it is processed; the CTO names the setting that keeps captures local. Translations come back; the parity check finds the Spanish page lists a 30-day retention where the source says 7 days. Fixed before release; acceptance version bumped.

## References

- `references/parity-checklist.md`: what to compare across languages and the release checks; read at steps 5 and 7.
