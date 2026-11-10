# Brief and intent capture

> **Use when:** a new piece starts, a request is vague ("make a video about this"), or the goal, audience, format or length is not written down yet.
> **Inputs:** the user's request; any source (website URL, code repository, asset folder, document, earlier video).
> **Outputs:** `brief.md` in the output folder (template: [../templates/brief.md](../templates/brief.md)), with the rubric answered and the defaults stated.
> **Next:** [brand-kit.md](brand-kit.md) for identity, then [narrative.md](narrative.md) for the story.

The brief is the contract every later step is checked against. One page. It says what the piece must make a stranger understand, not how it is animated.

## Ask little, default the rest

Ask at most three questions, and only the ones whose answer changes the piece. Everything else takes a default you state in the brief ("Assumed: landscape 1920x1080, 20 s, music on, no voiceover"). The user corrects defaults faster than they answer questionnaires.

| Decision | Ask when | Default |
|---|---|---|
| Goal (launch, feature, explainer, ad, recap, teaser, tutorial) | never obvious from the request | launch / announcement |
| Audience and where they see it | the platform is not named | the product's own users and buyers; landscape for site and YouTube |
| Subject and focus | the source has several products or features | the newest or most distinctive feature |
| Length | the platform has hard limits or it is a film | 18-22 s for a clip; 45-75 s for a narrated explainer |
| Format | several platforms | one master format, then rebuilt versions ([platforms.md](platforms.md)) |
| Tone | the brand voice is ambiguous | inferred from the source; see [../styles/](../styles/) |
| Voiceover and captions | explainer, tutorial, ad | off for a 15-25 s clip, on for anything that must explain |
| Music and SFX | never, unless silence is the idea | on, restrained |
| Call to action | ads and launches | the canonical URL or "available now" |
| Languages | international audience | the source language only |

Freeform direction ("like a fake 2016 Series A launch", "museum exhibit") is kept verbatim in the brief and mapped to the nearest tone preset for pacing.

## Read the source before you answer

| Source | Read, in order | Skip |
|---|---|---|
| Code repository | main page and its styles (exact colours and fonts), README, package manifest name and description, routes and key feature components, demo or example folders, `public/` or `assets/` | build output, lock files, tests, `.git/`, environment and secret files, keys, anything `.gitignore` hides for those reasons |
| Website URL | the page as a visitor sees it (a plain download can be an empty shell: render it in a headless browser, dismiss banners, scroll section by section), title, meta and social-preview tags, hero copy, section headings, CTAs, testimonials, demo videos, docs | logged-in areas unless the user provides access |
| Asset folder | logo files, brand guide, fonts, screenshots, footage, past videos | |
| A plain text request | what it says; ask for one real asset (logo or URL) if there is nothing to show | |

The strongest material is the product in use, not the product describing itself. Find its 2-3 beats: **entry, key action, result** ("drop a long video, watch it process, three vertical clips are ready").

## The rubric (answer all ten in the brief)

1. **What is it?** One sentence a stranger understands. What it does, not how it is built.
2. **Who is it for, and what does it do for them?**
3. **What sets it apart?** The one claim competitors cannot make.
4. **The strongest line.** The most impressive or funniest real claim from the source, verbatim.
5. **The visual hook.** The strongest visual the source owns: a UI moment, a palette, a diagram, an object.
6. **The flow worth showing.** Entry, key action, result; or "none: landing page only" and the hook visual carries it.
7. **The shortest satisfying length.** The minimum that lands the claim; cut everything else.
8. **Tone.** A preset plus a short creative direction in the user's words.
9. **Audio.** The role of sound: warm bed, sparse accents, cinematic support, dense rhythm, voiceover, or deliberate silence.
10. **The share line.** One sentence that would sit under the post.

A piece whose rubric cannot be answered is not ready to build: the missing answer is your next question.

## Nothing secret leaves the brief

Everything read here can end up in a public video. Never carry secrets, keys, tokens, internal hostnames or URLs, real customer or user names, emails or personal data into the brief, the script, the composition, the render or the copy. When the real UI shows such data, plan fictional stand-ins and say so in the brief.

## Gate

`brief.md` exists, the ten answers are filled, the defaults are listed, and the user has seen it (or, in an unattended run, it is the first thing reported). Then move on; do not wait for approval of a brief the user did not ask to approve.
