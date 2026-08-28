---
description: Check the Melaya connection and fix whatever is missing — pairing, app permissions, the local runner
---

Check the user's Melaya setup and get it working.

1. Call `melaya_setup_status`.
2. Report what is ready and what is not, in plain language — do not just dump the JSON.
3. Act on the first unmet requirement. Its `action` field names the exact fix.
   - If it is a command AND you have shell access on the user's own computer, run it yourself in a background shell.
   - If it is a command and you do not — you are on claude.ai, mobile, or another hosted surface — give the user the command to copy, and say that it must run on the machine that will host the Melaya runner, not on a server. Never report starting a runner you could not start.
   - If it needs the user (installing the app, enabling the accessibility service, signing into `claude`), tell them precisely what to do and why.
4. Re-check with `melaya_setup_status` and keep going until it reports ready, or until you are blocked on something only the user can do.

Finish by telling them what they can now ask for.
