# Health score

Score each component 0 to 100, higher is healthier, before weighting. The weights are an illustrative start; validate them against real renewals and cancellations before trusting the tiers.

## Components

| Component | Weight | 100 looks like | 0 looks like |
|---|---|---|---|
| Usage | 30 | Usage at or above the account's own first two weeks | No use for 14 days |
| Value | 25 | Most runs or answers succeed | Most fail |
| Breadth | 15 | Several products, surfaces or workflows in use | One abandoned workflow |
| Support sentiment | 15 | Positive or no open issues | Unanswered complaint, repeated failures |
| Billing health | 15 | Paid on time | Failed payment or cancellation started |

## Coverage rule

- A signal older than 14 days, or not readable, is unavailable.
- Score = sum(weight x observed score) / sum(observed weights).
- Report coverage = sum of observed weights.
- Below 60 percent coverage: "insufficient data", no tier, no automated action.

## Tiers (illustrative)

| Score | Tier | Default action |
|---|---|---|
| 80 to 100 | Healthy | Note expansion or reference potential for the CRO and CMO |
| 60 to 79 | Needs attention | A proactive, useful check-in |
| 40 to 59 | At risk | Cause-based intervention this week |
| 0 to 39 | Critical | Personal note drafted for the owner |

## Leading signals, flag regardless of score

- Usage down 50 percent or more for two weeks.
- The key product stopped (device offline, runner offline, no runs).
- Repeated failures on the same error.
- Billing page visits, a cancellation started, seats removed, a data export.
- An unhappy thread unanswered for more than one working day.
- A failed payment (check the billing rules for whether access stops at once).
