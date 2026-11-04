---
name: sign-system-architect
description: Semiotic art direction for websites. Decides what a site should signify, and how, before anything is styled. Produces SIGN-SYSTEM.md for the taste, motion and build skills.
---

# Sign system architect

A site that wins attention and moves people does so because every visible choice means something specific, and those meanings add up to one idea a stranger can feel without being told. Most generated sites fail here first. Their type, colour, imagery and motion are borrowed from the category average, so they signify only "a website of this kind".

This skill does the semiotic work that comes before styling. It reads the subject's own world for signs, maps what the category already says, chooses a position nobody else holds, and translates that position into concrete instructions for type, colour, image, layout, motion, copy and interaction. Its output, `SIGN-SYSTEM.md`, is a brief that the art direction, motion and build skills execute.

It does not choose fonts, write CSS or build pages. It tells the skills that do why each choice must be what it is.

## Where it sits in the pipeline

Run it after `narrative-architect` has produced `BEAT-MAP.md` (or after the brief is agreed, if there is no beat map). Run it before `reference-curator`, `design-taste-frontend`, `impeccable`, `brand-system-architect` or any layout or code generation.

- **Reads:** the brief, `BEAT-MAP.md` if present, any brand material, and source material about the subject.
- **Writes:** `SIGN-SYSTEM.md` in the project root.
- **Hands to:** `reference-curator` (what to look for), `design-taste-frontend` (which dealt direction carries the myth), `impeccable` (what `bolder`, `quieter` and `typeset` should push towards), `motion-choreographer` (what each motion means) and `accessibility-performance-auditor` (the reduced-motion reading must still carry the meaning).

Re-run it whenever the subject, audience or core opposition changes.

## Working rules

1. **Agree the communication goal before generating anything.** Confirm the subject, the audiences and the change in the reader you are after. Do not proceed on a guess when the person is present to ask.
2. **Source widely and distinctly before narrowing.** Gather signs from the subject's own world first, then the category, then adjacent and unrelated fields. Do not narrow until the inventory is broad.
3. **Offer variants, then lock.** Present three sign-system variants that differ in position, not in decoration. The person chooses. Only then write the final file.
4. **Every claim must be true of the subject.** A myth the denotation cannot support is a lie told in design. Do not naturalise a meaning the subject has not earned.
5. **Write plainly.** British English, sentence case headings, no jargon in the output without a one-line gloss. The file is read by build agents and by people outside semiotics.

## The method

Work through the stages in order. Each stage writes a section of `SIGN-SYSTEM.md`.

### Stage 1: intake

Establish, in the person's words where possible:

- **Subject:** what the site is about, in one sentence.
- **Audiences:** at least three readings to design for. Default set: *insiders* (practitioners, existing community), *the curious* (open, uninformed, the wide audience), *sceptics* (people who expect this category to be dull, naive or not for them).
- **Intended change:** what each audience should feel, believe or do after the visit. State it as a shift: from X to Y.
- **Constraints:** brand assets that must stay, accessibility requirements, languages, any cultural sensitivities.

### Stage 2: the native sign inventory

Collect 25 to 40 signs that already exist in the subject's world, before looking at any competitor. Look for:

- materials and textures, tools and objects, places and landscapes, weather and light
- bodies, gestures, postures, rituals and their sequence
- vocabulary, dialect words, names, mottos, numbers that matter
- historical documents, marks, lettering, emblems, uniforms, colours with provenance
- sounds and rhythms

Classify each sign by Peirce's three modes (Peirce, CP 2.247 to 2.249):

| Mode | Relation to what it means | Web example | Weight |
| --- | --- | --- | --- |
| **Icon** | resembles it | an illustration of a hold | useful for clarity, easily generic |
| **Index** | is physically caused by or connected to it | grass stain on a jacket, a scanned archive page, a real hand-cut letterform, ambient sound recorded on site | carries authenticity; prioritise |
| **Symbol** | means it by convention only | a shield logo, a lightbulb for "idea" | needs the audience to know the code; use sparingly, anchor it |

**Rule:** the sign system should be led by indices. Indexical signs are hard to fake and are what make a site feel like it was made by someone who was there. Symbols that the wide audience cannot decode must be anchored (Stage 7) or cut.

Record for each sign: the sign, its mode, its denotation (what it literally shows), its connotations (what it suggests), and where it came from.

### Stage 3: the category code audit

Now map what the category already says. Look at 8 to 15 sites in the same category and 3 to 5 in the category the sceptics would compare it to.

For each, record the paradigm choices (Saussure, 1916/1983): the option chosen on each axis where an alternative existed. Typical axes: serif or grotesque, dark or light ground, photographed or illustrated, centred or asymmetric, fast or slow motion, first person or institutional voice.

Then sort the category's codes using Williams (1977):

- **Dominant:** what nearly everyone does. These are the clichés to avoid or to subvert knowingly.
- **Residual:** older codes still in circulation, often carrying heritage connotations, often lazily (parchment textures, blackletter, sepia).
- **Emergent:** codes a few leading sites are starting to use. These date fastest.

The output is a short table and one sentence naming the category's default meaning: "Sites in this category currently signify ___".

### Stage 4: the semiotic square

Choose the core opposition the subject lives inside. It should be a tension the audience feels, not a style dichotomy. Examples: tradition against invention, belonging against freedom, violence against care, local against universal, effort against ease.

Build the square (Greimas and Rastier, 1968):

```
        S1  ───────── contrary ─────────  S2
         │  \                           /  │
   implication   contradiction   contradiction   implication
         │  /                           \  │
      not-S2 ─────── sub-contrary ─────── not-S1
```

- **S1 and S2:** the two poles (for example, *tradition* and *invention*).
- **not-S1 and not-S2:** their negations (*not tradition*, *not invention*).
- The four corners and the two complex terms (S1 and S2 together; neither S1 nor S2) give six candidate positions.

Plot the category's sites from Stage 3 on the square. The dominant code usually clusters in one corner. The distinctive position is usually an empty corner or a complex term, for example "tradition and invention at once", which is where living practices actually sit.

Cross-check with Floch's (2001) four valorisations to name what kind of value the position promises:

| Valorisation | The site promises | Typical register |
| --- | --- | --- |
| **Practical** | it works, it is useful | clear, functional, informative |
| **Utopian** | it gives meaning, identity, belonging | aspirational, mythic, communal |
| **Critical** | it is good value, considered, honest | comparative, rational, plain |
| **Ludic** | it is pleasurable, surprising, free | playful, sensory, gratuitous |

A site that moves a wide audience usually leads with one utopian or ludic value and proves it with practical or critical signs underneath.

### Stage 5: the myth statement

Barthes (1957/1972) showed that a sign's first meaning (denotation) can become the vehicle for a second, naturalised meaning (myth). Every memorable site carries one. Write it explicitly so it can be designed deliberately and checked for honesty.

Write three lines:

1. **Denotation:** what the site literally shows and says. ("Two people in white jackets gripping each other's collars on a village green.")
2. **Connotation:** what those signs suggest. ("Fairness, restraint, an old physical courtesy.")
3. **Myth:** the one sentence the reader should leave believing, as if it were simply true. ("Strength here has always been governed by honour.")

**Honesty check:** list the denotative evidence that supports the myth. If the evidence is thin, weaken the myth until it is supported. Do not let design do work the subject cannot back.

Then identify the **punctum** for the site and for each major beat (Barthes, 1980/1981): the specific, unplanned-looking detail that pierces the reader, as distinct from the *studium*, the general cultural interest of the scene. A worn cuff, a scorer's chalk mark, a child watching from a wall. Moving content runs on punctums, not on spectacle.

### Stage 6: translation into design channels

This is the core of the file. For each channel, state the decision, the meaning it carries, and the sign it derives from in the inventory. Use these grammars:

**Typography** (van Leeuwen, 2006). Describe type by its semiotic features rather than by name, so the build agent can choose fonts that match:

| Feature | Low pole means | High pole means |
| --- | --- | --- |
| Weight | delicacy, lightness, timidity | presence, solidity, insistence |
| Expansion | economy, pressure, tension | room, ease, generosity |
| Slope | upright, formal, static | movement, personal hand, informality |
| Curvature | angular, harsh, technical | round, soft, organic |
| Connectivity | discrete, modular, mechanical | joined, flowing, handwritten |
| Orientation | vertical, aspiring, tall | horizontal, grounded, settled |
| Regularity | irregular, crafted, imperfect | regular, standardised, industrial |

State the target position on each feature and why. Name the provenance if lettering comes from the subject's world (a sign painter, an archive, a stone).

**Colour** (van Leeuwen, 2011). Specify by feature, not just by hue:

- **Value** (light to dark), **saturation** (muted to intense), **purity** (pure to hybrid), **modulation** (flat to textured), **differentiation** (monochrome to varied), **hue** (warm to cold).
- Give each colour a provenance from the inventory (the lichen on a particular stone, a club ribbon, wet slate) and a job (ground, voice, signal).
- Check cross-cultural readings of key hues for the intended audiences; record any conflict.

**Imagery** (Kress and van Leeuwen, 2021). For each image role, state:

- **Contact:** *demand* (subject looks at the reader, asks for a relationship) or *offer* (subject is looked at, presented as information).
- **Social distance:** close-up (intimate), medium (social), long shot (impersonal, contextual).
- **Attitude:** frontal angle (involvement) or oblique (detachment); high angle (reader has power), eye level (equality), low angle (subject has power).
- **Modality:** how real it claims to be. Archival and documentary images claim high naturalistic modality; illustration claims lower. Mixing them is a meaning, not an accident.
- **Index preference:** real photographs, scans and recordings of the actual subject over stock or generated images. If imagery must be generated, it must not impersonate documentary evidence.

**Composition** (Kress and van Leeuwen, 2021):

- **Given and new** (left and right): place what the reader already accepts on the left, what you are introducing on the right.
- **Ideal and real** (top and bottom): the promise or essence above, the concrete evidence or action below.
- **Centre and margin:** a centred element is the nucleus everything else serves. Use centring only when one thing genuinely is the nucleus; it is not a default.
- **Salience:** name the single most salient element per beat and why.
- **Framing:** strong frames separate, weak frames connect. Decide where content should run together and where it should be cut apart.

**Motion** (Lakoff and Johnson, 1980). Motion is meaning carried by orientation, tempo and physics. Use the orientational metaphors the audience already lives by:

- up is more, better, rising; down is less, grounded, settling
- forward (into depth) is future and approach; backward is past
- in is intimacy and essence; out is release, context, the wider world
- heavy and slow is weight, seriousness, gravity; light and quick is ease, play
- resistance and release (scrub with lag, pin then let go) is effort and achievement

For each motion idea, state: what it does, what it means, which sign it embodies, and what the static reading is under `prefers-reduced-motion`. The meaning must survive with motion removed.

**Copy** (Jakobson, 1960). For each part of the site, name the dominant function:

- **Referential:** informs about the world.
- **Emotive:** expresses the speaker's feeling.
- **Conative:** addresses and moves the reader ("you").
- **Phatic:** keeps the channel open, builds relationship.
- **Metalingual:** explains the code itself (glossaries, definitions).
- **Poetic:** draws attention to the message's own form (rhythm, sound, the line itself).

Most hero sections should be poetic with a conative turn. Most proof sections should be referential. Any section using insider vocabulary needs a metalingual element.

**Sound and interaction.** If used, state what each sound or response indexes (is caused by) in the subject's world. A click that sounds like nothing in the subject's world is noise.

### Stage 7: reading paths for a wide audience

Hall (1980) distinguished three ways an audience decodes a message: the **dominant** reading (as intended), the **negotiated** reading (accepted in part, adapted to the reader's own situation) and the **oppositional** reading (understood, then rejected or turned against itself). Eco (1979) adds that every text constructs a *model reader*, and a text that assumes too much competence becomes closed to everyone else.

For each audience from Stage 1, walk the beats and record:

- what they will read at each beat (dominant, negotiated or oppositional)
- which signs they cannot decode
- the **anchorage** that fixes the intended meaning for them (Barthes, 1964/1977): a caption, a label, a single line of copy that tells the stranger what they are looking at without explaining the joke to the insider
- where the sceptic's oppositional reading is likely (looks twee, looks aggressive, looks exclusive) and the sign that pre-empts it

Then consider boundary translation (Lotman, 1990). Culturally specific material travels to a wide audience across a boundary where it must be translated, not flattened. Keep the specific sign; add the minimal anchorage that lets an outsider in. Never replace a local sign with a generic one to make it "accessible"; that loses the reason anyone would care.

Taste check before presenting variants: see `detail-craft/references/taste-lessons.md`. Each variant should name its colour temperature, its single personality face, and its (at most) three repeated devices.

### Stage 8: variants and lock

Generate three variants. Each must occupy a **different position on the square**, with its own myth statement and a short channel table. Do not produce three styles of the same position.

For each variant give: position, myth, valorisation, three signature signs, what it risks, and which audience it serves best.

Ask the person to choose, combine or redirect. When the person is not available, choose the variant whose myth is best supported by denotation and whose position is least occupied, and say so at the top of the file.

Then write the final `SIGN-SYSTEM.md`.

## The tests

Run all five on the locked system and record the result in the file.

1. **Commutation test.** For each signature choice (a font feature, a colour, an image type, a motion), mentally swap it for the category default. If the meaning does not change, the choice is empty: replace it with a sign that carries meaning, or remove it. This is the structuralist method for finding which differences signify (Saussure, 1916/1983; Barthes, 1964/1967).
2. **Stranger test.** Could someone with no knowledge of the subject state the myth after the first two beats, in their own words? If not, add anchorage.
3. **Insider test.** Would a practitioner wince at any sign as false, costume-like or wrong in detail? If so, it fails regardless of how it looks.
4. **Cliché test.** Does any sign appear in the dominant codes from Stage 3, or in the generic stock of web symbolism (lightbulbs, handshakes, globes, upward arrows, gradient blobs, "hero" stock photography)? Remove or deliberately subvert it.
5. **Static test.** With motion off, sound off and images unloaded (alt text only), does the site still carry the myth? Meaning must not depend on one channel.

## Anti-patterns: semiotic slop

- **Stock symbols:** conventional icons standing in for ideas the subject could show indexically.
- **Heritage costume:** residual codes (parchment, distressed textures, blackletter, sepia) applied to signal "old" without provenance.
- **Appropriation as ornament:** cultural signs lifted for texture without the community's meaning, context or credit.
- **Unanchored cleverness:** signs only insiders can read, presented to a wide audience without a way in.
- **Myth without evidence:** connotations the subject cannot support.
- **Motion without meaning:** parallax, reveals and scroll effects that could be swapped for any other effect with no loss.
- **Universal centring:** every element centred, so nothing is the nucleus.

## Output: SIGN-SYSTEM.md

Use this structure. Keep it to what build agents need; put working notes in an appendix.

```markdown
# Sign system: <project>

Status: <locked | draft> · Variant chosen: <name> · Date: <date>

## Communication goal
Subject, audiences, intended shift for each.

## Myth
Denotation / connotation / myth, with supporting evidence.
Valorisation and square position (with the square drawn).

## Signature signs
The five to eight signs that carry the system, each with Peirce mode, provenance and meaning.

## Channels
### Typography (feature targets and why)
### Colour (features, named colours with provenance and job)
### Imagery (contact, distance, attitude, modality, sourcing rules)
### Composition (given/new, ideal/real, centre/margin, salience, framing)
### Motion (each idea: action, meaning, sign, reduced-motion reading)
### Copy (dominant function per section; anchorage lines)
### Sound and interaction (if any)

## Beat assignments
For each beat in BEAT-MAP.md: the sign it foregrounds, its punctum, its dominant copy function, and the anchorage for outsiders.

## Reading paths
Per audience: expected reading, undecodable signs, anchorage, oppositional risk and pre-emption.

## Do not
Category clichés and slop specific to this subject.

## Test results
Commutation, stranger, insider, cliché, static.

## Handoff notes
- reference-curator: look for <...>
- design-taste-frontend: choose the dealt direction closest to <...>; reject any that <...>
- impeccable: bolder/quieter towards <...>
- motion-choreographer: <...>

## References
```

## References

- Barthes, R. (1967) *Elements of Semiology*. Trans. A. Lavers and C. Smith. London: Jonathan Cape. (Original work published 1964.)
- Barthes, R. (1972) *Mythologies*. Trans. A. Lavers. London: Jonathan Cape. (Original work published 1957.)
- Barthes, R. (1977) 'Rhetoric of the image', in *Image, Music, Text*. Trans. S. Heath. London: Fontana, pp. 32 to 51. (Original work published 1964.)
- Barthes, R. (1981) *Camera Lucida: Reflections on Photography*. Trans. R. Howard. New York: Hill and Wang. (Original work published 1980.)
- Chandler, D. (2017) *Semiotics: The Basics*. 3rd edn. London: Routledge.
- Eco, U. (1979) *The Role of the Reader: Explorations in the Semiotics of Texts*. Bloomington: Indiana University Press.
- Floch, J.-M. (2001) *Semiotics, Marketing and Communication: Beneath the Signs, the Strategies*. Trans. R. O. Bodkin. Basingstoke: Palgrave. (Original work published 1990.)
- Greimas, A. J. and Rastier, F. (1968) 'The interaction of semiotic constraints', *Yale French Studies*, 41, pp. 86 to 105.
- Hall, S. (1980) 'Encoding/decoding', in Hall, S. et al. (eds) *Culture, Media, Language*. London: Hutchinson, pp. 128 to 138.
- Jakobson, R. (1960) 'Closing statement: linguistics and poetics', in Sebeok, T. A. (ed.) *Style in Language*. Cambridge, MA: MIT Press, pp. 350 to 377.
- Kress, G. and van Leeuwen, T. (2021) *Reading Images: The Grammar of Visual Design*. 3rd edn. London: Routledge.
- Lakoff, G. and Johnson, M. (1980) *Metaphors We Live By*. Chicago: University of Chicago Press.
- Lotman, Y. M. (1990) *Universe of the Mind: A Semiotic Theory of Culture*. Trans. A. Shukman. London: I. B. Tauris.
- Oswald, L. R. (2012) *Marketing Semiotics: Signs, Strategies, and Brand Value*. Oxford: Oxford University Press.
- Peirce, C. S. (1931 to 1958) *Collected Papers of Charles Sanders Peirce*. Ed. C. Hartshorne, P. Weiss and A. Burks. Cambridge, MA: Harvard University Press. (Icon, index and symbol: CP 2.247 to 2.249.)
- Saussure, F. de (1983) *Course in General Linguistics*. Trans. R. Harris. London: Duckworth. (Original work published 1916.)
- van Leeuwen, T. (2006) 'Towards a semiotics of typography', *Information Design Journal*, 14(2), pp. 139 to 155.
- van Leeuwen, T. (2011) *The Language of Colour: An Introduction*. London: Routledge.
- Williams, R. (1977) *Marxism and Literature*. Oxford: Oxford University Press.
