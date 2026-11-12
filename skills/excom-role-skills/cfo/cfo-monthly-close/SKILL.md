---
name: cfo-monthly-close
description: Runs the month-end close in dependency order across billing, the affiliate platform, the accounting system and the usage ledger. It covers reconciliations with categorised and aged items, flux checks with drivers, and a close brief the owner can trust. Use when a month ends and the next begins, when the monthly report needs final numbers, or when someone asks "are the books closed" or "why don't these numbers match".
version: 2.0.0
---

# Monthly close checklist

Close each month in a fixed order, so the numbers in reports and goal trackers are final, reconciled and explained.

## Look up first

- Which system is the company's books (QuickBooks, Xero or other) and whether it is confirmed: `excom_knowledge_search` "systems of record". If no accounting app is granted, call `excom_request_setup`. Until then, close on billing and the affiliate platform only, and say so.
- The close calendar, variance thresholds and approval thresholds: `excom_knowledge_search` "close calendar" or "budget and thresholds". If missing, use the defaults in the checklist.
- Last month's close brief: `excom_recall`.

## Steps

1. Work the checklist in references/close-checklist.md, level by level. Never start a level before the one below it is reconciled, because a later reconciliation built on unreconciled inputs hides the real difference.
2. Level 1 (no dependencies):
   - `stripe_revenue_summary`, `stripe_list_payouts`, `stripe_list_refunds`, `stripe_list_credit_notes`, `stripe_list_disputes`.
   - Commissions: `affonso_list_commissions` (if on Affonso).
   - Vendor invoices from mail.
3. Level 2:
   - Payouts against bank deposits (`quickbooks_get_cash_position` or `xero_get_bank_summary`).
   - Commissions against paid invoices (the commission check skill).
   - Deferred revenue for yearly plans.
4. Level 3:
   - A usage-to-plan sample: `melaya_account_subscription` and `melaya_account_usage` against `stripe_get_subscription_details`. Mismatches go to the admin as a list.
   - The open items list: `quickbooks_get_month_end_close_checklist` or `xero_get_trial_balance`.
5. Level 4:
   - Draft the P&L (`quickbooks_get_profit_and_loss` or `xero_get_profit_and_loss`).
   - Flux check against last month and budget. Explain every line over its threshold with a one-line volume or rate driver.
6. Categorise each reconciling item as timing, adjustment (a human posts the entry) or investigate, and age it.
7. Write the close brief with `excom_save_draft`. Record the month's figures with `excom_record_measurement`. Insert into the monthly report only after approval. Propose one fix for whatever slowed the close with `excom_propose_task`.

## Output

```text
Close <month>: soft / hard
Checklist: task | level | done (tool, time) | owner | blocker
Reconciliations: account | A | B | difference | category | age | action
Flux: line | this month | last | variance | driver
Brief: revenue, new, churned, refunds, disputes, commissions, cash, open items, systems included
```

## Approvals

- Journal entries, bills, payments and invoices in the books (`quickbooks_create_journal_entry`, `xero_create_manual_journal`) are record writes and spend. They always ask, and a human posts them.
- Commission and payout approvals, refunds and write-offs are spend, and always ask.
- Writing into reports or sheets is a record write, and asks.

## Example

Stripe payouts for the month total 41,200 USD and bank deposits 40,950 USD. The 250 USD difference is a payout in transit on the last day: timing, clears on day 2. Tool spend is 34 percent over last month; the driver is the volume of new seats added mid-month.

## References

- references/close-checklist.md: day-by-day tasks, dependency levels, default thresholds and aging buckets. It loads with `excom_skill_load`.

Adapted from anthropics/knowledge-work-plugins (finance/skills/close-management/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
