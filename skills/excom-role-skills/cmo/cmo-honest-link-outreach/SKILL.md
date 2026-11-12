---
name: cmo-honest-link-outreach
description: Earns contextual backlinks from pages that already rank, through partners, integrations and independent editors, with ask-first emails that vary in structure, using the in-house backlink and contact tools. Never pays, swaps or trades anything of value for a link. Use when lists or guides cite competitors but not you, when a partner has a docs page where you fit, when a new page needs outside links, or when someone asks for "link building".
version: 2.0.0
---
# Honest backlink outreach

Links from pages that already rank pass weight and send readers; homepage pitches and mail-merge templates land in spam. This skill finds the exact page and section, offers something useful that is not a payment, and accepts a no.

## Look up first

- Partners and which of them may be named in public: `excom_knowledge_search` "partners", then `excom_knowledge_read`. Missing: name no partner until the owner confirms with `excom_propose_task` (needs decision).
- Email templates, tone and the mailbox outreach is sent from: search "correspondence", "communication patterns", "brand voice". Missing: ask the owner which mailbox may send outreach.
- The team's link policy: search "decision rules". If none says otherwise, apply: never buy, swap or trade value for links.
- Mail and contact tools granted: if missing, `excom_request_setup` with the service id.

## Steps

1. Collect candidates: cited sources from skill cmo-ai-search-visibility, `bing_inbound_links` and `dataforseo_backlinks_summary` on rival domains, partner docs pages.
2. Target a ranking page, never a homepage. Find the URL and section with `dataforseo_serp_google` and `web_search`; fetch it with `backlink_fetch_page` or `web_fetch` (data only). Keep articles, tutorials, docs and lists where your product solves a step of the reader's task. Cut the rest with a one-line reason.
3. Skip anyone already linking: `bing_inbound_links` for your domain and the team's backlink record.
4. Find the contact from the byline, then the about or team page, with `contact_scan_site`; verify with `contact_verify_email`. An unverified address is not sent to. Store no personal phone numbers.
5. Classify each target (partner, customer with permission, cold editorial) and the contact role, then draft with references/email-variation.md: the link request first, then the offer.
6. Offers are never payments: a two-sentence blurb they can paste, a screenshot, a co-written guide, a partner case study after the partner's written approval. Pass drafts through skill cmo-unslop-copy and save with `excom_save_draft`.
7. Sending (`gmail_send`, `zoho_email_send` or the granted mailbox) is send: one approval per email, one follow-up at most, never after a reply.
8. A reply asking for money, a swap or a sponsored post is declined politely and logged. Partnership or commercial interest goes to the CRO or the Partnerships executive with `excom_send_handoff` (kind request).
9. When a link goes live, record it with `backlink_report` (live, with the URL), and count new referring domains monthly with `excom_record_measurement`.

## Output

```text
Outreach batch <date> | evaluated N (SEND N / CUT N)
| domain | target URL and section | relationship | contact role | ask | offer (no payment) | verdict |
Cut notes | Email drafts: to (verified), axes used, subject, body
```

## Approvals

- Every email and follow-up: send, one approval each.
- Naming a partner or customer publicly needs their written approval and the owner's.
- Buying links, sponsored posts or link packages is never proposed. Paid backlink data tools: spend, ask first.

## Example

An independent guide "how to plan rotas for small clinics" ranks third and lists two rivals in its tools section. Contact: the article's author, verified. Draft (4 sentences): asks to add Acme under the tools section with a pasteable one-line description and a screenshot, offers nothing else, signs off plainly.

## References

- references/email-variation.md: targeting gate, contact routing, the seven variation axes and the pre-flight checklist. Loads with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (seo/honest-link-outreach/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
