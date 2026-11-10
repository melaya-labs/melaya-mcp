# Storyboard template

Copy to `content-output/<slug>/storyboard.md`; keep `timeline.json` in sync. Method: [../modules/storyboard.md](../modules/storyboard.md).

## Storyboard: {piece name}

- **Format:** {W}x{H}, 30 fps, {total} s = {frames} frames
- **Tone / look:** {tone-...} / {look-...}
- **Signature:** ground {}, camera verb {}, transition family {} (+ accents {}), true morph {}, spine device {}
- **Rhythm:** {e.g. fast, fast, SLOW, CUT, hold}
- **Music:** {track, BPM, slice start}; strong cues {D1 s, D2 s, D3 s}; beat-grid windows {}
- **Voiceover anchors:** {line key at s}
- **Caption zone reserved:** {yes: bottom 130 px / lower third / none}

### Scene {NN} - {name} ({start}-{end} s, {dur} s)
- **On screen:** {what is seen; the real product material referenced}
- **Reads:** "{exact words}" (hold {s} s settled)
- **Voiceover:** "{verbatim}" / none
- **Hero element:** {the one thing the eye finds first}
- **Motion verbs:** {element: SLAMS / RISES / TYPES ON / DRAWS / FLOATS / PUSHES IN / MORPHS INTO}
- **Sequential or interactive:** {"3 rows arrive one per beat" / "cursor clicks Approve" / none}
- **Morph:** {A becomes B, lands on {cue}} / none
- **Audio intent:** {what sound does here}; cue {s}
- **Transition out:** {name}, {duration} s, {centred on / landing on} {cue}

(repeat per scene; durations add up to {total} s)

### Checks
- [ ] Durations add up
- [ ] Every read respects the floor (0.8 s for 1-3 words, 0.3 s per word, 1.2 s minimum)
- [ ] Movement at least every 2-3 s; no scene over 6 s without a camera move
- [ ] Every sequential reveal and simulated interaction is named
- [ ] Nothing essential in the caption zone or outside the safe box
