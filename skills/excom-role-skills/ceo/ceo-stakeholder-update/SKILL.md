---
name: ceo-stakeholder-update
description: Drafts the periodic update for investors, advisors, partners or the team: progress, plans and problems in a few sentences each, outcome status, risks with their state, and one or two specific asks, with every number sourced. Use when the monthly update is due, when an investor or advisor asks about traction, when a milestone lands (first customer, a signed partner, a launch), or when someone says "write the update" or "send a recap".
version: 2.0.0
---

# Investor and stakeholder update

A short update readers absorb in under a minute and trust. Its asks turn readers into help: an introduction, a reseller, an affiliate with an audience.

## Look up first

- The outcomes (in your context) and last period's update: `excom_recall`.
- The audience list and its variants, the cadence, and the approved send path: `excom_knowledge_search` "recap recipients" or "investor update". If missing, ask the owner with `excom_propose_task` (needs_decision). Read recipient lists only. Never edit them.
- Claim rules: `excom_knowledge_search` "brand voice", "programme terms", "partner approvals". Partner names need the partner's written approval.

## Steps

1. Fix the window and the audience: investors and advisors, partners, or the team. Partners never see cash or cost lines.
2. Read the numbers this turn: `stripe_list_subscriptions` and `stripe_list_invoices` (customers, revenue), `affonso_get_affiliate_analytics` (affiliates, if on Affonso), signed partners per the definitions note, and what shipped from the release source you are granted (for example `gitea_list_releases` or `github_list_prs`). Ask the CFO for cash and runway and the CDO for activation with `excom_send_handoff` (kind question). If a source is missing, write "not measured".
3. Draft Progress, Plans and Problems, one to three sentences each, data first.
4. Give each outcome a status (green, amber, red) with the reason.
5. State each risk as resolved, owned (name the owner), accepted (say why) or mitigated (say how).
6. Write at most two asks, specific enough to act on ("introductions to resellers in region X").
7. Check every claim against the knowledge base: programme terms, product claims, partner names. Remove anything unapproved.
8. Save with `excom_save_draft` (draft). The send goes through the approved path, never from the executive directly.

## Output

```text
<Period> update (window <dates>, read <time>)
Headline: one sentence
Outcomes: <outcome> today/target, status, reason
Progress: 1 to 3 sentences
Plans: 1 to 3 sentences
Problems: 1 to 3 sentences
Risks: risk | resolved / owned / accepted / mitigated | owner or reason
Asks: 1 to 2
Sources: tool and window per number (kept in the draft)
```

## Approvals

- Any send, share or post asks. The owner approves the content and the recipient list.
- Naming a partner, customer or case study needs written approval and the owner's go.
- Cash and fundraising figures are confirmed by the owner before they leave the team.

## Example

Headline: "Acme crossed half its customer goal and signed its second reseller." Problems: "Checkout conversion fell after the price change. A fix ships next week." Ask: "Introductions to two agencies that resell analytics tools."

Adapted from anthropics/skills (skills/internal-comms/SKILL.md, examples/3p-updates.md) and anthropics/knowledge-work-plugins (product-management/skills/stakeholder-update/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
