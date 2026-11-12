---
name: cpo-code-session-handoff
description: Lets the product executive change code itself in one small, provable coding session (copy, docs, SEO, templates, small fixes) and hand the finished session to the CTO, who holds push and CI deploy. Covers scope, the goal and evidence for the engine, judging the session result, discarding bad sessions and a handoff the CTO can review without questions. Use when a product-owned fix needs code, when a doc or translation change must ship in the app, or when someone asks the CPO to "just fix it in the code".
version: 2.0.0
---
# Code a change and hand it to the CTO

The CPO may code and commit in an isolated coding session but cannot push: the CTO holds `excom_code_push` and CI deploys. Small, provable sessions get reviewed and deployed the same week.

## Look up first

- Your coding grant and repository list (the coding tools are offered only when the grant is on). If not offered, ask the owner with `excom_request_setup` to switch on coding for you, and stop; never work around it.
- The runbook that governs the change: `excom_knowledge_search` with the topic, for example "translation pipeline", "add a page runbook", "template authoring". If none exists, say so in the handoff.
- Commit message convention and checks: `excom_knowledge_search` "commit convention", "release checklist".
- The acceptance table (skill cpo-acceptance-criteria) and the evidence.

## Steps

1. Check scope: one theme, one repository, smallest diff that meets the criteria. Migrations, auth, access rules, secrets, version pins, extension or desktop changes and deploy scripts are not CPO sessions: send them to the CTO as a request.
2. Write the goal: what is wrong (evidence lines), what done looks like (passing results), likely files, and the rule to reproduce first with a check or test, fix the cause, and report the evidence addressed and the covering test.
3. Start with `excom_code_task` (record write): repository, goal, runbook, evidence. One active session per repository.
4. Follow with `excom_code_status` in short waits; a long session wakes you when it ends.
5. Judge the result, not the summary: diff within the expected files, commits in the team's convention, checks green, no violations, evidence addressed, covering test named. Otherwise `excom_code_discard` (draft) and start a narrower session.
6. User-facing text ships in every supported language in the same session, through the translation procedure.
7. Hand over with `excom_send_handoff` (kind request) to the CTO: session id, goal, acceptance link, diff stat, commits, checks and results, what to verify after deploy, which deploy job it needs. Ask the CQO for a go or no-go when it touches a public surface.
8. Track with `excom_update_task`; after the CTO reports the deploy, verify the passing results yourself (`web_fetch`, `melaya_run_diagnosis`) and record them with `excom_record_measurement`.
9. Review findings from the CTO are fixed in a new session; disagree only with a test or read that shows it.

## Output

```text
Handoff to CTO: <goal>
Session: id, repository, branch, engine. Diff: files, lines. Commits.
Checks: name, result; covering test; evidence addressed
Acceptance: link. Verify after deploy: list. Deploy job: <from the deploy runbook>
```

## Approvals

- Starting a coding session (record write under Prepare).
- Push to a branch (send) or the base branch and any deploy (production): the CTO only, through approval cards.
- Anything touching secrets, migrations, auth or deploy paths: not a CPO session.

## Example

A pricing page tooltip states an old limit. Session goal: replace the hardcoded limit with the value from the plan config, add a test that the tooltip reads the config. Result: 2 files, 1 commit, typecheck and tests green. Handoff names the frontend deploy job; after deploy, `web_fetch` shows the new limit.
