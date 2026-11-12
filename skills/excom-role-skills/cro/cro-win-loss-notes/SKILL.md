---
name: cro-win-loss-notes
description: Captures a short tagged note for every won, lost or no-decision outcome (deals, trials, partner talks), keeping the buyer's own words apart from the team's beliefs, and finds repeating reasons monthly. Use when a deal or trial closes, when a partner signs or declines, when someone claims "we always lose on price", or when asked "why are we winning or losing".
version: 2.0.0
---

# Win-loss notes

Tells the truth about why outcomes happen, from buyer evidence, because early outcomes decide what to fix before the next hundred.

## Look up first

- Competitors and positioning: `excom_knowledge_search` "competition", "positioning".
- The tag taxonomy if the team has one: search "win-loss taxonomy"; else use references/taxonomy.md and propose it with `excom_save_draft`.
- Where win-loss rows are kept (sheet or CRM field): search "win-loss log"; if none, propose a sheet to the owner with `excom_propose_task`.

## Steps

1. Collect evidence: `gmail_get_thread` or `zoho_email_get_content`; CRM with `hubspot_get_deal` or `odoo_crm_lead_list`; billing with `stripe_get_subscription` or `stripe_list_checkout_sessions`; usage through `melaya_tools`. Partners: `docusign_get_envelope_status` and the affiliate record (`affonso_get_affiliate` if your platform is Affonso).
2. Normalise the outcome: won, lost to a named alternative, no decision, trial churn. "Lost" where they chose nothing is no decision.
3. Keep two columns, never merged: what the buyer said (quote or labelled paraphrase, dated) and what the team believed. Only a belief means the reason is unknown.
4. Tag with the taxonomy, keeping the buyer's specific mechanism.
5. Save the note with `excom_save_draft` and append it by key (`sheets_append_row`, record write).
6. If the outcome matters and no buyer reason exists, draft one short honest question ("What made you decide?"). Draft class; the send asks. One per outcome.
7. Monthly: count each tag as "N of M outcomes with buyer evidence", attach exceptions, state sample size and bias. One outcome is one observation, never a pattern. Segment only with three or more outcomes per bucket.
8. Route hypotheses with evidence: product gaps to the CPO, activation blockers to the CXO, message to the CMO, price or plan shape to the CFO and owner (`excom_send_handoff` kind request).
9. Record the month's win rate with `excom_record_measurement`.

## Output

```text
Outcome: <won | lost to X | no decision | trial churn> on <date>
Account: <company or segment> | Product: <one> | Source: <direct | affiliate | partner>
Buyer said: "<quote>" (<channel, date>) or "no buyer evidence"
We believed: <line> | Tags: <tags>
What would have changed it: <line> | Follow-up owner: <role>
```

Monthly: tag counts with exceptions and confidence, then hypotheses (finding, test, owner).

## Approvals

- Questions to buyers or partners: send class.
- Sheet and CRM writes under the team's autonomy.
- Publishing a customer quote: the customer's written approval and the CMO, never from this skill.

## Example

Acme Retail churned after trial. Buyer said: "We couldn't get it connected to our store in the first week." Team believed: price. Tags: setup or activation, not price. Routed to the CXO with the thread.

## References

- references/taxonomy.md: default outcome tags and counting rules. Read at step 4; loads with `excom_skill_load` (section) or by paging.

Adapted from LMTYdotcom/skills (skills/competitive-win-loss-analysis/SKILL.md), MIT licence, and gtmagents/gtm-agents (plugins/competitive-intelligence/skills/win-loss-dataset/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
