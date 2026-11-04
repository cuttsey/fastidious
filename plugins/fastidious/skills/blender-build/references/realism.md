# Realism checklist

Look at every Cycles still at 100% and check for these tells. Each has a usual fix.

| Tell | Why it reads as CG | Fix |
|---|---|---|
| Plastic sheen | Roughness too low and too even | Raise base roughness; vary it with the colour noise; lower only where it's polished (grips, edges) |
| Uniform colour | One noise scale, or colour varying without roughness and relief | Three scales (figure, patches, fibre) driving colour, roughness and bump together |
| Perfect edges | Real edges are rounded and worn | Bevel or dome every end; lighten or darken worn edges |
| Perfect form | Turned or modelled with no error | Taper, bend, out-of-round, knots; nothing exactly straight or symmetrical |
| Floating | No contact shadow | Rest on z = 0 with the shadow-catcher floor; check the shadow under the contact point |
| Wrong texture scale | Grain or pores too big for the object's real size | Model in metres; tune noise scales against a real photo at the same framing |
| Flat light | One light or none | HDRI for reflections plus warm key, cool fill and a rim |
| Over-sharp everywhere | Real lenses have depth of field | f/2.8–5.6 on close-ups, focus on the detail that matters |
| Clean everywhere | Nothing in use is clean | Dents, scuffs, hand-darkening, dust in recesses, at very low strength |

## Capturing a real object (photogrammetry)

When the object exists (the Society's own cudgels, jackets, trophies, a carved boss), capture it rather than model it:

1. **Shoot** 60–150 photos in soft, even light (overcast or a light tent), the object on a turntable or walked around in
   three height rings, 60–80% overlap, nothing shiny (dust with matte spray only if the owner agrees), no background clutter.
2. **Reconstruct** with RealityScan (mobile or desktop), Apple's Object Capture (macOS `PhotogrammetrySession`, via
   Reality Composer or a small Swift tool), or Meshroom (open source).
3. **Clean** in Blender: decimate to a web budget, bake the high-resolution detail into a normal map, check scale in metres.
4. **Light and render** it with this skill's studio: write a tiny builder that imports the mesh (`bpy.ops.wm.obj_import`
   or `bpy.ops.import_scene.gltf`) and returns the object, and set `"material": {"type": "keep"}` to
   use the scan's own textures.

A captured object keeps its real definition, unlike splats or AI reconstructions, which soften detail.

## AI image-to-3D

Useful for drafts and organic shapes (Rodin, Meshy, Tripo; open models such as TRELLIS, Hunyuan3D). Expect messy
topology and baked-in lighting in the textures; check licence terms. Never present an AI reconstruction as a real
artefact.

## Getting a model through a strict sandbox

An Artifact's security policy can refuse `fetch()` of `data:` URIs and `blob:` image fetches, and three.js's GLTFLoader uses both. The page then falls back silently. Test locally with a CSP meta tag (`connect-src 'self'; img-src 'self' data: blob:`) before publishing. To pass: fetch the embedded glTF JSON yourself, decode the buffer, rebuild a GLB in memory and call `loader.parse()`; use a parser plugin to swap in `THREE.TextureLoader`, which loads through `<img>`. Bundle everything into one classic script (esbuild `--format=iife`) so nothing depends on import maps or modules. `tools/cudgel.src.js` in the DWS project is the worked example.
