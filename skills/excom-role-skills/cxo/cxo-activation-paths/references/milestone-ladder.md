# Milestone ladder and blocker checks

## Ladder template, one per product

```text
Product: <name from the products note>
Tutorial: <public first-success tutorial title>
Time to first success: <minutes, from the tutorial>
Aha: <first moment of value, e.g. a real answer, a task done on a device>
Activated: <the action that predicts return, e.g. a successful run, then a second day>
Sticky: <habit, e.g. a saved or scheduled workflow, approvals set>
Steps: 1) 2) 3) 4)
Common failure at each step: <from troubleshooting notes>
```

Keep 3 to 5 milestones per product. Tie each to a customer outcome, not a feature click.

## Generic funnel rungs

Registered, verified, connected an engine (a model key, a local runner, or a demo model), used the product, got value, paid. The ladder is not always monotonic (a demo model can deliver value with no key), so read the furthest stage each user reached rather than subtracting rungs.

## Blocker checks, in order

| Blocker | Evidence | Next step |
|---|---|---|
| Model cannot call tools | Runs on a free or small model, agents could not act | Switch to a tool-capable model or the user's own key |
| No engine connected | Verified, no key and no runner | Connect one model in a minute |
| Local runner never online | Runner token created, never seen | The packaged desktop install, or a cloud model instead |
| Device not paired | Device product chosen, no device | Pair on the device; codes expire quickly |
| Approval waiting | Run paused on an approval | Where to approve |
| Plan limit | Free limit used | Hand to the CRO |
| Busy, nothing failed | One session, no errors | A template matched to their stated goal |

## Rules

- One product and one next step per user.
- Every step links a public note that exists today.
- No internal ids, no promised dates or features.
