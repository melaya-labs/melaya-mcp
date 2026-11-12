---
name: partner-co-marketing
description: Plans, gets approved and measures a joint action with a partner (announcement, partner page, joint post, newsletter mention, template, listing), with the CMO owning voice and channels and the partner approving every claim. Use when planning a partner's first co-marketing action, when a partner proposes a joint campaign or launch, when a partner page or announcement is due, or for the monthly co-marketing review.
version: 2.0.0
---

# Co-marketing with partners and the CMO

One honest joint action per partner is the first public proof that a partnership is real and the main way partners bring customers.

## Look up first

- The relationship status and claim record for this partner: `excom_knowledge_search` "<partner> partnership" and "claim ledger". If no claim record exists, draft one from the signed agreement and threads with `excom_save_draft` before any copy.
- The partner launch runbook and the announcement post runbook: search "partner launch runbook", "announcement blog post runbook".
- Brand voice, channels and audiences: search "brand voice", "channels and audiences".

## Steps

1. Write the brief: goal (signups, partner-sourced customers), audience, action type, the one product featured, assets, the claim records it relies on, date. Save with `excom_save_draft`.
2. Check claim truth before copy: each statement is live, signed, being signed, jointly planned or proposed, and worded that way. Nothing public before the partner's written approval is recorded, because an overstated relationship is the most common partner mistake.
3. Hand the brief to the CMO (`excom_send_handoff` kind request): the CMO owns copy, voice and channels; the CLO reviews relationship wording when a page or agreement claim is involved.
4. Pick the action with references/actions.md.
5. Approvals: the owner approves every public send, the partner approver is named in writing, the CMO signs off copy. Send the review package from the partner mailbox (`zoho_email_save_draft` or `gmail_create_draft`, draft; the send asks). Review links stay inside the thread.
6. Launch on one agreed date and hour, each side in its own voice. Partner launch-day replies within the hour (drafted, approved).
7. Measure at 7 and 30 days: clicks, signups and customers from the partner link (`affonso_get_affiliate_analytics`, `affonso_list_referrals` if Affonso), site traffic from the UTM (`ga4_run_report` when granted, else ask the CMO). Record with `excom_record_measurement`.
8. Close out: a short retro, the "all live" note to the partner with every link, and the next action if this one produced signups.

## Output

```text
Partner: <company> | Relationship status: <one exact sentence>
Action: <type> | Product featured: <one> | Date and hour: <with timezone>
Claims used: <claim records> | Partner approver: <role> | CMO sign-off: <date>
Tracking: <link and UTM> | Day 7: clicks, signups | Day 30: signups, customers
Next action: <proposal or none>
```

## Approvals

- Every public post, page, article, newsletter or email: send or production, after written partner approval.
- Paid placements, sponsored newsletters, marketing development funds, event fees, ads: spend, never default, ask with the cost.
- Co-selling commitments, exclusivity or revenue terms: the owner only.

## Example

Acme CRM (technology partner, integration live). Action: joint post plus a partner page. Claim: "integration is live" (code and partner confirmation on file). Day 30: 140 clicks, 22 signups, 2 customers; next: a joint template for their users.

## References

- references/actions.md: action types, who does what, and when each fits. Read at step 4; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/partnership-development/skills/co-marketing-governance/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
