---
name: csco-monthly-spend-review
description: Produces the supplier side of the monthly report: model, cloud, edge, metered API and SaaS spend read from systems and invoices, cleaned (names, currencies, credits, duplicates), compared with revenue, with anomalies flagged and savings ranked for the CFO. Use when the monthly spend review is due, when a cost anomaly or budget alert fires, when a metered connector hits its cap, or when the CFO asks what a provider or channel costs.
version: 2.0.0
---
# Monthly supplier spend review

Shows what the company spent on suppliers, what looks wrong and which savings to take, with every number sourced. Closing "not measured" gaps is part of the job.

## Look up first

- The CFO's reporting format and budget lines: `excom_knowledge_search` "monthly report", "budget", or ask the CFO with `excom_send_handoff` (kind question).
- The supplier inventory and renewals calendar: `excom_knowledge_search` "supplier register", "renewals calendar".
- Plan prices and revenue definitions: `excom_knowledge_search` "pricing and plans".
- Last month's review: `excom_recall` (trend only when last month was measured).

## Steps

1. Models and usage: `melaya_eval_report` for the month (cost, tokens, cost per accepted run) and `melaya_account_usage`. Local and free providers bill zero, so totals understate compute; say so.
2. Cloud and edge with the granted tools, for example `aws_ce_get_cost_and_usage` by service, `aws_ce_get_anomalies`, `aws_budgets_describe_budgets`, `cloudflare_get_zone`. A provider billed only in a console is "not measured" unless an invoice is read.
3. Metered APIs where tools exist (for example `webshare_usage_stats`, `hunter_account`, `gads_budget_pacing`); a provider with no balance tool is "not measured".
4. SaaS invoices from `zoho_email_search` and `gmail_search` with `zoho_email_list_attachments` and `gmail_get_attachments` (read).
5. Clean the data with the rules in `references/cleaning-and-anomalies.md`.
6. Revenue side: `stripe_list_invoices` and `stripe_get_balance` (read) for supplier cost to revenue; the CFO's ledger is the record.
7. Flag anomalies and rank savings by monthly value with the action and owner (from the reference).
8. Write Observed, Suggested and Needs confirmation with `excom_save_draft`, send to the CFO with `excom_send_handoff` (kind request), and record total supplier spend and cost per accepted run with `excom_record_measurement`.

## Output

```text
Supplier spend review: <month>  read <date>
Observed: category | supplier | amount | source | vs last month
Not measured: item | why | tool that would read it
Anomalies: item | evidence | possible cause
Suggested savings: action | per month | owner | risk
Needs confirmation | Supplier cost to revenue: value or not measured
```

## Approvals

- Plan, cap, budget-object, top-up or cancellation changes: spend, the owner with the CFO.
- Creating or changing cloud budgets: spend.
- Writing to the CFO's ledger or a shared sheet: record write.

## Example

Acme's month: model cost up 60 percent, traced to one pipeline that switched to a larger model; cloud flat; a SaaS seat unused for 90 days; a posting API cost driven by customer actions. Savings ranked: move the pipeline back after a CQO check (largest), cancel the seat, review the posting cost model with the CFO.

## References

- `references/cleaning-and-anomalies.md`: cleaning rules, anomaly checks and savings levers; read at steps 5 and 7.

Adapted from Maxbase91/procurement-skills (spend-prism), MIT, Copyright (c) 2026 Maximilian Ziermann. Modified: rewritten generic for EXCOM.
