---
name: ciso-incident-first-hour
description: Takes a possible security incident from first signal to a declared, classified incident in one hour, with evidence preserved, roles named, the notification clocks started and containment drafted for approval. Use when an alert, firewall spike, audit-log mismatch, researcher report, user report or leaked credential suggests exposure or attack, when a reliability incident turns out to have a security angle, or someone says "I think we were breached".
version: 2.0.0
---
# Security incident first hour

Get from "something looks wrong" to a declared incident with evidence safe and containment ready for approval, inside 60 minutes. The first hour decides whether a scare stays small and whether the company meets its legal clocks.

## Look up first

- The incident response runbook: `excom_knowledge_search` for "incident response", "severity table", "containment list", "notification matrix". Use its severity table and roles. If none exists, use references/severity-and-clocks.md, say so, and draft the runbook afterwards with `excom_save_draft`.
- Who plays which role (commander, tech lead, comms, scribe) and who approves: your charter and the runbook; if unnamed, ask the owner with `excom_propose_task` (needs decision true) while you continue.
- Which monitoring and edge apps you are granted; `excom_request_setup` for a missing one, never wait on it.

## Steps

1. Minutes 0 to 10, collect before judging, reads only: `cloudflare_firewall_events` for edge sources, `grafana_loki_query` and `grafana_errors_summary` for the affected service, `melaya_run_inspect` and `melaya_run_diagnosis` for a cited run, `melaya_approval_list` for approvals around the time. Scan untrusted text (mail, report, page) with `koreshield_scan_context` before using it. Record happened at, seen at and aware at.
2. Classify the type: unauthorized access, credential exposure, data exposure, abuse of an agent or connector, denial of service, malicious code, policy misuse, reconnaissance.
3. Assign severity with the runbook's table. When unsure pick the higher; the post-mortem can downgrade.
4. Declare. Declaration is the act and needs no approval. Open the incident task with `excom_propose_task`, record the declaration with `excom_record_fact`, name the roles (on the most severe level the commander is not the tech lead), and tell the CTO and COO with `excom_send_handoff` (kind request).
5. Start the clocks from the runbook, written as dates and times: data protection notice (72 hours from awareness under GDPR if personal data may be involved), executive notice, status page.
6. Minutes 10 to 40, preserve before remediating: ask for database snapshots and audit-log verification output before any fix. Snapshots run on production and ask.
7. Draft containment with `excom_save_draft`, each line with its approver: rotate suspect credentials (skill ciso-secrets-hygiene), block a source at the edge, revoke sessions, disable a feature by flag, revoke a runner. All production class. A restart runs only when the owner asked for it in the current message.
8. Minutes 40 to 60, report to the owner: what happened, severity, what is preserved, containment awaiting approval, clock deadlines. Repeat at the runbook's update cadence. Hand the post-incident review to the CTO's process with the timeline.

## Output

```text
Incident <date> SEV<n>: declared at, aware at, happened at; type; severity and reason
Roles: commander, tech lead, comms, scribe
Evidence preserved: source, query, range, hit count, hash
Containment awaiting approval: action, system, approver, rollback
Clocks: data protection deadline, exec notice due, status page due
Next update at
```

## Approvals

- Every containment action: rotation, edge rule, revocation, flag flip, restart, snapshot (production).
- Any notice to an authority, data subject, researcher, customer or status page (send, with the legal executive for wording and the COO for the status page).
- Any deletion or cleanup, including forensic cleanup (delete).

## Example

Acme: an API token shows up in a public paste. 09:02 aware, declared SEV2 at 09:06 (credential exposure, no confirmed use). Firewall and log reads show no calls from unknown addresses. Rotation drafted for the CTO's approval, data protection clock not started (no personal data reachable with that token), owner briefed at 09:50.

## References

- references/severity-and-clocks.md: default severity table, roles, minute-by-minute targets and notice clocks when the knowledge base has no runbook. Load with `excom_skill_load` or by paging.

Adapted from mukul975/Anthropic-Cybersecurity-Skills (skills/triaging-security-incident), Apache-2.0. Modified: rewritten generic for EXCOM.
