# Films: several clips, parallel builds, assembly

> **Use when:** a piece runs past about 25 s or covers more than one product or feature, clips are built in parallel by several agents or people, clips must be joined on exact frames, or a long live process becomes a sped-up vertical video.
> **Inputs:** `storyboard.md` with a segment table, the master music track, the voiceover script if narrated.
> **Outputs:** `timeline.json` (segments in whole frames), `FILM_BRIEF.md`, one folder per clip, the assembled film, a review copy with burned counters.
> **Next:** [render-qa.md](render-qa.md), [review.md](review.md).

One clip tells one story in 15-25 s. Stretching one build to 60-70 s gives repetition, generic components and bad pacing. A longer film is several units, each built with the full workflow, joined on one master track.

## Structure

| Unit | Length (30 fps) | Job |
|---|---|---|
| Intro | about 7.7 s (230 frames) | build-up with no product UI; ends on a held breath (no text in the last 0.5 s, the hero pushed toward camera) exactly where the music drops |
| Bridge (narrated films) | 4 s (120 frames) | a title card before each product, from one template; the voice names the product at bridge start + 1.4 s |
| Product or feature unit | 12-16 s (for example 15.5 s = 465 frames) | one product: its own ground, camera verb, transition family and true morph |
| Outro | 8-10 s (240-300 frames) | one continuous shot: the products collapse into the mark, the tagline lines build as spoken, the real logo and URL hold to the end; the only unit with a baked music fade |

Grounds alternate across units (dark, colour, dark, light...); adjacent units differ the most. A recurring device (the same bridge template, a wheel that keeps turning from one bridge to the next) gives a long film its spine; the same entry into every unit with varied exits keeps it from feeling mechanical.

## The segment contract

| Contract | Value | Why |
|---|---|---|
| Frames | exact whole frames at 30 fps | units are placed on exact frame boundaries; the builder asserts the count |
| Canvas | the film's (1920x1080 or 1080x1920) | joins composite full frames |
| Music | the unit's own slice of the master, from 0, full length, at volume 1.0, no fades | the film plays the master underneath; locks stay aligned |
| Locks | 1-3 strong downbeats of the slice within 0.15 s | slices are cut on the same grid |
| Edges | nothing essential in the first and last 0.35 s | the join covers the first 0.45 s of the incoming unit |
| First and last frames | frame 0 is a full strong image; the last frame is settled | the join freezes the last frame |
| Poster | none baked (or stripped before assembly) | a baked poster flashes for one frame at every join |
| Folder | each builder writes only in its own folder | parallel builders never collide |
| Tagline | reserved for the intro and outro | no repetition |
| SFX | each unit writes its cue list with local times | the mixer shifts them by the unit's start (joins drop clip audio) |

Generate `timeline.json` once (name, start frame, frames, start and duration in seconds) and drive everything from it: the music slices, the builder, the mix, the captions, the review counters, the chapters.

## Parallel production

1. **Orchestrator first:** the segment table, the music (one master, extended on bar lines, sliced per unit on whole frames, a beats file per slice), the signature matrix, a source map (the exact UI files for each unit), and one shared `FILM_BRIEF.md`.
2. **Signature matrix:** no two units share a ground, a camera verb, a transition family or a morph type; one shader family in at most three units; each unit uses at least three distinct transitions (all shader or all CSS) and one true morph.
3. **Per-unit brief** (short): read the film brief; your product and folder; the contract (canvas, exact frames, slice and beats file with its strong downbeats, edges); the real UI sources; the moment (entry, key action, result) and the copy to keep verbatim; your signature; at most four reads; reply with the path, the ffprobe frame count, the transitions and morph with their times, and any limitation.
4. **Corrections mid-run:** one fact, one instruction, one file to touch; broadcast a renderer gotcha to every builder as soon as one hits it. Never resend the whole brief.
5. **Concurrency:** about 8 builders on one machine worked with 2 render workers each; vendor every library (CDN loads time out under load); long renders in the background with a polled log.
6. **Bookends:** give the intro and outro builders the measured shape of their slice (last hit, silences, an off-grid re-entry) and build their choreography on it.

## Assembly: freeze-frame joins

Shader transitions capture DOM, not playing video, so the film is a CSS-only composition: units play back to back as video elements on exact frame boundaries with the master audio underneath (sync cannot drift), and at each join the outgoing unit's last frame (a PNG) exits over the first 0.45 s of the incoming unit.

```bash
# per unit: strip a baked poster (drop frame 0, clone the new first frame), silent, CFR, dense keyframes
ffmpeg -nostdin -y -i unit.mp4 -an -vf "select=gte(n\,1),setpts=N/FRAME_RATE/TB,tpad=start=1:start_mode=clone" \
  -r 30 -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -g 15 assets/clips/unit.mp4
ffmpeg -nostdin -y -i unit.mp4 -vf "select=eq(n\,FRAMES-1)" -vframes 1 assets/freeze/unit.png
```

| Join | Recipe on the freeze layer (0.45 s) | Use |
|---|---|---|
| zoom-flash | scale 2.2, blur 14 px, opacity 0 in 0.22 s `expo.in`; a white layer 0.85 to 0 in 0.28 s | the music drop (spend it once) |
| zoom-through | scale 3.2, blur 10 px, opacity 0 in 0.36 s `expo.in`, after the outgoing unit pushed in (about 1.9x) in its last 0.35 s | bridge into its product |
| iris | circle clip driven by a CSS variable 75 to 0, `power3.in` | centred subjects |
| split | two diagonal halves (62% / 38%) fly apart x plus or minus 1400, y minus or plus 160, `power4.in` | ground flips |
| blinds | 8 strips of 135 px collapse on scaleY, stagger 0.03 | tech units |
| whip | x -2100, blur 18 px, 0.38 s `power4.in` | topic change |
| clock | conic mask 360 to 0, `power2.inOut` | time |
| card-fall | scale 0.55, radius 48, y 80, then y 1300, rotation 8 | dark to light ending |

Never repeat a join kind in one film; match the incoming unit's family for continuity, contrast it when the ground flips. Freeze layers alternate two tracks so neighbouring joins never share one. Assert in the builder that every join kind used has an animation (a missing one renders as a static freeze).

Render the film (about 6-8 min for 110-135 s at 3 workers), then the **finish pass**: mux the mix and burn captions on the captionless film in one script, so a caption or mix fix never re-renders the picture ([captions.md](captions.md)).

## Review copy with burned counters

For timecoded notes, burn a unit-local label (`{UNIT} local SS.cc s fN`) top-left and a global timecode top-right (both at the top when captions own the bottom), computed from frame numbers (`n - startFrame`, `between(n, a, b)`), never from time (a time-based counter reads one frame low). Long filter graphs go in a filter script file. CRF 22-23, preset veryfast.

## Process timelapse (vertical, 60-75 s)

For a long live process (an agent drawing, building, filling forms): hook in the first second (the finished result plus a two-line claim), then each sub-task full-frame at **one honest integer speed per segment** labelled on screen ("16x, uncut"), aiming for 11-22 s on screen per segment (speed = live seconds / target seconds); a real wall-clock stopwatch and a progress minimap; the last segment pulls back to the assembled result; the claim, then the lockup held at least 1.5 s. Cut the work area and the stopwatch at the same speed (`setpts=PTS/16`); overlays inside the vertical safe box.

## Gate

Every unit's frame count matches `timeline.json`; joins grabbed at J-0.1, J+0.12, J+0.30 and J+0.6 s and looked at; a 2.5 s contact sheet of the film; one master audio under everything with SFX mixed back in; the review copy built.
