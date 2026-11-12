---
name: cdo-experiment-readout
description: Plans and reads out experiments on pricing, onboarding, landing pages, offers or emails. It checks first whether the sample can answer the question, then reads one primary metric with guardrails, sample-ratio and logging checks, absolute and relative lift, and a ship or do-not-ship call. Use when an A/B test is about to start, at a test's planned end, when someone reports a dashboard "win", or when asked "should we test this" or "did the test work".
version: 2.0.0
---

# Experiment readout

Decide whether a test can answer its question before it starts, and read it out honestly at the end. At low volume, many tests cannot reach a useful sample. Saying so early saves weeks.

## Look up first

- The metric definitions (`excom_knowledge_search` "metrics definitions") and the outcome the test serves (in your context).
- The baseline of the primary metric over the last four full weeks, and eligible units per week: read from the funnel source, or ask the owner of the change.
- The smallest lift worth shipping. This is a business answer: ask the proposer with `excom_send_handoff` (kind question).

## Steps

1. Write the plan before launch:
   - A one-sentence hypothesis.
   - Exactly one primary metric, with numerator, denominator and window.
   - Two to four guardrails, each with a stop threshold.
   - Segments named in advance.
   - The unit: account for pricing, user or visitor otherwise.
2. Do the arithmetic first (references/sample-size.md). Below about 400 conversions a month on the primary metric, only very large lifts are detectable. Say so, and propose a direct change with a before-and-after read, or buyer interviews, instead.
3. Assignment: hash a stable id together with the experiment key. Count only units exposed to the change. Render variants before first paint.
4. Read live values:
   - Funnel source for registrations and activation.
   - `stripe_list_checkout_sessions` and `stripe_list_subscriptions` for paid conversion.
   - `posthog_get_feature_flag` and `posthog_compute_funnel` if the test runs in PostHog.
   - `ga4_run_report` for landing tests.
5. Before looking at the result, check sample ratio (does the split match the plan), duplicated events and bots. A surprisingly large win is more often a logging bug.
6. Read once, at the planned sample. Stop early only at a planned interim look with p below 0.001. Never extend a flat test. With several variants, divide 0.05 by their number.
7. Report the absolute and relative lift with a confidence interval, the guardrails, and whether the lift is worth shipping. Unplanned segments are new hypotheses, not findings.
8. Save with `excom_save_draft`. Record the result with `excom_record_measurement`. Send the decision request to the change owner (`excom_send_handoff`, kind request).

## Output

```text
Experiment <key>: hypothesis | unit | primary (window) | guardrails | segments
Plan: baseline | min lift | sample per arm | weeks | feasible (why)
Readout: SRM | exposures per arm | primary (abs, rel, CI, p) | guardrails | decision
Call: ship / do not ship / rerun bigger / switch to direct change
```

## Approvals

- Launching price or discount variants, coupons or affiliate offers is spend or a price change, and always asks.
- Creating or changing flags, key events or audiences is a record write, and asks.
- Sending test emails or posts to real users is a send, and asks.

## Example

Acme wants to test a new pricing page. Baseline: 3 percent of 1,200 weekly visitors start checkout. Detecting a 20 percent relative lift needs about 13,000 per arm, which is 22 weeks. Not feasible. Recommendation: ship the change as a direct change and compare 4 weeks before and after, with the guardrail that refunds must not rise.

## References

- references/sample-size.md: the sample-size formulas, unequal splits, averages, and when not to test. It loads with `excom_skill_load`.

Adapted from TerminalSkills/skills (skills/ab-test-setup/SKILL.md) and anthropics/knowledge-work-plugins (data/skills/statistical-analysis/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
