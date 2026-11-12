# Cost and latency fix catalog

Apply in this order and measure after each one before moving on. Savings ranges are typical, never a promise: only the after-measurement counts.

## Model spend

| Fix | When it applies | Typical effect | Measure with |
|---|---|---|---|
| Instrument per-request tokens | any driver without model, input tokens, output tokens, step and cost logged | makes the rest possible | per-step cost table |
| Route by complexity | classification, extraction, formatting, short summaries on a large model | large cut on routed traffic | cost per accepted run, CQO comparison on the same cases |
| Prompt caching | long static system prompts or repeated context sent on every call | large cut on cacheable input | cache hit rate, input cost |
| Output caps per step | steps without a max output or structured output | moderate cut | output tokens per step |
| Prompt trimming | context repeated between system and user turns, filler instructions | moderate input cut | input tokens per step |
| Fewer calls | loops or retries that re-ask the model for the same thing | depends on the loop | calls per run |

Rules:

- Tiers, not model names: small, mid, large. Model names churn; check the provider list at the time.
- A system prompt above roughly 2,000 tokens sent on every request is a high-value caching target.
- An endpoint with no output cap is a cost leak.
- Never call a cheaper route a win before the quality comparison passed.

## Latency and capacity

| Symptom | First measurement | Typical fix |
|---|---|---|
| Queue refusals | queue depth and lanes in use over time | lane sizing, shorter runs, scheduling heavy jobs off peak |
| Slow API route | p95 and p99 by route, slow query log | the measured query or payload, an index, pagination |
| Memory climb | memory per run over time, restarts | the leaking component found by comparison, never a blind restart schedule |
| Slow page (LCP) | Core Web Vitals per money page | render the largest element without waiting for scripts, fonts and images sized and preloaded |
| Bundle growth | bundle size per release | split the heavy dependency, remove the unused one |

Rules:

- Measure first, then change one thing, then measure again with the same window and load.
- Load tests and profilers run on test environments, never on production without the owner's approval.
- Paid profiling or monitoring tools are optional and always ask with the cost.
