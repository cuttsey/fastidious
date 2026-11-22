# text-repeat

**Job.** A big word fans out into a stack of its own copies as it travels up the screen, as if it echoes or is being printed again and again; the word itself stays put in the middle.

| Field | Value |
|---|---|
| Beat intents | `depth`, `reveal` |
| Rung | 2 (GSAP, ScrollTrigger) |
| Role | `supporting`; `signature` on a type-led page where repetition means something (batches, editions, layers, echoes) |
| Cost band | Low: 3.1 KB module (unminified) + GSAP core and ScrollTrigger (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Inputs

`mountTextRepeat(element, options)` returns `{ destroy }`. Put it on a block element holding one display word or short line.

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `copies` | `9` | 5 to 11, odd | Layers including the word |
| `spread` | `12` | 8 to 45 % | Step between layers, as a share of the word's height |
| `stagger` | `0.1` | 0 to 0.15 | Outer layers start later |
| `drift` | `0` | 0 to 0.2 | Sideways slant as a share of `spread` |
| `fade` | `false` | | Outer layers fade as they spread |
| `ease` | `power1` | | |
| `start`, `end`, `scrub` | `top bottom`, `bottom top`, `true` | | ScrollTrigger range |

CSS tokens: `--tr-copy` (colour of the copies), `--tr-bg` (a backing behind each layer, usually the section colour, so layers overlap cleanly), `--tr-stroke` with the `tr--outline` class for outlined copies.

## Cost (measured)

Clean-room example (three instances, three settings), headless Chrome with software rendering: 59.8 fps desktop, 60 fps mobile and reduced motion; no long tasks, no errors. An early run showed horizontal overflow from the sideways drift; the part now clips drift inside its own wrapper and passes. Transform and opacity only.

## Fallbacks

- **Reduced motion:** no copies are made; the word shows once.
- **Screen readers:** copies are `aria-hidden`, so the word is read once.
- **No JavaScript:** the word shows once.

## Differs from

- `drifting-words`: a field of different words drifting; `text-repeat` multiplies one word.
- `text-emphasis/axis-ramp`: changes the word's shape; `text-repeat` multiplies it.

## Provenance

- Source: [Text Repetition Scroll Effect, Codrops](https://github.com/codrops/TextRepetitionEffect), demos 1 and 4, MIT.
- Admitted: 22 November 2026, intake run 006.
- Changed: copies hidden from screen readers; the host's margin and padding untouched (room is made inside the part's own wrapper); one ScrollTrigger scrub replaces an observer plus ticker; all settings exposed; drift clipped inside the part; reduced-motion and teardown paths added.
- Clean-room test: an invented mushroom farm, Spore Hall (charcoal, cream, rust; Norwester, Bitter, Geist Mono). Passed.
