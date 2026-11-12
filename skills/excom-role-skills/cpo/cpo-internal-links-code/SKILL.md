---
name: cpo-internal-links-code
description: Does the code side of internal linking: measures contextual inbound links per page (nav and footer excluded), finds orphaned money pages, and adds topical body links, a reusable related-links block, hub links and breadcrumbs through a coding session. Use when a product, pricing, use-case or comparison page has few internal links, when the marketing executive hands over a linking plan, when a new page ships, or when someone asks "why doesn't this page rank" or "link the blog to the product".
version: 2.0.0
---
# Internal links in the site code

Route the traffic and link equity that posts, guides and docs already earn into the pages that convert. Marketing decides anchors and targets; this skill builds the link graph, the link components and the session that ships them.

## Look up first

- The money pages and the site's linking rules (link helpers, language prefixes, which routes are public): `excom_knowledge_search` "SEO system", "internal linking", "money pages". If missing, ask the marketing executive with `excom_send_handoff` (kind question).
- The last link report: `excom_recall` "internal links".
- Top pages by clicks: `gsc_search_analytics` (dimension page, 90 days). If Search Console is not granted, `excom_request_setup`, and rank sources by inbound links instead.
- Supported languages, because anchor text is user-facing: `excom_knowledge_search` "locales".

## Steps

1. Build the before graph in a coding session (`excom_code_task`, record write): contextual inbound links per public route from body content; nav, footer, language switchers and layouts excluded because sitewide links carry no topical context. Add pages generated from data files by hand. Ask for the table in the session summary, not a new repo file.
2. Classify: money page with under 3 contextual inbound links is an orphan, 3 to 9 underlinked, 10 or more fine. Sources are the top 20 non-money pages.
3. Match each source to one to three targets whose topic it already discusses; never link an unrelated page to reach a count.
4. Apply the placement and anchor rules in references/link-rules.md.
5. Use the site's link helpers so language prefixes are kept and every target is a real public route (a hand-built path can 404). Links render as real anchors, never click handlers. Anchor text lives in the translation files and ships in every supported language.
6. Where a page type has no related-links block, add one reusable component fed by the existing data, so new pages get links automatically. Hubs link children; children link the hub, two siblings and pricing; breadcrumbs match the BreadcrumbList data.
7. Follow with `excom_code_status`: the build checks pass and the after graph is in the summary; `excom_code_discard` on a violation.
8. Hand the session to the CTO with `excom_send_handoff` (kind request) for review, `excom_code_push` and deploy. After deploy, `web_fetch` three edited pages to confirm the links are in the served HTML.
9. Record before and after counts per target with `excom_record_measurement`.

## Output

```text
Internal links report <date>
| target | before (contextual) | after | distinct anchors | source pages | languages done |
Components added; hubs and breadcrumbs fixed; remaining orphans and why
```

Saved with `excom_save_draft`, with the session id and the CTO handoff.

## Approvals

- Starting the coding session (record write); push and deploy by the CTO (production).
- Anchor copy on pages marketing owns: agree with the marketing executive first.
- External or paid links are marketing's: optional, paid, ask first with the cost.

## Example

Acme's "/vs/rival" page has 1 contextual inbound link. Three guides discuss switching tools; each gets one link in its first third with anchors like "compare Acme with Rival on pricing". A related-comparisons block now links every comparison to two siblings. After: 7 contextual links, 5 distinct anchors.

## References

- references/link-rules.md: placement, anchor variety, dofollow and hub rules. Read at step 4 (`excom_skill_load` with the section, or page through).

Adapted from Illyism/seo-skills (seo/internal-linking), MIT. Modified: rewritten generic for EXCOM.
