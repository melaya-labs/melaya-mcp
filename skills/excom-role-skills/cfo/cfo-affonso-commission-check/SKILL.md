---
name: cfo-affonso-commission-check
description: Reconciles affiliate commissions with real payments before a payout cycle. Each commission must rest on a paid, external Stripe invoice at the rate of the affiliate's terms, net of refunds and disputes, and free of self-referral or excluded accounts. Payouts always ask. Use when monthly payouts approach, when a commission looks large, when a referred customer refunds or disputes, when an affiliate changes tier, or when someone asks "are these commissions right".
version: 2.0.0
---

# Affiliate commission check

Every commission must trace to money that actually arrived, at the agreed rate. That keeps the affiliate programme trusted and stops payouts leaking cash. Written for Affonso; the same checks apply on any affiliate platform.

## Look up first

- The programme terms: `excom_knowledge_search` "affiliate programme terms". You need the rates per tier, the duration, the attribution window, the approval hold, the payout threshold, the exclusions, any tier-change rules, and any referee discounts. If the note is missing, draft it from `affonso_get_payment_terms` and `affonso_list_groups` with `excom_save_draft`, and ask the owner to confirm it with `excom_propose_task` (needs_decision). Reconcile only against confirmed terms.
- The active affiliate definition: `excom_knowledge_search` "metrics definitions". The suggested default: an affiliate with at least one referred signup.

## Steps

1. Compare the live terms (`affonso_get_payment_terms`, `affonso_list_groups`, `affonso_get_group`) with the terms note. Any difference goes to the owner before anything else.
2. List the commissions that are pending or ready for payment (`affonso_list_commissions`). For each, read `affonso_get_commission` and `affonso_get_referral`.
3. Match each commission to Stripe. Find the customer with `stripe_search_customers`, then the invoice with `stripe_get_invoice`. The invoice must be paid, belong to an external account, and carry the affiliate's referral at checkout.
4. Recompute the amount: the paid amount, net of discount and tax, times the rate in force on the invoice date for that affiliate's tier. Renewals count only if the terms make the commission recurring.
5. Net out refunds and disputes: `stripe_list_refunds`, `stripe_list_credit_notes`, `stripe_list_disputes`.
6. Run the exclusion and tier checks in references/commission-checks.md: self-referral, the affiliate's own company, existing accounts, tier-change rules, and referee coupons against groups (`stripe_list_coupons`, `affonso_list_coupons`).
7. Classify each line:
   - Matches.
   - Timing: inside the hold, or the invoice is unpaid. It clears on its own.
   - Adjustment: wrong rate, or a refund not netted.
   - Investigate: no invoice behind it, an exclusion hit, or coupon drift.
   Age the open items: follow up at 31 to 60 days, escalate at 61 to 90, propose a reversal after 90.
8. Draft the approval list with `excom_save_draft`. Ask the revenue or partnerships role for affiliate context (`excom_send_handoff`, kind question). Record the totals with `excom_record_measurement`.

## Output

```text
Commission check, cycle <period>, read <time>
Terms: tier | rate | duration | discount | matches note (yes/no)
| Commission | Affiliate (masked) | Tier | Invoice | Paid | Expected | Claimed | Refund/dispute | Exclusion | Category | Age | Action |
Totals: approve | question | reverse | payouts due (currency)
```

## Approvals

- Approving, changing or reversing a commission (`affonso_update_commission`, `affonso_refund_conversion`) and any payout change (`affonso_update_payout`) is spend. It always asks, and the owner approves.
- Changes to terms, groups, coupons or fraud rules always ask, and are never put under a standing rule. Deletions are never proposed.

## Example

An affiliate at Acme claims a commission on a 49 USD invoice. Stripe shows the invoice paid and then fully refunded 10 days later. Category: adjustment. Proposed action: reverse the commission, for the owner to approve.

## References

- references/commission-checks.md: the exclusion, tier and coupon checks with how to read each one. Load it with `excom_skill_load` before step 6.

Adapted from anthropics/knowledge-work-plugins (finance/skills/reconciliation/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
