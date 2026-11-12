---
name: cmo-vs-alternatives
description: Writes or refreshes honest comparison pages ("You vs X"), competitor alternative pages and best-tool-for-persona lists, built on sourced switching triggers, real pricing math and a mandatory "where X is better" section. Use when a competitor changes pricing or ships, when buyers search "X alternative" or "you vs X", when a comparison page slips, or when sales keeps losing deals to one rival.
version: 2.0.0
---
# Comparison and alternatives pages

Ships comparison pages that give a buyer leaving a competitor a sourced reason to try you, and give AI assistants checkable facts to quote. Buyers comparing tools are the organic traffic closest to a purchase.

## Look up first

- Competitors, their category and the existing comparison verdicts: `excom_knowledge_search` "competitors" or "competition", then `excom_knowledge_read`. Missing: draft a competitor note with `excom_save_draft` from `dataforseo_competitors` and propose it.
- Your products, honest limits and compliance claims you may and may not make: search "products", "positioning", "security posture". Missing: ask the owner with `excom_propose_task` (needs decision); never claim a certification you cannot source.
- Your public prices: search "pricing and plans" and confirm on your live pricing page with `web_fetch`. Quote only what the public page shows.
- Existing comparison routes and where their copy lives: search "SEO system" or ask the CPO with `excom_send_handoff` (kind question). Rewrite or extend, never duplicate.

## Steps

1. Pick one competitor and the one product of yours it really competes with. Never compare your whole catalogue.
2. Check demand: `dataforseo_keyword_volume` and `bing_keyword_research` for "[x] alternative", "[x] alternatives", "you vs [x]", "[x] vs you"; `gsc_search_analytics` filtered on the competitor name. Choose the page type: head to head when buyers are choosing, an alternatives list when they are leaving, both when both have demand, none when neither has demand.
3. Mine switching triggers from public sources only: `web_search` for reviews and threads, `reddit_search_posts`, and the competitor's own pricing, changelog and docs with `web_fetch`. Apply the gates in references/page-structure.md. If you lose on every trigger, do not ship; report it to the owner instead.
4. Recheck every competitor price on its pricing page in this turn, because stored prices go stale. An unverifiable price becomes "check [x]'s pricing page".
5. Draft the page in the section order in references/page-structure.md, competitor's strengths first, then pass it through skill cmo-unslop-copy.
6. Save with `excom_save_draft` and send a claims review request to the CLO with `excom_send_handoff` (kind request); ask the CRO to confirm any price framing.
7. If the copy lives in code (and in several languages), send the approved copy to the CPO with `excom_send_handoff` (kind request). Deploy belongs to the production holder.
8. After deploy, `gsc_url_inspect` the URL, propose IndexNow and sitemap submission (send), and record the date the facts were checked with `excom_record_fact`.

## Output

```text
Competitor trigger file (draft): | trigger | category | evidence URL | count 12 mo | verified on live page (date) |
Where [X] wins: 3+ bullets
Page copy (draft): H1, verdict, trigger table, pricing math with source and date, switch steps, where X is better, FAQ, CTA
Summary: | route | target query | sourced facts | competitor wins (count) | status |
```

## Approvals

- Deploying the page (production) and IndexNow or sitemap pushes (send).
- Any named-competitor claim passes the CLO before it ships.
- Never use competitor logos or screenshots of their interface.

## Example

Acme's analytics tool loses deals to "DataCo". Reviews show three recurring complaints about a 5-seat minimum, confirmed on DataCo's pricing page today. The page opens: "Pick DataCo if you need its 300 native connectors and SOC 2 report. Pick Acme if you are a team of 1 to 4 and want flat pricing." Pricing math at 1, 5 and 25 seats follows, each figure footnoted with the URL and check date.

## References

- references/page-structure.md: trigger gates, section order, persona list rules, title limits. Read before drafting; loads with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (seo/vs-and-alternatives/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
