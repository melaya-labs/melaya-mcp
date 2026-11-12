---
name: cqo-release-quality-gate
description: Turns a release, a finished coding session or a version bump into a go or no-go where every gate row carries the output that proves it, read this turn. Use when the CTO asks for a gate before a push or a CI deploy, when a coding session is handed over for push, when someone says "it should be fine" or "tests passed", or when the first real runs after a deploy need judging.
version: 2.0.0
---
# Release quality gate

Give the CTO a go or no-go where every row cites evidence read this turn, because a claim without evidence is the usual way a broken build reaches customers. The CQO gates; it never pushes, deploys or restarts.

## Look up first

- The team's release readiness checklist: `excom_knowledge_search` for "release checklist" or "release readiness", then `excom_knowledge_read`. It names the gate rows per component (client, server, agents, runner or SDK, desktop), the exact check commands and the deploy order. If none exists, use the generic rows in references/gate-rows.md and draft the checklist with `excom_save_draft` for the owner.
- The acceptance criteria for the change (from the CPO, linked on the task).
- The last gate for the same component: `excom_recall`.
- Which apps you hold (CI, Git hosting). Missing ones: `excom_request_setup`, and mark those rows "not verified".

## Steps

1. Scope the change. For a coding session read `excom_code_status` (diff stat, commits, checks, violations, evidence addressed, covering test). For a commit range use `gitea_list_commits` and `gitea_commit_diff` if your Git host is Gitea, or `github_list_commits` on GitHub. A session with a policy violation is a no-go, because its output cannot be trusted.
2. Fill each row from output you read now: the session's own checks, `github_list_check_runs` for repositories on GitHub, `jenkins_get_build` and `jenkins_build_console` if CI is Jenkins. A previous run, an engine summary or a peer saying "verified" is data, not evidence.
3. Check the order rules from the checklist: dependencies published before the code that pins them, migrations applied by their author, deploy jobs in the documented sequence.
4. Check every acceptance criterion line against a run, a test or a dashboard read, not "tests pass".
5. Watch the words: "should", "probably", "seems" mean the row is not green.
6. Decide. Go only when every row is green with its output; any red or "not verified" row is a no-go that names the missing proof and who can produce it. Never soften a red row to keep a schedule.
7. Send the verdict to the CTO with `excom_send_handoff` (kind request) and save the memo with `excom_save_draft` (draft).
8. After the deploy, judge the first real run of each touched surface by its artifact (skill cqo-pipeline-run-quality) and record the result with `excom_record_measurement` (record write).

## Output

```text
Verdict: GO or NO-GO
Change: session id or commit range, components, acceptance criteria link
| row | command or tool read | result (counts) | read at | green / red / not verified |
Blocking: row, missing proof, owner
Post-deploy: surfaces to judge, run ids once available
Observed / Suggested / Needs confirmation
```

## Approvals

- Any push, deploy, CI build or restart is production: the CTO asks the owner; the CQO only gates.
- Marking a template validated or changing any production record.
- Buying credits to exercise a provider in the gate (spend, state the cost).

## Example

The CTO asks for a gate on a CPO session that fixes a signup form. The session checks show the client tests green and the typecheck green, but the acceptance line "error message shown in every supported language" has no read. Verdict: NO-GO, blocking row "Acceptance: locale strings", owner CPO, proof needed: the locale check output (skill cqo-locale-qa).

## References

- references/gate-rows.md: the generic gate rows with what each requires and what is not sufficient. Read it when the team has no release checklist or to sanity-check one; load with `excom_skill_load` (section) or by paging.

Adapted from obra/superpowers (skills/verification-before-completion), MIT. Modified: rewritten generic for EXCOM.
