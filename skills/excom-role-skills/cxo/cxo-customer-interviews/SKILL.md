---
name: cxo-customer-interviews
description: Runs small, honest interview rounds (five to ten conversations) or a short survey with paying customers, stalled trials, churned users or partners' clients: recruit from first-party data, script, consent, synthesise into counted themes, and route findings. Use when a decision needs the customer's own words, when a feedback theme has low confidence, for a monthly round with new customers, or when someone asks "why did they buy" or "why did they leave".
version: 2.0.0
---

# Customer interviews

First-hand reasons beat guesses for every product, pricing and messaging decision, and a small honest round is enough when the question is precise.

## Look up first

- The decisions pending in the team (from your tasks and `excom_recall` "open decisions") to pick the one question.
- Priority audiences and personas: `excom_knowledge_search` "audiences", "personas".
- Prior research and voice-of-customer reports: search "voice of the customer", "interviews".
- Consent and recording policy: search "privacy policy", "research consent". Missing: record nothing and ask the CLO.

## Steps

1. Write the brief: one decision, the hypothesis to disprove, who to talk to, how many (aim 10, accept 5), and what result would change the decision. Save with `excom_save_draft`.
2. Recruit from first-party data: paying customers (`stripe_list_subscriptions`), activated and stalled users (`melaya_tools`, `posthog_get_cohort` when granted). Partner clients only through their partner. Exclude staff, test accounts and anyone who opted out.
3. Draft a three-line invitation with a real reason, 20 minutes, and a booking link (`calendly_list_event_types`), in their language. Draft class; each send asks. One invitation and one reminder per person.
4. Run the script in references/interview-script.md. No leading questions, no pitching, no promises.
5. For larger samples, a survey under ten questions with one goal (references/interview-script.md). Drafts only; sending asks.
6. Consent: say how notes are used, record only with explicit consent, keep personal data out of shared notes.
7. Synthesise: one note per interview with labelled quotes; themes ranked by frequency and intensity with exceptions and the sample bias. Separate what people did from what they say they would do.
8. Route: product themes to the CPO, buying reasons and objections to the CRO, language and positioning to the CMO (`excom_send_handoff` kind request). Record interviews held and the "very disappointed" share with `excom_record_measurement`.

## Output

```text
Decision: <one sentence> | Hypothesis tested: <one>
Sample: <n> (<segments>), recruited from <source>, bias: <note>
Themes: <theme> | <n of N> | quotes | exceptions
Very disappointed: <x of N> | What changes: <implication> | Owner: <role>
```

## Approvals

- Every invitation, reminder and survey send: send class.
- Incentives (gift cards, credits, swag, extra plan time): spend or a plan change, never default, ask with the cost.
- Recording a call or sharing a quote outside the team: the participant's explicit consent first.

## Example

Decision: should onboarding lead with templates or with connecting tools? 7 interviews with users activated last month: 5 of 7 started from a template, 2 connected tools first because their job required one specific app. Implication: templates first, with a "connect your app" shortcut. Owner: CPO.

## References

- references/interview-script.md: the 20-minute script, the five-why method and survey rules. Read at steps 4 and 5; loads with `excom_skill_load` (section) or by paging.

Adapted from coreyhaines31/marketingskills (skills/customer-research/SKILL.md), MIT licence, and gtmagents/gtm-agents (plugins/customer-feedback-orchestration/skills/survey-design/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
