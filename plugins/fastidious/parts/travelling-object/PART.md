# travelling-object

**Job.** Carries one object, usually the hero image, through the page as the visitor scrolls, so the story is told around a single thing they never lose sight of.

| Field | Value |
|---|---|
| Beat intents | `manipulate` (primary), `hold` |
| Rung | 2 (GSAP, ScrollTrigger, Flip) |
| Role | `signature`: can carry a page's single defended idea when that idea is an object (a product, a material, a tool) |
| Cost band | Low: 1.6 KB module + GSAP core, ScrollTrigger and Flip (about 56 KB gzipped together, shared with other parts) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `object` | required | one element | Must be `position: absolute` (use `.to-object`), so resizing it never reflows neighbours |
| `slots` | required | 2 to 6 elements | In order of appearance. More than six turns a journey into a chase |
| `ease` | `sine.inOut` | any GSAP ease | `power2.inOut` reads more decisive; avoid elastic or back eases on a scrubbed journey |
| `hold` | `0.5` | 0.2 to 1 | Pause at each slot, as a fraction of one move |
| `scrub` | `true` | `true` or 0.3 to 1 s | A number adds smoothing; keep it under 1 s or the object lags the reader |
| `mode` | `'size'` | `'size'`, `'scale'` | `'scale'` is transform-only but stretches the image unless every slot shares one aspect ratio |
| `mobile` | `'static'` | `'static'`, `'travel'` | Static shows the object still in every slot |
| CSS `--to-radius`, `--to-fill`, `--to-slot-ratio`, `--to-focus` | see CSS | | From the brand system |

## Cost (measured)

Clean-room example, headless Chrome at 1440 × 900 and 390 × 844, software rendering: 60 fps while scrolling, 0 ms of long tasks, no horizontal overflow. These figures are a floor check only; confirm on a real mid-range phone before sign-off.

**Recorded exception.** In `'size'` mode the object's width and height are animated, which is a layout property. It is allowed here because the object is out of flow (absolutely positioned), so only one isolated box is laid out per frame and no neighbour reflows. Measured cost: zero long tasks.

## Fallbacks

- **Reduced motion:** no journey. The object stays still in its stage and each slot shows a still copy (copies hidden from assistive tech).
- **Small screens (default):** same as reduced motion. Set `mobile: 'travel'` only after testing the journey on a real phone.
- **No JavaScript:** the object shows in its stage; slots stay empty. Give slots a background from the brand system if that matters.

## Composition notes

- The object must be worth following: a product, a material, a place. A generic stock photo makes the journey pointless.
- Pair slots with copy that changes meaning at each stop (what it is, how it is made, where it goes). Each slot should answer a different question.
- Do not combine with another `signature` part on the same page.

## Provenance

- Source: [One Element Scroll, Codrops](https://github.com/codrops/OneElementScroll), MIT, by Codrops.
- Admitted: 22 November 2026, intake run 001.
- Changed: rebuilt as a module with inputs; removed the demo's extra effects (span drift, column parallax, related-demos grid, brightness filter); added reduced-motion and mobile branches, teardown, and an out-of-flow constraint; demo images and fonts removed.
- Clean-room test: restyled as an invented ropemaker (cold grey, condensed caps, original procedural artwork). The journey still reads as the idea, not as the source demo. Passed.
