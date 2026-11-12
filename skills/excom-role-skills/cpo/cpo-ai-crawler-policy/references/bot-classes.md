# Bot classes and decision order

## Classes

| Class | What it does | Typical value | Default |
|---|---|---|---|
| Search and answer retrieval | Indexes or fetches pages to answer queries and cite sources | Citations and visits from AI search | Allow |
| User-triggered fetch | Fetches a page because a person asked an assistant about it | A live prospect | Allow |
| Training crawler | Collects pages for model training | Shapes what models know about you; no direct visit | Allow unless a stated reason |
| Classic search engine | Web search indexing | Organic traffic | Allow |
| SEO tool crawler | Backlink and audit tools | Third-party visibility data | Allow at a polite rate |
| Unknown or spoofed | A known bot name from addresses the operator does not publish, or no identity | None, often abuse | Block at the edge |

## Verify the operator, not the user agent

- Any client can send any user agent string. Trust a bot name only when the request comes from the operator's published address ranges or passes the operator's reverse DNS check, as the edge provider's verified-bot list does.
- Search bots and their training siblings use separate user agents from the same company. Decide each one separately; blocking the training agent never requires blocking the search agent.

## Decision order

1. Is it verified? If not, treat it as unknown or spoofed.
2. Does it touch only public pages? Paths for the app, API and authenticated areas stay disallowed and access-controlled for every bot.
3. Is volume a real cost? Measure requests per day and bandwidth against total traffic before acting.
4. Prefer the lightest control: allow, then rate limit at the edge, then a per-bot robots rule, then an edge block for spoofed or abusive agents.
5. Every limit or block names one bot, its evidence and a review date.

## Never

- A blanket deny for unknown agents on public pages.
- Locking sitemaps to one engine.
- Serving crawlers a page that differs from what users see.
- Bare 403 walls on public marketing pages.
