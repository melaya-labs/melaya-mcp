---
name: ceo-strategic-bet-review
description: Reviews each strategic bet: a channel, a product push, a partner or affiliate programme, a pricing move. It checks the bet against failure signals written in advance, models what happens when two or three risks hit at once, and sets trigger points with a continue, double down, change or stop call. Use when the monthly bet review is due, when a bet's signal date arrives, before approving a new bet, or when two bad signals show up in the same week.
version: 2.0.0
---

# Strategic bet review

Every bet toward the team's outcomes needs written failure signals and a kill or double-down trigger. Without them, a losing bet keeps its budget by default.

## Look up first

- The active bets: `excom_recall` "bets", the decision log, and the last monthly report. If no register exists, build one from the decisions published so far and propose it to the owner.
- The outcomes each bet serves (in your context), and the risk notes: `excom_knowledge_search` "risks and open questions".
- Runway: ask the CFO with `excom_send_handoff` (kind question). Never estimate cash yourself.

## Steps

1. Give each bet one register line: the bet in one sentence, the outcome it serves, the money and time committed, the start date, the success signal, the failure signal, and the date the signal must show. Write missing signals before you read any data. Signals written after the data are rationalisations.
2. Read each signal this turn from its owner or source. For example, paid search: first-party signups and purchases per spend from the CFO and CDO. A product push: `stripe_list_subscriptions` by product. An affiliate programme: `affonso_get_affiliate_analytics` (if on Affonso).
3. Mark each bet on track, failure signal present, or too early. "Too early" is not success.
4. Choose at most three variables that could hit together. For each, state what changes, the probability (labelled as an estimate) and the timing.
5. Map the cascade role by role: CFO (cash), revenue (pipeline), CMO (acquisition cost), COO (capacity), CTO (delivery), CDO (measurement). Name where it can be interrupted, for example "if checkout starts fall below N a week, pause paid search before cash is touched".
6. Model three severities. Base: one variable. Stress: two. Severe: all three. Give the effect on each outcome and on runway, and the date it becomes unacceptable.
7. Set trigger points: a measurable signal, a threshold, the tool that reads it, and the role that watches it.
8. Recommend continue, double down (with the cost), change, or stop. Stop and double-down calls go to the owner through a decision memo. Save with `excom_save_draft`. Record readings with `excom_record_measurement` and triggers with `excom_record_fact`. Propose watcher tasks with `excom_propose_task`.

## Output

```text
Bet register (read <date>)
| Bet | Outcome | Committed | Success signal | Failure signal | Signal date | Reading (tool, window) | State | Call |
Scenario: variables A, B, C (probability, timing; estimates)
Cascade: trigger, then role by role, with interruption points
Severity: base / stress / severe: effect on outcomes, runway, date unacceptable
Triggers: signal | threshold | tool | watcher
```

## Approvals

- Stopping, scaling or re-budgeting a bet spends or frees money. The owner decides, with the cost stated.
- Pausing ads or changing an offer in another role's system asks, and goes through that role.

## Example

Bet: "Acme partners resell the product". Failure signal: fewer than 3 signed partners with a referred customer by week 8. Reading at week 8: 1. Recommendation: change. Narrow to one partner type, and reopen if 2 more sign by week 12.

Adapted from alirezarezvani/claude-skills (c-level-advisor/skills/scenario-war-room/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
