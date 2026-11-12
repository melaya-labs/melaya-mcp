# Commission checks

Run every check on every commission, not on a sample. Each check names what to read and what counts as a hit.

## Exclusions (from the programme terms)

| Check | How to read it | Hit |
|---|---|---|
| Self-referral | Compare the affiliate's email and domain (`affonso_get_affiliate`) with the customer's (`stripe_get_customer`) | Same email, or same company domain when the terms exclude the affiliate's own company |
| Existing account | The customer was created (`stripe_get_customer`, created date) before the referral date (`affonso_get_referral`) | The customer existed before the referral |
| Duplicate person | Several referred customers share a card fingerprint or billing details (`stripe_list_payment_methods`) | Same payment method across accounts |
| Staff or test | The definitions note's exclusion rule | Matches the rule |
| Platform fraud rules | `affonso_get_fraud_rules` | Note what the platform already blocks, so you do not double count |

## Rate and duration

- Use the rate of the affiliate's group on the invoice date, not today's rate.
- Recurring terms: renewals count until the duration ends. One-time terms: only the first payment counts.
- The base is the amount paid after discounts, excluding tax, unless the terms say otherwise.

## Tier changes

If the terms limit tier changes (for example, a cooldown between switches, or no move to a higher commission for some months after joining a discounted tier), check the affiliate's group history. A rate higher than the terms allow at the invoice date is an adjustment.

## Referee discounts

If a tier gives referred customers a discount through coupons, read `stripe_list_coupons` and `affonso_list_coupons`. Each affiliate in a discounted tier should have exactly one coupon at the tier's discount. Mismatches are coupon drift: report them to the owner and the revenue role. The CFO never fixes coupons.

## Referral at checkout

The checkout session that created the subscription should carry the affiliate referral (`stripe_get_checkout_session`, metadata). If Stripe shows a referral that is missing in the affiliate platform, that is leakage: report it to the CDO and the revenue role.

## Aging buckets

| Age | Status | Action |
|---|---|---|
| 0 to 30 days | Open | Normal, inside the hold |
| 31 to 60 days | Aging | Follow up with the affiliate owner role |
| 61 to 90 days | Overdue | Escalate to the owner |
| Over 90 days | Stale | Propose a reversal or a write-off |
