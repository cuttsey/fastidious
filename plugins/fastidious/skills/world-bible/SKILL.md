---
name: world-bible
description: Builds one consistent pictorial world for a project (period or medium, palette, light, lens, materials, cast, props and overlaid devices), stages the idea as a sequence of scenes in that world, and runs a series critic so every generated or commissioned image and film reads as one world and one story. Produces WORLD-BIBLE.md and a scene list. Use when a site, film or brand book needs illustration, painting, photography or footage made as a series rather than one image at a time.
---

# World bible

A single generated image can look extraordinary. Fifteen of them almost never look like one place. The light swings from scene to scene, the faces change, the palette drifts, one frame turns glossy and another flat, and the series reads as a mood board instead of a world. Viewers notice the drift before they can name it, and it is the quickest way for generated imagery to look generated.

The best sites in the exemplar set avoid this by direction, not by tool. pear.no stages its whole offer as labours in one Renaissance world: the same fresco blue, the same warm side light, the same cast and materials in every scene, with a few modern devices laid over it, each with a job. Film and animation studios have long done the same with a bible: one document that fixes the world before anything is drawn, so every artist and every shot obeys it.

This skill writes that bible, turns the idea into scenes inside it, and then judges the whole series as a series. It does not render anything. `fastidious-motion` (motion-director, shot-writer, frame-critic) and `asset-director` make the images and films; `render-engineer` plays them in the page.

## Where it sits in the pipeline

- **Runs:** in phase 4, after `SIGN-SYSTEM.md` and `BRAND-SYSTEM.md` are locked and alongside `reference-curator`, whenever the work needs a series of pictures. Re-run the series critic every time new imagery arrives.
- **Reads:** `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md` (myth, signature signs, Imagery channel), `BRAND-SYSTEM.md` (palette and type), `BEAT-MAP.md`, `COPY-DECK.md` (the claim each scene carries), and the person's `REFERENCES.md`.
- **Writes:** `WORLD-BIBLE.md` from `templates/WORLD-BIBLE.md`, and `SERIES-REVIEW.md` after each critique.
- **Hands to:** motion-director's `brief.json` (look, light, palette, never list) and shot-writer's shot list (one shot per scene card), `asset-director` (the brief every asset is checked against), `render-engineer` (scene lengths, frame counts, transitions), `detail-craft` (the overlaid devices), `copy-director` (which line lands on which scene), and `frame-critic` (the bible is its continuity reference).

## Working rules

1. **The world comes from the meaning.** Choose a world because it signifies the sign system's myth, never because it is fashionable. A world you cannot justify in one sentence from `SIGN-SYSTEM.md` is decoration.
2. **One world, a few devices.** Everything in the pictures belongs to the world. Anything from outside it (a modern instrument in an old painting, print dots over a sky) is a named device with one job, used the same way every time.
3. **Variants, then lock.** Offer three worlds that differ in kind (period, medium, register), with one key frame each. The person chooses. Record it with `option-ledger`.
4. **Anchor frames first.** Make and lock three anchor frames (opening, middle, close) before any other scene. Every later prompt and every critique refers to them.
5. **Rights and respect.** Reference public-domain works and traditions, the person's own references, or licensed material. Never prompt with a living artist's name or imitate one recognisable living style. Never depict a real person, a real brand's marks or a sacred image used as decoration. Record the source of every reference.
6. **Honest about making.** Record whether each image is generated, commissioned, photographed or licensed. Never present generated work as photography of real events, places or people.
7. **Write plainly.** British English, sentence case headings.

## Stage 1: Choose the world

From the myth and the native signs in `SIGN-SYSTEM.md`, list five to eight candidate worlds. A world is a period or tradition plus a medium: Dutch still life in oil, a 1950s railway poster, a botanical plate in watercolour, Ukiyo-e woodblock, an expedition photograph on glass plate, a cutaway engineering drawing, a stop-motion set in felt. For each, write what it signifies and why that fits the work.

Shortlist three that differ in kind. For each, write a one-paragraph sketch and generate or source one key frame (a hero scene) through the fastidious-motion pipeline, using a short provisional bible. Present the three side by side. The person chooses one.

## Stage 2: Stage the idea as scenes

Turn the beats and claims into a sequence of actions inside the world. The method comes from allegory, where an abstract idea is shown as figures doing something (Ripa, 1593), and from Panofsky's three levels of reading an image (1939); `references/allegory.md` has the working method.

- **One claim, one action.** Each scene shows the claim from `COPY-DECK.md` as a visible act a stranger can describe without the caption: grafting, gilding, hauling, measuring, pouring, mending.
- **The cast does the work.** Figures act; they do not pose. Give each recurring figure a fixed description and job.
- **A visible through-line.** One object or process carries across the scenes and changes state: a seed becomes a tree, a block becomes a statue, a map fills in. The close should answer the opening.
- **Read at three levels.** What is literally shown, what it conventionally means, and what it says about this business. Each scene must work at the first level for anyone, and at the third for the person the work is for.

Write a scene card for every scene (the template is in `WORLD-BIBLE.md`): the claim and copy key, the action, cast, props, place, light, lens, composition and type space, the device used if any, the medium (still, film or frame sequence), its length or frame count, and the transition in and out.

## Stage 3: Write the bible

Fill every section of `templates/WORLD-BIBLE.md`. Be concrete enough that two different people, or two different models, would make the same choice.

- **World and medium**, with three to five public-domain reference works, each with its collection and link, and what to take from it.
- **Palette:** five to eight colours in hex with roles and rough proportions, taken from `BRAND-SYSTEM.md` where they overlap, plus what is never used. Gold, for example, can be reserved for the thing that gains value.
- **Light:** direction, height, time of day, colour temperature, hardness, falloff, and where shadows fall. One light for the whole world unless a scene's meaning needs another, and then say why.
- **Lens and camera:** focal length range, camera height, depth of field, and the one or two camera moves allowed in film.
- **Surface and material:** how paint, paper, grain or film stock should look up close, and how each material renders (marble, timber, velvet, bronze).
- **Cast:** each figure with age, build, hair, dress, colour and role, written to be repeated verbatim in prompts. No real people.
- **Props and places:** each with its look and period.
- **Devices:** each overlaid device, what it looks like, its one job and where it may appear.
- **Type space:** where text sits in each kind of composition, and the calm areas that must stay clear.
- **Never:** the anachronisms, looks and tells that break the world (see `references/generated-tells.md`).
- **Prompt core:** the fixed paragraph every prompt starts with, assembled from the sections above, and the negative list.

## Stage 4: Anchor, then make the series

1. Make the three anchor frames with motion-director and shot-writer, using the prompt core. Critique them with frame-critic and Stage 5's checks. Lock them, and keep them in `world/anchors/`.
2. Make every other scene with the prompt core and the anchors as image references where the provider allows. One scene at a time, three options each, the critic choosing.
3. For film and frame sequences, hand render-engineer the scene lengths, frame counts and transitions from the scene cards, and keep the motion rules from the bible (one move per shot, eased, ending where the card says).

## Stage 5: The series critic

Judge the series as a series, not frame by frame. Run it as a clean-context subagent that has seen only `WORLD-BIBLE.md`, the scene cards, the anchors and the images.

1. **Measure:** `python3 scripts/series_check.py world/ --bible WORLD-BIBLE.md --sheet world/series-sheet.jpg`. For every image or film it reports the share of coloured pixels on the bible's palette, key (mean lightness), contrast, colourfulness, warmth and which side is brighter. It sorts findings into two kinds: **breaks the bible** (palette share under the minimum, or the bright side opposite the bible's light), which fail the check, and **look at full size** (a scene far from the series median), which may be a deliberate change of scene or drift. The brighter-side reading is a rough proxy, since composition also moves it, so confirm light by eye. It also writes a contact sheet in scene order, and needs `ffmpeg`.
2. **Look:** open the contact sheet and every flagged image at full size.
3. **Check each scene** against the bible: world and medium, palette, light, lens, materials, cast continuity (same faces, dress and hands across scenes), props and period, the device used correctly, type space clear, and every tell in `references/generated-tells.md`.
4. **Check the story:** cover the copy and read the contact sheet in order. Can a stranger tell what happens, and does the close answer the opening? Does each scene show its claim?
5. **Decide per scene,** using frame-critic's rule: pick, edit (one local fix, "nothing else"), or rewrite. Never keep the least bad option. When one scene drifts, fix that scene; when several drift the same way, fix the bible or the prompt core and remake from the anchors.

Write `SERIES-REVIEW.md`: the metrics table, the verdict for each scene with its reason, story findings, and the changes to the bible if any.

## The tests

- **One-world test:** shuffle the contact sheet; every frame still belongs to the same place, period and light.
- **Story test:** with the copy hidden, a stranger can retell the sequence.
- **Swap test:** the world could not be moved unchanged onto a competitor's site, because it is built from this subject's meaning.
- **Tells test:** no frame shows a tell from the list at full size.
- **Rights test:** every reference has a source, and nothing imitates a living artist, a real person or another brand.

## Anti-patterns

- A different style for every section, "to keep it interesting".
- A world chosen for fashion, with no line back to the sign system.
- Prompts written fresh for each scene instead of from the prompt core.
- Judging each frame alone and never the series.
- Decorative figures who pose instead of acting.
- Devices used once, or used for no job.
- Text set over the busiest part of a picture.

## Files

- `templates/WORLD-BIBLE.md`: the bible, with the scene card.
- `references/allegory.md`: staging an idea as actions, and reading an image at three levels.
- `references/generated-tells.md`: what makes a series look generated, and the fixes.
- `scripts/series_check.py`: the series metrics and contact sheet (Python 3 standard library and `ffmpeg`).

## References

- Block, B. (2008) *The Visual Story: Creating the Visual Structure of Film, TV and Digital Media*. 2nd edn. Burlington, MA: Focal Press.
- Gombrich, E. H. (1960) *Art and Illusion: A Study in the Psychology of Pictorial Representation*. London: Phaidon.
- Kress, G. and van Leeuwen, T. (2021) *Reading Images: The Grammar of Visual Design*. 3rd edn. London: Routledge.
- Panofsky, E. (1939) *Studies in Iconology: Humanistic Themes in the Art of the Renaissance*. New York: Oxford University Press.
- Ripa, C. (1593) *Iconologia*. Rome.
