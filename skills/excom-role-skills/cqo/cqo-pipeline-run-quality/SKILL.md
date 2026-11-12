---
name: cqo-pipeline-run-quality
description: Judges whether pipeline and executive runs really did the job by reading the delivered artifact and tool results, never the status, and splits real failures from classifier false positives with an owner for each. Use when running the weekly run acceptance review, before a template gets a validated badge, after a deploy for the first real runs, or when a run says success but the result looks thin or empty.
version: 2.0.0
---
# Pipeline run quality review

Decide whether runs actually did the job by reading what they delivered, because a run marked done with an empty body or a fallback answer is a failure the customer sees.

## Look up first

- What a correct artifact looks like for each pipeline in scope (expected fields, receipts, company context): the pipeline's own description and the team's template standards via `excom_knowledge_search` for "template standards" or "validation". If a pipeline has no definition of done, ask its owner with `excom_send_handoff` (kind question).
- The quality objective and its threshold (acceptance rate, cost per accepted run): your charter objectives and the team's outcomes, in your context.
- The last review: `excom_recall`.

## Steps

1. Pull the window: `melaya_eval_report` (acceptance, score, failure kinds, cost per accepted run), then per project. For executive pipelines also `excom_pipeline_status` and `excom_pipeline_runs_list`.
2. Pick the worst runs by failure kind (tool error, empty, false fallback) and a random sample of runs marked done, because hidden failures sit among the successes.
3. Diagnose each: `melaya_run_diagnosis` (verdict, failing tool, phase), then `melaya_run_inspect` with kinds reply and tool call, tool results only where needed and clipped. For executive runs, `excom_pipeline_run_get`.
4. Judge the artifact with references/green-red.md.
5. Separate real failures from classifier false positives and count both, because the split is usually not measured.
6. Reconcile any outcome unknown (a timed-out send) before calling a run failed or passed; never re-run a write to find out.
7. Write findings as Observed, Suggested and Needs confirmation, without confidence percentages. Send real failures to the CTO and the pipeline owner with `excom_send_handoff` (kind request), template issues to the CPO.
8. Record the acceptance rate and the real failure count with `excom_record_measurement` (record write) and propose fixes with `excom_propose_task`.

## Output

```text
Window, runs, evaluated, accepted %, cost per accepted run (tool and read time)
Real failures: | run | pipeline | failure kind | failing tool | artifact problem | owner |
False positives: | run | why the classifier was wrong |
Observed / Suggested / Needs confirmation
```

Saved with `excom_save_draft`.

## Approvals

- Any run outside the validation rule, or one that could send externally.
- Marking a template validated (production record).
- Deleting runs or pipelines other than throwaway validation ones (delete).
- Changing a loop setting or schedule on a saved pipeline.

## Example

Acme's weekly window: 120 runs, 104 evaluated, 81 percent accepted. In a sample of 10 "done" runs, 2 delivered a digest with zero items because a connector returned an empty list without an error. Logged as real failures (red: status done, body empty), owner CTO, suggested fix: the pipeline reports "no items found" and the connector check runs first.

## References

- references/green-red.md: the artifact rules for green and red runs. Read it at step 4; load with `excom_skill_load` (section) or by paging.
