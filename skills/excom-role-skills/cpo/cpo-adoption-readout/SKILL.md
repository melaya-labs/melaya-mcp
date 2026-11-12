---
name: cpo-adoption-readout
description: Reads whether a shipped feature is used and keeps people, with cohorts instead of totals: reach, activation, time to activate, repeat use and retention against a comparison cohort, ending in a keep, fix or retire call. Use when a release is two to six weeks old, in a monthly product review, before retiring a feature or template, or when someone asks "is anyone using this" or "did the launch work".
version: 2.0.0
---
# Feature adoption readout

Answer "did people use what we shipped, and did it keep them" with cohorts. The readout ends in a call that feeds the roadmap.

## Look up first

- The expected outcome written at roadmap time: `excom_recall` the feature name.
- The activation event that proves real use and the metric definitions: `excom_knowledge_search` "activation events", "metrics definitions". If none is defined for this feature, propose one with `excom_propose_task` (needs decision) before reading data, because a definition picked after seeing the numbers is biased.
- Which analytics apps you are granted; if none, `excom_request_setup` (for example posthog or google_analytics).
- Internal and test accounts to exclude: `excom_knowledge_search` "internal accounts".

## Steps

1. Define cohorts by signup week or first-exposure week, plus a comparison cohort (before the feature). Write the event definition down first and keep it identical across cohorts.
2. Pull data: `posthog_query_trends`, `posthog_compute_funnel`, `ga4_run_report`, `ga4_run_funnel_report`, `melaya_eval_report` for run acceptance, `melaya_runner_status` for runner reach. Admin-only dashboards: ask the data executive with `excom_send_handoff` (kind question).
3. Validate: cohort sizes, missing weeks, double counting, internal accounts excluded. Cohorts under 20 users are anecdotes, not rates.
4. Compute reach, activation, median time to activate, repeat use (two or more uses in 14 days), week 1 and week 4 retention against the comparison cohort.
5. Find where users stall (the step before the event), which segment adopts, anomalies that line up with a deploy or incident.
6. Call it: keep (at or above expectation), fix (people try and stall: write the fix as acceptance criteria), retire (low reach, no repeat use after fair exposure; propose to the board).
7. Suggest follow-ups: a five-user interview script for the support executive, an onboarding or doc change, a template that shows the feature.
8. Record each headline number with `excom_record_measurement` (metric, value, window, source).

## Output

```text
Adoption readout: <feature> <date>. Expected outcome; activation event definition
| cohort | size | reached | activated | median time | repeat 14d | w1 | w4 |
Comparison row; patterns (2 to 3); call: keep | fix | retire, why; follow-ups; not measured
```

Saved with `excom_save_draft`.

## Approvals

- Retiring or hiding a feature, template or page (delete class).
- Outreach to users for interviews (send, by the support executive).
- Paid analytics seats or tools: never default, ask with the cost.

## Example

Acme shipped scheduled reports. Cohort of week 1: 120 users, 54 percent reached, 31 percent activated, median 2 days, 18 percent repeat. Comparison feature: 25 percent activated. Users stall at "connect a destination". Call: fix, with a criterion "a default destination is offered at setup".

Adapted from phuryn/pm-skills (pm-data-analytics/skills/cohort-analysis), MIT. Modified: rewritten generic for EXCOM.
