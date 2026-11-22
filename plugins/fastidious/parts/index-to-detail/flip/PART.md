# index-to-detail / flip

**Job.** When the visitor opens an item, its picture glides from the grid to the detail view and back again on close: the calm way to keep their place.

| Field | Value |
|---|---|
| Concept | [`index-to-detail`](../CONCEPT.md) |
| Beat intents | `manipulate` |
| Rung | 2 (GSAP core and Flip) |
| Role | `supporting` |
| Cost band | Low: 1.8 KB module + GSAP core and Flip (shared) |
| Licence | MIT (Fastidious, original), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

Same markup contract and options as `echo-trail` (`grid`, `panel`, `items`, `chrome`, `onOpen`), so a build can swap variants without touching markup. Plus:

| Input | Default | Safe range |
|---|---|---|
| `duration` | `0.9` | 0.6 to 1.1 s |
| `ease` | `power3.inOut` | in-out eases |

The panel becomes usable as soon as the picture has nearly landed (80% of `duration`), not after the words finish.

## Cost (measured)

Clean-room example, headless Chrome: 60 fps, 0 ms of long tasks opening and closing, desktop and mobile. Transform only (Flip in scale mode).

## Fallbacks and access

Same as `echo-trail`: crossfade under reduced motion; Enter or Space opens; focus moves to the close button and back to the item; Escape closes; grid and chrome are inert while open. Tested.

## Provenance

- Original Fastidious part, built 22 November 2026 (intake run 003) from the concept description, using GSAP Flip as a general technique. Codrops' GridToSlider showed the technique but was not ported: its job is a grid-to-slider mode switch with a hue-shift hover, not index-to-detail.
- Clean-room test: the same ropemaker's index as `echo-trail`, so the two variants can be compared side by side. Passed.
