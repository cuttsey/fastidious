# Parts index

One line per part; variants listed under their concept. Read the part's `PART.md` before using it.

| Part | Job | Intents | Rung | Role | Cost | Licence |
|---|---|---|---|---|---|---|
| [`travelling-object`](travelling-object/PART.md) | Carries one object through the page as the visitor scrolls | manipulate, hold | 2 | signature | low | MIT (Codrops) |
| [`inline-image-expand`](inline-image-expand/PART.md) | Opens a window of imagery inside a headline, pushing the last words aside | reveal, manipulate | 2 | supporting | low | MIT (Codrops) |
| **[`text-emphasis`](text-emphasis/CONCEPT.md)** (concept) | Makes the words that matter land as they are read | | | | | |
| ↳ [`marker-sweep`](text-emphasis/marker-sweep/PART.md) | Sweeps a marker under facts in running copy | reveal | 2 | supporting | low | MIT (Codrops) |
| ↳ [`char-rise`](text-emphasis/char-rise/PART.md) | Brings a short display line forward out of depth | reveal | 2 | supporting | low | MIT (Codrops) |
| ↳ [`scramble`](text-emphasis/scramble/PART.md) | Decodes figures and labels into place | reveal | 2 | supporting | low | MIT (Codrops) |
| ↳ [`axis-ramp`](text-emphasis/axis-ramp/PART.md) | Moves a display word along its font's weight and width axes so the type carries the story | reveal, manipulate | 2 | supporting; signature in scrub mode | low | MIT (Fastidious) |
| [`sticky-stack`](sticky-stack/PART.md) | Stacks sections like dealt cards; the old one steps back as the next arrives | hold, depth | 1–2 | supporting | low | MIT (Codrops) |
| [`lagging-columns`](lagging-columns/PART.md) | Outer grid columns trail the centre and settle, giving a catalogue weight | depth | 1 | supporting | very low | MIT (Codrops) |
| [`interruptible-menu`](interruptible-menu/PART.md) | Full-screen menu that reverses instantly from wherever it is when interrupted | reveal | 2 | supporting | low | MIT (Codrops) |
| **[`index-to-detail`](index-to-detail/CONCEPT.md)** (concept) | Takes the visitor from an index into one item and back, without losing their place | | | | | |
| ↳ [`echo-trail`](index-to-detail/echo-trail/PART.md) | A trail of the item's image echoes from grid to detail | manipulate | 2 | supporting | low | MIT (Codrops) |
| ↳ [`push`](index-to-detail/push/PART.md) | The rest of the index is shoved off screen to make room for the chosen item | manipulate | 2 | supporting | low | MIT (Codrops) |
| ↳ [`flip`](index-to-detail/flip/PART.md) | The item's picture glides to the detail and home again | manipulate | 2 | supporting | low | MIT (Fastidious) |
| [`hero-slideshow`](hero-slideshow/PART.md) | Full-bleed objects one at a time; four transitions with distinct characters | hold, manipulate | 2 | signature | low | MIT (Codrops) |
| [`process-curve`](process-curve/PART.md) | A real process curve draws on scroll with a big live readout | manipulate, reveal | 2 | signature | low | MIT (Fastidious) |
| [`grain-light`](grain-light/PART.md) | Film grain and a drifting soft light: depth without 3D | depth, rest | 1 | supporting | very low | MIT (Fastidious) |
| [`live-status`](live-status/PART.md) | One honest line about now: open, closing soon, closed until… | rest | 1 | supporting | very low | MIT (Fastidious) |

| **[`view-change`](view-change/CONCEPT.md)** (concept) | Turns a change of view into a moment and hides the swap | | | | | |
| ↳ [`type-curtain`](view-change/type-curtain/PART.md) | A wall of the brand's words swings across while the view changes | manipulate | 2 | signature | low | MIT (Codrops) |
| ↳ [`pixel-cover`](view-change/pixel-cover/PART.md) | Blocks sweep across in the brand colour while the view changes | manipulate | 2 | supporting | low | MIT (Codrops) |
| [`drifting-words`](drifting-words/PART.md) | The brand's vocabulary drifts across columns as you scroll | depth, rest | 2 | signature | low | MIT (Codrops) |
| [`pixel-resolve`](pixel-resolve/PART.md) | Pictures resolve from coarse blocks to full detail as they arrive | reveal | 1 | supporting | very low | MIT (Codrops) |
| [`image-trail`](image-trail/PART.md) | The pointer paints a trail of the brand's pictures | manipulate | 2 | supporting | low | MIT (Codrops) |
| [`text-repeat`](text-repeat/PART.md) | A big word fans out into a stack of its own copies as it rises | depth, reveal | 2 | supporting | low | MIT (Codrops) |
| [`context-aware-fixed`](context-aware-fixed/PART.md) | A fixed logo or link steps aside while a picture passes under it | reveal | 2 | supporting | very low | MIT (Codrops) |
| [`page-transition`](page-transition/PART.md) | Moves between pages as one place: content rises away, clicked pictures travel into the next page | manipulate, reveal | 1–2 | supporting | very low | MIT (Fastidious) |
| [`endless-loop`](endless-loop/PART.md) | A page with no end: the first panel returns after the last | hold, depth | 2 | signature | low | MIT (Codrops) |


Shared dependency: GSAP 3.15 (core, ScrollTrigger, Flip, SplitText), installed by the host project, never bundled here. GSAP is free under its own [standard no-charge licence](https://gsap.com/standard-license), not MIT; check its terms for your use.
Lenis (MIT) is a further dependency of `endless-loop` only.

Type: every face is chosen from the [`fonts/`](fonts/README.md) registry (Awwwards free fonts collection) and loaded by reference; no font files are kept.
