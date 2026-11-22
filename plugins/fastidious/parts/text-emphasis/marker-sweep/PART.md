# text-emphasis / marker-sweep

**Job.** Sweeps a marker under the facts in a sentence at the moment the reader reaches them, so the numbers the argument rests on are the ones remembered.

| Field | Value |
|---|---|
| Concept | [`text-emphasis`](../CONCEPT.md) |
| Beat intents | `reveal` |
| Rung | 2 (GSAP, ScrollTrigger) |
| Role | `supporting` |
| Cost band | Low: 1.1 KB module + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| markup | `<mark data-emphasis>` | a figure or short phrase | Never more than a few words; marks do not wrap |
| `start` | `'top 72%'` | 60% to 80% | The reading line |
| `duration` | `0.65` | 0.4 to 0.9 s | |
| `ease` | `power3.out` | out-eases only | The marker should arrive decisively and settle |
| `stagger` | `0.18` | 0.1 to 0.3 s | Between marks in one block, in reading order |
| CSS `--ms-fill`, `--ms-ink` | yellow, inherit | brand colours | Check text-on-fill contrast is at least 4.5:1 |
| CSS `--ms-inset-top`, `--ms-inset-bottom`, `--ms-overhang`, `--ms-radius` | see CSS | | A low inset reads as a highlighter; a full inset reads as a label |

## Cost (measured)

Clean-room example, headless Chrome, desktop and mobile: 60 fps, 0 ms of long tasks, no overflow. Transform only.

## Fallbacks

- **Reduced motion and no JavaScript:** marks show at rest, fully filled. Nothing is ever hidden.
- **Screen readers:** text is never split; the sentence is read unchanged. `<mark>` is announced as highlighted in some screen readers, which is the intended meaning.

## Differs from

- `char-rise` (same concept): char-rise animates display lines themselves; marker-sweep only adds emphasis to running text.

## Provenance

- Source: [On-Scroll Text Highlight Animations, Codrops](https://github.com/codrops/OnScrollTextHighlight), effects 6 and 7, MIT.
- Admitted: 22 November 2026, intake run 001.
- Changed: width and height animation replaced with `scaleX`; trigger moved to the reading line; plays once instead of resetting; reading-order stagger per block; no text splitting; reduced-motion and no-JS states show marks at rest.
- Clean-room test: restyled as an invented ironmonger (iron-grey paper, serif body, rust marker). Passed.
