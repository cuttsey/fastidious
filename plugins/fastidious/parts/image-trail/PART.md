# image-trail

**Job.** Lets the visitor paint with the brand's pictures: moving the pointer (or dragging on a phone) leaves a trail of images that bloom and fade, so a body of work is felt rather than listed.

| Field | Value |
|---|---|
| Beat intents | `manipulate` |
| Rung | 2 (GSAP core) |
| Role | `supporting`; `signature` on a portfolio or studio site whose idea is the volume of its work |
| Cost band | Low: 1.7 KB module + GSAP core (shared); runs only while on screen |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Notes |
|---|---|---|
| markup | `.it-area` with `.it-img` images | Images are decorative repeats (`aria-hidden`); put the real content in the area's text |
| `pool` | `20` | Image elements cycled (sources repeat to fill it) |
| `threshold` | `80` | px of travel per image |
| `lag`, `maxPerFrame` | `0.1`, `4` | |
| `show`, `hide`, `endScale` | `0.4`, `0.4`, `0.2` | |
| CSS `--it-width`, `--it-ratio`, `--it-radius` | | |

## Cost (measured)

60 fps, 0 ms of long tasks, desktop and mobile.

## Fallbacks and access

- **Touch:** dragging draws the trail; vertical page scrolling stays native (`touch-action: pan-y`).
- **Reduced motion:** still images appear and fade where the pointer passes, with no travel or scaling.
- **Keyboard and screen readers:** decorative only; never put information solely in the trail.

## Provenance

- Source: [Motion Trail Animations, Codrops](https://github.com/codrops/MotionTrailAnimations), demo 1 and its trail engine, MIT.
- Admitted: 22 November 2026, intake run 004 (rejected in run 002 as a trend; that reason no longer applies, and the touch concern was wrong: the engine uses pointer events, which cover touch).
- Changed: listens only inside its own area instead of the whole window; pauses off screen; images from the host; demo imagery removed.
- Clean-room test: a swim club's season, original still-life pictures. Passed.
