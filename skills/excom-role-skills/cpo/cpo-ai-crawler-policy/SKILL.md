---
name: cpo-ai-crawler-policy
description: Decides, bot by bot and with the marketing executive, whether each AI crawler is allowed, rate-limited or blocked, keeping AI search and answer visibility by default and never blanket-blocking, then ships robots and llms file changes in code and proposes edge rules. Use when a crawler's volume or cost is questioned, a new AI bot appears in logs, someone asks to "block AI bots" or "stop scrapers", or on the monthly check that AI crawlers still get full pages.
version: 2.0.0
---
# AI crawler policy, bot by bot

If your company wants to be found and cited in AI answers, the default is welcome. This skill decides per bot when to limit or block, with evidence, and never blanket-blocks, because one broad rule can erase the site from AI search.

## Look up first

- The company's crawler stance and current rules: `excom_knowledge_search` "crawler policy", "robots", "AI visibility", and `excom_recall` past bot decisions. If no stance is written, ask the owner with `excom_propose_task` (needs decision): "Do we want AI search and answer visibility?"
- The marketing executive's AI visibility goals (citations, AI referrals) from the team's outcomes.
- Edge evidence: the CTO or CISO holds it (bot management, firewall events, traffic by user agent).

## Steps

1. Read the current state: `web_fetch` robots.txt and llms.txt. Ask the CTO or CISO with `excom_send_handoff` (kind question) for `cloudflare_get_bot_management`, `cloudflare_firewall_events` and `cloudflare_traffic_analytics` filtered by user agent, if your edge is Cloudflare.
2. Classify each bot with references/bot-classes.md: search and answer retrieval, user-triggered fetch, training crawler, SEO tool crawler, unknown or spoofed.
3. Decide with the rules there: retrieval and user-triggered allow; training allow by default and limit only with a reason marketing accepts; SEO tools allow at a polite rate; spoofed agents blocked at the edge; anything hammering app, API or authenticated paths rate-limited at the edge, never by robots.txt alone.
4. Never: a blanket deny on public pages, hidden sitemaps, a different page for crawlers than for users, or blocking a search bot to stop its training sibling (they use separate user agents).
5. Confirm allowed crawlers get the real content: `web_fetch` two product pages and pricing; the served HTML holds text, prices and structured data.
6. Agree the decision table with the marketing executive via `excom_send_handoff` (kind request); bring in the CISO for abuse or spoofing.
7. Ship robots.txt and llms.txt changes in a coding session (`excom_code_task`, record write) and hand it to the CTO for `excom_code_push` and deploy. Edge rules are proposals to the CTO or CISO, never applied by you.
8. After deploy, re-fetch robots.txt; once approved, record the decision with `excom_publish_decision`. Review in 30 days with marketing's AI visibility read and `excom_record_measurement`.

## Output

```text
AI crawler policy <date>
| bot | operator | purpose | evidence (volume, paths, codes) | decision | where (robots, edge) | reason | agreed by marketing | review date |
Unchanged defaults; code session id; edge proposal (if any)
```

Saved with `excom_save_draft`.

## Approvals

- robots.txt or llms.txt changes ship through the CTO (production).
- Edge firewall or rate-limit rules (production, CTO or CISO, the owner approves).
- Blocking any search or retrieval bot needs marketing's agreement and the owner's approval.
- Paid bot-management or AI visibility tools: optional, ask first with the cost.

## Example

Logs show 40,000 hits a day from a bot named like a known training crawler, from hosting addresses its operator does not publish. Class: spoofed. Decision: block at the edge (proposal to the CISO), robots unchanged. The real training crawler stays allowed.

## References

- references/bot-classes.md: bot classes, how to verify an operator, and the decision order. Read at step 2 (`excom_skill_load` with the section, or page through).

Adapted from Illyism/seo-skills (seo/block-ai-scrapers), MIT. Modified: rewritten generic for EXCOM.
