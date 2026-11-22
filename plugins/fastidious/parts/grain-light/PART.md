# grain-light

**Job.** Gives a flat section material depth (fine film grain and a soft light that drifts towards the visitor's pointer) without 3D and at almost no cost.

| Field | Value |
|---|---|
| Beat intents | `depth`, `rest` (safe on rest beats: it adds texture, not movement of content) |
| Rung | 1 (canvas tile drawn once, CSS transform) |
| Role | `supporting` |
| Cost band | Very low: 1.7 KB module, no dependencies |
| Licence | MIT (Fastidious, original), see `LICENSE` |

## Inputs

| Input | Default | Notes |
|---|---|---|
| `section` | required | The element to texture; it is never clipped (layers live in their own clipping box) |
| `grainOpacity` | `0.08` | Or CSS `--gl-grain-opacity`; 0.05 to 0.15 |
| `light` | `true` | The drifting light |
| `follow` | `0.06` | How quickly the light chases the pointer |
| `drift` | slow | Idle drift on touch screens |
| CSS `--gl-light-colour`, `--gl-light-size`, `--gl-light-opacity`, `--gl-light-blend`, `--gl-grain-blend` | | Blend modes are optional and cost more on weak devices |

## Cost (measured)

Clean-room example, headless Chrome with software rendering: 59.9 fps desktop, 60 fps mobile, 0 ms long tasks. An earlier version using an overlay blend mode measured 54.5 fps, so the default grain is an alpha tile with no blending. The light loop runs only while the section is on screen.

## Fallbacks

- **Reduced motion:** grain is static; the light does not move.
- **No JavaScript:** no texture; the section is unchanged.

## Provenance

- Original Fastidious part, built 22 November 2026 (intake run 003) from `WANTED.md`. Inspired by the grain and light shaders in premium prompt libraries, built from a written description only.
- Composition fix: the first version set `overflow: hidden` on its host, which clipped `travelling-object` in the composition test. Layers now sit in their own clipping box.
