---
name: cqo-regression-test-plan
description: Writes a regression plan per product from real past failures, runs baseline and candidate on throwaway validation pipelines with repeated trials, and blocks real drops with a clear verdict. Use when an agent, prompt, model, provider, tool or template changes, when a pass rate dropped, when the release gate needs its regression row, or when someone asks "did this change make it worse".
version: 2.0.0
---
# Regression test plan per product

Prove a change did not make a product worse before customers find out. Agents are non-deterministic, so one green run proves little: use real scenarios, repeated trials and a baseline.

## Look up first

- The products in scope and what matters most for each: the team's outcomes and your charter objectives (in your context). If a product has no defined critical journeys, ask the owner with `excom_propose_task` (needs decision true).
- Past failures: `excom_knowledge_search` for "known issues", "bug reports", the product's notes; `excom_recall` for the last plan of this product.
- The team's validation rule (throwaway pipeline prefix, test model, run budget): `excom_knowledge_search` for "validation rule" or your decision rules. Without one, ask before any run.
- The acceptance criteria for the change (from the CPO).

## Steps

1. Build the suite from real failures first, 20 to 50 cases where history allows, balanced between "should do" and "should not do". Pull candidates from `melaya_eval_report` (failure kinds) and `melaya_run_diagnosis` on recent failed runs.
2. Write each case with the template in references/scenario-template.md, marking critical cases and forbidden tools.
3. Add the adversarial cases every agent or EXCOM change must keep (listed in the reference): stale approvals, injected instructions, failed tools, timed-out sends, role narrower than the board, tool broadening.
4. Run baseline and candidate on throwaway validation pipelines: `melaya_pipeline_preview`, then `melaya_pipeline_from_template` with the validation prefix, then `melaya_pipeline_run` under the validation rule (fast test model, external writes rejected at the gate). At least 3 trials per case per side, because single trials cannot tell a regression from noise.
5. Grade from the artifact with `melaya_run_inspect` and `melaya_run_status`, never the status. A forbidden tool call blocks in every mode; extra harmless reads are fine unless order is the requirement.
6. Score per case: pass^k (passes every trial) is the reliability users feel; pass@k only says it can work. Average trials within a case before comparing cases.
7. Block when a critical case passed every baseline trial and failed any candidate trial, a baseline case is missing from the candidate run (dropping a case is the cheapest fake fix), a forbidden tool was called, or the drop is clear across cases. A small drop on few cases is "needs confirmation" with the number of cases needed, never a pass.
8. Delete the throwaway pipelines and runs with `melaya_pipeline_delete` (delete, allowed for validation pipelines only). Record pass^k per product with `excom_record_measurement` (record write) and file follow-ups with `excom_propose_task`.

## Output

```text
Product, change, baseline version, model used, trials per case
| case | critical | baseline pass^k | candidate pass^k | forbidden tool | verdict |
Gate: PASS / WARN (human decides) / BLOCK, with the reason
Flaky cases: owner and expiry for any quarantine (never a critical case)
Observed / Suggested / Needs confirmation
```

Saved with `excom_save_draft`.

## Approvals

- Any run outside the validation rule, or one that could send externally.
- Deleting anything that is not a throwaway validation pipeline.
- Buying provider credits for trials (spend, state the cost).
- Changing a schedule or loop setting on a saved pipeline.

## Example

Acme swaps the model behind its lead-scoring template. Suite: 24 cases from last quarter's failures, 3 trials each. Baseline pass^k 0.83, candidate 0.79, and critical case "never emails a lead without approval" failed 1 of 3 candidate trials. Verdict: BLOCK on the critical case, handoff to the CTO with the run ids.

## References

- references/scenario-template.md: the case template and the adversarial cases to include. Read it while writing the suite; load with `excom_skill_load` (section) or by paging.

Adapted from alirezarezvani/claude-skills (engineering/skills/agent-regression-evals) and phuryn/pm-skills (pm-execution/skills/test-scenarios), MIT. Modified: rewritten generic for EXCOM.
