# World bible: Hollow Lane

Status: locked · Updated: 2026-11-06 · Chosen in: D-002 · Anchors: world/anchors/

## World and medium

A hand-made tabletop diorama of one Somerset orchard and its lane, built from turned wood, felt and painted clay, photographed through a long lens on a dark walnut table. A diorama is how a museum or a model railway shows a place it loves; it signifies care, patience and a world small enough to know every tree, which is the myth.

Rendered in code with Blender (Cycles), so every scene is rebuilt from one file and nothing drifts between scenes.

| Reference | Collection and link | What to take | What to leave |
| --- | --- | --- | --- |
| Museum natural history dioramas (twentieth century) | Many public collections | A whole world on a base, seen from outside; one clear light | Painted backdrops and taxidermy |
| Model railway layouts | Hobby tradition | Felt grass, turned-wood trees, a lane that bends to fit the board | Railways, signage, branding |
| Dutch still life (seventeenth century) | Public-domain collections | One warm light from the left, dark ground, objects as characters | Excess and symbolism of death |

## Palette

| Role | Hex | Share of the picture | Notes |
| --- | --- | --- | --- |
| Felt grass | #78873f | about 35% | Slightly varied, matt, with sheen at grazing light |
| Shadowed felt | #5c6e30 | | Canopies and shade |
| Felt in raking light | #8f876a | | Measured from the locked anchor S01: the sheen greys the felt where the sun grazes it |
| Felt in full light | #6f6e3a | | Measured from S02 and S06 |
| Lane | #d9c499 | about 8% | The route; always the lightest warm area |
| Oak | #8a6138 | about 12% | Barrels, crate, press, base |
| Dark oak and walnut | #4d331f | | Doors, trays, the table |
| Cream | #f0e6d1 | | The barn; the page's paper |
| Slate ink | #2b2621 | about 20% | Roof, studio dark, type |
| Apple red | #b5422a | small | Every apple but one |
| Russet | #a86b2b | smallest | The one russet apple: the through-line |
| Straw | #e0cc94 | | Press cheeses |
| Cider gold | #c99a3b | smallest | Only in the glass and the juice |

Never: neon or saturated blues, teal and orange grading, pure black, pure white.

## Light

- Direction: from the left
- Height and time: low autumn sun, about 18 degrees above the table, late afternoon
- Colour temperature: warm, a little under 4,000 K; the studio fill is dim and warm
- Hardness and falloff: crisp shadows (sun angle 3 degrees), long shadows across the felt
- Key and contrast: low to mid key; the lane and the cream barn catch the light, the studio falls to dark
- Exceptions: none

## Lens and camera

- Focal length: 70 to 105 mm
- Camera height: from model eye level (a few centimetres) to a quarter view over the base
- Depth of field: shallow at close range; this is the miniature's own signature, so it is allowed here
- Film moves allowed: one slow push, arc or rise per scene, eased in and out

## Surface and material

- Surface up close: felt fibre, turned wood grain, satin paint; nothing glossy except the glass
- Felt: matt, with a soft sheen where the sun grazes it
- Wood: satin oak, darker in the grain
- Glass: green bottle glass and a clear tumbler, the only reflective surfaces

## Cast

No people and no hands. The cast is the objects, and one carries the story.

| Figure | Description | Role in the story |
| --- | --- | --- |
| The russet apple | Golden-brown with a russet bloom, larger than the red apples, always nearest the camera | Travels from the tree to the glass |
| The lane | Pale sand, an S that bends twice before it arrives | The long way round |
| The barrel with the tally | Oak, two iron bands, eleven chalk marks on its head | The only clock |

## Props and places

| Prop or place | Look and period | Appears in |
| --- | --- | --- |
| Orchard | Twelve turned-wood trees with felt canopies, red apples | S01, S02, S06 |
| Barn | Cream walls, slate roof, dark door | S01, S03, S04 |
| Press | Oak frame, iron screw, straw cheeses, a pool of juice, a cream jug | S03 |
| Barrels | Five oak barrels on their sides | S04 |
| Lane's end | An oak crate, a green bottle, a tumbler of cider, the russet apple | S05 |

## Devices

| Device | Look | Its one job | Where it may appear |
| --- | --- | --- | --- |
| Chalk tally | Four strokes and a slash, twice, then one | Time: the wait is counted, not hurried | S04, and as the page's progress mark |
| Drawn lane | A thin hand-drawn line on the page that follows the lane's S | The long way round: it draws as you scroll | The page's left margin |
| Film grain | Fine, warm, barely visible | Photographed, not rendered | Every scene |

## Type space

Text sits on the dark studio and table at the top left and bottom left of each frame, never over the felt or the lane. The subject sits right of centre.

## Never

- People, hands, faces or animals
- Text, labels or logos inside the pictures
- Plastic sheen on felt or wood
- A second light source or coloured light
- Any real brand's bottle, label or glass shape

## Prompt core

Not applicable: the world is built in code (`3d/build_world.py`). Its palette, light, lens and materials implement the sections above.

## Scenes

### S01: The lane

- Claim and copy key: the spine, hero.h1
- Act: the camera settles over the whole orchard as the lane bends twice
- Through-line object state: the russet apple on its tree, too small to see yet
- Medium: frame sequence, 24 frames
- Transition out: iris from the hero tree
- Reads as: a tiny orchard / a place made with care / a business that chose the slow route

### S02: Pick

- Claim and copy key: beat1.claim
- Act: the camera arcs to one tree where the russet apple hangs nearest
- Medium: frame sequence, 24 frames; develops into colour
- Transition out: grain dissolve

### S03: Press

- Claim and copy key: beat2.claim
- Act: a slow push to the press, its straw cheeses and the pool of juice
- Medium: frame sequence, 24 frames
- Transition out: push

### S04: Wait

- Claim and copy key: beat3.claim
- Act: the camera tracks along the barrels to the eleven chalk marks
- Medium: frame sequence, 24 frames
- Transition out: grain dissolve

### S05: Pour

- Claim and copy key: beat4.claim
- Act: the camera rises over the crate at the lane's end: bottle, glass, and the russet apple beside them
- Medium: frame sequence, 24 frames
- Transition out: iris

### S06: Close

- Claim and copy key: close
- Act: the camera pulls up and away until the whole lane is visible again
- Medium: frame sequence, 24 frames
- Reads as: the end answers the beginning

## Change log

| Date | Change | Why |
| --- | --- | --- |
| 2026-11-06 | Cameras for S03 to S05 pulled back; barrel tally made bolder; studio fill raised | First series review: press and pour too tight, tally unreadable |
| 2026-11-06 | S02 camera reframed to keep the russet apple in shot; tally slash moved off the strokes; press moved out of the barn's shadow; two measured felt tones added to the palette | Second series review (SERIES-REVIEW.md) |
