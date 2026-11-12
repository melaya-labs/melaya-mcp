---
name: coo-service-level-misses
description: Handles a missed service level: runs lost in a deploy, edge 5xx errors that look like app failures, approvals or replies waiting too long, paused triggers. It sets a severity, finds the likely cause, routes the fix, drafts the status update and user reply, and writes a blameless postmortem, turning repeats into fixes. Use when a red threshold trips, when a user or partner reports a failure, after a deploy, or for the weekly misses count.
version: 2.0.0
---

# Service-level misses

Every miss is a risk to activation and to paying customers. Classify it, get the right owner moving, tell users clearly, and fix what repeats.

## Look up first

- The service levels and red thresholds: `excom_knowledge_search` "service levels". If missing, use the defaults in the weekly ops review skill, label them "default", and propose them to the owner.
- Who executes production fixes (operator, CTO) and how to reach them: `excom_knowledge_search` "escalation" or "on-call".
- The user reply tone and the support mailbox: `excom_knowledge_search` "communication patterns".

## Steps

1. Detect:
   - `melaya_run_diagnosis` and `melaya_eval_report` through `melaya_tools`.
   - `cloudflare_traffic_analytics` by status.
   - `melaya_approval_list`.
   - `melaya_pipeline_trigger` for paused reasons.
   - The support inbox.
   - `grafana_list_firing_alerts` or `sentry_list_issues`, if granted.
2. Set the severity:
   - SEV1: down for all users.
   - SEV2: a major feature degraded for many users.
   - SEV3: a minor feature affected for some users.
   - SEV4: low impact.
   Signup, checkout and payments are at least SEV2 while a customer outcome is open.
3. Find the likely cause before proposing anything:
   - Edge 520 and 522 mean the edge could not reach the origin. 524 means a wait over 100 seconds.
   - App responses carry CORS headers; edge error pages do not, so a "CORS error" is often an edge error.
   - Correlate with the last deploy (your code host's commits) and with firewall events (`cloudflare_firewall_events`).
4. Route the fix with `excom_send_handoff` (kind request), with the run id kept inside the team:
   - Production to the CTO and the operator.
   - Support patterns to the customer experience role.
   - Vendor blockers to the supply role.
   - Possible credential exposure straight to the security role, never quoted.
5. Draft the status update and the user reply (`zoho_email_save_draft` or `gmail_create_draft`): plain text, what happened, what was done, no internal ids.
6. After resolution, write a blameless postmortem using references/postmortem-template.md, and save it with `excom_save_draft`.
7. Record the miss (service level, duration, severity) with `excom_record_measurement`. A third miss of the same kind becomes a fix proposal (`excom_propose_task`), and a pipeline candidate if recovery is manual.

## Output

```text
Miss: <service level> | SEV<n> | status | started | resolved
Evidence: tool, window, values | Likely cause, confidence
Routed: role | request | due
Drafts: status update, user reply
Postmortem (after resolution) | Weekly count: service level | misses | repeats
```

## Approvals

- Restarts, rollbacks, migrations, edge or firewall changes and kill switches are production, and always ask. The operator or owner executes them.
- Sending replies, status updates or status page posts is a send, and always asks.
- Resuming triggers and creating external issues are record writes, and ask.

## Example

Users report "CORS errors" at Acme. The edge shows 41 errors of class 522 in an hour, starting right after a deploy. Set as SEV2. The CTO and operator are asked to check origin health and roll back. The user reply is drafted. The postmortem follows the next day.

## References

- references/postmortem-template.md: the postmortem layout with five whys and action items. It loads with `excom_skill_load`.

Adapted from anthropics/knowledge-work-plugins (engineering/skills/incident-response/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
