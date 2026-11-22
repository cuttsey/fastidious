# endless-loop

**Job.** A page with no end: scroll past the last panel and the first one arrives again, seamlessly, so an index of work or objects reads as a cycle.

| Field | Value |
|---|---|
| Beat intents | `hold`, `depth` |
| Rung | 2 (GSAP, ScrollTrigger, Lenis) |
| Role | `signature` on a page that is itself an index; never on a page with content after the loop |
| Cost band | Low: 1.4 KB module + Lenis (5.4 KB, MIT) + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Codrops), see `LICENSE`; Lenis MIT; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Notes |
|---|---|---|
| `container` | required | Holds the panels in order |
| `clones` | `1` | Panels repeated at the end to hide the seam |
| `seamScale` | `true` | The first panel shrinks away as you leave it and grows as it returns |
| `lerp` | `0.1` | Lenis smoothing |

## Constraint

An endless page has no footer. Always give the page a fixed way out (navigation, contact), as the example does.

## Cost (measured)

60 fps, 0 ms of long tasks, desktop and mobile. Wrap tested: scrolling down past the last panel returns to the start.

## Fallbacks and access

- **Reduced motion:** an ordinary finite page; no loop, no Lenis.
- **Keyboard:** clones are inert and hidden from assistive tech; if focus ever reaches the seam it is sent back to the start.
- **No JavaScript:** a finite page of panels.

## Provenance

- Source: [Infinite Loop Scrolling, Codrops](https://github.com/codrops/LoopScrolling), MIT. The demo credits Bureau DAM's site as its inspiration; recorded as a fact.
- Admitted: 22 November 2026, intake run 004 (rejected in run 001 as a recreation; that reason no longer applies).
- Changed: rebuilt around any panels; clones made inert and hidden; reduced-motion opt-out; Lenis updated to 1.3; demo imagery and fonts removed.
- Clean-room test: an ironmonger's endless index of objects. Passed.
