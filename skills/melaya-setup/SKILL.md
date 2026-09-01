---
name: melaya-setup
description: Use for anything involving Melaya. Connecting for the first time; setting up phone or browser control; pairing a phone, installing the app, starting the local runner; driving an Android phone or a browser; building, validating, scheduling or debugging agent pipelines; reading connected services; diagnosing a failed run. Also use for "why can't Claude see my phone", "melaya says no device", "runner not connected", "that app is not allowed", "the pipeline lost a field I set", or any Melaya tool that fails in a way that looks like setup.
---

# Operating Melaya

Melaya gives you the user's own account: their Android phone, a browser they connected, their agent pipelines, the services they authorised, and the record of what every run did. Seventy-six tools across eight permissions.

This skill is the operating discipline. Read the section for what you are about to do; the traps in it are real failures, not hypotheticals.

## Always start here

Call `melaya_setup_status`.

One call returns every requirement with a done flag, and every unmet one comes back with the exact command or URL that fixes it. Do not guess at what is missing, and do not walk the user through a checklist the tool has already answered. One call, then act on `nextStep`.

Call it again after any Melaya tool fails in a way that smells like setup rather than like a mistake: "no device", "no runner", "app not allowed", "no allowed sites".

## Two things that shape everything you do

**Where you are running** decides what you can do about a command. With shell access on the user's own computer, run it. Without it, on claude.ai or mobile or any other hosted surface, hand the command over and say which machine it belongs on: the runner exists to execute where the user's own credentials and hardware are. Never report having started something you could not start.

**What you can see** depends on what the user granted. Your tool list is already filtered to their consent. If a capability is missing it is because they declined it, not because Melaya lacks it. Say that plainly and offer to have them reconnect. Do not hunt for another route to the same thing; there isn't one, and looking is the wrong instinct.

## Setting up

**1. A Melaya account.** They already have one if the connection authorised at all; OAuth cannot complete without it.

**2. A paired Android phone.** Call `melaya_phone_pair`. It returns an 8-character code valid for five minutes plus an install link. The user opens that link on the phone, installs, and enters the code.

Say these out loud, because each one surprises people:

- It is a direct APK download, not a Play Store install, so Android asks them to allow installing from this source. That prompt is expected.
- There is no iOS build. Android only.
- After installing they must enable the Melaya accessibility service in Android Settings. That is what lets the agent read the screen and tap. Nothing works without it.
- Battery optimisation should be disabled for the app, or Android stops it responding when the screen is off.

**3. Allow-listed apps.** Pairing on its own grants nothing. Call `melaya_phone_apps` to see what is installed and what is already allowed, then tell the user which apps this task needs. They grant them in the Melaya app or on the phone.

There is no tool that adds one, and asking for it is not a workaround. `melaya_phone_restrict_apps` can only **narrow**: every package you submit must already be allowed, and anything you omit loses access, so read the current list first and include everything that should stay.

**4. A paired browser**, only if the task needs a desktop site. `melaya_browser_pair`, then the user installs the Melaya extension on Chrome or Edge and clicks Connect. Then `melaya_browser_attach` for the tab they want.

Browser control needs at least one allowed origin, added by the user on the Melaya browser page. An empty list is refused rather than treated as "all sites"; that choice only exists on a screen that can ask for it properly.

**5. The local runner**, only for autonomous agent runs, not for driving a device directly. Call `melaya_runner_setup`. It mints a token and returns the exact `npx` command.

With shell access, run it in a background shell and poll `melaya_runner_status` until connected. Without, give the user the command and say plainly that it runs on their own machine, not on a server. First start takes up to a minute while it builds a Python virtualenv; it needs Node 18+ and Python 3.11+ on PATH. Treat the token as a credential: do not write it anywhere they might commit. `melaya_runner_revoke` kills one.

**6. Claude Code signed in on the runner machine**, if phone agents will use the user's own Claude subscription. If `melaya_setup_status` reports it unavailable on a connected runner, the fix is `claude` once in a terminal, then restart the runner. No API key, no connector.

## Driving a device

Phone or browser, one loop, every time:

1. **Read.** `melaya_phone_screen` or `melaya_browser_screen`.
2. **Act on a specific element.** Prefer clicking by text or resource id over tapping coordinates. Ids survive a layout change; coordinates do not.
3. **Read again** to confirm what actually happened.

Never act on an assumption about what is in front of you. If a screen returns no readable elements it is a canvas, a game or a video: take a screenshot and read the image yourself. You have vision. **Never ask the user to describe their own screen** — that is a failed run.

Before working in an unfamiliar phone app, call `melaya_phone_playbook`. Melaya keeps navigation notes, real resource ids and known traps for common apps, and reading them first saves many wasted turns.

`melaya_phone_batch` and `melaya_browser_batch` exist for sequences you are confident about. Keep them short: each step is re-gated server-side and the batch aborts at the first failure, so a long batch that fails early wastes more than it saved.

If the user says stop, call `melaya_phone_stop` or `melaya_browser_stop` immediately.

## Building a pipeline

**Prefer a template.** `melaya_pipeline_templates` lists validated ones; `melaya_pipeline_from_template` instantiates with overrides. This avoids every trap below, because the payload is already correct.

Hand-authoring, when no template fits, is a three-step loop and skipping the middle step is the most common way to waste the user's time:

1. Write the config.
2. **`melaya_pipeline_preview`.** Free, unpersisted, no quota.
3. `melaya_pipeline_save`.

Then read it back with `melaya_pipeline_get`.

The traps, all real:

- **Unknown fields vanish silently.** The builder ignores what it does not recognise and still answers 200. A clean save proves nothing. Preview returns the code it would generate; check that every field you authored actually appears in it.
- **Author with `steps[]`, not the flat `agents[]` list.** The flat form requires fields a minimal agent does not have and will be rejected.
- **The name you send is not the name you get.** Names are normalised on save. Use the canonical name from the response for every later get, run or delete, or they 404.
- **Discover ids, do not invent them.** `melaya_pipeline_registry` for tool and agent ids, `melaya_model_list` for provider and model strings. A guessed model id is accepted silently and fails at run time, which is the worst failure on this surface because nothing points at the cause.
- **Never inline a credential.** A config carrying an API key is refused. Credentials live in Connectors and are resolved server-side at run time.
- **Gate every write-capable tool.** Put send, post, payment and external-write tool ids into the agent's `human_approval_tools`. The registry tells you which tools are read-only.

`melaya_pipeline_schedule` arms the cron separately from the config. A `schedule` field in the config alone does not start anything.

## Reading connected services

`melaya_connector_list` shows what is connected, `melaya_connector_tools` what those services unlock, `melaya_connector_call` reads.

**Read-only, structurally.** There is no write path and no argument that creates one. If a task needs something sent or changed in a connected service, the answer is a Melaya pipeline that includes it, not a different call here.

`melaya_connector_test` turns "the pipeline failed" into "your Odoo key is dead" in one call. Reach for it before debugging anything else.

## When a run fails

`melaya_run_status` first, and read `outcome`, never `status`: every finished run reports `status: "done"` whether it succeeded or not.

Then `melaya_run_diagnosis` for per-phase verdicts and tool forensics, or `melaya_run_inspect` for what the agents actually said and did. `melaya_eval_report` answers the wider question: what fails most, and what does it cost.

If a run is stalled rather than failed, check `melaya_approval_list`. It is probably waiting on a human.

## Four boundaries you cannot move

All enforced by the device or the platform, not by these instructions. If an action is refused, explain what happened and ask. There is no way around it, and looking for one is the wrong instinct anyway: you read text off the user's screen, and a boundary you could widen in response to what you read would not be a boundary.

1. **The allow-list.** Apps on the phone, origins in the browser. You can hand access back, never take more.
2. **Publishing and paying.** Both stage an approval and wait for a person. You see the exact text first; so do they.
3. **Approvals are listed, never decided.** `melaya_approval_list` shows the queue. The user approves in the Melaya app or on their phone.
4. **No credentials, no trading, no administration.** Not gaps to work around; they are not on this surface at any permission.

## Driving directly vs launching an agent

Drive the device yourself when the task is short, exploratory, or something the user is watching. It is faster and they can see what is happening.

Use `melaya_run_phone_agent` when the task is long or repetitive and should keep going after this conversation moves on. It needs a connected runner with a signed-in CLI, and returns a run id you poll with `melaya_run_status`.

## When nothing else fits

`melaya_gateway_list` lists the read-only platform toolkit; `melaya_gateway_call` runs one. Search that before concluding Melaya cannot do something.

It reports how many entries it withheld for lack of permission. A non-zero count means the user declined that scope, not that the tool is gone.
