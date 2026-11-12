---
name: csco-vendor-inventory
description: Builds and refreshes one inventory of everything the company depends on (compute host and edge, model and API providers, metered APIs, SaaS, signing and developer accounts, distribution channels, device hardware) with owner, plan, cost, renewal date, data processed, single points of failure and fallback. Use when no supplier register exists, for the quarterly SaaS inventory, when a supplier is added, or when someone asks "what do we depend on for X".
version: 2.0.0
---
# Vendor and provider inventory

For a software company the supply chain is providers, not pallets. One inventory answers cost, renewal and fallback questions without searching mail each time.

## Look up first

- The supplier register and subprocessor list: `excom_knowledge_search` "supplier register", "subprocessor list". If none exists, start one from this skill and propose it with `excom_save_draft`.
- Continuity plans per supplier: `excom_knowledge_search` "business continuity", "supplier fallback". If missing, mark fallback "none recorded".
- Connected services and accounts: `melaya_connector_list`, `melaya_account_subscription`.
- Device hardware used for testing (phones, computers): `excom_knowledge_search` "hardware register"; if none, ask the owner with `excom_propose_task` (needs_decision true) and record make, model, OS, owner and purpose only.

## Steps

1. Pull what is live: `melaya_connector_list`; `melaya_model_list` per provider id for key state (ok, no_key, invalid_key, error); `melaya_runner_status` for local and CLI providers. For infrastructure use the granted cloud tools, for example `aws_ce_get_cost_and_usage`, `alibaba_ecs_describe_instances` (count and region only) and `cloudflare_get_zone` for the edge plan.
2. Pull what is paid: `zoho_email_search` and `gmail_search` for welcome, trial, invoice, receipt and renewal subjects over 90 days (read); amounts from `zoho_email_list_attachments` and `gmail_get_attachments`. Metered APIs where tools exist (for example `hunter_account`, `webshare_subscription`, `gads_account_summary`). A provider with no balance tool is "not measured".
3. Fill each row with the fields in `references/inventory-fields.md`. Customer-selected model providers are the customer's choice, not your subprocessors; label them so.
4. Before the first payment to a new supplier, ask the CLO to screen it with `excom_send_handoff` (kind request). Bank details stay with the CFO.
5. Flag: no fallback, a trial that converts, renewal within 30 days, terms or DPA not on file, single point of failure.
6. Save the inventory with `excom_save_draft`. Creating a sheet with `sheets_create` or rows with `sheets_append_row` is a record write; if Sheets is not granted, `excom_request_setup` with the service id google_sheets.
7. Hand renewal dates to `csco-renewals-calendar` and missing terms to the CISO with `excom_send_handoff` (kind request). Record inventory completeness with `excom_record_measurement`.

## Output

```text
Row: supplier | category | purpose | owner role | plan | amount and period (source) | renewal | processes customer data | SPOF | fallback | terms on file | evidence and read date | flags
Summary: rows | complete | not measured | flags by type
```

## Approvals

- Creating the sheet or writing rows: record write.
- Buying, upgrading, renewing, cancelling: spend, with the amount.
- Contacting a vendor: send.
- Adding a supplier that processes customer data: the owner, with the CISO and CLO.

## Example

Acme's first inventory: 31 rows. The compute host is a single point of failure with fallback "rebuild from backup, off-site copy pending"; two SaaS trials convert within 30 days; one metered API has no balance tool (not measured). Completeness: 22 of 31 rows have owner, plan, amount and renewal date.

## References

- `references/inventory-fields.md`: categories, row fields and flag rules; read at steps 3 and 5.

Adapted from anthropics/knowledge-work-plugins (operations/skills/vendor-review), Apache-2.0, and Maxbase91/procurement-skills (supplier-truthcheck), MIT, Copyright (c) 2026 Maximilian Ziermann. Modified: rewritten generic for EXCOM.
