# Type and colour: Hollow Lane

The first version of this page used Newsreader on a warm cream and brown palette. Both were chosen from memory, and both read as the defaults of AI-built pages. This is the second version, made with `type-director` and `colour-director`.

## Type

**Brief.** A slow, handmade English craft, told as a seventeenth-century world in miniature. The display face should carry English printing history and a hand-made texture; the text face should read easily at length on a dark ground; labels should feel like a printer's small capitals.

**Lookup.** `type_lookup.py --genre "seventeenth-century,old style,english" --voice rustic,english,craft --max-overuse 1` returned the Fell types, Libre Caslon and Sorts Mill Goudy first. `--live` confirmed the Fell faces on Google Fonts: one weight, roman and italic, latin only, with separate SC families.

**Specimens.** Round one (`type/specimen-round-1.png`) compared Fell with Cabin, Caslon Display with Caslon Text, Goudy with Crimson Pro, and Newsreader alone, on the old palette. Round two (`type/specimen-round-2.png`) set three pairings on the new palette.

**Chosen.** IM Fell Double Pica for display, with its SC family for labels and buttons; Source Serif 4 for reading, with old-style figures. The Fell types were cut for printing in seventeenth-century England, so their irregular texture says "made by hand, over time" before a word is read. Source Serif 4 has optical sizes and steady colour at 17 to 20 px on a dark ground.

## Colour

**Sources.** `palette.py extract` over the six scene posters returned ten browns and olives, all within one hue family and below 0.07 chroma: the orchard world is warm and muddy. The old page palette fails `palette.py check` for the same reason ("one temperature, low chroma").

**Combination.** `palette.py wada --near "#a86b2b,#6f6e3a"` (the russet apple and the lit felt) returned Wada's combination 243 first: Raw Sienna, Ivory Buff, Olive Green and Slate. The slate is the counterweight the world lacks: a cool ground that makes the warm film and the sienna read as warm.

**Roles.** Slate deepened to `#18222a` for the ground; Ivory Buff lightened to `#f1e3c3` for text on dark and for paper; Raw Sienna for the one action (the button) and, lightened, for labels; Olive deepened to `#565b33` for labels on paper. `colour/tokens.json` holds every pair, and `colour/sheet.html` shows them.

**Checks.** Every text pair passes 4.5:1 and every large pair 3:1; no cliché is detected. `legibility-check.js --full --motion` measures the labels and copy against the real film at phone and desktop widths.
