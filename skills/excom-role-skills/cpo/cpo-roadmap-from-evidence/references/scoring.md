# Evidence scoring

## Source weight

| Source | Weight | Why |
|---|---|---|
| Usage signal (eval failures, funnel drop, activation stall) | 3 | Behaviour, not opinion |
| Ask from a paying customer or a signed partner | 3 | Revenue at stake |
| Bug report with a reproduced run | 2 | Verified, but one account |
| Support thread | 1 | Real, often duplicated |
| Prospect, community or social ask | 1 | Signal of demand, low certainty |

A theme backed by a single source is marked "weak" whatever its score.

## Reach

Accounts affected, read this turn. Use the count directly when under 100, otherwise bands: 100 to 499 counts as 150, 500 or more counts as 600. Exclude owner, test and internal accounts.

## Outcome fit

| Fit | Multiplier |
|---|---|
| Moves a team outcome directly | 2 |
| Moves it indirectly (retention, activation, trust) | 1 |
| No link to any outcome | 0.5 |

## Score

Score = sum of source weights x reach x outcome fit.

## Opportunity score (when satisfaction data exists)

Opportunity = importance x (1 minus satisfaction), both on a 0 to 1 scale. High importance and low satisfaction are the best opportunities. Without satisfaction data, write "not measured" rather than guessing.

## Effort and risk

Effort S (under a week), M (one to three weeks), L (more). Flag risk separately: a migration, a release of something users install, a store submission, a change to an extension or desktop app, a legal or security review. High risk lowers the rank only when the score gap is small.
