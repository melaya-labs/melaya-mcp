# Analysis pitfalls

| Pitfall | What goes wrong | Detect | Prevent |
|---|---|---|---|
| Join explosion | A many-to-many join multiplies rows: a customer with several subscriptions or products counted several times | Row count after the join exceeds distinct ids | Count distinct ids; aggregate before joining |
| Survivorship | Churned, deleted or failed entities are left out, so rates look better | Ask "who is not in this dataset?" | Include churned and deleted rows in denominators |
| Incomplete period | A partial week or month is compared with a full one | The window ends today or mid-period | Compare complete periods, or the same number of days |
| Denominator shift | The base changed between periods (new exclusion, new product, new definition) | Definitions differ across periods | Recompute both periods on one definition, and note the change |
| Average of averages | Rates averaged across groups of very different size | Groups of unequal size | Aggregate from raw counts |
| Time zones | Systems count days in different zones (billing often UTC, ad platforms in the account's zone, reports in the team's zone) | Daily totals that do not match across tools | Align on one zone and state it |
| Retention bound | Raw events kept for a limited time cannot rebuild long windows | Window longer than event retention | State the bound; use milestone tables that outlive raw events |
| Selection bias | Segments defined by the outcome being measured | Segment rule mentions the result | Define segments before looking at outcomes |
| Cohort vs all users | A cohort count read as the whole user base | Label missing on the number | Always label: registered in window, or all users |
| Vendor counter as fact | Ad-platform or newsletter numbers presented as registrations | Source is a vendor | First-party for registrations, activation, purchases |
| Logging spike | A jump right after a release | Change aligned with a deploy | Check duplicates, bots and event names first |

## Pre-delivery checklist

- [ ] Population, cohort, window and time zone stated for every number
- [ ] Definitions match the definitions note, or differences are stated
- [ ] At least two figures re-read at the source this turn
- [ ] No pitfall from the table is left unchecked
- [ ] Totals reconcile across breakdowns
- [ ] Changes over 30 percent have a named cause
- [ ] Caveats written for readers
