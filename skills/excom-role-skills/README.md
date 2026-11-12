# EXCOM role skills

Generic domain skills for AI executives, one folder per role, one skill per recurring job. They are the role skill packs Melaya EXCOM ships built in, published here for any agent: every skill reads the company's own goals, terms and definitions from its knowledge base at run time instead of hardcoding them.

Each skill is `<role>/<skill>/SKILL.md` (frontmatter `name`, `description`, `version`; sections Look up first, Steps, Output, Approvals, Example) with optional `references/` files loaded on demand. `<role>/pack.json` holds the EXCOM metadata (title, prompt hint, the roles it is suggested for, icon, category, source). The router is [SKILL.md](SKILL.md).

## Install

Copy this folder into your agent's skills folder (for Claude Code, `~/.claude/skills/excom-role-skills`), or add a single role skill's `SKILL.md` as a project instruction. Tool ids in the steps are Melaya MCP and connector tools; with another platform, map them to the equivalent tools.

## Index

| Role | Skill | What it is for | Adapted from |
|---|---|---|---|
| ceo | [Build your company knowledge vault](ceo/ceo-company-knowledge-vault/SKILL.md) | no vault yet? build and attach one | Adapted from kepano/obsidian-skills obsidian-markdown and obsidian-headless by Steph Ango (MIT), modified |
| ceo | [Decision memo](ceo/ceo-decision-memo/SKILL.md) | options, trade-offs, reversibility | Adapted from knowledge-work-plugins product-management/skills/stakeholder-update (decision records) by Anthropic (Apache-2.0), modified |
| ceo | [Goal tracker](ceo/ceo-goal-tracker/SKILL.md) | outcomes vs target, leading signals | Adapted from TerminalSkills skills/okr-planning by terminal-skills (Apache-2.0), modified |
| ceo | [Priority reset when goals slip](ceo/ceo-priority-reset/SKILL.md) | goal slipping, stop and start | Adapted from claude-skills c-level-advisor/skills/strategic-alignment by Alireza Rezvani (MIT), modified |
| ceo | [Investor and stakeholder update](ceo/ceo-stakeholder-update/SKILL.md) | investor update draft | Adapted from anthropics/skills internal-comms (3P updates) and knowledge-work-plugins product-management/skills/stakeholder-update by Anthropic (Apache-2.0), modified |
| ceo | [Strategic bet review](ceo/ceo-strategic-bet-review/SKILL.md) | bets, failure signals, kill triggers | Adapted from claude-skills c-level-advisor/skills/scenario-war-room by Alireza Rezvani (MIT), modified |
| ceo | [Cross-executive trade-off log](ceo/ceo-tradeoff-log/SKILL.md) | competing asks, decision record | Adapted from claude-skills c-level-advisor/skills/decision-logger by Alireza Rezvani (MIT), modified |
| ceo | [Weekly board brief](ceo/ceo-weekly-board-brief/SKILL.md) | Monday brief, three decisions | Adapted from claude-skills c-level-advisor/skills/board-meeting by Alireza Rezvani (MIT), modified |
| cfo | [Affiliate commission check](cfo/cfo-affonso-commission-check/SKILL.md) | commissions vs paid Stripe invoices | Adapted from knowledge-work-plugins finance/skills/reconciliation by Anthropic (Apache-2.0), modified |
| cfo | [Cash and runway, 13-week view](cfo/cfo-cash-runway-13-week/SKILL.md) | 13-week cash, runway, risks | Adapted from knowledge-work-plugins small-business/skills/cash-flow-snapshot by Anthropic (Apache-2.0), modified |
| cfo | [Model and infrastructure cost watch](cfo/cfo-model-cost-watch/SKILL.md) | model, API and infra cost | Adapted from TerminalSkills skills/llm-cost-optimizer by terminal-skills (Apache-2.0), modified |
| cfo | [Monthly close checklist](cfo/cfo-monthly-close/SKILL.md) | month-end close, day by day | Adapted from knowledge-work-plugins finance/skills/close-management by Anthropic (Apache-2.0), modified |
| cfo | [Pricing change impact](cfo/cfo-pricing-change-impact/SKILL.md) | price change effect, migration | Adapted from TerminalSkills skills/pricing-strategy by terminal-skills (Apache-2.0), modified |
| cfo | [Spend review](cfo/cfo-spend-review/SKILL.md) | spend vs budget, every spend asks | Adapted from knowledge-work-plugins finance/skills/variance-analysis by Anthropic (Apache-2.0), modified |
| cfo | [Stripe collections and failed payments](cfo/cfo-stripe-collections/SKILL.md) | failed payments, dunning drafts | Adapted from knowledge-work-plugins small-business/skills/invoice-chase by Anthropic (Apache-2.0), modified |
| cfo | [Unit economics per product and plan](cfo/cfo-unit-economics/SKILL.md) | margins, payback, LTV per product | Adapted from claude-skills finance/skills/saas-metrics-coach by Alireza Rezvani (MIT), modified |
| cro | [Demo and call prep brief](cro/cro-call-prep/SKILL.md) | one-page brief before a call | Adapted from gtmagents/gtm-agents plugins/sales-calls/skills/call-brief-framework (Apache-2.0), modified |
| cro | [Follow-up cadence without spam](cro/cro-follow-up-cadence/SKILL.md) | sequenced follow-ups, never spam | Adapted from gtmagents/gtm-agents plugins/email-sequence-orchestration/skills/cadence-design (Apache-2.0), modified |
| cro | [Inbound replies from the answer library](cro/cro-inbound-answer-library/SKILL.md) | draft replies from approved answers | Adapted from stephenrogan/csm-skills skills/objection-handler (MIT), modified |
| cro | [Lead qualification by fit and intent](cro/cro-lead-qualification/SKILL.md) | fit and intent score per product | Adapted from gtmagents/gtm-agents plugins/sales-prospecting/skills/lead-qualification (Apache-2.0), modified |
| cro | [Weekly pipeline review and forecast](cro/cro-pipeline-forecast/SKILL.md) | weekly review with a goal forecast | Adapted from gtmagents/gtm-agents plugins/sales-pipeline/skills/forecast-discipline (Apache-2.0), modified |
| cro | [Pricing and plan fit](cro/cro-pricing-plan-fit/SKILL.md) | map a need to one plan or product | Adapted from gtmagents/gtm-agents plugins/pricing-strategy/skills/packaging-framework (Apache-2.0), modified |
| cro | [Trial-to-paid conversion](cro/cro-trial-to-paid/SKILL.md) | upgrade moments from usage and billing | Adapted from coreyhaines31/marketingskills skills/paywalls (MIT), modified |
| cro | [Win-loss notes](cro/cro-win-loss-notes/SKILL.md) | why deals are won or lost | Adapted from LMTYdotcom/skills skills/competitive-win-loss-analysis (MIT) and gtmagents/gtm-agents plugins/competitive-intelligence/skills/win-loss-dataset (Apache-2.0), modified |
| cmo | [Affiliate recruiting and activation on Affonso](cmo/cmo-affiliate-recruiting/SKILL.md) | recruit and activate Affonso affiliates | Adapted from coreyhaines31/marketingskills skills/referrals and skills/influencer-marketing (MIT), modified (generic) |
| cmo | [AI search visibility report](cmo/cmo-ai-search-visibility/SKILL.md) | GEO visibility brief, no paid tracker | Adapted from Illyism/seo-skills seo/ai-seo-report (MIT) and coreyhaines31/marketingskills skills/ai-seo (MIT), modified (generic) |
| cmo | [Refresh a post or guide that slipped](cmo/cmo-blog-refresher/SKILL.md) | refresh slipping posts and guides | Adapted from Illyism/seo-skills seo/blog-refresher (MIT), modified (generic) |
| cmo | [Build in public from shipped work](cmo/cmo-build-in-public/SKILL.md) | progress posts from shipped work | Adapted from coreyhaines31/marketingskills skills/social/references/ship-post.md (MIT), modified (generic) |
| cmo | [Content coverage map](cmo/cmo-content-coverage/SKILL.md) | topic gaps against queries and rivals | Adapted from Illyism/seo-skills seo/content-coverage (MIT), modified (generic) |
| cmo | [Directory and registry submissions](cmo/cmo-directory-submissions/SKILL.md) | free directory and MCP listings | Adapted from Illyism/seo-skills seo/directory-submissions (MIT), modified (generic) |
| cmo | [Honest backlink outreach](cmo/cmo-honest-link-outreach/SKILL.md) | earn links, never buy them | Adapted from Illyism/seo-skills seo/honest-link-outreach (MIT), modified (generic) |
| cmo | [Internal linking plan](cmo/cmo-internal-linking/SKILL.md) | route link equity to money pages | Adapted from Illyism/seo-skills seo/internal-linking (MIT), modified (generic) |
| cmo | [Reddit threads that rank for buying queries](cmo/cmo-reddit-serp/SKILL.md) | ranking Reddit threads, draft replies | Adapted from Illyism/seo-skills seo/reddit-serp (MIT), modified (generic) |
| cmo | [Title and snippet fixes for click-through](cmo/cmo-seo-title-optimization/SKILL.md) | CTR fixes from striking distance | Adapted from Illyism/seo-skills seo/seo-title-optimization (MIT), modified (generic) |
| cmo | [Weekly social content engine](cmo/cmo-social-engine/SKILL.md) | plan, draft, publish, route inbound | Adapted from coreyhaines31/marketingskills skills/social (MIT), modified (generic) |
| cmo | [De-slop copy for brand voice and answer engines](cmo/cmo-unslop-copy/SKILL.md) | remove AI tells, answer first | Adapted from Illyism/seo-skills content/unslop-seo (MIT), modified (generic) |
| cmo | [Comparison and alternatives pages](cmo/cmo-vs-alternatives/SKILL.md) | honest /vs and alternative pages | Adapted from Illyism/seo-skills seo/vs-and-alternatives (MIT), modified (generic) |
| cmo | [Weekly SEO review loop](cmo/cmo-weekly-seo-review/SKILL.md) | Tuesday GSC, Bing and CWV review | in-house |
| cmo | [YouTube metadata that ranks](cmo/cmo-youtube-seo/SKILL.md) | titles, chapters, key moments | Adapted from Illyism/seo-skills content/youtube-seo (MIT), modified (generic) |
| coo | [Account and API key setup](coo/coo-account-key-setup/SKILL.md) | new provider account and keys | in-house |
| coo | [Handoff delay audit](coo/coo-handoff-delay-audit/SKILL.md) | slowest handoffs, measured | Adapted from claude-skills business-operations/skills/process-mapper by Alireza Rezvani (MIT), modified |
| coo | [Turn repeated work into a pipeline](coo/coo-repeat-work-to-pipeline/SKILL.md) | repeats to managed pipeline | Adapted from knowledge-work-plugins operations/skills/process-optimization by Anthropic (Apache-2.0), modified |
| coo | [Runbook upkeep](coo/coo-runbook-upkeep/SKILL.md) | stale runbooks, refresh from reality | Adapted from knowledge-work-plugins operations/skills/runbook by Anthropic (Apache-2.0), modified |
| coo | [Service-level misses](coo/coo-service-level-misses/SKILL.md) | SLA misses, severity, postmortem | Adapted from knowledge-work-plugins engineering/skills/incident-response by Anthropic (Apache-2.0), modified |
| coo | [Vendor and tool inventory](coo/coo-vendor-tool-inventory/SKILL.md) | vendors, tools, renewals, risk | Adapted from knowledge-work-plugins operations/skills/vendor-review by Anthropic (Apache-2.0), modified |
| coo | [Weekly operations review](coo/coo-weekly-ops-review/SKILL.md) | Friday ops report, red items first | Adapted from knowledge-work-plugins operations/skills/status-report by Anthropic (Apache-2.0), modified |
| cto | [Coding session hygiene](cto/cto-coding-session-hygiene/SKILL.md) | small diffs, test first, evidence | Adapted from obra/superpowers skills/test-driven-development and skills/verification-before-completion (MIT), modified |
| cto | [Cost and performance watch](cto/cto-cost-performance-watch/SKILL.md) | measure spend and latency first | Adapted from alirezarezvani/claude-skills engineering/llm-cost-optimizer/skills/llm-cost-optimizer and engineering/skills/performance-profiler (MIT), modified |
| cto | [Monitor, fix, deploy, verify loop](cto/cto-fix-deploy-verify-loop/SKILL.md) | monitored error to verified fix | in-house |
| cto | [Incident root cause](cto/cto-incident-root-cause/SKILL.md) | root cause before any fix | Adapted from obra/superpowers skills/systematic-debugging (MIT), modified |
| cto | [Safe deploy through CI](cto/cto-jenkins-safe-deploy/SKILL.md) | one job at a time, verified | in-house |
| cto | [Partner go-live](cto/cto-partner-go-live/SKILL.md) | signed partner to live pages | in-house |
| cto | [Post-incident review](cto/cto-post-incident-review/SKILL.md) | blameless review within 72 hours | Adapted from alirezarezvani/claude-skills engineering-team/skills/incident-commander (MIT), modified |
| cto | [Push review and gate](cto/cto-push-review-gate/SKILL.md) | review a session before push | Adapted from alirezarezvani/claude-skills engineering/skills/pr-review-expert and obra/superpowers skills/requesting-code-review (MIT), modified |
| cto | [Runner release and model provider change](cto/cto-runner-provider-change/SKILL.md) | all pins together, publish then deploy | in-house |
| cpo | [Acceptance criteria for a change](cpo/cpo-acceptance-criteria/SKILL.md) | scenario and passing result table | Adapted from phuryn/pm-skills pm-execution/skills/test-scenarios (MIT), modified |
| cpo | [Feature adoption readout](cpo/cpo-adoption-readout/SKILL.md) | did the shipped feature get used | Adapted from phuryn/pm-skills pm-data-analytics/skills/cohort-analysis (MIT), modified |
| cpo | [AI crawler policy, bot by bot](cpo/cpo-ai-crawler-policy/SKILL.md) | per-bot AI crawler decisions | Adapted from Illyism/seo-skills seo/block-ai-scrapers (MIT), modified |
| cpo | [Code a change and hand it to the CTO](cpo/cpo-code-session-handoff/SKILL.md) | code, commit, hand over to push | in-house |
| cpo | [Keep public and in-app docs true](cpo/cpo-docs-upkeep/SKILL.md) | docs match the product, every language | in-house |
| cpo | [Internal links in the client code](cpo/cpo-internal-links-code/SKILL.md) | link components and related links | Adapted from Illyism/seo-skills seo/internal-linking (MIT), modified |
| cpo | [Release notes from what shipped](cpo/cpo-release-notes/SKILL.md) | user-facing notes from commits | Adapted from phuryn/pm-skills pm-execution/skills/release-notes (MIT), modified |
| cpo | [Roadmap from weighted evidence](cpo/cpo-roadmap-from-evidence/SKILL.md) | rank asks by weighted evidence | Adapted from phuryn/pm-skills pm-product-discovery/skills/analyze-feature-requests and prioritize-features (MIT), modified |
| cpo | [SEO fixes in a coding session](cpo/cpo-seo-autopilot/SKILL.md) | fix SEO findings in client code | Adapted from Illyism/seo-skills seo/seo-autopilot (MIT), modified |
| cpo | [Technical SEO roast of the site](cpo/cpo-seo-roast/SKILL.md) | fatal-first technical SEO audit | Adapted from Illyism/seo-skills seo/seo-roast (MIT), modified |
| cxo | [Activation paths per product](cxo/cxo-activation-paths/SKILL.md) | first-success path for each product | Adapted from gtmagents/gtm-agents plugins/product-led-growth/skills/onboarding-blueprint (Apache-2.0), modified |
| cxo | [Customer interviews](cxo/cxo-customer-interviews/SKILL.md) | recruit, script and synthesise interviews | Adapted from coreyhaines31/marketingskills skills/customer-research (MIT) and gtmagents/gtm-agents plugins/customer-feedback-orchestration/skills/survey-design (Apache-2.0), modified |
| cxo | [Feedback loop to the CPO](cxo/cxo-feedback-to-cpo/SKILL.md) | tagged customer insights for the CPO | Adapted from gtmagents/gtm-agents plugins/customer-feedback-orchestration/skills/insight-synthesis and plugins/voice-of-customer/skills/customer-feedback-taxonomy (Apache-2.0), modified |
| cxo | [Churn and health signals](cxo/cxo-health-signals/SKILL.md) | account health score and interventions | Adapted from coreyhaines31/marketingskills skills/churn-prevention (MIT) and gtmagents/gtm-agents plugins/customer-success/skills/risk-scoring-framework (Apache-2.0), modified |
| cxo | [Help-docs gaps](cxo/cxo-help-docs-gaps/SKILL.md) | find and fix missing help docs | Adapted from gtmagents/gtm-agents plugins/technical-writing/skills/doc-requirements-matrix (Apache-2.0), modified |
| cxo | [Onboarding email sequence](cxo/cxo-onboarding-emails/SKILL.md) | behaviour-triggered onboarding drafts | Adapted from coreyhaines31/marketingskills skills/onboarding (MIT), modified |
| cxo | [Support macros from the answer library](cxo/cxo-support-macros/SKILL.md) | vetted answers for repeat questions | Adapted from gtmagents/gtm-agents plugins/technical-writing/skills/quality-review-checklist (Apache-2.0), modified |
| cxo | [Trial rescue for stalled users](cxo/cxo-trial-rescue/SKILL.md) | rescue stalled trials, then stop | Adapted from stephenrogan/csm-skills skills/re-engagement-email-writer (MIT), modified |
| cdo | [Affiliate and partner attribution](cdo/cdo-affiliate-attribution/SKILL.md) | who brought which customer | Adapted from TerminalSkills skills/analytics-tracking by terminal-skills (Apache-2.0), modified |
| cdo | [Dashboard upkeep](cdo/cdo-dashboard-upkeep/SKILL.md) | dashboards stay true and current | Adapted from knowledge-work-plugins data/skills/build-dashboard by Anthropic (Apache-2.0), modified |
| cdo | [Data quality checks](cdo/cdo-data-quality-checks/SKILL.md) | check numbers before they ship | Adapted from knowledge-work-plugins data/skills/validate-data by Anthropic (Apache-2.0), modified |
| cdo | [Experiment readout](cdo/cdo-experiment-readout/SKILL.md) | test plan, power, readout | Adapted from TerminalSkills skills/ab-test-setup and knowledge-work-plugins data/skills/statistical-analysis (Apache-2.0), modified |
| cdo | [Metric definitions, one source per KPI](cdo/cdo-metric-definitions/SKILL.md) | one definition and source per KPI | Adapted from claude-skills c-level-advisor/skills/chief-data-officer-advisor by Alireza Rezvani (MIT), modified |
| cdo | [Privacy-safe data handling](cdo/cdo-privacy-safe-data/SKILL.md) | personal data, consent, retention | Adapted from TerminalSkills skills/gdpr-compliance by terminal-skills (Apache-2.0), modified |
| cdo | [Funnel analytics per product](cdo/cdo-product-funnel/SKILL.md) | per-product funnel, bottleneck | Adapted from TerminalSkills skills/product-analytics by terminal-skills (Apache-2.0), modified |
| chro | [Affiliate and community contributor support](chro/chro-affiliate-community-support/SKILL.md) | affiliates, community tiers, contributors | in-house |
| chro | [Contractor and freelancer management](chro/chro-contractor-management/SKILL.md) | contractor register, renewals, exits | Adapted from tuanductran/hr-skills hr-contingent-workforce (MIT), modified |
| chro | [Hiring brief and job description](chro/chro-hiring-brief/SKILL.md) | role brief and fair job description | Adapted from sara-hamza/people-ops-claude job-description-builder and JordzPope/claude-skills-hiring-interviews hiring-manager-intake, essential-criteria-review (MIT), modified |
| chro | [Interview loop and scorecards](chro/chro-interview-loop/SKILL.md) | structured interviews, scorecards, debrief | Adapted from anthropics/knowledge-work-plugins human-resources/skills/interview-prep (Apache-2.0) and JordzPope/claude-skills-hiring-interviews structured-interview-guide, decision-record (MIT), modified |
| chro | [Onboarding plan for a hire or contractor](chro/chro-onboarding-plan/SKILL.md) | onboarding checklist with access evidence | Adapted from anthropics/knowledge-work-plugins human-resources/skills/onboarding (Apache-2.0) and sara-hamza/people-ops-claude onboarding-planner (MIT), modified |
| chro | [People policy upkeep](chro/chro-people-policy-upkeep/SKILL.md) | review dates, redrafts, plain answers | Adapted from sara-hamza/people-ops-claude policy-drafter (MIT) and anthropics/knowledge-work-plugins human-resources/skills/policy-lookup (Apache-2.0), modified |
| chro | [Candidate screening rubric](chro/chro-screening-rubric/SKILL.md) | fair documented screening rubric | Adapted from JordzPope/claude-skills-hiring-interviews scoring-guide, question-fairness-check and sara-hamza/people-ops-claude redact-hr-data (MIT), modified |
| chro | [Team rhythm and workload health](chro/chro-team-rhythm-workload/SKILL.md) | approval load and weekly rhythm check | Adapted from tuanductran/hr-skills hr-wellbeing (MIT) and anthropics/knowledge-work-plugins human-resources/skills/people-report (Apache-2.0), modified |
| ciso | [Access review](ciso/ciso-access-review/SKILL.md) | who has access and should they | Adapted from mukul975/Anthropic-Cybersecurity-Skills skills/performing-access-review-and-certification (Apache-2.0), modified |
| ciso | [Compliance evidence catalogue](ciso/ciso-compliance-evidence/SKILL.md) | controls mapped to dated evidence | Adapted from alirezarezvani/claude-skills ra-qm-team/skills/soc2-compliance (MIT), modified |
| ciso | [Security incident first hour](ciso/ciso-incident-first-hour/SKILL.md) | declare, preserve, contain, clocks | Adapted from mukul975/Anthropic-Cybersecurity-Skills skills/triaging-security-incident (Apache-2.0), modified |
| ciso | [Phishing and mailbox safety](ciso/ciso-phishing-mailbox-safety/SKILL.md) | suspicious mail and mailbox rules | Adapted from mukul975/Anthropic-Cybersecurity-Skills skills/conducting-phishing-incident-response (Apache-2.0), modified |
| ciso | [Security questionnaire answers](ciso/ciso-questionnaire-answers/SKILL.md) | sourced answers, no overclaiming | in-house |
| ciso | [Secrets hygiene and rotation plan](ciso/ciso-secrets-hygiene/SKILL.md) | leaks, rotation, never show values | Adapted from alirezarezvani/claude-skills engineering/skills/env-secrets-manager (MIT), modified |
| ciso | [Vendor security review](ciso/ciso-vendor-security-review/SKILL.md) | tier, evidence, residual risk | Adapted from mukul975/Anthropic-Cybersecurity-Skills skills/managing-third-party-vendor-risk (Apache-2.0), modified |
| ciso | [Vulnerability and dependency triage](ciso/ciso-vuln-dependency-triage/SKILL.md) | exploited first, fix order with deadlines | Adapted from mukul975/Anthropic-Cybersecurity-Skills skills/performing-cve-prioritization-with-kev-catalog (Apache-2.0), modified |
| clo | [Contract review against the playbook](clo/clo-contract-review/SKILL.md) | playbook review, graded redline drafts | Adapted from anthropics/knowledge-work-plugins legal/skills/review-contract (Apache-2.0) and kevanwee/playbook-as-code SKILL.md (MIT), modified |
| clo | [Terms and legal pages upkeep](clo/clo-legal-pages-upkeep/SKILL.md) | legal pages and language parity | in-house |
| clo | [Marketing claims review](clo/clo-marketing-claims-review/SKILL.md) | comparison pages, testimonials, AI-washing | Adapted from anthropics/knowledge-work-plugins legal/skills/legal-risk-assessment (Apache-2.0), modified |
| clo | [Open-source licensing and attribution](clo/clo-oss-licensing-attribution/SKILL.md) | licences, notices, third-party attribution | in-house |
| clo | [Partner and affiliate agreement terms](clo/clo-partner-affiliate-agreements/SKILL.md) | e-signature, programme terms, filing | Adapted from anthropics/knowledge-work-plugins legal/skills/signature-request, vendor-check (Apache-2.0) and Maxbase91/procurement-skills supplier-truthcheck (MIT), modified |
| clo | [Privacy and data-processing requests](clo/clo-privacy-requests/SKILL.md) | DSAR clock, DPA and privacy answers | Adapted from anthropics/knowledge-work-plugins legal/skills/compliance-check, legal-response (Apache-2.0), modified |
| clo | [Regulatory watch](clo/clo-regulatory-watch/SKILL.md) | AI, privacy, platform and store rules | Adapted from anthropics/knowledge-work-plugins operations/skills/compliance-tracking, legal/skills/compliance-check (Apache-2.0), modified |
| cqo | [Bug triage and severity](cqo/cqo-bug-triage-severity/SKILL.md) | reproduce, classify, route a bug | in-house |
| cqo | [Customer-reported defect loop](cqo/cqo-defect-loop/SKILL.md) | root cause to verified prevention | Adapted from alirezarezvani/claude-skills ra-qm-team/skills/capa-officer (MIT), modified |
| cqo | [Docs accuracy check](cqo/cqo-docs-accuracy-check/SKILL.md) | doc claims verified against the product | in-house |
| cqo | [Translation and locale QA](cqo/cqo-locale-qa/SKILL.md) | locale parity and language tag checks | Adapted from alirezarezvani/claude-skills engineering/skills/i18n-localization (MIT), modified |
| cqo | [Pipeline run quality review](cqo/cqo-pipeline-run-quality/SKILL.md) | judge runs by artifacts, not status | in-house |
| cqo | [Regression test plan per product](cqo/cqo-regression-test-plan/SKILL.md) | scenarios, trials and a regression verdict | Adapted from alirezarezvani/claude-skills engineering/skills/agent-regression-evals and phuryn/pm-skills pm-execution/skills/test-scenarios (MIT), modified |
| cqo | [Release quality gate](cqo/cqo-release-quality-gate/SKILL.md) | go or no-go with evidence per row | Adapted from obra/superpowers skills/verification-before-completion (MIT), modified |
| csco | [Monthly supplier spend review](csco/csco-monthly-spend-review/SKILL.md) | supplier spend, anomalies, savings | Adapted from Maxbase91/procurement-skills spend-prism (MIT), modified |
| csco | [Procurement request](csco/csco-procurement-request/SKILL.md) | buy requests, quotes, spend asks | Adapted from Maxbase91/procurement-skills bid-compass (MIT), modified |
| csco | [Provider outage and fallback plan](csco/csco-provider-outage-fallback/SKILL.md) | outage triage and supplier fallbacks | Adapted from anthropics/knowledge-work-plugins operations/skills/runbook, risk-assessment (Apache-2.0), modified |
| csco | [Provider model and price refresh](csco/csco-provider-price-refresh/SKILL.md) | model catalogs, prices, promo expiries | in-house |
| csco | [Cost and contract renewals calendar](csco/csco-renewals-calendar/SKILL.md) | trials, renewals, certificates, expiries | Adapted from anthropics/knowledge-work-plugins legal/skills/vendor-check (Apache-2.0), modified |
| csco | [Vendor and provider inventory](csco/csco-vendor-inventory/SKILL.md) | suppliers, providers, owners, costs | Adapted from anthropics/knowledge-work-plugins operations/skills/vendor-review (Apache-2.0) and Maxbase91/procurement-skills supplier-truthcheck (MIT), modified |
| csco | [Vendor risk review with the CISO](csco/csco-vendor-risk-review/SKILL.md) | periodic supplier risk with the CISO | Adapted from anthropics/knowledge-work-plugins operations/skills/risk-assessment (Apache-2.0) and Maxbase91/procurement-skills supplier-truthcheck (MIT), modified |
| partnerships | [Partner agreement via the DocuSign template](partnerships/partner-agreement-docusign/SKILL.md) | draft, owner sends, file when signed | in-house |
| partnerships | [Co-marketing with partners and the CMO](partnerships/partner-co-marketing/SKILL.md) | joint campaigns with the CMO | Adapted from gtmagents/gtm-agents plugins/partnership-development/skills/co-marketing-governance (Apache-2.0), modified |
| partnerships | [Partner enablement](partnerships/partner-enablement/SKILL.md) | talk tracks, demos, reinforcement | Adapted from gtmagents/gtm-agents plugins/sales-handoff-orchestration/skills/enablement-kit and plugins/sales-enablement/skills/reinforcement-loop (Apache-2.0), modified |
| partnerships | [Marketplace and launch-community listings](partnerships/partner-marketplace-listings/SKILL.md) | marketplaces, registries, launch sites | Adapted from coreyhaines31/marketingskills skills/directory-submissions (MIT), modified |
| partnerships | [Partner onboarding kit](partnerships/partner-onboarding-kit/SKILL.md) | kit, tracking link, first action | Adapted from gtmagents/gtm-agents plugins/referral-program-orchestration/skills/partner-ops (Apache-2.0), modified |
| partnerships | [Partner pipeline review against the goal](partnerships/partner-pipeline-review/SKILL.md) | weekly review, signed means filed | Adapted from gtmagents/gtm-agents plugins/partnership-development/skills/partner-revenue-desk (Apache-2.0), modified |
| partnerships | [Integrator and agency programme offer](partnerships/partner-programme-offer/SKILL.md) | recruit with the standing programme tiers | Adapted from gtmagents/gtm-agents plugins/referral-program-orchestration/skills/incentive-design (Apache-2.0), modified |
| partnerships | [Partner sourcing list](partnerships/partner-sourcing-list/SKILL.md) | ranked list of partners to approach | Adapted from gtmagents/gtm-agents plugins/partnership-development/skills/partner-ecosystem-map (Apache-2.0), modified |

## Credits and licences

Many skills adapt open-source agent skills, rewritten for EXCOM (generic company facts, exact tool ids, approval rules; scripts and install steps removed). Every adapted skill names its source in its last line and in `pack.json`, and each role folder's `THIRD_PARTY.txt` records the repository, commit, licence, original path and changes, with the full licence texts. Only permissive licences are used (MIT, Apache-2.0).

| Repository | Roles |
|---|---|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | ceo, cfo, coo, cto, cdo, ciso, cqo |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | ceo, cfo, coo, cdo, chro, clo, csco |
| [anthropics/skills](https://github.com/anthropics/skills) | ceo |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | cro, cmo, cxo, partnerships |
| [gtmagents/gtm-agents](https://github.com/gtmagents/gtm-agents) | cro, cxo, partnerships |
| [Illyism/seo-skills](https://github.com/Illyism/seo-skills) | cmo, cpo |
| [JordzPope/claude-skills-hiring-interviews](https://github.com/JordzPope/claude-skills-hiring-interviews) | chro |
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | ceo |
| [kevanwee/playbook-as-code](https://github.com/kevanwee/playbook-as-code) | clo |
| [LMTYdotcom/skills](https://github.com/LMTYdotcom/skills) | cro |
| [Maxbase91/procurement-skills](https://github.com/Maxbase91/procurement-skills) | clo, csco |
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | ciso |
| [obra/superpowers](https://github.com/obra/superpowers) | cto, cqo |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | cpo, cqo |
| [sara-hamza/people-ops-claude](https://github.com/sara-hamza/people-ops-claude) | chro |
| [stephenrogan/csm-skills](https://github.com/stephenrogan/csm-skills) | cro, cxo |
| [TerminalSkills/skills](https://github.com/TerminalSkills/skills) | ceo, cfo, cdo |
| [tuanductran/hr-skills](https://github.com/tuanductran/hr-skills) | chro |
