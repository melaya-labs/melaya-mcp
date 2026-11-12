---
name: coo-runbook-upkeep
description: Keeps the team's runbooks true. It finds runbooks past their review date and runbooks that drifted from what really happened in tasks, pipeline runs and releases, then drafts corrections for each owner role with the evidence attached. Use when the weekly or monthly runbook pass is due, after a runbook run that needed a workaround, after a release that renamed a tool, file or step, or when someone says "the runbook is wrong" or "nobody follows this procedure".
version: 2.0.0
---

# Runbook upkeep

A runbook is only useful if the next executive can follow it without getting stuck. Check each one against its review date and against the last real run, then get the owner to correct it.

## Look up first

- The runbook index (owner, collaborators and source for each runbook): `excom_knowledge_search` "runbooks", then `excom_knowledge_read`. If there is no index, draft one from the runbooks you find with `excom_save_draft` and propose it.
- Each runbook's properties: updated, reviewed, review interval, owner.
- The editing rules for the knowledge base: `excom_knowledge_search` "editing rules". Owners apply edits; you propose them.

## Steps

1. List due dates. Due = reviewed + review interval. Mark each runbook overdue, due within 7 days, or current.
2. Look for drift, not just age. For every run since the last review, compare what happened with the written steps:
   - `excom_read_tasks` for tasks named after the runbook, with their notes and execution refs.
   - `excom_pipeline_runs_list` and `excom_pipeline_run_get` for pipelines that implement it.
   - Commits and releases that touched what it names, from whichever code host you are granted (for example `gitea_list_commits` or `github_list_prs`).
   Drift signals: skipped or reordered steps, extra manual steps, a tool or file that no longer exists, a failed check that was waved through, an approval asked where the runbook marks none, or the reverse.
3. Check every tool the runbook names against what you are actually granted (`excom_list_recommended_apps`). A renamed or removed tool is drift.
4. Classify each finding:
   - Wording.
   - Step change.
   - Safety: a missing approval point, a secret handled in the open, an operator-only step not marked.
   - Ownership.
5. Draft each correction in the runbook format in references/runbook-template.md, with a history line that cites the evidence.
6. Send each draft to the owner role with `excom_send_handoff` (kind request). Safety findings also go to the security role (kind question).
7. Save the upkeep report with `excom_save_draft`. Record the overdue, drifted and corrected counts with `excom_record_measurement`. Propose one task per correction. Runbooks that are often repeated by hand go to the repeat-work-to-pipeline skill.

## Output

```text
Runbook upkeep <date>
| Runbook | Owner | Reviewed | Due | State | Last real run | Drift | Class | Sent to |
Corrections: one draft per runbook, each with an evidence history line
Counts: overdue x, drifted x, corrected x
```

## Approvals

- Editing a knowledge note or shared document is a record write. It asks, and the owner role applies it.
- Never run a send, spend, production or operator-only step to "test" a runbook.
- Secrets never go into a runbook. Name the operator step, never its value.

## Example

Acme's "release the desktop app" runbook says to upload the build to the store portal. The last two release tasks show an extra signing step done by hand. Classified as a step change with a safety finding (the signing key handling is not marked operator-only). Draft sent to the CTO and the security role.

## References

- references/runbook-template.md: the runbook layout and the step table. It loads with `excom_skill_load`.

Adapted from anthropics/knowledge-work-plugins (operations/skills/runbook/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
