---
name: ceo-tradeoff-log
description: Keeps one append-only log of trade-offs between executives and the owner's calls on them. Each entry records options, the decision, one owner, due and review dates, what it supersedes, and rejected proposals that must not resurface without new evidence. Use when two roles compete for the same week, budget or engineer, after the owner decides anything, when an old argument comes back, or on the weekly check for overdue actions.
version: 2.0.0
---

# Cross-executive trade-off log

The log stops the same argument from being replayed every week. It catches two decisions that contradict each other and gives every action one owner.

## Look up first

- Existing entries: `excom_recall` "trade-off log" and earlier `excom_publish_decision` records.
- The competing asks: `excom_read_tasks` and the handoffs you received.
- Who approves what: your charter's approval rules. If they are unclear for this resource, ask the owner with `excom_propose_task` (needs_decision).

## Steps

1. Frame the trade-off. Name the shared resource, each ask, the outcome each serves, and the cost of delay. One sentence each.
2. Ask each requesting executive with `excom_send_handoff` (kind question): the measurable result expected, the latest date it still matters, and their plan without the resource. Read the answers independently.
3. Check the log before writing:
   - Rejected before. Show the date and reason. Reopen only on the owner's explicit request or new evidence.
   - Contradiction. Two active decisions on one topic disagree.
   - Owner clash. One action has two owners.
   Offer one of: supersede the old decision, merge the two, or let the owner choose.
4. Recommend one allocation, ranked by outcome impact, then reversibility, then cost of delay. Name what is deferred and until when.
5. Draft with `excom_save_draft` and put the question in the weekly brief.
6. After the owner decides, publish with `excom_publish_decision` and record the entry with `excom_record_fact`. Mark the superseded entry. Never delete an entry, because the history is the record.
7. Propose the actions with `excom_propose_task`, one owner each. Tell the affected executives what they get and what is deferred with `excom_send_handoff` (kind request).
8. Weekly: list overdue actions and decisions past their review date, and carry them into the brief.

## Output

```text
[date] <title>
Trade-off: <resource>, asks from <role A> and <role B>
Decision: <one statement> | Owner: <role> | Due: <date> | Review: <date>
Rationale: <1 to 2 sentences>
Owner override: <what changed from the recommendation, or blank>
Rejected: <proposal> because <reason> (reopen only on explicit request or new evidence)
Actions: <action> | owner | due
Supersedes: <date or none> | Superseded by: <filled later>
```

## Approvals

- The decision belongs to the owner. You propose, record and follow up.
- Moving money between roles is spend, and asks with the amount.
- Notifying people outside the executive team is a send, and asks.

## Example

The CPO wants the CTO for an onboarding fix. The CMO wants the CTO for a launch page. Both need the same week. Recommendation: onboarding first, because activation is the outcome furthest behind. The launch page is deferred one week, and the CMO is told the review date.

Adapted from alirezarezvani/claude-skills (c-level-advisor/skills/decision-logger/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
