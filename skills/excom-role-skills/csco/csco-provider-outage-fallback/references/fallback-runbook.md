# Fallback table and supplier runbook

## Fallback table (fill from the continuity plan)
| Supplier type | Detection | Typical fallback | Owner |
|---|---|---|---|
| Model provider | key errors, run failures, provider status | route affected pipelines to a second configured provider; customer-selected providers are the customer's switch | CTO |
| Compute host | edge 5xx, health checks, log stream goes silent | rebuild from the latest backup on a replacement host; check the backup is off the failed host | CTO |
| Edge or DNS | edge errors, certificate failures | origin ingress with in-process rate limiting for a short window | CTO |
| Payments | webhook failures, status page | existing subscriptions keep working; new checkouts show a clear error | CFO, CTO |
| Mail lanes | bounces, send failures | hold broadcast mail; keep security mail on the transactional lane | COO |
| Logs and metrics | ingestion errors | keep logs on host; re-ship later | CTO |
| Secrets vault | secret fetch errors | refuse new credential writes; documented fallback path | CTO, CISO |

## Runbook per critical supplier
Owner | frequency (on incident, quarterly review)
Purpose: what this fallback protects.
Prerequisites: second provider configured, backup verified, access needed.
Procedure: numbered steps, each with expected result and what to do if it fails.
Verification: how to confirm customers are served again.
Rollback: how to return to the primary supplier.
Escalation: who, how, when.
History: date, who ran it, notes.

## After-incident questions
- Did detection come from our signals or from a customer?
- Did the fallback work as written? What step was missing?
- Is the single point of failure still there? What would remove it, and at what cost?
