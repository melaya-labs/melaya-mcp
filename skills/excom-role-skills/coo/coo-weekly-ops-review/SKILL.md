---
name: coo-weekly-ops-review
description: Writes the weekly operations report for the CEO and the owner, readable in two minutes. It gives green, amber or red per area (platform, runs, edge errors, approvals, schedules and triggers, inbox, goal-linked operations), red items first, with metrics against target, risks, decisions needed and next week's priorities. Use when the week ends, after a deploy week or an incident, or when someone asks "how are operations" or "what broke this week".
version: 2.0.0
---

# Weekly operations review

One report, red items first, so the CEO's decisions rest on how operations actually ran.

## Look up first

- Service levels and red thresholds per area: `excom_knowledge_search` "service levels" or "operations thresholds". If missing, use the defaults below, label them "default", and propose them to the owner.
- The week's daily summaries and red items: `excom_recall`.
- The report's day and destination: `excom_knowledge_search` "weekly rhythm".

## Steps

1. Platform: `melaya_setup_status` and `melaya_runner_status` through `melaya_tools`. Note any runner that is offline or on an old release.
2. Runs: `melaya_eval_report` for acceptance and failure kinds, and `melaya_run_diagnosis` on runs ended by a restart. Default red: any run lost to a restart, or daily acceptance under 90 percent.
3. Edge: `cloudflare_traffic_analytics` by status (or your edge provider). Default red: more than 10 errors of one 5xx class in 24 hours, or a spike after a deploy. If the app is missing, call `excom_request_setup`.
4. Approvals: `melaya_approval_list`. Default red: anything pending more than 24 hours.
5. Schedules and triggers: `melaya_pipeline_trigger` (get, events) and `excom_pipeline_status`. Red: any auto-pause or failing verdict.
6. Inbox and support: the support mailbox (`zoho_email_list` or `gmail_list_threads`). Count threads waiting more than a business day. When the same question comes in three times, propose a docs or product fix.
7. Goal-linked operations: open failed payments (CFO), affiliate applications waiting (revenue or partnerships role), partner threads waiting (CEO). Ask each with `excom_send_handoff` (kind question).
8. Status per area. Lead with a three-line headline. Give each risk its mitigation and owner, and each decision needed its context, deadline and recommendation.
9. Save with `excom_save_draft`. Send the link to the CEO with `excom_send_handoff` (kind request). Record the weekly values with `excom_record_measurement`.

## Output

```text
Operations review, week <range>, overall green/amber/red
Headline: 3 lines, red first
Metrics: metric | target | actual | trend | status | source
Done (verified only) | In progress: item | owner | ETA
Risks: risk | impact | mitigation | owner
Decisions: decision | context | deadline | recommendation
Next week: 1 to 3 priorities
```

## Approvals

- Posting or emailing the report is a send, and asks.
- Fixes that touch production (restart, migration, edge setting, deploy) are executed by the operator after approval, never by the COO.
- Resuming triggers or schedules and creating issues are record writes, and ask.

## Example

Headline: "Red: 3 runs lost during Tuesday's deploy. Amber: two approvals waited more than 2 days. Green: inbox under one day." Decision: "Move deploys to the low-traffic window (recommendation: Thursday 06:00)?"

Adapted from anthropics/knowledge-work-plugins (operations/skills/status-report/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
