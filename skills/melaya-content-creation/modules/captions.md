# Captions and subtitles

> **Use when:** a piece has a voice or must work muted: timing captions from a voiceover or script, choosing a style, burning them in, shipping SRT and VTT sidecars, or captioning other scripts and languages.
> **Inputs:** voiceover takes and their script (`caption` field), or a transcript; `design.md`; the platform's caption zone ([platforms.md](platforms.md)).
> **Outputs:** `captions.srt`, `captions.vtt`, `captions.ass` (burn-in), or a caption track inside the composition; a burned render when needed.
> **Next:** [render-qa.md](render-qa.md).

Most social views are muted. Captions are part of the design, planned from the brief: the caption band is reserved before any layout is drawn.

## Timings

| Source | Method |
|---|---|
| A script you voiced with TTS | no speech recognition needed: measure the speech segments with ffmpeg `silencedetect` (noise -35 dB, minimum pause 0.18 s), split the script after each period and comma, map chunks to segments one to one, or by each chunk's character midpoint when counts differ |
| Recorded or unknown speech | word timestamps from a Whisper-class model with the language forced (the HyperFrames `transcribe` command, or faster-whisper `medium` int8 on CPU); align the words to the known script text so spelling is exact |
| A finished transcript (SRT, VTT, JSON) | import it, then re-cut it with the rules below |

Always name the model and the language: a default English-only model silently translates other languages. Check source-language word times first: recognisers place the first word after a long pause up to a second early (find words whose first 0.35 s is mostly silence). [../scripts/captions.py](../scripts/captions.py) builds SRT, VTT and ASS from word timings or from a script plus silence detection, applying the rules below.

## Cue rules

| Rule | Phrase captions | Word-highlight (karaoke) captions |
|---|---|---|
| Characters per line | 42-44 (vertical 32-38) | about 30 (CJK 14) |
| Lines | at most 2, balanced (minimise the longer line); merged cue under 80 characters | one balanced chunk, split at punctuation |
| Words per group | | 2-3 high energy, 3-5 conversational, 4-6 calm |
| Start | on speech | 0.1 s before the first word |
| Hold after speech | +0.25 s, at most +0.5 s | +0.35 s |
| Minimum duration | 0.8 s; merge a cue under 0.9 s into the next when the gap is under 0.6 s | 0.9 s |
| Gap between cues | at least 20 ms (two frames is safer for burn-in) | one group visible at a time |
| Fades | 90 ms in and out | pop on the current word at most 1.04-1.07 scale with a word gap of at least 0.3em |
| End of piece | gone 0.4 s before the last frame | same |

- **No double text.** A line already on screen verbatim (a tagline, an end card) is not burned again; it stays in the SRT and VTT sidecars so platform captions remain complete. Localised versions burn everything: the viewer needs the translation.
- **Captions never duplicate the UI** and never cover faces or the product.
- When a camera move pushes on-screen text into the caption band, end the cue on its last word instead of holding it.

## Position and style

- Landscape: bottom centre, inside title-safe, a band of the bottom 130-160 px kept free of essential content (y above 920-950 at 1080p). Vertical: a lower third around y 1430-1580, above the platform's caption and username area and left of the right action rail; non-product beats can carry centred, very large captions (about 98 px, punch word 118 px).
- One typeface voice and one accent colour; the punch is colour and size only. No rainbow words, boxes, stickers or confetti.
- A plate that reads on light and dark grounds: opaque box at about 38% dark alpha with 14 px padding, or a white fill with a 3-4 px dark outline and a soft shadow.

```text
ASS style for 1920x1080 burn-in (PlayResX 1920, PlayResY 1080, WrapStyle 2, ScaledBorderAndShadow yes):
Style: Cap,{Display Font},44,&H00FFFFFF,&H00FFFFFF,&H00000000,&H9E000000,-1,0,0,0,100,100,0,0,3,14,0,2,200,200,52,1
Each dialogue line starts with {\fad(90,90)}.
The Events Format line must include the Name field, or a stray comma shows on every cue.
```

Burn-in tools (libass) need TTF or OTF files in a fonts folder; without them they silently fall back to a system font. Compare a burned frame with a sample of the intended face.

## Burn-in or sidecar: ship both

- **Sidecars** (SRT and VTT) for platforms, players and accessibility.
- **A burned version** for social feeds and direct sharing.
- **Render the picture captionless once,** then burn: a caption fix becomes a minutes-long finish step instead of a full re-render.

```bash
ffmpeg -nostdin -y -i film_nocap.mp4 -i mix.wav -map 0:v -map 1:a \
  -vf "subtitles=captions.ass:fontsdir=fonts/ttf" -c:v libx264 -crf 16 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 256k -t 45.0 -movflags +faststart film_captioned.mp4
```

- **Styled HTML captions without re-rendering the film:** build a composition containing only the caption band (for example 1920x160 on a transparent ground), render it as MOV with alpha (ProRes 4444), and overlay it at the band's position. The cost is per captured frame, so a thin band renders several times faster than the full frame.
- **Inside a HyperFrames composition:** all captions in one caption sub-composition on one track, one group visible at a time, each group hard-hidden at its end time; registry caption styles (highlight, pill karaoke, editorial emphasis, kinetic slam and more) are sub-compositions with transparent grounds. Run the check with a caption zone so content and captions do not collide.

## Scripts and languages

| Script | Characters per chunk | Notes |
|---|---|---|
| Latin, Cyrillic | about 30 (karaoke) or 42-44 (phrase) | a face with full coverage of the alphabet |
| Devanagari | about 30 | a Devanagari-capable TTF |
| Chinese, Japanese, Korean | 13-16 | per-character tokens, no word gap, punctuation attached to the previous character; full-width punctuation |
| Arabic, Hebrew | about 30 | right-to-left element, a font with proper shaping; numbers and Latin brand names stay left-to-right runs; the highlight runs right to left |

Per-language production (translation, voice, fit loop): [multilingual.md](multilingual.md).

## Gate

Every cue respects the rules; nothing essential sits under the caption band (grab a frame under the longest two-line cue); burned text is the intended font; SRT and VTT exist; captions end 0.4 s before the last frame.
