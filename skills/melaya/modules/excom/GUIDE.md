<!-- Module of the melaya skill. Entry point: ../../SKILL.md -->
> Use when: the task is about Melaya EXCOM, the executive team of AI executives (CEO, CFO, CRO, CMO, COO, CTO, CPO and more) that reads the user's connected apps, drafts and acts under the autonomy the user sets. Covers creating a team end to end for the user (the New team wizard step by step, or the autopilot setup where you do it for them through Computer Control or Browser Control), personal and project teams and "Apply my connectors", the apps each role plans, mailboxes and aliases per executive, autonomy levels, action classes, rules and limits, approvals and channels, knowledge sources, and executives that operate the user's computer (the COO creating accounts). Load references/autopilot-setup.md to run the setup for the user, references/roles-and-apps.md for which apps each role uses.

# Melaya EXCOM: an executive team of AI executives

EXCOM gives a company a team of AI executives. Each executive has a charter (its role), goals, accounts bound from the user's connected apps, knowledge sources, a mailbox, rules and an autonomy level. They read, research, draft and, within the limits the user sets, act. Every action is classified and decided by the Melaya server before it runs, and everything is in the Audit tab.

The app is at https://app.melaya.org/excom. There is no `melaya_excom_*` MCP tool: a team is created and changed in the app. To do it for the user, you drive the app with Browser Control (`melaya_browser_*`, the Melaya browser extension) or Computer Control (`melaya_computer_*`, the Melaya desktop app). Load `references/autopilot-setup.md`.

## Rules that always apply

1. The user approves. Never approve, decline or edit an EXCOM approval card for them, and never switch the team to a wider autonomy than they asked for.
2. Connecting a service, signing in and choosing what to share are the user's steps. Accounts are bound read-only by default; widening a grant to draft or write is the user's choice, per account.
3. Passwords, one-time codes, card numbers and legal acceptances are the user's. Hand them back (`melaya_computer_handoff`, or ask in chat) and continue after they confirm.
4. An executive can never change its own grants, budget, rules, members or autonomy. Do not try to make one do it.
5. For a dry run, set the team to Prepare (or Observe): nothing leaves without the user's approval.

## Where things are

| Need | Where |
|---|---|
| Create a team | EXCOM page, the Team switch at the top, **New team** (with no team yet the page offers it). |
| Switch teams | The Team switch (name, executive count, status dot). |
| Pause or resume | The play / pause button in the header. Pause stops new work at once. |
| Autonomy of the team | The Autonomy switch in the header (Observe, Prepare, Run within rules). |
| Team settings | The gear: Profile, Members, Model, Knowledge, Channels, Limits and schedule (budget, message caps, quiet hours, review time), Objectives, Skills, Danger zone. |
| One executive | Click it on the Stage or in the rail: Chat, Goals, Tasks, Tools and accounts (accounts, mailbox, computer control), Knowledge, Rules, Skills, Model, Schedule, Memory. |
| Decisions waiting | The Actions tab and the approvals pill; also Telegram, WhatsApp, Slack or Teams cards when set. |
| What happened | The Audit tab (every tool call, its class, the decision and the account used), exportable. |

## Create a team: the New team wizard

Six steps in one panel, saved as you go (closing it and coming back resumes it):

1. **Who is this team for?** Choose how to set it up:
   - **I'll follow the steps** (the steps below), or
   - **Set it up for me with my AI assistant**: the panel detects the user's computer, links the Melaya desktop app download, shows a checklist (desktop app installed and signed in, computer online, the Safety tab set to Autonomous for MCP clients, the Melaya MCP connected in the assistant) and a **Copy prompt** button. The prompt tells the assistant (you) to install this skill and create the team from the user's answers. See `references/autopilot-setup.md`.

   Then pick **My team** (runs on the user's own connectors and keys, only they see it) or **A project team** (runs on the project's credential pool; members get roles and an approver can be added), and the project.
2. **Your company in one line.** Pick a source (Website, Obsidian, Drive, Notion, Confluence or a File) and draft: Melaya fills the profile line by line, each line with its source. Or type the company name and one line. Every line stays editable.
3. **Pick your first executives.** Roles are proposed from what is connected (a CRM suggests a CRO, accounting suggests a CFO, a mailbox a CEO, GitHub a CTO), with the accounts that will be bound shown read-only. Three is enough to start; executives ask for more connections as tasks.
4. **How much should they do?** Observe, Prepare (recommended) or Run within rules (see below).
5. **How should your team reach you?** Telegram, WhatsApp, Slack, Teams, the phone app, email. The in-app inbox is always on. Can be skipped.
6. **Ready to start.** The summary and the team's name; **Start the team** creates the team and each executive, then a read-only first pass: nothing is sent, spent or changed.

After Start, missing inputs become tasks in the Actions tab ("Asked by the team"), and the first brief arrives after the first pass.

## Personal and project teams

A project team runs on the project's connectors, not the owner's personal ones. On the project's Connectors page, **Apply my connectors** copies the owner's connected accounts into the project in one step, product by product for Google (tick every product the team needs). A few connectors whose tokens rotate on every refresh cannot be copied (for example X, TikTok, LinkedIn API, Canva, Microsoft Ads, Reddit Ads, Yandex Webmaster): the user connects those directly on the project. Leave test-only accounts out of a production team.

## The apps each role plans

Each role plans its apps by capability slot (mailbox, calendar, chat, docs and knowledge, CRM, accounting, payments, ads, social, analytics, support desk, HR, recruiting, code, monitoring, cloud, data warehouse, e-signature, shipping, compliance ...), a few apps per slot, in priority order, bound read-only. The executive's Tools pane shows **Recommended for this role** with a coverage score, apps **Connected but left out**, and apps **Not in Melaya yet**. When the user connects an app later, every executive whose role uses it gets read access automatically (the team setting is on by default), or an item asks the owner to give it. Full table per role: `references/roles-and-apps.md`.

## Mailboxes and aliases

Each executive's mailbox account (Zoho Mail, Gmail or Outlook) has two lists, set under the executive's **Tools and accounts > Mailbox**:

- **Sends as**: the addresses it may send from, the first one being its default. Enforced.
- **Reads**: the addresses whose mail it may list and search (mail sent to them). Enforced on lists and searches. Empty means the whole mailbox.

A common layout uses the company's aliases: the CEO on the main address with the whole mailbox; the CRO sending as sales@ and partners@ and reading those plus the main address; the CMO marketing@ and press@; the CFO finance@; the COO ops@, vendors@ and legal@; the CTO tech@ and security@; the CPO product@ and support@. Adding the main address to each "Reads" list keeps every executive aware of the shared inbox. Add one mail wake per alias ("new email to <alias>", Inbox only) so each executive wakes on its own mail; one message wakes it once.

## Autonomy, action classes and rules

| Level | What it does |
|---|---|
| Observe | Reads only, a daily brief, nothing is written anywhere. |
| Prepare (recommended) | Reads and drafts. Every send, spend or change asks first. |
| Run within rules | Sends and updates under the rules the user approved; anything outside them still asks. |

The team sets the ceiling; a role can only be narrower. Every tool call is classified before it runs: read, propose, draft, send, record change, spend, delete, production, legal or people, secret, pipeline schedule, self-modification. Spend, delete, production, legal or people, secrets and pipeline schedules always ask, in every mode; self-modification never runs. Rules come from approvals: after three identical approvals of the same class and scope, the executive proposes a rule with the bounds it observed, and the user allows it or keeps asking. Limits apply before any rule: optional daily budget, external messages per day, recipients per message, quiet hours (20:00 to 07:00 by default), the review time.

## Dry runs

The autonomy level is the only control. To test a team safely, use Prepare: executives read and draft, and every send, record change, spend or deletion waits as a card the user approves or declines; nothing leaves without their approval. Observe is stricter still (reads and proposed tasks only). Move to Run within rules only when the user asks and the rules they approved cover what the team may do on its own.

## Approvals and channels

Cards wait in the Actions tab and on the channels the user chose (Telegram, WhatsApp, Slack, Teams, the phone app). Any one decision answers the card. Show the user what is waiting; never decide for them.

## Knowledge

Team knowledge (shared by all executives) and executive knowledge: websites, an Obsidian vault, Drive, Notion, Confluence, uploaded files. Executives search before answering and cite their sources. Team settings > Knowledge, or the executive's Knowledge pane.

## Executives that operate the user's computer

Under an executive's **Tools and accounts > Computer control**, the owner can let it operate their computer through the Melaya desktop app: typically the COO, to create accounts, generate keys and verify mail. It is off for every executive until the owner switches it on, and only the member whose computer it is can switch it on. Its pieces:

- **Identity for new accounts (team)**: the preferred sign-up email and a Google sign-in identity to use as a backup.
- **Accounts created**: the account profiles the executive made, and which are connected to Melaya.
- **Stored secrets**: keys and passwords it captured are kept as encrypted handles, never shown to the model; the owner can reveal or delete one.

The allowed apps, their levels and the computer's approval mode still apply (Computer Control > Apps and Safety tabs). Password fields are handed to the user. Load `../../modules/devices-computer/GUIDE.md`.

## Definition of done

- [ ] The team exists with the agreed scope (personal or project), roles, models and autonomy, and is paused or started as the user asked.
- [ ] The accounts each role needs are connected (on the project for a project team) and bound at the access the user chose.
- [ ] Mailboxes: each executive sends as and reads the agreed aliases; one wake per alias.
- [ ] Autonomy, limits, quiet hours and channels set as agreed.
- [ ] Nothing approved, sent or widened on the user's behalf; the user got a short summary and the open tasks.
