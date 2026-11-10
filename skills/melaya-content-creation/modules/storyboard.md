# Storyboard and beat planning

> **Use when:** turning a script into timed scenes, planning beats against music or voiceover, writing a shot list, or re-laying out a piece for another format.
> **Inputs:** `script.md`, one tone preset and one look from [../styles/](../styles/), the target format from [platforms.md](platforms.md).
> **Outputs:** `storyboard.md` (template: [../templates/storyboard.md](../templates/storyboard.md)), `timeline.json`, and a shot list when footage or captures are needed ([../templates/shot-list.md](../templates/shot-list.md)).
> **Next:** [design-system.md](design-system.md), then the build ([hyperframes.md](hyperframes.md)); [audio.md](audio.md) in parallel.

The storyboard is the contract between the plan and the build. It names what is seen, read and heard in each scene and why; the build decides selectors, tweens and code.

## Every scene states

| Field | Example |
|---|---|
| Name, start-end, duration | `03 - Approve (7.7-10.0, 2.3 s)` |
| On screen | "The paused send row grows into an approval card; the user's cursor approves" |
| Reads | exact words, with the settled hold of each |
| Voiceover | the verbatim line, if any |
| Hero element | the one thing the eye finds first (twice the size of anything else, found within 300 ms) |
| Motion verb per element | SLAMS, RISES, TYPES ON, DRAWS, FLOATS, PUSHES IN, MORPHS INTO |
| Sequential or interactive | "three rows arrive one per beat", "cursor clicks Approve"; or none |
| Transition out | family and mood (clean, hard, dramatic, soft, chaotic) |
| Audio intent | what sound should do emotionally; music cue to aim at |

Name every sequential reveal and every simulated interaction explicitly. A builder will not invent rhythm the plan did not ask for.

## Durations

- Count them: the scene durations must add up to the target. A 15-25 s piece usually lands at 18-22 s.
- Beats of 1.5-3.5 s; a 5-7 word line needs 2-2.5 s; no scene over about 6 s without a camera move inside it.
- First visible motion within 0.2 s of a scene start. Movement at least every 2 s in vertical, every 2-3 s elsewhere.
- One deliberate held frame per piece (the payoff or the lockup), at least 1.5 s.
- Nothing essential in the first and last 0.35 s of a clip that will be joined to others ([films.md](films.md)).
- Declare the rhythm before building: "fast, fast, SLOW, fast, CUT, hold".

## Signature per piece (or per clip in a film)

| Element | Choose one | Rule |
|---|---|---|
| Ground | dark, light, brand-colour full bleed, split, warm | adjacent clips never share one |
| Camera verb | fly-through with parallax, slow dolly with rack focus, orbit of a hero object, whip pans, orthographic schematic with self-drawing lines, overhead crane, radial contraction, vertical dive | one per clip; pan and zoom on separate wrappers |
| Transition family | one primary plus one or two accents ([transitions.md](transitions.md)) | the most distinctive at the opening, the boldest on the hero reveal |
| True morph | at least one: an element becomes the next ([morphs.md](morphs.md)) | named concretely: "the cursor puck becomes the Hand-back button" |
| Spine device | one object or motif that threads every beat (a light that only grows, a mascot, a wheel) | makes separate beats read as one piece |

## Pacing by tone

The tone preset sets scene count, scene length and transitions; see the presets in [../styles/](../styles/). Quick reference:

| Tone | Scenes in 20 s | Scene length | Transitions |
|---|---|---|---|
| playful (default) | 4-5 | 3-5 s | crossfade, clean slide |
| polished | 3-4 | 4-6 s | slow crossfade 0.6-0.8 s |
| startup-parody | 4-5 | one claim each | hard cut, minimal |
| chaotic | 6-8 | some under 2 s | hard cut, flash, zoom cut |
| deadpan | 3-4 | 4-7 s | very slow crossfade 0.8-1.0 s |
| cinematic | 4-5 | 3-5 s | dramatic wipe, crossfade with scale |
| feature-cards | 4-6 | 3-4 s | clean slide or wipe 0.35-0.45 s |

## Music and voice anchors

- With music: pick 1-3 **strong cues** (drops, swells, strong downbeats) for the major moments (hero reveal, true morph, logo) and a beat-grid window for sequential reveals. Cue data is guidance; readability and story win ([audio.md](audio.md)).
- Sequential **text** on a fast grid (beats under 0.6 s apart) snaps to every other beat, or arrives quickly and holds as a set. Accents (dots, glows, ticks) may hit every beat.
- With voiceover: the voice sets the length. Lay scenes out from the measured voice takes, then lock big reveals to spoken words.

## timeline.json: one source of truth

Write timing once, in frames at the delivery frame rate (30 fps by default), and let every script read it: the build, the mix, the captions, the review copy, the chapters.

```json
{ "fps": 30, "width": 1920, "height": 1080,
  "segments": [
    { "name": "hook", "start_frame": 0, "frames": 75 },
    { "name": "reveal", "start_frame": 75, "frames": 105 } ],
  "voiceover": [ { "key": "hook", "start_s": 0.5 } ],
  "music": { "file": "assets/music/bed.wav", "start_s": 0 } }
```

A length change is one edit here, never a hunt through several files.

## Vertical one-shot planning

For a vertical piece, plan a **world map** instead of a shot list: a tall world (about 400 px per second of runtime) with stations at absolute coordinates, and a table of `t | camera (x, y, zoom, ease) | station or event | bridge object`. Each row's exit is the next row's entrance. The pain is a place the camera travels through; the product is an event that happens to that place. Without such a physical metaphor there is no one-shot: find one before building.

## Shot list (when real footage or captures are needed)

For each shot: surface (phone, desktop, browser), screen or URL, the action, length to capture, speed it will play at, data to stage, and privacy notes. Record each surface separately at native resolution, unedited.

## Gate

Durations add up, every scene has its fields, reads respect the floor, the signature is named, the anchors (cues or voice) are listed, and `timeline.json` matches the storyboard.
