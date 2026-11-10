# Share copy and publishing package

> **Use when:** writing the caption that ships with a piece, the per-platform post copy, YouTube titles, descriptions and chapters, a Product Hunt kit, or assembling the final delivery folder and handing it to the user.
> **Inputs:** the render and poster, `brief.md` (share line, CTA, platforms), the voice card, `assets/ledger.md`.
> **Outputs:** `share-copy.txt`, optional `share-copy-variants.md`, the publishing package (template: [../templates/publishing-package.md](../templates/publishing-package.md)), a short report to the user.
> **Next:** done; publishing itself only after the user's yes.

## share-copy.txt

One canonical caption, postable as is: one to three sentences, specific to this product, in the piece's tone, using the product's own words. Never "excited to share", never generic SaaS language, no hype words, no claims the video does not show. Variants for other platforms go in `share-copy-variants.md`, never in this file.

| Tone | Shape |
|---|---|
| playful | "Made {product}. It {does the thing, in the product's own terms}. {Best line from the product}." |
| polished | "Introducing {product}: {clean one-liner from the source}." |
| startup-parody | "We built {product} to solve {problem stated completely seriously}. {Deadpan fact}." |
| chaotic | "{SHORT CLAIM IN CAPS}. {Product} is {overstated description}. Link below." |
| deadpan | "I made {product}. It {does the thing}." |
| cinematic | "{Product}. {Tagline, verbatim or lightly adapted}." |
| feature-cards | "{Product} is live. {Feature 1}, {feature 2} and {feature 3}, in one place." |

## Per-platform copy

| Platform | What to write |
|---|---|
| X | the hook line first, at most 280 characters on standard accounts; the link in the post or the first reply; 0-2 hashtags |
| LinkedIn | the first 210 characters carry the hook and the promise (that is what shows before "see more"); short paragraphs; the CTA and URL at the end; 3 hashtags at most; upload the SRT |
| Instagram, TikTok | the first line is the hook; the CTA in the caption ("link in bio" only if it is true); 3-5 specific hashtags; alt text for carousels |
| YouTube | title "{benefit} \| {product}" under 100 characters; description: hook, what it is, a feature list, how to start, the canonical URL (verified), caption languages, chapters, 3-5 hashtags; tags about 470 of 500 characters, specific first; chapters at 0:00 then at least two more, each at least 10 s, timed from the render |
| Product Hunt | name, tagline (about 60 characters), description (about 260), gallery images and the video link, topics, and the maker's first comment: why it exists, who it is for, what is next, an honest ask for feedback |

CTA honesty: never promise access, keys, invites or replies that are not actually offered at publish time. The default is the canonical URL and "available now" or "follow along".

## Distribution sequence (when the user wants a plan)

| When | What |
|---|---|
| T+0 | the primary platform with the master format |
| T+4 h | the short vertical cut on a second platform |
| T+24 h | a reply or follow-up clip answering the top comment |
| T+48 h | communities where the audience gathers, with a native post rather than a bare link |

A pinned comment carries the link and one line of context. Every cut is its own render, never a crop.

## The delivery folder

```text
content-output/<slug>/
  <slug>_<format>_<lang>.mp4      one file per format and language, poster baked as frame 0
  poster.jpg                      the poster frame (custom thumbnail where platforms accept one)
  thumbnail_1280x720.jpg          when YouTube is a target
  captions.<lang>.srt / .vtt      sidecars per language
  share-copy.txt                  the canonical caption
  share-copy-variants.md          per-platform copy (optional)
  publishing-package.md           titles, descriptions, chapters, hashtags, alt text, attributions
  brief.md  script.md  storyboard.md  composition/  assets/ledger.md  qa/
```

Attribution lines required by asset licences (from the ledger) go into the package and, where the licence requires it, into the description.

## Telling the user

Report in a few lines: where the video, poster and copy are; one sentence on the creative angle; the duration, formats and languages; any limitation (a missing asset, a fallback font, a step left to them); and an offer to re-roll a scene, try another tone or make another format. Never post, upload or schedule anything without the user's explicit yes.

## Gate

`share-copy.txt` exists and is specific; the package lists every deliverable with its platform copy; required attributions are present; nothing was published without a yes.
