# lagging-columns

**Job.** Gives a grid a little weight as it scrolls: outer columns trail the centre and settle a moment later, so a catalogue or index feels physical without slowing anyone down.

| Field | Value |
|---|---|
| Beat intents | `depth` |
| Rung | 1 (plain JavaScript, transform only; no GSAP) |
| Role | `supporting` |
| Cost band | Very low: 1.4 KB module, no dependencies; the loop sleeps when nothing moves |
| Licence | MIT (Codrops), see `LICENSE` |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `grid` | required | any grid or flex wrap | The host's own layout; columns are detected from where items sit |
| `baseLag` | `0.1` | 0.06 to 0.2 | Follow speed of the centre column per frame; lower trails more |
| `lagStep` | `0.025` | 0.01 to 0.04 | Extra trail per column away from the centre |
| `maxOffset` | `140` | 60 to 200 px | Cap on how far a column may trail |
| `itemSelector` | `:scope > *` | | |

## Cost (measured)

Clean-room example, headless Chrome: 60 fps, 0 ms of long tasks on desktop and mobile, no overflow.

## Fallbacks

- **Reduced motion:** off; the grid scrolls normally. Listens for the preference changing.
- **Keyboard and screen readers:** the DOM is never restructured, so reading and tab order stay row by row. (The source rebuilt the grid into column wrappers, which changed reading order to column by column.)
- **No JavaScript:** a normal grid.

## Differs from

- `sticky-stack`: both add depth on scroll, but sticky-stack is for a sequence of full sections; lagging-columns is for many small items at once.

## Provenance

- Source: [Elastic Grid Scroll, Codrops](https://github.com/codrops/ElasticGridScroll), demo 1, MIT.
- Admitted: 22 November 2026, intake run 002.
- Changed: ScrollSmoother removed (the page keeps native scrolling, and the part no longer needs GSAP's smoother wrapper markup); per-item lag replaces column wrappers so DOM order is kept; idle loop; reduced-motion off switch; demo portraits and fonts removed.
- Clean-room test: restyled as an invented hardware catalogue of product cards (not portrait photography). Passed; the lag reads as weight, not as a photo-gallery effect.
