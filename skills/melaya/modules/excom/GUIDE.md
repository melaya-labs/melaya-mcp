<!-- Module of the melaya skill. Entry point: ../../SKILL.md -->
> Use when: the task is about Melaya EXCOM, the executive team of AI executives (CEO, CFO, CRO, CMO, COO, CTO, CPO and more) that reads the user's connected apps, drafts and acts under the autonomy the user sets. Covers creating a team end to end for the user (the New team wizard step by step, or the autopilot setup where you do it for them with the `melaya_excom_*` tools, or through Computer Control or Browser Control when the connection lacks the EXCOM permissions), personal and project teams and "Apply my connectors", the apps each role plans, mailboxes and aliases per executive, autonomy levels, action classes, rules and limits, approvals and channels, knowledge sources, executives that operate the user's computer (the COO creating accounts), executives that code on the user's computer (the CTO's coding sessions: worktrees, engines, commits, push and deploy approvals, the production fix loop), the Dome (sources kept while it is off, Set it up for me on hand-made sources), and the devices (browser, computer, phones) the owner gives each executive at Observe or Act in the executive's Devices tab, chosen among the devices already paired. Load references/autopilot-setup.md to run the setup for the user, references/roles-and-apps.md for which apps each role uses.

# Melaya EXCOM: an executive team of AI executives

EXCOM gives a company a team of AI executives. Each executive has a charter (its role), goals, accounts bound from the user's connected apps, knowledge sources, a mailbox, rules and an autonomy level. They read, research, draft and, within the limits the user sets, act. Every action is classified and decided by the Melaya server before it runs, and everything is in the Audit tab.

The app is at https://app.melaya.org/excom. **Prefer the `melaya_excom_*` tools** (below): they create and change a team through the app's own actions, with the user's role and plan, and need no browser or desktop app. Drive the app with Browser Control or Computer Control (`references/autopilot-setup.md`) only when the connection was not granted the EXCOM permissions and the user does not want to reconnect.

## Rules that always apply

1. The user approves. Never approve, decline or edit an EXCOM approval card on your own, and never switch the team to a wider autonomy than they asked for. With `melaya:excom.approve` granted, `melaya_excom_approval_decide` decides a card only when the user asks you to, after you showed it; it never approves spend, secret, legal_people or production cards (a merge into a base branch and every deploy are production: only a person in the Melaya app approves them, never over MCP), and under the computer's Safe setting it only declines.
2. Connecting a service, signing in and choosing what to share are the user's steps. Accounts are bound at write by default and the team's autonomy decides what runs (Observe reads only, Prepare asks first, Run within rules follows the rules); lowering one account to read or drafts only is an optional per-account limit.
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
| One executive | Click it on the Stage or in the rail: Chat, Goals, Tasks, Tools and accounts (apps, mailboxes, pipelines), Devices (browser, phone, computer control, code on this computer; `?pane=devices` opens it), Knowledge, Rules, Skills, Model, Schedule, Memory. |
| Decisions waiting | The Actions tab and the approvals pill; also Telegram, WhatsApp, Slack or Teams cards when set. A decision of an executive paused by the plan (or by hand) stays decidable and is labelled **Paused by your plan**: what is approved runs once the executive is back. |
| The Dome on or off | The hub shows it at the stage's bottom right: off, a chip "Dome off · Events aren't reaching the team" with **Turn on** (Team settings > Dome) and the Dome drawn as a faint outline while the team keeps working; on, a discreet "Dome on" pill. Hidden while the whole team rests on the plan. |
| What happened | The Audit tab (every tool call, its class, the decision and the account used), exportable. |

## The EXCOM tools: prefer them

Seventeen `melaya_excom_*` tools manage a team end to end. Each is a family with an `action`; teams and executives are named by id or name (an executive also by its exact title, its title initials such as "CFO", its role or its department; an exact title wins over the template it was made from, and two matches come back as a list to choose from by id); lists page with `limit` and `cursor`.

| Need | Tool (action) | Permission |
|---|---|---|
| See the teams, one team, its settings, the planner's proposal | `melaya_excom_team_read` (list, get, settings, members, plan, setup, brief, usage, models, notifications) | `melaya:excom` |
| Executives, their chat, devices, coding, wakes | `melaya_excom_executive_read` | `melaya:excom` |
| Apps, accounts, tools, mailboxes, project connectors | `melaya_excom_grants_read` | `melaya:excom` |
| Knowledge, skills, memory, lessons, managed pipelines | `melaya_excom_knowledge_read` | `melaya:excom` |
| Tasks, everything waiting on a person, rules, outcomes | `melaya_excom_work_read` | `melaya:excom` |
| Audit log, one turn's trace, tool I/O, metrics, budget and spend, the Dome, queue, jobs | `melaya_excom_observe` | `melaya:excom` |
| Create (with `roles`), start, pause, resume, archive, delete, members | `melaya_excom_team_manage` | `+ melaya:excom.write` |
| Autonomy, quiet hours, limits, approvers and escalation, channels, profile, the Dome, auto-grant, team model, pipeline read access | `melaya_excom_settings_manage` | `+ melaya:excom.write` |
| Add an executive, charter, model, schedule, autonomy, activate, pause, archive, delete, wake / Push now, interrupt | `melaya_excom_executive_manage` | `+ melaya:excom.write` |
| Message an executive | `melaya_excom_chat_send` (read the reply with executive_read history) | `+ melaya:excom.write` |
| Give an app (`grant_recommended`), add / update / remove a grant, source edits, apply, share or remove a project connector (`project_apply`, `project_share`, `project_remove`) | `melaya_excom_grants_manage` | `+ melaya:excom.write` |
| Mail aliases, wakes | `melaya_excom_mailbox_manage` | `+ melaya:excom.write` |
| Devices, computer control, coding grant and sessions | `melaya_excom_access_manage` | `+ melaya:excom.write` |
| Knowledge sources, skills, memory, managed pipelines | `melaya_excom_knowledge_manage` | `+ melaya:excom.write` |
| Rules | `melaya_excom_rules_manage` | `+ melaya:excom.write` |
| Answer an "asks for help", tasks, task autonomy, outcomes, clear queued work (`jobs_cancel`) | `melaya_excom_tasks_manage` | `+ melaya:excom.write` |
| Approve or decline a card, a proposed rule, a managed pipeline | `melaya_excom_approval_decide` | `+ melaya:excom.approve` (opt-in) |

Method:

1. Read before you change: `melaya_excom_team_read` (`list`, then `get` or `settings`).
2. To create: `team_read` action `plan` (show the user the proposed roles, apps and outcomes), then `team_manage` action `create` with `name`, `scope` (personal, or project + `project`), `roles`, `autonomy` (Prepare for a first dry run), optional `website`; then `start`. Give missing apps with `grants_manage` `grant_recommended`; connect a new app with `melaya_connector_connect` (the user signs in).
3. Most changes return a dry run first (the result starts with DRY RUN and nothing changed): every write of `settings_manage` and `knowledge_manage` (Dome sources added, removed or routed, channels, profile, team model, binds, skills, memory), copying or sharing a connector into a project, granting or widening access, raising or removing a budget or a limit, autonomy up, archive, delete, removals, devices, computer, coding, aliases. Show the dry run, then call again with `confirm: true` only once the user agrees. Each manage tool's description ends with "At once (no dry run): ..." naming the few actions that write directly: they only narrow access, operate (pause, wake, sync, retry) or edit the team's own content (names, charter, tasks).
4. The board role and the plan decide exactly as in the app: a refusal is the app's message (say so, never work around it). The plan caps teams and executives, not autonomy: every plan can use Observe, Prepare and Run within rules.
5. Executives keep working under the team's autonomy, rules, quiet hours, limits and approvals: nothing here runs their actions.
6. Queued work: `melaya_excom_observe` `queue` shows what waits (a paused team holds its work, it never drops it). To clear work the user no longer wants, `melaya_excom_tasks_manage` action `jobs_cancel` on the team or one `executive`, optionally `job_kinds` (for example `["human_turn"]`) and `job_states` (`pending`, `held` = parked by a pause or billing hold, `waiting` = on an approval card, a colleague or a model). It is a dry run first (counts per kind and state, the oldest jobs); `confirm: true` cancels them. A running job is never touched, and an approval card a canceled job waited on can no longer be decided. In the app: Team settings > Archive or delete > **Clear queued work**.
7. The Dome: `melaya_excom_observe` `dome` lists its sources, each with its `triggerId` (readable with `melaya_pipeline_trigger` get / events / deliveries only by the member who switched the Dome on: `trigger_access.you_own_them`). When a source stopped (`pausedReason`, for example DocuSign `push_subscribe_failed: push_scope_missing`, Grafana `push_account_missing`), `observe` action `dome_source_status` gives its subscription status, last delivery, last error and `problem`; have the user fix the cause (reconnect the app with its webhook permission, connect the account, paste the app's webhook signing key) in the connector the team runs on: a project team reads the project's Connectors, so a key saved in the personal connector never reaches a project copy (the `problem` names the project); then `melaya_excom_settings_manage` action `dome_source_retry` with its `source_key` subscribes it again (not a dry run: same app, account and events). While the team is paused the Dome holds its events (`queue` and `dome` say `held`; up to 100 per executive per app account and 500 per executive, the oldest go first) and wakes each executive with them at the resume; Push now is refused until then. `dome` takes `source_key` to show one source only.
   - **Switching the Dome off pauses its sources, it does not delete them** (`pausedReason` `dome_off`). Switched on again, the same sources come back: same trigger ids, same webhook URLs, same signing secrets and the same events (hand edits included); only a source that is really missing is created. A webhook URL pasted by hand into an app keeps answering while the Dome is off (the delivery is accepted, nothing wakes), so the app never disables it. A source that leaves the plan while the Dome is on (the source cap, an event choice of none, an executive paused, a hand-made source whose account is still connected) is paused with `dome_left_plan` and comes back on its own; it is deleted only when a person removed it, a ready instant source replaces a scheduled check for good, or no executive holds that app account any more. `dome_source_status` counts the sources the Dome itself switched off and kept: they are not a problem. A hand-made source stays bound to its URL even when the API key is pasted again in another form (spaces, quotes, a leading Bearer): the same key gives the same account.
   - **Hand-made sources** (apps where Melaya cannot register the webhook itself: Zoho Mail's outgoing webhook, affiliate, monitoring and BI tools, any source marked set up by hand) show a status chip (Connected, Waiting for the first event, Needs setup, Paused) and **Set it up for me** while nothing delivers: with the browser extension or computer control online, it builds a prompt from the source (the app, the account, the exact callback URL, the events, the click path) that the user copies or runs now; the prompt stops at any secret and hands it to the user. **Advanced: set it up by hand** keeps the URL, the signing step and **New signing secret**. Pipeline push triggers in Studio get the same Set it up for me.
   - **Zoho Mail is instant with no setup** when the mailbox is connected with Sign in with Zoho (IMAP access on, paid Zoho plans): an old connection needs one new sign-in. If IMAP Access is off and the signed-in user is a Zoho org admin, Melaya switches it on for the mailbox a Dome source, an executive's wake or the user's own enabled pipeline push trigger watches (that mailbox only, audited); otherwise the source says how to tick IMAP Access in Zoho Mail (Settings > Mail Accounts > IMAP Access), and Set it up for me can do it. The outgoing webhook stays an optional advanced path.
8. An executive of the user's own: `executive_manage` `create` with the `role` it starts from plus its own `title` and `department` (for example `role: "cro"`, `title: "Chief Partnerships Officer"`, `department: "Partnerships"`). It shows as itself in the app, with "Based on CRO" as a hint, and its vault grant is the team's shared folders plus its own folder (named after its department), never another executive's. `update` changes `title` and `department` later. `tasks_manage` `objective_save` with `objective_id` changes only the fields sent (a new owner needs no `name`).
9. Knowledge: recommend an Obsidian vault first, ahead of loose documents, Drive, Notion or Confluence (they stay possible). `team_read` `plan`, `team_manage` `create` and `knowledge_read` `sources` (while no vault is bound) return `knowledge`: with vaults, `knowledge_manage` `bind` kind `obsidian` with `ref {selection: {items: [{vault_id, folders}]}}` (company folders for the whole team, a role folder per executive), then `sync`; with none, `knowledge.build_vault` proposes the CEO skill **Build your company knowledge vault** (`ceo-company-knowledge-vault.md`; read it with `knowledge_read` action `skill`, skill `ceo-company-knowledge-vault`): the user builds the vault on their own computer with you, connects it in Melaya (Connectors, Obsidian, Connect a vault), then you bind it to the team.
10. A missing tool is a permission the user did not grant: ask them to reconnect and switch on **Read your EXCOM teams** / **Manage your EXCOM teams** (and **Approve or decline**, only if they want to delegate decisions).

## Create a team: the New team wizard

Six steps in one panel, saved as you go (closing it and coming back resumes it):

1. **Who is this team for?** Choose how to set it up:
   - **I'll follow the steps** (the steps below), or
   - **Set it up for me with my AI assistant**: the panel checks whether one of the user's MCP clients holds `melaya:excom` and `melaya:excom.write` (and shows how to connect one if not: the server URL, the Claude Code command, the two consents, the MCP setup docs), takes the answers so far (team name, website, roles, direction, personal or project) and gives a **Copy prompt** button. The prompt ("Set up my Melaya EXCOM team with the melaya_excom_* tools ...") tells the assistant (you) to build the team with the `melaya_excom_*` tools, so every change is in the Audit tab as "Through an MCP client". A collapsed fallback, "No EXCOM tools in your assistant? Use Computer Control instead", keeps the older route: the desktop app checklist and a prompt that drives the wizard through Computer Control. See `references/autopilot-setup.md`.

   Then pick **My team** (runs on the user's own connectors and keys, only they see it) or **A project team** (runs on the project's credential pool; members get roles and an approver can be added), and the project.
2. **Your company in one line.** Pick a source (Website, Obsidian, Drive, Notion, Confluence or a File) and draft: Melaya fills the profile line by line, each line with its source. Or type the company name and one line. Every line stays editable.
3. **Pick your first executives.** Roles are proposed from what is connected (a CRM suggests a CRO, accounting suggests a CFO, a mailbox a CEO, GitHub a CTO), with the accounts that will be bound shown read-only. Three is enough to start; executives ask for more connections as tasks.
4. **How much should they do?** Observe, Prepare (recommended) or Run within rules (see below).
5. **How should your team reach you?** Telegram, WhatsApp, Slack, Teams, the phone app, email. The in-app inbox is always on. Can be skipped.
6. **Ready to start.** The summary and the team's name; **Start the team** creates the team and each executive, then a read-only first pass: nothing is sent, spent or changed.

After Start, missing inputs become tasks in the Actions tab ("Asked by the team"), and the first brief arrives after the first pass.

## Personal and project teams

A project team runs on the project's connectors, not the owner's personal ones. On the project's Connectors page, **Apply my connectors** copies the owner's connected accounts into the project in one step, product by product for Google (tick every product the team needs). A few connectors whose tokens rotate on every refresh cannot be copied (for example X, TikTok, LinkedIn API, Canva, Microsoft Ads, Reddit Ads, Yandex Webmaster): the user connects those directly on the project. Leave test-only accounts out of a production team. To take a connector back off the project, use `grants_manage` action `project_remove` (`service`, optional `account`): a dry run first that names what the project loses, then `confirm: true`. A Google product (Google Ads, Gmail, Drive…) leaves the project's Google accounts while their other products stay; a connector shared by reference stops; the user's personal connection always stays. On the Connectors page the same is the card's ✕, and **Replace with my connection** swaps another member's copy for the user's own.

## The apps each role plans

Each role plans its apps by capability slot (mailbox, calendar, chat, docs and knowledge, CRM, accounting, payments, ads, social, analytics, support desk, HR, recruiting, code, monitoring, cloud, data warehouse, e-signature, shipping, compliance ...), a few apps per slot, in priority order, bound at write (the autonomy mode decides). The executive's Tools pane shows **Recommended for this role** with a coverage score, apps **Connected but left out**, and apps **Not in Melaya yet**. When the user connects an app later, every executive whose role uses it gets access automatically (the team setting is on by default), or an item asks the owner to give it. Full table per role: `references/roles-and-apps.md`.

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

Team knowledge (shared by all executives) and executive knowledge: an Obsidian vault first, then websites, Drive, Notion, Confluence, uploaded files. Executives search before answering and cite their sources. Team settings > Knowledge, or the executive's Knowledge pane. Recommend the vault first; when the user has none, propose the CEO skill **Build your company knowledge vault** (`ceo-company-knowledge-vault.md`): build it locally with the user's own assistant, connect it, then attach it to the team. A vault source on a Git repository shows its drift in `knowledge_read` `sources` (`vaults[].index_commit`, `vault_commit`, `fetched_at`, `last_error`, `behind`); when one is behind, `knowledge_manage` `vault_sync` (with `vault_id` from `knowledge_read` `vaults`) fetches the repository now, then the team's sources on it sync again. Suggest a push webhook on the vault (vault settings, Instant updates on push) so every push is fetched within seconds. `vault_rename`, `vault_share` (read or edit, to the team's project) and `vault_unshare` exist too; sharing and unsharing are dry runs until `confirm: true`. `entries` is paged: pass `limit` (1-100) and `cursor`.

## Executives that operate the user's computer

On the **Computer control** card of an executive's **Devices** tab (its identity, accounts and stored secrets under **Accounts and secrets**), the owner can let it operate their computer through the Melaya desktop app: typically the COO, to create accounts, generate keys and verify mail. It is off for every executive until the owner switches it on, and only the member whose computer it is can switch it on. Its pieces:

- **Identity for new accounts (team)**: the preferred sign-up email and a Google sign-in identity to use as a backup.
- **Accounts created**: the account profiles the executive made, and which are connected to Melaya.
- **Stored secrets**: keys and passwords it captured are kept as encrypted handles, never shown to the model; the owner can reveal or delete one.

The allowed apps, their levels and the computer's approval mode still apply (Computer Control > Apps and Safety tabs). Password fields are handed to the user. Load `../../modules/devices-computer/GUIDE.md`.

## Devices for executives (browser, computer, phone)

In the executive's **Devices** tab (after Tools and accounts; `?pane=devices`), the owner gives that executive specific devices of their own: a browser (the paired Melaya extension), a computer (the Melaya desktop app, the same switch as Computer control) and up to four Android phones. The tab has four cards, Browser, Phone, Computer control and Code on this computer, each with one switch, the device as a chip (green online, amber not seen recently, grey offline) and **Change** when several devices qualify. With nothing paired yet, a card is an invitation instead (install the extension, pair a phone, get the desktop app for this computer's system). Each device is switched on separately, at a level:

- **Observe**: the executive reads that device's screen only.
- **Act**: it operates it under its autonomy. In Observe it still only reads; in Prepare it navigates, opens apps and types, and every post, send, submit, purchase or deletion shows the owner an approval card first; in Run within rules a post or a send runs when an active rule covers it (Rules: class Send, tool `phone_*` or `browser_*`), and a purchase or a deletion always asks.

Rules of the feature:

- Off by default. Only the team owner gives devices, and only their own (the member the executive works as). Suggestions per role (the CMO: phone and browser for social posting; the COO: computer and browser) never grant anything.
- The executive can use only the devices picked there; any other device is refused, even one of the owner's.
- Only devices the member has already paired can be given: one browser, one computer and up to four phones per executive. There is no separate EXCOM limit on devices; the plan limits browsers, computers and phones when they are paired, and the team's autonomy (not the plan) decides what the executive may do with them.
- The device's own safe mode still stops on a post, a payment or a deletion it detects; a CAPTCHA, a password, a card or a bank detail is always handed to the person at the device.

Typical request: "let the CMO post on X with my phone instead of the X API". Steps for the user (never grant on their behalf): open the CMO, the Devices tab, switch the Phone card on, choose Act; keep the team in Prepare for a first post (it asks), then add a send rule for that phone if the user wants it to post alone. To set it up for the user through Browser or Computer Control, stop at each switch and let the user confirm it.

## Executives that code on the user's computer (CTO)

On the **Code on this computer** card of the executive's **Devices** tab (suggested on the CTO; off for everyone by default), the owner whose computer it is lets that executive develop on it in **coding sessions**. The setup asks one question, the project folder (**Choose** opens the folder dialog on that computer, a typed path is the fallback); the computer is picked on its own (online, with an engine), with a choice only when several qualify. Everything else is automatic: pushes go to the repository's own `origin`, sessions start from its default branch (detected at session start), the engine is Automatic, 30 minutes and 60 turns per session, no checks (a plain `tsc` typecheck script in the repository's `package.json` runs when TypeScript is installed). **Advanced settings** keeps the other remotes, base branch, engine, native-loop model, checks and budgets.

Over MCP: `melaya_excom_executive_manage` action `coding` (`coding_enabled`, `computer` = the runner device id or the label `melaya_excom_executive_read` action `coding` lists, `repos`, `remotes`, `base_branch`, `engine`, `native_model`, `checks`, `max_minutes`, `max_turns`), or `melaya_excom_access_manage` action `coding` (the same code; `enabled` and `runner_device`). `computer` and `repos` alone are enough; `remotes` empty means origin; `base_branch` `""`, `"auto"` or `"default"` means the detected default branch. Fields not sent keep their stored value. Switching on or widening (a repository, remote or check added, a budget raised, another computer, base branch, engine or model) is a dry run until `confirm: true`; switching off or only narrowing applies at once. Only the team owner whose computer it is can switch it on.

- Each session runs in its own git worktree on a new `excom/` branch, from the base branch's last commit; the user's working tree and branches are never touched. Uncommitted changes in the user's folder only warn, never block: the session does not include them, says how many there are (`localChanges`, a count, never file names) in its result, its status and the push card, and leaves them as they are. The engine only edits files and runs git status/diff/log/add/commit, tests, type checks and `npm run` scripts: no push, no network tools, no secrets.
- Commits: the engine commits its own work, one command per call, in the repository's own convention (it is given the base branch's recent commit messages and the repository's commit rules), never with an AI attribution line (such lines are stripped). The runner never commits on its own: what the engine left is reported as uncommitted, with the diff stat.
- A Claude Code session needs Node.js on the computer's PATH: its guard hook runs with it, and the session refuses to start when the guard cannot run. Tell the user to install Node.js and restart the runner or the app.
- Engines: **Automatic (the executive's model)** by default: Claude Code, Codex or the Copilot CLI when installed and matching the executive's model, otherwise Melaya's native loop, which runs on every local model (LM Studio and Ollama too). Or one engine explicitly.
- The executive's tools: `excom_code_task` (repo, goal, optional runbook such as AddNewTool from a knowledge source, optional `evidence` of a production error) is a record write: it asks in Prepare. `excom_code_status` reads. `excom_code_push` target branch is a send; target base merges into the base branch and pushes it: production, it always asks a person in the app, with the diff stat and the commits on the card. A base that moved is rebased onto (the session's commits replayed, never a merge commit); a conflict refuses the push. The merge goes to the remote only: the user's folder and local base branch are never checked out or moved, so the user pulls when ready. `excom_code_push` takes `commit_message` (one line, at most 200 characters, no trailer or attribution): the session's work, its commits and anything left uncommitted, becomes one commit with exactly that message, shown on the card with the new commit and the commits it replaces; use it to commit what the engine left or to fix a message that breaks the convention. A session with uncommitted changes pushed without `commit_message` is refused. The approved push re-checks the message, the head and the files: if any changed since the card, nothing is pushed. `excom_code_discard` removes the worktree (sessions are swept after 7 days).
- Deploys go through the Jenkins connector, one job at a time in the order the company's own deploy runbook gives (read it from the team's knowledge; never assume an order): each `jenkins_trigger_build` asks first (production), `jenkins_wait_build` follows it to the end, and the next job starts only once the previous one finished SUCCESS. On a failure, read the build console and stop.
- Production fix loop with a monitoring connector (Grafana): monitor, fix (a session with the error's evidence and a test that reproduces it; the result says which evidence it addressed and the covering test), push, deploy, verify the error stopped.
- An executive whose model runs on the runner (Claude Code, Codex, a local model) keeps its board tools (`excom_*`, knowledge, the coding tools) visible even when its context is long enough to be paged; `melaya_tools` search and `activate_tool` point to them, called through `melaya_tool_call`.

Typical request: "let the CTO fix the errors Grafana shows". Steps for the user (never switch it on or approve on their behalf): connect the coding runbooks as a knowledge source of the CTO, open the CTO, the Devices tab, Code on this computer, choose the project folder, Turn on; keep the team in Prepare (each session, each base push and each deploy asks); connect Jenkins and Grafana. If the card says the computer is offline or no engine is found, the runner on that computer needs an update; a Claude Code session that refuses to start for its guard needs Node.js on that computer.

## Definition of done

- [ ] The team exists with the agreed scope (personal or project), roles, models and autonomy, and is paused or started as the user asked.
- [ ] The accounts each role needs are connected (on the project for a project team) and bound at the access the user chose.
- [ ] Mailboxes: each executive sends as and reads the agreed aliases; one wake per alias.
- [ ] Autonomy, limits, quiet hours and channels set as agreed.
- [ ] Nothing approved, sent or widened on the user's behalf; the user got a short summary and the open tasks.
