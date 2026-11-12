---
name: cro-follow-up-cadence
description: Plans and drafts the next honest follow-up on every open lead, prospect or partner thread, spaced by behaviour signals and capped per message family, then stops. Use when threads are waiting on the other side, before launching an outreach batch, on the weekly hygiene pass, when a partner goes quiet, or when someone asks "who should we chase" or "did we follow up".
version: 2.0.0
---

# Follow-up cadence without spam

Nobody warm is forgotten and nobody gets the same message twice, because missed follow-ups lose deals and repeated ones burn the mailbox.

## Look up first

- The follow-up cadence per message family: `excom_knowledge_search` "follow-up cadence" or "correspondence templates". If missing, use references/cadence.md and propose it as the team default with `excom_save_draft`.
- The mailbox bound for each purpose (outreach, inbound, partners) from connector settings; if two fit, ask.
- Daily send caps and quiet hours from the team's rules (`excom_recall` "send caps").

## Steps

1. Read open threads: `gmail_search`, `gmail_list_threads`, `gmail_get_thread`, `zoho_email_search`. Ledger status by key with `sheets_read_range`; CRM activities with `odoo_activity_list` or `hubspot_list_deals`.
2. Check signals since the last touch before any nudge: reply, booking (`calendly_list_events`), signup or first use (`melaya_tools`), affiliate or partner signup (`affonso_list_referrals` if your affiliate platform is Affonso). A signal replaces the nudge with a real answer, because behaviour beats fixed delays.
3. Find the family and step for each thread and its due date (references/cadence.md).
4. Suppress when: a human already answered; they said no, unsubscribed or left; a bounce; a pipeline already sent its bump; quiet hours; the day's cap reached; a decision is pending with the owner.
5. Draft in the same thread: shorter than the last mail, one idea restated in a line, a one-word answer asked, the opt-out line. Partner nudges carry news, not repetition. `gmail_create_draft` or `zoho_email_save_draft` (draft).
6. Reserve or update the ledger row by key (`sheets_update_by_header`, record write), then ask for the send (`gmail_send_draft`, `gmail_reply`, `zoho_email_reply`: send class) with the never-twice guards on.
7. After the closing note, mark the row as no reply by key and schedule nothing. Only a new genuine trigger restarts it.
8. Record due, drafted and suppressed counts with `excom_record_measurement`.

## Output

```text
| Thread | Family | Last touch | Signal since | Step | Due | Draft id | Suppressed because |
```

Saved with `excom_save_draft`; a task per due date with `excom_propose_task`.

## Approvals

- Every follow-up, DM or message: send class.
- Ledger and CRM writes under the team's autonomy; deleting rows always asks.
- Arming or changing an outreach pipeline schedule: always asks.

## Example

Acme asked for pricing 11 days ago, got the answer, then silence; no signup since. Family "sales", step 1 due: "One more thing: I can set up the starter template for your support inbox and send you the first output. Interested?" with the opt-out line.

## References

- references/cadence.md: default cadence per family and the suppression list. Read at step 3; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/email-sequence-orchestration/skills/cadence-design/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
