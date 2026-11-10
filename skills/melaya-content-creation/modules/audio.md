# Audio: music, beat grid, SFX, voiceover, mix

> **Use when:** choosing or preparing music, measuring its beats, planning sound effects, generating and placing a voiceover, ducking, setting loudness, or fixing audio that clips, drifts or ends early.
> **Inputs:** `storyboard.md` (audio intent per scene, anchors), `script.md` (voiceover lines), `timeline.json`.
> **Outputs:** the music slice and `beats.json`, an SFX plan, voiceover takes, `mix.wav` at the target loudness; all files and their licences in `assets/ledger.md`.
> **Next:** [captions.md](captions.md) for a narrated piece; the build ([hyperframes.md](hyperframes.md)).

Default posture: one tasteful music bed plus a few well-timed effects feels more finished than silence. Silence only when the user turns audio off or the concept needs it.

## Music

- **Energy first.** A calm corporate bed under a trailer-scale edit reads as filler; wrong-energy music is a common rejection reason. Feature teasers and clean product tones: 110-120 BPM. Launch films: 118-130 BPM driving tracks. Deadpan: a quiet bed at 0.12-0.18.
- **Licence:** owned, commissioned, generated, or a stock licence that covers this use; record it. A brand with a house track reuses it as a brand asset.
- **Enter near energy, never on a calm intro.** Measure loudness every 2 s (rising = build, plateau = body, dip = breakdown, jump = drop) and start the slice so the hardest cut lands on the drop. Check `start + length` stays inside the track.
- **Measure the beat grid, never assume it.** [../scripts/beatgrid.py](../scripts/beatgrid.py) (NumPy only) gives tempo, beat, first downbeat, bar length, a confidence (above about 2 is solid) and the strong downbeats; the HyperFrames `beats` command gives a beat grid with per-beat strength (take the strongest as cues). Half or double tempo: narrow the BPM range. Near breakdowns and the track end, look at the actual onsets.
- **Extend or reshape on bar lines only** (`D(k) = firstDownbeat + k * bar`), with a 0.03 s triangular crossfade at each splice (0 clicks, longer smears the downbeat). Splice inside the same section at the same energy, and listen to every splice.
- **Slice per segment on whole frames** (start = startFrame / fps) and write a beats file per slice with times relative to the slice; only the last segment gets a baked fade.

## Locking picture to music

| Event | Lock | Tolerance |
|---|---|---|
| Major reveal, true morph, logo | a strong downbeat; 1-3 locks in a 15-25 s piece | within 0.15 s |
| Sequential accents (rows, dots, ticks, presses) | consecutive beats | within 0.10 s |
| Sequential readable text | every other beat, or arrive fast and hold the set | readability wins |
| An arrival (morph lands, button bottoms out) | ends on the beat: start = beat - duration | |
| A slam or press | starts 30-60 ms early so the settle lands on the beat | |
| A shader burn or flash | centred: start = beat - duration / 2 | |

Mark locks in the composition (`// beat-locked 5.80`). Cue data biases timing; it never overrides readability or the story.

## Sound effects

- **Match motion only:** card sounds for card-like reveals, a short impact for a payoff, clicks for presses, key ticks for typing, a switch for a toggle, a soft drop when a row lands, a bell or soft bong for an approval or the lockup.
- **One sonic palette** for the whole piece, in the same key and space as the music, mixed under it; prefer soft, warm sounds with little high-frequency energy for anything repeated.
- **Timing:** impacts 20-30 ms ahead of the visual lock; clicks at the bottom of the press; a toggle's mechanism 60 ms after its click; typing one tick every third character (3-5 per field), rotating about 8 samples; alternate two samples on repeated presses.
- **Restraint:** nothing on the music's own drop, nothing on rapid logo swaps, at most two sounds stacked, none in the first and last 0.35 s of a clip that will be joined. One sound placed in a silence makes the re-entry hit.
- **Density by tone:** polished or deadpan 1-3 cues; playful or feature-cards 3-6; cinematic 2-3 big cues plus interaction clicks; chaotic on most beats. A 15 s product clip with heavy interaction can carry up to about 20.
- **Levels:** music bed 0.30-0.40 standalone (never above 0.5); SFX 0.45-0.85 (polished pieces at the low end, repeated clicks about 0.3). In a film built from clips, every clip carries its music slice at exactly 1.0 so standalone versions match; the assembly owns fades and levels.

## Voiceover

| Engine | Use | Notes |
|---|---|---|
| HyperFrames `tts` (Kokoro, local, free) | English and several major languages | voices such as `af_heart` (US English); `--speed 1.05`; `--list` shows voices; output 24 kHz mono |
| Other local engines (Piper, MMS VITS) | languages a first engine covers poorly | test pronunciation of the brand name |
| Hosted voices (any provider the user has) | expressive or cloned brand voices | paid: ask first; record the licence |
| A human recording | flagship pieces | send the script with the timing budget per line |

- One take per sentence (or per section): more control over placement and fixes.
- Post-process every take: trim edges, normalise to about -18 LUFS, resample to 48 kHz stereo.
- Fix mispronunciations by rewording or respelling in the `tts` field, never by fighting the engine.
- Speed: about 1.05 for explainers, up to 1.10 for hype; above about 1.1 an English voice sounds synthetic. Too long for the slot: shorten the sentence.
- **Placement:** first line at section start + 0.3-0.5 s; on a title card at card start + 1.4 s so the name is spoken as the card settles; outro + 0.3 s. Measure each take and let the voice set scene lengths; the tightest acceptable gap between takes is about 0.27-0.4 s.

## Mix and loudness

| Setting | Value |
|---|---|
| Music bed under voice | 0.30-0.34, ducked by the voice |
| Sidechain duck | threshold 0.02, ratio 12-16, attack 6 ms, release 650 ms (the bed swells back between phrases) |
| Voice | about 1.6-1.8 relative gain over a 0.30 bed |
| SFX bus | 0.9, single cues capped at about 0.7 |
| Sum | `amix` with `normalize=0` (the default halves every input) |
| Delivery | about -14 LUFS integrated, true peak -1.5 dBTP, LRA 11 (social and web); a limiter at 0.95 when not normalising |

In HyperFrames, prefer the composition's own audio tools: a voiceover carve on the music bed (grouped voice clips as its source, strength about 0.8) and volume automation lanes for fades, one mechanism per track. Outside it, [../scripts/duck_mix.sh](../scripts/duck_mix.sh) runs the ffmpeg chain:

```bash
ffmpeg -nostdin -i music.wav -i vo.wav -filter_complex \
 "[0:a]volume=0.30[m];[1:a]volume=1.8,asplit=2[vo][sc];\
  [m][sc]sidechaincompress=threshold=0.02:ratio=16:attack=6:release=650[md];\
  [md][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]" \
 -map "[a]" -ar 48000 -ac 2 -t 45.0 mix.wav
```

- Duck in a two-input pass to a WAV first, then mux; a large multi-input graph can silently truncate.
- Force the final length with `-t` (never `-shortest`) and pad audio to the picture (`apad`): loudness normalisation can return a few tens of milliseconds short.
- Final fades: 0.3-0.4 s in, 1.2-2.4 s out at the very end only; joining two beds, a 1 s quarter-sine crossfade.
- Gates: no clipping (`volumedetect` max below 0 dB), no dead air over 0.8 s in a short piece, audio length equal to picture length, every boundary listened to.

## Gate

The ledger lists every audio file and its licence; the beat grid is measured; locks and SFX are planned with their times; voice takes fit their slots; the mix meets the loudness target and matches the picture length.
