# view-change / pixel-cover

**Job.** Covers the screen with a sweep of blocks in the brand's colour, changes the view behind them, and sweeps them away: a quick, graphic change of view.

| Field | Value |
|---|---|
| Concept | [`view-change`](../CONCEPT.md) |
| Beat intents | `manipulate` (between views) |
| Rung | 2 (GSAP core) |
| Role | `supporting`; `signature` on a graphic, digital or playful brand |
| Cost band | Low: 1.3 KB module + GSAP core (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Use

Same API as `type-curtain`: `await mountPixelCover(opts).play(swap)`.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `rows`, `columns` | `8`, `14` | Bigger cells read bolder; smaller read finer |
| `direction` | `'down'` | `'up'` sweeps from the bottom |
| `duration`, `spread`, `jitter` | `0.4`, `0.03`, `5` | Jitter breaks the edge of the sweep |
| CSS `--pxc-colour`, `--pxc-gap` | | Pick a colour that contrasts with both the view you leave and the view you arrive at (the composition test caught an orange cover vanishing over an orange section). A gap shows the grid; leave it at 0 for a solid cover |

## Cost (measured)

60 fps, 0 ms of long tasks, desktop and mobile. Total change about 1.3 s.

## Fallbacks and access

Reduced motion: a flat fade covers the swap. The overlay is `aria-hidden`; move focus into the new view in the swap callback.

## Provenance

- Source: [Pixel Transition, Codrops](https://github.com/codrops/PixelTransition), demo 1, MIT.
- Admitted: 22 November 2026, intake run 004 (rejected in run 002 as a trend look; that reason no longer applies).
- Changed: shares `type-curtain`'s promise API; builds its own cells; cells overlap slightly so no seam shows the swap (the source left hairline gaps); reduced-motion path; demo content removed.
- Clean-room test: the ironmonger's two views, rust blocks on iron grey. Passed.
