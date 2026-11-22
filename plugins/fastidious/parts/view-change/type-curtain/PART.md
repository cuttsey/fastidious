# view-change / type-curtain

**Job.** Turns a change of view into a moment: a wall of the brand's own words swings across the screen, the view changes behind it, and the new one emerges.

| Field | Value |
|---|---|
| Concept | [`view-change`](../CONCEPT.md) |
| Beat intents | `manipulate` (between views or chapters) |
| Rung | 2 (GSAP core) |
| Role | `signature` for type-led brands; use for a few big moments, never for every link |
| Cost band | Low: 1.6 KB module + GSAP core (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Use

```js
const curtain = mountTypeCurtain({ words: ['forged', 'filed', 'blacked', 'hung'] });
await curtain.play(() => { /* swap the view here; may be async */ });
```

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `words` | required | 3 to 8 words | The brand's vocabulary, never filler |
| `lines`, `repeat` | `11`, `3` | | Rows, and words per row |
| `speed` | `1.4` | 1.2 to 1.8 | Time scale; 1.4 is about 2 s in total. The source ran at 1 (2.5 s) |
| `rotate`, `scale` | `-90`, `2.7` | | |
| `swapAt` | `0.5` | 0.45 to 0.6 | When the view underneath changes |
| `ground` | `true` | | A solid layer under the type, so the swap is never glimpsed |
| CSS `--tc-font`, `--tc-weight`, `--tc-colour`, `--tc-size`, `--tc-ground` | | | `--tc-ground` should match the page background |

## Cost (measured)

Clean-room example, headless Chrome: 60 fps, 0 ms of long tasks on desktop and mobile, no overflow.

## Fallbacks and access

- **Reduced motion:** the words fade in flat, the view swaps behind them, and they fade out; no rotation or travel.
- **Screen readers:** the wall is `aria-hidden`; move focus into the new view in the swap callback (the example does).
- **No JavaScript:** views must still be reachable as ordinary pages or sections.

## Provenance

- Source: [Kinetic Typography Page Transition, Codrops](https://github.com/codrops/KineticTypePageTransition), MIT.
- Admitted: 22 November 2026, intake run 003.
- Changed: rebuilt as a promise-based transition around any swap; builds its wall from a word list; about 40% faster; adds a ground layer so the swap is fully hidden (the source let the old view show through the gaps); reduced-motion path; removed the demo's article system and fonts.
- Clean-room test: restyled as an invented ironmonger (rust condensed caps on iron grey, the brand's own verbs). Passed.
