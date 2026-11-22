# interruptible-menu

**Job.** A full-screen menu that opens with presence but never makes the visitor wait: change your mind halfway and it reverses from exactly where it is, fast.

| Field | Value |
|---|---|
| Beat intents | `reveal` (navigation) |
| Rung | 2 (GSAP core, 3.15 or later for `easeReverse`) |
| Role | `supporting` |
| Cost band | Low: 1.8 KB module + GSAP core (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `toggle`, `menu` | required | | Menu needs an `id`; links or buttons inside |
| `scatter` | `[]` | 0 to about 12 elements | Page elements that fly outwards as the menu opens; optional |
| `scatterDistance` | `600` | 300 to 900 px | |
| `openDuration`, `openEase` | `0.8`, `expo` | 0.5 to 1 s | |
| `clipDelay` | `0.3` | 0 to 0.4 s | Lets the scatter lead the menu |
| `fullCloseEase` | `expo.in` | | Reverse ease when closing a fully open menu |
| `interruptSpeed` | `2.5` | 1.5 to 4 | Time scale for a close that interrupts an opening |
| CSS `--im-bg`, `--im-ink` | | | |

## Cost (measured)

Clean-room example, headless Chrome: 60 fps, 0 ms of long tasks on desktop and mobile, no overflow. Full close 1.2 s; an interrupted close completed in 0.3 s, measured from a close 250 ms into the opening.

## Fallbacks and access

- **Reduced motion:** a 0.25 s fade; no clip or scatter.
- **Keyboard:** `aria-expanded` on the toggle; the menu is `inert` and hidden from assistive tech while closed; focus moves to the first item on open and back to the toggle on close; Escape closes. Tested.
- **No JavaScript:** the menu stays hidden; give the toggle a fallback link to a navigation page, or render the menu inline without the part.

## Provenance

- Source: [Ease Reverse Clip Menu, Codrops](https://github.com/codrops/EaseReverseClipMenu), MIT.
- Admitted: 22 November 2026, intake run 002.
- Changed: rebuilt as a module around any toggle and menu; demo controls, background video and cover images removed; scatter made optional; focus management added; reduced-motion fade added.
- Clean-room test: restyled as an invented ironmonger (rust menu over iron grey, no game UI or video). Passed.
