---
name: cpo-release-notes
description: Turns what actually shipped (deployed commits, coding session results, closed tickets) into user-facing release notes grouped by product, benefit first, with action-required items stated exactly and copy ready for every supported language. Use when a deploy is verified, before announcing a release or a changelog, for a monthly product recap, or when someone asks "what's new" or "write the changelog".
version: 2.0.0
---
# Release notes from what shipped

Write notes a user understands in ten seconds: what changed for them, led by the benefit, with anything that needs their action stated plainly. Only what is live goes in.

## Look up first

- The last release point: `excom_recall` "release notes".
- The release and deploy procedure (what counts as live, which branch deploys): `excom_knowledge_search` "release checklist", "deploy runbook".
- Product names, brand voice and supported languages: `excom_knowledge_search` "products", "brand voice", "locales". If missing, ask the owner with `excom_propose_task` (needs decision).
- The CTO's deploy report and the CQO's go or no-go for the window.

## Steps

1. List what shipped: `gitea_list_commits` since the last release point (or your repo host's equivalent), `gitea_commit_diff` when unclear, `gitea_list_releases` for tags; `jenkins_get_build` on the deploy builds if your CI is Jenkins and you hold the read grant, otherwise ask the CTO with `excom_send_handoff` (kind question). A commit not deployed is not shipped.
2. Read coding session results (`excom_code_status`) for the summary and covering test.
3. For each change: what changed, who it affects, why it matters. Drop refactors, test-only commits and anything hidden or internal-beta.
4. Categorize: New, Improved, Fixed, Action required, Deprecated.
5. Write each entry in one to three sentences, benefit first, plain words, no ticket numbers, codenames or file paths, in the house voice.
6. Anything users must install or update: quote the exact pinned command or version the product shows, never "latest".
7. Check every claim against the product and the canonical numbers; anything the CQO has not verified live is left out or marked "rolling out".
8. Hand copy for other languages through the translation procedure, the campaign version to the marketing executive and support macros to the support executive with `excom_send_handoff` (kind request).
9. Record the new release point with `excom_record_fact`.

## Output

```text
# <Product> release notes, <date>
## New
- <Product area>: <what you can do now and why it helps>
## Improved / ## Fixed / ## Action required (what, who, by when, exact command)
Internal appendix (not published): commit range, builds, sessions, items left out and why
```

Saved with `excom_save_draft`.

## Approvals

- Publishing anywhere public: site or changelog page (production, through the CTO), email, social or community posts (send, executed by marketing or support).
- A paid translation run (asks with the cost).
- Naming a customer or partner (needs their consent; the CEO decides).

## Example

Technical: "Added retry with backoff on connector token refresh." Note: "Fixed: connected apps no longer disconnect after a brief outage, so scheduled runs keep working overnight." Action required: "Update the runner to the version shown in Settings to use the new browser tools."

Adapted from phuryn/pm-skills (pm-execution/skills/release-notes), MIT. Modified: rewritten generic for EXCOM.
