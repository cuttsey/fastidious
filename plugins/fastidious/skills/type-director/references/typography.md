# Typography method

## From meaning to genre

Typefaces carry history. Start from the period, material and register in `SIGN-SYSTEM.md`, find the genre that shares them, and only then look for faces. The genres follow the Vox-ATypI classification (Vox, 1954; adopted by ATypI, 1962), extended with the sans families it predates.

| If the subject is | Look first at | Because |
| --- | --- | --- |
| Rural, handmade, English, seventeenth or eighteenth century | Fell types, Caslon, Garalde old styles | They were cut and printed in that world; their irregularity reads as hand and time |
| Literary, scholarly, cultural | Garalde old style, calligraphic old style (Alegreya), Bembo-like (Cardo) | Centuries of books |
| Rational, Enlightenment, scientific, legal | Transitional (Baskerville, Fournier lineage) | Sharper contrast, vertical stress: the age of reason |
| Luxury, fashion, perfume, formality | Didone (Bodoni Moda) | Extreme contrast reads as precision and expense |
| Victorian, industrial, almanac, poster | Modern faces, Clarendon (Besley), fat face, wood type | Nineteenth-century print |
| Modernist, Bauhaus, architecture | Geometric sans (Jost) | Circle, square, triangle |
| Civic, signage, public service | Neo-grotesque or humanist sans (Public Sans, Barlow, Source Sans 3) | Signs, forms, legibility |
| English civic and craft, twentieth century | Humanist sans after Johnston and Gill (Cabin) | London Transport and English lettering |
| Engineering, data, documents | Grotesque plus monospace (IBM Plex, Fragment Mono, Courier Prime for typed records) | Instruments and typed records |

## Scoring candidates

Score each candidate 0 to 3 on every line. Shortlist three pairings that differ in genre, not three variants of one.

| Criterion | What 3 looks like |
| --- | --- |
| Meaning | The genre's history matches the sign system's period, material and register |
| Voice | Its texture at text size matches the voice adjectives in `BRAND-SYSTEM.md` |
| Craft | Real italics, real small caps, old-style and tabular figures where the work needs them; optical sizes if it is set across a wide range |
| Range | Enough weights and styles for the hierarchy without faking any |
| Language | Every subset the work needs, including accents in names |
| Distinction | Overuse 0 or 1 in `typefaces.json`; not one of the families on every AI-built page |
| Delivery | Licence fits the use; available from a host the build can load (Artifacts: Google Fonts, or inlined files) |

Distinction is a criterion, not a veto. A widely used face is right when its meaning is right and the setting is exceptional. A rare face set badly is still badly set.

## Pairing

- **Contrast in structure, harmony in proportion.** Pair across genres (a serif with a sans, a Garalde with a humanist sans), and match x-height and stroke weight so the two sit on one line without one shouting.
- **One family is often enough.** A superfamily with optical sizes (Source Serif 4, Newsreader, Literata) can carry display and text alone. Add a second face only when it does a job the first cannot: labels, data, a historical display voice.
- **Never two display faces.** One voice speaks; the other explains.
- **The utility face** (labels, figures, captions) is usually a sans or a mono, small, with letter-spacing of +0.04 to +0.12 em in capitals or small caps.

## Setting

- **Scale.** Choose a modular ratio from the density of the content: 1.2 to 1.25 for dense information, 1.333 to 1.5 for editorial, 1.618 or larger for a few huge statements. Derive every size from the base; round to whole pixels.
- **Measure.** 45 to 75 characters for body text; about 66 is ideal (Bringhurst, 2004). Narrower on phones is fine; wider never is.
- **Leading.** 1.4 to 1.6 for body, tighter as size grows: about 1.1 to 1.2 for headings and 0.9 to 1.0 for very large display.
- **Tracking.** Tighten large display slightly (about -0.01 to -0.03 em); open small capitals and labels (+0.04 to +0.12 em); never track lower-case body text.
- **Optical size.** Use `font-optical-sizing: auto` with families that have an `opsz` axis, or pick the display and text cuts by hand (Caslon Display and Text, Fell sizes).
- **Figures.** Old-style figures in running text, lining in headings, tabular wherever numbers align.
- **Small caps.** Only real ones (`font-variant-caps: small-caps` on a face with `smcp`, or an SC family). Faked small caps are shrunken capitals and look thin.
- **Wrapping.** `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs; write display lines with their breaks.
- **Loading.** Subset to the languages used, load only the weights used, `font-display: swap`, and set a fallback with `size-adjust` and `ascent-override` so the page does not jump.
- **Access.** Body at least 16 px (18 to 20 px for long reading), text spacing that survives WCAG 1.4.12 overrides, and no meaning carried by weight or style alone.

## Sources

- Bringhurst, R. (2004) *The Elements of Typographic Style*. 3rd edn. Vancouver: Hartley and Marks.
- Lupton, E. (2010) *Thinking with Type*. 2nd edn. New York: Princeton Architectural Press.
- Vox, M. (1954) classification of typefaces, adopted by ATypI in 1962 as the Vox-ATypI classification.
- W3C (2023) *Web Content Accessibility Guidelines (WCAG) 2.2*, success criterion 1.4.12, Text spacing.
