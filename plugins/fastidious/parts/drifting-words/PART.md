# drifting-words

**Job.** Turns a list of the brand's own words (materials, services, ingredients, places) into a slow typographic field: each word drifts across the columns as it enters, settles at the centre, and drifts away as it leaves.

| Field | Value |
|---|---|
| Beat intents | `depth`, `rest` |
| Rung | 2 (GSAP, ScrollTrigger) |
| Role | `signature` on a type-led page whose idea is its vocabulary; otherwise `supporting` |
| Cost band | Low: 1.1 KB module + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Notes |
|---|---|---|
| markup | `.dw` grid; `[data-dw]` words with `data-dw-home` and `data-dw-away` column numbers | `.dw-break` adds space between groups |
| `columns` | `10` | Grid columns |
| `ease` | `expo.inOut` | `data-dw-ease` per word |
| CSS `--dw-gap`, `--dw-row`, `--dw-space` | | |

Pair with `text-emphasis/scramble` for words that decode as they arrive.

## Cost (measured)

60 fps on desktop and mobile; 91 ms of long tasks at load on desktop and 56 ms on mobile (setting up one trigger pair per word), 0 ms while scrolling. Transform only; the page keeps its native scroll.

## Fallbacks and access

- **Reduced motion and no JavaScript:** every word rests in its home column.
- **Small screens:** home columns collapse to the left edge and the drift still plays; words never cause sideways scrolling.
- **Screen readers:** words are ordinary text in reading order.

## Provenance

- Source: [Scroll Text Motion, Codrops](https://github.com/codrops/ScrollTextMotion), MIT. The demo credits satto.studio as its inspiration; recorded here as a fact, not a verdict.
- Admitted: 22 November 2026, intake run 004.
- Changed: the drift is a transform computed from column numbers, not a class swap measured with Flip, so nothing reflows; ScrollSmoother no longer required; reduced-motion and mobile rules added; demo words and fonts removed.
- Clean-room test: an ironmonger's vocabulary with rust initials spelling the name. Passed.
