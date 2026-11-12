---
name: partner-onboarding-kit
description: Takes a newly signed or joined partner from signature to a first live action within the team's onboarding window: onboarding kit sent, tracking link tested, first co-marketing action scheduled, each step tracked. Use when an agreement is filed or a partner joins the programme, on the daily check of partners still in onboarding, or when a partner says "where do I start".
version: 2.0.0
---

# Partner onboarding kit

A partner who does nothing in the first weeks rarely brings a customer, so every new partner gets the kit, a working link and one first action fast.

## Look up first

- The onboarding window and what it must contain (kit, tracking link, first co-marketing action): `excom_knowledge_search` "partner onboarding". If missing, use 14 days and these three milestones, and propose it with `excom_save_draft`.
- Kit sources: search "brand kit", "integrator materials", "partner decks", "claims policy", "programme terms".
- Whether the partner is signed: the team's signed-partner definition (agreement filed in the partner's folder under the agreements folder); search "partner agreements folder".

## Steps

1. Day 0: confirm the start. Signed: the agreement is filed (`drive_search` in the partner's folder). Joined: the affiliate record and tier (`affonso_get_affiliate` if your platform is Affonso). Create one task per milestone with due dates (`excom_propose_task`).
2. Days 0 to 2, tracking: read the partner's links (`affonso_list_promotion_urls`); create a specific promotion URL only if needed (`affonso_create_promotion_url`, record write). Ask the partner to click once; confirm the click next day with `affonso_get_affiliate_analytics`, because an untested link silently loses attribution.
3. Days 0 to 3, the kit (references/kit-contents.md): draft with `excom_save_draft`; the send asks.
4. Days 3 to 10, first co-marketing action, chosen with the CMO through partner-co-marketing: a partner page or announcement (the partner launch runbook in knowledge), a joint post, a newsletter mention, a listing, or a joint template.
5. Day 7, check-in: did they open the dashboard, share the link, ask anything? Draft one short note with one concrete idea for their audience (draft).
6. End of window: kit sent, link clicked, first action live or dated. Escalate gaps to the CRO or CMO with `excom_send_handoff` kind request.
7. Hand qualified customer leads the partner brings to the CRO; commission questions to the CFO.
8. Record days to first action and partners active within the window with `excom_record_measurement`.

## Output

```text
| Partner | Signed or joined on | Tier | Link tested | Kit sent | First action (type, date) | Day 7 check-in | End-of-window status | Blocker and owner |
```

Saved with `excom_save_draft`.

## Approvals

- Sending the kit, check-ins or any partner email: send class.
- Affiliate record changes and promotion URLs: record write; commission, coupon or group changes: spend, always asks.
- Publishing a partner page, post or listing: send or production, after the partner's written approval.

## Example

Acme Agency signed on day 0. Day 1 link clicked once, confirmed. Day 2 kit sent. Day 6 joint post scheduled with the CMO for day 9. Day 14 status: active, first action live, 3 clicks, 1 signup.

## References

- references/kit-contents.md: what goes in the kit and the claim rules. Read at step 3; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/referral-program-orchestration/skills/partner-ops/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
