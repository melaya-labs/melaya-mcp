---
name: cro-trial-to-paid
description: Finds free and trialing accounts at a real upgrade moment (value seen, limit reached, checkout abandoned) from billing and usage signals, and drafts the matching offer from the published plans only. Use when converting free users to paid, when checkouts are started but not finished, when users hit plan limits, or when someone asks "who is ready to upgrade" or "why don't trials convert".
version: 2.0.0
---

# Trial-to-paid conversion

Converts users at the moment they have seen value, with an offer the published plans already allow, because an early or invented offer costs trust and margin.

## Look up first

- The paying-customer goal in the team's outcomes, and your charter objectives (in context).
- Plans, limits, standalone products and billing rules: `excom_knowledge_search` "pricing and plans". Quote nothing that is not there.
- Who counts as a user and which accounts to exclude (staff, test, comped): search "metrics definitions". If missing, ask the CDO with `excom_send_handoff` kind question.
- Referral discounts that already apply at checkout: search "affiliate programme terms".

## Steps

1. Build the cohort: `stripe_list_subscriptions` (trialing, active), `stripe_list_checkout_sessions` (not completed), `stripe_search_customers`; usage through `melaya_tools`; funnels with `posthog_compute_funnel` or `ga4_run_funnel_report` when granted, else `excom_request_setup` or ask the CDO.
2. Tag each account with one moment: value seen (a successful use, then a return), limit reached, checkout abandoned, payment at risk, or no value yet.
3. If no value yet, hand to the CXO (trial rescue) and make no offer, because an upgrade ask before value loses the user.
4. If payment at risk, route to the CFO; no offer.
5. Otherwise map to one offer the pricing note allows: the single-surface product, the next plan up, the yearly option where published, or a contact-sales path for teams. If the user was referred with a referral discount, it already applies; never add another.
6. Draft: what they achieved in their own usage, what the limit or plan changes, one link, an easy "not now". Under 90 words. `gmail_create_draft` (draft) and `excom_save_draft`.
7. One upgrade message per account per week across CRO and CXO: check `excom_read_tasks` first.
8. Ask for the send (send class). Record new paying accounts this week with `excom_record_measurement` and hand each to the CXO for onboarding.

## Output

```text
| Account | Plan now | Moment | Evidence (dated) | Offer (from the pricing note) | Draft id | Status |
Cohort: <n> | per moment: <counts> | converted this week: <n>, source of each
```

## Approvals

- Every message to a user: send class.
- Any billing write (payment link, checkout, subscription, coupon, promotion code): spend, always asks.
- Discounts, trial extensions, seat exceptions, custom quotes: the owner only.

## Example

Acme Studio used all free runs in 4 days with 9 successes and came back daily. Moment: limit reached. Offer: the entry paid plan from the pricing note. Draft: "You ran 9 workflows this week and hit the free limit. The next plan gives you N runs a month. Upgrade here, or reply 'not now'."

Adapted from coreyhaines31/marketingskills (skills/paywalls/SKILL.md), MIT licence. Modified: rewritten generic for EXCOM.
