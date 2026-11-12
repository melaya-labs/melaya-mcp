---
name: partner-programme-offer
description: Recruits integrators, agencies, resellers and communities into the company's partner or affiliate programme and makes the offer using only the standing tiers the owner approved, routing every other ask to the owner. Use when a qualified partner is ready to hear terms, when a partner asks "what do I earn" or "can my clients get a discount", when someone wants to switch tier, or when a custom deal is requested.
version: 2.0.0
---

# Integrator and agency programme offer

Standing, pre-approved terms let partners say yes without a negotiation per partner, which is what makes a partner goal reachable.

## Look up first

- The programme terms the owner approved (tiers, commission, audience benefit, attribution window, approval period, payout rules, exclusions, switch rules, legacy mechanisms never to offer): `excom_knowledge_search` "partner programme terms" or "affiliate programme terms". If none are recorded, offer nothing and ask the owner with `excom_propose_task` (needs decision true).
- The partner goal in the team's outcomes (in context).
- Proposal and materials templates: search "partner proposal template", "integrator materials".

## Steps

1. Read the live programme so the offer matches reality. If your affiliate platform is Affonso: `affonso_get_program`, `affonso_get_payment_terms`, `affonso_list_groups`. Missing app: `excom_request_setup`. If live settings disagree with the knowledge note, stop and ask the CFO (`excom_send_handoff` kind question).
2. Match behaviour to tier with references/tier-matching.md, because the right tier is the one that rewards customers who stay.
3. State the common terms exactly as recorded, including exclusions. Never mention a mechanism the note marks as legacy.
4. Explain tier switching as recorded (cooldowns and locks), so nobody is surprised later.
5. Draft the offer from the proposal template: what the company does in one line, the product that fits their clients, what is already integrated, the tier and why, what they get after joining (tracking link, dashboard, brand kit), the next step. Plain text, from the partner mailbox bound in connector settings (`zoho_email_save_draft` or `gmail_create_draft`, draft) and `excom_save_draft`.
6. Anything outside the standing tiers (higher rate, custom revenue share, exclusivity, territory, co-selling commitments, white label, minimums, paid marketing funds, payment terms) goes to the owner with the ask, the evidence and a default: `excom_send_handoff` kind request to the CEO. Never hint that better terms exist.
7. On yes: create or invite them on the chosen tier (`affonso_create_affiliate`, or the self-serve join with `affonso_create_embed_token`; record write), then start partner-onboarding-kit.
8. Record offers made and accepted with `excom_record_measurement`.

## Output

```text
Partner: <company> | Type: <integrator | agency | reseller | community>
Clients and channel: <line>
Tier offered: <tier name from the terms note> because <line>
Terms stated: <attribution, approval, payout, exclusions as recorded>
Off-tier asks: <none | sent to owner on date> | Draft: <id> | Next step: <dated>
```

## Approvals

- Sending the offer or any reply: send class.
- Creating or changing the partner record: record write; any commission, coupon, group incentive or payout change: spend, always asks.
- Any term outside the standing tiers: the owner only.

## Example

Acme Automation, an implementation agency with 30 SMB clients, keeps the client relationship. Tier: the default implementer tier from the terms note, because their clients stay long and need no launch discount. Next step: "Join today; we'll pick your first client use case on Thursday's call."

## References

- references/tier-matching.md: how to map partner behaviour to a tier and the questions to ask first. Read at step 2; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/referral-program-orchestration/skills/incentive-design/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
