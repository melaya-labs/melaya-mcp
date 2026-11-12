---
name: cfo-pricing-change-impact
description: Models a proposed price, plan, bundle, coupon or affiliate discount change before it ships. It finds the weak lever in the current pricing from billing data, estimates the effect on customers, revenue and affiliate earnings in three cases, checks mechanics such as coupon cadence and existing subscribers, and writes a migration and rollback memo for the owner. Use when someone proposes a price change, a discount or a new plan, or when checkout starts do not turn into purchases.
version: 2.0.0
---

# Pricing change impact

Prices are the owner's decision. This skill makes the decision informed and, where possible, reversible.

## Look up first

- The current public offer: `excom_knowledge_search` "pricing and plans". The published page wins for anything said to customers. Values that exist only in billing are never quoted as public.
- Affiliate terms, if they exist: `excom_knowledge_search` "affiliate programme terms". A price change also changes affiliate earnings.
- The goal of the change (more customers, more revenue per customer, larger buyers, covering a cost): ask the proposer with `excom_send_handoff` (kind question) if it is not stated.

## Steps

1. Read the live catalogue: `stripe_list_products`, `stripe_list_prices`, `stripe_list_coupons`, `stripe_list_promotion_codes`. List every mismatch with the pricing note, and every undocumented code, first.
2. Read the evidence:
   - The mix by plan (`stripe_list_subscriptions`).
   - Abandonment (`stripe_list_checkout_sessions`, open and expired).
   - Usage against limits on a sample (`melaya_account_usage` through `melaya_tools`, where it applies).
   - Checkout starts and paid conversion by plan, from the CDO.
3. Find the weak lever:
   - Most customers on one plan: packaging.
   - Instant yeses and no objections: price too low.
   - Starts without purchases: price, or trust at checkout.
   - Free users active for months who never pay: the free tier gives the paid reason away.
   With very few paying customers, bracket the price between cost to serve plus fees and the value of the job done, and test with real buyers.
4. Model three cases (low, expected, high), each labelled as an estimate: customers gained or lost, revenue per month, the effect on the outcomes, and the effect on affiliate earnings.
5. Check the mechanics:
   - Existing subscribers: grandfather them or migrate them with notice.
   - Yearly plans and coupon duration: a repeating monthly coupon on a yearly invoice can grant far more than intended.
   - Bundles and referee coupons tied to affiliate tiers.
6. Write the migration and the rollback, with a review signal and date (after the next 20 to 30 paying customers, or 90 days).
7. Ask the revenue role for objections heard and the CMO for the copy change (`excom_send_handoff`). Save the memo with `excom_save_draft`. Record the baselines with `excom_record_measurement`.

## Output

```text
Change: <what>, goal <goal>
Current: price | billing state | public value and read date | match
Weak lever: <diagnosis> (evidence)
Impact (estimates): case | customers | revenue/month | outcome effect | affiliate effect
Mechanics: existing subscribers | yearly and coupons | bundle | referee coupons
Migration, rollback, review signal and date | Approvals needed
```

## Approvals

- Creating or changing a price, product, coupon or promotion code (`stripe_create_price`, `stripe_update_price`, `stripe_create_coupon`, `stripe_create_promotion_code`) always asks. The owner decides.
- Changing affiliate incentives always asks.
- Announcing prices to customers or affiliates is a send, and always asks.

## Example

Acme proposes cutting its mid plan from 49 to 39 USD. Evidence: 60 percent of checkouts expire on that plan. Expected case: plus 12 customers a month, minus 3 percent revenue, and affiliates earn 20 percent less per referral. Recommendation: test a first-month coupon on new accounts instead. It is reversible.

Adapted from TerminalSkills/skills (skills/pricing-strategy/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
