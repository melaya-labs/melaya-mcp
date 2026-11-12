# Weekly SEO review defaults

Use these until the team's metrics or rhythm note sets its own. Propose them to the owner the first time.

## Default thresholds

| Signal | Threshold | Action |
|---|---|---|
| Non-brand clicks, 28 days vs prior 28 | down more than 20 percent | Investigate top movers this review; tell the owner |
| A key page not indexed | any | CPO handoff the same day |
| New route not indexed after 7 days | any | Check canonical, rendering, links; resubmit after the fix |
| Key page failing mobile vitals | any of LCP, INP, CLS | CPO handoff with the opportunities list |
| Crawl errors | new type or more than 10 new URLs | CPO handoff |
| A page down 3 or more positions on its main query | any | cmo-blog-refresher |
| Striking-distance query with no fitting page | any | cmo-content-coverage |

## Brand split

Define brand queries as those containing the company or product names from the products note. Report brand and non-brand separately every week; a stable total can hide a non-brand fall.

## Comparing weeks

- Same windows every week (7 and 28 days, each against its prior period).
- Search Console data lags by a couple of days; read the same lag every time.
- Note deploys, launches and outages in the review, since they explain most jumps.

## Review note template

```text
SEO review <date>
Windows: 7d and 28d vs prior | Data lag: N days
Google: clicks, impressions, CTR, position (brand / non-brand)
Bing: clicks, impressions
Indexing: new routes N, indexed N / N, sitemap status, crawl issues
Vitals (mobile): key pages pass or fail
Authority (monthly): referring domains, new this month
Events this week: deploys, launches, outages
Top movers: page or query, change, likely cause
Actions (max 5): action, owner, due
Last week's actions: done, open, dropped (why)
```

## Escalation

- Tracking or property access lost: owner, the same day.
- A drop across all pages at once: check for a deploy, robots.txt or canonical change before anything else, then the CPO.
- Metric definitions disputed between sources: CDO.
