<!-- Reference of the excom module of the melaya skill. Generated from the EXCOM app matrix (role slots) of the Melaya platform, 2026-11-11. -->
# EXCOM roles and the apps each one plans

Each executive plans its apps by capability slot (mailbox, accounting, CRM, ...). A slot lists the apps in priority order; the planner binds at most `cap` connected accounts per slot, read-only by default. "Required" slots are what the role needs to do its job; the others widen it. An app connected later reaches every executive whose role uses it, read-only, when the team allows it (on by default). Apps marked in the product as "Not in Melaya yet" are left out here.

## Chief Executive Officer (CEO)

Department: Leadership.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Mailbox | yes | 1 | gmail, outlook, zoho_mail | Reads the threads behind each decision and drafts your replies. |
| Calendar | no | 1 | google_calendar, outlook | Prepares a short brief for every meeting the evening before. |
| Team chat | no | 2 | slack, microsoft_teams | Follows what the teams discuss and posts the weekly brief where they read it. |
| Documents and wiki | yes | 3 | notion, confluence, google_drive, google_docs, sharepoint, onedrive, obsidian, superhuman_docs | Keeps the strategy, decisions and commitments in your shared workspace. |
| Decks and spreadsheets | no | 2 | google_slides, google_sheets, metabase, looker | Builds the board and investor update from verified numbers. |
| Goals and portfolios | no | 1 | asana | Follows company goals, portfolios and project health without asking each team for an update. |
| Meeting recordings | no | 2 | zoom, google_meet | Turns leadership meetings into minutes with owners and dates. |
| Hiring | no | 1 | greenhouse, lever, ashby | Reads hiring progress for the board: open roles, pipeline by stage, time to hire and offer acceptance. |
| E-signature | no | 1 | docusign | Tracks the board consents and key contracts waiting for a signature. |

## Chief Financial Officer (CFO)

Department: Finance.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Accounting and ERP | yes | 2 | odoo, sap_s4hana, oracle_fusion, quickbooks, xero | Reads invoices, payments and the ledger to collect and reconcile. |
| Payments and billing | no | 2 | stripe, shopify | Reconciles payouts, refunds and disputes with the books. |
| Expenses and purchasing | no | 2 | sap_concur, sap_ariba | Lists every expense report and supplier invoice waiting for approval. |
| Bank accounts | no | 1 | plaid | Gives the daily cash position across your banks. |
| Cloud costs | no | 3 | aws, azure, gcp | Compares cloud spend with the budget and flags anomalies. |
| Sales pipeline | no | 1 | hubspot, salesforce, pipedrive, attio | Turns signed and expected deals into the cash forecast. |
| Payroll and compensation | no | 1 | sap_successfactors, bamboohr, personio, hibob | Checks payroll cost against the budget. |
| Spreadsheets and reports | no | 3 | google_sheets, onedrive, sharepoint, google_docs, google_slides | Keeps the cash summary and the board pack current. |
| Dashboards (BI) | no | 1 | powerbi, metabase, looker | Checks that the finance dashboards are fresh and match the books. |
| Mailbox | yes | 1 | gmail, outlook, zoho_mail | Reads the finance mailbox and drafts reminders and answers. |

## Chief Revenue Officer (CRO)

Department: Sales.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| CRM | yes | 2 | hubspot, salesforce, pipedrive, attio, odoo, sap_s4hana | Moves qualified deals forward and keeps the pipeline clean. |
| Mailbox | yes | 1 | gmail, zoho_mail, outlook | Answers every inbound sales thread within a working day. |
| Prospecting | no | 2 | hunter, linkedin | Finds and verifies the right contacts at target accounts. |
| Calendar and booking | no | 2 | google_calendar, calendly, outlook | Books meetings and prepares each one. |
| Sales calls | no | 1 | zoom, google_meet | Summarises every sales call with the next step in the CRM. |
| Proposals and signatures | no | 2 | google_docs, google_slides, onedrive, sharepoint, docusign | Drafts proposals and follows them to signature. |
| Subscriptions and renewals | no | 1 | stripe | Spots renewals, expansions and churn risk in subscriptions. |
| Invoices and bookings | no | 1 | quickbooks | Follows bookings, quotes and customer balances in the books. |
| Messaging | no | 1 | whatsapp | Follows up with prospects who prefer messages. |
| Events | no | 1 | luma | Follows up with the people met at events. |

## Chief Marketing Officer (CMO)

Department: Marketing.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Social accounts | yes | 8 | instagram, facebook, threads, x, linkedin, linkedin_api, youtube, tiktok, marsel, discord, telegram, telegram_user, reddit, bluesky, mastodon, pinterest | Answers comments, mentions and messages, and posts in the brand voice. |
| Mailbox | no | 1 | zoho_mail, gmail, outlook | Reads press, partner and creator mail and drafts the answers. |
| CRM | no | 1 | hubspot, salesforce, attio, pipedrive, odoo | Hands every qualified lead to sales with its source campaign. |
| Website analytics | yes | 2 | google_analytics, posthog, mixpanel, amplitude | Reports traffic, sign-ups and conversions per channel. |
| Search (SEO) | no | 3 | google_search_console, bing_webmaster, dataforseo, yandex_webmaster, baidu_ziyuan, indexnow | Tracks rankings and fixes the pages that lose search traffic. |
| Advertising | no | 4 | google_ads, meta, microsoft_ads, tiktok_ads, reddit_ads, amazon_ads, pinterest | Keeps ad spend in line with the conversions it brings. |
| Email marketing | no | 2 | klaviyo, mailchimp, loops, resend, sendgrid, mailgun | Runs newsletters and lifecycle emails and watches deliverability. |
| Website | no | 2 | wordpress, webflow, wix | Publishes posts and landing pages. |
| Design and content production | no | 3 | canva, modelrush, elevenlabs, removebg | Produces on-brand visuals, videos and voice-overs. |
| Events and webinars | no | 2 | luma, zoom | Runs event pages, registrations and follow-ups. |
| Brand documents and reports | no | 2 | notion, confluence, google_drive, google_docs, google_slides, google_sheets, sharepoint, onedrive | Reads the brand guidelines and builds the marketing reports. |
| Affiliates and outreach | no | 2 | affonso, hunter | Tracks affiliates and finds the right contacts for press and partners. |
| Newsletters and launches | no | 2 | substack, medium, producthunt | Publishes long-form posts and follows product launches. |
| Reviews | no | 1 | google_business_profile | Answers reviews on the sites customers read. |

## Chief Operating Officer (COO)

Department: Operations.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Business system (ERP) | yes | 2 | odoo, sap_s4hana, oracle_fusion | Watches orders, deliveries and service levels where they are recorded. |
| Project tracking | yes | 3 | jira, linear, monday, clickup, trello, asana, airtable, superhuman_docs | Measures stalled work and slow handoffs on the boards your teams use. |
| Service desk and incidents | no | 2 | servicenow, zendesk, intercom, freshdesk, pagerduty, sentry | Keeps every ticket and incident inside its service level with an owner. |
| App access | no | 1 | okta | Checks who can use which business app and spots unused or orphaned access. |
| Online orders | no | 1 | shopify, sap_commerce | Follows each order from checkout to delivery. |
| Shipping and tracking | no | 1 | shipstation, aftership, easypost | Catches orders waiting to ship and late or failed deliveries. |
| Mailbox | no | 1 | gmail, outlook, zoho_mail | Reads and answers the operations mailbox. |
| Team chat | no | 2 | slack, microsoft_teams | Announces process changes and chases owners where the teams talk. |
| Procedures and wiki | no | 2 | confluence, notion, sharepoint, google_docs, google_drive, onedrive | Writes the procedures (SOPs) and keeps them current. |
| Spreadsheets | no | 1 | google_sheets | Keeps the operations trackers current. |
| Calendar and meetings | no | 2 | google_calendar, zoom, google_meet | Prepares the operations reviews and records their actions. |
| Scheduled jobs and uptime | no | 1 | tickstem | Notices failed scheduled jobs and outages. |
| Field messaging | no | 1 | whatsapp, twilio | Reaches field teams and suppliers by message. |
| Password manager | no | 1 | bitwarden, keepass | Stores every login and API key it creates, by handle: it never sees a password. |

## Chief Technology Officer (CTO)

Department: Engineering.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Source code | yes | 2 | github, gitlab, gitea | Tracks pull requests, failed runs and releases. |
| Issue tracking | no | 2 | jira, linear | Keeps every incident and bug with a root cause and an owner. |
| Incidents and changes | no | 1 | servicenow, jira, pagerduty | Follows incidents and change requests to closure. |
| Monitoring and uptime | no | 2 | tickstem, cloudflare, route53, sentry | Notices downtime, alarms and failing health checks. |
| Cloud | yes | 3 | aws, gcp, azure, alibaba, sap_btp | Reads alarms, deployments and cost anomalies in your cloud accounts. |
| Team chat | no | 1 | slack, microsoft_teams | Follows the incident and deploy channels. |
| Runbooks and docs | no | 2 | confluence, notion, google_drive, sharepoint, onedrive, obsidian | Keeps runbooks, decisions and post-mortems current. |

## Chief Product Officer (CPO)

Department: Product.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Specs and roadmap docs | yes | 2 | notion, confluence, obsidian, google_docs, google_drive, sharepoint, onedrive | Writes specs with acceptance criteria and keeps the roadmap current. |
| Issue tracking | no | 2 | jira, linear, github, gitlab | Links feedback to roadmap items and follows delivery. |
| Product analytics | yes | 2 | posthog, mixpanel, amplitude | Measures activation, retention and feature adoption. |
| Customer feedback | no | 3 | zendesk, centercode, hubspot, salesforce, odoo, intercom, freshdesk | Collects feature requests and bug reports with the customers behind them. |
| Feedback channels | no | 2 | slack, microsoft_teams | Reads the feedback channels where teams pass customer requests. |
| User interviews | no | 2 | zoom, google_meet, calendly | Schedules user interviews and summarises them. |
| Roadmap boards | no | 1 | airtable, superhuman_docs, monday, clickup, trello, asana | Reads the roadmap where your team keeps it. |
| Pricing and plans | no | 1 | stripe | Follows plan mix, upgrades and downgrades. |
| Launches | no | 1 | producthunt | Follows launches and the comments they get. |
| Spreadsheets | no | 1 | google_sheets | Keeps the prioritisation sheet current. |

## Chief People Officer (CHRO)

Department: People.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| HR system | yes | 2 | sap_successfactors, oracle_fusion, odoo, bamboohr, personio, hibob | Keeps onboarding, leave and headcount in step with the HR system. |
| Recruiting | no | 2 | sap_successfactors, oracle_fusion, odoo, bamboohr, personio, hibob, airtable, greenhouse, lever, ashby | Follows every candidate from application to offer. |
| Payroll | no | 1 | hibob, personio | Checks every pay change before the payroll run. |
| Mailbox | yes | 1 | gmail, outlook, zoho_mail | Reads and answers the jobs and people mailboxes. |
| Employee accounts and access | no | 1 | okta, google_workspace_admin, outlook | Opens accounts and app access for joiners and closes them for leavers, after approval. |
| Calendar and scheduling | no | 2 | google_calendar, calendly, outlook | Books interviews and onboarding meetings. |
| Interview recordings | no | 1 | zoom, google_meet | Summarises every interview against its scorecard. |
| Handbook and policies | no | 2 | google_drive, sharepoint, notion, confluence, google_docs, onedrive, obsidian | Keeps the handbook and onboarding checklists current. |
| Spreadsheets | no | 1 | google_sheets | Keeps the headcount plan current. |
| Team chat | no | 2 | slack, microsoft_teams | Welcomes new joiners and shares people announcements. |
| Sourcing and pay benchmarks | no | 2 | linkedin, quratedai | Finds candidates and checks salaries against the market. |
| E-signature | no | 1 | odoo, docusign | Sends offers and contracts for signature. |

## Chief Customer Officer (CXO)

Department: Customer experience.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Support desk | yes | 2 | zendesk, jira, servicenow, salesforce, hubspot, odoo, oracle_fusion, intercom, freshdesk | Keeps every ticket inside its service level with an owner. |
| Support channels | no | 4 | whatsapp, slack, microsoft_teams, telegram, discord, twilio | Answers customers where they write to you. |
| Mailbox | yes | 1 | gmail, zoho_mail, outlook | Reads and answers the support mailbox. |
| Knowledge base | no | 2 | confluence, notion, sharepoint, google_drive, onedrive, obsidian | Drafts replies from your help articles and fills the gaps. |
| Billing and churn | no | 1 | stripe | Catches failed payments and cancellations the same day. |
| Orders | no | 1 | shopify | Answers order-status questions from the order itself. |
| Delivery tracking | no | 1 | aftership, shipstation, easypost | Answers where-is-my-order questions from the carrier tracking. |
| Product usage | no | 1 | posthog, mixpanel, amplitude | Scores account health from product usage. |
| Onboarding calls | no | 2 | calendly, zoom, google_meet | Books and follows up every onboarding call. |
| Customer emails and reviews | no | 1 | klaviyo, loops | Sends onboarding emails and follows product reviews. |
| Account context | no | 1 | attio, pipedrive | Reads the account history before answering. |
| Spreadsheets | no | 1 | google_sheets | Keeps the support trackers current. |
| App and review sites | no | 1 | google_business_profile | Answers app store and review-site feedback. |

## Chief Information Security Officer (CISO)

Department: Security.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Identity and Microsoft 365 admin | yes | 1 | outlook, okta, google_workspace_admin | Reviews sign-ins, admin roles and security alerts. |
| Cloud security | yes | 3 | aws, azure, gcp, alibaba, sap_btp | Reviews cloud findings, audit logs and access. |
| Code security | no | 2 | github, gitlab, sentry | Watches repository access and code changes. |
| Domains, DNS and firewall | no | 3 | cloudflare, route53, godaddy, namecheap | Watches the firewall, certificates, DNS and domain locks. |
| Threat intelligence | no | 1 | abusech | Checks suspicious hosts, URLs and files against threat feeds. |
| Security tickets | no | 1 | servicenow, jira, pagerduty | Opens and follows a ticket for every finding. |
| Risk and access controls | no | 1 | oracle_fusion, vanta, drata | Tracks control status and segregation of duties. |
| Team chat | no | 1 | slack, microsoft_teams | Raises and follows security incidents with the teams. |
| Security policies and evidence | no | 1 | sharepoint, onedrive, confluence, google_drive | Keeps security policies and audit evidence current and finds files shared too widely. |
| Password manager | no | 2 | bitwarden, keepass | Reviews reused, weak and old passwords, two-step login and the vault's access log; never reads a password. |

## Chief Legal Officer (CLO)

Department: Legal and compliance.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Contract repository | yes | 3 | google_drive, sharepoint, onedrive, confluence, notion, obsidian | Finds every contract, its renewal and notice dates and key clauses. |
| Drafting | no | 1 | google_docs | Drafts and redlines contracts against your playbook. |
| Mailbox | yes | 1 | gmail, zoho_mail, outlook | Triages contracts and legal questions that arrive by email. |
| E-signature | no | 1 | odoo, docusign | Follows each contract to signature. |
| Supplier contracts | no | 1 | sap_ariba | Reads supplier contract workspaces and their terms. |
| Risk and compliance registers | no | 2 | oracle_fusion, servicenow, vanta, drata | Keeps the risk, control and privacy registers current. |
| Brand domains | no | 2 | godaddy, namecheap, route53 | Watches brand domain renewals and locks. |
| Open-source licences | no | 1 | github | Checks the licences of the code you ship. |
| Legal requests | no | 1 | slack, microsoft_teams | Picks up legal requests from the team channels. |

## Chief Data Officer (CDO)

Department: Data.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Data warehouse | yes | 2 | snowflake, databricks, gcp, aws | Answers number questions with the query and the timestamp. |
| App databases | no | 1 | postgres, mysql | Reads the application database behind the numbers. |
| Product and web analytics | no | 3 | google_analytics, posthog, mixpanel, amplitude | Checks that analytics numbers match their source. |
| Metric dictionary | no | 2 | google_sheets, airtable, notion, confluence, google_drive, onedrive, sharepoint, obsidian | Keeps the metric dictionary current: definition, source, owner and refresh. |
| Source systems | no | 3 | stripe, hubspot, salesforce, odoo, shopify, sap_s4hana, pipedrive | Traces revenue and pipeline numbers to the system that produced them. |
| Search data | no | 1 | google_search_console | Checks the search numbers marketing reports. |
| Dashboards (BI) | no | 2 | powerbi, metabase, looker | Finds broken dashboards and conflicting definitions. |

## Chief Supply Chain Officer (CSCO)

Department: Supply chain and procurement.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| ERP and inventory | yes | 2 | odoo, sap_s4hana, oracle_fusion | Watches stock, purchase orders and deliveries where they are recorded. |
| Procurement | no | 1 | sap_ariba, oracle_fusion | Follows approvals, sourcing events and supplier invoices. |
| Sales channels | no | 2 | shopify, sap_commerce | Keeps channel stock and orders in step with the warehouse. |
| Shipping and tracking | no | 2 | shipstation, easypost, aftership | Tracks shipments, carrier exceptions and shipping costs. |
| Mailbox | yes | 1 | gmail, outlook, zoho_mail | Logs every supplier email about a date or price change against its order. |
| Team chat | no | 2 | slack, microsoft_teams | Coordinates with the warehouse and buyers. |
| Spreadsheets and trackers | no | 2 | google_sheets, airtable, onedrive, sharepoint, google_drive, google_docs | Keeps the supplier scorecards and trackers current. |
| Supplier messaging | no | 1 | whatsapp, twilio | Chases suppliers by message. |

## Chief Quality Officer (CQO)

Department: Quality.

| Slot | Required | Cap | Apps in Melaya (priority order) | Why |
|---|---|---|---|---|
| Code and reviews | no | 2 | github, gitlab, gitea | Verifies changes against their acceptance criteria. |
| Issues and defects | yes | 2 | jira, linear | Verifies completed work and tracks escaped defects. |
| Inspections and nonconformances | no | 2 | odoo, sap_s4hana, oracle_fusion | Follows inspections, nonconformances and corrective actions. |
| Complaints | no | 2 | zendesk, servicenow | Classifies every complaint and links it to a corrective action. |
| Beta feedback | no | 1 | centercode | Reads beta feedback before each release. |
| Controlled documents | no | 2 | confluence, sharepoint, notion, google_drive, onedrive, google_docs | Keeps procedures and controlled documents current. |
| Spreadsheets | no | 1 | google_sheets | Keeps the quality KPIs current. |
| Mailbox | no | 1 | gmail, outlook, zoho_mail | Reads the quality mailbox and drafts the answers. |
| Team chat | no | 1 | slack, microsoft_teams | Raises quality issues with the teams. |
| Scheduled jobs | no | 1 | tickstem, pagerduty | Notices failed scheduled jobs and incidents. |
| Compliance and testing | no | 1 | vanta, drata, sentry | Tracks control evidence, test runs and error regressions. |

