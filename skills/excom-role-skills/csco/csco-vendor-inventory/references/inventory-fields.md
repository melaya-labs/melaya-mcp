# Inventory categories, fields and flags

## Categories
- Compute and hosting (production hosts, databases, object storage, backups)
- Edge and DNS (CDN, TLS, registrar)
- Model providers (hosted APIs, routers, local and CLI engines)
- Metered APIs (search, data, enrichment, proxies, ads, posting)
- SaaS and operating tools (mail, docs, trackers, design, analytics)
- Signing and developer accounts (code-signing certificates, store developer programmes, business identifiers they require)
- Distribution channels (app stores, package registries, extension stores, directories)
- Observability and logs
- Payments and billing
- Device hardware (test phones and computers)

## Row fields
supplier | category | purpose | owner role | plan or tier | amount and billing period (source: invoice or console, or "not measured") | renewal date | cancel-by date | processes customer data (yes/no, subprocessor row) | data location | single point of failure (yes/no) | fallback (from the continuity plan, or "none recorded") | terms or DPA on file (yes/no/verify) | security evidence (from the CISO) | evidence source and read date | flags

## Never record
Keys, tokens, passwords, instance ids, IP addresses, internal hostnames, bank details, serial numbers, personal data.

## Flags
- no fallback recorded
- trial converts to paid (date, price)
- renewal or cancel-by within 30 days
- terms or DPA not on file
- single point of failure
- no balance or usage tool (cost not measured)
- unused in 90 days (candidate to cancel)
- customer-driven cost billed to the company

## Scoring (quick)
Cost, lock-in and exit cost, security posture (CISO), reliability: low, medium or high, each with one line of evidence.
