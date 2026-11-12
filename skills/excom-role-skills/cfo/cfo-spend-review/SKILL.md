---
name: cfo-spend-review
description: Reviews what the company spends or is asked to spend: tools, ads, providers, payouts and paid data calls. It compares actuals with budget, explains each variance with a volume or rate driver, finds duplicate or unused tools, and turns every new request into a costed proposal. Every spend asks. Use when the weekly or monthly spend read is due, when a trial or renewal notice arrives, when someone proposes a purchase or a paid tool, or when asked "where is the money going".
version: 2.0.0
---

# Spend review

Know every dollar going out, explain every variance, and make each new spend an explicit decision. Spend that moves no outcome is the first to go.

## Look up first

- Budgets per line, approval thresholds and the ads budget: `excom_knowledge_search` "budget and thresholds". Lines without a budget are marked "no approved budget". Ask the owner to set one with `excom_propose_task` (needs_decision).
- The tool and vendor list: `excom_knowledge_search` "vendor inventory", or ask the COO.
- The outcomes (in your context). Every proposal names the outcome it moves.

## Steps

1. List the spend lines: ads, SaaS, hosting, providers, paid data calls, affiliate payouts, store and certificate fees.
2. Read actuals:
   - Ads: `gads_budget_pacing` and `gads_change_history`, or your ad platform.
   - Company-paid run and research cost: `melaya_cost_summary` through `melaya_tools`.
   - Affiliate payouts: `affonso_list_payouts`.
   - Vendors: `quickbooks_get_expenses_by_vendor` or `xero_get_profit_and_loss`.
   - Trials and renewals: mail (`gmail_list_threads`, `zoho_email_search`).
   Lines with no connector are entered from the invoice.
3. Compute each line's variance against budget, last month and forecast. Investigate when the team's thresholds are crossed. Defaults: 10 percent over budget, 20 percent month over month.
4. Split each investigated variance into volume (more seats, runs, clicks) and rate (a higher price, a model change, an auto-applied bid). Write one line per variance: favourable or unfavourable, amount and percent, driver, whether it repeats, and the action.
5. Find sprawl: two tools doing one job, trials that converted without approval, unused seats.
6. Write every new request as a proposal: what, vendor, amount and billing period, the outcome it moves, the expected return and how it will be measured, the cheapest alternative (including a free tier or doing nothing), and the cancel terms.
7. Save with `excom_save_draft`. Record the totals with `excom_record_measurement`. Propose approvals and cancellations with `excom_propose_task`. Humans act in the vendor consoles.

## Output

```text
Spend review <period>, read <time>, currency <code>
| Line | Budget | Actual | Variance | % | Driver | Repeats? | Action |
Sprawl: tool | monthly cost | proposal
Proposals: item | vendor | amount/period | outcome | expected return and measure | alternative | cancel terms | approver
```

## Approvals

- Every spend always asks: purchases, renewals, upgrades, ad budget or bid changes, paid listings, paid data calls, payouts. State the amount first.
- Cancellations are done by a human after approval.
- No standing rule is ever proposed for a money-moving action.

## Example

Acme's model costs rose 46 percent month over month. The driver is rate, not volume: one pipeline was switched to a larger model and runs stayed flat. Proposal: move its classification step back to the smaller model and measure for two weeks.

Adapted from anthropics/knowledge-work-plugins (finance/skills/variance-analysis/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
