# Cleaning rules, anomaly checks, savings levers

## Cleaning (before any analysis)
1. Normalise supplier names (strip legal suffixes, merge obvious variants of one supplier).
2. Convert currencies to the reporting currency and flag the rates used.
3. Keep credits and refunds; report gross and net if material.
4. Flag possible duplicate invoices (same supplier, date, amount); never remove them silently.
5. Keep VAT-inclusive and VAT-exclusive views apart.
6. Separate one-off purchases from recurring spend.
7. Separate expense reimbursements and internal recharges from supplier spend.
8. State which period and basis (invoice date or usage date) you used.

## Anomaly checks
- Month-on-month jump above 25 percent on any supplier.
- A new supplier with no approved spend request.
- Spend on a tool unused in 90 days.
- A metered API near or over its cap, or blocked by a server-side budget.
- A model with spend but no price row (billed at zero) or a price row with no spend.
- Customer-driven costs billed to the company.
- A trial that converted without a decision.

## Savings levers (rank by value per month)
- Cancel or downgrade unused seats and plans.
- Move a pipeline to a cheaper validated model (CTO and CQO check quality first).
- Cache or batch metered calls; remove duplicated calls between pipelines.
- Pass customer-driven costs through, or let customers bring their own keys or apps.
- Annual plans only where usage is proven and stable.
- Negotiate with leverage: volume, competitor quote, renewal timing.

## Output discipline
Every figure names its tool or invoice and read date. Estimates are labelled. Nothing is applied by the persona.
