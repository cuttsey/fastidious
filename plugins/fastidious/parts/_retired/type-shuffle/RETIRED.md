# type-shuffle (retired, run 004)

- Source: [Type Shuffle Animation, Codrops](https://github.com/codrops/TypeShuffleAnimation), MIT.
- Concept: `text-emphasis` (decoding text into place).
- Comparison: `text-emphasis/scramble` does the same job on GSAP's ScrambleTextPlugin, keeps the real words available to screen readers, and runs on the shared ticker. Type Shuffle drives every character with its own timer and rewrites it through `innerHTML`, with no reduced-motion path.
- Verdict: same concept, one clearly better. Retired on engineering, not on resemblance. Its "cascade" style (letters passing along the line like a typewriter) is worth adding to `scramble` as a mode later.
