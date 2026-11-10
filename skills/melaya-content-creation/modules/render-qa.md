# Render, QA and delivery

> **Use when:** checking a composition before render, rendering drafts and finals, sampling frames, verifying duration, frame count and loudness, baking the poster, or encoding delivery files.
> **Inputs:** `composition/` (or a Remotion project), `storyboard.md` (reveal and transition times), the mix.
> **Outputs:** the render, `poster.jpg` baked as frame 0, `qa/` (stills, contact sheet, report), delivery encodes. Checklist: [../templates/render-checklist.md](../templates/render-checklist.md).
> **Next:** [publishing.md](publishing.md); [review.md](review.md) when a human reviews.

## 1. Before rendering

- Lint while authoring; then the single gate: HyperFrames `check` with **zero errors** (lint, runtime, layout overflow and overlap, motion, WCAG AA contrast). Read every warning. Info items mid-transition (occluded text during a cut, overflow during a push-in) are expected.
- A lint error disables the layout and contrast audits: "0 samples" is not a pass.
- Mark intentional cases instead of restructuring (`data-layout-allow-overflow`, `data-layout-allow-overlap`, `data-layout-ignore`). Fix every contrast failure with a colour from the palette family; the only bypass skips all contrast checks, so do not use it.
- Structure warnings that only affect the editor's timeline view do not affect the render; do not restructure a working composition to silence them.

## 2. Draft, then look

Render a draft and grab stills at **every reveal (settled)** and **every mid-transition** (whip midpoint, morph mid-flight, shader peak), plus the first and last frames; build a contact sheet. [../scripts/qa_frames.sh](../scripts/qa_frames.sh) does both and writes the report.

```bash
npx hyperframes render --quality draft --output ../draft.mp4
for t in 0.05 1.2 1.9 3.6 5.8 7.7 9.7 11.6 13.5 15.4; do
  ffmpeg -nostdin -v error -y -ss $t -i ../draft.mp4 -frames:v 1 ../qa/qa_$t.png; done
ffmpeg -nostdin -v error -y -i ../draft.mp4 -vf "fps=2,scale=480:-1,tile=6x6" -frames:v 1 ../qa/contact.jpg
```

Look at every image. Check for:

| Problem | Look for |
|---|---|
| Overflow, collisions | text leaving its box, overlapping reads, descenders clipped |
| Unreadable text | holds shorter than the floor, low contrast, text under the caption band or platform overlays |
| Empty or black frames | mid-transition holes, a blank frame 0, a whip midpoint on an empty frame |
| Muddy double exposure | two busy layouts crossfading |
| Wrong font | serif or system fallback glyphs, especially inside transitions |
| Soft morphs | a blob mid-morph, a doubled logo at the hand-off |
| Colour shifts | a light ground going grey during a shader |
| Generic look | pill rows, stat cards, repeated entrances ([design-system.md](design-system.md)) |

Fix, re-check, re-grab only the frames that changed. Never render the final on speculation: a render costs minutes.

## 3. After rendering

- **Duration and frames:** `ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 out.mp4` equals the plan; video and audio durations equal the target.
- **Audio:** loudness about -14 LUFS integrated and -1.5 dBTP for social (`ffmpeg -i out.mp4 -af ebur128=peak=true -f null -`), no clipping, no dead air over 0.8 s, every voice take complete, every section boundary listened to.
- **Sync:** each spoken name lands while its title is settled; every word-locked reveal within a frame.
- **Caption band:** draw it on the frame under the longest cue (`drawbox=y=950:w=iw:h=130:color=red@0.25:t=fill`) and confirm nothing essential sits under it.
- **Never trust a truncated log:** search the render output for the completion line or a failure; confirm a new file exists before copying "the latest" render. A suspiciously small file is a black render (a library failed to load).

## 4. Poster frame, baked as frame 0

Pick the strongest **settled** frame (the hook line, the hero reveal or the lockup, fully animated in), save it as `poster.jpg`, and replace only frame 0's pixels with it: every thumbnail grabber shows it, and the duration, frame count and audio stay identical. [../scripts/poster.sh](../scripts/poster.sh) does both.

```bash
ffmpeg -nostdin -y -ss 3.2 -i video.mp4 -frames:v 1 -q:v 2 poster.jpg
ffmpeg -nostdin -y -i video.mp4 -i poster.jpg \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='eq(n,0)'[v]" -map "[v]" -map 0:a? \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart video.poster.mp4 \
  && mv video.poster.mp4 video.mp4
```

Clips that will be joined into a film are delivered without a baked poster (or have it stripped before assembly: [films.md](films.md)).

## 5. Delivery encodes

| File | Settings |
|---|---|
| Master | H.264 CRF 14-16, preset slow, `yuv420p`, keyframe interval 60 (`keyint=60:min-keyint=30`), AAC 256k 48 kHz, `+faststart` |
| Social upload | CRF 17-19, preset medium or slow; light UI-heavy pieces need the lower CRF (about 4-7 Mbps at 1080p) to keep small text crisp |
| YouTube 4K upload | upscale with `scale=3840:2160:flags=lanczos,unsharp=5:5:0.7:5:5:0`, CRF 15, AAC 320k (a 4K upload gets a higher bitrate tier, so the 1080p stream is crisper) |
| Chat or email | two-pass about 1500 kbps, AAC 96k (about 15 MB per minute) |
| Review preview | CRF 23, preset veryfast |
| Transparent overlay | MOV ProRes 4444 (alpha) |

Force exact lengths with `-t`, never `-shortest`. Run ffmpeg with `-nostdin` in scripts (a waiting stdin can hang a job for minutes).

## 6. Render settings that hold up

- Draft for looking, high or delivery quality for finals; same frame rate as the plan.
- Under parallel load: 2 workers per render (3 for a single film), a 120 s page navigation timeout, a 60 s check timeout, every library vendored. Run long renders in the background with a log that ends in an explicit exit line, and poll it.
- Some features slow renders (shader transitions disable fast capture: budget about a minute per 15 s at 2 workers). Never use an experimental alternate capture path for finals.

## Gate

Check passed with zero errors; every reveal and mid-transition still looked at; frame count, duration and loudness match; poster baked; delivery files named per [publishing.md](publishing.md).
