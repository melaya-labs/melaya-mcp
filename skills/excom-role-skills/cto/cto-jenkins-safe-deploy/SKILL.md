---
name: cto-jenkins-safe-deploy
description: Deploys pushed commits to production through CI one job at a time, in the order the deploy runbook sets, with a rollback plan written first, an approval per build, a verified live commit and a deploy marker. Use when commits are on the base branch and must go live, when a hotfix is ready, when a deploy failed and needs a rollback, or when someone asks "deploy it" or "is it live yet".
version: 2.0.0
---
# Safe deploy through CI

Commits reach production only through the base branch and the matching CI job. Run the jobs in order, stop at the first red build, prove what is live and mark the deploy, so a failed deploy never takes down what customers pay for.

## Look up first

- The deploy runbook: `excom_knowledge_search` "deploy runbook". It names the CI jobs, which components each deploys, their order, the jobs the CTO must never trigger, and the build provenance marker that proves the live commit. If missing, stop and ask the owner with `excom_propose_task` (needs decision true); never infer job names.
- CI access: if your CI is Jenkins, the `jenkins_*` tools. If not granted, `excom_request_setup` for jenkins; never ask for a token in chat and never deploy another way.
- The quality go for the release and whether a security post-deploy check is required (`excom_read_tasks`).
- Release prerequisites: when version pins moved, the release must already resolve (for npm, `npm_package_info`).

## Steps

1. Confirm the gate: quality go exists, the security check is planned when a gate, secret or edge rule changed, and pinned releases resolve. If not, stop.
2. Pick the jobs from the diff using the deploy runbook. Confirm names and last results with `jenkins_list_jobs` and `jenkins_get_job`.
3. Write the rollback plan before the first trigger: the commit to revert, the job to re-run, the approver.
4. `jenkins_queue`: never trigger while a build of the same job is queued or running.
5. Trigger the first job with `jenkins_trigger_build` (production, always asks). Never start the next job before the previous one is green, because a half-deployed stack is worse than a delayed one.
6. Wait with `jenkins_wait_build` (repeat) and read `jenkins_get_build`. On red, read `jenkins_build_console` (masked tail), stop the sequence and report. A runaway build may be stopped with `jenkins_abort_build` (production, asks).
7. Verify what is live after each green job: the provenance marker names the pushed commit (ask the owner or operator to read it if no tool exposes it), the health route answers when fetched with `web_fetch`, and long-running work survived the restart (`grafana_loki_query` for interrupted or reattached markers, if the runbook names them).
8. Mark the deploy with `grafana_create_annotation` (record write): job, build number, commit.
9. Post-deploy check within 30 minutes: `grafana_errors_summary` for a window starting after the deploy against the window before. Smoke one non-sending pipeline on the team's test model and read `melaya_run_diagnosis`.
10. If errors rose or the smoke failed: propose the rollback (revert through a session and `excom_code_push`, then re-run the same job), both production. Tell the owner and the COO.
11. Close: `excom_update_task` with build numbers, `excom_record_measurement` for errors before and after, and ask the CISO for post-deploy verification when relevant.

## Output

```text
Deploy record
Commits: shas on the base branch
Gate: quality go (link), security check (n/a or passed)
Rollback plan: revert <sha>, re-run <job>
Jobs: <job> #n green / <job> #n green (or stopped at ...)
Live: provenance commit matches yes/no, health ok, long-running work ok
Annotation: yes/no
Errors before/after (window): a / b
```

Recorded with `excom_update_task`.

## Approvals

- `jenkins_trigger_build` and `jenkins_abort_build`: production, every call, no rule can cover them.
- Any restart outside the job, production migration or environment staging.
- The rollback push and its re-run.

## Example

Acme's deploy runbook lists jobs API, Workers, Web in that order. The diff touches API and Web, so two jobs: API #212 green, provenance shows the pushed sha, health 200; Web #98 green. Errors 4 before, 3 after. Annotation created, task closed.
