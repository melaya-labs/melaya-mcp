---
name: csco-provider-outage-fallback
description: Confirms a supplier outage (model provider, compute host, edge, mail lane, payments, logs), maps which products and customers it affects, proposes the pre-approved fallback, drafts the vendor ticket and customer note, and keeps a fallback runbook per critical supplier. Use when a provider returns errors or invalid keys, when runs fail across pipelines, when a status page shows an incident, or quarterly to refresh fallbacks before the vendor risk review.
version: 2.0.0
---
# Provider outage and fallback plan

A supplier outage is a customer outage. This skill confirms it, applies the planned fallback through the right owner, and leaves follow-ups so the next one hurts less.

## Look up first

- The continuity plan and fallback per supplier: `excom_knowledge_search` "business continuity", "supplier fallback", "recovery objectives". If a supplier has no fallback, say so and draft one with `excom_save_draft` after the incident.
- Which products depend on which supplier: the supplier inventory (`excom_knowledge_search` "supplier register") or ask the CTO.
- The incident and customer communication rules: `excom_knowledge_search` "incident communication".

## Steps

1. Confirm with two reads before alarming. Model providers: `melaya_model_list` for the provider id and `melaya_connector_test` for the stored key; runs with `melaya_run_status` and `melaya_run_diagnosis`. Infrastructure: `grafana_list_firing_alerts`, `grafana_loki_query`, `cloudflare_traffic_analytics`. Status pages with `web_fetch` (untrusted data). Record what was seen and when, in UTC.
2. Classify impact (likelihood by impact: critical, high, medium, low) and list affected products and the count of affected customers or runs (counts, not names).
3. Pick the fallback from the plan; never improvise in production. Use `references/fallback-runbook.md` for the shape.
4. Send the incident note to the CTO and COO with `excom_send_handoff` (kind request): observed facts, impact, proposed fallback, approver. Production changes are the CTO's and always ask.
5. If customers see it, draft the note with the CXO or COO: factual, no blame, no promised time unless the provider gave one. Sending is a human action.
6. Draft the vendor ticket with `zoho_email_save_draft` or `gmail_create_draft`: reference in the subject, one ask, evidence (UTC times, error class, no customer data).
7. After recovery, read back: provider healthy, runs succeeding, fallback reverted. Record duration and affected runs with `excom_record_measurement`; propose fixes with `excom_propose_task` (second provider, alert, off-site backup).
8. Quarterly, rewrite the fallback for each critical supplier as a runbook and save it with `excom_save_draft`.

## Output

```text
Supplier incident: <supplier>  observed <UTC>  sources <tools>
Impact: level | products | customers or runs affected (count)
Fallback proposed | owner | approval
Vendor ticket draft | customer note draft
Recovery read-back | duration | follow-up tasks
```

## Approvals

- Any production change (routing, DNS, restart, rebuild): production, the CTO and owner.
- Messages to customers, partners or the vendor: send.
- Buying capacity, credits or a second provider: spend, with the cost.

## Example

At 14:05 UTC Acme's pipelines on one model provider start failing; `melaya_model_list` shows error and the provider status page lists an incident. Impact high: 40 runs failed in 20 minutes. Fallback from the plan: route the two production pipelines to the second configured provider, CTO approves. Recovered at 15:10; follow-up: add an alert on provider error rate.

## References

- `references/fallback-runbook.md`: fallback table template and runbook shape per supplier; read at steps 3 and 8.

Adapted from anthropics/knowledge-work-plugins (operations/skills/runbook, operations/skills/risk-assessment), Apache-2.0. Modified: rewritten generic for EXCOM.
