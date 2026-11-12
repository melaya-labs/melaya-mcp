---
name: cmo-seo-title-optimization
description: Rewrites page titles and meta descriptions to win more clicks on pages that already rank, driven by striking-distance and Search Console data, then hands the change to whoever edits the site and measures the result. Use when pages rank on page one or two but get few clicks, when click-through falls while position holds, when new pages need titles, or when someone mentions titles, snippets or CTR.
version: 2.0.0
---
# Title and snippet fixes for click-through

Pages ranking 5 to 20 with many impressions and a low click rate are the cheapest organic win: one title change, no new page. Every title must stay true to the page and the brand voice.

## Look up first

- Brand voice and banned words: `excom_knowledge_search` "brand voice", "positioning", then `excom_knowledge_read`. Missing: apply references/title-patterns.md and propose a voice note with `excom_save_draft`.
- Where titles live (a route SEO config, a CMS, page copy files) and any engine-specific length rules: search "SEO system". Missing: ask the CPO with `excom_send_handoff` (kind question).
- Product facts and counts that may appear in titles: search "products".
- Search Console granted: if not, `excom_request_setup` with service google_search_console.

## Steps

1. Pull candidates: `gsc_striking_distance` for 28 and 90 days with an impression floor, then `gsc_search_analytics` with dimensions query and page to read clicks, impressions, CTR and position per URL. Add `bing_query_stats`.
2. Rank pages by impressions times the CTR gap (typical CTR for the position minus actual). Take at most 10 pages per batch, so the effect can be measured.
3. For each page, `web_fetch` the live page: current title, description, H1, slug. Name the primary query and the intent (product, pricing, comparison, guide, how-to, definition, list).
4. Read the results page: `dataforseo_serp_google` for the primary query. Note repeated patterns (numbers, "vs", "alternative", "how to") and what the snippet must promise to earn the click.
5. Write 3 to 5 options per page with the formula and patterns in references/title-patterns.md. Keep the slug, because changing it breaks links and language alternates.
6. Pick one title and description per page, run them through skill cmo-unslop-copy, save the batch with `excom_save_draft` and send it to the CPO with `excom_send_handoff` (kind request). Translated routes need the change in every language.
7. After deploy, record the change date with `excom_record_fact`. Twenty-eight days later read the same query and page rows and record CTR before and after with `excom_record_measurement`. Revert a title that lost clicks.

## Output

```text
Title batch <date> (window, source)
| page | primary query | position | impressions | CTR now | current title | proposed title (chars) | proposed description (chars) | why |
```

## Approvals

- The code or CMS change and deploy (production).
- Legal and partner pages need their owners' approval as well.
- Paid rank trackers: spend, ask first with the cost.

## Example

Acme's "Shift templates" page ranks 7 for "free shift schedule template" with 4,000 impressions and 0.8 percent CTR. Options: "Free Shift Schedule Template for Small Teams" (44 chars), "Shift Schedule Template: Free, Editable, Printable" (50 chars). Recommended: the first, because the results page is full of "free ... template" titles and the page serves small teams.

## References

- references/title-patterns.md: the title formula, intent patterns, length rules and common fixes. Loads with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (seo/seo-title-optimization/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
