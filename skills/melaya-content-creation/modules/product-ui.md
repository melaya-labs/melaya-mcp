# Product UI and simulated use

> **Use when:** a scene shows the product being used: recreating screens from the source, staging mock data, simulating cursors, typing, taps, toggles and approvals, or placing real screen recordings inside the design.
> **Inputs:** the UI inventory in `brand-kit.md`, the repo or site, `storyboard.md` (the entry, key action, result beats).
> **Outputs:** recreated UI scenes (HTML and CSS) with fictional data, an interaction schedule (cursor path, presses, typing), notes on any footage used.
> **Next:** [hyperframes.md](hyperframes.md); [audio.md](audio.md) for the matching clicks and key ticks.

The product doing its job beats the product describing itself. Recreate it from source instead of using screenshots: a recreation is crisp at any camera distance, every element can move and morph, and the copy is exactly the product's.

## Method

1. **Find the screen.** Trace route, page, components (web, extension, mobile, native) for each beat of the flow.
2. **Read the source, never guess.** Grid, paddings, radii, labels, colour constants, icon names, state names, button order. For a large component, have a helper extract the visual anatomy (layout px values, card anatomy, states, tokens, three real sample rows) with file and line citations.
3. **Keep real copy verbatim:** labels, state names, ids in the monospace face.
4. **Pick one working moment:** entry, key action, result, lived as a user would. Not a tour of every panel.
5. **Recreate the minimum the moment needs,** absolutely positioned (or measured once at setup) so cursors and morphs can target each element. Icons from path strings, real integration logos copied locally, colours from the source constants.
6. **Include three or more real secondary affordances** (filters, toolbars, toggles, zoom buttons, export): without them a scene reads as a demo, with them as the product.
7. **Push beyond the product only in staging:** camera, light, depth, grounds. The UI itself stays true.

Concept or trust stories (security, autonomy, scale) can use a physical metaphor with one giant word per beat instead of UI; keep UI grammar for product demos.

## Data rules

- Fictional people and companies, `.example` domains, a generic "Community" app instead of a real social network. No real private individuals, no real customers, no impersonated brands.
- Real third-party names and logos only where the product genuinely integrates them, unaltered.
- Small illustrative UI text is fine ("Order confirmed", "3/3 passed", a filename). Invented claims, metrics, scores and testimonials are not; counters and gauges show real UI states.
- Density from the real product: 4-12 items where the page shows 20 (typical: 12 tools, 8 connectors, 4 workflows); derived, seeded data, never `Math.random`.
- Real architecture only: a diagram is rebuilt from the actual docs, never with invented nodes.
- Keep the copy rules of the voice card; keep real ellipses in progress states ("Connecting..."); never add exclamation marks to success toasts.

## Simulated interaction

| Action | Recipe | Sound |
|---|---|---|
| Cursor travel | measured target, `power2.inOut` glide, tip offset applied (land the arrow tip, not its box) | none |
| Press | cursor scale 0.86 for 0.07 s with yoyo, origin at the tip; target button 0.94 in sync; label swap by instant set at +0.06 s | click at the bottom of the press (press starts 30 ms before the beat) |
| Click with weight | dip to 0.80 over 0.10 s, rebound `back.out(2.4)` over 0.16 s, button 0.94, 1.02, 1.0, then the consequence | click |
| Typing | per-character spans set visible over time, or a proxy counter slicing the string; human 0.019 s per character, a fast agent 0.008 s, a URL 45 ms | a key tick every third character, 3-5 per field, rotating about 8 samples |
| Caret | opacity 1 to 0.15, 0.25 s `steps(1)`, finite repeats | none |
| Tap ripple | 64 px ring, scale 0.3 to 1.7, opacity 0.95 to 0, 0.5 s `power2.out` | soft click |
| Toggle | on-layer fade 0.18 s, knob x 0 to 28 in 0.22 s `back.out(2)` | click, then the switch sound 60 ms later |
| Approve | fill layer inside the button 0.18 s, border to success 0.35 s, toast slides in | bell or soft impact |
| Status pill | "queued" to "running" (spinner one and a half turns within a beat) to "done" `back.out(2.2)` | drop |
| Scroll inside a card | y 0 to -N, 0.8 s `power2.inOut`, with top and bottom fade overlays | none |

- **Two cursors, two owners:** the user's arrow and the agent's own cursor (a puck or named pointer). At most two named cursors at once; fade them before the next camera move.
- **Measure targets once,** synchronously at setup, before any tween, after fonts load; never inside an update callback.
- **State is stacked siblings toggled by opacity** (enabled, disabled, running, done), never text rewritten in a callback (a seek or a discovery pass can fire callbacks out of order).
- Speed tells the story: a second row types faster than the first when the agent "learns".
- The most persuasive moment is often a pause: a write stopped for human approval, then approved.

## Real footage inside the design

- Ask for raw recordings of each surface separately, at native resolution, unedited (a portrait phone recording and the desktop as two files); cropping a composited demo into a phone reads as a strip.
- Map a long recording by sampling one frame every 30 s, then cut working clips with dense keyframes (`-g 15`) so they seek fast.
- Playback rate is energy: 2.4-3.5x on search and scroll, 1.2-1.5x where a value must be read. Keep `seek + duration * rate` inside the clip.
- Put recordings in a device or browser frame with a gentle push-in, and layer at least three moving elements over it (a counter, a self-drawing line, a status ring). Never pin callouts to scrolling footage; pin only to frozen frames.
- Grade b-roll to one look (for example brightness 0.5-0.72, saturation 0.5-0.66, contrast 1.08).

## Checklist per recreated screen

- [ ] Every label found by searching the source for the string.
- [ ] Colours from source constants or tokens.
- [ ] Ids and scopes exact, in the monospace face.
- [ ] Data fictional, `.example` domains; no invented number on screen.
- [ ] Three or more real secondary affordances.
- [ ] Elements absolutely positioned or measured once; decorative skeletons excluded from the layout audit.
