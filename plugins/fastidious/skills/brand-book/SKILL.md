---
name: brand-book
description: Produce a Digital Brand Book, a browsable, published guide that holds a brand's position, voice, logo, colour, type, imagery, brand codes, layout, motion, sound, iconography, applications, downloads and governance. Each rule comes with a specimen, dos and don'ts, and the reason behind it. Use when someone asks for a brand book, brand guidelines, brand portal, identity guide or style guide for people to follow, or wants an existing project's identity documented for partners, volunteers, agencies or new staff. It works from the project's own decisions (POSITIONING, SIGN-SYSTEM, BRAND-SYSTEM, DETAIL-PLAN, the built site) and never invents facts. Layout and visual design come from the studio's design skills, not from any reference portal.
---

# Brand book

A brand book is the identity's operating manual. Someone who has never met the team should be able to make a correct poster, post, page or jacket from it alone. People open it to answer a question ("which logo on a dark photo?", "what do we call the referee?", "can I use this green for text?"), so every page must answer one quickly and show the answer, not just describe it.

**What makes it good:** each rule has a reason, a specimen and a boundary (do / don't). **What makes it bad:** pages of adjectives, mood words with no rule, values without contrast checks, logos without clear space, and anything that only the designer could apply.

**The personality is the product,** here too. The book is itself an application of the identity. It uses the brand's own tokens, type, voice, cursor, scrollbar and hover gesture, and its microcopy speaks in the brand voice. Facts stay plain.

## Where it sits

- **Reads (in this order of authority):** `POSITIONING.md`, `FRAME.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md`, `DETAIL-PLAN.md`, `DESIGN-RATIONALE-DETAILS.md`, the built site (CSS tokens, components, copy), logo files, imagery folders, and any older brand material the person has, such as decks, guides, merch or social templates.
- **Writes:** `brand-book/` in the project. It holds `index.html` (the book), `brand-book.css` and `img/`, plus `BRAND-BOOK-GAPS.md`, the list of decisions the book could not source. Publish it as an Artifact when the person wants to share it.
- **Design comes from the studio, not the reference.** Use `brand-system-architect` tokens, `design-taste-frontend` house rules and checks (`lint.mjs`, `inspect.mjs`), and `detail-craft`, including the v1 baseline of cursor, scrollbar and hover gesture plus a six-register rationale for the book's own signature details. Brand portals such as Frontify-style sites taught us **what content to include, not how to lay it out.**

## The method

### Stage A: inventory the sources
List every source file and asset with what it settles. Prefer the most recent locked decision. If two sources disagree, note it in `BRAND-BOOK-GAPS.md` and do not pick silently.

Before drafting any statement, look for the organisation's own published words: its About page, mission, values and constitution. Quote those exactly and cite them. Only draft when nothing exists, and mark the draft *To decide*. Confirm the organisation's exact name and primary colour with the person if any source disagrees.

### Stage B: fill the content model
Work through `references/content-model.md` chapter by chapter. For each required item:
- **Sourced:** write it with its source in mind, and keep its wording where the source is the brand's own copy.
- **Derivable:** a rule that follows directly from locked decisions, such as a contrast table from tokens or a minimum size from logo detail. Write it and mark it *recommendation* in the page footer.
- **Missing:** do not invent it. Add a short "To decide" note on the page saying what is needed and who decides, and list it in `BRAND-BOOK-GAPS.md`. Examples are print colour values (CMYK, Pantone), a sound identity, icons, photography of real members and partner lockups.

Never invent facts, quotes, member numbers, partners or results. Dos and don'ts may use invented *sample* copy, labelled as examples.

### Stage C: make every page answer a question
Each page follows the page anatomy in `references/content-model.md`: purpose line, the rule, the specimen, dos and don'ts, why, and the source or status. Specimens are real: actual swatches with values and contrast results, real type at real sizes, the real logo on real grounds, real images, and screenshots of real applications.

### Stage D: build
- One HTML document with a persistent chapter index: a sidebar on desktop and a menu on phones. Each chapter has a stable `#anchor` so people can link straight to "#logo-clear-space".
- Copy buttons for colour values and token names. Show values as text that can be selected too, since a copy button can fail.
- Downloads: link the real files (SVG logos, a tokens CSS file, font links). Never a link to nothing.
- Apply the brand's v1 baseline (cursor, scrollbar, hover gesture). Plan one signature moment that comes from the brand's idea, such as a cover that performs the brand's core sign.
- **Applications are always built with `supermock`.** Every brand book's Applications chapter opens with an "In the world" page of moving mockups made by the `supermock` skill. These are:
  - the real site captured on a laptop and a phone;
  - at least one out-of-home placement pinned into a real, credited photograph from the brand's own region;
  - animated display ads (MPU, half page, leaderboard);
  - a showreel.

  Ship them as MP4s with posters, muted, looping and played only on screen. Label placements as concepts, and credit the photographs. Static photos of kit and print sit below them.
- **Templates are part of the book.** Render social templates at each platform's exact size: X header, LinkedIn cover, Facebook cover, YouTube banner (with its 1546×423 safe area), a 4:5 post per content type, and a story. Use a script, so a token change re-renders them all. Ship the PNGs and editable sources, and note each safe area on its page.
- **Image tiles: fill on the focal point first** (Plan A, `object-fit: cover` with a per-image `object-position`, checked by eye; `detail-craft/scripts/focus.py` suggests a crop). **Matte only when cropping would lose what matters** (Plan B, `detail-craft/assets/matte.js`): text, a whole object or a template. Transparent cut-outs keep the ground.
- **Both themes.** If the brand has a dark mode, the book follows it, using the brand's role tokens and Light/Dark switch. **Specimens never follow the theme.** Swatches, scheme cards, contrast rows, logo tiles, clear-space and lockup examples use literal colours, so they always show the real thing.
- **The Iconography chapter comes from the `iconography` skill:** its need-test results, style specification, set, motifs and specimen. If the skill hasn't been run for the brand, run it first.
- Drop any chapter the person rules out (for example sound) rather than leaving it as a gap.
- Keep it light and printable in spirit. No moment may hide a rule behind motion.

### Stage E: check
- Run `lint.mjs` and `inspect.mjs` from `design-taste-frontend`. Justify every allow.
- Content checks:
  - every chapter in the model is present or listed as a gap;
  - every colour pairing shown as text-safe passes WCAG;
  - every image is credited;
  - every download resolves;
  - no fact appears that the sources do not hold.
- Review screenshots at desktop and phone width before reporting.

### Stage F: report
Summarise what the book covers, list the gaps with who decides each, and give the link. Write the six-register rationale only for the book's signature moment and baseline details. The identity's own rationale already lives in `DESIGN-RATIONALE-DETAILS.md`; link to it, don't repeat it.

## Guardrails
- The book documents decisions; it does not make new brand decisions silently. A new rule the book needs is either a *recommendation* (derivable) or a *gap* (needs a decision).
- Archival and documentary images are shown at full definition and credited. Never re-render them for effect.
- Keep the voice section practical: principles with do/don't sentence pairs, a word list and real microcopy. Avoid lists of adjectives.
