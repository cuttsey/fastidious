---
name: iconography
description: Decide whether a product needs icons at all, which kind, and in what style, and find the motifs and illustrations that carry the brand's world through the UI. Covers UI icons (navigation, actions, status), pictograms (content, techniques, categories), motifs (repeated graphic devices drawn from the subject), and illustration (spot, hero, empty states). It derives the style from the brand (stroke from type stems, corners from shape tokens, a grid, optical sizes), chooses between an open library and a custom set (with licences), and audits and specimens the result. Part of the detail layer. Use when building or reviewing any UI that might use icons, when someone asks "what icons should we use?", "do we need illustrations?" or "what's our motif?", or when a design reads generic because of stock symbols.
---

# Iconography and motifs

Icons are the cheapest way to make an interface look like everyone else's. A row of tinted squares with a lightbulb, a rocket and a handshake signals "template" before a word is read. Done well, the same layer becomes one of the strongest carriers of personality. Think of a set drawn with the brand's own stroke, symbols taken from the subject's world, and one motif that recurs like a signature.

**The personality is the product.** Every mark must look like it was drawn by the same hand that set the type and must come from the same world as the brand. An icon that could move unchanged to a competitor's site fails the swap test.

## Where it sits
- **Part of `detail-craft`.** It runs in its Stage C (ambient layer) and feeds its signature moments. Its rationale follows detail-craft's six registers.
- **Reads:** `SIGN-SYSTEM.md` (the native sign inventory, Peirce modes and clichés to avoid), `BRAND-SYSTEM.md` (type, stems, radii, colour roles, motion), `DETAIL-PLAN.md`, the built UI and the content model (what actually needs a symbol).
- **Writes:** `ICONOGRAPHY.md` (decisions, the style specification and the motif rules), `assets/icons/` (SVG files plus a sprite), and a specimen page from `scripts/specimen.mjs`. It feeds the brand book's Iconography chapter.

## The method

### Stage A: the need test (do this first, and be willing to answer "none")
List every place a symbol might go. For each one, ask in order:
1. **Is there room for the word?** If yes, use the word. Words beat icons for comprehension almost everywhere.
2. **Is this a universal convention?** Examples: close ×, menu, search, play/pause, external link ↗, download, the arrow on an action, a check or cross. Conventions earn an icon *with* a label, or alone where space truly forces it, always with an accessible name.
3. **Does the reader need to scan or compare many items fast?** Examples: categories, levels, statuses, filters, file types. Pictograms or encoded marks such as dots, pins and shapes earn their place here.
4. **Is it decoration?** Then it is a *motif* (Stage D), not an icon, and it must come from the subject's world. Otherwise cut it.

Record the outcome per slot: **word**, **convention icon plus label**, **pictogram or encoded mark**, **motif** or **nothing**. Many good brands end with five to ten icons in total, and that is a strong position, not a gap.

### Stage B: library or custom (see `references/decision-guide.md`)
- **Open library** (Lucide, Phosphor, Tabler, Heroicons, Material Symbols) for conventions. Pick one, never mix two, and match its stroke and corners to the brand (Stage C). Check its licence.
- **Custom set** when icons carry the brand's subject (a curriculum, a menu, techniques, places) or when fewer than about twelve icons are needed. Draw them on the brand's grid. A small custom set beats a large borrowed one.
- **Hybrid:** library conventions plus custom subject pictograms, drawn to the same stroke, grid and corners.

### Stage C: derive the style from the brand (never pick it by taste)
Fill in the style specification table in `references/decision-guide.md`:
- **Grid and keyline:** 24 px with a 2 px live-area margin (16 px for dense UI). Optical sizes at 16, 20, 24 and 32.
- **Stroke:** take it from the text face's stem at the size icons sit beside. Usually 1.5–2 px at 24. A heavy condensed display brand may use 2–2.25 px; a fine editorial brand 1.25–1.5 px.
- **Corners and terminals:** match the shape tokens (pill radius means round caps and joins; cut corners mean square caps and miter joins).
- **Fill or outline:** outline at rest and filled for a selected or active state, or one style only. Never mixed in one row.
- **Colour:** `currentColor` only, inheriting text colour. The accent appears only as a state. Icons used as essential graphics need 3:1 contrast against their ground (WCAG 1.4.11).
- **Detail:** reduce until it reads at 16 px. Strip perspective, shading and tiny counters.
- **Motion:** icons move only to confirm (draw-on, a nudge, a state morph), using the brand's motion tokens and respecting reduced motion.

### Stage D: motifs, the brand's recurring marks (see `references/motifs.md`)
Draw two or three motifs from the sign inventory, indexical first (marks caused by the subject: a chalk line, a stitch, a stamp, a footprint, a tide line). For each one, define:
- its meaning;
- where it appears (section edges, progress, bullets, dividers, empty states, loaders, the cursor);
- its scale range;
- its density (how many per screen at most);
- what it must never do.

A motif earns its place by repetition with variation. It is the same mark at three scales and in three jobs, never sprinkled.

### Stage E: illustration (only if it carries something photography can't)
- Choose a **modality**: documentary (photographs, archive), diagrammatic (how something works), or expressive (mood, character). Mixing modalities is a meaning. Do it deliberately and label it.
- Draw from the same stroke and colour roles as the icons. Spot illustrations follow the icon grid at 2–4× scale.
- **Empty states and errors** get the brand voice plus one small motif, not a stock scene.
- Never present illustration or AI imagery as documentary evidence.

### Stage F: build, audit, specimen
1. Draw or adapt the SVGs into `assets/icons/`: `viewBox="0 0 24 24"`, `fill="none"` and `stroke="currentColor"` (or `fill="currentColor"` for solid marks), with no hard-coded colours, no transforms left in, and clean paths.
2. Run `node <skill>/scripts/icon-audit.mjs assets/icons`. It checks viewBox, stroke widths, caps and joins, hard-coded colours, transforms, size and naming consistency. Fix every fail.
3. Run `node <skill>/scripts/specimen.mjs assets/icons --out icons-specimen.html`. The sheet shows every icon at 16, 20, 24 and 32, in light and dark, beside a line of the brand's text. Look at it: one hand, one weight, one grid?
4. In the UI, an icon beside a word is `aria-hidden="true"`. An icon-only control has an accessible name (`aria-label`) and a visible tooltip on hover and focus where possible. A decorative motif is `aria-hidden` and carries no meaning that isn't also in text.

### Stage G: rationale and handover
Add one entry per decision to `DESIGN-RATIONALE-DETAILS.md` (six registers). Write `ICONOGRAPHY.md` and pass the rules to the brand book's Iconography chapter: the need test results, the style specification, the set, the motifs, dos and don'ts, and the licence.

## Clichés to refuse
Lightbulb (idea), rocket (launch or growth), handshake (partnership), globe (international), shield-and-tick (security), gears (process), target (goals), trophy (success), brain (smart), puzzle pieces (solution), sparkles (AI or magic), people icons in a circle (community). Also: icons in tinted rounded squares above three feature cards, emoji as section markers, two libraries mixed, and decorative icons beside every heading. If the brief seems to need one, find the subject's own sign instead (see `references/motifs.md`).

## Output: ICONOGRAPHY.md
```
# Iconography: <project>
## Need test (slot → word | convention+label | pictogram | motif | nothing)
## Source (library + licence | custom | hybrid) and why
## Style spec (grid, stroke, caps/joins, corners, fill rule, sizes, colour, motion)
## The set (name, meaning, where used)
## Motifs (name, meaning, sign mode, uses, scale, density, never)
## Illustration (modality, style, where, never)
## Accessibility (labels, contrast, motion)
## Rationale (six registers, per decision)
```
