---
name: chro-contractor-management
description: Keeps every contractor and freelancer on one register with scope, owner, end date and access list, drafts statements of work, raises classification questions for the CLO, runs renewal reviews and closes access on exit. Use when the team engages, renews or ends a freelancer, agency or contractor, when an engagement has run for months in the same role, or when someone asks "who do we pay outside payroll".
version: 2.0.0
---
# Contractor and freelancer management

Keeps non-employees visible and correctly scoped, so long "temporary" engagements do not drift into misclassification and nobody keeps access after the work ends.

## Look up first

- The contractor register and any agreements: `excom_knowledge_search` "contractor register", "contractor agreements". If none exists, say so and propose starting one with `excom_save_draft`.
- The engagement terms the owner approved (deliverables, budget, dates): from the owner or `excom_recall`. If missing, ask with `excom_propose_task` (needs_decision true).
- The offboarding procedure: `excom_knowledge_search` "offboarding procedure". If missing, use the exit steps below.
- Current memberships: `melaya_project_list`, `melaya_team_list`, `melaya_approval_list`.

## Steps

1. Draft the statement of work: deliverables, acceptance criteria, schedule, reviewer, payment milestones (amounts left to the owner and CFO), IP and confidentiality expectations (the CLO drafts clauses), and what the contractor will not access.
2. Raise classification flags as questions for the CLO with `excom_send_handoff` (kind question), never as a verdict: does the team control how and when the work is done, is the person integrated like an employee, is it open ended, are you their only client, has it run past 12 months in the same role. Classification is legal or people: the owner decides with counsel.
3. Before the first payment to a new entity, ask the CLO to screen it (sanctions, registry, tax number) with `excom_send_handoff` (kind request). Payments go to the CFO.
4. Plan access with least privilege and separately from employee onboarding: viewer or runner role, no shared mailbox credentials, connectors shared only if the owner chooses project connectors. Any `melaya_team_invite` asks the project owner.
5. Keep the register row (fields in Output). Writing it with `sheets_append_row` is a record write; if Sheets is not granted, `excom_request_setup` with the service id google_sheets, or keep it in the draft.
6. Renewal: 30 days before the end date, draft a review (deliverables met, spend from the CFO, still needed, tenure). Flag engagements over 6 months for review and over 12 months for escalation, because long same-role engagements carry the highest reclassification risk. Propose keep, change or end with `excom_propose_task`.
7. Exit: list memberships and pending approvals, draft the offboarding record (removals, credential rotation, verification timestamps). Removals are delete class and ask the owner. Hand the record to the CISO with `excom_send_handoff` (kind request).

## Output

```text
Register row: id | role | entity (kept in system of record) | owner | start | end | scope link | agreement status | budget (CFO) | access granted | classification review date | next action
Statement of work draft | Classification questions for the CLO
Renewal review or offboarding record with dates
```

## Approvals

- Engaging, renewing, ending or classifying a contractor: legal or people, the owner.
- Signing or sending the agreement: the owner through the CLO.
- Any payment or deposit: spend.
- Invites and removals: permission change or delete, the project owner.
- Messages to the contractor: send.

## Example

A freelance translator at Acme has worked 7 months on the same monthly task. The renewal review shows deliverables met, spend in line, and flags tenure past 6 months with three classification questions for the CLO. The owner decides to convert the work to a fixed-scope project with an end date.

Adapted from tuanductran/hr-skills (skills/hr-contingent-workforce), MIT. Modified: rewritten generic for EXCOM.
