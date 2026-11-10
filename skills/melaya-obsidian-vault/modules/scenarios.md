# Scenario playbooks

> **Use when:** starting a vault and you want the end-to-end order of modules for the situation, with its specific defaults.
> **Inputs:** the scenario recognised in [intake.md](intake.md).
> **Outputs:** the module path, the sections and the defaults for that scenario.
> **Next:** the first module of the path.

Every path starts with intake, tools and sources, uses `scaffold.py` for the skeleton, runs the batch loop (extraction, extract-types, architecture, properties, writing, graph, validation) per source, and ends with a report. Only the differences are listed.

## 1. Solo founder

- **Path:** intake, tools, sources, scaffold, extraction (Drive, Notion, mail by label, chat channels), architecture, properties, writing, graph, validation, agents.
- **Sections:** 10 Company, 20 Product, 30 Customers and Market, 40 Sales and Marketing, 50 Operations, 70 Finance and Legal (internal), 90 Reference.
- **Defaults:** whole vault internal; personal mail excluded; one canonical fact sheet each for pricing, metrics and key dates; decision records from mail and chat; investors, customers and partners as organisations.
- **Done:** an assistant answers the founder's 10 test questions with citations.

## 2. Team wiki

- **Path:** intake (owners per section), sources (wiki, docs, team channels, tickets), scaffold, extraction, architecture (one hub per team area), writing, graph, validation, agents (team assistant read-only), maintenance (monthly).
- **Sections:** 10 Team, 20 Projects, 30 Processes, 40 Systems, 50 Decisions, 90 Reference.
- **Defaults:** `owner` and `review_every` on every note (`required_by_zone` extended to all notes); one decision record per significant decision; runbooks from incident tickets; an Editing Protocol naming who writes where.

## 3. Company handbook

- **Path:** intake (audience: every employee; HR as owner), sources (handbook docs, policies, HR wiki, onboarding decks), scaffold, extraction, writing (policy voice, second person), zones (public culture pages vs internal policies), multilingual if needed, validation, agents (an onboarding assistant), maintenance (quarterly policy review).
- **Sections:** 10 About Us, 20 How We Work, 30 Policies, 40 Benefits and Tools, 50 Onboarding, 90 Reference.
- **Defaults:** every policy a `reference` note with `owner`, effective date and `review_every: 180d`; FAQ notes with folded callouts; no individual cases, no salaries, no personal data.

## 4. Research vault

- **Path:** intake (research questions as test questions), sources (PDF library, reference manager export, web clippings, lab notes, transcripts), scaffold, extract-types (PDF with OCR, web, audio), architecture (add `literature` and `claim` types), writing (claims with page citations), graph (concepts to claims to literature), views (Bases per question, Canvas argument maps), validation.
- **Sections:** 10 Questions, 20 Concepts, 30 Literature, 40 Methods, 50 Data, 60 Findings, 70 Writing, 90 Reference.
- **Defaults:** one literature note per source with full reference, key claims, method, limits, and your reading clearly separated; atomic claim notes linking evidence for and against; citation keys as aliases; quotes short and paged.

## 5. Client project vault

- **Path:** intake (client, scope, NDA, retention), sources (shared drive folder, project channel, mail label, tickets), sensitivity triage (confidential), scaffold, extraction, writing, zones (a client-shareable zone if deliverables are shared), validation, agents (project assistant scoped to the folder), maintenance (weekly while active), archive at close.
- **Sections:** 10 Client, 20 Scope and Contract (internal), 30 Deliverables, 40 Meetings, 50 Decisions, 60 Risks, 90 Reference.
- **Defaults:** the client name only where the owner allows; contract terms summarised, the contract linked; one vault per client or a strict folder per client with a deny list for other clients' names; at close, `status: archived` and a closing note.

## 6. Migration from Notion, Confluence, Drive, OneNote or Evernote

- **Path:** intake (cut-over date), tools, sources (the export), migration (the system's recipe), extraction (ledger over every page), architecture (mapping table), properties, writing (normalise, do not rewrite everything at once), graph, validation, maintenance (refresh until the old system is retired).
- **Defaults:** keep page names when they are good; a redirect table; drop empty, duplicate and obsolete pages after the owner reviews the list; databases become folders plus Bases.

## 7. Personal knowledge base

- **Path:** intake (what the person wants to find again), sources (notes apps, bookmarks, highlights, journals with consent), scaffold (private, `zones.default: internal`), extraction, architecture (areas, projects, resources, journal), writing, graph, views.
- **Sections:** 10 Areas, 20 Projects, 30 Resources, 40 Journal, 90 Reference.
- **Defaults:** private vault only; light properties (type, description, tags, updated); journals mined for decisions and ideas, not copied whole unless asked; no third-party personal data.

## 8. Multilingual vault

- **Path:** intake (languages and readers per language), sources, multilingual (layout choice), scaffold (`--languages`), extraction, writing (voice card per language), graph (per-language trees), validation, maintenance (stale translations).
- **Defaults:** layout A (one language, others summarised) unless every page must be translated; properties and tags in the primary language; translations linked both ways.

## 9. Public plus private zones (docs site plus internal notes)

- **Path:** intake (what is public), sources, scaffold (`--internal`), zones (manifest, flags, deny list), writing (public voice, no internals), graph, validation, zones again (export), agents (public assistant bound to public folders only).
- **Defaults:** public notes describe what users do and see, never how it is built inside; internal notes may link out to public ones; `export_public.py` before every publish; `denylist_public` filled with internal names.

## 10. Team knowledge for AI agents (agent-first vault)

- **Path:** intake (the agents' jobs and questions), sources, scaffold, writing (chunk-friendly), graph, agents (binding, scopes, editing protocol), validation, maintenance (scheduled refresh pipeline).
- **Defaults:** strong descriptions and At a glance on every note; canonical fact sheets; per-agent write folders; test questions run through the bound agent.

## 11. Ongoing sync and refresh (added to any scenario)

- **Path:** maintenance (incremental refresh with the ledger), extraction, writing, validation, on a cadence.
- **Defaults:** monthly for wikis and docs, weekly for tickets and chats; a refresh report each run; gone items reviewed, never auto-deleted.

## 12. Rescue of an existing messy vault

- **Path:** intake (keep or change conventions), validation (baseline report), graph (graph_report), architecture (target sections), properties (backfill with scripts or by hand), maintenance (dedupe, merge, split, rename in Obsidian), graph, validation.
- **Defaults:** never restructure without the owner's yes; fix in passes (links and names first, then properties, then hubs, then style); report before and after metrics.

## The final report (every scenario)

Notes per section and type; sources with read, written, skipped and gone counts; the checker's RESULT line and remaining warnings; open questions with owners; what was excluded and why; how to refresh (commands or the scheduled pipeline); the test questions with the notes that answer them.
