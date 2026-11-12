---
name: ceo-decision-memo
description: Turns an open question into a one-page decision memo for the owner. It holds two or three real options plus doing nothing, what each costs and defers, its reversibility, one recommendation, and the signal that would reopen it. Use when executives disagree, when a choice is one-way (a price, a contract term, a public claim, a spend), when a weekly brief decision needs more than three lines, or when someone asks "should we...".
version: 2.0.0
---

# Decision memo

A memo the owner can decide in five minutes. Decisions taken this week instead of next month are how outcomes move.

## Look up first

- The team's outcomes (in your context). Every option is judged by its effect on them.
- Past decisions on the same topic: `excom_recall`. A rejected proposal reopens only with new evidence.
- The approval rules in your charter (what always asks), and the current offer: `excom_knowledge_search` "pricing and plans" or "programme terms" when the decision touches them. If a needed fact is missing, ask the owner one precise question with `excom_propose_task` (needs_decision). Never assume the fact.

## Steps

1. Frame the decision as one question the owner answers yes or no, or by picking an option. Name the outcome it moves.
2. Collect evidence from owners with `excom_send_handoff` (kind question): the CFO for cost and cash, the CDO for the metric and its baseline, the COO for operating load, the revenue or partnerships role for customer and partner effect. Read the key numbers yourself where you have the app.
3. Write two or three real options plus "do nothing for now". For each, state what it gets, what it costs (money, people time, engineering time), what it defers, the main risk, and the first measurable signal of success.
4. Rate reversibility. Two-way door: undone within a week at low cost. Costly to reverse: a public page, a programme change with a lock-in. One-way: a published price, a signed term, a spend. One-way options always go to the owner, whatever the autonomy mode.
5. Recommend one option. State the assumption it rests on, labelled as an estimate, and the reopen trigger (a measurable signal and a date).
6. Save with `excom_save_draft` (draft). When the owner decides, record it with `excom_publish_decision`, log it with the trade-off log skill, and propose follow-ups and a review task with `excom_propose_task`.

## Output

```text
Decision: <question>
Outcome moved: <outcome>
Context: 3 to 5 facts, each with tool, window, read time
Options:
  A <name>: gets | costs | defers | risk | first signal | reversibility
  B <name>: same
  C Do nothing for now: same
Recommendation: <option>, because <reason>; rests on <assumption, estimate>
Reopen trigger: <signal, date>
Approvals needed: <spend / price / send / legal>, and who approves
Review date: <date>
```

## Approvals

- Options that spend money, change a price, commit to a legal or partner term, or publish a claim are decided by the owner, always.
- Sending the memo outside the team is a send, and asks. The memo itself executes nothing.

## Example

"Should Acme add a yearly plan at a discount before quarter end?" A: launch now (cash now, lower revenue per customer, costly to reverse). B: test with 20 accounts (slower, reversible). C: do nothing. Recommendation: B, resting on the assumption that yearly buyers churn less. Reopen trigger: 10 yearly purchases in two weeks.

Adapted from anthropics/knowledge-work-plugins (product-management/skills/stakeholder-update/SKILL.md, decision records), Apache-2.0. Modified: rewritten generic for EXCOM.
