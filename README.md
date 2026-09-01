<div align="center">

# Melaya MCP Server

**Let an AI assistant use your Android phone, your browser, and the rest of your Melaya account.**

[![MCP Registry](https://img.shields.io/badge/MCP_Registry-org.melaya%2Fmelaya-6E56CF)](https://registry.modelcontextprotocol.io)
[![smithery badge](https://smithery.ai/badge/info-h530/melaya)](https://smithery.ai/servers/info-h530/melaya)
[![Tools](https://img.shields.io/badge/tools-76_across_8_domains-22D3EE)](#what-it-can-do)
[![Auth](https://img.shields.io/badge/auth-OAuth_2.1_%2B_PKCE-10B981)](#permissions)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)

[Documentation](https://github.com/melaya-labs/melaya/blob/main/docs/mcp.md) · [Melaya](https://melaya.org) · [Device Control](https://melaya.org/en/product/agentic-device-control) · [MCP Server](https://melaya.org/en/product/mcp)

</div>

<p align="center">
  <img src="https://melaya.org/blog/july-2026/three-pillars.png" width="860" alt="Melaya: assistant, agent builder and paired phone on one runtime">
</p>

Melaya pairs a phone to your account and gives an agent the same view of it a person has: it reads the screen through Android's accessibility tree, then taps, types, swipes, and moves between apps. No per-app integration, no vendor API. **If you can use the app, so can the agent.**

This is a remote [Model Context Protocol](https://modelcontextprotocol.io) server. MCP is a vendor-neutral standard, so one endpoint works everywhere:

```
https://api.melaya.org/mcp
```

Nothing to install, no SDK required.

## Connect

<table>
<tr>
<td width="120" align="center"><img src="assets/clients/claude-code.svg" width="34"><br><b>Claude Code</b></td>
<td>

```bash
claude mcp add --transport http melaya https://api.melaya.org/mcp
```

</td>
</tr>
<tr>
<td width="120" align="center"><img src="assets/clients/codex.svg" width="34"><br><b>Codex CLI</b></td>
<td>

```bash
codex mcp add melaya --url https://api.melaya.org/mcp
```

Direct HTTP needs `experimental_use_rmcp_client = true` in `~/.codex/config.toml`.

</td>
</tr>
<tr>
<td width="120" align="center"><img src="assets/clients/cursor.webp" width="34"><br><b>Cursor</b></td>
<td>

`~/.cursor/mcp.json`, or `.cursor/mcp.json` for one project:

```json
{ "mcpServers": { "melaya": { "url": "https://api.melaya.org/mcp" } } }
```

</td>
</tr>
<tr>
<td width="120" align="center"><img src="assets/clients/anthropic.webp" width="34"><br><b>Claude</b></td>
<td>

claude.ai, Desktop and mobile: **Settings → Connectors → Add custom connector**, paste `https://api.melaya.org/mcp`

</td>
</tr>
<tr>
<td width="120" align="center"><img src="assets/clients/openai.webp" width="34"><br><b>ChatGPT</b></td>
<td>

**Settings → Connectors → Developer mode**, paste the same endpoint

</td>
</tr>
<tr>
<td width="120" align="center"><img src="assets/clients/mistral.webp" width="34"><br><b>Le Chat</b></td>
<td>

**Connectors → Add custom MCP connector**

</td>
</tr>
<tr>
<td width="120" align="center"><b>VS Code</b></td>
<td>

```bash
code --add-mcp '{"name":"melaya","type":"http","url":"https://api.melaya.org/mcp"}'
```

</td>
</tr>
<tr>
<td width="120" align="center"><b>Everything else</b></td>
<td>

Windsurf, Zed, Cline, Goose, Lovable, Gemini CLI, Qwen Code and any other MCP client take the same block, in whichever file that client uses for MCP servers:

```json
{ "mcpServers": { "melaya": { "url": "https://api.melaya.org/mcp" } } }
```

</td>
</tr>
</table>

Authentication is OAuth 2.1 with PKCE. You choose which permissions to grant on a Melaya consent page; the assistant receives a scoped token. Your password is never shared.

Then just ask:

> Connect my phone and go through my unread Instagram DMs.

---

## What it can do

### Operate your phone

Read the screen, open apps, tap, type, scroll, swipe, screenshot. You watch it work, and one control stops everything.

<p align="center">
  <img src="https://melaya.org/blog/july-2026/device-agent-overlay.png" width="300" alt="The agent working, with a live step trace and a stop control">
</p>

Melaya ships navigation playbooks for common apps, so the agent arrives knowing where things are instead of exploring blindly.

<p align="center">
  <img src="https://melaya.org/blog/july-2026/app-playbooks.png" width="680" alt="App playbooks: navigation map, stable control ids, canonical step sequence">
</p>

### Operate a browser

The same read-act-verify loop on a desktop site, through the Melaya extension on Chrome or Edge. **You attach the tab; the model never picks one.**

<p align="center">
  <img src="https://melaya.org/blog/browser-control/live-session.png" width="680" alt="A live browser session, driven step by step">
</p>

It can also **debug** the page it is on: network activity, console output, and a performance diagnosis that ranks causes with the file and the number behind each, rather than handing over a raw panel. Credential values are redacted at capture, before anything reaches the model.

### Build and run agents

List the template library and instantiate a validated template, or author a pipeline from scratch, validate it before saving, schedule it, and watch it run. Hand a long or recurring job to an autonomous agent on your own machine, on your own model subscription, that carries on after the conversation ends.

<p align="center">
  <img src="https://melaya.org/blog/june-2026/agent-builder.png" width="700" alt="The Melaya Agent Builder">
</p>

### Read your connected services

Mail, documents, your ERP. **Read-only, structurally**: the write path is blocked in two independent places, so a write stays blocked even if Melaya's own tool catalog is out of date.

### Find out what happened

Runs, transcripts, tool traces, failure diagnosis, cost, and what your agents have learned across runs.

---

## What it cannot do

Enforced on the device itself, not on the server, so no prompt and no agent instruction can move them.

### It only touches what you allow-list

Apps on the phone, origins in the browser. The agent can hand access back, narrowing the list or clearing it, but **only you can grant it**.

<p align="center">
  <img src="https://melaya.org/blog/device-control/app-permissions.jpeg" width="280" alt="The allow-list, in the Melaya app">
</p>

That asymmetry is deliberate. The agent reads text off your screen, and text can be written by anyone: a message, a comment, a web page. A boundary it could widen in response to what it reads would not be a boundary.

### Publishing and paying always ask you

You see the exact text before it goes out, and approvals reach you even when the phone is locked.

<p align="center">
  <img src="https://melaya.org/blog/july-2026/on-device-approval.png" width="420" alt="An approval card, showing the exact text before it publishes">
  &nbsp;
  <img src="https://melaya.org/blog/july-2026/sleeping-phone.png" width="230" alt="An approval on a locked phone">
</p>

### There is a STOP control

On the phone overlay and in the Melaya app. It halts everything immediately, across every agent and every connected assistant.

### Approvals are listed here, never decided here

The gate exists to put a human between an agent and a consequential action, and the caller here is a model reading untrusted content. You approve in the Melaya app or on your phone.

Password fields are excluded from screen reads.

Also deliberately absent, and enforced by tests rather than by convention: **trading** (it writes against live exchange keys), **administration** (no honest consent sentence exists for it), and **credential values of any kind**.

---

## Permissions

Eight scopes, one per domain. You grant them individually.

| Scope | What it allows |
|---|---|
| `melaya:read` | Your workspace: pipelines, runs, traces, evaluations, pending approvals |
| `melaya:platform` | Your account and plan: tier, usage against limits, subscription |
| `melaya:runner` | Set up and check the Melaya runner on your computer |
| `melaya:phone` | Operate your paired Android phone, inside apps you allow-listed |
| `melaya:browser` | Operate a connected browser, on sites you allowed |
| `melaya:pipelines` | Create, edit, schedule, run and cancel agent pipelines |
| `melaya:connectors` | Read data from connected services. Read only |
| `melaya:team` | Read project membership, and invite people you name |

The tool list your assistant receives is filtered to what you granted, so connecting for phone control alone shows **21 tools rather than all 76**. If a capability seems missing, you declined it; reconnect and approve it.

> [!NOTE]
> **If you also use the Melaya SDK**, "connectors" means something different there. In the SDK it is project credential storage. Here, `melaya:connectors` is reading data from services you already connected. This surface cannot store, read or delete a credential.

## Requirements

- A Melaya account — free at [melaya.org](https://melaya.org)
- An Android phone (Android 8 or newer) for phone control. There is no iOS build.
- The Melaya extension on Chrome or Edge for browser control
- For autonomous agents: Node 18+, Python 3.11+, and a signed-in CLI on the machine hosting the runner

## Privacy

Screen and page content read during a run goes to Melaya and to whichever model you selected, for the duration of that run. The [privacy policy](https://melaya.org/en/legal/privacy) covers collection, retention and deletion.

One credential does cross the boundary, and it is worth naming: if you set up the optional local runner, the command you are given contains a runner token. It is valid for 7 days, revocable in settings or with `melaya_runner_revoke`, and unavoidable because the runner starts from a command line. On a hosted assistant that command appears in your conversation history. Nothing else does; provider and connector credentials are resolved server-side and never reach the assistant.

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
- [Support](mailto:info@melaya.org)

## License

Apache-2.0, matching the [Melaya SDKs](https://github.com/melaya-labs/melaya).

It covers what is in this repository — the registry manifest, the plugin packaging, the skills and this documentation. It is not a licence to the Melaya service itself: using the hosted server at `api.melaya.org` needs a Melaya account and is governed by the [Terms](https://melaya.org/en/legal/terms).
