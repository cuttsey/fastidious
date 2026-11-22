# text-emphasis / char-rise

**Job.** Brings a short display line forward out of depth, letter by letter, so a section opener or closing line arrives as an event.

| Field | Value |
|---|---|
| Concept | [`text-emphasis`](../CONCEPT.md) |
| Beat intents | `reveal` |
| Rung | 2 (GSAP, ScrollTrigger, SplitText) |
| Role | `supporting`; can be `signature` only on a type-led page whose idea is the words themselves |
| Cost band | Low: 1.1 KB module + GSAP core, ScrollTrigger and SplitText (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

| Input | Default | Safe range | Notes |
|---|---|---|---|
| markup | `data-char-rise` on a heading | one line, under about 40 characters | Longer lines turn the stagger into a wait |
| `depth` | `260` | 120 to 400 px | |
| `tilt` | `-50` | -20 to -70 deg | |
| `perspective` | `520` | 400 to 900 px | |
| `duration` | `0.9` | 0.6 to 1.2 s | |
| `stagger` | `0.035` | 0.02 to 0.05 s | Keep total stagger under about 1 s |
| `ease` | `power3.out` | out-eases | |
| `start` | `'top 78%'` | 65% to 85% | |

## Cost (measured)

Clean-room example, headless Chrome, desktop and mobile: 60 fps, no overflow. Long tasks: 0 ms on desktop; one 50 ms task on mobile when the text is split at load. Transform and opacity only.

## Fallbacks

- **Reduced motion:** a plain fade of the whole line; no depth or tilt.
- **Screen readers:** SplitText keeps an accessible label on the line, so it is read as one phrase, not letter by letter.
- **No JavaScript:** the line shows normally.

## Differs from

- `marker-sweep` (same concept): marker-sweep emphasises facts inside running text; char-rise animates a whole display line.

## Provenance

- Source: [On-Scroll Text Highlight Animations, Codrops](https://github.com/codrops/OnScrollTextHighlight), effect 1, MIT.
- Admitted: 22 November 2026, intake run 001.
- Changed: Splitting.js replaced with GSAP SplitText (accessible label kept); trigger at the reading line; plays once instead of resetting; depth, tilt and timing exposed as inputs; reduced-motion fade; split reverted on teardown.
- Clean-room test: restyled as an invented swim club (cold sea bands, rounded heavy display). Passed.
