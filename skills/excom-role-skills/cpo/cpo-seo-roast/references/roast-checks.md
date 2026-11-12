# Roast checks

## Crawl control (fatal)

- robots.txt defaults to allow, disallows only private or authenticated paths, keeps any per-bot rules the crawler policy decided, and points at the sitemap or sitemap index.
- Script and style paths are never disallowed: search engines render with them.
- The sitemap returns XML, lists only live canonical URLs, and per-language sitemaps exist when the site is multilingual.
- An unknown path returns a real 404, not a 200 copy of the home page.

## Rendering (fatal)

- Fetch each money page and two localized versions. The served HTML carries the main content, exactly one self-referencing canonical, at least one structured data block, and the right html lang. A blank app shell is fatal for crawlers that do not run scripts.
- Above-the-fold content is not hidden by an entrance animation in the served HTML (a hero frozen invisible delays the largest paint).
- Links on marketing pages point at real public routes; app pages go to the app domain.

## Indexing

- Money pages inspected: indexed, canonical as declared, no redirect chain, no stray noindex.
- Submitted versus indexed counts per sitemap; Bing crawl issues read.
- No "indexed" claim without an inspection result.

## Languages (revenue)

- hreflang is reciprocal on every pair checked, with x-default.
- Titles and descriptions are localized, not the source language.
- No source-language strings left on localized money pages.

## Numbers and pricing (revenue)

- Counts stated in the home heading, product pages, llms.txt and structured data are identical and come from one generated source.
- Plans, prices and limits are plain text in the served HTML and match the Offer structured data and llms.txt.
- Organization, WebSite and product structured data are present; any dataset citation URLs resolve.

## Speed (revenue)

- Core Web Vitals on home and two product pages, mobile first. Regressions tied to animation, fonts or a new script are revenue tier.

## Money-page links

- Each money page: in the sitemap, linked from home or main nav, at least three contextual inbound links from body content (nav and footer excluded), within three clicks of home.

## Fluff (bottom line only)

- Missing alt text, meta description length, heading order, minor schema warnings.
