---
name: cxo-health-signals
description: Scores paying and trialing accounts from usage, value, support and billing signals with an explicit coverage rule for missing data, flags early churn signals, and picks the intervention and owner for each at-risk account. Use when running the weekly account health check, on a failed payment, cancellation or downgrade, when a paying account keeps hitting errors, or when someone asks "who is about to churn".
version: 2.0.0
---

# Churn and health signals

The best save happens before the customer clicks cancel, and every early customer kept counts twice: one not lost and one reference won.

## Look up first

- Customer and retention goals in the team's outcomes (in context).
- Who counts as a customer and which accounts to exclude: `excom_knowledge_search` "metrics definitions"; else ask the CDO.
- Billing rules (what happens on a failed payment, grace periods): search "pricing and plans", "billing rules".
- Save-offer policy: search "retention offers". None recorded means no save offers; ask the owner if one is needed.

## Steps

1. Read billing: `stripe_list_subscriptions` (active, trialing, past due), `stripe_list_invoices` (failed), `stripe_list_events` (cancellations, downgrades). Missing app: `excom_request_setup` with service id "stripe".
2. Read usage through `melaya_tools` (account usage, run status); trends with `posthog_query_trends` when granted.
3. Read support: sweep notes, `zoho_email_search`, `discord_get_messages`; `intercom_search_conversations` and `intercom_csat_summary` when granted.
4. Score with references/health-score.md. Missing or stale signals are unavailable, not zero; report coverage, and below the coverage floor write "insufficient data", because a guessed score triggers the wrong action.
5. Flag leading signals regardless of score (references/health-score.md).
6. Intervene by cause: setup or failure, a precise fix (cxo-support-macros, cxo-activation-paths); usage drop without failures, a value-first note; limit reached or upgrade intent, hand to the CRO; payment failure, refund or cancellation about money, route to the CFO with no save offer unless the policy allows it; critical paying accounts, a personal note drafted for the owner.
7. Draft each intervention (draft) and ask for the send. Log every cancellation cause for cxo-feedback-to-cpo.
8. Monthly, back-test: did at-risk flags precede cancellations? Change weights only on that evidence. Record accounts by tier with `excom_record_measurement`.

## Output

```text
| Account | Plan | Score | Coverage | Tier | Leading signals (dated) | Cause | Intervention | Owner | Due |
Count by tier | newly at risk | cancellations this week with causes
```

## Approvals

- Every message to a customer: send class.
- Discounts, pauses, credits, refunds, plan changes or any billing write: spend, the CFO and owner decide.
- Dunning emails: always ask.

## Example

Acme Legal (team plan): runs down 60 percent in two weeks, last 9 runs failed on the same expired connector token, no reply to the last mail. Score 41 at 85 percent coverage, at risk. Cause: setup. Intervention: the reconnect macro plus a short personal note.

## References

- references/health-score.md: component weights, coverage rule, tiers and leading signals. Read at steps 4 and 5; loads with `excom_skill_load` (section) or by paging.

Adapted from coreyhaines31/marketingskills (skills/churn-prevention/SKILL.md), MIT licence, and gtmagents/gtm-agents (plugins/customer-success/skills/risk-scoring-framework/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
