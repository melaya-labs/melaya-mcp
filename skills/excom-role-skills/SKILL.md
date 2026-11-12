---
name: excom-role-skills
description: Domain playbooks for AI executives (CEO, CFO, CRO, CMO, COO, CTO, CPO, customer, data, people, security, legal, quality, supply chain, partnerships): one skill per recurring job, each with what to look up in your company's knowledge first, exact tool ids, approvals and an example. Use when acting as or for an executive role, when running an EXCOM team, or when asked for a board brief, pipeline review, SEO plan, incident root cause, cash view, contract review or any role routine, even if no skill is named.
version: 2.0.0
---

# EXCOM role skills

One playbook per recurring executive job, grouped by role. Each is generic: it reads your company's goals, terms and definitions from your knowledge base at run time and asks when something is missing, so it works for any company.

## How to use

1. Pick the role folder that owns the work (table below), then the skill whose line matches the task.
2. Open `<role>/<skill>/SKILL.md` and follow it. Open a `references/` file only when the skill says so.
3. Do its **Look up first** step before anything else: the facts it needs come from your team's goals, your charter and your knowledge base, never from memory.
4. Respect its **Approvals** section: sending, spending money and production changes always wait for a human.

In Melaya EXCOM these skills ship built in: each executive carries its role's pack, loads one with `excom_skill_load`, and the owner can switch any of them off.

## Skills by role

### ceo (Chief Executive Officer)

- [ceo-company-knowledge-vault](ceo/ceo-company-knowledge-vault/SKILL.md): no vault yet? build and attach one
- [ceo-decision-memo](ceo/ceo-decision-memo/SKILL.md): options, trade-offs, reversibility
- [ceo-goal-tracker](ceo/ceo-goal-tracker/SKILL.md): outcomes vs target, leading signals
- [ceo-priority-reset](ceo/ceo-priority-reset/SKILL.md): goal slipping, stop and start
- [ceo-stakeholder-update](ceo/ceo-stakeholder-update/SKILL.md): investor update draft
- [ceo-strategic-bet-review](ceo/ceo-strategic-bet-review/SKILL.md): bets, failure signals, kill triggers
- [ceo-tradeoff-log](ceo/ceo-tradeoff-log/SKILL.md): competing asks, decision record
- [ceo-weekly-board-brief](ceo/ceo-weekly-board-brief/SKILL.md): Monday brief, three decisions

### cfo (Chief Financial Officer)

- [cfo-affonso-commission-check](cfo/cfo-affonso-commission-check/SKILL.md): commissions vs paid Stripe invoices
- [cfo-cash-runway-13-week](cfo/cfo-cash-runway-13-week/SKILL.md): 13-week cash, runway, risks
- [cfo-model-cost-watch](cfo/cfo-model-cost-watch/SKILL.md): model, API and infra cost
- [cfo-monthly-close](cfo/cfo-monthly-close/SKILL.md): month-end close, day by day
- [cfo-pricing-change-impact](cfo/cfo-pricing-change-impact/SKILL.md): price change effect, migration
- [cfo-spend-review](cfo/cfo-spend-review/SKILL.md): spend vs budget, every spend asks
- [cfo-stripe-collections](cfo/cfo-stripe-collections/SKILL.md): failed payments, dunning drafts
- [cfo-unit-economics](cfo/cfo-unit-economics/SKILL.md): margins, payback, LTV per product

### cro (Chief Revenue Officer)

- [cro-call-prep](cro/cro-call-prep/SKILL.md): one-page brief before a call
- [cro-follow-up-cadence](cro/cro-follow-up-cadence/SKILL.md): sequenced follow-ups, never spam
- [cro-inbound-answer-library](cro/cro-inbound-answer-library/SKILL.md): draft replies from approved answers
- [cro-lead-qualification](cro/cro-lead-qualification/SKILL.md): fit and intent score per product
- [cro-pipeline-forecast](cro/cro-pipeline-forecast/SKILL.md): weekly review with a goal forecast
- [cro-pricing-plan-fit](cro/cro-pricing-plan-fit/SKILL.md): map a need to one plan or product
- [cro-trial-to-paid](cro/cro-trial-to-paid/SKILL.md): upgrade moments from usage and billing
- [cro-win-loss-notes](cro/cro-win-loss-notes/SKILL.md): why deals are won or lost

### cmo (Chief Marketing Officer)

- [cmo-affiliate-recruiting](cmo/cmo-affiliate-recruiting/SKILL.md): recruit and activate Affonso affiliates
- [cmo-ai-search-visibility](cmo/cmo-ai-search-visibility/SKILL.md): GEO visibility brief, no paid tracker
- [cmo-blog-refresher](cmo/cmo-blog-refresher/SKILL.md): refresh slipping posts and guides
- [cmo-build-in-public](cmo/cmo-build-in-public/SKILL.md): progress posts from shipped work
- [cmo-content-coverage](cmo/cmo-content-coverage/SKILL.md): topic gaps against queries and rivals
- [cmo-directory-submissions](cmo/cmo-directory-submissions/SKILL.md): free directory and MCP listings
- [cmo-honest-link-outreach](cmo/cmo-honest-link-outreach/SKILL.md): earn links, never buy them
- [cmo-internal-linking](cmo/cmo-internal-linking/SKILL.md): route link equity to money pages
- [cmo-reddit-serp](cmo/cmo-reddit-serp/SKILL.md): ranking Reddit threads, draft replies
- [cmo-seo-title-optimization](cmo/cmo-seo-title-optimization/SKILL.md): CTR fixes from striking distance
- [cmo-social-engine](cmo/cmo-social-engine/SKILL.md): plan, draft, publish, route inbound
- [cmo-unslop-copy](cmo/cmo-unslop-copy/SKILL.md): remove AI tells, answer first
- [cmo-vs-alternatives](cmo/cmo-vs-alternatives/SKILL.md): honest /vs and alternative pages
- [cmo-weekly-seo-review](cmo/cmo-weekly-seo-review/SKILL.md): Tuesday GSC, Bing and CWV review
- [cmo-youtube-seo](cmo/cmo-youtube-seo/SKILL.md): titles, chapters, key moments

### coo (Chief Operating Officer)

- [coo-account-key-setup](coo/coo-account-key-setup/SKILL.md): new provider account and keys
- [coo-handoff-delay-audit](coo/coo-handoff-delay-audit/SKILL.md): slowest handoffs, measured
- [coo-repeat-work-to-pipeline](coo/coo-repeat-work-to-pipeline/SKILL.md): repeats to managed pipeline
- [coo-runbook-upkeep](coo/coo-runbook-upkeep/SKILL.md): stale runbooks, refresh from reality
- [coo-service-level-misses](coo/coo-service-level-misses/SKILL.md): SLA misses, severity, postmortem
- [coo-vendor-tool-inventory](coo/coo-vendor-tool-inventory/SKILL.md): vendors, tools, renewals, risk
- [coo-weekly-ops-review](coo/coo-weekly-ops-review/SKILL.md): Friday ops report, red items first

### cto (Chief Technology Officer)

- [cto-coding-session-hygiene](cto/cto-coding-session-hygiene/SKILL.md): small diffs, test first, evidence
- [cto-cost-performance-watch](cto/cto-cost-performance-watch/SKILL.md): measure spend and latency first
- [cto-fix-deploy-verify-loop](cto/cto-fix-deploy-verify-loop/SKILL.md): monitored error to verified fix
- [cto-incident-root-cause](cto/cto-incident-root-cause/SKILL.md): root cause before any fix
- [cto-jenkins-safe-deploy](cto/cto-jenkins-safe-deploy/SKILL.md): one job at a time, verified
- [cto-partner-go-live](cto/cto-partner-go-live/SKILL.md): signed partner to live pages
- [cto-post-incident-review](cto/cto-post-incident-review/SKILL.md): blameless review within 72 hours
- [cto-push-review-gate](cto/cto-push-review-gate/SKILL.md): review a session before push
- [cto-runner-provider-change](cto/cto-runner-provider-change/SKILL.md): all pins together, publish then deploy

### cpo (Chief Product Officer)

- [cpo-acceptance-criteria](cpo/cpo-acceptance-criteria/SKILL.md): scenario and passing result table
- [cpo-adoption-readout](cpo/cpo-adoption-readout/SKILL.md): did the shipped feature get used
- [cpo-ai-crawler-policy](cpo/cpo-ai-crawler-policy/SKILL.md): per-bot AI crawler decisions
- [cpo-code-session-handoff](cpo/cpo-code-session-handoff/SKILL.md): code, commit, hand over to push
- [cpo-docs-upkeep](cpo/cpo-docs-upkeep/SKILL.md): docs match the product, every language
- [cpo-internal-links-code](cpo/cpo-internal-links-code/SKILL.md): link components and related links
- [cpo-release-notes](cpo/cpo-release-notes/SKILL.md): user-facing notes from commits
- [cpo-roadmap-from-evidence](cpo/cpo-roadmap-from-evidence/SKILL.md): rank asks by weighted evidence
- [cpo-seo-autopilot](cpo/cpo-seo-autopilot/SKILL.md): fix SEO findings in client code
- [cpo-seo-roast](cpo/cpo-seo-roast/SKILL.md): fatal-first technical SEO audit

### cxo (Chief Customer Officer)

- [cxo-activation-paths](cxo/cxo-activation-paths/SKILL.md): first-success path for each product
- [cxo-customer-interviews](cxo/cxo-customer-interviews/SKILL.md): recruit, script and synthesise interviews
- [cxo-feedback-to-cpo](cxo/cxo-feedback-to-cpo/SKILL.md): tagged customer insights for the CPO
- [cxo-health-signals](cxo/cxo-health-signals/SKILL.md): account health score and interventions
- [cxo-help-docs-gaps](cxo/cxo-help-docs-gaps/SKILL.md): find and fix missing help docs
- [cxo-onboarding-emails](cxo/cxo-onboarding-emails/SKILL.md): behaviour-triggered onboarding drafts
- [cxo-support-macros](cxo/cxo-support-macros/SKILL.md): vetted answers for repeat questions
- [cxo-trial-rescue](cxo/cxo-trial-rescue/SKILL.md): rescue stalled trials, then stop

### cdo (Chief Data Officer)

- [cdo-affiliate-attribution](cdo/cdo-affiliate-attribution/SKILL.md): who brought which customer
- [cdo-dashboard-upkeep](cdo/cdo-dashboard-upkeep/SKILL.md): dashboards stay true and current
- [cdo-data-quality-checks](cdo/cdo-data-quality-checks/SKILL.md): check numbers before they ship
- [cdo-experiment-readout](cdo/cdo-experiment-readout/SKILL.md): test plan, power, readout
- [cdo-metric-definitions](cdo/cdo-metric-definitions/SKILL.md): one definition and source per KPI
- [cdo-privacy-safe-data](cdo/cdo-privacy-safe-data/SKILL.md): personal data, consent, retention
- [cdo-product-funnel](cdo/cdo-product-funnel/SKILL.md): per-product funnel, bottleneck

### chro (Chief People Officer)

- [chro-affiliate-community-support](chro/chro-affiliate-community-support/SKILL.md): affiliates, community tiers, contributors
- [chro-contractor-management](chro/chro-contractor-management/SKILL.md): contractor register, renewals, exits
- [chro-hiring-brief](chro/chro-hiring-brief/SKILL.md): role brief and fair job description
- [chro-interview-loop](chro/chro-interview-loop/SKILL.md): structured interviews, scorecards, debrief
- [chro-onboarding-plan](chro/chro-onboarding-plan/SKILL.md): onboarding checklist with access evidence
- [chro-people-policy-upkeep](chro/chro-people-policy-upkeep/SKILL.md): review dates, redrafts, plain answers
- [chro-screening-rubric](chro/chro-screening-rubric/SKILL.md): fair documented screening rubric
- [chro-team-rhythm-workload](chro/chro-team-rhythm-workload/SKILL.md): approval load and weekly rhythm check

### ciso (Chief Information Security Officer)

- [ciso-access-review](ciso/ciso-access-review/SKILL.md): who has access and should they
- [ciso-compliance-evidence](ciso/ciso-compliance-evidence/SKILL.md): controls mapped to dated evidence
- [ciso-incident-first-hour](ciso/ciso-incident-first-hour/SKILL.md): declare, preserve, contain, clocks
- [ciso-phishing-mailbox-safety](ciso/ciso-phishing-mailbox-safety/SKILL.md): suspicious mail and mailbox rules
- [ciso-questionnaire-answers](ciso/ciso-questionnaire-answers/SKILL.md): sourced answers, no overclaiming
- [ciso-secrets-hygiene](ciso/ciso-secrets-hygiene/SKILL.md): leaks, rotation, never show values
- [ciso-vendor-security-review](ciso/ciso-vendor-security-review/SKILL.md): tier, evidence, residual risk
- [ciso-vuln-dependency-triage](ciso/ciso-vuln-dependency-triage/SKILL.md): exploited first, fix order with deadlines

### clo (Chief Legal Officer)

- [clo-contract-review](clo/clo-contract-review/SKILL.md): playbook review, graded redline drafts
- [clo-legal-pages-upkeep](clo/clo-legal-pages-upkeep/SKILL.md): legal pages and language parity
- [clo-marketing-claims-review](clo/clo-marketing-claims-review/SKILL.md): comparison pages, testimonials, AI-washing
- [clo-oss-licensing-attribution](clo/clo-oss-licensing-attribution/SKILL.md): licences, notices, third-party attribution
- [clo-partner-affiliate-agreements](clo/clo-partner-affiliate-agreements/SKILL.md): e-signature, programme terms, filing
- [clo-privacy-requests](clo/clo-privacy-requests/SKILL.md): DSAR clock, DPA and privacy answers
- [clo-regulatory-watch](clo/clo-regulatory-watch/SKILL.md): AI, privacy, platform and store rules

### cqo (Chief Quality Officer)

- [cqo-bug-triage-severity](cqo/cqo-bug-triage-severity/SKILL.md): reproduce, classify, route a bug
- [cqo-defect-loop](cqo/cqo-defect-loop/SKILL.md): root cause to verified prevention
- [cqo-docs-accuracy-check](cqo/cqo-docs-accuracy-check/SKILL.md): doc claims verified against the product
- [cqo-locale-qa](cqo/cqo-locale-qa/SKILL.md): locale parity and language tag checks
- [cqo-pipeline-run-quality](cqo/cqo-pipeline-run-quality/SKILL.md): judge runs by artifacts, not status
- [cqo-regression-test-plan](cqo/cqo-regression-test-plan/SKILL.md): scenarios, trials and a regression verdict
- [cqo-release-quality-gate](cqo/cqo-release-quality-gate/SKILL.md): go or no-go with evidence per row

### csco (Chief Supply Chain Officer)

- [csco-monthly-spend-review](csco/csco-monthly-spend-review/SKILL.md): supplier spend, anomalies, savings
- [csco-procurement-request](csco/csco-procurement-request/SKILL.md): buy requests, quotes, spend asks
- [csco-provider-outage-fallback](csco/csco-provider-outage-fallback/SKILL.md): outage triage and supplier fallbacks
- [csco-provider-price-refresh](csco/csco-provider-price-refresh/SKILL.md): model catalogs, prices, promo expiries
- [csco-renewals-calendar](csco/csco-renewals-calendar/SKILL.md): trials, renewals, certificates, expiries
- [csco-vendor-inventory](csco/csco-vendor-inventory/SKILL.md): suppliers, providers, owners, costs
- [csco-vendor-risk-review](csco/csco-vendor-risk-review/SKILL.md): periodic supplier risk with the CISO

### partnerships (Partnerships (a partner-channel executive made from the CRO template))

- [partner-agreement-docusign](partnerships/partner-agreement-docusign/SKILL.md): draft, owner sends, file when signed
- [partner-co-marketing](partnerships/partner-co-marketing/SKILL.md): joint campaigns with the CMO
- [partner-enablement](partnerships/partner-enablement/SKILL.md): talk tracks, demos, reinforcement
- [partner-marketplace-listings](partnerships/partner-marketplace-listings/SKILL.md): marketplaces, registries, launch sites
- [partner-onboarding-kit](partnerships/partner-onboarding-kit/SKILL.md): kit, tracking link, first action
- [partner-pipeline-review](partnerships/partner-pipeline-review/SKILL.md): weekly review, signed means filed
- [partner-programme-offer](partnerships/partner-programme-offer/SKILL.md): recruit with the standing programme tiers
- [partner-sourcing-list](partnerships/partner-sourcing-list/SKILL.md): ranked list of partners to approach
