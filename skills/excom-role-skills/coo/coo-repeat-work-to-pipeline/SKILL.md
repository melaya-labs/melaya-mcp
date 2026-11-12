---
name: coo-repeat-work-to-pipeline
description: Turns work repeated by hand into a managed pipeline. It finds the same manual step three times in tasks or summaries, maps the current flow and its waste, drafts a config with every write gated, validates it with melaya_pipeline_preview, and proposes it with excom_pipeline_propose, which runs a dry-run trial before any schedule. Use when the weekly automation pick is due, when a colleague asks "can this run on its own", or when the same report, read or follow-up keeps coming back.
version: 2.0.0
---

# Turn repeated work into a pipeline

One repeatable workflow a week, turned into a managed pipeline, frees executive time for the outcomes. Every write stays gated by a human.

## Look up first

- Recent tasks and recalled repeats: `excom_read_tasks` and `excom_recall`.
- Existing pipelines and templates: `excom_pipeline_list`, plus templates through `melaya_tools` (`melaya_pipeline_templates`).
- The grants of the executive who will own the pipeline (your context or the owner). A pipeline cannot use what that executive is not granted.

## Steps

1. Detect repeats. Look for tasks with the same verb and object over recent weeks, and steps done by hand in daily summaries. Keep only candidates seen three or more times.
2. Map the current flow of the best candidate: every step, tool, decision, handoff, approval and wait, with who does it and how long it takes. Name the waste: waiting, rework, handoffs, steps that add nothing, manual reads.
3. Look for an existing solution: an existing pipeline (perhaps paused or failing) or a template. Prefer a template to a new build.
4. Design the future state:
   - Reads run automatically.
   - Every write stays gated: sends, record writes, spend.
   - Remove steps that add nothing.
   Managed pipelines refuse phone, browser and computer tools and the platform's own demo model. Account names must be accounts already assigned.
5. Draft the config and run `melaya_pipeline_preview` through `melaya_tools`. Preview is free and saves nothing. It is the only check that catches an invented field, because the builder silently drops unknown fields. Fix and preview again until it is clean.
6. Write the acceptance check: what output, by when, and how a human tells a good run from a bad one.
7. Propose with `excom_pipeline_propose` (pipeline schedule class, always asks). Include the config or template, the schedule, the owner executive, the acceptance check, and the time saved per cycle. On approval, the platform first runs a dry-run trial with writes removed. Only a passed trial gets the full config and a schedule.
8. Follow up with `excom_pipeline_status` after the trial and the first runs. Failed runs go to the CTO with the run id (`excom_send_handoff`, kind request). Record the time saved with `excom_record_measurement`. Updates and rollbacks go through `excom_pipeline_change`, which asks.

## Output

```text
Candidate: <work>, seen N times (task refs)
Current: step | tool | who | time | wait | waste
Future: step | tool | gated (send / record write / spend)
Preview: clean, or the issues fixed
Acceptance check: <observable result, time>
Saving: hours per cycle (estimate) | schedule | owner executive | proposal id | trial result
```

## Approvals

- Creating, scheduling, changing, pausing or retiring a managed pipeline always asks.
- Write tools inside the pipeline stay human-approved at run time. Sends, spend and production always ask.
- Executives propose. They never save or schedule directly.

## Example

Every Monday, the CFO reads the billing balance, payouts and active subscriptions and drafts the same summary. Seen 4 times. Pipeline: three reads plus a draft step, no writes, scheduled Monday at 07:00. Acceptance: a draft with every number sourced exists by 08:00. Saving: 40 minutes a week.

Adapted from anthropics/knowledge-work-plugins (operations/skills/process-optimization/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
