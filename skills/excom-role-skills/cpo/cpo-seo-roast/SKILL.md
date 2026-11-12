---
name: cpo-seo-roast
description: Runs a blunt technical SEO audit of the company site and its code: crawl control, rendering, canonicals, hreflang, structured data, consistent numbers, pricing visibility, speed and money-page links, ranked fatal, revenue, compounding and fluff, ending in fixes for a coding session. Use when organic traffic or signups are flat, a page will not index, after a release that touched routes or templates, monthly, or when someone says "audit the site" or "why don't we rank".
version: 2.0.0
---
# Technical SEO roast

Find what stops the site from being crawled, indexed, understood or chosen, say it in one blunt line, and turn fatal and revenue issues into code fixes. Alt text on a page a search engine cannot reach earns nothing, so fatal comes first.

## Look up first

- The site's SEO system notes (rendering, canonical rules, sitemaps, structured data, supported languages, crawler policy): `excom_knowledge_search` "SEO system", "sitemap", "structured data". If none exists, draft one from what you find with `excom_save_draft`.
- The money pages (product, pricing, use cases, comparisons, docs): `excom_knowledge_search` "money pages" or ask the marketing executive with `excom_send_handoff` (kind question).
- Canonical numbers and prices: `excom_knowledge_search` "products", "pricing".
- Granted apps: Search Console, Bing Webmaster, PageSpeed, DataForSEO. Missing ones: `excom_request_setup`, and write "not verified" instead of guessing.

## Steps

1. Open with a one-line verdict, never a score.
2. Run the checks in references/roast-checks.md: crawl control and rendering with `web_fetch`; indexing with `gsc_url_inspect`, `gsc_bulk_inspect`, `gsc_sitemap_list`, `bing_crawl_issues`, `bing_url_info`; languages (hreflang reciprocity, localized titles); numbers and pricing; speed with `pagespeed_core_web_vitals` and `pagespeed_opportunities`; site-wide issues with `dataforseo_on_page_summary` (metered, one crawl per roast).
3. Money-page links: each needs at least three contextual inbound links from body content (skill cpo-internal-links-code).
4. Rank every finding: FATAL blocks crawl, index or render of a money page; REVENUE indexed but cannot rank or convert; COMPOUNDING authority, links, AI visibility (with the marketing executive); FLUFF one line, untouched while rows above remain.
5. Save the roadmap; open one task per fatal or revenue fix with `excom_propose_task`, fix them with skill cpo-seo-autopilot, and hand compounding items to the marketing executive with `excom_send_handoff`.

## Output

```text
SEO roast <date>. Verdict: <one blunt line>
| # | tier | issue | URL or file | what it blocks (one sentence) | fix | owner | status |
Verify after fix: the exact reads that must pass
Fluff: one line. Not verified: what a missing app prevented
```

Saved with `excom_save_draft`.

## Approvals

- Code changes ship through a coding session that the CTO pushes and deploys (production).
- Sitemap submissions and IndexNow pings (send).
- Paid crawls beyond one on-page summary; SEO suites are optional, paid, ask first with the cost.

## Example

Verdict: "Every product page serves two canonicals, so Google trusts none." FATAL row: product pages, duplicate canonical from a static tag plus the per-route tag, fix: remove the static tag, verify one canonical in the served HTML. REVENUE row: pricing prices load by script only, so AI crawlers see no price.

## References

- references/roast-checks.md: the full check list per tier, with pass and fail rules. Read at step 2 (`excom_skill_load` with the section, or page through).

Adapted from Illyism/seo-skills (seo/seo-roast), MIT. Modified: rewritten generic for EXCOM.
