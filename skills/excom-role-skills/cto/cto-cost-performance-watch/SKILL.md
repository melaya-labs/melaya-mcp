---
name: cto-cost-performance-watch
description: Measures model and cloud spend per accepted run and the latency, queue and page-speed numbers users feel, compares them with your thresholds, and proposes the cheapest measured fix. Use when running the weekly cost and performance review, when the CFO asks why spend moved, when queue refusals, slow pages, slow runs or memory climbs appear, or before launching a feature that adds model calls.
version: 2.0.0
---
# Cost and performance watch

Keep spend per accepted run and user wait times under control with numbers from systems, not impressions. Cheap, fast runs protect margin and keep trials converting.

## Look up first

- Thresholds and baselines: your charter objectives in context, then `excom_knowledge_search` "objectives and metrics" or "capacity thresholds" (queue refusals, run lanes, request pool limits, page speed targets). If none exist, report raw numbers and propose thresholds with `excom_propose_task` (needs decision true).
- The team's test model policy for smoke and comparison runs: `excom_knowledge_search` "test model". If missing, use the cheapest model your grants allow and never a frontier model.
- Granted apps: cost tools, `grafana_*`, `pagespeed_*`, cloud billing. Missing: `excom_request_setup`, then continue with what you have.

## Steps

1. Classify the job: audit (spend exists, breakdown unknown), optimisation (drivers known), or design review (new feature). Ask only for what the conversation does not already give.
2. Measure spend: `melaya_agent_cost_summary` and `melaya_cost_summary` for the period, `melaya_account_usage`, and `melaya_eval_report` for cost per accepted run. Cloud spend: `aws_ce_get_cost_and_usage` only if AWS is granted.
3. Find the few drivers: sort by feature or pipeline, then model, then tokens. If token logging is missing for a driver, that gap is the first finding, not a guess.
4. Measure performance: `grafana_prom_query_range` for queue depth, lanes, memory per run and restarts; `grafana_loki_query_range` for queue refusals and slow requests; `pagespeed_core_web_vitals` for the money pages (LCP first).
5. Compare each number with its threshold and last period. A change is a finding only outside normal noise; say so when the sample is small.
6. Propose fixes in return order from references/fix-catalog.md, each with expected effect and how it will be measured.
7. Smoke or compare only on non-sending pipelines with the test model.
8. Code changes go through skill cto-coding-session-hygiene and skill cto-push-review-gate. Routing that changes user-visible quality needs a CQO before and after comparison on the same cases.
9. After a fix ships, measure over a comparable window and record with `excom_record_measurement`.
10. Escalate a crossed threshold to the owner (and the COO for queue refusals) with `excom_send_handoff`; spend decisions go to the CFO.

## Output

```text
Period: <this> vs <previous>
Spend: total, per accepted run, top 3 drivers (feature, model, tokens) with source tool
Performance: queue refusals, lanes peak, request pool, run memory, LCP per money page
Threshold crossings: none / list with message sent
Proposals: fix, expected effect, measure, owner, approval needed
Measured after previous fixes: before -> after (window)
```

Saved with `excom_save_draft`.

## Approvals

- Any spend: bigger instances, new cloud resources, paid profiling or monitoring tools (ask with the monthly cost).
- Deploys of fixes (production) and environment changes.
- Changing a customer-facing default model (product decision with the CPO).

## Example

Acme's spend per accepted run rose from 0.9 to 1.4 cents. Top driver: a summarising step sending a 6,000-token static prompt on every call with no cap. Proposals: prompt caching on the static part, a per-step output cap, route the classification step to the small tier. After deploy: 1.0 cents over a comparable week, CQO comparison unchanged.

## References

- references/fix-catalog.md: cost and latency fixes in return order with their typical effect and how to measure them. Read at step 6 (page it in or load with `excom_skill_load`).

Adapted from alirezarezvani/claude-skills (engineering/llm-cost-optimizer/skills/llm-cost-optimizer, engineering/skills/performance-profiler), MIT. Modified: rewritten generic for EXCOM.
