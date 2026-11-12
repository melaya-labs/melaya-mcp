---
name: partner-enablement
description: Equips partners to pitch, demo and implement the product correctly (enablement brief, talk track, demo path, objection table, plan guidance) and reinforces partners who are signed but not producing. Use when a partner has received the onboarding kit, when a partner asks how to demo or answer an objection, when a launch changes what partners sell, or for the monthly check on signed partners with no referred signups.
version: 2.0.0
---

# Partner enablement

Signed partners only move the customer goal when they can show one product working for their own clients.

## Look up first

- Products, positioning, the claims policy and the public first-success tutorials: `excom_knowledge_search` "products", "positioning", "claims policy", "getting started".
- Plans for client recommendations: search "pricing and plans".
- The active-affiliate definition: search "metrics definitions"; if missing, propose "at least one referred signup" to the owner.
- Approved answers to common objections: search "answer library" or use cro-inbound-answer-library.

## Steps

1. Segment partners: producing, active but not producing, silent. Read `affonso_get_affiliate_analytics` and `affonso_list_referrals` if Affonso, and partner threads (`zoho_email_search`).
2. Build the enablement brief per partner type with references/enablement-brief.md and save it with `excom_save_draft`.
3. Ask the CMO to review talk tracks and assets for voice, and the CPO to confirm facts on new features (`excom_send_handoff` kind request).
4. Deliver: a short email with the brief and links (`zoho_email_save_draft` or `gmail_create_draft`, draft; the send asks), and offer one enablement call (booking link: send class).
5. Monthly, active but not producing: one useful touch each (a template for their vertical, an answer to an objection their clients raise, a co-marketing idea). At most two touches a month, because more reads as pressure.
6. Silent after 60 days: one honest check-in asking whether they still want to be active, then pause under cro-follow-up-cadence.
7. Send objections and missing features partners hear to the CPO with their words; recurring questions become answer-library entries.
8. Record partners producing with `excom_record_measurement`.

## Output

- The enablement brief per partner type.
- Monthly:

```text
| Partner | Segment | Clicks | Signups | Customers | Last touch | Next reinforcement | Feedback captured |
```

## Approvals

- Every email, invite or message to partners: send class.
- Any incentive, bonus, contest or prize to drive partner activity: spend and an owner decision.
- Publishing enablement material publicly: send class with the CMO.

## Example

Acme Digital (agency) signed 35 days ago: 40 clicks, 0 signups. Their clients ask "will it post without me checking?". Touch: the approvals answer from the library plus a demo path showing an approval step, and one template for social scheduling.

## References

- references/enablement-brief.md: the brief sections and the reinforcement rules. Read at step 2; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/sales-handoff-orchestration/skills/enablement-kit/SKILL.md and plugins/sales-enablement/skills/reinforcement-loop/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
