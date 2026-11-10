# Visual design system

> **Use when:** setting typography, colour roles, grounds, layout, safe areas and the motion language of a piece, or checking why a design reads as generic or AI-made.
> **Inputs:** `brand-kit.md`, the look preset from [../styles/](../styles/), the format from [platforms.md](platforms.md).
> **Outputs:** `design.md`: type scale, colour roles per ground, surfaces, easing vocabulary, layout grid and safe areas, banned patterns for this piece.
> **Next:** [motion.md](motion.md), [product-ui.md](product-ui.md) or [stills.md](stills.md); then the build.

A shared system is what makes several scenes, clips or authors read as one piece. It is small on purpose: two typefaces, five colour tokens, a handful of eases.

## Typography

| Role | Weight | 16:9 (1920x1080) | 9:16 (1080x1920) | 1:1 (1080x1080) | Settings |
|---|---|---|---|---|---|
| Hero read | 800-900 | 104-200 px (one word 172-200) | 110-150 px, about 8-10 characters per line | 96-130 px | tracking -0.01 to -0.045em; line-height 0.90-0.95 for one line, 1.10-1.12 stacked |
| Secondary line | 300-400 | 46-124 px | 72-96 px | 72-96 px | the light weight under a heavy line carries hierarchy |
| UI labels and HUD (mono) | 400-600 | 11-22 px inside recreated UI | 18-28 px (UI scaled up) | 16-24 px | caps tracked 0.18-0.34em |
| URL in a lockup (mono) | 500 | 36-48 px | 40-56 px | 36-48 px | typed at about 45 ms per character |
| Burned captions | 700 | 44-54 px | 54-62 px lower third, up to 98 px centred | 48 px | see [captions.md](captions.md) |

- **Hierarchy comes from weight contrast, not more fonts:** 300 over 800-900 at the same size, one accent word.
- **Minimum effective size:** 30 px after all scaling in vertical (text inside a 65% device mockup is authored at 46 px or more); body at least 20 px full-screen, 32 px in a feed; check legibility on a 270 px wide thumbnail.
- **Embedding:** one static font file per weight, one `@font-face` each, `font-display: block`, and the family declared on `html, body`, the root and every scene root (some capture paths do not inherit fonts). Tabular numbers for any figure of 18 px or more.
- **Overused defaults** (Inter, Roboto, Open Sans, Lato, Poppins, Montserrat-as-default, Playfair, Syne and similar) read as generated when the brand has no font. Prefer a characterful family of the right class. The brand's own font always wins.
- After any font change, re-check every headline for overflow, line breaks and collisions; a narrower, taller face needs new sizes and line-height about 1.12.

## Colour

- **Five tokens per piece:** ground, text, signature accent, secondary accent, warning; neutrals free. At most two accents visible in a scene; strictest premium looks use one accent only. Sample five frames: more than seven distinct colours (gradients excluded) fails.
- **Accent means something.** One colour only ever means "needs you" or the payoff; never decoration, never a rainbow of punch words.
- **Grounds alternate** between scenes or clips (dark, colour full-bleed, dark, light...) so a long piece breathes.
- **Gradients fade to the same hue at zero alpha** (`rgba(r,g,b,0)`), never `transparent`, which leaves dark fringes in captures. No gradient text at hero size; no aurora fills.
- Chrome (surfaces, borders) stays at or below 45% luminance on dark designs so frames do not read as screenshots.

Surface recipes (colour-neutral):

```css
/* raised card, dark ground */
box-shadow: 0 24px 52px -18px rgba(0,0,0,.92), 8px 8px 22px rgba(0,0,0,.52),
  -5px -5px 16px rgba(255,255,255,.05), inset 0 1px 0 rgba(255,255,255,.10), 0 0 0 1px rgba(255,255,255,.045);
/* raised card, light ground */
box-shadow: 0 22px 44px -16px rgba(15,23,42,.34), 7px 7px 17px rgba(15,23,42,.13), -6px -6px 16px rgba(255,255,255,.98);
/* readable scrim behind a read over busy UI */
background: radial-gradient(ellipse at 30% 60%, rgba(10,14,22,.9) 0%, rgba(10,14,22,.55) 40%, rgba(10,14,22,0) 70%);
```

Text over footage: a 4-8 px outline of the ground colour painted behind the fill (`paint-order: stroke fill`) or one soft shadow. One tight and one wide shadow at most; stacked heavy shadows look fat and blurry.

## Layout

- **Safe areas** on every format: action-safe 90% (5% inset) for anything visible, title-safe 80% (10% inset) for reads and key content. Platform overlays add more ([platforms.md](platforms.md)). Guides live in the preview, never in the composition.
- **Use the canvas:** one panel at least 1500 px wide at 1080p; two panels at least 720 px each; a recreated device at least 85% of the frame width in vertical, or crop to one region at 60% or more.
- **At most two text blocks per frame,** one dominant element at twice the size of anything else.
- **Density from the product:** if the real page shows 20 items, show 4-12, never 1-3.
- When a caption band is reserved (bottom 130 px at 1080p), centre content on the remaining area, not on the canvas middle.

## Easing vocabulary

| Ease | Use | Typical duration |
|---|---|---|
| `expo.out` | slams, landings, arrivals | 0.42-0.9 s |
| `power4.out` | mask rises, skew slides | 0.4-0.55 s |
| `power3.inOut` | morphs, camera moves, the default single move | 0.45-1.6 s |
| `power2.inOut` | neutral transitions | 0.4-0.8 s |
| `power3.in`, `expo.in` | accelerating into a cut, zoom-through, whip | 0.2-0.42 s |
| `sine.inOut` | holds, drifts, breathing | 1.2-3.6 s |
| `back.out(1.3-2.4)` | pops, buttons landing, the accent word (one per scene) | 0.3-0.5 s |
| `none` | clocks, progress, dashes, spins | any |
| `steps(1)` | caret blink | 0.25 s |

Energy sets duration: calm 0.5-0.8 s, medium 0.3-0.5 s, high 0.15-0.3 s. Use five to seven eases in a piece, a signature ease in most tweens, and vary eases inside a sequence; identical eases read as mechanical. Overshoot only on transforms, never on opacity.

## What reads as generic or AI-made (ban per piece)

| Avoid | Do instead |
|---|---|
| Rows of rounded pill chips, symmetric three-card grids, stat-card rows | the product doing the thing; asymmetric layouts; real chips only where the UI has them |
| Cards sliding in, the same letter-drop on every line | camera language, true morphs, a different entrance per read |
| Particles, blobs, waveforms, equaliser bars, confetti | light and texture made from the product's own data |
| Raw screenshots | UI recreated in HTML and CSS from source |
| One transition everywhere | one family per clip, different across clips |
| Rainbow or purple gradients, glow on everything | one accent, restraint; glow is seasoning |
| Step tags ("01 ..."), tutorial framing in a launch piece | story beats |

## Gate

`design.md` lists the type scale for the format, the colour roles with contrast checked, the surfaces, the easing set, the safe areas and the banned patterns for this piece.
