# Stills: carousels, thumbnails, posters, product shots

> **Use when:** the deliverable is an image or a set of images: a social carousel, a video thumbnail or cover, a launch poster or social card, a link-preview image, a Product Hunt gallery, or product shots in device frames.
> **Inputs:** `brief.md`, `brand-kit.md`, `design.md`; the video (if the still belongs to one).
> **Outputs:** PNG or JPG files at the platform sizes (and a PDF for document carousels), each checked at its smallest display size.
> **Next:** [render-qa.md](render-qa.md) for the checks, [publishing.md](publishing.md).

Stills follow the same system as the video: the same tokens, type, real UI and copy rules. Build them as HTML pages (one per still) and capture them; text stays real text, crisp at any size.

## Rendering

- Build each still as a fixed-size HTML page using the composition's CSS and assets, then capture it at device scale 2 and downscale for delivery, or capture a frame of the composition (HyperFrames `snapshot --at <t>`).
- Wait for fonts and images before capturing (fonts loaded, every image decoded).
- Document carousels: print the pages to one PDF at the slide size, one slide per page, fonts embedded.
- Deliver PNG for UI and text, JPG (quality 85-92) for photographic covers; keep each under the platform's size limit.

| Still | Size |
|---|---|
| YouTube thumbnail | 1280x720, under 2 MB |
| Vertical cover (Reels, TikTok, Shorts) | 1080x1920, key content in the central 1080x1440 |
| Instagram or LinkedIn carousel slide | 1080x1350 (or 1080x1080) |
| Link preview (Open Graph) | 1200x630 |
| Product Hunt gallery | about 1270x760; thumbnail 240x240 |
| X or LinkedIn single image | 1200x675 (16:9) or 1080x1350 |

## Carousels

- **Slide 1 is the hook,** written like a video hook ([narrative.md](narrative.md)): a number, a reversal or the result. It must work as a single image in the feed.
- **One idea per slide,** at most about 25 words, the heading at 64-96 px on 1080 wide, body at 36-44 px.
- **Shape:** hook, problem, 3-6 steps or proofs (each with real UI or a concrete example), a summary slide, a CTA slide. 6-10 slides is the sweet spot.
- **Continuity:** a consistent grid and margin (at least 72 px), a progress mark (dots or "3/8"), and one element that bleeds across a slide edge to invite the swipe.
- **Proof over claims:** real screens and real outputs; no invented numbers.

## Thumbnails and covers

- **Readable at 168 px wide** (the smallest list view): three to five words at most, high contrast, one focal object or face, no thin type.
- **Compose from the piece itself:** the big title, the hero UI card bleeding off an edge, the logo; a frame of the film rebuilt at thumbnail size reads better than a raw frame.
- **Honest:** the thumbnail shows something that is in the video.
- **Poster frame for the video:** pick the strongest settled frame (text fully in, not mid-transition) and bake it as frame 0 so every platform's idle thumbnail shows it ([render-qa.md](render-qa.md)).
- Test at 100% and at 168 px wide, on light and dark interface backgrounds.

## Product shots

- **Device frames from layered HTML,** not stock mockups of unknown licence: a body with the right radius, the screen inset, a thin bezel, a contact shadow, an optional glass glare. The screen is the recreated UI or a real capture at native resolution.
- **Angles:** straight-on for UI clarity; a 10-20 degree turn for hero shots; never a perspective that makes UI text unreadable.
- **Grounds:** the brand ground, a soft radial light behind the device, one accent at most. A floor shadow (blurred ellipse at 25-40% alpha) grounds the device.
- **Sets:** the same camera angle, light and ground across every shot of a set, so they read as one launch.
- **Scale:** the device takes at least 60-70% of the frame width in a hero shot.

## Posters and social cards

- One headline (the angle in five to eight words), one visual (real UI or the product), the logo, the URL. Title-safe margins.
- Link previews crop to about 1.91:1 in most apps: keep the headline and logo in the central 1080x560.

## Gate

Every still is at its platform size, readable at its smallest display size, uses only real UI and approved facts, and has its assets in the ledger.
