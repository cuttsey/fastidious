---
name: blender-build
description: Build complex, realistic 3D objects with real-looking materials, scripted in Blender (headless, Python) so every model is reproducible from a spec. Produces transparent studio stills composited on the brand ground, turntable MP4s, image sequences for scroll scenes, and compressed glTF/GLB with baked PBR textures for the web. Use when someone wants a 3D object, product render, hero model, turntable, "make it 3D", a realistic render of an object from the brand's world, or a glTF for three.js. Pairs with detail-craft (3D routes A, B, C) and supermock.
---

# blender-build

Realism comes from four things, in order: **light, materials, imperfection, camera.** Geometry matters less than people
think; a simple shape with honest light and a material that varies the way real material varies reads as real. A perfect
shape with flat colour reads as a render.

The method is **code first**: every object is a Python builder plus a JSON spec, run headless by Blender. Nothing is
hand-edited in a `.blend`, so "make it darker" or "shorter, with more knots" is a one-line change and a re-run, and the
same spec makes the stills, the turntable and the web model.

## Where it sits
- **Reads:** `DETAIL-PLAN.md` (which 3D route the moment uses), `BRAND-SYSTEM.md` (grounds, palette), the subject's real
  reference photographs.
- **Writes:** in the project, `3d/<name>.json` (the spec) and `3d/out/`: `<name>-<shot>.png` (transparent),
  `<name>-<shot>-ground.jpg` (on the brand ground), `<name>-turntable.mp4` and its frames, `<name>.glb` and its baked maps,
  `<name>-report.json`.
- **Feeds:** detail-craft Route A (frame sequence on a canvas), Routes B and C (GLB in three.js), supermock (stills and
  turntables as presentation clips), brand books (object renders).

## Tools
| File | Does |
|---|---|
| `scripts/blender.sh <spec.json> [--preview\|--draft] [--only stills,turntable,glb] [--shot name]` | Runs a spec headless. `--shot` renders one named still. `--preview`: EEVEE, half size, seconds, composition only. `--draft`: Cycles, half size, 32 samples, for judging materials and shadows. Neither: full render. |
| `scripts/run.py` | The runner inside Blender: builds the object, material, studio, then each output. |
| `scripts/polyhaven.py search <words> --type hdris\|textures` and `get <id> --res 1k` | Fetches CC0 HDRIs and PBR texture sets into `cache/polyhaven/<id>/` with a `credit.json`. |
| `lib/studio.py` | AgX colour, HDRI world, three area lights, shadow-catcher floor, cameras with depth of field, transparent renders, brand-ground compositing (ffmpeg), turntables. |
| `lib/materials.py` | `wood_stick` (procedural: grain, fibres, knots, end grain, polished grip, oiled coat) and `pbr` (image maps by Poly Haven/ambientCG names). Add new procedural materials here. |
| `lib/export.py` | Bakes base colour, roughness and normal to the builder's UVs, exports GLB (Draco, WebP where supported). |
| `objects/*.py` | Builders: `build(params) -> object`. `cudgel.py` is the worked example. |

Requires Blender 4.2+ (AgX, Principled v2) and ffmpeg. Blender is found at `/Applications/Blender.app` or `$BLENDER`.

## The method

### 1. Choose the route from what the object must do
| The object must… | Make |
|---|---|
| look its best in one or a few frames (hero, brand book, case study) | stills, Cycles |
| perform a change on scroll (turn, open, assemble) | an image sequence (detail-craft Route A): the turntable output or keyed frames, 120–200 frames, WebP |
| be handled by the visitor (spin, inspect) | GLB with baked maps (Routes B/C), under ~3 MB |
| be a real object the Society owns | **capture it** (photogrammetry, see `references/realism.md`), then use this skill's studio to light and render it |

### 2. Gather references, then write the builder
Look at real photographs of the object before modelling: proportions, how it wears, where it's darker, how the ends
look. Write down measurements in real units (metres). A builder:
- makes geometry with **real dimensions** and **no perfect symmetry**: taper, bend, out-of-round, bumps, worn edges;
- writes **per-vertex attributes** the material reads (where it's worn, knotted, cut, painted);
- writes **UVs that bake cleanly** (no overlaps; a texel density roughly even), so the GLB matches the render;
- rests the object on z = 0, its long axis along +X.

### 3. Material: variation at three scales
Every believable surface varies at a **large** scale (figure, staining, fading), a **middle** scale (knots, patches,
wear zones) and a **fine** scale (fibres, pores, scratches) in colour, roughness and relief together. A material that varies
in only one channel or one scale looks synthetic. Use a CC0 scan (`pbr`) when the material is a common surface; use a
procedural one when it must follow the object's own form (grain along a stick, wear on a grip).

### 4. Light and camera
- An **HDRI** for reflections (Poly Haven studio HDRIs: `studio_small_09`, `photo_studio_01`), at 0.4–0.7 strength,
  plus the three area lights. Warm key, cool fill, a rim to separate the edge.
- **Real lenses:** 50–60 mm for the whole object, 85–135 mm for details, depth of field at f/2.8–5.6 on details only.
- Render transparent; composite onto the brand ground. The shadow travels with the object.

### 5. Check, then render properly
1. `--preview` for composition (seconds).
2. `--draft` for materials and light; **look at it** at 100% for the tells in `references/realism.md` (plastic sheen, uniform colour,
   perfect edges, floating, wrong scale of texture). Fix the spec, re-run.
3. Then the full set: stills (96–128 samples), turntable (40 samples), GLB.
4. Check the GLB: size, texture count, and load it in `assets/glb-viewer.html` (copy it beside the file and serve it; `window.RESULT` reports vertices and maps) before handing it on.

## What procedural materials can and can't do
A procedural material follows the object's form and holds up at whole-object framing. In close-up (the object filling the frame) the denoiser smooths fine fibres into streaks and it stops passing as a photograph. For any close-up, blend in a scanned CC0 texture (`pbr`) or capture the real object. Tested on the cudgel: the hero and the end grain pass, the grip close-up doesn't.

Long thin objects also make weak turntables: most of the frame stays empty. Prefer a slow push along the object or a turn about its own axis, framed tight.

## Publishing as an Artifact
Artifacts don't serve `.glb`. Convert to embedded glTF JSON (`<name>.gltf.json`, buffer as a base64 data URI, about a third larger before gzip). GLTFLoader reads it the same way. Don't use Draco there: its decoder needs wasm or a large JS file. Bundle three.js into one classic script, and test against a strict CSP first: see the sandbox section of `references/realism.md`.

## Rules
- **Real objects only, honestly labelled.** A render of an object type ("a cudgel") is an illustration; never present it
  as a specific historical artefact, a photograph, or the Society's own object unless it was captured from that object.
- **Credit every HDRI and texture** from `credit.json` (CC0 needs no credit legally; give it anyway).
- **Keep archival images sharp.** Don't re-render archival photographs as 3D (see the user's feedback on splats).
- **Budgets:** GLB under ~3 MB, turntable MP4 under ~4 MB, image sequences 15–30 KB a frame.
- Machine notes: on Intel Macs Cycles runs on the CPU. A 1600×1000 still at 96 samples takes a few minutes; turntables
  run in the background (`run_in_background`) and are checked with a preview first.
