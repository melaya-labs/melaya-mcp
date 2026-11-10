# Worked example: a company vault from Drive, Notion, Slack and mail

Fictional throughout: Quillfeather Labs (a 9-person company selling a fountain-pen Refill Kit by subscription), its founder Ines Varga, its operations lead Tomas Reyes, and its reseller Harbor Lane Stationers. Domains are `.example`. The flow follows scenario 1 (solo founder growing into a team) in [../modules/scenarios.md](../modules/scenarios.md).

## 1. Charter (intake)

Three questions asked: who reads it (Ines, the team, and the team's assistant), is anything public (not yet), may mail be read (only the `Customers` and `Suppliers` labels, since 2025-01-01). Defaults stated: one vault, all internal; English; monthly refresh.

Test questions (excerpt):

| # | Question | Answered in |
|---|---|---|
| 1 | What is in a Refill Kit box and what does it cost per month? | [[Refill Kit]], [[Pricing Facts]] |
| 2 | Who approves a new reseller, and on what terms? | [[Decision Reseller Margin]] |
| 3 | How does a customer return a damaged kit? | [[Returns Process]] |
| 4 | Which supplier makes the pouches, and what is the lead time? | [[Pouch Supplier]] |
| 5 | What did we decide about a bottle-ink product? | open question (no source) |

## 2. Inventory and triage (sources)

| Source | Scope | Items | Sensitivity | Handling |
|---|---|---|---|---|
| Google Drive | shared drive "Company", 6 folders | 142 files (61 Docs, 23 Sheets, 14 Slides, 44 PDF) | internal; `Finance/Payroll` personal | import; Payroll excluded |
| Notion | workspace "Ops" | 88 pages, 3 databases (Suppliers, Resellers, Roadmap) | internal | import |
| Slack | `#product`, `#ops`, `#announcements`, 2025-01 to now | about 9,400 messages | internal; DMs personal | public channels only, decisions and FAQs |
| Gmail | labels `Customers`, `Suppliers` | 610 threads | confidential (third-party addresses) | decisions and terms only, no addresses |

Excluded and recorded in the Source Ledger: `Finance/Payroll/` (personal), DMs (personal), `credentials.xlsx` found in `Ops/Old` (secret, owner told to move it to the password manager).

Listings recorded, for example Notion:

```bash
python3 scripts/ledger.py plan --vault ~/vaults/quillfeather --source notion --listing work/notion-listing.jsonl
# notion: 91 new, 0 changed, 0 unchanged, 0 gone -> pending items recorded
```

## 3. Skeleton

```bash
python3 scripts/scaffold.py --vault ~/vaults/quillfeather --name "Quillfeather Labs" \
  --sections "10 Company,20 Product,30 Customers,40 Sales and Marketing,50 Operations,90 Reference" \
  --internal "70 Finance and Legal" --owner ines --today 2026-11-10
python3 scripts/check_vault.py --vault ~/vaults/quillfeather   # RESULT: 0 errors, 0 warnings
```

`zones.default` is then set to `internal` in `_Meta/vault-config.json`, since nothing is public yet.

## 4. Batches (extraction, writing, graph, validation)

Order: Notion (curated), Drive Docs, Sheets and Slides, then Slack and Gmail to add decisions and dates. Batches of 25.

Progress line after Notion batch 2: "Notion: 50 of 91 read, 22 notes written, 9 skipped (empty or duplicate), 0 failed. Hubs rebuilt; checker 0 errors."

Conflict met: the Drive pricing deck (2026-03-02, slide 4) says 12 pouches per box; the Notion product spec (2026-10-01) says 12 as well but the Resellers database says 10 for reseller boxes. Both are true for different SKUs: two rows in [[Pricing Facts]], each cited. A Slack message (`#ops`, 2026-09-14) mentions a 15-pouch box "maybe next year": recorded as an open question in [[Refill Kit]], not as a fact.

## 5. Notes (excerpts)

`20 Product/Refill Kit.md`:

```markdown
---
type: concept
description: The Refill Kit is Quillfeather's subscription product, a reusable cartridge plus sealed ink pouches.
tags:
  - area/product
  - topic/refill-kit
  - source/notion
aliases:
  - Kit
  - Refill box
related:
  - "[[Product]]"
  - "[[Ink Pouch]]"
  - "[[Pricing Facts]]"
audience: team
owner: ines
status: current
source_of_truth:
  - "Product spec v3 (Notion, Ops > Product), read 2026-11-03"
  - "[[Pricing Facts]]"
updated: 2026-11-03
reviewed: 2026-11-03
review_every: 90d
open_questions: true
---

# Refill Kit

The Refill Kit lets a fountain-pen user refill a standard cartridge in under a minute, without a bottle.

## At a glance

- One reusable cartridge and twelve [[Ink Pouch|ink pouches]] per box (product spec v3, 2026-10-01).
- Sold by subscription only, monthly or quarterly: prices in [[Pricing Facts#Plans]].
- Refilling: [[Refill Process]]. Returns: [[Returns Process]].

## How it works

The cartridge holds a needle; pressing a pouch onto it fills the cartridge (product spec v3, section Mechanism, 2026-10-01). See [[Refill Process#^step-2]].

## Open questions

| Question | Owner | Why open |
|---|---|---|
| Is a 15-pouch box planned? | ines | mentioned once in #ops (2026-09-14), no decision found |

## Related

- [[Product]]
- [[Ink Pouch]]
- [[Pricing Facts]]
- [[Harbor Lane Stationers]]

## Changelog

- 2026-11-03 import: created from Notion product spec v3 (batch b002).
```

`50 Operations/Decision Reseller Margin.md` (from a mail thread and a Slack announcement):

```markdown
# Decision Reseller Margin

Resellers buy kits at a fixed 30 percent below the monthly subscription price.

## At a glance

- Decision: fixed 30 percent margin, no volume tiers.
- Decided by Ines Varga on 2026-04-01, source: mail thread "Reseller terms v2" (Suppliers label, 2026-04-01) and #announcements (2026-04-02).
- Applies to every reseller signed after 2026-04-01. Review on 2027-04-01.
...
```

## 6. Graph and checks

```text
python3 scripts/graph_report.py --vault ~/vaults/quillfeather
- Notes 214, links 1,486, 6.9 links per note on average.
- Components 1 (largest 214). Max hops from Home 3.
- Orphans 0, dead ends 0, weakly linked (<3) 17, unresolved links 0.
- Sections that never link to each other: 40 Sales and Marketing <-> 90 Reference
```

The last line led to links from campaign notes to [[Glossary]] terms (`autolink.py --types term --apply`, 31 links). Final check: `RESULT: 0 errors, 4 warnings` (four notes over 8 KB until `add_contents.py --apply`, then 0).

## 7. Bound to the team assistant (agents)

The vault is connected in Melaya as a folder on Ines's computer with a cloud copy; the team's Assistant chats tick it read-only with folders `10 Company/`, `20 Product/`, `30 Customers/`, `50 Operations/`, `90 Reference/` (Finance and Legal left out). The five test questions: four answered with citations, the fifth answered "no sourced decision, see the open question in Refill Kit", which is a pass.

## 8. Report to the owner

214 notes (10 hubs, 58 concepts and references, 31 processes, 24 decisions, 19 people and teams, 42 meetings, 30 terms); Notion 91 items (61 written, 27 skipped, 3 duplicate), Drive 142 (88 written, 49 skipped, 5 failed: encrypted PDFs), Slack 9,400 messages (decisions and FAQs only, 46 notes fed), Gmail 610 threads (38 notes fed). 7 open questions with owners. Excluded: payroll, DMs, a credentials sheet. Refresh: monthly, `ledger.py plan` per source, then the batch loop.
