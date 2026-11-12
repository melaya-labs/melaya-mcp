---
name: cmo-weekly-seo-review
description: A fixed weekly read of organic search from Search Console, Bing Webmaster, PageSpeed and backlink data that checks indexing of new pages, finds quick wins, flags speed failures and ends in at most five owned actions. Use when the team's weekly SEO day comes round, after a deploy that added or renamed pages, when organic clicks drop, or when someone asks "how is SEO doing" or "why did traffic fall".
version: 2.0.0
---
# Weekly SEO review loop

One repeatable weekly read that keeps indexing, titles and pages from drifting unnoticed, and turns what it finds into a handful of owned actions instead of a report nobody acts on.

## Look up first

- The team's acquisition outcome and your charter objectives (in context); `excom_recall` for last week's review so weeks compare on equal windows.
- The review day, thresholds and metric definitions: `excom_knowledge_search` "weekly rhythm", "metrics definitions", "SEO system", then `excom_knowledge_read`. Missing: use the defaults in references/review-template.md and propose them to the owner with `excom_propose_task` (needs decision).
- Site properties and verification status: the SEO note. Search Console or Bing not granted: `excom_request_setup` with service google_search_console or bing_webmaster.
- The list of key pages (home, pricing, product pages): the products note or the SEO note.

## Steps

1. Performance: `gsc_search_analytics` for the last 7 and 28 days against the prior periods, by query and by page; `gsc_top_queries`; `bing_query_stats` and `bing_rank_traffic_stats`. Split brand from non-brand, because brand clicks hide non-brand losses.
2. Quick wins: `gsc_striking_distance`. Pages with a click-rate gap go to skill cmo-seo-title-optimization; queries with no fitting page go to skill cmo-content-coverage.
3. Indexing: list routes added this week (ask the CPO with `excom_send_handoff`, kind question, or read the sitemap with `web_fetch`); check them with `gsc_bulk_inspect` and `bing_url_info`; read `gsc_sitemap_list` and `bing_crawl_issues`. Not indexed after a week: check canonical, rendering and inbound links.
4. Submission: after a route batch, propose `gsc_sitemap_submit`, `bing_submit_urls` and `indexnow_submit_urls` for live new URLs (send, unless an approved rule covers resubmission after deploys).
5. Speed: `pagespeed_core_web_vitals` (mobile) for key pages, `pagespeed_opportunities` for any page failing LCP, INP or CLS. Fixes go to the CPO with `excom_send_handoff` (kind request) and the evidence.
6. Authority, monthly rather than weekly: `dataforseo_domain_rank_overview` and `dataforseo_backlinks_summary` (paid per call), `bing_inbound_links` for new referring domains.
7. Content health: articles published this week by any automated writer are read with `web_fetch` for voice and truth; off-brand ones and pages that slipped more than three positions go to skill cmo-blog-refresher.
8. Decide at most five actions, each with an owner (a CMO skill, the CPO for code, the production holder for deploy or DNS, the CDO for definitions) and a due date. Create them with `excom_propose_task`.
9. Record headline numbers with `excom_record_measurement` (28-day clicks and impressions, non-brand clicks, indexed share of new routes, key pages passing vitals) and save the review with `excom_save_draft`.

## Output

```text
SEO review <date> (7d and 28d vs prior)
Google: clicks N (delta), impressions N, CTR, avg position | non-brand clicks N
Bing: clicks N, impressions N | New routes: N, indexed N (Google), N (Bing)
Vitals (mobile): pass/fail per key page | Top movers: | page or query | change | likely cause |
Actions (max 5): | action | owner | due |
```

## Approvals

- Sitemap, Bing URL and IndexNow submissions: send, until a rule covers them.
- Code, robots.txt, DNS or search property changes: production, through the CPO and the production holder.
- Paid tools beyond the planned DataForSEO calls: spend, ask first with the cost.

## Example

Acme, week 12: Google clicks down 18 percent over 28 days, all of it non-brand, concentrated on two guides that lost position after a competitor refreshed theirs. Three new routes, one not indexed (canonical points to staging). Actions: refresh both guides (cmo-blog-refresher), CPO fixes the canonical, resubmit the sitemap after deploy.

## References

- references/review-template.md: default thresholds, the escalation table and the review note template. Loads with `excom_skill_load` or by paging.
