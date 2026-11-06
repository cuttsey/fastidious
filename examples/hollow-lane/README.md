# Hollow Lane: a worked example

Hollow Lane is an invented Somerset cider maker, made to prove Fastidious end to end in a trade unlike any of the exemplars. Nothing here is for sale, and the finished page says so.

It exercises the newest parts of the stack together:

- **`copy-director`** wrote every line from the positioning and the beats. `COPY-DECK.md` passes `copy_lint.py` with no failures and no warnings.
- **`world-bible`** chose the world (a hand-made tabletop diorama of one orchard and its lane, lit by a low sun from the left), staged the claims as acts in it, with one russet apple carried from tree to glass, and ran two rounds of the series critic. `SERIES-REVIEW.md` records what it caught: the apple leaving the frame, the press standing in the barn's shadow, a striped chalk tally, and two false alarms on light direction.
- **`type-director` and `colour-director`** chose the type and palette by lookup, not memory: the Fell types with Source Serif 4, set against Wada's combination 243, with a cool slate as the counterweight to the warm orchard. `TYPE-AND-COLOUR.md` records the search, the specimens and the checks.
- **`render-engineer`'s scroll film** plays the six scenes on one WebGL canvas, scrubbed by the native scroll position, through an iris, a grain dissolve and a push, with posters and copy in the HTML for reduced motion and for browsers without WebGL.

The imagery is rendered in code with Blender, so the whole world rebuilds from `3d/build_world.py`. No image or video model was used.

## Files

| Path | What it is |
| --- | --- |
| `BRIEF.md` | The frame, the positioning and a summary of the sign system |
| `COPY-DECK.md` | Every line by key, with its evidence |
| `WORLD-BIBLE.md` | The world, its palette, light, lens, cast, devices and scene cards |
| `SERIES-REVIEW.md` | Two rounds of the series critic |
| `TYPE-AND-COLOUR.md` | How the typefaces and palette were found and checked |
| `type/` | Two rounds of pairing specimens |
| `colour/` | The palette tokens and its contrast sheet |
| `3d/build_world.py`, `3d/render.sh` | The world in code, and the render and sequence steps |
| `site/` | The page, the kit and the frame sequences (about 2.5 MB) |
| `qa/` | Contact sheets: the series, the page at desktop and phone widths, and the fallbacks |

## Run it

Serve `site/` with any static server, for example `python3 -m http.server -d site`, and open it in a browser. To rebuild the frames, install Blender as a Python module (`pip install bpy`) and run `3d/render.sh`; on two CPU cores it takes about forty minutes.
