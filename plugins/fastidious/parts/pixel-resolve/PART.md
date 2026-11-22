# pixel-resolve

**Job.** Pictures arrive as the visitor reaches them, resolving from coarse blocks to full detail in a few quick steps, like a print developing.

| Field | Value |
|---|---|
| Beat intents | `reveal` |
| Rung | 1 (canvas, no dependencies) |
| Role | `supporting` |
| Cost band | Very low: 1.5 KB module; the canvas exists only while an image resolves |
| Licence | MIT (Codrops), see `LICENSE` |

## Inputs

| Input | Default | Notes |
|---|---|---|
| markup | `<img data-pixel-resolve>` inside a positioned `.pr-box` | A real image: alt text, srcset and lazy loading are kept |
| `steps` | `[1, 2, 4, 9, 100]` | Percent of full resolution at each step |
| `first`, `each` | `300`, `80` ms | |
| `threshold` | `0.2` | Share of the image visible before it starts |

## Cost (measured)

60 fps, 0 ms long tasks, desktop and mobile. One shared IntersectionObserver for all images.

## Fallbacks and access

- **Reduced motion:** images show normally.
- **No JavaScript:** ordinary images.
- **Screen readers:** the `<img>` and its alt text are untouched; the canvas is `aria-hidden`.

## Provenance

- Source: [On-Scroll Pixelated Image Loading, Codrops](https://github.com/codrops/ImagePixelLoading), MIT. The demo credits a designer's site as its inspiration; recorded as a fact.
- Admitted: 22 November 2026, intake run 004 (rejected in run 001 as a recreation; that reason no longer applies).
- Changed: works on real `<img>` elements with object-fit cropping matched exactly; canvas removed when done; shared observer instead of a ScrollTrigger per image; reduced-motion path; demo imagery removed.
- Clean-room test: a chandlery catalogue with original still-life artwork. Passed.
