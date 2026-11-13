---
name: identity-director
description: Designs a brand identity that fits the character of the business. Reads what customers have at stake to set the register, mines one idea from the name, verb or promise, draws it as a mark, grows the mark into a motif and a system, gives the brand one colour move its category does not use, and proves it on real objects in the world. Use whenever a project needs a logo, mark or identity made or judged, before colour-director, type-director and brand-system-architect lock the system.
---

# Identity director

Generated identities fail in a few predictable ways. The logo is a word in a neutral sans on white. The palette is the category's code (blue for money, purple on black for creative AI, green for health). The idea, if there is one, needs a paragraph to explain. And the only proof is a laptop on a table.

The best startup identity work does the opposite. Primary's fourteen case studies (studied 2026-11-13, see `references/primary-portfolio.md`) show the pattern clearly: Lovable's heartbeat, Paper's two sheets folded into a P, Weaver's woven grid lines, Solidroad's golden road and Owner's star that helps owners shine. Each idea comes from the business itself. Each becomes a mark, then a motif, then a system, set at a loudness that suits what the customer has at stake. And each is proven on socks, totes, stages and subway posters, not only on screens.

This skill works the same way. It decides the identity's idea, mark, register and owned colour move, then hands them to the colour, type and world specialists to build.

## Where it sits in the pipeline

- **Runs:** in phase 4, after `sign-system-architect` and before `colour-director`, `type-director` and `brand-system-architect`. Run it again if the positioning changes.
- **Reads:** `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md`, the voice in `BRAND-SYSTEM.md` if it exists, `COPY-DECK.md`, `REFERENCES.md`, and any existing logo or brand material.
- **Writes:** `IDENTITY.md` (from `templates/IDENTITY.md`) and `identity/` (the category audit, mark sketches as SVG, application renders).
- **Hands to:** `colour-director` (the register, the owned colour move and the competitors' colours), `type-director` (the register and the genre the idea suggests), `world-bible` and `asset-director` (the material and the motif), `iconography` (the motif), `brand-book` (the mark, its rules and the applications).

## Working rules

1. **Read the character before the look.** What does the customer risk, and what do they make? Stakes set the register; the register sets how loud the identity may be.
2. **Mine one idea from the business.** The name, the product's verb, the promise or the customer's world. State it in one sentence a stranger could repeat. If it needs a second sentence, it is not the idea yet.
3. **Borrow from outside the category.** A publication, an era, a craft, a place: Heron took the New Yorker into private credit, Frame took 90s New York old money into payments. Never borrow from a competitor.
4. **The mark draws the idea.** One shape that still reads at 16 pixels, in one colour, upside down on a sticker.
5. **Grow a motif from the mark.** One part of the mark repeats as a device with a job: a pattern, a frame, a bullet, a loader. Same mark, three scales, three jobs.
6. **Own one colour move.** One hue across everything, a gradient with a meaning, a named kit, or one warm signal on quiet grounds. It must not be the category's code. Tint the lights and give the darks a hue.
7. **Material is the idea made physical.** Paper, knit, leather, blur, sky. Choose it with the idea, not after.
8. **Prove it in the world.** At least six applications, two of them objects only this brand would make. Device mock-ups alone prove nothing about the brand.
9. **Two directions, then lock.** Two directions that differ in idea, not in styling. The person chooses; record it with `option-ledger`.
10. **Write plainly.** British English, sentence case headings.

## Stage 1: Read the character

Write the first section of `IDENTITY.md`:

- **What the customer risks:** money, health, reputation, time, or nothing much.
- **What the customer makes or does:** builds, writes, cooks, invests, recovers.
- **The register**, chosen from three:

| Register | When | What it allows | Precedents |
| --- | --- | --- | --- |
| Trust | Customers risk money, health or reputation | A hued deep ground, a tinted light, one warm signal, an editorial serif or calm geometric sans | Heron, Frame, Alan, Incentiv |
| Warm | Customers are small owners or teams who need a friend | One colour people can name, illustration or a mascot, friendly type | Owner, Solidroad, Loti |
| Expressive | Customers make things | A gradient, a colour kit, collage, tactile material, a stretchable type family | Lovable, Craft, Paper, Weaver, Gist |

A trust brand can still be warm (Alan's orange), and an expressive brand still needs restraint somewhere (Lovable's cream ground).

- **The category code:** audit five competitors. Record each one's main colours as hexes, its type genre and its kind of mark in `identity/category.md`. The code is whatever most of them share. This list is the input to the ownership check.

## Stage 2: Mine the idea

Write at least six candidate ideas, at least one from each source:

| Source | Question | Examples |
| --- | --- | --- |
| Name | What picture is in the word? | Lovable: a heartbeat. Paper: two sheets. Weaver: crossing lines. Solidroad: a golden road. |
| Verb | What does the product let people do? | Gist: remix. Frame: put things in a frame. |
| Promise | What changes for the customer? | Owner: owners shine. |
| Customer's world | What objects, places and rituals do they live with? | Loti: a bird's-eye watch over the internet. |
| Reference | Which era, publication or craft outside the category shares the brand's attitude? | Heron: the New Yorker. Titan: the 1980s. |

Score each from 0 to 2 on four tests, and take the two highest:

- **Ownable:** no competitor could use it.
- **Drawable:** it becomes one simple shape.
- **Extensible:** it gives a motif, a material and a way of writing.
- **True:** it comes from the business, not from a mood board.

Run `python3 scripts/precedents.py --source name` (or `--register`, `--structure`) to see how studied identities answered the same question.

## Stage 3: Mark and motif

For each direction:

- Draw the mark as SVG in `identity/`. Test it at 16, 32 and 512 pixels, in one colour, reversed, and on a busy photograph.
- Name the motif and give it three jobs (for example: a pattern on packaging, a frame for screenshots, a bullet in lists).
- Write the one-sentence idea above the mark. If the mark does not show that sentence, redraw it.

## Stage 4: Hand over the system

- **Colour:** give `colour-director` the register, the owned move you intend and the category's hexes. It builds the palette and runs `palette.py fit tokens.json --register <register> --category "<competitor hexes>"`, which names the palette's structure, flags register breaks and fails a signal that sits within 25 degrees of a competitor's hue.
- **Type:** give `type-director` the register and the genre the idea suggests (an editorial serif for an idea from a publication; a grotesk with condensed widths for a remixable kit).
- **Material and imagery:** give `world-bible` the material and the motif, so every picture comes from the identity's world.

## Stage 5: Prove it in the world

Make at least six applications and render them with the real palette and type, as HTML scenes or Blender renders (`blender-build`):

- Two that every brand needs: the product screen and a social post.
- Two at street scale: a billboard, a subway poster, a stage screen or shop window.
- Two objects only this brand would make: Lovable's socks, Weaver's knit patch, Paper's embossed cap, Owner's hoodie.

Check each one at thumbnail size beside the competitors' equivalents. The brand should be recognisable from colour and motif alone, with the name covered.

## Stage 6: Write `IDENTITY.md`

Use `templates/IDENTITY.md`: the character, the register, the category code, the idea in one sentence, the mark and its tests, the motif and its jobs, the owned colour move, the material, the applications, the second direction and why it lost, and what is never done.

## The tests

- **Sentence test:** the idea fits in one sentence a stranger could repeat.
- **Swap test:** the mark, the colour move and the motif could not move to a competitor.
- **Favicon test:** the mark reads at 16 pixels in one colour.
- **Covered-name test:** the brand is recognisable with its name hidden.
- **Sock test:** the identity works on an object that is not a screen or a page.
- **Register test:** the loudness suits what the customer has at stake.
- **Ownership test:** `palette.py fit` passes against the category's colours.

## Anti-patterns

- A wordmark on white as the whole identity.
- The category's colour code: blue for money, purple on black for creative tools, green for health.
- An idea that needs a paragraph.
- The literal reading of the name with nowhere to go (a star for Stellar).
- A neutral near-black ground with one glowing accent.
- Device mock-ups as the only proof.
- Two directions that differ only in colour.

## Files

- `references/primary-portfolio.md`: the fourteen identities studied, the palette structures, type and material, and the weaker cases.
- `references/precedents.json`: the same cases as data (register, idea source, mark, structure, measured palette, type, material, verdict). Read by `precedents.py` and by `colour-director`'s `palette.py fit`.
- `scripts/precedents.py`: search the precedents (standard library).
- `templates/IDENTITY.md`: the identity record.

## References

- Primary (2026) [Work](https://www.primary.studio/work), [Pricing](https://www.primary.studio/pricing). Case studies observed 13 November 2026.
- Romaniuk, J. (2018) *Building Distinctive Brand Assets*. Melbourne: Oxford University Press.
- Sharp, B. (2010) *How Brands Grow*. Melbourne: Oxford University Press.
- Wheeler, A. (2017) *Designing Brand Identity*. 5th edn. Hoboken: Wiley.
