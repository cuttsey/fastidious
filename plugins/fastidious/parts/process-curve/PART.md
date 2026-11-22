# process-curve

**Job.** Tells the story of a process (a roast, a tide, a rope being closed) as one curve that draws as the reader scrolls, with a large live readout and named moments, so a real number becomes the drama.

| Field | Value |
|---|---|
| Beat intents | `manipulate`, `reveal` |
| Rung | 2 (GSAP ScrollTrigger; SVG) |
| Role | `signature` when the process is the brand's idea; otherwise `supporting` |
| Cost band | Low: 1.8 KB module + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Fastidious, original), see `LICENSE` |

## Honest data only

The curve is drawn straight between the business's own data points; the part never smooths, extrapolates or invents. It refuses to run with fewer than two points. Examples that use sample data must say so on the page.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `data` | required | `[[x, y], ...]` real units, x increasing |
| `xLabel`, `yLabel`, `title` | | Used for the accessible name and table |
| `formatX`, `formatY` | `String` | Units belong here (`12.8 t/m`, `4.6 m`) |
| `marks` | `[]` | `[{ x, label }]` named moments that light up as reached |
| `start`, `end`, `scrub` | `top 70%`, `bottom 40%`, `0.4` | |
| CSS `--pc-accent`, `--pc-ink`, `--pc-ghost`, `--pc-readout-font`, `--pc-label-font` | | |

## Cost (measured)

60 fps, 0 ms long tasks, desktop and mobile.

## Fallbacks and access

- **Reduced motion:** the whole curve is drawn and the readout shows the final value.
- **Screen readers:** the SVG has an accessible name, and a visually hidden table holds every data point.

## Provenance

Original Fastidious part, built 22 November 2026 (intake run 003) from `WANTED.md`, prompted by the roast-curve section on Profitize Build's demo pages.
