---
name: csco-provider-price-refresh
description: Collects the supply-side facts for a model catalog refresh: which models each provider lists or retires, enforced context windows, official prices per million tokens, promotional prices and end dates, key and quota problems, ranked by the spend they affect, for the CTO's refresh runbook. Use when the monthly provider pass is due, when a provider launches, retires, renames or reprices a model, when a promotion ends, or when a provider key starts failing.
version: 2.0.0
---
# Provider model and price refresh

A missing price row bills a model at zero and cost ceilings never fire; a wrong context window makes agents lose their task. This skill feeds the CTO accurate, sourced facts.

## Look up first

- The provider refresh runbook (owner, canonical tables, deploy steps): `excom_knowledge_search` "provider models and costs runbook", then `excom_knowledge_read`. If missing, ask the CTO with `excom_send_handoff` (kind question).
- Provider ids the platform uses and how prices resolve: `excom_knowledge_search` "model providers", "cost tracking".
- Known promotions and their end dates from the last pass: `excom_recall`.

## Steps

1. Key and catalog state: `melaya_model_list` per provider id with a stored key (ok, no_key, invalid_key, error) and the live model ids; `melaya_runner_status` for local and CLI providers. Without a key, say the protected models API was not queried and use the official catalog pages.
2. For each new or changed model, read the official model card and pricing page with `web_fetch`; aggregators only as labelled low-confidence cross-checks. Record the fields in `references/research-rules.md`.
3. Record every promotion with its end date and the price after, and every retirement with its date and successor. Search vendor mail for deprecation notices (`zoho_email_search`, `gmail_search`, read).
4. Diff against what the platform bills: ask the CTO with `excom_send_handoff` (kind question) for the current price and window rows; list new, renamed, retired and repriced models.
5. Rank the diff by spend affected using `melaya_eval_report` for the last 30 days, so costly rows are fixed first.
6. Send the findings to the CTO (kind request) and the price rows to the CFO (kind request) to verify against pricing pages. Never edit code, tables or settings.
7. Save findings with `excom_save_draft`; record models with a verified price row and models unscored with `excom_record_measurement`.

## Output

```text
Provider refresh: <date>
Key state: provider | ok/no_key/invalid_key/error | read at
Findings: provider | model | window | max output | input | output | cache read | cache write | REAL/APPROX | gating | source URL | as of | confidence
Promotions: model | promo price | ends | price after
Retirements: model | date | successor
Diff vs billing, ranked by 30-day spend
```

## Approvals

- Paid model-list or probe runs over a few dollars: spend, with the estimate.
- Deploys, runner releases, table edits: production, the CTO.
- Buying credits or changing a provider plan: spend.
- Enabling a provider for customers: a product decision for the CTO and CPO.

## Example

A provider announces its flagship's promotional price ends next week. The refresh records the promo price, the end date and the standard price from the pricing page (REAL, high confidence). The 30-day eval report shows that model carries most of Acme's model spend, so the row is first in the CTO's list.

## References

- `references/research-rules.md`: required fields, source order and honesty rules; read at step 2.
