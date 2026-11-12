---
name: ceo-weekly-board-brief
description: Builds the weekly brief for the owner, with three decisions to take this week, each backed by evidence read this turn, one owner and a due date, drawn from verified tasks, measurements and colleagues' independent views. Use when the week starts, when the owner asks "what needs me this week" or "where are we", when decisions pile up unanswered, or before a board or investor call.
version: 2.0.0
---

# Weekly board brief

One page, three decisions the owner must take this week. Each one rests on numbers read this turn and is tied to the team's outcomes. The brief turns the executives' work into human decisions instead of a status dump.

## Look up first

- The team's outcomes and your charter objectives (in your context). These are the goals every decision is ranked against.
- Last week's brief and its open decisions: `excom_recall`. If none exists, this is week one; say so.
- The metric definitions: `excom_knowledge_search` "metrics definitions". If missing, use the plain metric names, label them "definition pending", and ask the CDO with `excom_send_handoff`.
- The day and time the team expects the brief, and where it is filed: `excom_knowledge_search` "weekly rhythm" or "reports folder". If not found, ask the owner with `excom_propose_task` (needs_decision).

## Steps

1. List last week's open decisions and whether each was taken. An overdue decision becomes decision one unless the owner closed it, because unanswered decisions are the most expensive item on the page.
2. Read `excom_read_tasks` for tasks verified or failed since the last brief. Only verified tasks count as progress. A task marked done without verification is reported as "claimed, not verified".
3. Read each outcome's current value from its source, for example `stripe_list_subscriptions` for paying customers, `affonso_get_affiliate_analytics` for affiliates (if your programme runs on Affonso), and `drive_search` on the partner agreements folder for signed partners. Use the team's definitions. If an app is not granted, call `excom_request_setup` and write "not measured".
4. Ask each executive who owns a candidate decision with `excom_send_handoff` (kind question): at most five points, each tagged VERIFIED (read this week, with tool and window) or ASSUMED, a recommendation, and "what would change my mind". Read the answers separately so one view does not anchor the rest.
5. Critic pass. Where did everyone agree too easily? Which shared assumption is unverified? Whose voice is missing (customer, partner, affiliate)? Drop candidates that move no outcome and protect no cash.
6. Keep three. Rank by outcome impact, then cost of delay, then reversibility.
7. Record each headline number with `excom_record_measurement`. Save the brief with `excom_save_draft` (draft). Propose one task per decision with `excom_propose_task`: owner, due date, evidence.

## Output

The format is in references/brief-template.md: outcomes at a glance, three decisions, carried-over items, red items, and what was not measured.

## Approvals

- Sharing, posting or emailing the brief is a send, and always asks.
- Creating a document in a shared drive is a record write. It asks under the team's autonomy.
- A decision that spends money, changes a price or commits to a term is presented to the owner, never executed.

## Example

Acme's outcome is "N paying customers this quarter". The count is 40 percent behind the straight line. Checkout starts are up and paid conversions are flat. Decision 1: "Approve a checkout fix sprint this week (CTO, due Friday)?" Evidence: checkout sessions expired, read from Stripe for the last 7 days, VERIFIED. What would change it: support tickets showing a price objection instead.

## References

- references/brief-template.md: the exact brief layout and field rules. Read it before drafting. It loads with `excom_skill_load`.

Adapted from alirezarezvani/claude-skills (c-level-advisor/skills/board-meeting/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
