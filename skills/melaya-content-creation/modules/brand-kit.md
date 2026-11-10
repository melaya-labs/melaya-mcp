# Brand kit extraction

> **Use when:** a piece needs the identity of a brand or product: colours, fonts, logo, voice, product UI, motion habits; from a website, a code repository or an asset folder.
> **Inputs:** the source named in the brief.
> **Outputs:** `brand-kit.md` (tokens, fonts, logo files, voice card, UI inventory, motion vocabulary) and the logo and font files copied into `assets/`.
> **Next:** [design-system.md](design-system.md) turns the kit into a design for the format; [narrative.md](narrative.md) uses the voice.

A kit is extracted, never imagined. Every value cites where it came from (file and line, or page and selector). When a value cannot be found, say "not found" and choose a neutral fallback, labelled as a fallback.

## Where each value comes from

| Value | Code repository | Website | Asset folder |
|---|---|---|---|
| Colours | `:root` custom properties, theme or token files, utility-framework config, design-token JSON; else the most used background, text and border colours | computed styles of `body`, headings, primary buttons, links, cards (read in a headless browser) | brand guide |
| Fonts | `@font-face`, font imports, the font family on `body` and headings; font files in the repo | the font stylesheet links and `@import`s, computed `font-family` of headings and body | font files and the guide |
| Logo | SVG in the assets or public folder, the app icon | inline SVG in the header, the icon links, the social-preview image | logo files (prefer SVG, then the largest PNG with transparency) |
| Voice | README tone, UI strings, marketing pages in the repo | hero, headings, CTAs, error and empty states | guide, past posts |
| Product UI | routes and components of the key flow, their states, real labels | screenshots of the key flow at the video's aspect ratio | screenshots, recordings |
| Motion | the product's own animations (transitions, loaders, hovers) | the same, observed in the browser | past videos |

Keep the real logo files untouched. A morph may end on a vector stand-in, but the final frame always shows the real artwork ([morphs.md](morphs.md)).

## Tokens: roles, not a palette dump

Name colours by role. A film uses at most five tokens plus neutrals; two accents visible at once at most.

| Token | Role | Rule |
|---|---|---|
| `ground` | the background of most scenes | dark and light grounds may alternate between scenes |
| `surface` | raised cards and panels | slightly lighter than the ground (dark) or white on pale grey (light) |
| `text` | primary text | contrast at least 4.5:1 on ground and surface (WCAG AA) |
| `muted` | metadata, secondary text | `text` at about 60% alpha, still readable |
| `accent` | the one attention colour | used for meaning only ("this needs you", the payoff word), never decoration |
| `accent-2` | secondary product colour | only where the real UI uses it |
| `success`, `warning` | states | only on real states (approved, failed) |

Copy chrome tokens (surfaces, borders, shadows) from the product's design variables verbatim, as hex, so values stay searchable. Accent tokens are for emphasis only. Check text and accent contrast on both grounds before the design step.

## Fonts

- Record a display face (headlines, lockups), a text face (UI, captions) and a monospace (code, URLs, counters). Two families is better than three.
- Check the licence allows embedding in video. Use the files from the source; otherwise a free family of the same class (geometric sans, grotesk, humanist, slab, serif, condensed) and say so.
- Keep one static file per weight you use (a variable font file can lose weights in some capture paths), plus TTF or OTF copies for subtitle burn-in tools.
- The brand's own font overrides any "overused font" lint warning. Never copy a reference video's typefaces.

## Voice card

Three or four adjectives, the register (formal or informal address), sentence length, words the brand uses, words it never uses, punctuation habits, and five real lines from the source that show the voice. Default copy rules unless the brand says otherwise: verbs first, numbers over adjectives, no exclamation marks, no hype words (revolutionary, seamless, cutting-edge, unleash, supercharge, game-changing, magic), no "excited to share". Per-language cards: [multilingual.md](multilingual.md).

## UI inventory (for product-in-use scenes)

For the 2-3 beats of the flow: the screen, its route or component file, the exact labels and ids, the states it passes through (empty, loading, success, error), colours from source constants, icon names, and three realistic sample rows. [product-ui.md](product-ui.md) rebuilds from this.

## Motion vocabulary

List the product's own gestures (a pulse, a slide-in panel, a progress style, a hover effect) as named entries: two-word name, what it means, its curve and duration. Quoting a real interaction makes the video recognisable to users; a finite named list keeps a long piece consistent.

## Gate

`brand-kit.md` has every token with its source, the fonts with licence notes and files present, the logo files copied, the voice card and the UI inventory. Any fallback is labelled.
