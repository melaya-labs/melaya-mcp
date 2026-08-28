# Melaya MCP Server

Let an AI assistant operate your Android phone.

Melaya pairs a phone to your account and gives an agent the same view of it a person has: it reads the screen through Android's accessibility tree, then taps, types, swipes, and moves between apps. No per-app integration, no vendor API — if you can use the app, so can the agent.

This is a remote [Model Context Protocol](https://modelcontextprotocol.io) server. MCP is a vendor-neutral standard, so one endpoint works everywhere:

```
https://api.melaya.org/mcp
```

Nothing to install, no SDK required.

## Connect

**Claude Code**

```bash
claude mcp add --transport http melaya https://api.melaya.org/mcp
```

**Claude** (claude.ai, Desktop, mobile) — Settings → Connectors → Add custom connector.

**ChatGPT** — Settings → Connectors → Developer mode. Team, Business, Enterprise and Education plans.

**Mistral Le Chat** — Connectors → Add custom MCP connector.

**Cursor, VS Code, Zed, Cline, Goose, Windsurf** and any other MCP client — add it wherever the client takes a remote MCP server URL.

Authentication is OAuth 2.1 with PKCE. You choose which permissions to grant on a Melaya consent page; the assistant receives a scoped token. Your password is never shared.

Then just ask:

> Connect my phone and go through my unread Instagram DMs.

## What it can do

**Operate your phone.** Read the screen, open apps, tap, type, scroll, swipe, screenshot. Melaya ships navigation playbooks for common apps, so the agent acts like it already knows Instagram or WhatsApp instead of exploring blindly.

**Run agents that keep working.** Hand a long or recurring phone task to an autonomous Melaya agent that runs on your own machine, on your own model subscription, and carries on after the conversation ends.

**Reach your Melaya account.** Pipelines, runs and traces, agent memory, RAG stores, usage and plan limits.

## What it cannot do

Enforced on the phone itself, not on the server, so no prompt and no agent instruction can move them:

- **The agent only touches apps you allow-list, and it cannot add to that list.** It can hand access back — narrow the list, or clear it entirely — but only you can grant it, in the Melaya app or on the phone. The agent reads text off your screen, and text can be written by anyone; a boundary it could widen in response to what it reads would not be a boundary.
- **Publishing and paying always ask you.** Posting a comment, creating a post, or anything resembling a payment stages an approval card on the phone and waits. You see the exact text first.
- **There is a STOP control**, on the phone overlay and in the Melaya app. It halts everything immediately, across every agent and every connected assistant.

Password fields are excluded from screen reads.

## Requirements

- A Melaya account — free at [melaya.org](https://melaya.org)
- An Android phone (Android 8 or newer). There is no iOS build.
- For autonomous agents: Node 18+, Python 3.11+, and a signed-in CLI on the machine hosting the runner

## Privacy

Screen content read during a run goes to Melaya and to whichever model you selected, for the duration of that run. The [privacy policy](https://melaya.org/en/legal/privacy) covers collection, retention and deletion.

One credential does cross the boundary, and it is worth naming: if you set up the optional local runner, the command you are given contains a runner token. It is valid for 7 days, revocable in Melaya settings, and unavoidable because the runner starts from a command line. On a hosted assistant that command appears in your conversation history. Nothing else does — provider and connector credentials are resolved server-side and never reach the assistant.

Disconnecting in Melaya settings immediately revokes the connection's ability to renew itself. A token it already holds keeps working until it expires, at most one hour.

## What's in this repo

| Path | Purpose |
|---|---|
| `server.json` | Manifest for the [official MCP Registry](https://registry.modelcontextprotocol.io) |
| `.mcp.json` | Remote server declaration |
| `.claude-plugin/`, `skills/`, `commands/` | Claude Code plugin packaging — one distribution of the same server |

The server itself runs as part of the Melaya platform; this repo is its public manifest, packaging and documentation.

## Links

- [Full documentation](https://github.com/melaya-labs/melaya/blob/main/docs/mcp.md)
- [Melaya SDKs](https://github.com/melaya-labs/melaya) — nine languages
- [Privacy Policy](https://melaya.org/en/legal/privacy) · [Terms](https://melaya.org/en/legal/terms)
- [Support](mailto:support@melaya.org)

## License

Apache-2.0, matching the [Melaya SDKs](https://github.com/melaya-labs/melaya).

It covers what is in this repository — the registry manifest, the plugin packaging, the skills and this documentation. It is not a licence to the Melaya service itself: using the hosted server at `api.melaya.org` needs a Melaya account and is governed by the [Terms](https://melaya.org/en/legal/terms).
