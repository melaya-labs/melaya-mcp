---
name: cdo-affiliate-attribution
description: Credits registrations and paying customers to affiliates, partners and channels. It counts active affiliates (at least one referred signup), joins referrals to Stripe customers, audits UTM tagging and unmapped referrers, and flags leakage, self-referrals and existing accounts for the commission check. Use when preparing the weekly affiliate and ads reviews, when an affiliate or partner asks for their numbers or claims a customer, when a new partner page goes live, or when asked "who brought this customer".
version: 2.0.0
---

# Affiliate and partner attribution

Know which affiliate, partner or channel brought each signup and customer. That way the team invests in the sources that move its outcomes, and pays commissions only on real referrals.

## Look up first

- The active affiliate and signed partner definitions: `excom_knowledge_search` "metrics definitions". If missing, propose the defaults (an active affiliate has at least one referred signup; a signed partner has a signed agreement filed in its partner folder) and use them, labelled "proposed".
- The programme terms (attribution window, exclusions): `excom_knowledge_search` "affiliate programme terms".
- The tagging convention for links: `excom_knowledge_search` "tracking conventions". If missing, propose the one below.

## Steps

1. Affiliates: `affonso_list_affiliates`, `affonso_list_referrals` and `affonso_get_affiliate_analytics`, or your affiliate platform's equivalents. Count enrolled, active (at least one referred signup) and with a paying customer.
2. Join to money. For each referred customer, check the Stripe subscription (`stripe_search_customers`, `stripe_list_customer_subscriptions`) and the referral on the checkout. A paying customer whose signup carried a referral that is missing in the platform is leakage: report it to the CFO and the revenue role.
3. Join to first-party data: registrations with an affiliate referral, a UTM source, a paid click id, or nothing. Platform referral counts and first-party registrations will differ (blockers, consent, cookie expiry). Show both and name the cause.
4. Tagging audit. Proposed convention:
   - utm_source: the partner or affiliate slug.
   - utm_medium: affiliate for affiliates; referral or partner for partners.
   - utm_campaign: identical across platforms.
   Compare with what affiliates use (`affonso_list_promotion_urls`, `affonso_get_tracking_settings`) and what arrives (`ga4_run_report` by session source and medium). List untagged or inconsistent links.
5. Unmapped referrers: if they exceed the team's threshold (default: 10 percent of sessions), propose channel rules to engineering.
6. Partners: for each signed partner, count registrations and paying customers from their links in the window. Share a partner's metrics only with that partner's written approval.
7. Quality flags for the CFO's commission check: self-referrals (shared email or domain), existing accounts credited as new, one person behind several accounts.
8. Save with `excom_save_draft`. Record active affiliates, attributed registrations and attributed paying customers with `excom_record_measurement`. Send tagging fixes to the CMO and leakage and exclusions to the CFO (`excom_send_handoff`).

## Output

```text
Attribution audit, window <dates>
Affiliates: enrolled | active (1+ referred signup) | with a paying customer
| Source | Clicks | Registrations (first-party) | Registrations (platform) | Paying (Stripe) | Gap, cause |
Leakage | Tagging issues | Unmapped referrers share | Exclusion flags
```

## Approvals

- Changing tracking settings, promotion links, referrals or coupons (`affonso_update_tracking_settings`, `affonso_create_referral`, `affonso_update_referral`) is a record write, and asks. Those systems belong to the revenue role or the CFO.
- Changing GA4 settings or channel groups is a record write, and asks.
- Sending numbers to an affiliate or partner is a send, and asks.

## Example

Acme has 64 affiliates enrolled, 19 active and 7 with a paying customer. Two customers paid through links carrying a referral that the platform never recorded: leakage, sent to the CFO and CRO. A newsletter link arrives as "Newsletter / email" instead of the affiliate medium: tagging fix sent to the CMO.

Adapted from TerminalSkills/skills (skills/analytics-tracking/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
