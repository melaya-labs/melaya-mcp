---
name: cmo-ai-search-visibility
description: Measures how often your company is cited or recommended when people ask AI assistants and search engines the questions your products answer, compares with competitors, checks crawler access and page extractability, and ends with three next actions. Use when a monthly GEO or AI visibility brief is due, after comparison or guide pages ship, or when someone asks "are we in ChatGPT answers" or "why do AI tools recommend our rival".
version: 2.0.0
---
# AI search visibility report

A sampled, repeatable read of AI-answer visibility built from free reads (web search, SERP data, Search Console, Bing, your own crawler files), not a paid tracker. It tells the team where it is cited, where it is missing, and which skill fixes each gap.

## Look up first

- The prompt set from last month: `excom_recall`. Missing: build one with references/prompt-set.md and store it with `excom_record_fact`, so months compare.
- Products and competitors: `excom_knowledge_search` "products", "competitors", then `excom_knowledge_read`. Missing: ask the owner with `excom_propose_task` (needs decision) for the three rivals that matter most.
- Metric definitions for visibility: search "metrics definitions". Missing: propose "cited rate" and "recommended rate" as defined in references/prompt-set.md to the CDO with `excom_send_handoff` (kind question).
- Search Console and Bing granted: if not, `excom_request_setup` with the service id.

## Steps

1. Run each prompt through `web_search` (it fails over across several engines that assistants also retrieve from) and `dataforseo_serp_google` (organic results plus any AI Overview block and its sources). Note whether your site is cited, which page, which rival pages, which independent lists and threads.
2. Repeat each prompt three times across the month and report a rate with its sample size ("cited 2 of 3"), because AI answers are non-deterministic and one run is an anecdote.
3. Separate citation from recommendation: being a source is not being on the shortlist. Record whether you are named as an option and how you are framed.
4. Map the third-party sources cited most (lists, threads, directories, code repositories). They feed skills cmo-reddit-serp, cmo-directory-submissions and cmo-honest-link-outreach.
5. Check foundations with `web_fetch` and the checklist in references/prompt-set.md: crawler access in robots.txt, an llms.txt whose facts match the products note, prerendered or server-rendered pages with one canonical and structured data. Gaps go to the CPO with `excom_send_handoff` (kind request).
6. Read organic support: `gsc_search_analytics` for the matching queries and `bing_query_stats`. There is no AI-specific report in Search Console; a page that does not rank is rarely cited.
7. Check extractability on the five most important pages (answer in the first 40 words, question H2s, self-contained comparison blocks, dated facts). Fixes go through skill cmo-unslop-copy.
8. Write the brief in short paragraphs: where you are cited, where you are missing, who owns the answer and why, and three next actions with the skill for each. Save with `excom_save_draft`.
9. Record cited rate, recommended rate and sample size with `excom_record_measurement`.

## Output

```text
AI visibility <month>: prompts N, runs per prompt N, engines read
| prompt | cited (rate) | recommended (rate) | your page | top rival cited | top third-party source |
Foundations: crawler access ok/gap, llms.txt ok/gap, rendering ok/gap
Brief (3 to 6 short paragraphs) | Next actions: action | skill | owner
```

## Approvals

- Paid trackers: spend, optional, ask first with the monthly cost; never a step.
- Changes to robots.txt, llms.txt or structured data: production, through the CPO and the production holder.

## Example

Acme, 20 prompts, 3 runs each. Cited on 6 of 20 prompts (rate 0.3, n=60), recommended on 2. A rival owns "best rota app for nurses" through two independent lists that never mention Acme. Next actions: pitch both lists (cmo-honest-link-outreach), add a persona page (cmo-vs-alternatives), fix a stale llms.txt count (CPO).

## References

- references/prompt-set.md: how to build the prompt set, the rate definitions and the foundations checklist. Loads with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (seo/ai-seo-report/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
Adapted from coreyhaines31/marketingskills (skills/ai-seo/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
