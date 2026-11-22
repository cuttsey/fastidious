# context-aware-fixed

**Job.** A fixed element (the logo, a booking link, a section label) steps aside while a picture or a clashing section passes underneath it, and comes back once it has passed, so it never sits awkwardly on top of the content.

| Field | Value |
|---|---|
| Beat intents | `reveal` (a supporting courtesy, not a beat of its own) |
| Rung | 2 (GSAP, ScrollTrigger, SplitText) |
| Role | `supporting` |
| Cost band | Very low: 5.9 KB module (unminified) + GSAP core, ScrollTrigger and SplitText (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

`mountContextAwareFixed(fixed, options)` returns `{ destroy }`. `fixed` is a selector, an element or a list of elements; mount separate groups to give them different effects.

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `blocks` | `'[data-caf-block]'` | | The sections the element should step aside for: full-bleed pictures, colour fields it would clash with |
| `effect` | `'slide'` | `slide`, `scale`, `scatter`, `shuffle` | `slide` lifts the content out of a mask; `scale` shrinks it to its left edge; `scatter` throws the letters; `shuffle` blinks the letters out and decodes them back |
| `duration` | `0.6` | 0.4 to 0.8 s | |
| `ease` | `power4` | out-eases | |
| `offsetStart` | `30` | 0 to 80 px | How early it steps aside before the block arrives |
| `offsetEnd` | `10` | 0 to 40 px | How long after the block has passed it waits |

The element's own position is read on every ScrollTrigger refresh, so it works wherever the element is fixed (top, bottom, a corner) and after a resize.

## Cost (measured)

Clean-room example (a logo and a booking link, three full-bleed pictures), headless Chrome with software rendering: 60 fps desktop, mobile and reduced motion; no long tasks, no overflow, no errors. Transform and opacity only (the source's blur effect was dropped). Checked at 14 scroll positions with real wheel scrolling: the element was hidden exactly when a block was under it and shown when none was.

## Fallbacks

- **Reduced motion:** a short fade out and back.
- **Keyboard:** focus brings the element back while a block is under it; it steps aside again when focus leaves.
- **Screen readers:** `scatter` and `shuffle` split letters with SplitText, which keeps the element's accessible name ("Book a boat", not letter by letter).
- **No JavaScript:** the element simply stays.

## Differs from

- `interruptible-menu`: opens and closes a menu on request. This part moves a fixed element out of the way by itself.

## Provenance

- Source: [Context-Aware Animation for Fixed Elements on Scroll, Codrops](https://github.com/codrops/ContextAwareLogoAnimationScroll), effects 1, 3, 4 and 5, MIT.
- Admitted: 22 November 2026, intake run 006.
- Changed: the element is wrapped or split once at mount instead of rewriting its HTML on every pass; whether it is hidden is read from the triggers rather than counted, so overlapping blocks and jumps in scroll never leave it stuck (a counting version failed this check during intake); trigger lines follow the element's real position; the blur effect was dropped; focus brings it back; reduced motion fades.
- Clean-room test: an invented narrowboat hire, Tidelock (paper, lock-gate red, canal green-black; Archivo, Libertinus Serif, Geist Mono). Passed.
