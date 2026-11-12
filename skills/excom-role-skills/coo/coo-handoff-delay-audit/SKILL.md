---
name: coo-handoff-delay-audit
description: Measures where work waits: handoffs between executives, approvals pending on humans, drafts waiting to be sent. It works from timestamps, not opinions, computes median and slow-case delays, finds the one constraint per flow, and proposes one fix per bottleneck. Use when the weekly audit is due, when a goal-critical flow is slow (a partner reply, affiliate onboarding, a failed payment follow-up, a release), or when someone asks "why did this take two weeks".
version: 2.0.0
---

# Handoff delay audit

Most elapsed time in operating work is waiting, not doing. Measure the waits, name the single constraint, fix it, and report delays as facts about queues, never as blame.

## Look up first

- The flows that matter for the team's outcomes (in your context): for example lead to signed partner, affiliate signup to first referral, failed payment to recovered, bug report to fix released, draft to approved send.
- Service-level targets and approval reminder settings: `excom_knowledge_search` "service levels" and your team settings. If none exist, propose a target (for example approvals answered within one business day) to the owner.

## Steps

1. Build each flow's stage list from records:
   - `excom_read_tasks` for created, claimed, updated and verified times.
   - `melaya_approval_list` through `melaya_tools` for approval waits.
   - `excom_pipeline_runs_list` for run waits.
   - The issue tracker if granted (`linear_get_issues`, `jira_search_issues`).
   Type each stage as value-add, wait or rework.
2. Over the last four weeks, compute each stage's median and slow case (P90). Then compute each flow's total cycle time and its value-add, wait and rework shares. A value-add share under 10 percent means the flow is mostly waiting.
3. Flag bottlenecks with fixed rules:
   - A stage whose median is more than twice the mean of the value-add stages.
   - Waiting above 40 percent of the cycle.
   - Rework above 15 percent.
   - Any approval or handoff past its service-level target.
4. Name the constraint: the one stage that limits the flow. Speeding up any other stage only piles work up in front of it.
5. Rank the five slowest handoffs across all flows by measured delay and their effect on revenue, cost or customers.
6. Propose one fix per bottleneck, aimed at the constraint:
   - Remove the handoff.
   - Batch the approvals.
   - Propose a standing rule after repeated identical approvals.
   - Set an approver order or a reminder.
   - Turn the step into a pipeline.
7. Save with `excom_save_draft`. Record the median and slow-case values per flow with `excom_record_measurement`. Ask each owner for a fix date with `excom_send_handoff` (kind request) and track it with `excom_propose_task`.

## Output

```text
Handoff audit, weeks <range>
| Flow | Cycle median | Cycle P90 | Value-add % | Wait % | Rework % | Constraint |
Five slowest handoffs: from | to | median wait | P90 wait | effect | evidence
Bottlenecks: stage | rule hit | fix | owner | date
```

## Approvals

- Changing approval routing, reminders, rules or team settings is the owner's or an approver's decision, and asks.
- Messaging people outside the team about delays is a send, and asks.

## Example

At Acme, the time from an affiliate's application to their approval has a median of 6 days. Of that, 5.5 days is an approval card waiting for the owner. Fix: batch affiliate approvals into one daily card and propose a standing rule for applicants who meet the published criteria.

Adapted from alirezarezvani/claude-skills (business-operations/skills/process-mapper/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
