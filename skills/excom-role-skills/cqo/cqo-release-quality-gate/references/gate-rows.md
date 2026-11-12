# Generic release gate rows

Use these when the team's release checklist is missing, or to check it covers the basics. Replace the generic command names with the exact ones from the checklist.

| Row | Requires (read this turn) | Not sufficient |
|---|---|---|
| Client | the app's own typecheck configuration, tests and lint, each with 0 failures | a default typecheck config, "looks fine" |
| Server | build, tests, lint, and any tool-surface or API contract check, with 0 failures | a green typecheck alone |
| Agents or workers | the full test folders and any code generation parity check | one test file passing |
| Runner, SDK or package | every place that pins the version names the same version, and the release resolves in the registry (`npm_package_info`, `pypi_package_info`) | a version bumped in one place |
| Desktop or mobile | the packaging gate, signing on a tag, installer or package scan | a local build |
| Order | dependencies published before the code that pins them; migrations applied by their author; deploy jobs in the documented sequence | "we will deploy together" |
| Covering test | red then green on the original symptom | code changed, assumed fixed |
| Acceptance | each criterion line checked with a run, a test or a dashboard read | tests passing |
| Docs and strings | user-facing text present in every supported locale, docs claims updated | English only, "docs later" |
| Post-deploy | first real run of each touched surface judged by its artifact | build status green |

## Evidence words

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | the test command output with 0 failures | a previous run, "should pass" |
| Build succeeds | the build output, exit 0 | lint passing, logs look good |
| Bug fixed | the original symptom re-run and passing | code changed |
| Regression test works | seen red, then green | passes once |
| Agent or engine done | the diff and checks of the session | the engine's summary |
| Requirements met | each criterion line checked | tests passing |

## No-go wording

State the row, the missing proof, and who can produce it. Example: "Server: no contract check output in the session; the CTO to run it in the session checks or add it to the grant's checks."
