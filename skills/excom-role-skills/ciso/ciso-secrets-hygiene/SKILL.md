---
name: ciso-secrets-hygiene
description: Finds where a credential leaked (code, deletion hunks, logs, run transcripts, mail, chat), classifies it, drafts a rotation plan with every consumer and an old-value-denied test, and records the rotation without ever showing a value. Use when a key, token or password was seen somewhere it should not be, before a release security gate, when a rotation is due, a person with access leaves, or a vendor reports a breach.
version: 2.0.0
---
# Secrets hygiene and rotation plan

Keep every credential out of code, notes, logs and chat, and when one escapes, get it rotated with a clean record. A leaked production or connector key is the fastest way to lose customer trust.

## Look up first

- The secrets policy and rotation procedure: `excom_knowledge_search` for "secrets policy", "rotation runbook", "containment list". If missing, use the plan template in Output and draft the policy afterwards with `excom_save_draft`.
- The secret inventory: `excom_secret_list` (names, owners, ages only).
- Who rotates (operator, CTO) and who approves: your charter and the runbook; if unclear, ask the owner with `excom_propose_task` (needs decision true).
- Which code, log and repository apps you are granted; `excom_request_setup` for a missing one.

## Steps

1. Describe secrets as policies, never values: no env names paired with values, key paths, addresses or token prefixes long enough to search for.
2. Never ask for, read back or quote a value. Do not use a reveal tool to check anything; the check is whether the old value is denied after rotation, done by the operator.
3. Find exposure, reads only:
   - Code: `github_list_secret_scanning_alerts`, `gitea_commit_diff` on commits since the last release. Read deletion hunks too: they carry the full old content.
   - Logs and runs: `grafana_loki_query` with a pattern for the token shape (not the value), `melaya_run_inspect` only on a cited run.
   - Mail and chat: only the message the reporter named.
4. Classify each finding: live production credential, live third-party connector credential, test or revoked value, false positive. Unknown counts as live and is SEV2 until proven stale.
5. Draft the rotation plan with `excom_save_draft` (draft): identifier, every consumer system (missed consumers are where rotations fail), order, who runs it, restart needed, the old-value-denied test. Ask the CTO to confirm consumers with `excom_send_handoff` (kind request).
6. Rotation, env staging, gate flips and restarts are production class. A restart runs only when the owner asked for it in the current message.
7. After the operator rotates, record identifier, revocation time, activation time, systems, actor, approver, restart, denied-test result with `excom_record_fact`. Never the value, a prefix or a hash.
8. Prevent the repeat: propose with `excom_propose_task` the gate that would have caught it (pre-commit scan, CI scan, log redaction, moving the value into the secret store). If the leak is in a coding session diff, tell the CTO to hold its push.

## Output

```text
Secret exposure <date>
Signal: where seen (file and commit, log query, message id), when, by whom
Classification: live prod | live connector | test | false positive
| identifier | consumers | rotation owner | order | restart | old-value-denied test | approver | status |
After rotation: revocation time, activation time, actor, approver
Prevention task: gate, owner, date
```

## Approvals

- Any rotation, revocation, env staging, gate flip or restart (production).
- Deleting history, rewriting a commit, purging a log (delete).
- Telling a vendor, partner or customer about an exposure (send, with the legal executive for wording).

## Example

Acme: a payment webhook secret appears in a deleted line of a merged commit. Classified live production. Consumers confirmed by the CTO: API server and one managed pipeline. Plan drafted: rotate at the provider, update the secret store, restart the API (owner to request), confirm the old value is rejected. A CI secret scan is proposed as prevention.

Adapted from alirezarezvani/claude-skills (engineering/skills/env-secrets-manager), MIT. Modified: rewritten generic for EXCOM.
