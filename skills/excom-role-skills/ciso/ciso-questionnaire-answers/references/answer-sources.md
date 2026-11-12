# Questionnaire answer sources and traps

Search the knowledge base for the note type in the middle column. Cite the note title and its updated date in the answer row.

## Question families

| Question family | Note to search for | Typical evidence |
|---|---|---|
| Encryption in transit | TLS baseline or edge configuration note | Minimum TLS version, HSTS, certificate management |
| Encryption at rest | Disk or database encryption note | What is encrypted, key management, who holds keys |
| Access control and MFA | Access provisioning procedure, last access review | Two-person approval, MFA enforcement, review dates |
| Incident response | Incident response runbook, last drill or post-mortem | Severity levels, roles, notice timelines, drill dates |
| Business continuity and recovery | Recovery objectives note, continuity plan, restore test log | RTO and RPO values, last restore test result |
| Vulnerability management | Patching policy, weekly vulnerability brief | Scan cadence, fix deadlines, last scan date |
| Vendors and subprocessors | Subprocessor list, vendor review records | Named subprocessors, transfer safeguards |
| Data protection and privacy | Privacy policy, DPA template, records of processing | Lawful basis, retention, data subject requests |
| Secure development | Release security gate, code review rules | Secret scanning, dependency checks, approvals before production |
| Responsible disclosure | Disclosure policy, security.txt | Contact, response times, safe harbour |
| Compliance frameworks | Control mapping note, compliance platform readiness | Criteria in scope, what is operating, no report claims |
| Logging and monitoring | Monitoring and alerting notes | Retention, alerting, audit log integrity |

## Answer types

- Yes: a dated record exists and you read it this turn.
- Partial: something exists but not all of what was asked (for example a policy without a drill).
- No: nothing exists. Add the roadmap date only if one is written.
- Needs owner: legal, commercial or hosting facts you cannot verify.

## Overclaim traps

- "SOC 2 compliant" or "ISO certified" without an issued report or certificate.
- "Penetration tested" when only automated scans ran.
- "24/7 monitoring" when alerts page nobody at night.
- "All data encrypted" when only some stores are.
- "No subprocessors" when model, hosting or mail providers process customer data.
- A product capability stated beyond its real platform or limits.
- Customer names or logos as references without written approval.

## Never in an external answer

Secrets, internal hostnames, IP addresses, internal ids, personal contact details of staff, draft roadmap items presented as done.
