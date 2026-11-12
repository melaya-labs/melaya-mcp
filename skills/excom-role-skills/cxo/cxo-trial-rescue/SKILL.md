---
name: cxo-trial-rescue
description: Finds users who signed up and stalled before first success or went silent, diagnoses why from their own setup and runs, and drafts at most three short rescue messages that each offer a concrete fix, then stops. Use when recent signups have not reached value, when a user's first runs failed and they left, when a trial nears its end with nothing achieved, or when someone asks "how do we save these trials".
version: 2.0.0
---

# Trial rescue for stalled users

Most stalls are setup problems, so a precise fix sent at the right moment converts better than any discount, and silence after three tries protects the relationship.

## Look up first

- Who counts as a user and the funnel rungs: `excom_knowledge_search` "metrics definitions". Missing: ask the CDO.
- Activation-help email template and follow-up cadence: search "activation help template", "follow-up cadence".
- Known blockers and their fixes: search "troubleshooting", "known issues".
- Free-tier limits: search "pricing and plans".

## Steps

1. Build the cohort: recent signups who did not reach "got value", with `posthog_compute_funnel` or `posthog_get_cohort` when granted, else ask the CDO (`excom_send_handoff` kind question). Exclude staff, test, comped and duplicate accounts.
2. Diagnose each user from facts (setup status, failed runs and error codes, product chosen) through `melaya_tools`, using references/rescue-messages.md. Never guess a cause.
3. Check prior contact: `gmail_search` or `zoho_email_search`; `excom_read_tasks` for open CRO or CXO tasks. One rescue sequence per user unless a new trigger appears.
4. Draft message 1, value first: what happened in their account, the fix, one doc link, "Reply yes and I'll send the exact steps." Under 90 words, plain text, their language, support-engineer tone, no price. `gmail_create_draft` or `zoho_email_save_draft` (draft) and `excom_save_draft`.
5. Message 2 about a week later, only if no reply and no progress: a new angle in one sentence or a template for their goal.
6. Message 3 about a week after that: an honest close, then stop and mark the user closed.
7. Before each send, recheck progress; cancel if they succeeded. Sends wait for approval and respect quiet hours.
8. Users who reply get the steps the same day. Record users rescued (reached value within 14 days of message 1) with `excom_record_measurement`.

## Output

```text
| User | Product | Cause (evidence) | Msg 1 | Msg 2 | Close | Progress since | Status |
Cohort size | causes ranked | rescued count and rate
```

## Approvals

- Every message to a user: send class.
- Trial extensions, credits, discounts or plan changes: the owner or CFO, never offered here.
- Product or docs changes to remove a blocker: hand to the CPO.

## Example

Acme Consulting verified 5 days ago, ran 3 pipelines on a free router model, all "agent could not use tools". Message 1: "Your agents ran on a model that can't call tools, so they couldn't act. Pick a tool-capable model or connect your own key; it takes a minute. Reply yes for the steps."

## References

- references/rescue-messages.md: cause table and message patterns. Read at steps 2 and 4; loads with `excom_skill_load` (section) or by paging.

Adapted from stephenrogan/csm-skills (skills/re-engagement-email-writer/SKILL.md), MIT licence. Modified: rewritten generic for EXCOM.
