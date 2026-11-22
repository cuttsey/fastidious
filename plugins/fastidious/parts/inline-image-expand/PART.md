# inline-image-expand

**Job.** Opens a small window of imagery inside a headline as it is read, pushing the last words aside, so the picture and the sentence arrive as one thought.

| Field | Value |
|---|---|
| Beat intents | `reveal`, `manipulate` |
| Rung | 2 (GSAP, ScrollTrigger) |
| Role | `supporting`; `signature` only on an editorial page where image and word are the idea |
| Cost band | Low: 1.3 KB module + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| markup | `data-ie` on the heading; `.ie-window > img` then `.ie-after` | one window per heading | Put the window before the last word or two of a line |
| `start`, `end` | `'top 85%'`, `'top 30%'` | | Scroll range of the opening |
| `scrub` | `0.6` | `true` or 0.3 to 1 s | |
| `ease` | `power2.inOut` | in-out eases | |
| `zoom` | `1.35` | 1.1 to 1.6 | How far the picture starts zoomed in |
| CSS `--ie-width` | `2.4em` | 1.6 to 3.2 em | In em, so it scales with the type |
| CSS `--ie-ratio`, `--ie-radius`, `--ie-gap`, `--ie-focus` | see CSS | | `--ie-radius: 0` gives hard, square windows |

## Constraint

The words after the window slide into place, so they must sit on the same line as the window. If they wrap, the part detects it and only reveals the window, which still works but loses the slide. Write the headline so the window and the last word share a line at every breakpoint you support.

## Cost (measured)

Clean-room example, headless Chrome, desktop and mobile: 60 fps, 0 ms of long tasks, no overflow. Transform and clip-path only; the layout never changes while scrolling.

## Fallbacks

- **Reduced motion and no JavaScript:** the natural layout, which is the open state. Nothing is hidden.
- **Screen readers:** the image is decorative inside a heading, so give it `alt=""` unless it carries information the words do not.

## Provenance

- Source: [On-Scroll Expanding Image Animation within Typography, Codrops](https://github.com/codrops/ImageExpansionTypography), effect 1, MIT.
- Admitted: 22 November 2026, intake run 001.
- Changed: the original animated the window's width with Flip, reflowing the headline on every frame. Rebuilt so space is reserved in the layout and closed with transforms, making the final state the natural layout. Added a wrapped-line guard, tokens and a reduced-motion state. Demo images, fonts and the companion paragraph skew effect removed.
- Clean-room test: restyled as an invented ropemaker (stark white, heavy condensed caps, square windows, original artwork). Passed.
