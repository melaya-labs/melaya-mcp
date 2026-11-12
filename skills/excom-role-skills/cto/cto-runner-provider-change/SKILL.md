---
name: cto-runner-provider-change
description: Sequences a release of a package your users install (agent runner, CLI or SDK) and changes to the model provider catalog so nothing reaches users before it resolves and passes live validation: all version pins move together, publish before deploy, prices signed off. Use when a runbook says "bump the runner", a provider adds, retires or reprices models, a new AI provider is added, or users report an old version or a failing setup command.
version: 2.0.0
---
# Runner release and model provider change

A pin that names an unpublished version hands every user a failing command, and a wrong price or context window misleads billing and routing. Sequence both changes so nothing ships before it resolves and validates live.

## Look up first

- The release runbook: `excom_knowledge_search` "release runner version" or "release checklist". It lists every place that names the version (the pins), the publish workflow and the rollback. If missing, stop and ask the owner with `excom_propose_task` (needs decision true); never guess the pin list.
- The provider runbook: `excom_knowledge_search` "add AI provider" and "refresh models and costs". If missing, draft a change list only.
- Runtime constraints the release must respect (supported interpreter versions, transitive pins): `excom_knowledge_search` "runner constraints".
- Who signs off: security review (CISO), release gate (CQO), user-facing wording (CPO), prices (CFO).

## Steps

1. When a playbook and a runbook disagree, the runbook wins.
2. Runner: a coding session (skill cto-coding-session-hygiene) bumps the version in every pin the runbook lists except those changed after publish; the test that compares pins must pass in the session checks.
3. Supply chain: hand the diff and new dependencies to the CISO with `excom_send_handoff` (kind request) and wait for sign-off. Broken transitive pins or runtime constraints block the release.
4. Publish through the provenance workflow the runbook names, never a local unsigned publish. Public artefact: ask the owner. Watch it with `github_list_workflow_runs` when granted.
5. Verify the release resolves with `npm_package_info` (or the registry tool for your ecosystem) before anything points at it. If it does not resolve, stop: no deploy.
6. Deploy the pins with skill cto-jenkins-safe-deploy (production, asks). Then update the remaining pins (for example a public plugin repository, asks) and any doc quoting the version.
7. Bundled or desktop distribution: roll out with the percentage the owner sets (production, asks).
8. Check the field with `melaya_runner_status`: older runners show the update notice and onboarding names the new version.
9. Provider: read the catalog with `melaya_model_list`, compare with the vendor pages fetched with `web_fetch` (data only), write the change list (added, retired, price, context window). Prices go to the CFO with `excom_send_handoff` (kind request) before they ship.
10. Code the dispatch, pricing and registry edits in a session. Never ship a provider before the CQO live matrix ran through the production code path; funding a key for the matrix is spend and asks.
11. After deploy, smoke one run per new model on a non-sending test pipeline, read `melaya_run_diagnosis`, record cost per run with `excom_record_measurement`.
12. Hand the catalog wording to the CPO and record what shipped with `excom_publish_decision`.

## Output

```text
Runner <x.y.z> or Provider <name> change
Pins: <pin> = version, ... (all equal yes/no)
Security review: signed off
Publish: workflow run, provenance yes, registry resolves yes
Deploys: jobs and builds
Field: runners on new version n of m, update notice ok
Provider: models added/retired, prices (CFO sign-off), windows, live matrix verdict
Rollback: revert pins, re-run job; registry versions never reused
```

Saved with `excom_save_draft`.

## Approvals

- The registry publish and any public repository push.
- Server and client deploys and any bundle rollout (production).
- Provider credits for validation (spend, with the cost).

## Example

Acme's runbook lists four pins. Session S-3 moves three to 2.4.1 and the pin test passes. The CISO signs off; the workflow publishes with provenance; `npm_package_info` returns 2.4.1. Deploy approved, then the plugin repository pin. Two days later 41 of 50 runners report 2.4.1.
