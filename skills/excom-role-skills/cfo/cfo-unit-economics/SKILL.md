---
name: cfo-unit-economics
description: Computes unit economics per product and plan: revenue per account, churn, gross margin, acquisition cost, affiliate share, payback, LTV and LTV to CAC, each labelled healthy, watch or critical, with the top issues and one focus metric. Use when pricing, ads or affiliate decisions are coming, in the monthly close, when the CEO asks which product or plan to push, or when someone asks "are we making money on each customer".
version: 2.0.0
---

# Unit economics per product and plan

Shows where the next customers are cheapest to win and keep. The goal is to put money and effort behind the products and plans that pay back.

## Look up first

- Products, plans and list prices: `excom_knowledge_search` "pricing and plans". Map Stripe prices to them with `stripe_list_products` and `stripe_list_prices`.
- What the company pays to serve a customer, as opposed to what customers pay themselves (for example, inference on their own keys): `excom_knowledge_search` "cost to serve" or "systems and tools". If unclear, ask the owner with `excom_propose_task` (needs_decision).
- Affiliate terms, if there is a programme: `excom_knowledge_search` "affiliate programme terms".

## Steps

1. Before showing each metric, explain it in one sentence: MRR, ARPA, churn, gross margin, CAC, affiliate share, payback, LTV, LTV to CAC.
2. Revenue: `stripe_list_subscriptions` (active) and `stripe_revenue_summary` for the month. Normalise yearly prices to a month. Exclude staff and test accounts per the definitions note.
3. Churn and expansion: from `stripe_list_events` (cancellations, downgrades, upgrades). Below about ten customers per line, report counts, not percentages.
4. Acquisition cost: ad spend (`gads_campaign_performance`, or your ad platform) divided by first-party paid conversions from the CDO. Model a recurring affiliate commission as a share of LTV, not a one-off cost.
5. Cost to serve: company-paid costs per active customer (`melaya_cost_summary` through `melaya_tools`, plus vendor invoices the CFO tracks) and payment fees (`stripe_list_charges`).
6. Compute per product and plan:
   - Gross margin.
   - Payback = CAC / monthly gross margin per customer.
   - LTV = ARPA x margin / churn, capped at 36 months when churn data is thin.
   - LTV to CAC.
7. Label each line for the company's stage: healthy, watch, or critical. Write "too few to judge" instead of scoring a thin line.
8. Pick at most three issues, most damaging first. For each: what is happening, why it matters for the outcomes, and two or three actions for this month. Then name one focus metric with a numeric target.
9. Save with `excom_save_draft`. Record the ratios with `excom_record_measurement`. Hand any price question to the pricing change impact skill.

## Output

```text
Unit economics <month>, read <time>, currency <code>
| Product/plan | Customers | ARPA | Churn | Margin | CAC | Affiliate share | Payback | LTV | LTV:CAC | Status |
Overall: 2 to 3 sentences
Issues (max 3): what / why / fix this month
Working: 1 to 2 points
Focus metric: <metric>, target <number> by <date>
Missing data and assumptions
```

## Approvals

- Nothing here writes outside the team. Price, plan, coupon or affiliate changes that follow are the owner's decision, and always ask.
- Paid data pulls are spend, and ask with the cost.

## Example

Acme's entry plan has an ARPA of 20 USD, 80 percent margin and 8 percent monthly churn, so LTV is 200 USD. CAC from ads is 260 USD: critical. Fix this month: move ad spend to the mid plan (payback 4 months) and add an onboarding check-in to cut churn.

Adapted from alirezarezvani/claude-skills (finance/skills/saas-metrics-coach/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
