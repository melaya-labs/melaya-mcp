---
name: cpo-seo-autopilot
description: Fixes technical SEO findings in the site's own code through one scoped coding session: re-reads each finding, fact-checks pages against recent product changes, codes the fix with the build's checks, hands the finished session to the CTO to push and deploy, then verifies and submits the changed URLs. Use when an SEO roast left findings, when a page drops out of the index, a canonical or hreflang is wrong, a price or count changed and pages still show the old one, or someone says "fix the SEO issues".
version: 2.0.0
---
# SEO fixes in a coding session

Turn findings into a real change a crawler can see: one focused session in the site repository that fixes the cause, passes the build's checks, and reaches production through the CTO. Advice in a document is not work.

## Look up first

- The SEO system notes and the procedures for adding pages or routes: `excom_knowledge_search` "SEO system", "add a page runbook", "add a route".
- Past fixes and their outcome: `excom_recall` "SEO fix", so a fix that failed twice is not tried a third time.
- The site repository and your coding grant. If coding tools are not offered, ask the owner with `excom_request_setup` to switch on coding for you, and stop.
- Supported languages and the translation procedure: `excom_knowledge_search` "locales", "translation pipeline".

## Steps

1. Re-read each finding now (`web_fetch`, `gsc_url_inspect`, `gsc_striking_distance`, `bing_crawl_issues`). Drop rows that no longer reproduce.
2. Fact check: `gitea_list_commits` (or your repo host's equivalent) since the last run; if a price, plan, limit or count changed, list every page that states the old fact.
3. Pick one theme per session (for example "canonicals and hreflang on comparison pages"), because small diffs review and deploy faster.
4. Write the goal with evidence: URLs, what the served HTML shows, what it must show, files to look at (route SEO config, sitemap and prerender lists, robots and llms files, structured data builders, link helpers).
5. Start it with `excom_code_task` (record write), naming the repository, the goal, the runbook and the evidence. Ask the engine to reproduce with a check first.
6. Follow with `excom_code_status`. Judge the result, not the summary: diff stat, commits, checks, violations, evidence addressed, covering test. A violation or red check: `excom_code_discard` and rethink.
7. New user-facing strings ship in every supported language in the same session.
8. Hand the session to the CTO with `excom_send_handoff` (kind request): session id, findings fixed, checks, what to verify. You cannot push; the CTO reviews and pushes with `excom_code_push` and deploys through CI.
9. After deploy: re-fetch the pages, `gsc_url_inspect` the changed URLs, then propose `indexnow_submit_urls`, `bing_submit_urls` and `gsc_sitemap_submit` (send).
10. Record each fix with `excom_record_fact` and the before and after read with `excom_record_measurement`. If the same fix failed twice, stop and report.

## Output

```text
SEO fix session <date>: theme
| finding | URL | file changed | check that proves it | session id | deployed | verified after deploy |
Handoff to CTO: session id, diff stat, commits, checks, verify list. Next: rows left
```

## Approvals

- Starting the coding session (record write under Prepare).
- Push and deploy: the CTO only (production, always asks).
- IndexNow, Bing and sitemap submissions (send).
- Deleting or redirecting a page with traffic or links: flag it in the handoff first.

## Example

Finding: 40 comparison pages declare an hreflang to a language that has no such page, so engines ignore the set. Session goal: emit alternates only for languages with a published page; check: the build's prerender verification plus a test on the alternate list. CTO pushes and deploys; inspection shows the alternates now resolve.

Adapted from Illyism/seo-skills (seo/seo-autopilot), MIT. Modified: rewritten generic for EXCOM.
