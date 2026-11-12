---
name: ceo-goal-tracker
description: Tracks the team's outcomes over their horizon. For each one it gives baseline, today, the value expected today and the target, with green, amber or red status, a leading indicator, and a recovery plan for anything behind. Use when the week starts, when the owner asks "are we on track", when a colleague reports a result, at the third and two-thirds points of the horizon, or when a goal such as customers, partners or affiliates looks behind.
version: 2.0.0
---

# Goal tracker

One live view of the team's outcomes, with the leading indicators that predict each one weeks before it lands. The point is no surprise at the end of the horizon.

## Look up first

- The outcomes, their targets, their horizon and their start date: the team's outcomes in your context. If an outcome has no target or horizon, propose one to the owner with `excom_propose_task` (needs_decision). Do not track an invented target.
- How each outcome is counted: `excom_knowledge_search` "metrics definitions". If an outcome counts affiliates or partners and the note lacks a definition, propose these defaults to the owner and to the CDO:
  - An active affiliate has generated at least one referred signup. Anyone else is only an account.
  - A signed partner has its signed agreement filed in that partner's folder under the team's partner agreements folder in Google Drive. Get the folder id from the knowledge base ("partner agreements folder").
- Last readings: `excom_recall`.

## Steps

1. Restate each outcome as a key result: definition, baseline at the start, target, horizon. Outputs ("launch X") are not results. Ask which number X should move.
2. Read today's value from the source of truth.
   - Paying customers: `stripe_list_subscriptions` (status active), with staff and test accounts excluded per the definitions note.
   - Affiliates: `affonso_list_affiliates`, then `affonso_get_affiliate_analytics` per affiliate (or your affiliate platform's equivalent). Count only those with at least one referred signup.
   - Partners: `drive_search` inside the partner agreements folder. Count partners whose folder holds a signed agreement. Drafts and unsigned versions do not count.
   - Other outcomes: the tool named in the definitions note. If the app is not granted, call `excom_request_setup` and mark the outcome "not measured".
3. Pick one leading indicator per outcome. Examples: checkout starts and first successful use for customers, affiliates with a first click for active affiliates, agreements sent for signature for partners.
4. Expected today = baseline + (target - baseline) x elapsed share of the horizon. Green when at or above 90 percent of expected, amber at 70 to 90 percent, red below 70 percent or when the leading indicator fell two weeks running.
5. For each amber or red outcome, write one change, its owner, and the date the leading indicator should move. Red goes to the owner through the priority reset skill.
6. Record each reading with `excom_record_measurement`. Update the outcome tasks with `excom_update_task` or `excom_propose_task`. Put the table in the weekly brief draft (`excom_save_draft`).

## Output

```text
Outcomes, day D of H (start <date>), read <time>
| Outcome | Definition | Baseline | Today | Expected | Target | Status | Leading indicator (trend) | Source |
Amber/red plans: outcome | change | owner | date the indicator should move
Definitions pending: outcome | proposed default | sent to
```

## Approvals

- Changing an outcome, its target or its horizon is the owner's decision. Propose it, never edit it.
- Recovery plans that spend money (ads, incentives, paid listings) ask, with the cost.

## Example

Acme's outcome is "N active affiliates in 90 days". On day 30, 120 affiliates are enrolled but only 22 have a referred signup, so 22 count. Expected by now: 33. 22 / 33 = 67 percent, so the status is red. Plan: the partnerships role sends a first-post kit to the 98 inactive accounts (owner: partnerships). The indicator to watch is first clicks, due within 10 days.

Adapted from TerminalSkills/skills (skills/okr-planning/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
