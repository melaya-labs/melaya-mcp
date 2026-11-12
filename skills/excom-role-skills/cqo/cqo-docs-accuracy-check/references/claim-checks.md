# Claim checks

| Claim type | Example | Verify with |
|---|---|---|
| Count of tools or connectors | "over 200 integrations" | `melaya_connector_list`, `melaya_connector_tools` |
| Templates and validated badges | "40 ready-made templates" | `melaya_pipeline_templates` |
| Models and providers | "works with 20 providers" | `melaya_model_list` |
| A setup or usage flow | "connect in 3 steps" | a run on a throwaway validation pipeline under the validation rule, read with `melaya_run_inspect`; or the UI walked by a human |
| Code fact | "retries 3 times" | the source file named in the note (`gitea_repo_file` or `github_get_file`) |
| Plan limit or price | "unlimited runs on Pro" | the pricing note in the knowledge base and the billing app the CFO holds (ask with `excom_send_handoff`) |
| Capability | "the agent can fill web forms" | a validation run, or the tool list of the connector |
| Safety statement | "nothing is sent without approval" | the tool's write mark in `melaya_connector_tools` and an approval card seen in a validation run |
| Public site page | a product or pricing page | `web_fetch` of the served page |

## House rules to check on every page

- No certification or compliance claim the company does not hold.
- Platform limits stated as they are (for example, which operating systems a feature supports).
- No hidden, beta-internal or unreleased integration named in public copy.
- Banned characters from the house style (often em or en dashes) absent.
- Counts quoted from the canonical numbers source or a live read made this turn, never typed from memory.

## Verdicts

- true: the live read matches the claim.
- false: the live read contradicts it; write the exact replacement wording.
- unverifiable: no read can prove it now; name what would (an app, an account, a human check).

## Weekly sample

Three public pages and one in-app section, picked from pages touched by the last release first, then the most visited.
