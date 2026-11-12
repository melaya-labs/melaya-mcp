---
name: cmo-internal-linking
description: Builds an internal linking plan that routes traffic and link equity from guides and blog posts into the pages that convert (product, pricing, use case and comparison pages), with exact sentences and anchors, then hands the code change to whoever edits the site. Use when informational pages earn clicks but money pages get none, when a new page ships with no inbound links, or after a content batch goes live.
version: 2.0.0
---
# Internal linking plan

Informational pages usually earn most organic visits while the pages that convert sit orphaned. A few contextual links in body copy move both ranking signals and readers. You own the plan; the edit goes to whoever changes the site.

## Look up first

- Money pages (product, pricing, use cases, comparisons, hubs): `excom_knowledge_search` "SEO system", "site structure", "products". Missing: ask the CPO with `excom_send_handoff` (kind question) for the list of public routes and where body copy lives.
- Site rules that break links (prerendered routes only, language prefixes, sitewide footer links): same notes. Missing: verify each target with `web_fetch` before planning a link to it.
- Who edits the site: the team charter in your context (usually the CPO codes and the CTO deploys). If the site runs on a CMS you are granted, check your grants for its tools.
- Search Console granted: if not, `excom_request_setup` with service google_search_console.

## Steps

1. Rank source pages: top 20 non-money pages by clicks from `gsc_search_analytics` (dimension page, 90 days) and `bing_page_stats`.
2. Count contextual inbound links per money page. Ask the CPO for a body-link count from the repository (nav and footer excluded), or sample prerendered pages with `web_fetch`. Fewer than 3 contextual links: orphan target; 3 to 9: underlinked; 10 or more: fine. Footer and nav links do not count, because a template link carries no topical context.
3. Match each source to 1 to 3 targets its topic already covers. Never add an unrelated target to reach a count.
4. Write the anchor plan with the rules in references/anchor-rules.md: at least one link in the upper 40 percent of the body, 2 to 4 new links per page, descriptive anchors, varied across the site.
5. Prefer wrapping an existing phrase. If none fits, draft one new useful sentence. Add one short callout per source page right after the section that explains the problem; numbers only from the products note.
6. Check hubs and laterals (references/anchor-rules.md). Every target must be a live, indexable page; translated pages need the same links in every language the site ships.
7. Save the plan with `excom_save_draft`, then hand it to the CPO with `excom_send_handoff` (kind request) as file, sentence, anchor, target. Track with `excom_propose_task`.
8. After deploy, re-count with the same method and record before and after with `excom_record_measurement`. Propose an IndexNow push for changed URLs (send).

## Output

```text
Internal links plan <date> | sources N | links planned N | callouts N
| target | contextual before | planned after | distinct anchors | source pages |
| source page | sentence (existing or new) | anchor | target | upper 40%: yes/no |
Remaining orphans: target, reason (needs a page: see cmo-content-coverage)
```

## Approvals

- The code change, push and deploy (production, through the roles that hold them).
- IndexNow or sitemap submissions (send).

## Example

Acme's guide "how to export invoices to CSV" gets 900 clicks a month; its pricing page has 2 contextual links. Plan: wrap "export every invoice as a spreadsheet" in paragraph two with a link to the export feature page, add one sentence linking "compare plans for teams of five" to pricing, and a callout after the "why exports fail" section.

## References

- references/anchor-rules.md: placement, anchor and hub rules plus the verification checklist. Loads with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (seo/internal-linking/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
