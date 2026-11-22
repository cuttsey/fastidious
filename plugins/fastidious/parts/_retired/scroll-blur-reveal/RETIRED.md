# scroll-blur-reveal (retired, run 001)

- Source: [On-Scroll Blur Reveal, Codrops](https://github.com/codrops/ScrollBlurTypography), MIT.
- Concept: `text-emphasis` (same shared job at paragraph scale).
- Comparison, both restyled and run headless in Chrome: blur reveal 46.8 fps and 1,130 ms of long tasks (it animates `filter: blur`, repainting every frame); `marker-sweep` and `char-rise` 60 fps and 0 ms.
- Also: it hides body copy until the reader reaches it, which slows reading, the opposite of the concept's job.
- Verdict: same concept, one clearly better. Retired; not normalised. Revisit only if a brief needs paced paragraph reveals and a transform-only version exists.
