# Asset sourcing and generation

> **Use when:** a piece needs images, icons, logos, fonts, footage, screen captures, music, sound effects or a voice, and you must find, generate, capture or prepare them with clear rights.
> **Inputs:** `storyboard.md` and its shot list, `brand-kit.md`.
> **Outputs:** files in `assets/` (frozen, local, relative paths) and `assets/ledger.md` with the source and licence of each.
> **Next:** the build ([hyperframes.md](hyperframes.md)), [audio.md](audio.md), [stills.md](stills.md).

## Order of preference

1. **The brand's own assets** (logo, fonts, screenshots, footage, product components). Reuse beats re-creation.
2. **Recreated from source** (UI rebuilt in HTML, diagrams from the real architecture) ([product-ui.md](product-ui.md)).
3. **A media tool already installed:** with the HyperFrames `media-use` skill, one verb (`resolve --type bgm|sfx|image|icon|logo|voice|grade|lut --intent "..."`) finds, generates or reuses an asset, freezes it into the project and records it in a ledger. Check what it reports about licence before publishing.
4. **Libraries with clear licences** (below).
5. **Generation** with a model the user has (image, music, voice, video). Paid generation waits for the user's yes.

Never: scraped images of unclear origin, a competitor's assets, real people's likeness without consent, redrawn or recoloured third-party logos, music ripped from a video.

## Sources by type

| Type | Good sources | Rules |
|---|---|---|
| Logos | the brand's own files; for integrations, the partner's official press or brand page, the app's own SVG | official marks only, unaltered, with their clear space; a logo is never generated |
| Icons | open icon sets with permissive licences (for example Lucide ISC, Tabler MIT, Phosphor MIT, Material Symbols Apache-2.0); the product's own icon set | inline SVG paths, one stroke weight per piece; keep each set's licence notice |
| Fonts | the brand's files; open families under the SIL Open Font License | one static file per weight, plus TTF or OTF for subtitle burn-in |
| Photos and b-roll | the brand's own; stock with a licence that covers commercial video (check each site's current terms) | grade every clip to one look; avoid recognisable people unless released |
| Music | owned or house tracks; generated tracks; production-music licences | the licence must cover the platforms and paid use if it is an ad |
| Sound effects | CC0 collections (for example the Kenney audio packs); your own recordings | prefer soft, warm sounds for repeated use |
| Voice | local TTS (HyperFrames `tts`), the user's hosted voice provider, a recorded human | a cloned voice only with the owner's consent |
| Generated images | any image model the user has | write the prompt with the brand's palette and look; no text inside generated images (typeset it in the composition) |

## Screen captures and footage

- **Prefer recreation for final quality.** Live recordings drift and drop frames on the wall clock; when footage is needed, capture it deterministically or as raw recordings per surface.
- **Scripted browser tours** (Playwright or Puppeteer): a 1920x1080 viewport, device scale 1, smooth cursor glides (about 22 steps, 80 ms settle), typing at about 60 ms per key, scrolling in 8 or more wheel ticks over 1.2 s, selectors from stable attributes with ordered fallbacks, scene markers written to `timeline.json`.
- **Capture hygiene:** clear onboarding gates in local storage at load instead of clicking through tutorials; hide overlays with an injected stylesheet (removing DOM loses to re-mounts); never approve, send or delete during a capture; credentials from the environment, a one-time code handed over by the human, never hard-coded.
- **Full-page stills** render blank below the fold on lazy pages: force content visible, scroll each section into view, wait, screenshot the viewport, stack the shots, and scroll the tall image inside a device frame with the timeline.
- **Validate every take:** decode it (`ffmpeg -i take.webm -f null -`) and check the frame count and duration; look at one frame per take.
- **Long live processes** (an agent drawing, building, filling a form): record with a GPU encoder (a CPU recorder can slow the app threefold), keyframes every second, a graceful stop and a 3 s tail; one live capture at a time; never render while capturing ([films.md](films.md) has the vertical speed-ramp recipe).
- **Screens inside 3D devices:** a pre-extracted image sequence drawn into a canvas texture per frame, not a live video texture (parallel render workers can capture before a seek decodes, giving black screens).

## Preparing files

| Need | Do |
|---|---|
| SVG that renders empty as an image | rasterise to PNG at twice the display size |
| Logo on a dark ground without a light variant | ask for one; never invert colours automatically |
| Transparent cut-out of a person or product | HyperFrames `remove-background` or any matting model; check edges on both grounds |
| Footage that seeks slowly | re-encode with dense keyframes (`-g 15`), constant frame rate, `yuv420p` |
| Fonts for burn-in | TTF or OTF copies in `fonts/ttf/` |
| Many small images in a shader scene | embed as data URIs, set before the timeline is built |

## The ledger

One row per file in `assets/ledger.md`, written when the file is added:

```text
| file | type | source (URL, tool or "own") | licence | attribution needed | notes |
| assets/music/bed.wav | music | generated, prompt in work/music.txt | owned output | no | 124 BPM, measured |
| assets/sfx/soft-impact.wav | sfx | CC0 pack | CC0 | no | |
| assets/icons/check.svg | icon | open icon set | ISC | keep notice | |
```

Anything without a clear licence is replaced before publishing. Attribution lines the licences require go into the publishing package ([publishing.md](publishing.md)).

## Gate

Every file in `assets/` is local, referenced relatively, and has a ledger row with its licence; nothing paid was generated without a yes.
