# Troubleshooting

> **Use when:** a render is black, short, frozen or slow; fonts fall back; text overflows; audio clips, drifts or ends early; captions misbehave; transitions or morphs look wrong; captures fail; an assembly is off by a frame.
> **Inputs:** the symptom, the composition, the render log, a grabbed frame.
> **Outputs:** the cause and the fix, applied in the owning module.
> **Next:** the module named in the fix; then [render-qa.md](render-qa.md).

General rule: every frame is a pure function of time. Most failures are a frame that depends on something else (the wall clock, a network load, a callback, a measurement taken at the wrong moment).

## Renders

| Symptom | Cause | Fix |
|---|---|---|
| Black video, tiny file, no error | a library loaded from a CDN failed, so the timeline never registered | vendor every library locally; keep a vendor checklist; probe page errors in a headless browser |
| Video cut early, or audio "fails" at the end | root `data-duration`, `meta.json` and the timeline length disagree | make the three equal |
| Frozen at frame 0 | timeline key does not match the composition id, or the timeline was built asynchronously | register `window.__timelines["<id>"]` synchronously at the end of the script |
| Sub-composition shows static frames | host id, inner root id and timeline key differ | use one id for all three |
| Element snaps to its end state at frame 0 | a later `fromTo` on the same property rendered its start at build time | `immediateRender: false` |
| Label shows its final text from frame 1 | text changed inside a timeline callback (callbacks fire during discovery and seeks) | pre-build each state as a stacked element and toggle opacity |
| Different frames on each render | `Math.random`, `Date.now`, `repeat: -1`, timers outside the timeline | seeded values, time-derived state, finite repeats |
| Elements jump off screen mid-tween | CSS `translate(-50%, -50%)` fighting GSAP x and y | set `xPercent` and `yPercent: -50` at t = 0, or centre with flex |
| Reveal stutters | animating `left`, `top`, width or height | transforms and opacity only |
| Phone screen inside a 3D model is black in some renders | a live video texture captured before its seek decoded, in some workers only | a pre-extracted image sequence drawn into a canvas texture |
| SVG image renders empty | the compiled page drops it | rasterise to PNG |
| Renders time out under load | CDN fetches, slow page navigation | vendor libraries; 120 s navigation timeout; 2 workers per render |
| "Target crashed" | GPU memory: a filtered, scaled full-frame video at high device scale | bake the motion and grade into the clip with ffmpeg and composite a transparent text layer; lower the device scale; retry |
| Log looks fine but the old cut shipped | a truncated log hid the failure, or "latest file" picked a stale render | search the log for the completion line; confirm the new file exists before copying |

## Fonts and type

| Symptom | Cause | Fix |
|---|---|---|
| Serif fallback inside transitions | the capture does not inherit fonts from the page | declare the family on `html, body`, the root, every scene and inner app root; `font-display: block` |
| Weights 300 or 900 missing | a single variable font file | one static file per weight, one `@font-face` each |
| Fonts or images vanish only during shader cuts | file-loaded fonts and images are not captured | embed as data URIs, set before the timeline is built |
| Overflow after a font change | new metrics (narrower and taller) | re-check every headline, resize, line-height about 1.12 |
| Check flags overlap on stacked titles that look fine | tall line boxes at tight line-height | inspect the frame; mark intentional stacks allow-overlap, or raise line-height |
| Descenders clipped on gradient text | the clip box is too tight | padding-bottom 40-60 px, line-height at least 1.10 |
| Burned captions in the wrong font | libass cannot read woff2 | TTF or OTF in a fonts folder passed to the subtitles filter |

## Transitions and morphs

| Symptom | Cause | Fix |
|---|---|---|
| Black frames during a shader transition | an element was static while being swapped | keep a settle tween running until the next event |
| Dark fringes on gradient edges | `transparent` in a gradient | the same hue at zero alpha |
| Light ground turns grey, warm ground olive | a tone-mapping shader (light-leak) | another shader, or only under a musical swell |
| Iris opens from the wrong place | the shader iris always opens from the centre | centre the subject, or use a scaled disc |
| Circle clip tween does nothing | string interpolation of `circle()` | a CSS variable inside the clip, or a scaled element |
| Polygon morph breaks | different vertex counts | pad with repeated points |
| White flash reads grey | `brightness()` filter | an opacity pop of a white layer |
| Soft blob mid-morph | morph too long, overlapping shapes | under 0.3-0.5 s; hide trailing shapes |
| Muddy double exposure | crossfading two busy layouts | stagger, or dip through the ground |
| Flicker between scenes | CSS and a shader engine both switching scenes | one system switches scenes |

## Audio

| Symptom | Cause | Fix |
|---|---|---|
| Silent render | an audio element without an `id` | give every audio element an id |
| Mux truncated, video cut | a multi-input filter graph plus `-shortest` | duck to a WAV in a two-input pass; force length with `-t` |
| Audio a few frames short | loudness normalisation trimmed the tail | `apad` and `-t` equal to frames / fps |
| Everything quieter than expected | `amix` normalises by default | `normalize=0` |
| Energy drops at a cut | the music entered on its calm intro | enter near a loudness peak |
| Wrong tempo | half or double tempo detected | narrow the BPM range |
| Clicks or smears at a splice | no crossfade, or a long one | 0.03 s triangular, on bar lines |
| Outro misses the music | assumed grid; the slice has silences and an off-grid re-entry | measure the slice's onsets and build on them |
| Standalone clips differ in level | different bed volumes per clip | one fixed level in the contract |
| SFX missing in the assembled film | joins drop clip audio | mix a cue list back onto the master |
| Voice takes overlap or cut off | slot budgets not checked | measure each take; shorten the sentence |

## Captions

| Symptom | Cause | Fix |
|---|---|---|
| A stray comma on every cue | the ASS Events format line lacks `Name` | add the field |
| Subtitles filter fails on Windows paths | `:` and `\` parsed as options | run from the project folder with a relative path |
| Captions cover UI | no reserved band | keep essentials above the band; end the cue early on push-ins |
| Same text twice | a tagline burned as a caption | filter verbatim on-screen lines from the burn; keep them in the SRT |
| First word early after a pause | recogniser timing | re-time from an energy scan |
| Wrong language in captions | default English model translated | name the model and the language |

## Captures and assembly

| Symptom | Cause | Fix |
|---|---|---|
| Full-page screenshot black below the fold | lazy painting and content visibility | force visible, scroll each section into view, screenshot the viewport |
| Tutorial overlays in every capture | onboarding re-arms per page | clear its storage gate at load |
| Removed overlay comes back | the app re-mounts it | inject a hiding stylesheet |
| Recorded app runs slowly | a CPU screen recorder | a GPU recorder; one capture at a time; never render during a capture |
| A poster flashes at every join | baked poster frames | strip frame 0 and clone the next before assembly |
| Notes land one frame off | counters computed from time | frame arithmetic (`n - startFrame`) |
| Concat fails or drifts | mismatched codec, size, fps or pixel format | re-encode to one spec |
| Several builders hung silently for hours | long foreground tool calls | background jobs with a polled log and an explicit exit line |
