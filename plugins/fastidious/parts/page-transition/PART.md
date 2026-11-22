# page-transition

**Job.** Moving from one page to another feels like one continuous place: the header holds still, the page content rises away and the next arrives, and a picture or title the visitor clicked travels with them into the page it opens.

| Field | Value |
|---|---|
| Beat intents | `manipulate`, `reveal` |
| Rung | 1 (browser View Transitions API, no library); rung 2 when it hands off to a `view-change` part |
| Role | `supporting`; the shell other transitions plug into |
| Cost band | Very low: 5.9 KB module (unminified) and 1.3 KB CSS, no dependencies |
| Licence | MIT (Fastidious, original), see `LICENSE` |

## How it works

`mountPageTransition(options)` intercepts same-origin links, fetches the next page (prefetched on hover or focus), and swaps only the element marked `data-pt-container`. Three paths, in order:

1. **View Transitions API** where the browser has it. Elements marked `data-pt-name` inside a link's `data-pt-group` and inside the new page's matching `data-pt-group` morph into each other (for example the card's picture becoming the page's hero).
2. **A `view-change` part** (`type-curtain`, `pixel-cover`) through `await cover.play(swap)`, when view transitions are missing or turned off.
3. **A plain swap.**

Every path updates the address, history (back and forward work), the title, moves focus to the new page's `h1`, scrolls to the top and announces the new title to screen readers. If the fetch fails, the browser simply loads the page. For a site with no script at all, the CSS alone turns on the browser's cross-document transitions where supported.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `container` | `'[data-pt-container]'` | The part of each page that changes |
| `links` | `'a[href]'` | Add `data-pt-skip` to a link to leave it alone |
| `cover` | `null` | A `view-change` part instance |
| `useViewTransitions` | `true` | |
| `prefetch` | `true` | |
| `onLeave(old)`, `onEnter(new, url)` | | Destroy parts in the old page, mount parts in the new one |
| CSS `--pt-duration`, `--pt-ease` | `.45s`, a strong in-out curve | |

Markup: `data-pt-group="<id>"` on a card link and on the matching page's wrapper; `data-pt-name="img"` (or `title`, `price`) on the elements that should travel. Names only need to be unique within a group.

## Cost (measured)

Clean-room example (an index and two detail pages), headless Chrome with software rendering: about 60 fps desktop, mobile and reduced motion; no long tasks, no overflow, no errors. Navigation tested on both paths (view transitions, and the `pixel-cover` fallback): the address and title change, focus lands on the new `h1`, the announcement is made, the page script is not reloaded (the shell persists), and Back returns to the index.

## Fallbacks

- **Reduced motion:** the swap happens without animation; covers are skipped.
- **Old browsers:** the cover path or a plain swap; with no script, ordinary page loads.
- **Screen readers:** a polite live region announces each new page title; focus moves to its heading.

## Differs from

- `view-change/type-curtain`, `view-change/pixel-cover`: they hide one swap. This part decides when a swap happens, fetches the page, keeps history and focus right, and can use them as its cover.

## Provenance

- Fills the wanted part "Page transition shell" (seen in Codrops' interlude Astro starter).
- The shared-element idea follows [Animating Multi-Page Navigations with Browser View Transitions and Astro, Codrops](https://github.com/codrops/astro-shop-view-transitions) (MIT); built as an original, framework-neutral part, with no code from the Astro demo.
- Admitted: 22 November 2026, intake run 006.
- Clean-room test: an invented moorland walking guide, Granite Way (peat, lichen, sky; Bagnard, Hanken Grotesk, Trispace). Passed.
