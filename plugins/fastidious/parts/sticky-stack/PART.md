# sticky-stack

**Job.** Stacks sections like cards being dealt: each new section slides over the last, which steps back, so a sequence (a timetable, a process, a range) reads as one deck the visitor works through.

| Field | Value |
|---|---|
| Beat intents | `hold`, `depth` |
| Rung | 1 for the stacking (pure CSS `position: sticky`), 2 for the exit motion (GSAP, ScrollTrigger) |
| Role | `supporting` |
| Cost band | Low: 1.2 KB module + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| markup | `.ss-section` siblings | 3 to 7 sections | The last section never animates out |
| `exit` | `'drift'` | `'drift'`, `'recede'` | Drift: the old card darkens and slides up a little. Recede: it shrinks back and fades, like a card put down. Pick one per page |
| `drift` | `15` | 8 to 25 % | For `'drift'` |
| `scale` | `0.6` | 0.5 to 0.85 | For `'recede'` |
| `dim` | `0.45` | 0 to 0.7 | Overlay opacity on the outgoing card; 0 turns it off |
| `tilt` | `0` | -20 to 20 deg | Optional secondary tilt for an element matching `mediaSelector` |
| CSS `--ss-height`, `--ss-dim-colour` | `100svh`, black | | |

## Cost (measured)

Clean-room example, headless Chrome: 60 fps on desktop and mobile; one 71 ms task at load on desktop (ScrollTrigger set-up), 0 ms while scrolling; no overflow. Transform and opacity only.

## Fallbacks

- **Reduced motion and no JavaScript:** the cards still stack (CSS only); nothing scales, drifts or dims.
- **Keyboard and screen readers:** sections stay in document order; sticky positioning does not change reading order.

## Provenance

- Source: [Sticky Sections, Codrops](https://github.com/codrops/StickySections), demos 1 and 7, MIT.
- Admitted: 22 November 2026, intake run 002. Of the 15 demos, the other 13 are close variations on these two exits and were not kept separately.
- Changed: brightness and contrast filter replaced with an overlay's opacity (no repaint per frame); Lenis no longer required; exit style and strengths exposed as inputs; demo 3D renders and fonts removed.
- Clean-room test: restyled as an invented swim club's timetable (flat colour fields, no 3D objects). Passed.
