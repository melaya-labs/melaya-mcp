---
name: cfo-model-cost-watch
description: Watches AI model, research API and infrastructure costs the company pays, kept apart from what customers pay on their own keys. It covers cost per accepted run, outlier runs, models priced by a fallback, team budgets and per-service caps, and hosting growth, with measured savings proposals. Use when the weekly cost read is due, after a model or pipeline change, when cost per run jumps, before capacity or quota decisions, or when asked "why is our AI bill up".
version: 2.0.0
---

# Model and infrastructure cost watch

Catches silent cost drift before it becomes an invoice: a model priced by a fallback, a research cap reached, a budget switched off. Cheap, reliable runs keep each customer profitable.

## Look up first

- Who pays which cost (company-paid models and services against customer-paid keys or subscriptions): `excom_knowledge_search` "cost to serve" or "systems and tools". If unclear, ask the owner with `excom_propose_task` (needs_decision). Never add customer-side estimates to company cost.
- Team budgets and per-service daily caps: your team settings, and `excom_knowledge_search` "budget and thresholds".
- The procedure for adding a new model's price: `excom_knowledge_search` "provider models and costs runbook".

## Steps

1. Split costs by who pays. Company-paid usually means: its own models and servers, shared app API usage, vendor-backed research calls, hosting, storage and backups.
2. Measure, through `melaya_tools`:
   - Acceptance rate and cost per accepted run on the company's own pipelines (`melaya_eval_report`).
   - Cost by provider and model (`melaya_cost_summary`, `melaya_agent_cost_summary`).
   - Usage against plan caps (`melaya_account_usage`).
3. Find the outliers: the five most expensive runs, and any run above ten times the median. Run `melaya_run_diagnosis` on each to see the phase where the cost went (retries, long context, loops).
4. Check pricing integrity. List every model whose cost came from a fallback price because its id is missing from the price card. An unknown price is unknown, never zero. Ask the CTO to add it (`excom_send_handoff`, kind request).
5. Check caps and budgets: research calls against the daily caps, budgets that are switched off, and posts or calls whose cost grows with content (links, long outputs).
6. Propose savings, each measured before and after:
   - Route simple steps to a cheaper model, validated on real cases.
   - Cache a stable prompt prefix.
   - Batch non-urgent work.
   - Remove repeated research calls.
   Changing a pipeline's model is a pipeline change, and asks.
7. Infrastructure: hosting, storage and backup invoices, plus the growth of stored history. Ask the COO for host load. Flag every place where a measured value replaces an assumption.
8. Save with `excom_save_draft`. Record cost per accepted run and company-paid cost with `excom_record_measurement`. Message the owner when cost per accepted run doubles, a cap is reached, or an unknown-price model runs in production.

## Output

```text
Cost watch <window>, read <time>
Company-paid: line | amount | trend | source
Customer-paid estimate (context only): amount
Cost per accepted run: value | previous | change
Outliers: run date | cost | phase | cause
Fallback-priced models: provider | model | runs | action
Caps and budgets: service | used / cap
Proposals: change | expected saving (estimate) | how measured | approval
```

## Approvals

- Changing a pipeline (`excom_pipeline_change`), a budget or a cap is a record write or spend, and asks.
- Buying credits, upgrading hosting or a provider plan is spend, and always asks with the cost.
- Production changes on servers are the operator's, never the executive's.

## Example

Acme's cost per accepted run went from 0.04 to 0.11 USD. Diagnosis: one pipeline retries a failing scrape five times. Proposal: cap retries at one and add a cached fallback. Expected saving: 0.05 USD per run, measured over the next 200 runs.

Adapted from TerminalSkills/skills (skills/llm-cost-optimizer/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
