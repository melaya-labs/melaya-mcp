---
name: chro-hiring-brief
description: Turns a vague need for a person into an outcome-based hiring brief and a fair, inclusive job description draft the owner can approve. Use when the owner or another executive says "we need someone for", asks to scope a first hire, a contractor or a freelancer, wants a job description written or checked for bias, or before any job ad is posted, even if they only describe the work.
version: 2.0.0
---
# Hiring brief and job description

Produces a one-page brief and a job description that screen on what predicts success in the work, so the role is scoped honestly before anyone is contacted. A clear brief also says why a human is needed where an agent or a managed pipeline could do the job.

## Look up first

- The team's outcomes and your charter objectives (in context): which outcome the role moves. `excom_recall` for any earlier brief or hiring decision.
- The hiring policy and first-hire criteria: `excom_knowledge_search` "hiring policy", "first hire", "people policies", then `excom_knowledge_read`. If none exists, ask the owner with `excom_propose_task` (needs_decision true): "What would trigger this hire, and who approves the pay range?"
- Pay ranges and employment types: only from an approved note or the owner. Never estimate; leave "Verify" placeholders.
- Brand voice for public text: `excom_knowledge_search` "brand voice". If missing, write plain and neutral.

## Steps

1. Run a short intake with the requester through `excom_send_handoff` (kind question): at most five questions, each with a default (purpose, outcomes in 6 to 12 months, day-one skills, work pattern and time zones, employment type considered).
2. Write the purpose line and 3 to 6 observable outcomes ("signs N partners from the current pipeline by day 60"), not activities. If the scope is really two roles, say so.
3. Derive requirements from outcomes. Apply the job test to each essential: could someone without it do the job well after normal induction? If yes, move it to desirable or cut it. Cap essentials at 6; replace year counts with the capability they stood for; drop degree filters unless a licence requires one.
4. Apply the exclusion test with `references/fairness-checks.md`: rewrite or justify anything that could disadvantage a protected group, and mark each justification for the owner to confirm.
5. Separate conditions (right to work, hours, equipment) from scored criteria. Conditions are checked the same way for everyone and never scored.
6. Draft the job description (500 to 800 words, plain words, adjustments statement with a contact route that is not the decision maker). Save brief and description with `excom_save_draft`. A Docs copy with `docs_create` is a record write; if Docs is not granted, `excom_request_setup` with the service id google_docs.
7. Ask the CLO with `excom_send_handoff` (kind request) to review employment-type wording and jurisdiction statements. Then propose "owner approves brief and pay range" with `excom_propose_task`, and load `chro-screening-rubric` next.

## Output

```text
Hiring brief: <role>   status: draft for owner
Outcome it moves: <team outcome>   Why a human: <reason>
Outcomes (6 to 12 months): 1..6, observable
Essentials (max 6): criterion | why | how we will test it
Desirable (max 4)
Conditions (not scored)
Employment type considered (owner decides with CLO) | Pay range: approved or "Verify"
Assumptions | Changes made (check job only)
```

## Approvals

- Publishing or sending the ad anywhere: send.
- Paid job boards or recruiters: spend, quote the cost first.
- Deciding to hire, the employment type and the pay: legal or people, the owner decides.
- Creating the document in a shared drive: record write.

## Example

The owner writes "we need help with partners". The brief comes back with purpose "run partner onboarding so signed partners launch within 14 days", four outcomes tied to the team's partner outcome, five essentials each with a test, "5 years in SaaS" rewritten as "has run a partner or customer onboarding end to end", and pay range "Verify: not approved".

## References

- `references/fairness-checks.md`: job test, exclusion test and wording checks; read at step 4 (page it, or `excom_skill_load` with the section name).

Adapted from sara-hamza/people-ops-claude (plugins/people-ops/skills/job-description-builder) and JordzPope/claude-skills-hiring-interviews (skills/hiring-manager-intake, skills/essential-criteria-review), MIT. Modified: rewritten generic for EXCOM.
