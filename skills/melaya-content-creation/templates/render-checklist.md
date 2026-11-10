# Render checklist

Copy into `qa/report.md` and tick each line. Method: [../modules/render-qa.md](../modules/render-qa.md).

## Before render
- [ ] Root `data-duration`, `meta.json` and the timeline length are equal ({s} s)
- [ ] Every library and asset is local and relative; the asset ledger is complete
- [ ] Lint clean; check passes with 0 errors; every warning read
- [ ] Fonts: one static file per weight, declared on every scene root

## Draft and look (times from the storyboard)
- [ ] Settled reveals: {t1, t2, ...}
- [ ] Mid-transitions: {t1, t2, ...}
- [ ] Mid-morphs and logo hand-off: {t}
- [ ] First and last frames
- [ ] Contact sheet (2 fps, 6x6)
- [ ] No overflow, collisions, fallback fonts, empty frames, muddy crossfades, grey grounds
- [ ] Nothing essential under the caption zone (band drawn on the longest-cue frame)

## Final render
- [ ] Frame count {frames} and duration {s} confirmed with ffprobe; audio as long as picture
- [ ] Loudness about -14 LUFS integrated, true peak about -1.5 dBTP, no clipping, no dead air over 0.8 s
- [ ] Each spoken name lands on its settled title; locked reveals within a frame of their word or cue
- [ ] Poster picked at a settled frame ({t} s) and baked as frame 0
- [ ] Delivery encodes made: {master, social, 4K, chat}
- [ ] Captions: SRT and VTT per language; burned version checked for font and position
- [ ] Every deliverable named per the publishing package
