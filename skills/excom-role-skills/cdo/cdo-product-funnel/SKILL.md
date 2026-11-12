---
name: cdo-product-funnel
description: Builds the funnel for each product, from sessions to registration, activation, return and paid, using first-party events with GA4, PostHog and Stripe as supporting views. It finds the stage that loses the most would-be paying users, reads cohort retention, and flags instrumentation errors. Use when running the weekly metric review, before growth, pricing or onboarding decisions, after a product launch, or when someone asks "where do we lose people" or "why aren't signups converting".
version: 2.0.0
---

# Funnel analytics per product

The customer outcome is won at the blocking stage, not everywhere at once. Show each product's funnel and name that stage.

## Look up first

- The product list and the first successful outcome that defines activation for each product: `excom_knowledge_search` "metrics definitions" and "products". If a product has no activation definition, propose one to the owner. Do not guess it.
- The staff and test exclusion rule and the cohort rule: the same note.
- Which analytics apps are granted. Call `excom_request_setup` for PostHog or GA4 if a needed one is missing.

## Steps

1. Define the stages per product: awareness (sessions by channel), registration, activation (the product's first successful outcome), return within 7 days, first paid checkout. State the cohort: users registered in the window.
2. Read the first-party counts for 7 and 28 days from the team's funnel source (admin export or warehouse, per the definitions note). Add context views: `ga4_run_funnel_report` for landing to signup, and `posthog_compute_funnel` or `posthog_query_trends` for in-product steps.
3. Read paid conversion by product: `stripe_list_subscriptions` and `stripe_list_checkout_sessions`, with prices mapped to products, staff and test excluded.
4. Compute the conversion and the median time between stages. The bottleneck is the stage with the largest absolute loss of would-be paying users, not the lowest rate.
5. Retention: build a weekly cohort table per product (week 1, 2, 4). A flattening curve means a habit is forming; a curve heading to zero means none is. Split by channel, and by affiliate-referred against not.
6. Activation signals: which first actions are followed by paying. Report them as correlations, never as causes.
7. Data quality: a product funnel at zero while its ground-truth table has rows is an instrumentation error, not a business result. Flag it and do not interpret that product.
8. Save with `excom_save_draft`. Record the per-product conversion with `excom_record_measurement`. Send the bottleneck and one proposed fix or experiment to the product and marketing roles with `excom_send_handoff` (kind request).

## Output

```text
Funnel per product, 7d and 28d, cohort registered in window, read <time>
| Product | Sessions | Registered | Activated | Returned 7d | Checkout started | Paid | Biggest loss stage | Median time to activate |
Retention cohorts: product | cohort | W1 | W2 | W4
Signals linked to paying (correlation) | Data-quality flags
Focus: product | stage | change | owner | signal date
```

## Approvals

- Creating key events, audiences, custom definitions or annotations in GA4 or PostHog is a record write, and asks.
- Paid data pulls are spend and go through the CFO.
- Sharing per-product numbers outside the team needs the owner.

## Example

Acme product B: 900 registered, 310 activated, 40 checkout starts, 6 paid. Product A: 300 registered, 60 activated, 30 starts, 18 paid. B's biggest absolute loss sits between activation and checkout. Proposal: an in-product upgrade prompt after the third successful use (owner CPO, signal: checkout starts within 2 weeks).

Adapted from TerminalSkills/skills (skills/product-analytics/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
