# text-emphasis (concept)

**Shared job.** Makes the words that matter most land as the visitor reads, without slowing the reading down.

This concept holds four variants. Each earns its place because there is a real brief where it is the right choice over its sibling.

| Variant | Use it when | Do not use it when | Register | Rung | Cost band |
|---|---|---|---|---|---|
| [`marker-sweep`](marker-sweep/PART.md) | Body copy carries hard facts (figures, durations, places) that the page's argument rests on. Pairs with the premium bar's "copy built on facts" rule. | The emphasised phrase is longer than a few words, or would wrap. | Calm to editorial | 2 | Low |
| [`scramble`](scramble/PART.md) | Figures, labels or short lines in a technical, data or coded voice: the words decode into place. | The text is long, or the brand is warm and material. | Technical | 2 | Low |
| [`char-rise`](char-rise/PART.md) | A short display line is itself the moment: a section opener, a chapter title, a closing line. | It would be applied to body copy, or to more than one line per screen. | Expressive | 2 | Low |
| [`axis-ramp`](axis-ramp/PART.md) | Heavier, lighter, wider or narrower means something for the product (filling, fading, rising), and the word can carry that change; also scroll-bound, as a signature. | The font has no variable axes, the text is longer than a display word, or the change would only be decoration. | Expressive to editorial | 2 | Low |

Every variant except `axis-ramp` in scrub mode plays once, at the reading line, and never reset when the reader scrolls back. Do not use both on the same line.

## Considered and not admitted under this concept

- **Blur reveal** (from Codrops' On-Scroll Blur Reveal). Same job at paragraph scale, but animates `filter: blur`, which repaints every frame: 1,130 ms of long tasks and 46.8 fps in the headless check, against 0 ms and 60 fps for both admitted variants. It also hides copy until the reader reaches it, which slows reading. Retired at gate 5; see `../INTAKE-LOG.md`.
