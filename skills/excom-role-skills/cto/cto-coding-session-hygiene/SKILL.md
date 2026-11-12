---
name: cto-coding-session-hygiene
description: Shapes and judges EXCOM coding sessions so every change is small, covered by a test seen failing first, and proven by the session's own result rather than its summary. Use when starting excom_code_task for a fix or feature, when a coding session ends and must be judged, when a colleague asks how to scope a session, or when someone says "the agent says it is done", "tests pass" or "ship it" without proof.
version: 2.0.0
---
# Coding session hygiene

Keep what reaches review small, tested and proven by the session's own fields. A clean session is cheap to review and safe to push; a sprawling one wastes a deploy window.

## Look up first

- The coding grant: repositories, base branch, configured checks and the computer. If `excom_code_task` is not offered, the grant is off or the computer is offline: ask the owner with `excom_request_setup`. Never work around it.
- The runbook that governs the change: `excom_knowledge_search` for "coding sessions", "release checklist" or the area (for example "translation pipeline"). If none exists, proceed without and note it.
- The team's commit message convention: `excom_knowledge_search` "commit convention". If missing, use one line per change in the form type(scope): description, and propose the note with `excom_save_draft`.

## Steps

1. Scope small: one goal, one repository, one concern. If the diff will plausibly exceed about 300 changed lines, split the goal, because large diffs hide defects.
2. Write the goal test first: "Reproduce <symptom> with a failing test in <area>, then fix the cause, then run the checks." Pass the evidence (redacted, capped) and the runbook. Start with `excom_code_task` (record write, asks under Prepare).
3. Wait with `excom_code_status` (up to 60 seconds per call). Never start a second session on the same repository.
4. Judge the result, not the summary. Read status, diff stat, commits, checks, violations, evidence addressed and covering test. Apply the proof table below. A violation means the session failed and can never be pushed.
5. If nothing shows the covering test failed before it passed, ask for a new session with that instruction, because a test never seen red proves nothing.
6. A check reported "not run" is not a pass. Ask the owner to update the runner or fix the grant.
7. Bad session: `excom_code_discard` (draft) and start a narrower one. Good session: review it with skill cto-push-review-gate. A session from another executive always goes through that gate; only the CTO pushes.
8. Record the verdict with `excom_update_task` and any lesson (a flaky test name) with `excom_record_fact`.

| Claim | Proof required | Not enough |
|---|---|---|
| Tests pass | each check listed as passed, 0 failures | the engine's summary |
| Bug fixed | covering test red then green; evidence addressed lists every item | code changed |
| Build ok | typecheck and build checks passed in this session | lint passed |
| Done | diff stat and commits present, no violations | status done alone |

## Output

```text
Session <id> on <repo> (<branch>)
Goal: ...
Diff: files, +/- lines, commits
Covering test: name, red then green (yes or no)
Checks: name result, name result
Evidence addressed: E1, E2 (missing: ...)
Violations: none or list
Verdict: ready for review | discard and redo (reason)
```

## Approvals

- Starting a coding session under Prepare (record write).
- Any push: branch is send, base is production and always asks (CTO only).
- Production actions, migrations and restarts never happen inside a session.
- Commit messages carry no AI co-author trailer; no env file, key file or credential path is touched.

## Example

The CPO hands over session S-42 for Acme's pricing page: diff 3 files, +40 -12, checks "client typecheck passed, unit tests passed", covering test "renders plan limits as text" listed red then green, no violations. Verdict: ready for review. A second session reports "tests pass" but its checks list shows "not run": verdict discard, ask the owner to update the runner.

Adapted from obra/superpowers (skills/test-driven-development, skills/verification-before-completion), MIT. Modified: rewritten generic for EXCOM.
