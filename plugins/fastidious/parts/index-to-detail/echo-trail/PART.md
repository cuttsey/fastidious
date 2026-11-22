# index-to-detail / echo-trail

**Job.** When the visitor opens an item, a trail of its image echoes from the grid to the detail view and wipes away, so they see where the detail came from; closing returns them to the same item.

| Field | Value |
|---|---|
| Concept | [`index-to-detail`](../CONCEPT.md) |
| Beat intents | `manipulate` |
| Rung | 2 (GSAP core) |
| Role | `supporting`; `signature` on a portfolio or product range where browsing the index is the idea |
| Cost band | Low: 2.7 KB module + GSAP core (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `grid`, `panel` | required | | Panel holds `.et-panel-img`, `.et-panel-body` and a `.et-close` button |
| `items` | `'.et-item'` | | Each holds an `<img>`; buttons or links preferred; other elements are made focusable |
| `onOpen(item, panel)` | none | | Fill the panel's words from the item; the part only moves pictures |
| `chrome` | `[]` | | Elements to fade while open (header, filters) |
| `direction` | `'top-bottom'` | four directions | Wipe direction for echoes and reveal |
| `steps` | `6` | 3 to 10 | Number of echoes |
| `stepDuration`, `stepInterval`, `pause` | `0.35`, `0.05`, `0.14` | | Total open time is about 1.2 s at defaults; keep it under 1.5 s |
| `path` | `'linear'` | `'linear'`, `'sine'` | Sine arcs the trail |
| CSS `--et-panel-bg`, `--et-panel-ink`, `--et-radius` | | | |

## Cost (measured)

Clean-room example, headless Chrome: 60 fps, 0 ms of long tasks opening and closing, on desktop and mobile; no overflow. Echoes are temporary fixed elements animated with opacity and clip-path, removed when done.

## Fallbacks and access

- **Reduced motion:** crossfade to the detail, no echoes.
- **Keyboard:** items open with Enter or Space; focus moves to the close button on open and back to the item on close; Escape closes; the grid and chrome are `inert` while the panel is open. Tested: focus lands on the close button, then back on the item.
- **No JavaScript:** items are plain buttons; give them real links to detail pages if the site has them.

## Provenance

- Source: [Repeating Image Transition, Codrops](https://github.com/codrops/RepeatingImageTransition), MIT.
- Admitted: 22 November 2026, intake run 002.
- Changed: rebuilt as a module taking grid, items and panel from the host; reads `<img>` elements instead of inline background styles; WebGL "silk" and "ink" surfaces removed (flat echoes only, keeping it at rung 2); scroll lock no longer assumes Lenis; kept the source's keyboard, inert and reduced-motion behaviour.
- Clean-room test: restyled as an invented ropemaker's product index (cold grey, original artwork, not a fashion lookbook). Passed.
