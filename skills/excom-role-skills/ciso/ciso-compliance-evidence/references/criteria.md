# SOC 2 criteria and typical evidence

General framework knowledge. Your own mapping in the knowledge base wins where it differs.

## Security (Common Criteria, always in scope)

| Criterion | Domain | Typical operating evidence |
|---|---|---|
| CC1 | Control environment | Signed policies, org chart, role descriptions, code of conduct acknowledgements |
| CC2 | Communication and information | Security page, internal policy announcements, customer notices |
| CC3 | Risk assessment | Risk register reviews with dates and treatment decisions |
| CC4 | Monitoring | Quarterly control reviews, internal audit notes, corrective actions |
| CC5 | Control activities | Policies mapped to technical controls, exceptions log |
| CC6 | Logical and physical access | Access reviews, provisioning and offboarding tickets, MFA reports, key rotation records |
| CC7 | System operations | Vulnerability briefs, scanner logs, alerting, incident tickets and post-mortems |
| CC8 | Change management | Approval cards or reviews per change, deploy records, emergency change log |
| CC9 | Risk mitigation | Vendor reviews, contracts with security terms, insurance |

## Optional criteria

| Criterion | Select when | Typical evidence |
|---|---|---|
| Availability (A1) | Customers depend on uptime or you sign SLAs | Capacity reviews, backup jobs, restore tests, disaster recovery drills with measured recovery times |
| Confidentiality (C1) | You hold contractually confidential data | Data classification, encryption settings, deletion records |
| Processing integrity (PI1) | Outputs must be complete and accurate (payments, reports) | Input validation, reconciliation records, error handling reviews |
| Privacy (P1 to P8) | You process personal data for customers | Privacy notice, consent records, data subject request log |

## Type I versus Type II

| | Type I | Type II |
|---|---|---|
| Tests | Design at one date | Design and operation over a period |
| Period | A single date | Usually 3 to 12 months, often 6 |
| Evidence | Descriptions, policies | Descriptions plus records across the whole period |

Rules: operating evidence must cover the whole observation period for each control; a control that started mid-period is a gap for the earlier part.

## Common mistakes

- Counting a written policy as an operating control.
- Linking evidence that contains secrets, personal data or customer material.
- Claiming "SOC 2 compliant" without an issued report; say "controls mapped to SOC 2 criteria".
- Letting evidence expire between audits; track expiry dates monthly.
- Treating an empty connector list as proof that nothing exists.
