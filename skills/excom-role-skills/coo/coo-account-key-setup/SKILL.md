---
name: coo-account-key-setup
description: Opens a provider account and connects it end to end on the owner's computer, following the account playbook. The flow is plan, profile, generated password, signup, email verification, test and live keys, then saving and a test read. Secrets are kept by handle only, and CAPTCHAs, payments and ID checks go to a human. Use when asked to "create an account", "get API keys", or "connect <provider>", or when a colleague's setup request names a service with no account yet.
version: 2.0.0
---

# Account and API key setup

A new analytics, payment or partner tool becomes usable by the team the same day. Secret values are never seen by the executive, and never appear in tasks or reports.

## Look up first

- Computer control is on for you: `computer_status`. If it is off, hand the steps to the owner with `excom_request_setup` and stop.
- The signup identity and email: `excom_identity`. You also need a mailbox for that address assigned to you.
- The provider's existing profile: `excom_account_profile` (get). The provider's official domain, the keys needed (test, live, publishable, webhook secret), and where each goes: ask the requester if any of these is unclear.

## Steps

1. Plan. Claim or propose one task, "Create the <provider> account" (`excom_propose_task`), covering the plan (free unless a human chose one), the keys needed and their destinations.
2. Profile. Run `excom_account_profile` (set): provider, login email, sign-in method, URL, status in progress.
3. Password. Run `excom_secret_generate` with the label "<provider> password", then `excom_secret_save` to the profile's password slot.
4. Sign up. Open the official domain only with `computer_open_url`, and check the address bar. Read the page with `computer_screen`. Type names and email with `computer_type`. Type every password field by handle with the secret-typing tool, never as text. Accept only the standard terms of a free or test plan.
5. Never bypass. For a CAPTCHA, bot check, phone or ID verification, or payment form, use `computer_handoff` with one sentence saying what the human must do, then `computer_screen` and continue.
6. Verify the email. Search the mailbox for the provider's newest message, waiting with `computer_wait` between searches, for up to five minutes.
   - A code: `excom_secret_capture` (source text), then type it by handle.
   - A link: `computer_open_url`, on the provider's domain only.
   Set the profile status to verified.
7. Keys. Open the API keys page, test mode first. Never screenshot a key. Capture it with `excom_secret_capture`, from the screen element or by clicking Copy and capturing from the clipboard. Label it, for example "<provider> test secret key". Live keys that need business, bank or ID details are a human step: say so in the task.
8. Save. Run `excom_secret_save` for each key to the profile, to the Melaya connector (account label "Test" or "Live"; make live the default only if the owner asked), and to the password manager if one is assigned.
9. Check. If the connector is assigned to you, run one read on the Test account.
10. Report in the task (`excom_update_task`): provider, login and sign-in method, each secret by label, handle and fingerprint (never a value), where each copy is stored, what a human still has to do, and what failed. Set the profile status to created. Stop at once on `computer_stop`, a human's stop, or anything unexpected on screen, and say what you saw.

## Output

```text
Account: <provider> | login <email> | sign-in <method> | profile <status>
Secrets (handles only): label | handle | fingerprint | saved to
Connector: service | account label | read check result
Human steps left: live activation, billing, 2FA backup, ID check | Failures
```

## Approvals

- Paid plans, cards, bank accounts, ID or business verification are human steps, never done by the executive.
- Revealing a secret (`excom_secret_reveal`) always asks, and is almost never needed.
- Making a live key the default, accepting non-standard terms, or connecting production billing is the owner's decision.

## Example

Asked to connect a product analytics tool, you open its official site, sign up with the team's ops address, and type the password by handle. A CAPTCHA appears: you hand it off and the owner solves it. You verify by code, capture the project API key, save it to the connector as "Test", and run one read. The report lists the handles and says that billing remains for a human.
