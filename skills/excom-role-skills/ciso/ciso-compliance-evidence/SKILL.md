---
name: ciso-compliance-evidence
description: Keeps a catalogue that ties each security control the company says it runs to a dated record proving it ran, marks every control operating, designed only or gap, and plans the cheapest record that closes each gap. Use when preparing SOC 2 or ISO 27001 readiness, when an auditor, customer or partner asks for evidence, when the compliance platform flags failing tests or expiring evidence, or when someone asks "are we SOC 2 ready".
version: 2.0.0
---
# Compliance evidence catalogue

Show, control by control, what is proven, what is only written down and what is missing. Buyers ask for this before they sign; an honest catalogue shortens procurement without overclaiming.

## Look up first

- The control mapping: `excom_knowledge_search` for "SOC 2 mapping", "control matrix", "statement of applicability". It lists criteria, controls and where evidence lives. If missing, draft one from references/criteria.md with `excom_save_draft` and propose it.
- The criteria in scope (Security always; Availability, Confidentiality, Processing Integrity, Privacy only if chosen): read the decision with `excom_recall`. If no decision exists, ask the owner with `excom_propose_task` (needs decision true).
- Known gaps the team already accepted: search "security risks and open questions" and "risk register".
- Your compliance platform: Vanta or Drata, if granted; otherwise `excom_request_setup` with service vanta or drata, and work from the knowledge base.
- Last catalogue: `excom_recall`.

## Steps

1. Read platform state, reads only. If it is Vanta: `vanta_framework_readiness`, `vanta_failing_controls_by_framework`, `vanta_failing_tests`, `vanta_evidence_expiring_soon`. If it is Drata: `drata_framework_readiness`, `drata_failing_controls_by_framework`, `drata_failing_tests`, `drata_evidence_expiring_soon`.
2. For each control find the record that proves it ran in the period: approval cards and deploy records (change control), the last access review, the weekly vulnerability brief and scanner logs, incident drills and post-mortems, backup restore results, vendor reviews, policy approval dates. A policy or plan is design evidence, not operating evidence.
3. Mark each control: operating (record and date), designed only (policy, no run record), gap (neither). Accepted gaps stay gaps until a record exists.
4. Type I versus Type II: Type I tests design at a point in time; Type II tests operation over a period, usually 3 to 12 months. Never call the company Type II ready while operating evidence covers less than the period.
5. Plan each gap: the cheapest record that would close it, owner role, date. Propose with `excom_propose_task`; people evidence through the CHRO, technical evidence through the CTO.
6. Evidence uploads and links (`vanta_add_document_link`, `drata_create_evidence`) are record writes and ask under the team's autonomy. Never upload anything holding secrets, personal data or client material.
7. Record readiness figures read this turn with `excom_record_measurement`.

## Output

```text
Evidence catalogue <month>: framework, criteria in scope, platform readiness (tool)
| criterion | control | operating/designed/gap | evidence record | date | owner | expires |
Gaps: cheapest closing record, owner, date
Expiring within 30 days
Wording allowed externally this month (one line per claim)
```

Saved with `excom_save_draft`.

## Approvals

- Uploading, linking or deleting evidence in the compliance platform (record write or delete).
- Engaging an auditor, pentest vendor or paid platform tier (spend, with the cost).
- Any external statement about compliance status (send, through the revenue owner with the legal executive).

## Example

Acme, Security criteria only: 31 controls, 19 operating, 8 designed only, 4 gaps (no restore drill this year, no retained access review, no tabletop, vendor reviews undocumented). External wording this month: "We operate controls mapped to SOC 2 Security criteria; no SOC 2 report has been issued."

## References

- references/criteria.md: the SOC 2 criteria, typical evidence per criterion and the Type I versus Type II rules. Read at step 2 or when drafting a missing mapping; load with `excom_skill_load` or by paging.

Adapted from alirezarezvani/claude-skills (ra-qm-team/skills/soc2-compliance), MIT. Modified: rewritten generic for EXCOM.
