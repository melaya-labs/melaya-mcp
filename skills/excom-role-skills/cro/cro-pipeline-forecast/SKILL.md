---
name: cro-pipeline-forecast
description: Reconciles every lead source (CRM, ledgers, billing, affiliate platform, mailboxes) into one graded pipeline, forecasts customers against the team's goal, and lists the decisions the owner must make this week. Use when it is time for the weekly pipeline review, before a board or CEO review, when the forecast moves a lot, or when someone asks "are we on track", "what's in the pipeline" or "how many customers will we have".
version: 2.0.0
---

# Weekly pipeline review and forecast

One graded view and an honest forecast against the goal, because scattered sources hide both stalled deals and missed targets.

## Look up first

- The customer goal, its deadline and milestones in the team's outcomes (in context). If the goal has no milestones, propose a straight line and ask the owner with `excom_propose_task` (needs decision true).
- Last week's forecast: `excom_recall` "pipeline forecast".
- Metric definitions (paying customer, staff and test exclusions): `excom_knowledge_search` "metrics definitions"; if missing, ask the CDO.
- Where the pipeline of record lives (CRM or ledgers): search "pipeline of record"; if undecided, read all and flag the gap.

## Steps

1. Money first: `stripe_revenue_summary`, `stripe_list_subscriptions` (new active), `stripe_list_checkout_sessions` (not completed). Count paying customers only from billing, without staff or comped accounts.
2. Funnel: `posthog_compute_funnel` or `ga4_run_funnel_report` when granted, else ask the CDO (`excom_send_handoff` kind question).
3. Pipeline: `hubspot_list_deals` or `odoo_crm_opportunity_list`, ledgers with `sheets_read_range`, activities with `odoo_activity_list`; partner and affiliate sourced deals with `affonso_list_referrals` and `affonso_get_affiliate_analytics` if your affiliate platform is Affonso.
4. Grade each opportunity with references/grading.md. No dated next step means not commit.
5. Inspect commit and best case with four questions: what changed, is the next step verifiable and owned, what negative signals exist, what backfills it if it slips.
6. Forecast: customers to date plus weighted commit, best case and pipeline, by product and source. State the weights as assumptions. Compare with the run rate the goal needs.
7. Check guardrails (references/grading.md). On a breach, escalate to the CEO with `excom_send_handoff` kind request and a short memo.
8. Write the owner's decision list (terms, discounts, activations, replies waiting), each with a default. Copy money lines to the CFO.
9. Record customers, commit and forecast with `excom_record_measurement`, and the forecast with `excom_record_fact` for next week.

## Output

```text
Week of <date> | Paying customers: <n> (billing, read <date>) | Needed run rate: <n>/week
Forecast to goal date: <n> = commit <n> x w1 + best case <n> x w2 + pipeline <n> x w3
By source: direct <n>, affiliate <n>, partner <n>
Changes since last week (with reasons) | Guardrail breaches | Decisions for the owner
```

Plus the graded table; saved with `excom_save_draft`.

## Approvals

- Stage changes, CRM and ledger writes: record write under the team's autonomy.
- Messages to move a deal: send class.
- Discounts, terms or exceptions in the decision list: the owner only.

## Example

Goal N customers by day 90, day 40 today, 14 paying. Commit 6, best case 10, pipeline 30. Forecast 14 + 4.2 + 3 + 3 = 24 by day 90 at current rates: behind the line; decision asked: "approve two partner co-marketing actions to add pipeline".

## References

- references/grading.md: grade exit criteria, default weights and guardrails. Read at step 4; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/sales-pipeline/skills/forecast-discipline/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
