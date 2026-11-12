---
name: cfo-stripe-collections
description: Works failed payments, past-due subscriptions and open invoices in Stripe. It checks each case for a recent payment or dispute, scores payment history, and drafts one tone-matched reminder per customer. Every send waits for approval. Use when running the weekly collections pass, the day a payment fails, before the month close, or when someone asks "who owes us money" or "why did this customer lose access".
version: 2.0.0
---

# Stripe collections and failed payments

Recover revenue already earned. A past-due customer is a paying customer about to drop out of the count, so a prompt, kind reminder matters.

## Look up first

- The reminder tone, the languages and the sending mailbox: `excom_knowledge_search` "communication patterns" or "collections". If missing, draft in plain neutral English and ask the owner which mailbox sends.
- The staff and test exclusion rule: `excom_knowledge_search` "metrics definitions".
- What a payment failure does to access: `excom_knowledge_search` "pricing and plans" (billing facts). Quote it only if the note states it.

## Steps

1. Pull the cases: `stripe_list_events` (invoice.payment_failed since the last pass), `stripe_list_invoices` (open, past due), and `stripe_list_subscriptions` (past_due). If Stripe is not granted, call `excom_request_setup` and stop.
2. Check each customer before drafting:
   - `stripe_get_invoice` for the last attempt and the next retry.
   - `stripe_list_recent_charges` and `stripe_list_customer_subscriptions` for a payment in the last 14 days. If one exists, flag "possibly paid, verify" and draft nothing.
   - `stripe_list_disputes`. A disputed customer gets no reminder; hand the case to the owner.
3. Skip staff and test accounts. Never contact anyone who is not on Stripe's open list.
4. Score the last 6 to 12 invoices: good payer, occasionally late, or repeat late. Note the decline reason when Stripe gives one.
5. Draft one message per customer, consolidating all open items. Match the tone to the score:
   - Good payer: gentle. "Your card was declined, here is how to update it."
   - Occasionally late: clear, with the date access pauses.
   - Repeat late: short and firm.
   Write in plain text, in the customer's language when known, with no internal ids.
6. Save drafts with `gmail_create_draft` or `zoho_email_save_draft` on the sending mailbox (a record write under the team's autonomy). With no mailbox, use `excom_save_draft`.
7. Present the batch: a summary table, then every draft. One approval covers one batch. Any edit or added customer starts a new round.
8. A week after the human sends, re-read with `stripe_get_invoice` and record the amount recovered with `excom_record_measurement`. Repeated declines on one plan go to the revenue role. Checkout or portal bugs go to the COO (`excom_send_handoff`).

## Output

```text
Collections batch, read <time>
| Customer (masked) | Plan | Amount due | Days late | Reason | Score | Tone | Draft |
Possibly paid: list | Excluded (dispute, staff, test): list
Recovered since last pass: amount (tool, window)
```

## Approvals

- Sending any reminder or invoice (`gmail_send_draft`, `stripe_send_invoice`) is a send, and always asks.
- Retrying a charge (`stripe_pay_invoice`), voiding, refunding (`stripe_refund`), cancelling, or adding a coupon is spend or delete, and always asks with the amount.
- Creating a portal session or updating a customer record is a record write, and asks.

## Example

Three failed renewals at Acme. One customer paid yesterday: flagged "possibly paid", no draft. One customer is in dispute: handed to the owner. One good payer with an expired card: gentle draft with the update link, sent after the owner approves.

Adapted from anthropics/knowledge-work-plugins (small-business/skills/invoice-chase/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
