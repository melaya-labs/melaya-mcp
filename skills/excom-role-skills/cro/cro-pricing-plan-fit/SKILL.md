---
name: cro-pricing-plan-fit
description: Recommends exactly one plan or standalone product for a stated need, quoting only the company's published price list, and routes anything off-list (discounts, custom quotes, seat exceptions) to the owner. Use when a prospect asks "which plan do I need" or "how much is it", when a limit blocks a user, when a pricing objection appears, or when a partner needs a plan for a client.
version: 2.0.0
---

# Pricing and plan fit

One recommendation with the two facts that decided it, because most "too expensive" conversations are plan-fit mistakes.

## Look up first

- The published plans, limits, standalone products, bundles and yearly options: `excom_knowledge_search` "pricing and plans", then `excom_knowledge_read`. Use the public price list over internal catalogs when they differ. If the note is missing or stale, ask the CFO (`excom_send_handoff` kind question) and quote nothing.
- What is contractual rather than built (SSO, SLA, private deployment): same note or "claims policy".
- Referral discounts that apply at checkout: search "affiliate programme terms".

## Steps

1. Qualify with seven facts: usage volume a month, cloud or own machines, seats, projects, schedules and triggers, which surface or product, who approves actions.
2. If they have an account, read instead of asking: subscription and usage through `melaya_tools`, `stripe_list_customer_subscriptions`, `stripe_get_subscription`. Missing app: `excom_request_setup` with service id "stripe".
3. Build the fence table from the pricing note with references/fit-table.md, then pick the smallest option that covers all seven facts, because oversizing loses the deal and undersizing loses the customer.
4. Write the recommendation: the plan or product, the two deciding facts, the price exactly as published with the note's date, the yearly option if published, the one limit to know. Mention a referral discount only if it already applies; never add one.
5. If a price looks inconsistent, verify with `stripe_list_prices` and the CFO before quoting.
6. Off-list asks (discount, promo code, custom quote, seat exception, currency, invoice terms, refund) go to the owner with evidence and a default recommendation: `excom_send_handoff` kind request to the CEO and a decision draft with `excom_save_draft`. Never hint a discount is possible.
7. Draft the reply (`gmail_create_draft`, draft) and record the outcome in the CRM (`hubspot_update_deal` or `odoo_crm_lead_update`, record write).
8. Log recurring plan-shape objections for the monthly review with the CFO and CMO (`excom_propose_task`).

## Output

```text
Need: <their words> | Deciding facts: <two>
Recommendation: <plan or product>, <price as published>, <yearly if published>
Limit to know: <one> | Referral discount: <applies | none>
Off-list asks: <none | sent to owner on date> | Source: <pricing note, date>
```

## Approvals

- Sending the recommendation or proposal: send class.
- Any billing write (checkout, payment link, coupon, promotion code, subscription change): spend.
- Any discount, custom quote, seat exception, refund or term: the owner only.

## Example

Acme Labs: 2 people, 300 runs a month, schedules every hour, cloud only. The pricing note's fence for hourly schedules starts at the team plan, so recommend it with its published monthly and yearly price; limit to know: seat count.

## References

- references/fit-table.md: how to build the fence table from the pricing note, and the rules for contractual items. Read at step 3; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/pricing-strategy/skills/packaging-framework/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
