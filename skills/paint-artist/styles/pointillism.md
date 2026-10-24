# pointillism: Seurat

Preset: [pointillism.json](pointillism.json). Analysing A Sunday on La Grande Jatte selects this base.

## What defines it

No strokes at all: small round dots of pure, unmixed hues placed side by side so they mix in the eye (optical mixing), with complementary dots next to each other for vibration (orange near blue, red near green). Even dot size, a regular rhythm, a light ground.

## Recipe

| Layer | Tool, width | Key settings |
|---|---|---|
| dots | Brush 7 | hex grid every 6 px, `jitter` 0.25, colours by Floyd-Steinberg error diffusion in linear RGB, `complement` 0.06 |
| dots | Brush 5 | every 5 px where the canvas still differs by more than 7 dE |
| dots | Brush 3 | every 4 px on `detail` where it differs by more than 9 dE |

Palette: 20 fixed pure pigments (`mode: fixed`): whites, lemon, cadmium, orange, vermilion, crimson, pink, lilac, violet, ultramarine (light and dark), cobalt, cerulean, pale blue, emerald, viridian, yellow-green, ochre, sienna. No ground: dots on white.

## Do / don't

- Do keep the palette pure: the mixing must happen between dots, never in a single swatch.
- Do expect many dots (about 30,000 at 450x672, est. 450 s); the time cap trims the finest layer on bigger canvases.
- Don't use oil or watercolour (their texture blurs the dots); don't add outlines.

Live test candidate: no; it is the slowest style per area.
