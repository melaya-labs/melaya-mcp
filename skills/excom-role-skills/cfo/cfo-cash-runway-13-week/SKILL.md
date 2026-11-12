---
name: cfo-cash-runway-13-week
description: Builds a week-by-week cash view for the next 13 weeks. It covers the opening balance, inflows placed by payout lag, committed outflows, the closing balance with low and high bands, runway in weeks, and the risks that could push cash below the floor. Use when running the weekly cash read, before any large spend or pricing decision, when a dispute or failed payout lands, or when the owner asks "how long can we last" or "can we afford this".
version: 2.0.0
---

# Cash and runway, 13-week view

How long the company can last decides how hard it can push its outcomes. This view makes that number concrete, with its uncertainty.

## Look up first

- The cash floor, the approved budgets and the reporting currency: `excom_knowledge_search` "budget and thresholds". If missing, ask the owner with `excom_propose_task` (needs_decision).
- Which accounting system is the company's books: `excom_knowledge_search` "systems of record". Never use figures from a database that is not confirmed as the company's own books.
- Known commitments: `excom_knowledge_search` "vendor inventory", plus renewal mail.

## Steps

1. Read the opening balance: `stripe_get_balance` (available and pending per currency) and `stripe_list_payouts` (arrival dates). For the bank side, use `quickbooks_get_cash_position` or `xero_get_cash_position` when that system is granted and confirmed. Otherwise ask the owner for the balance and its date. With no confirmed balance, head the view "net change only". Never assume a balance.
2. Read recurring inflows from `stripe_list_subscriptions` (active, trialing, past_due) by renewal date. Use `stripe_preview_upcoming_invoice` for large renewals. Count trialing and past_due only in the high band.
3. Measure payout lag from charge to payout with `stripe_list_recent_charges` and `stripe_list_payouts`, and use it to place inflows in the right week.
4. List outflows:
   - SaaS renewals and vendor invoices, from mail (`gmail_list_threads`, `zoho_email_search`) and the vendor inventory.
   - Affiliate payouts due, with `affonso_list_payouts` (if on Affonso).
   - Ads pacing, with `gads_budget_pacing`.
   - Payroll and contractors, from the owner.
   Items with no connector are entered from the invoice, or labelled as an estimate.
5. Build two bands. Low: slowest observed lag, trialing and past_due excluded, estimates at their high end. High: every renewal collected on time. With fewer than three payouts on record, use plus or minus 30 percent and say so.
6. Runway in weeks = closing cash in the low band / average weekly net burn.
7. Name at most five risks, largest first, each with its amount and week.
8. Record cash, burn and runway with `excom_record_measurement`. Save the view with `excom_save_draft`. If the low band crosses the floor within 13 weeks, raise it to the owner with `excom_propose_task` (needs_decision).

## Output

```text
13-week cash, read <time>, currency <code>, opening <amount> as of <date> (source)
| Week | Inflows | Outflows | Net | Closing | Low | High | Notes |
Runway (low band): N weeks | Weekly burn: amount
Risks: risk | amount | week | owner
```

## Approvals

- Payments, payout approvals, refunds, cancellations and budget changes are spend, and always ask with the amount.
- Writing to a sheet, a document or the books is a record write, and asks.
- Sharing the view outside the team is a send, and asks.

## Example

Acme opens with 120k USD as of Monday (bank, owner-confirmed). Weekly burn in the low band is 9k, so runway is 13 weeks. Risk: an annual tool renewal of 18k lands in week 4 while 11k sits in pending payouts.

Adapted from anthropics/knowledge-work-plugins (small-business/skills/cash-flow-snapshot/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
