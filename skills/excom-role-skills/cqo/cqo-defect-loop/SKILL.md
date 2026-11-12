---
name: cqo-defect-loop
description: Runs the corrective and preventive loop on a customer-reported defect: evidence of the trigger, a five-whys root cause backed by runs and logs, the fix, a preventive action, and an effectiveness check before closing. Use when the same defect is reported three or more times, when a paying account or partner is blocked, when a "fixed" defect comes back, or when a failed outcome keeps repeating.
version: 2.0.0
---
# Customer-reported defect loop

Find the cause, fix it, stop it coming back and prove that it stopped, because a defect that recurs after "fixed" is what turns a paying customer into a churned one.

## Look up first

- Which accounts matter most (paying, partners, affiliates) and any quality objective: the team's outcomes and your charter objectives, in your context.
- The bug triage and known issues notes: `excom_knowledge_search` for "bug triage", "known issues", "post-incident review"; `excom_recall` for earlier loops on the same defect.
- The agreed effectiveness window. If the team has none, use two weeks and say so; ask the owner to set one with `excom_propose_task` (needs decision true).
- The support app you hold, if any (`intercom_search_conversations`, `hubspot_list_tickets`); otherwise the CXO's handoff is the source.

## Steps

1. Record the trigger with objective evidence: what, where, when, how many accounts, which plan. Read the runs with `melaya_run_diagnosis`. Never copy personal data into the record.
2. Decide if the loop is needed. Required: a defect that sent, wrote or charged without approval (bring in the CISO or CFO); the same defect 3 or more times; a paying account or partner blocked. Otherwise evaluate: an isolated defect with a workaround usually stays in triage (skill cqo-bug-triage-severity).
3. Root cause with five whys, each answer backed by a run, a log or a code read. Stop at a cause within the company's control whose removal would stop the defect. It must explain every symptom in the reports.
4. Corrective action: the fix. The CPO writes the acceptance criterion; the CTO fixes it in a coding session with a covering test. Hand both over with `excom_send_handoff` (kind request) and open tasks with `excom_propose_task`.
5. Preventive action: what stops the same class of defect elsewhere: a regression case (skill cqo-regression-test-plan), a deterministic check in the release gate, a known-issues entry, a docs fix, or a versioned playbook change run on canary tasks, then promoted or rolled back.
6. Effectiveness check after the fix ships: read back the receipt, not the status. The covering test is green, the original scenario passes 3 trials, and no new report of the same defect arrives in the window. Read `melaya_eval_report` for the failure kind trend.
7. Close or reopen. Closed only when the effectiveness check passed; otherwise reopen with the new evidence. The CXO tells the customer; the CQO never replies.
8. Record recurrences before and after with `excom_record_measurement` (record write) and update the task with `excom_update_task`.

Writes never retry inside the loop: a timed-out send is outcome unknown and is reconciled first.

## Output

```text
Trigger: evidence, count, accounts affected (no personal data)
Root cause: five whys with the source of each answer
Corrective: fix, owner, session or commit, covering test
Preventive: regression case, gate check, docs or playbook change
Effectiveness: window, trials, recurrence count, verdict
Status: open / verifying / closed / reopened
Observed / Suggested / Needs confirmation
```

Saved with `excom_save_draft`.

## Approvals

- Replies to customers or partners (send, by the CXO after approval).
- Any deploy of the fix (production, through the CTO).
- Credits, refunds or goodwill gestures (spend, CFO and owner, with the amount).
- Changes to a production pipeline or playbook customers use.

## Example

Acme's weekly export failed for 4 accounts in a month. Five whys: the export timed out, because the file grew past the tool's limit, because pagination was never added, because the acceptance criteria had no "large account" case. Corrective: pagination with a covering test. Preventive: a large-account case in the regression suite and the release checklist. Effectiveness: 3 green trials and zero reports in two weeks, then closed.

Adapted from alirezarezvani/claude-skills (ra-qm-team/skills/capa-officer), MIT. Modified: rewritten generic for EXCOM.
