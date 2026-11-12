---
name: cto-incident-root-cause
description: Finds the proven root cause of a production error from logs, metrics and recent changes before any fix is proposed, and hands a coding session a ready evidence object. Use when a monitoring alert fires, errors spike after a deploy, a customer run fails in production, a previous fix did not stop the error, or someone says "just restart it" or "it is probably X".
version: 2.0.0
---
# Incident root cause

Turn an alert or error spike into a root cause backed by evidence and an evidence object a coding session can act on. A guessed fix costs a deploy window and hides the real fault.

## Look up first

- Monitoring access: which of `grafana_*`, `sentry_*` or a log source you are granted. If none, `excom_request_setup` for your monitoring app and stop at a written question; never guess from memory.
- The team's incident response runbook and severity table: `excom_knowledge_search` "incident response". If missing, propose one with `excom_save_draft`.
- Past occurrences: `excom_recall` and `excom_knowledge_search` "known issues" for the same message.
- Service map (components and boundaries): `excom_knowledge_search` "architecture" or "deploy runbook".

## Steps

1. Read the evidence before touching anything. `grafana_list_firing_alerts`, then `grafana_errors_summary` over the window (30 minutes before first seen to now). For the top message run `grafana_error_context`. Read every message and stack trace to the end. With Sentry, `sentry_hot_issues_now` and `sentry_get_issue` give the same.
2. Bound it: constant, periodic, or tied to one tenant, model or route? Use `grafana_loki_query_range` with the drill-down query and `grafana_loki_patterns` to see whether the shape is new; `grafana_prom_query` for saturation (queue depth, memory, restarts). For a failed pipeline run, `melaya_run_diagnosis` on two failing runs and one passing run. A client error that looks like CORS or rate limiting is often an edge 5xx: check `cloudflare_firewall_events` when granted.
3. Check what changed: `grafana_list_annotations` for deploy markers, `gitea_list_commits` and `gitea_commit_diff` (or `github_list_commits`) since the last good period. Config, version pins and provider model changes are candidates too.
4. Compare with the closest path that still works and list every difference. At each component boundary note what goes in and what comes out; the boundary where good input becomes bad output is where to look.
5. One hypothesis at a time: "X is the root cause because Y, shown by Z." Test it with the smallest read that could disprove it. If it fails, write a new one; never stack guesses.
6. Hand the fix to a coding session with the evidence object: start `excom_code_task` (record write) or follow skill cto-fix-deploy-verify-loop. The session must reproduce the error with a failing test first.
7. If three fixes already failed for the same error, stop and send a design memo to the owner with `excom_send_handoff` (kind question) before a fourth attempt, because repeated failures point at the architecture.
8. Security smell (exposure, unknown source, secret in a log): hand to the CISO with `excom_send_handoff` (kind request). The CISO commands security incidents; the CTO stays technical lead.
9. Record the root cause with `excom_record_fact` and the follow-up with `excom_propose_task`.

## Output

```text
Root cause memo: <service>
Trigger: alert or report, first seen, last seen, count (tool, window)
Evidence: E1..En (message, query, redacted sample)
Changes in window: deploys and commits
Hypotheses tried: H1 result, H2 result
Root cause: X because Y, shown by Z
Fix proposal: smallest change at the source + covering test + rollback
Evidence object: service, errors, logs, query, first_seen, last_seen, count, source
```

Saved with `excom_save_draft`; the evidence object goes to the session.

## Approvals

- Starting a coding session under Prepare (record write).
- Any silence, restart, config change or deploy is production. A restart runs only when the owner asked for it in the current message.
- Customer or status page messages are sent by the COO or CXO after approval.

## Example

Acme's API shows 5xx on the export route after the 14:00 deploy. `grafana_errors_summary` shows 312 "null tenant id" errors, first seen 14:06. The deploy diff changed the tenant lookup; one passing route still uses the old helper. Root cause: the new helper drops the header for background jobs, shown by error context lines with job ids only. Evidence object handed to a session.

Adapted from obra/superpowers (skills/systematic-debugging), MIT. Modified: rewritten generic for EXCOM.
