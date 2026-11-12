---
name: ceo-priority-reset
description: Resets priorities when an outcome slips. It finds orphan work that serves no outcome, roles pulling against each other, and outcomes nobody owns, locates the stage that blocks the slipping outcome, and proposes a short stop, keep and start list for the owner. Use when the goal tracker shows red, or amber two weeks running, when the owner asks why a goal is behind, at the midpoint of a horizon, or when the team feels busy but outcomes do not move.
version: 2.0.0
---

# Priority reset when goals slip

When an outcome is behind, the cause is rarely effort. It is usually one of three things: work that does not connect to the outcome, two roles pulling against each other, or an outcome nobody owns.

## Look up first

- The outcomes, their tracker reading and leading indicators (in your context, and `excom_recall`).
- Open work: `excom_read_tasks`. Managed pipelines: `excom_pipeline_list` and `excom_pipeline_status`.
- Funnel stage definitions: `excom_knowledge_search` "metrics definitions". If missing, ask the CDO with `excom_send_handoff`.

## Steps

1. State the priority for the rest of the horizon in one sentence, naming the outcome and the lever. If it takes a paragraph, it is not a priority yet.
2. Articulation test. Ask every executive with `excom_send_handoff` (kind question): "What is the single most important priority until the end of the horizon, and which of your tasks serves it most?" If fewer than most of them agree, restate the priority before moving any task.
3. Map every open task and pipeline to an outcome. If it is fully done, does it move the outcome directly, or only in theory?
4. Find the three failure patterns:
   - Orphans: connect them or stop them.
   - Conflicts: one role's success hurts another's, for example discounts that undercut a pricing test, or outreach volume that floods support. Pick one shared metric.
   - Gaps: an outcome with no owner or no task this week. Name an owner.
5. Find the blocking stage of the slipping outcome. For example, high checkout starts with low paid conversion points at checkout or price, not acquisition. Confirm with the CDO.
6. Build the list. Stop: orphans and low-yield work, with the time or money freed. Keep: direct contributors. Start: at most two actions aimed at the blocking stage, each with an owner and a dated signal.
7. Draft with `excom_save_draft` as a decision for the owner. After the owner decides, `excom_publish_decision`. Then `excom_update_task` for the changes, `excom_pipeline_change` to pause stopped pipelines (this asks), and tell each executive with `excom_send_handoff` (kind request).

## Output

```text
Priority until <end>: <one sentence>
Articulation: x of y executives named it
Slipping outcome: <outcome>, blocking stage <stage> (evidence, tool, window)
Orphans | Conflicts | Gaps: item | owner | action
Stop / Keep / Start: item | owner | freed or needed effort | dated signal
```

## Approvals

- Re-prioritising other executives' work is the owner's call. You propose.
- Pausing, retiring or rescheduling a managed pipeline asks.
- Start items that spend money ask, with the cost.

## Example

Acme's customer outcome is red. Five tasks serve awareness and none serve checkout. Stop two content tasks (freeing 6 hours a week). Start: a checkout error audit (CTO, signal by Friday) and a pricing page FAQ (CMO, signal: fewer checkout exits within 2 weeks).

Adapted from alirezarezvani/claude-skills (c-level-advisor/skills/strategic-alignment/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
