# index-to-detail / push

**Job.** When the visitor opens an item, every other item is shoved off the screen in the direction it sits, while the chosen picture flies into the detail view; on close they all come back. Opening one thing visibly makes room for it.

| Field | Value |
|---|---|
| Concept | [`index-to-detail`](../CONCEPT.md) |
| Beat intents | `manipulate` |
| Rung | 2 (GSAP core and Flip) |
| Role | `supporting`; `signature` on an index page whose idea is choosing one thing out of many |
| Cost band | Low: 6.0 KB module (unminified) + GSAP core and Flip (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

Same markup contract and options as `echo-trail` and `flip` (`grid`, `panel`, `items`, `chrome`, `onOpen`), so a build can swap variants with one line. Plus:

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `duration` | `0.9` | 0.7 to 1.2 s | |
| `ease` | `expo.out` | out-eases | A hard start reads as a shove |
| `gap` | `24` | 0 to 80 px | How far past the screen edge pushed items travel |

Items above the chosen one leave by the top, below by the bottom, beside it by the left or right. The panel background fades in late (three quarters through the move), so the push is seen before the detail covers it.

## Cost (measured)

Clean-room example, headless Chrome with software rendering (floor checks): 59.9 fps desktop, 60 fps mobile and reduced motion; no long tasks, no overflow, no errors. Transform and opacity only. Open and close tested: focus moves to the close button on open and back to the item on Escape; every item returns to its place.

## Fallbacks

- **Reduced motion:** no push; the index fades out and the detail fades in.
- **Keyboard and screen readers:** items are buttons; the index is made inert while the detail is open; Escape closes.

## Differs from

- `flip`: the others fade quietly; here they are pushed away. Use `push` when making room is the point, `flip` when opening detail is routine.
- `echo-trail`: echoes make the journey of the picture visible; `push` makes the space around it move.

## Provenance

- Source: [Grid Item Push Animation, Codrops](https://github.com/codrops/PushGridItems), demo 1, MIT; concept by Rémi Clauss.
- Admitted: 22 November 2026, intake run 006.
- Changed: rebuilt on the shared index-to-detail contract; neighbours pushed with transforms rather than re-placed in grid rows and columns, so it works with any grid; focus management, Escape and reduced motion added; the panel keeps the shared detail layout.
- Clean-room test: an invented tool lending library, Saltbox (moss green and bone; Mattone, Libertinus Sans, Trispace). Passed.
