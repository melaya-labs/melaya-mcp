# Bug severity

Use the team's own table when the knowledge base has one; this is the generic default.

| Severity | Meaning | Response |
|---|---|---|
| S1 | Data exposure, money moved wrongly, a send or write without approval, a whole product down | Tell the CTO at once; the CISO declares the incident when security is involved |
| S2 | A core flow fails for many users with no workaround (setup, saving, approvals, a scheduled delivery) | Fix this week, add a regression case |
| S3 | One feature or connector fails, a workaround exists | Next release |
| S4 | Cosmetic, wording, a translation slip | Batch with docs or locale fixes |

## Mapping to incident levels

- S1 and S2 follow the incident severity table of the CTO and CISO. If an incident was declared, keep its level; the post-incident review may downgrade it, the CQO never does.
- A silent failure (status done, nothing delivered) is at least S2, because nobody notices until a customer does.

## Rules

- Severity is set from impact read this turn: users affected, money or data involved, workaround available.
- "Cannot reproduce" lists the steps tried and the environment used, and becomes needs info with a question.
- No personal data or tokens from attachments go into notes.
- A done state cites its receipt: the covering test or the passing run id.
- Rejected always carries a reason the CXO can give the reporter.

## Daily cadence

- Sweep open reports daily, needs info weekly.
- Reports naming a new failure kind or a paying account go first.
