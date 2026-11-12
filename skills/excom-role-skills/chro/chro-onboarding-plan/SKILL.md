---
name: chro-onboarding-plan
description: Builds a dated onboarding plan for a new hire, contractor or workspace teammate: access request with least privilege, invite and two-factor, policy acknowledgements, Day 1 and Week 1, 30/60/90 goals, and an evidence record for the CISO. Use when someone has a start date, when a teammate is invited into a project, when asked "how do we get them set up", or when an onboarding record is missing for an audit.
version: 2.0.0
---
# Onboarding plan for a hire or contractor

Gets a new person productive in the first week and leaves an audit-ready record: who asked, who approved, what access at what role, two-factor on, policies acknowledged.

## Look up first

- The decision that triggers onboarding: `excom_read_tasks` or `excom_recall`. Without a human decision, stop: the trigger is a legal or people decision.
- The onboarding and access procedure: `excom_knowledge_search` "access provisioning", "onboarding checklist", then `excom_knowledge_read`. If missing, use `references/onboarding-checklist.md` and propose saving it as the team's procedure with `excom_save_draft`.
- The policy set to acknowledge: `excom_knowledge_search` "information security policy", "acceptable use", "remote working". If missing, ask the owner with `excom_propose_task` (needs_decision true).
- Seats on the plan and project roles: `melaya_project_list`, `melaya_team_list`.
- The team's outcomes (in context) for 30/60/90 goals.

## Steps

1. Record the access request (role, projects, start date, reason per project) with `docs_create` (record write). The requester cannot approve their own request; if the team has one person, flag the missing second approver to the owner.
2. Check seats with `melaya_team_list` and propose the narrowest role: viewer first, runner if they must run pipelines, editor only with a written reason. The invite through `melaya_team_invite` is a permission change and always asks the project owner; it never grants owner.
3. Draft the welcome mail (logistics, two-factor within 24 hours, desktop app or runner install) with `gmail_create_draft` or `zoho_email_save_draft`. Sending asks.
4. List the connectors their pipelines need and whether shared pipelines use personal or project connectors; that choice is the owner's.
5. Build the acknowledgement pack from the policy set; the person signs, record the date. For a contractor the agreement goes through the CLO first.
6. Write Day 1, Week 1 and 30/60/90 goals from the checklist reference, each goal tied to a team outcome and a data source.
7. Confirm the runner or desktop app is online with `melaya_runner_status` once installed, because this is the step that most often stalls.
8. Close the checklist with dates (`docs_insert_markdown`), hand it to the CISO with `excom_send_handoff` (kind request), and record time to onboard with `excom_record_measurement` from dates read this turn.

## Output

```text
Onboarding plan: <role>  start <date>  type <employee/contractor/teammate>
Access: project | role | reason | approved by | date
Pre-start | Day 1 | Week 1 checklists
30/60/90: goal | data source | team outcome
Acknowledgements: policy | version | signed date
Evidence: two-factor date | runner online date | sent to CISO date
```

## Approvals

- Invites, role changes, connector sharing: permission change, the project owner.
- Welcome mail and calendar invites: send.
- Equipment or software seats: spend, with the amount.
- Account creation and permission flags: platform admin only.

## Example

A contractor joins Acme's marketing project on Monday. Plan: runner role on one project (reason: runs the weekly report pipeline), welcome draft with the two-factor deadline, acknowledgement of three policies, Week 1 task "run the report pipeline and fix one failing step", 30-day goal tied to the team's content outcome.

## References

- `references/onboarding-checklist.md`: pre-start, Day 1, Week 1 and goal templates plus the evidence lines; read at step 6.

Adapted from anthropics/knowledge-work-plugins (human-resources/skills/onboarding), Apache-2.0, and sara-hamza/people-ops-claude (plugins/people-ops/skills/onboarding-planner), MIT. Modified: rewritten generic for EXCOM.
