---
name: cto-post-incident-review
description: Writes a blameless post-incident review of an availability incident within 72 hours: timeline rebuilt from systems, impact counted, root and contributing causes found with five whys, and owned actions with dates and proof of done. Use when an outage, degraded product, failed or rolled-back deploy, or runs lost to a deploy were resolved, when someone asks "what happened yesterday", or when the same failure came back.
version: 2.0.0
---
# Post-incident review

Turn one bad day into a known issue that never repeats: what happened, why, what helped, what hurt, and owned actions with dates.

## Look up first

- The team's incident response runbook and severity table: `excom_knowledge_search` "incident response". If missing, use the table in references/pir-template.md and propose the runbook with `excom_save_draft`.
- The incident task, roles and approvals: `excom_read_tasks` and `excom_recall`.
- The known-issues note: `excom_knowledge_search` "known issues". If missing, draft the first entry with `excom_save_draft`.
- Recovery targets (detection and recovery time objectives) in your charter objectives or the knowledge base; if none, record the measured times and propose targets.

## Steps

1. Confirm the class. Availability incident: continue. Any sign of exposure, attack or a leaked secret: hand to the CISO with `excom_send_handoff` (kind request) and write only the technical section.
2. Confirm severity with the team's table. Severity can be lowered by the review, never silently.
3. Rebuild the timeline from systems, not memory: `grafana_loki_query_range` and `grafana_errors_summary` for first and last error, `grafana_list_annotations` for deploys, `jenkins_get_build` for build times, `gitea_list_commits` or `github_list_commits` for what shipped, `melaya_run_diagnosis` for affected runs, `excom_read_tasks` for decisions. Times in UTC; mark gaps where no record exists.
4. Measure impact: duration, products and routes affected, runs failed or interrupted, customers who reported it (counts only). Each number cites its source.
5. Root cause with five whys, each answer backed by evidence, until a cause within the team's control whose removal would have prevented the incident. Then contributing causes by area (code, config and pins, deploy process, monitoring, capacity, handoffs).
6. Check the response: time to detect, declare, mitigate, recover; whether updates reached the incident commander at the cadence the runbook sets; whether a rollback plan existed before the deploy.
7. Actions: specific, owned by a role, dated, with a proof of done (a test, an alert rule, a runbook line). Propose each with `excom_propose_task`. Alert rule changes are proposals, not created here.
8. Draft the known-issues entry (symptom, cause, fix) with `excom_save_draft`.
9. Share the draft with the CQO (test gaps), the COO (customer communication) and the CISO when relevant, using `excom_send_handoff` (kind question).
10. Record detect and recover times with `excom_record_measurement`.

## Output

The review, saved with `excom_save_draft` titled "PIR <short name>", following references/pir-template.md: summary, severity, timeline, impact, root cause, contributing causes, response, actions, known-issues entry.

## Approvals

- Any fix deploy, restart, silence or rollback named in the actions (production).
- Any public status note or customer message (send, by the COO or CXO).
- Edits to knowledge notes outside your own folder (record write).

Blameless: roles and systems, never people at fault. No secrets, internal addresses, customer names or raw run payloads.

## Example

Acme's Web job deployed a config that disabled the job queue for 47 minutes. Timeline from annotations and logs; 212 runs delayed, 3 failed, 2 customer reports. Five whys end at "the deploy check does not verify queue consumers". Actions: add a consumer health check to the deploy runbook (CTO, Friday, proof: runbook line and a red test run), add an alert on queue depth (owner approval).

## References

- references/pir-template.md: the review template and a default severity table. Read at steps 2 and the output (page it in or load with `excom_skill_load`).

Adapted from alirezarezvani/claude-skills (engineering-team/skills/incident-commander), MIT. Modified: rewritten generic for EXCOM.
