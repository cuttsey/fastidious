---
name: type-director
description: Chooses and sets the typography of a site, film or brand: finds typefaces whose history matches the work's meaning, checks them live against Google Fonts, renders specimens of three pairings with the project's real copy, and writes the type system (faces, scale, measure, leading, tracking, figures, loading). Use whenever a project needs typefaces chosen or its typography judged, before brand-system-architect locks the type tokens.
---

# Type director

Typography is the first thing a visitor reads and the last thing most generated work gets right. Left alone, a model reaches for the same few families every time (Inter, Space Grotesk, Playfair Display, Fraunces, Instrument Serif), sets them at default sizes and calls it a brand. The page reads as made by no one in particular.

This skill chooses type the way a type director does: from meaning first, then by looking. It reads the sign system, finds the genres whose history fits, shortlists real faces from a curated catalogue checked against live Google Fonts data, sets them side by side with the project's own words, and only then decides. It writes the decision into the brand system with every setting a builder needs.

## Where it sits in the pipeline

- **Runs:** in phase 4, after `SIGN-SYSTEM.md` and the voice in `BRAND-SYSTEM.md`, and before brand-system-architect locks the type tokens. Run it again whenever the work's register changes.
- **Reads:** `SIGN-SYSTEM.md` (period, material, register, Typography channel), `BRAND-SYSTEM.md` (voice), `COPY-DECK.md` (the real lines), `WORLD-BIBLE.md` if there is one, `REFERENCES.md`, and the colours from `colour-director` when they exist.
- **Writes:** `type/` (specimens) and the Typography section of `BRAND-SYSTEM.md`.
- **Hands to:** brand-system-architect (tokens), the build (faces, loading, settings), `copy-director` (display line lengths at the chosen sizes) and `detail-craft` (the one display-type event).

## Working rules

1. **Meaning before looking.** Name the genre the sign system calls for, and why, before opening any catalogue. `references/typography.md` maps period, material and register to genres.
2. **Look things up; never type a name from memory alone.** Confirm every candidate with `scripts/type_lookup.py --family "<name>" --live`: that it exists where the build will load it, with the weights, styles, axes and language subsets the work needs.
3. **Judge set, not named.** Decide only from a rendered specimen with the project's real copy, at desktop and phone sizes, on the project's real colours.
4. **Distinction counts.** Faces marked overuse 3 in `references/typefaces.json` are the defaults of templates and AI-built pages. Use one only when its meaning is plainly right, and say why in `DESIGN-RATIONALE.md`.
5. **Variants, then lock.** Three pairings that differ in genre, not three variants of one. The person chooses; record it with `option-ledger`.
6. **Licences and hosts.** Google Fonts and Fontshare faces are free to use; commercial faces need a licence the client buys. Artifacts load fonts only from Google Fonts or from inlined files.
7. **Write plainly.** British English, sentence case headings.

## Stage 1: The type brief

From the sign system and voice, write five lines in `type/BRIEF.md`:

- **Genre and why:** for example, "seventeenth-century English old style, because the subject is a slow, handmade English craft".
- **Texture:** even and quiet, or irregular and handmade; light or dark on the page.
- **Range needed:** display, text, labels, figures; italics; small caps; languages.
- **Where it is set:** sizes from the smallest label to the largest statement, and the grounds it sits on.
- **What to avoid:** genres and faces that would say the wrong thing, plus the template defaults.

## Stage 2: Look up candidates

```
python3 scripts/type_lookup.py --genre "<genre words>" --voice "<voice words>" --max-overuse 1
python3 scripts/type_lookup.py --family "<candidate>" --live
python3 scripts/type_lookup.py --overused
python3 scripts/type_lookup.py --commercial
```

The catalogue holds about eighty annotated faces on Google Fonts and Fontshare, with their genre, lineage, voice, features, pairings, cautions and an overuse rating. It is a starting point, not a boundary: search Google Fonts and the person's own references beyond it, then add good finds to the catalogue. For a client with a budget, propose a commercial face from `--commercial` alongside a free equivalent.

Score each candidate with the rubric in `references/typography.md`, and shortlist three pairings that differ in genre.

## Stage 3: Specimens

```
python3 scripts/specimen.py --pair "Display|Text|Utility" --pair "..." --pair "..." \
    --copy COPY-DECK.md --bg "<ground>" --fg "<text>" --accent "<label colour>" --out type/specimen.png
```

It downloads the real font files from Fontsource (the Google Fonts files on the npm registry), caches them, and sets each pairing with the project's spine, subhead, body copy, a label and a line of figures, beside a phone-width column. Look at the full-size image. Check texture at body size, the display line's rhythm and breaks, italics, figures, label legibility, and how the faces sit together on one line. Present the three to the person with a sentence on what each says.

## Stage 4: The type system

Write the Typography section of `BRAND-SYSTEM.md`:

- Faces with roles (display, text, utility), weights and styles used, and their source and licence.
- The scale: base size, ratio and every step in pixels and rem, for desktop and phone.
- Measure, leading and tracking per role; optical-size settings; figure styles per context; how small caps are made.
- Loading: the exact Google Fonts URL or files, subsets, `font-display`, and a fallback stack with `size-adjust` to stop layout shift.
- One display-type event: where the type itself becomes the picture, and its size.

## The tests

- **Squint test:** blur the specimen; the hierarchy still reads from size and weight alone.
- **Swap test:** the faces could not move unchanged to a competitor's site, because their history is this subject's.
- **Paragraph test:** a 60-word paragraph at body size on a phone reads comfortably, with no rivers and even colour.
- **Figure test:** prices, dates and quantities read well in their context.
- **Access test:** body at least 16 px; text spacing survives WCAG 1.4.12 overrides; contrast passes on every ground.

## Anti-patterns

- Choosing from the fonts the model happens to remember.
- A template default with no reason in the rationale log.
- Two display faces arguing.
- Faked small caps, faked italics or faked bold.
- Display faces at body size, or text faces blown up without optical adjustment.
- A type scale with no ratio, sizes picked one by one.

## Files

- `references/typefaces.json`: the curated catalogue, with overuse ratings and commercial suggestions.
- `references/typography.md`: genre mapping, scoring rubric, pairing and setting rules.
- `scripts/type_lookup.py`: catalogue search and live Google Fonts checks (standard library; uses npm for the offline fallback).
- `scripts/specimen.py`: pairing specimens with real copy and real font files (npm; Playwright for Python to render).

## References

- Bringhurst, R. (2004) *The Elements of Typographic Style*. 3rd edn. Vancouver: Hartley and Marks.
- Lupton, E. (2010) *Thinking with Type*. 2nd edn. New York: Princeton Architectural Press.
- Vox, M. (1954) classification of typefaces, adopted by ATypI in 1962.
