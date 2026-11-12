---
name: chro-team-rhythm-workload
description: Measures the human owner's approval and meeting load and the executives' task and pipeline queues from systems of record, finds system patterns, and proposes a sustainable rhythm (batched approvals, rule candidates, paused low-value work). Use when the weekly people check is due, when approvals pile up or expire, when the owner says the load is too high, or before adding a pipeline or executive that adds approvals.
version: 2.0.0
---
# Team rhythm and workload health

In an EXCOM company the team is a few humans plus AI executives, so workload health means the humans' load (approvals waiting, meetings, messages that need a person) and the executives' queues. When approvals pile up, every outcome slows.

## Look up first

- The team's rhythm (board review time, weekly and monthly cadence): `excom_knowledge_search` "team rhythms", "weekly rhythm". If missing, propose one with `excom_save_draft`.
- The owner's working hours and preferred approval slot: `excom_recall`; if unknown, ask with `excom_propose_task` (needs_decision true).
- Last week's measurements: `excom_recall` (compare only when they exist).
- Calendar app granted; if not, skip meeting load and say so.

## Steps

1. Approval load: `melaya_approval_list`. Count pending items, age of the oldest, group by class (send, spend, legal or people, permission) and by role. List expired approvals: they are lost work.
2. Executive queues: `excom_read_tasks` for overdue, waiting on human, blocked and outcome unknown, by role. `excom_pipeline_status` for failing or paused pipelines.
3. Meeting load, only if a calendar is granted: `gcal_list_events` for the week (count and hours; no titles or attendee names copied).
4. Find patterns in the system, not in people: approvals arriving outside working hours, the same action approved three times with the same scope (a rule candidate), roles sending many low-value approvals, duplicate asks.
5. Propose changes ranked by hours saved: one daily approval slot; rules for repeated same-scope approvals (never for spend, delete, production or legal or people); moving non-urgent items to the weekly slot; pausing a pipeline whose output nobody uses.
6. Record pending approvals, oldest age and overdue tasks with `excom_record_measurement`, each with its source.
7. Save the note with `excom_save_draft`; send proposals to the COO or the role concerned with `excom_send_handoff` (kind request).
8. Never comment on health, mood or personal circumstances, and never infer them from activity data.

## Output

```text
Workload check: week of <date>   sources: approvals, tasks, pipelines, calendar (if granted)
Metric | value | last week | source | read at
Pending approvals by class and role; oldest age
Overdue or blocked tasks by role | failing or paused pipelines
Patterns (system, not person)
Proposals: change | hours saved (estimate, labelled) | owner | needs approval
```

## Approvals

- Pausing or rescheduling a pipeline: pipeline schedule, always asks.
- Creating a rule from repeated approvals: the approver accepts or narrows it.
- Moving or creating calendar events: send.
- Another role's autonomy or grants: never changed by this skill.

## Example

Acme's owner has 41 pending approvals, the oldest 3 days old; 19 are the same "append ledger row" action from one outreach pipeline. The proposal: a rule for that action with a daily cap (saves about 20 minutes a day, estimate), and a single 09:00 approval slot. Expired approvals: 4, listed with their tasks.

Adapted from tuanductran/hr-skills (skills/hr-wellbeing), MIT, and anthropics/knowledge-work-plugins (human-resources/skills/people-report), Apache-2.0. Modified: rewritten generic for EXCOM.
