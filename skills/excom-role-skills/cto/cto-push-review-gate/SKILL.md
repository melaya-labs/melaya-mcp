---
name: cto-push-review-gate
description: Reviews a finished coding session (your own or one handed over by the CPO or another executive) for blast radius, secrets, test delta and breaking changes, then gates excom_code_push to the branch and the base. Use when a session is ready to push, when a colleague asks "can you push this", when a change touches auth, schema, migrations, pins or the deploy path, or before any base push.
version: 2.0.0
---
# Push review and gate

The CTO is the only executive that holds `excom_code_push`. Every session, including CPO product, docs and SEO changes, passes this review before it leaves the computer, and ends in a verdict the owner can approve on one card.

## Look up first

- The acceptance criteria for the change (from the handoff, the task or `excom_knowledge_search` "acceptance criteria <feature>"). If a product change has none, ask the CPO with `excom_send_handoff` (kind question) before reviewing code.
- The release checklist and security gate: `excom_knowledge_search` "release checklist" and "release security gate". If missing, use references/review-checklist.md and propose the note with `excom_save_draft`.
- Version pins and locale rules for the repository: `excom_knowledge_search` "version pins" and "locales". If missing, ask the owner with `excom_propose_task` (needs decision true).

## Steps

1. Read the result with `excom_code_status`. Refuse to review if a check failed or did not run, or any violation exists; ask for a new session instead.
2. Blast radius: give each changed file a tier (critical, high, medium, low) using references/review-checklist.md. Any critical file makes this a significant change.
3. Security pass: scan the diff for secrets, including deletion hunks, which carry old content. No key, token, password, internal hostname or personal data may enter a commit. For a significant change, hand the diff summary to the CISO with `excom_send_handoff` (kind request) and wait for the security gate.
4. Test delta: new behaviour without a test is a must fix; deleted tests without deleted code is a must fix; auth, payment and approval paths need a covering test per branch changed.
5. Breaking changes: migrations with a down file and code that tolerates the migration being absent; new environment keys documented and staged by the owner, never in the diff; all version pins agree; new UI strings present in every locale the team ships; public routes keep their SEO invariants.
6. Component split: a client-only commit must not force a server restart. Note which CI jobs the push will need.
7. Write findings labelled must, should, nit or question, in one round. Must items go back to the author with `excom_send_handoff` (kind request). Push back on a finding only with a test or code that proves it.
8. Verdict go: `excom_code_push` target branch (send, asks). After review and the quality go, `excom_code_push` target base (production, always asks). If the head moved since the card, the push refuses: review again.
9. Record the verdict with `excom_update_task` and continue with skill cto-jenkins-safe-deploy.

## Output

```text
Review: session <id> (<author role>) <repo> <branch> -> <base>
Acceptance criteria: met / not met (row by row)
Blast radius: file tier, ...  Significant: yes/no (security gate: passed/pending)
Secrets scan: clean / finding
Tests: covering tests, delta
Breaking: migrations, env keys, pins, locales, SEO invariants
Findings: must ..., should ..., nit ..., question ...
Verdict: push to branch | push to base | send back
CI jobs needed: ...
```

Saved with `excom_save_draft` and linked on the task.

## Approvals

- `excom_code_push` target branch (send) and target base (production): every call shows a card, even with a rule.
- Any deploy that follows (production).
- A significant change waits for the CISO review; a public-surface change waits for the CQO go.

## Example

The CPO hands over session S-17 (Acme help center copy, 6 files). Checks green, no violations. Tiers: 5 low, 1 high (an i18n namespace). Two locales lack the new key: must fix, sent back. The resubmitted session passes; push to branch, then base after the CQO go.

## References

- references/review-checklist.md: blast radius tiers and the full pre-push checklist. Read when tiering files or when the team has no release checklist note (page it in or load with `excom_skill_load`).

Adapted from alirezarezvani/claude-skills (engineering/skills/pr-review-expert) and obra/superpowers (skills/requesting-code-review), MIT. Modified: rewritten generic for EXCOM.
