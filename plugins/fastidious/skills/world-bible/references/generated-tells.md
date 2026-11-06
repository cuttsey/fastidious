# Generated tells

The signs that make a series of images read as generated, and what fixes each. The series critic checks every scene for all of them at full size.

## Within a frame

| Tell | What it looks like | Fix |
| --- | --- | --- |
| Hands and feet | Extra or fused fingers, a thumb on the wrong side, a hand that grips nothing | Re-crop so hands are out of frame or simple; regenerate the region; specify the grip in the prompt |
| Pseudo-text | Letter-like marks on signs, books, labels or plans | Ask for blank surfaces; set any real text in post from `BRAND-SYSTEM.md` |
| Plastic sheen | Skin, fabric and stone all with the same soft gloss | Name each material and its finish; describe the paint or film surface; lower "detail" language |
| Melted geometry | Columns, tools, scaffolding or ladders that bend, merge or end in nothing | Simplify the structure; regenerate with the structure described step by step |
| Everything lit | Fill light from every side, no real shadow | State one light, its direction and its falloff; ask for shadows to fall in a named direction |
| Fake depth | Uniform background blur at any focal length | Specify lens and aperture from the bible; prefer deep focus for painted worlds |
| Doubled objects | Two of an object that should be unique (two suns, two hero props) | Name the object as singular and its position |
| Symmetry by default | Centred subject, mirrored composition | Place the subject on the bible's composition rules; reserve the type space |
| Teal and orange | Cinematic grade the world does not have | State the palette; run the palette check |
| Over-detail | Every surface busy at the same level | Ask for areas of rest; a painter leaves passages loose |
| Faces | The same face on everyone, or a face that changes between scenes | Fixed cast descriptions; anchor frames as references; fix faces before anything else |

## Across a series

| Tell | What it looks like | Fix |
| --- | --- | --- |
| Light swings | Sun from the left in one scene, the right in the next | One light in the bible; the series check reports which side the light falls from |
| Palette drift | Scenes warming or cooling over the sequence | Prompt core with hex roles; the series check flags outliers |
| Key and contrast drift | One scene murky, the next bright and flat | Target key and contrast in the bible; regrade or remake outliers |
| Medium drift | One scene oil, the next watercolour, the next a render | Name the medium and surface in the prompt core, first, every time |
| Costume and prop drift | The cast's dress, colour or props changing between scenes | Fixed descriptions copied verbatim; anchors as references |
| Scale drift | The hero object changing size without meaning | Note the object's scale on every scene card |
| Device drift | An overlaid device used differently in each scene | One job and one look per device, written in the bible |

## In film

| Tell | Fix |
| --- | --- |
| Morphing between frames, objects changing identity | Shorter clips, one move, a stronger start frame; reject the take |
| Two camera moves in one shot | One move per shot, written in the motion prompt |
| Floating, weightless motion | Name the physical cause: wind, a hand, gravity; ease in and out |
| Flicker in texture or light | Lower motion strength; regenerate; never fix by blurring |

The rule from frame-critic stands: never keep the least bad option. A scene that shows a tell at full size is edited or rewritten.
