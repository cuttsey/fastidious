# text-emphasis / axis-ramp

**Job.** Moves a display word along a variable font's weight and width axes, so the type itself carries the story: something filling, fading, rising or running out.

| Field | Value |
|---|---|
| Concept | [`text-emphasis`](../CONCEPT.md) |
| Beat intents | `reveal` (intro, enter), `manipulate` (scrub) |
| Rung | 2 (GSAP, ScrollTrigger, SplitText) |
| Role | `supporting` in intro or enter mode; `signature` in scrub mode when the word is the page's idea |
| Cost band | Low: 8.7 KB module (unminified) + GSAP core, ScrollTrigger and SplitText (shared). Needs a variable font, which the host already loads for its display type |
| Licence | MIT (Fastidious, original), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## When the meaning is in the axis

Use it only when heavier, lighter, wider or narrower *means* something for this product: a balance growing, a friendship thinning, dough rising, a signal fading, a deadline getting closer. If the change would only be decoration, use `char-rise` instead.

## Modes

| Mode | What the visitor sees | Plays |
|---|---|---|
| `intro` | Letters settle from a start state into a ramp across the word, first to last, once the font has loaded | Once, on load |
| `enter` | The same, when the word reaches the reading line | Once, never resets |
| `scrub` | The whole word travels between two states (weight, width, opacity) as the reader scrolls through a section | Bound to scroll, both ways |

## Inputs

`mountAxisRamp(target, options)` returns `{ ready, destroy }`. `target` is an element or a selector.

| Input | Default | Safe range | Notes |
|---|---|---|---|
| `mode` | `'enter'` | `intro`, `enter`, `scrub` | |
| `startState` | `{ wght: 900, wdth: 100 }` | within the font's axes | Where every letter begins (intro, enter) |
| `ramp` | `{ wght: [900, 100], wdth: null }` | within the font's axes | First-letter and last-letter targets; letters between are interpolated. A single number sets every letter the same. `null` keeps the start value |
| `duration` | `1.4` | 0.8 to 2 s | Weight changes read slowly; under 0.8 s they look like a flicker |
| `stagger` | `0.07` | 0.04 to 0.1 s | |
| `ease` | `'expo.out'` | out-eases | |
| `delay` | `0` | 0 to 1 s | Intro only: time it after the hero's other moves |
| `start` | `'top 85%'` | 65% to 90% | Enter only |
| `from`, `to` | `{wght 900, wdth 125, opacity 1}` to `{wght 120, wdth 70, opacity 0.4}` | within the font's axes; opacity at least 0.35 | Scrub only |
| `trigger`, `scrubStart`, `scrubEnd` | the word, `'top top'`, `'bottom bottom'` | | Scrub only: usually a tall section with the word pinned or sticky inside it |
| `scrub` | `0.4` | `true` to 1 | Smoothing in seconds |
| `maxChars` | `14` | up to about 16 | Longer text is shown at its final ramp with no motion, and the console says why |
| `lockBox` | `true` | | Leave on: it is what keeps the neighbours still |
| `fontTimeout` | `3000` | 1500 to 4000 ms | If the font has not loaded by then, the word is shown at its end state with no motion |
| `reducedSteps` | `3` | 2 to 4 | Scrub under reduced motion: the word jumps between this many states instead of moving continuously |

**Markup.** Put it on a heading or a paragraph (an element with a role), or on a `<span>` inside running text. For intro and enter, SplitText puts the word's text on the element as its accessible name and hides the letters from screen readers. Scrub does not split the word, so no label is needed; do not add `aria-label` to a `<p>`.

**Font.** The host loads a variable font whose `@font-face` declares its ranges, for example `font-weight: 100 900; font-stretch: 62% 125%`. Width moves need a width axis; with a weight-only font, leave `wdth` at 100.

## How it stays cheap

Changing a font axis reflows the text on every frame, which is why the library normally animates only transform and opacity (see `../../README.md`). This part keeps the reflow contained:

- **Locked box.** Before any motion it measures the word at every state it will pass through and fixes the box at the largest. A block word gets a fixed height and layout containment; an inline word gets a fixed width as an inline block (no layout containment, which would lose its baseline). Words beside it do not move: in the example, the word after `doubles` stayed on the same pixel while the weight went from 300 to 900.
- **Short text only.** `maxChars` keeps it to display words.
- **Font gate.** Nothing moves until the variable font has loaded, so the fallback font never plays the animation.
- **Rebuild on resize.** The lock is measured again when the container's width changes. A word that has already played is not replayed.

## Cost (measured)

Clean-room example (four instances: an intro, a scrub across a 320svh section, an inline enter and a block enter), headless Chrome with software rendering, so these are floor checks, not device figures:

| Run | fps | Long tasks | Overflow | Errors |
|---|---|---|---|---|
| Desktop 1440 × 900 | 59.9 | 0 ms (an earlier run showed one 63 ms task at load: split, measure, ScrollTrigger set-up) | none | none |
| Mobile 390 × 844 | 60.0 | 0 ms | none | none |
| Reduced motion | 59.9 | 0 ms | none | none |

Also checked: a missing font file (the end state is shown at once, no errors), a resize after the intro (no replay, the lock is measured again) and teardown.

## Fallbacks

- **Reduced motion:** intro and enter show the final ramp at once. Scrub jumps between `reducedSteps` states, so the meaning survives without continuous movement.
- **Font missing or slow:** the end state, without motion.
- **No JavaScript:** the word shows at the host's own weight.
- **Screen readers:** the word is read once as a word, never letter by letter.

## Differs from

- `char-rise` (same concept): moves letters in space. axis-ramp keeps them in place and changes their shape.
- `scramble` (same concept): changes which characters show. axis-ramp keeps the characters and changes their weight.

## Provenance

- Seen at: the Overdue example page on Muzli (reviewed 22 November 2026), where a friend's name thins and condenses as the days since the last call go up. Built from a written description only; no code taken.
- Built: 22 November 2026, intake run 005, as an original.
- Clean-room test: an invented sourdough-starter app, Leaven (flour blue, rye and yeast yellow; Archivo and Geist Mono, referenced through the font registry (`../../fonts/`)). The direction is reversed from the reference: the word fills as the starter rises. Passed.
