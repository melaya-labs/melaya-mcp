<!-- Reference of the excom module of the melaya skill. Entry point: ../GUIDE.md -->
# Set up an EXCOM team for the user, end to end (autopilot)

Use this when the user asks you to create their Melaya EXCOM team for them, usually after copying the prompt from the wizard's "Set it up for me with my AI assistant" option. You do every step in the app yourself, from the user's answers, and stop only for what is theirs: passwords, one-time codes, CAPTCHAs, legal acceptances and approval cards.

## 0. Before you start (check, do not assume)

1. `melaya_setup_status`: act on its gaps first.
2. You need one way to operate the app:
   - **Computer Control** (preferred for autopilot): `melaya_computer_status` shows the user's computer online through the Melaya desktop app. The user's web browser must be allowed in Computer Control > Apps at **Full control** (ask them if it is not; never allow it yourself).
   - or **Browser Control**: `melaya_browser_status` / `melaya_browser_attach` with the Melaya extension paired. Work in your own tab (`melaya_browser_tabs` with `action: "open"`).
3. For the setup to run without a card on every submit, the user sets **Computer Control > Safety > Agents connected over MCP** to **Autonomous** on that computer (opening a program or a macro still asks). If it is Safe, every submit waits for their approval: tell them once, then wait for their decisions. Never change it for them.
4. Read `../GUIDE.md` (EXCOM) and `../../devices-computer/GUIDE.md` (Computer Control) before acting.

## 1. Collect the inputs (one short message)

Ask only what you cannot read yourself; offer defaults:

| Input | Default if the user has no preference |
|---|---|
| Team for: personal or a project (which one) | Personal |
| Company website (or another source: Obsidian vault, Drive, Notion, Confluence, a file) | The website |
| Goals for the first weeks (for example first paying customers, partners, affiliates) | Read from the company profile |
| Roles | CEO, CRO, CMO, CFO, COO, CTO, CPO (or the three proposed from their connected apps) |
| Autonomy | Prepare (the safe dry run: nothing leaves without the user's approval) |
| Mailbox aliases per role | One alias per role on the main mailbox, each also reading the main address |
| Channels for decisions | The in-app inbox plus their phone (Telegram or WhatsApp if linked) |
| Models | The team's working provider (never pick one that is not working) |

## 2. Create the team (the New team wizard)

Open https://app.melaya.org/excom, then New team. For each step: read the window, act, verify.

1. Who is this team for: My team or A project team (pick the project). Continue.
2. Company: pick the source, type the website, **Draft from my site**; wait for the lines; correct any line the user's answers contradict. Continue.
3. Executives: select the agreed roles (or **Use the proposed three** and add the rest). Continue.
4. Autonomy: the agreed level. Continue.
5. Channels: the agreed channels, or **Skip for now**. Continue.
6. Ready: set the team name, check the summary, **Start the team**.

If a step reports a gap (no working model, no project), fix it with the user, then continue. Read the result of Start: every executive created, or the ones that could not start and why.

## 3. Connectors

- Personal team: the executives use the user's connected apps. Missing ones show as "Needed" in each executive's Tools pane; list them for the user and give the connect link (`melaya_connector_connect`). The sign-in is theirs.
- Project team: on the project's Connectors page, **Apply my connectors**, ticking every Google product the team needs. List the connectors that cannot be copied and ask the user to connect them directly on the project.

## 4. Per executive

Open each executive (click it on the Stage or in the rail):

- **Tools and accounts**: confirm the bound accounts; leave them read-only unless the user asked for more.
- **Mailbox**: Sends as (default first) and Reads lists per the agreed aliases; add a mail wake per alias (Zoho "new email to" a given address).
- **Computer control** (only if the user asked, typically the COO): switch it on, fill the Identity for new accounts (sign-up email, Google identity).
- **Goals**: the agreed objectives with their owner.

## 5. Team settings

- **Limits and schedule**: message and recipient caps, quiet hours, review time; budget as the user wants (none when their models are subscriptions).
- **Knowledge**: add the team's sources (website, vault, Drive, Notion, Confluence).
- **Objectives**: the agreed outcomes (for example 5 paying customers, 3 signed partners, 20 active affiliates).
- Pipelines the user already runs stay as they are; link them to the executives who should see them.

## 6. Finish

- Leave the team paused or started, as the user asked.
- Summarise in plain words: the team, roles, models, autonomy, mailboxes, what is connected, what is still needed (with links), where decisions will arrive.
- Never approve the cards that appear: point the user to the Actions tab or their phone.

## Things that are always the user's

Signing in to an app or a vendor, passwords and codes, CAPTCHAs, payments, legal acceptances, approving cards, widening an app's access level or the computer's approval mode, and connecting accounts that cannot be copied.
