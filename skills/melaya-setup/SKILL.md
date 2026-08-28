---
name: melaya-setup
description: Use when connecting Melaya for the first time, when a Melaya tool reports something missing, or when the user asks to set up phone control, pair a phone, install the Melaya app, start the Melaya local runner, or fix a Melaya connection. Also use for "why can't Claude see my phone", "melaya says no device", "runner not connected", or any Melaya onboarding question.
---

# Setting up Melaya

Melaya gives you control of the user's Android phone and their agent pipelines. Getting there takes a few pieces of setup.

How much of it you can do yourself depends on where you are running. In Claude Code you have shell access on the user's own computer, so run the commands. On claude.ai, mobile, or any other hosted surface you do not — give the user the command to run and say which machine it belongs on. Never report having done something you could not do.

## Always start here

Call `melaya_setup_status`.

It returns every requirement with a done flag, and every unmet one comes back with the exact command or URL that fixes it. Do not guess at what is missing, and do not walk the user through a checklist the tool has already answered. One call, then act on `nextStep`.

Call it again after any Melaya tool fails in a way that smells like setup — "no device", "no runner", "app not allowed".

## The five things that have to be true

**1. A Melaya account.** The user already has one if the connection authorised at all; OAuth cannot complete without it.

**2. A paired Android phone.** Call `melaya_phone_pair`. It returns an 8-character code valid for five minutes plus an install link. The user opens that link on the phone, installs the app, and enters the code.

Things worth saying out loud when you walk them through it:

- It is a direct APK download, not a Play Store install, so Android will ask them to allow installing from this source. That prompt is expected.
- There is no iOS build. Android only.
- After installing they must enable the Melaya accessibility service in Android Settings. That is what lets the agent read the screen and tap; nothing works without it.
- Battery optimisation should be disabled for the app, or Android will stop it responding when the screen is off.

**3. Allow-listed apps.** Pairing on its own grants nothing. Call `melaya_phone_apps` to see what is installed, then `melaya_phone_allow_apps` with the apps the user names.

`melaya_phone_restrict_apps` can only **narrow** the list. Every package you submit must already be allowed, and anything you omit loses access — so read the current list first and include everything that should stay.

You cannot add an app. If a task needs one the user has not granted, ask them to add it in the Melaya app or on the phone. That restriction is deliberate: you read text off the user's screen, and an agent that could widen its own permissions in response to what it reads would effectively have none.

**4. The local runner.** Needed only for autonomous agent runs, not for driving the phone directly.

Call `melaya_runner_setup`. It mints a token and returns the exact `npx` command.

If you have shell access on the user's own computer, run it in a background shell and poll `melaya_runner_status` until it reports connected. If you do not, give the user the command and tell them plainly that it runs on their own machine, not on a server — the runner exists precisely to execute where their Claude Code credentials and local resources are.

First start takes up to a minute while it builds a Python virtualenv. It needs Node 18+ and Python 3.11+ on PATH. Treat the token as a credential: do not write it anywhere the user might commit.

**5. Claude Code signed in on the runner machine.** Phone agents run on the user's own Claude subscription, read by the runner from their local Claude Code install. If `melaya_setup_status` reports Claude Code unavailable on a connected runner, the fix is for the user to run `claude` once in a terminal to sign in, then restart the runner. There is no API key and no connector to configure.

## Driving the phone

One loop, every time:

1. `melaya_phone_screen` — see what is actually there.
2. Act on a specific element. Prefer `melaya_phone_click` by text or resource id over `melaya_phone_tap` by coordinate; ids survive layout changes and coordinates do not.
3. `melaya_phone_screen` again — confirm what happened.

Never act on an assumption about what is on screen. If the screen returns no readable elements it is a canvas, game, or video surface: use `melaya_phone_screenshot` and read the image yourself. You have vision. Never ask the user to describe their own screen — that is a failed run.

Before working in an unfamiliar app, call `melaya_phone_playbook`. Melaya keeps navigation notes, real resource ids, and known traps for the common apps, and reading them first saves many wasted turns.

## Two boundaries you cannot move

The app allow-list and the publish/payment approval gate are both enforced on the phone itself, not on the server, and neither can be moved from here — you can hand access back, never take more. If an action is refused, explain what happened and ask the user. Do not look for a way around it; there isn't one, and trying is the wrong instinct anyway.

If the user says stop, call `melaya_phone_stop` immediately.

## Driving directly vs launching an agent

Drive the phone yourself with the `melaya_phone_*` tools when the task is short, exploratory, or something the user is watching. It is faster and they can see what is happening.

Use `melaya_run_phone_agent` when the task is long or repetitive and should keep going after this conversation moves on. It needs a connected runner with Claude Code signed in, and it returns a run id you poll with `melaya_run_status`.

## When something is not covered by a dedicated tool

`melaya_tools` lists the Melaya platform toolkit — pipelines, runs and traces, agent memory, RAG stores, project and cost data. `melaya_call_tool` runs one. Search that list before concluding Melaya cannot do something.

That gateway does not reach the user's third-party connectors (Gmail, Slack, ERP systems). Those are registered per-conversation inside the Melaya Assistant. To use one, run a Melaya pipeline that includes it, or point the user at the Melaya Assistant.
