---
name: cxo-onboarding-emails
description: Designs a short, behaviour-triggered onboarding email sequence per product for new users and new paying customers, each email with one goal and a suppression rule, and hands it to the CMO for sending. Use when a product has no onboarding emails, when activation drops, when a new paying customer arrives, when a key step or screen changed, or when someone asks "what do new users receive".
version: 2.0.0
---

# Onboarding email sequence

Time to value decides whether a signup pays, so each email moves the user one step toward first success and stops the moment they get there.

## Look up first

- Each product's activation path and milestone: cxo-activation-paths, or `excom_knowledge_search` "getting started".
- Funnel data per step and the activation definition: search "metrics definitions"; else ask the CDO (`excom_send_handoff` kind question).
- How broadcasts are sent and who owns them: search "email campaign runbook". Missing: hand the drafts to the CMO and ask.
- Brand voice and supported languages: search "brand voice".
- Plans, only for the paying-customer welcome: search "pricing and plans".

## Steps

1. Define activation for the product as one action that predicts return, and the time it should take (from the tutorial).
2. Find the step with the largest loss: `posthog_compute_funnel` or `ga4_run_funnel_report` when granted, else the CDO.
3. Design at most five emails with references/sequence-template.md: each has one goal, one link, a behaviour trigger and a suppression rule, because a mail about a step already done teaches users to ignore you.
4. Paying customers: a welcome naming their plan's limits and support level, and a check on first success a week later.
5. Write each email: subject naming the outcome, three to six lines, the step, one doc link, plain text, the user's language and register. No prices except in the paying-customer welcome.
6. Align with in-app guidance so both point to the same next step. Caps: one onboarding email a day, three a week, none while a rescue or upgrade message is active for the user (check `excom_read_tasks`).
7. Save drafts with `excom_save_draft` and hand the set to the CMO, who owns broadcasts (`excom_send_handoff` kind request). The CLO checks consent and opt-out.
8. After two weeks live, read activation by email received and unsubscribes; propose one change. Record activation within 7 days with `excom_record_measurement`.

## Output

```text
Product: <one> | Activation: <action> within <time>
Email n: trigger <event> | goal <one> | subject | body | link | suppress when <event>
Caps: 1 a day, 3 a week, paused during rescue or upgrade messages
Measure: activation within 7 days by email received
```

## Approvals

- Launching or sending any email or campaign: send class; the real send is confirmed by a human.
- Template deploys or renderer code: production, CTO.
- Promotions or discounts in onboarding: the owner decides.

## Example

Workflow builder, activation = one successful run within 2 days. Biggest loss: verified but no model connected. Email 2 "Connect a model in one minute" triggers 1 day after verification without a key; suppressed once a key exists.

## References

- references/sequence-template.md: the default five-email sequence and writing rules. Read at step 3; loads with `excom_skill_load` (section) or by paging.

Adapted from coreyhaines31/marketingskills (skills/onboarding/SKILL.md), MIT licence. Modified: rewritten generic for EXCOM.
