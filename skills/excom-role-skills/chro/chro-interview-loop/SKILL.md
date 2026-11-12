---
name: chro-interview-loop
description: Designs a structured interview loop with stages, a question bank, behaviourally anchored scorecards, a debrief agenda and a decision record the owner signs. Use when shortlisted candidates move to interview, when a contractor needs a trial task or working session, when someone asks "what should we ask them" or "how do we compare these candidates", or when an interviewer needs a briefing.
version: 2.0.0
---
# Interview loop and scorecards

Gives every candidate the same questions, scored against the same anchors, ending in a written decision record. Structured interviews predict performance better than conversation and protect the team when one person decides.

## Look up first

- The approved brief and screening rubric: `excom_recall`, or `excom_knowledge_search` "hiring brief <role>".
- Who interviews and whether a paid work sample is allowed: from the owner. If unknown, ask with `excom_propose_task` (needs_decision true).
- Real rules candidates may be tested on (pricing rules, partner programme terms, approval rules): `excom_knowledge_search` "partner programme terms", "approval rules". Use them in situational questions; never invent rules.
- Calendar app granted (Google Calendar or Calendly); `excom_request_setup` with the service id gcal or calendly if not.

## Steps

1. Choose 4 to 6 competencies from the essentials and map each to one stage: screening call, structured interview, work sample, final conversation. If only one person interviews, say so and add a work sample to balance the single view.
2. Build the question bank from `references/question-bank-and-scorecard.md`: per competency two behavioural questions, one situational question set in the team's real context, two probes. Same questions, same order, for everyone.
3. Check every question for fairness (no protected characteristics; real requirements asked as "can you meet this").
4. Build the scorecard from the rubric anchors with a notes column for verbatim evidence and the scoring rules.
5. Scheduling: read availability with `gcal_find_free_slots` or `calendly_list_event_types`; draft invitations with `gmail_create_draft`. Creating events with `gcal_create_event` or links with `calendly_create_one_off_link` sends an invitation: send class.
6. Write the interviewer briefing (one page) and, after the interviews, the debrief agenda: scores and evidence per criterion before any overall view.
7. Draft the decision record with blank lines for the owner's decision and date; save with `excom_save_draft` and propose the decision with `excom_propose_task`. After a yes, ask the CLO for the contract with `excom_send_handoff` (kind request) and load `chro-onboarding-plan`.

## Output

```text
Interview loop: <role>
Stage | duration | competencies | interviewer | format
Question bank: competency | behavioural Q1, Q2 | situational Q | probes
Scorecard: criterion | anchor 1 | 3 | 5 | score | evidence notes
Interviewer briefing | Debrief agenda
Decision record: candidate id | scores | evidence | recommendation | decision (owner) | date
```

## Approvals

- Invitations, events or links to candidates: send.
- Paying for a work sample or recruiting tool: spend, with the amount.
- Hire or no-hire, offer, pay: legal or people, the owner.
- Sharing candidate notes outside the loop: only with the owner's approval.

## Example

For a support lead at Acme: four competencies, a 30-minute screen, a 60-minute interview, and a work sample "answer these three real tickets using the help centre". The situational question uses the team's actual refund rule from the knowledge base. Candidate C-03's decision record shows 4, 5, 3, 4 with quoted evidence; the owner signs "hire" with the date.

## References

- `references/question-bank-and-scorecard.md`: question patterns, scoring rules, debrief and decision record templates; read at steps 2, 4 and 6.

Adapted from anthropics/knowledge-work-plugins (human-resources/skills/interview-prep), Apache-2.0, and JordzPope/claude-skills-hiring-interviews (skills/structured-interview-guide, skills/decision-record), MIT. Modified: rewritten generic for EXCOM.
