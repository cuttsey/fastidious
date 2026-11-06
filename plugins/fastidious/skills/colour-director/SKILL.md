---
name: colour-director
description: Sources and builds a colour palette from the subject's own world and from historic colour combinations, then tests it for contrast, value range, chroma and the palettes every template uses. Extracts colours from photographs and frames, searches Sanzo Wada's Dictionary of Color Combinations for proven sets, builds OKLCH tonal ramps for both themes, and writes the colour system. Use whenever a project needs a palette chosen or judged, before brand-system-architect locks the colour tokens.
---

# Colour director

Generated palettes fail in a few predictable ways. They borrow the category's average (warm cream with terracotta, near-black with one acid green, a purple-to-blue gradient). They keep every colour at one temperature and one middling chroma, so the page looks muddy. Or they pick colours one at a time, so nothing has a job and nothing has a partner.

Painters and printers solved this long ago by working from combinations, not single colours, and from the light and materials in front of them. Sanzo Wada's *A Dictionary of Color Combinations* (first published in the 1930s) records 348 of them, built from traditional pigments; Josef Albers (1963) showed that a colour's effect depends on what sits beside it. This skill works the same way: it takes colours from the subject's own world, finds proven combinations that contain them, and tests the result as a set.

## Where it sits in the pipeline

- **Runs:** in phase 4, after `SIGN-SYSTEM.md` (its Colour channel), alongside `world-bible` (whose frames are a source) and `type-director` (whose specimens need the colours), and before brand-system-architect locks the colour tokens.
- **Reads:** `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md` (voice), `WORLD-BIBLE.md` and its frames, the person's `REFERENCES.md` and images, and any existing brand colours.
- **Writes:** `colour/` (sources, tokens, sheets) and the Colour section of `BRAND-SYSTEM.md`.
- **Hands to:** brand-system-architect (tokens), `world-bible` (the palette its scenes must hold), `type-director` (grounds and text colours for specimens), and the build.

## Working rules

1. **Source before you pick.** Every colour comes from somewhere you can name: a photograph or frame of the subject's world, a historic combination, a pigment, a reference in the person's library, or an existing brand colour. Record the source beside the hex.
2. **Combinations, not colours.** Choose sets that already work together, then assign roles. Never assemble a palette one favourite at a time.
3. **Give every colour a job.** Ground, surface, text, accent, signal. One accent carries the action; signals (success, warning, error) are separate from it.
4. **Value first.** A palette that fails in greyscale fails in colour. Keep a wide range of lightness so hierarchy survives without hue.
5. **One loud colour.** At most one, occasionally two, high-chroma colours; the rest support.
6. **Muddy needs a counterweight.** One temperature works when values are wide and colours are clean (as `detail-craft/references/taste-lessons.md` advises, with a dark tinted towards it). When the sources are low in chroma and all one hue family, add one cool to a warm palette, or one warm to a cool one, or it turns muddy.
7. **Variants, then lock.** Three palettes that differ in idea (for example: the world's own light, a historic combination, a cooler counterpoint). The person chooses; record it with `option-ledger`.
8. **Write plainly.** British English, sentence case headings.

## Stage 1: Gather sources

- **The subject's world:** `python3 scripts/palette.py extract <photos or frames> --k 8` returns the colours of the images with their share, in OKLCH. Use the person's photographs, public-domain artworks from museum open-access collections, the world bible's anchor frames, and site photography. Note what the extraction says about the world: muddy, one temperature, or crisp.
- **Historic combinations:** `python3 scripts/palette.py wada --near "<anchor hexes>" --size 3 --top 6` finds the combinations in Wada's dictionary that contain colours closest to your anchors. The data is Matt DesLauriers's MIT-licensed dataset of the book's 159 colours and 348 combinations.
- **The person's references:** colours they admire in `REFERENCES.md`, each with what it borrows.
- **The category audit:** what competitors use, so the palette can avoid it.

## Stage 2: Build three palettes

For each idea, choose a combination, then assign roles and build ramps:

- `python3 scripts/palette.py scale "<hex>" --steps 11` makes an OKLCH ramp on the colour's hue, from near-white to near-black, clipped to the sRGB gamut. Take grounds, surfaces, borders and text from the ramps so tints stay related.
- Make the dark theme from the same ramps, not by inverting: lower the chroma of large dark grounds, raise the accent's lightness until it passes on the dark ground, and keep the neutrals' hue bias.
- Write `colour/tokens.json`: the colours, and the text pairs and large-text pairs the design will use.

## Stage 3: Check

```
python3 scripts/palette.py check colour/tokens.json
python3 scripts/palette.py sheet colour/tokens.json --out colour/sheet.html
```

The check reports WCAG contrast for every pair (4.5:1 text, 3:1 large text), the value range, the number of high-chroma colours, and the palettes every template uses: cream with terracotta, near-black with an acid pop, purple-to-blue, teal and orange, pure greys, and one muddy temperature. It exits with a failure for a contrast failure or a cliché. The sheet shows the swatches and every text pair. Then check by eye on the real work: on the specimens, the frames and the page.

## Stage 4: The colour system

Write the Colour section of `BRAND-SYSTEM.md`: every token with its hex, OKLCH values, source, role and the pairs it may be used in; the light and dark values; the proportions (roughly how much of the page each colour covers); and what is never used. Hand the palette to `world-bible` so the imagery holds it.

## The tests

- **Greyscale test:** desaturate the page; the hierarchy still reads.
- **Swap test:** the palette could not move unchanged to a competitor's site.
- **Source test:** every colour names where it came from.
- **Temperature test:** a single-temperature palette is clean and wide in value; a muddy one has gained a counterweight.
- **Contrast test:** every pair passes, in both themes, on the real backdrops (run `legibility-check.js` over images and film).

## Anti-patterns

- Colours picked one at a time from memory.
- The template palettes the check names.
- Several loud colours competing.
- A dark theme made by inverting the light one.
- Neutrals that are pure grey.
- An accent used for decoration as well as action.

## Files

- `scripts/palette.py`: extract, wada, scale, check and sheet (standard library; ffmpeg for extract).
- `references/wada-colours.json` and `wada-colours.LICENSE.md`: the Wada dataset (MIT, Matt DesLauriers, after Dain Blodorn Kim).

## References

- Albers, J. (1963) *Interaction of Color*. New Haven: Yale University Press.
- DesLauriers, M. (2020) [*dictionary-of-colour-combinations*](https://github.com/mattdesl/dictionary-of-colour-combinations). GitHub, MIT licence.
- Ottosson, B. (2020) [*A perceptual color space for image processing*](https://bottosson.github.io/posts/oklab/).
- Wada, S. (2010) *A Dictionary of Color Combinations*. Tokyo: Seigensha. First published in the 1930s.
- W3C (2023) *Web Content Accessibility Guidelines (WCAG) 2.2*.
