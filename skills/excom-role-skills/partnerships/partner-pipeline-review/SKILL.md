---
name: partner-pipeline-review
description: Counts partners by stage against the team's partner goal and milestones, counting as signed only partners whose signed agreement is filed in their Drive folder, separates partner-sourced from partner-influenced revenue, and lists stalled partners and owner decisions. Use when it is time for the weekly partner review, before a CEO or board review, when the signed count falls behind a milestone, or when someone asks "how many partners have we signed".
version: 2.0.0
---

# Partner pipeline review against the goal

One weekly view of the partner channel that counts only what is proven, because a verbal yes is not a signed partner and double-counted revenue misleads every decision.

## Look up first

- The partner goal, deadline and milestones in the team's outcomes (in context). No milestones: propose a straight line and ask the owner (`excom_propose_task`, needs decision true).
- The signed-partner definition: the signed agreement is filed in that partner's folder under the partner agreements folder. Read the folder id: `excom_knowledge_search` "partner agreements folder". Missing: ask the owner.
- The active-affiliate definition from the metrics note (search "metrics definitions"). If it lacks one, propose "an active affiliate has generated at least one referred signup" to the owner.
- Last week's numbers: `excom_recall` "partner review".

## Steps

1. Read: ledger rows (`sheets_read_range`); threads waiting on the team in the partner mailbox (`zoho_email_search`); partner calls booked (`calendly_list_events`); envelopes (`docusign_list_envelopes`, `docusign_get_envelope_status`); partners and results (`affonso_list_affiliates`, `affonso_get_affiliate_analytics`, `affonso_list_referrals`, `affonso_list_commissions` if Affonso).
2. Verify signed: for each partner with a completed envelope, `drive_search` with folder id = the agreements folder and name = the partner, then inside that folder. Count as signed only when the agreement file is there. Completed but not filed: run the filing steps of partner-agreement-docusign.
3. Stage every partner with references/stages.md.
4. Compare with the milestones and the weekly call target. Compute the gap and what it needs upstream at observed conversion rates, with sample sizes.
5. Revenue desk: classify partner-linked customers as sourced (came through their tracking link), influenced or co-sell. Only sourced earns commission; influenced is reported, never paid without an owner decision. Disputes and double counting to the CFO (`excom_send_handoff` kind question).
6. Stalled partners (no movement for 10 working days): a next step under cro-follow-up-cadence, or a close.
7. Hand partner-brought customer leads to the CRO; commissions due to the CFO.
8. Write the decision list for the owner and CEO: off-tier asks, agreements waiting to be sent, disputes, strategic partners.
9. Record signed (filed), active and calls booked with `excom_record_measurement`, and the week with `excom_record_fact`.

## Output

```text
Day <n> of <goal period> | Signed (filed): <n> (milestone today <n>) | Active: <n> | Producing: <n>
Calls booked this week: <n> of <target>
Funnel: sourced, contacted, call, offer, agreement out, completed not filed, signed
Gap to next milestone and what it needs (rates, sample sizes)
Partner-sourced customers | Influenced | Disputes | Stalled with next step | Decisions (each with a default)
```

## Approvals

- Messages to partners: send class; sending agreements: the owner.
- Ledger and CRM stage changes, filing agreements: record write under the team's autonomy.
- Commission, conversion, refund or payout actions: spend, always asks, prepared with the CFO.

## Example

Goal N partners by day 90, day 45. Completed envelopes 9, filed 8 (Acme Labs not filed: filed today, now 9). Milestone today 9: on track. Calls this week 11 of target 15: sourcing list needs 30 more names.

## References

- references/stages.md: stage exit criteria and the sourced versus influenced rules. Read at step 3; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/partnership-development/skills/partner-revenue-desk/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
