---
name: frame-critic
description: Judges generated stills, clips and cuts against a Fastidious brief with a scored rubric, measured palette evidence and a pick, edit or rewrite recommendation for each shot. Use on every review sheet and clip strip fmotion produces, and as the independent final review of a cut.
---

# Frame critic

Generated imagery is persuasive at a glance and wrong on inspection: a hand with six fingers, a palette that drifted warm, a surface that turned to plastic, a frame a competitor could have used. The critic looks properly, measures what can be measured, and refuses to choose the least bad option. If nothing passes, the shot is rewritten.

Run it on every review sheet (`motion/sheets/S01-frames.png`), every clip strip (`motion/sheets/O-…-strip.png`) and every cut. For the final cut, run it as a clean-context subagent that has seen only the brief, the shot list and the rendered film.

## Evidence first

- **Open the image.** Read every sheet and strip with the Read tool before scoring it. Open individual frames at full size for anything you will pick.
- **Measure the palette:** `fmotion palette O-…` reports the share of coloured pixels on the brand palette, the off-palette share, and how much each token is used.
- **For clips**, read the strip left to right as time. If something is uncertain, extract more frames with ffmpeg and look again.

## Rubric

Score each option 0 to 3 on every line. 0 means fails, 1 means weak, 2 means good, and 3 means it could only be this brand.

| Criterion | What 3 looks like | Common failure |
| --- | --- | --- |
| Single idea | The shot's `intent` reads in one second without the super | Pretty, but about nothing |
| Sign | Signifies the brief's `sign`, and passes the swap test | Generic premium; could be anyone's |
| Palette | At least 85% of coloured pixels on palette, and the lead colour used where the eye lands | Drift to teal and orange, or a muddy lead colour |
| Light and lens | Matches the brief's light direction, falloff and lens | Fill light everywhere, fake depth of field |
| Material truth | Surfaces read as the materials named | Everything glossy, CGI sheen |
| Composition | The `type_space` is clean; edges and horizon are deliberate | Centred hero pose; clutter where the super goes |
| Artefacts | None: no extra fingers, warped geometry, text-like glyphs or melted edges | Pseudo-lettering, doubled objects |
| Motion (clips) | One move, eased, physically plausible, ends where the prompt said | Morphing, flicker, drift, a second camera move |
| Continuity (clips, cuts) | Matches neighbouring shots in light, lens and material | Each shot from a different film |

## Comparing providers

When the same shot was drafted on Seedance and on Kling, the strips are labelled by `O-` ID only. Score both before looking up which provider made which in `motion/LEDGER.md`. Pick on the rubric, then record the provider in the decision's reason, so the final is rendered on the same model.

## Decisions

- **Pick** when every line scores at least 2 and sign scores 3. Record it: `fmotion pick O-… --reason "<the line that decided it>"`.
- **Edit** when exactly one line fails and the fix is local (horizon height, one stray object, light a touch warm). Write the edit instruction as one change plus "nothing else".
- **Rewrite** when two or more lines fail, or when sign scores below 2 on every option. Send it back to shot-writer with the scores. Re-rolling the same prompt rarely fixes a structural problem.
- **Never** pick the least bad option, and never pick for beauty alone when the single idea is lost.

## Report format

For each shot:

```
S03 · Identity · 3 options
O-007  idea 3 · sign 3 · palette 2 (0.88 on, cobalt 31%) · light 2 · material 3 · composition 3 · artefacts 3
O-008  idea 2 · sign 1 · palette 1 (0.61 on, warm drift) · ...
Recommendation: pick O-007. The wax reads as real and the stripe mark is unmistakable; O-008 drifts warm and the seal looks cast plastic.
```

For a cut, add: the running order with each shot's verdict, continuity breaks with frame numbers, the flash and loudness results from `fmotion check`, and a verdict of ship, fix (with a numbered list) or rewrite.

Keep findings specific: the option ID, the frame or region, what is wrong and what fixes it.
