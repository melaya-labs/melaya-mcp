# Research rules for model facts

## Fields per model
| Field | Rule |
|---|---|
| model key | the exact id or id family the platform prices |
| context window | the input limit the API enforces, not the marketing headline; if input and output share one budget, record the total and say so |
| max output | separate output cap if stated |
| prices | input, output, cache read, cache write per million tokens; mark REAL (pricing page) or APPROX (inferred from a sibling tier) |
| gating | true when a large window is beta, opt-in or tier-gated; record the exact flag |
| source URL and as-of date | the official page and the date read |
| confidence | high, medium or low, with a one-line reason |

## Source order
1. The provider's own model card and pricing page.
2. The provider's models API (live list) when a key is available.
3. Aggregators and routers as cross-checks only, labelled low confidence.

## Honesty rules
- Version-exact: coder, vision and dated variants often differ; resolve each.
- When sources disagree, prefer the provider's current model card and note the conflict.
- Never borrow a sibling's number, never estimate a missing value, never score from marketing prose.
- No comparable benchmark: record "unscored", not a guess.
- A promotional price always carries its end date and the price after.
- Never copy a key into a note, draft, screenshot or message.

## Triggers for an off-cycle pass
A flagship launch, a retirement notice, an alias that now resolves to a different model, a promotion ending, a provider key turning invalid.
