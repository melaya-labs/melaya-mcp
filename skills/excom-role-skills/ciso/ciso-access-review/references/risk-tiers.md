# Access review: default risk tiers and findings

Use these only when the knowledge base has no ranked system inventory. Say in the output that the default tiers were used.

## Tiers

| Tier | Systems | Review depth |
|---|---|---|
| High | Production hosts and edge, source control and the deploy branch, CI and deploy tools, monitoring with write rights, the secret store, application admin accounts, payment and billing admin, mailbox and identity admin | Every entitlement, every review |
| Medium | Shared drives, collaboration and chat tools, connector accounts used by executives and pipelines, analytics with personal data | Every entitlement, or a sample of at least half with all admins |
| Low | Read-only tools, public tools, tools with no customer or personal data | Admins and leavers only |

## Review types

- User review: a manager confirms each person's rights.
- Entitlement review: a system owner confirms everyone holding one right (best for admin roles).
- Privileged review: every admin, key and service account, by the security role with the CTO.
- Separation of duties: nobody both requests and approves their own access, nobody both writes and approves production changes alone.

## Findings to flag

| Finding | Default decision |
|---|---|
| Leaver still holds access | Revoke now (production, asks) |
| Role change kept old rights | Revoke the old rights |
| Admin without MFA | Enforce MFA or remove admin |
| Shared or orphan account | Assign an owner or disable |
| Key or token with no owner or older than the rotation policy | Rotate or revoke |
| Runner or device of a leaver | Revoke the runner |
| Self-approved access | Re-approve by a second person or revoke |
| Mail forwarding to an outside address | Investigate with the phishing and mailbox skill |

## Evidence an auditor expects

- The scope and its date, who reviewed each system, every decision, every revocation with its execution date and verification read, exceptions with owner and expiry, and the next review date.
