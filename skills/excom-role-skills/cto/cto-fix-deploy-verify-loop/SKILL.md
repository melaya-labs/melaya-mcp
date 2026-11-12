---
name: cto-fix-deploy-verify-loop
description: Closes a production error end to end: monitor, find the cause, fix it in a coding session with a test, review and push, deploy through CI, then prove from monitoring that the error stopped. Use when a monitoring alert wakes you, the daily reliability check finds a noisy service, a customer-visible error has a log signature, a previous fix did not hold, or someone asks "is it fixed in production".
version: 2.0.0
---
# Monitor, fix, deploy, verify loop

Keep the loop whole so no fix is called done until the error count says so. Each step has its own skill; this one sequences them.

## Look up first

- Your charter objectives in context (for example a post-deploy check window) and `excom_recall` for past loops on this error.
- Monitoring and CI access: `grafana_*` and `jenkins_*` (or your equivalents). Missing app: `excom_request_setup`. Coding grant off: ask the owner with `excom_send_handoff` (kind question). Never fake a step.
- The deploy runbook and the team's known-issues note: `excom_knowledge_search` "deploy runbook", "known issues". If the deploy runbook is missing, stop before deploying and ask the owner with `excom_propose_task` (needs decision true).

## Steps

1. Orient: read the alert payload, then `excom_read_tasks` for an open task on the same error.
2. Monitor: `grafana_errors_summary` for the window. Pick one error, the one with the most customer impact, not the loudest.
3. Evidence: `grafana_error_context` on that message; find the root cause with skill cto-incident-root-cause. No root cause hypothesis, no loop.
4. Task: `excom_propose_task` carrying the evidence (service, errors, logs, query, first seen, last seen, count, source).
5. Fix: `excom_code_task` with repository, one-line goal, governing runbook and evidence (record write, asks under Prepare). The session reproduces with a test and reports evidence addressed and the covering test. Follow skill cto-coding-session-hygiene.
6. Review and push: skill cto-push-review-gate; `excom_code_push` branch (send), then base (production, always asks).
7. Deploy: skill cto-jenkins-safe-deploy, only the jobs the diff needs, in the runbook's order. On red, read `jenkins_build_console` and stop.
8. Mark: `grafana_create_annotation` with commit and build (record write).
9. Verify: `grafana_errors_summary` with a window that starts after the build finished and ends now. The fixed message must not appear after the deploy. Allow at least 30 minutes of normal traffic, or the alert's usual recurrence interval, before calling it stopped.
10. If it persists or a new error appeared, say so on the task, gather new evidence, start a new session. Never mark done on a deploy alone.
11. Close: `excom_record_measurement` (count before and after, windows), `excom_update_task` with receipts, and a known-issues entry drafted with `excom_save_draft` when the cause is reusable.

Silences (`grafana_create_silence`, `grafana_expire_silence`) are production. Propose one only to quiet a known alert during an approved deploy, with an end time, and expire it after verification.

## Output

```text
Loop <service>
Error: message, first seen, last seen, count (window, query)
Root cause: one line
Session: id, diff stat, covering test, evidence addressed
Push: branch (approved) / base (approved, sha)
Deploy: job #build green, ...
Annotation: yes
Verify: window after deploy, count after, last seen
Status: stopped | persists (next session id)
```

## Approvals

- `excom_code_task` under Prepare (record write).
- `excom_code_push` branch (send) and base (production).
- `jenkins_trigger_build`, `jenkins_abort_build` and any silence: production, every call.
- Any restart or environment change: only when the owner asked in the current message.

## Example

Alert "checkout 5xx" fires for Acme. Error "price is undefined", 87 in 30 minutes. Root cause: a renamed field in the plan payload. Session S-8 adds a failing test, fixes the mapping; push to branch and base approved; job Web #44 green; annotation added. Forty minutes after the build: 0 occurrences, last seen 2 minutes before the deploy. Status stopped.
