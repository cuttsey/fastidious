# text-emphasis / scramble

**Job.** Decodes a word or figure into place as it is reached, as if it were coming off an instrument: for brands with a technical, data or coded voice.

| Field | Value |
|---|---|
| Concept | [`text-emphasis`](../CONCEPT.md) |
| Beat intents | `reveal` |
| Rung | 2 (GSAP, ScrollTrigger, ScrambleTextPlugin) |
| Role | `supporting` |
| Cost band | Low: 1.2 KB module + GSAP core, ScrollTrigger and ScrambleTextPlugin (4 KB) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP and its plugins under GSAP's own no-charge licence, not bundled |

## Inputs

| Input | Default | Notes |
|---|---|---|
| markup | `data-scramble` on short text | Figures, labels, single lines |
| `chars` | `upperCase` | Or any string: use the characters the brand actually uses (`0123456789°:` for a conditions board) |
| `duration` | `1` | Per element; `data-scramble-duration` overrides |
| `revealDelay`, `speed` | `0.2`, `0.6` | |
| `start`, `once` | `top 80%`, `true` | |

## Cost (measured)

60 fps, 0 ms of long tasks, desktop and mobile.

## Fallbacks and access

- **Screen readers and search:** the real words sit in a visually hidden copy; the scramble plays on an `aria-hidden` copy, so nothing ever reads out garbage.
- **Reduced motion and no JavaScript:** the words show directly.

## Provenance

- Source: the scramble in [Scroll Text Motion, Codrops](https://github.com/codrops/ScrollTextMotion), MIT. The demo credits satto.studio as its inspiration.
- Admitted: 22 November 2026, intake run 004.
- Best in class: Codrops' TypeShuffleAnimation does the same job with a hand-rolled loop that rewrites every character with `innerHTML` on its own timer. This part replaces it; see `_retired/type-shuffle/`.
- Clean-room test: a swim club's conditions board with the brand's own character set. Passed.
