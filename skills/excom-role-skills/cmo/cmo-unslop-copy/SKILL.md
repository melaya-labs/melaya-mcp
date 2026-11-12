---
name: cmo-unslop-copy
description: Cleans any public copy before it reaches an approver: grounds every claim in sourced facts, puts the answer first so search and AI answer engines can quote it, and removes AI writing tells against the team's brand voice. Use when a page, post, email, listing or reply draft is ready for review, when pipeline output sounds generated, or when someone says the copy "sounds like AI", "too salesy" or "off brand".
version: 2.0.0
---
# De-slop copy for brand voice and answer engines

The last gate before a human sees a draft. Three passes in order: ground the claims, shape for extraction, strip the tells. Generated filler loses readers, and answers buried under preamble never get quoted.

## Look up first

- The brand voice and banned words: `excom_knowledge_search` "brand voice", "words we never use", "positioning", then `excom_knowledge_read`. For a social surface also `social_brand_voice` for that platform. Missing: apply references/slop-table.md alone and propose a voice note with `excom_save_draft`.
- Product facts, counts and prices: search "products", "pricing and plans".
- Surface rules (link policy per platform, register per language, closing style): the same voice note. Missing: ask the owner with `excom_propose_task` (needs decision) for the link policy before any social draft ships.

## Steps

1. Identify the surface (page, company post, founder post, short post, community reply, email, listing) and the language.
2. Pass 1, grounding. Every claim names a mechanism or a number. Replace feelings with mechanics ("asks for your approval before it posts" beats "safe and seamless"). Check each number against the notes read this turn. A number you cannot source becomes a NEEDS FACT marker for the approver, never a guess. Competitor-swap test: a paragraph that could sit unchanged on a rival's site is rewritten around something specific to you, or cut. Remove "experts say" and "many teams find".
3. Pass 2, answer-engine shape (pages and long posts). Direct answer in the first 40 words. At least one H2 phrased as the buyer's exact question, followed by a one or two sentence answer. Sentence case headings, no skipped levels. Comparison items in identical self-contained blocks (verdict, best for, trade-off, price).
4. Pass 3, the tells. Fix every pattern in references/slop-table.md, plus the team's banned words.
5. Apply the surface rules from the voice note: link policy, register, hashtags, closing line, disclosure.
6. Read once for rhythm: split sentences over 30 words, vary length.
7. Save the clean version with `excom_save_draft` next to the original, with the receipt. Publishing happens in the skill that owns the channel, and asks there.

## Output

```text
Unslop receipt: <draft> (<surface>, <language>)
First 40 words: now lead with <answer>
Headings: N converted, question H2 added: <text>
Grounding: N vague claims replaced; NEEDS FACT markers: N (list)
Tells removed: N dashes, N banned words, N filler clauses
Surface rules checked: links, register, closing, disclosure
```

## Approvals

- Nothing is published or sent from this skill (send happens in the channel skill, with approval).
- Open NEEDS FACT markers go to the approver, never filled with guesses.

## Example

Before: "In today's fast-paced world, Acme seamlessly empowers teams to transform scheduling." After: "Acme builds next week's rota from your staff's availability in about a minute, then asks a manager to approve it before anyone is notified."

## References

- references/slop-table.md: the 20 patterns to remove, with fixes. Loads with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (content/unslop-seo/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
