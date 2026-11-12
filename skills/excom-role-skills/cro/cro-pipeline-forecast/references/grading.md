# Pipeline grading and guardrails

## Grades and exit criteria

| Grade | Exit criteria |
|---|---|
| Commit | Checkout started or a written yes on a plan, next step dated within 7 days, owner named |
| Best case | Hot lead (score 80 or more) with value seen in their own usage, or a call booked |
| Pipeline | Warm lead with a dated next step |
| Upside | Worth keeping, no dated next step |

An opportunity without a dated next step can never be commit.

## Default forecast weights

| Grade | Weight |
|---|---|
| Commit | 0.7 |
| Best case | 0.3 |
| Pipeline | 0.1 |
| Upside | 0 |

Replace the defaults with observed conversion once there are at least 20 closed outcomes per grade, and say so in the memo.

## Guardrails

- Coverage: best case plus commit below twice the customers still needed this month.
- Volatility: commit count moved by more than 5 in a week without a written reason.
- Accuracy: forecast missed two weeks in a row by more than 20 percent.
- Hygiene: a commit without a next step or an owner.

On any breach: a short memo to the CEO (what broke, why, the fix proposed, the decision needed).

## Inspection questions

1. What changed since last week (contact, budget, competition, product gap)?
2. Is the next step verifiable, dated and owned?
3. What negative signals exist (failed usage, silence, price objection, legal)?
4. If it slips, what backfills it?
