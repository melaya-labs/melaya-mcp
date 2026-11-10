# Platform specs

> **Use when:** deciding sizes, durations, safe zones, caption and copy limits for YouTube, Shorts, TikTok, Reels, Instagram, LinkedIn, X or Product Hunt, or making a version of a piece for another platform.
> **Inputs:** the target platforms from the brief.
> **Outputs:** a spec line per deliverable (canvas, fps, duration, safe box, caption zone, copy limits, cover or thumbnail size) recorded in `brief.md`.
> **Next:** [storyboard.md](storyboard.md) (each format is re-laid-out, never cropped), [render-qa.md](render-qa.md), [publishing.md](publishing.md).

Platform limits change often. Treat the numbers below as the planning baseline and confirm a hard limit (maximum length, file size, caption length) in the platform's current help pages before publishing.

## Canvases

| Format | Canvas | Use |
|---|---|---|
| Landscape 16:9 | 1920x1080 (4K 3840x2160 for YouTube masters) | YouTube, X, LinkedIn, website hero, launch film |
| Vertical 9:16 | 1080x1920 | Shorts, TikTok, Reels, Stories |
| Portrait 4:5 | 1080x1350 | Instagram and LinkedIn feeds, carousels |
| Square 1:1 | 1080x1080 | LinkedIn and X feeds, carousels |

30 fps unless the source footage is 24, 25 or 60. H.264 (High), `yuv420p`, AAC 48 kHz, `+faststart`.

## Per platform

| Platform | Canvas | Length to aim for | Captions | Copy and cover |
|---|---|---|---|---|
| YouTube | 16:9 | 45 s-3 min for launches and explainers; any length | upload SRT or VTT per language; burned only for social cuts | title up to 100 characters (benefit first), description with chapters, tags about 470 of 500 characters; thumbnail 1280x720 under 2 MB |
| YouTube Shorts | 9:16 | 15-35 s (allowed up to about 3 min) | burned, lower third | title with the hook; the cover frame is chosen in the app |
| TikTok | 9:16 | 15-35 s; hook in the first second | burned; native captions can be added in the app | first line of the caption carries the hook; 3-5 specific hashtags |
| Instagram Reels | 9:16 | 15-30 s (allowed up to about 3 min) | burned | cover 1080x1920 with the key content in the central 3:4 area (the profile grid crops it); a few relevant hashtags |
| Instagram feed and carousel | 4:5 (or 1:1) | carousel up to 20 slides; 6-10 is typical | text on the slides | first slide is the hook; caption up to about 2,200 characters |
| LinkedIn | 16:9, 1:1, 4:5 or 9:16 | 30-90 s | upload SRT; burned for muted autoplay | about 210 characters show before "see more"; document carousels (PDF) at 1080x1350 or 1080x1080, 8-12 pages |
| X | 16:9 or 1:1 (9:16 accepted) | 15-60 s (standard accounts up to about 2 min 20 s) | burned, or SRT upload | 280 characters on standard accounts; the first frame is the thumbnail |
| Product Hunt | gallery images about 1270x760; a square thumbnail 240x240 (GIF allowed) | a 30-90 s video linked from YouTube | YouTube's captions | name about 40 characters, tagline about 60, short description about 260; the maker's first comment tells the story |

Publish the same master in the order your audience is largest; native uploads beat links. A vertical piece can go to TikTok, Reels and Shorts as one file when it respects the strictest safe zone.

## Safe zones

Everywhere: action-safe 90% (5% inset) and title-safe 80% (10% inset). Platform overlays add more:

| Canvas | Keep essentials inside | Caption zone |
|---|---|---|
| 1920x1080 | title-safe 1536x864 at (192, 108) | bottom 130-160 px reserved when captions are burned (y above 920-950) |
| 1080x1920 (all short-video apps) | x 60-940, y 220-1480; nothing essential right of x 960 in the lower half (the like, comment and share rail) | lower third about y 1430-1580; never in the bottom 440 px (caption, username, music line) |
| 1080x1350 | 960x1200 centred | bottom 120 px |
| 1080x1080 | title-safe 864x864 at (108, 108); keep lockups centred (some feeds crop slightly) | bottom 110 px |

Reserve the caption zone in the storyboard, before any layout is drawn. Check with a band drawn on a grabbed frame ([render-qa.md](render-qa.md)).

## Re-laying out for another format (never crop)

Rebuild with the same angle, real UI, morph, music slice and beat locks; change the layout:

- Side-by-side becomes top and bottom; camera moves become vertical; UI is scaled up (a phone screen can fill a vertical frame, a desktop UI is cropped to one region at 60% or more of the width).
- Hook in the first 1-2 s, top-centre of the safe box. Hero type 110-150 px, at most about 10 characters per line; plan line breaks.
- Transitions travel the long axis (whips and splits at y plus or minus 2100-2300 in vertical; blinds as 8 strips of 240 px).
- Iris and clock wipes work in any aspect.
- Same frame count, music slice and beat file when the versions must stay in sync.

## Duration and chapters

- Social clips 15-20 s with the hook under 2 s; ads 15 s with the end card held at least 1.5 s; process timelapses 60-75 s with the hook under 1 s.
- YouTube chapters: the first at 0:00, at least three, each at least 10 s; compute timestamps from the rendered segments (ffprobe), not from the plan.

## Gate

Every deliverable has its canvas, length, safe box, caption zone and copy limits written in the brief; each version is its own layout.
