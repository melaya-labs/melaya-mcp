# Vendor tiers, evidence and cadence

Default model when the knowledge base has no vendor risk policy. Say in the review that the default was used.

## Tiers

| Tier | Inherent risk | Examples |
|---|---|---|
| Critical | Production access or customer data at scale; an outage stops the service | Hosting, database, identity, payment processor, primary model provider |
| High | Personal data, a connector with write scope, or customer content in some flows | Mail delivery, analytics with user ids, transcription, CRM |
| Moderate | Internal data only, no customer content | Project tools, internal docs, design tools |
| Low | No data and no access | Stock media, public reference tools |

## Evidence by tier

| Tier | Ask for | Read carefully |
|---|---|---|
| Critical | SOC 2 Type II or ISO 27001, recent pentest summary, incident response description, subprocessor list, full questionnaire (SIG or CAIQ) | Exceptions, audit period, scope, carve-outs, open highs |
| High | SOC 2 or ISO attestation, short questionnaire (SIG Lite or CAIQ), subprocessor list | Exceptions and scope |
| Moderate | Security page, short self-attestation | Data location, deletion on exit |
| Low | None beyond the profile | |

## Reassessment

| Tier | Cadence | Also re-review when |
|---|---|---|
| Critical | Every year | Breach, acquisition, region change, new subprocessors, scope change |
| High | Every year | Same triggers |
| Moderate | Every two years | Breach or data scope change |
| Low | On change only | Starts handling data |

## Contract terms to request

- Breach notice window in hours, with the contact path.
- Data return or certified destruction at exit.
- Audit or evidence rights (report sharing at minimum).
- Subprocessor flow-down and change notice.
- Transfer safeguards for data leaving the region.
- Security obligations matched to the tier.

## Concentration and fourth parties

Note when several vendors depend on the same upstream provider; one outage or breach can hit all of them. Record the critical fourth parties of Critical vendors.

## Offboarding a vendor

Revoke access and tokens, remove integrations and keys, confirm data return or destruction in writing, update the subprocessor list and the inventory.
