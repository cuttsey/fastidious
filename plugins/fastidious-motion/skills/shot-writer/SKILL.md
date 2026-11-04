---
name: shot-writer
description: Writes the shot list for generated film from a Fastidious brief, with one idea and one camera move per shot, prompts written as photographs and camera directions, and several deliberately different directions per shot. Use after motion-director's brief is approved, or when a generated shot needs rewriting rather than re-rolling.
---

# Shot writer

A model can only be as specific as the words it is given. Most weak generations come from prompts that describe a mood ("premium, innovative, cinematic") instead of a picture. This skill writes pictures: what is in the frame, where the light comes from, what the lens is doing, what moves and how the camera follows. The brand's palette, light, texture and avoid list are added to every prompt by `fmotion` from the brief, so shot prompts carry only what is specific to the shot.

## Inputs

`motion/brief.json` (approved), and `BEAT-MAP.md` if the film has one. If there is no beat map, write the beats first: an opening that states the tension, a middle that builds the case, and a close that resolves into the single idea.

## Per shot

Write each entry in `motion/shotlist.json` in this order.

1. **`intent`**: the one thing this shot says, in a sentence, and which beat it serves. If you cannot write it, the shot is not needed.
2. **`seconds`**: its length in the cut. **`clip_seconds`**: the generated length, between 4 and 15, at least one second longer than `seconds` so there are handles to cut on.
3. **`super`**: the line of type that will sit over it, if any, at most six words. Set `type_space` to where the frame must stay quiet for it ("in the left third", "above the horizon").
4. **`frame.prompt`**: the still, written like a photographer's shot note. Use this order: subject, its state, setting, light, lens and framing, material detail. Give concrete nouns and measurable relations ("a hairline sliver", "the right third", "at table height"), not adjectives of quality.
5. **`frame.directions`**: two to four genuinely different takes on the same intent. Vary one of angle, scale, light, time or what is in focus. Three wordings of the same idea do not count. At least one direction must be one the category would not normally choose. That is where distinction comes from.
6. **`motion.prompt`**: what changes during the clip and how it ends. One action. Describe its speed and its final state, because models drift when the end is open.
7. **`motion.camera`**: one move from the vocabulary below, or `locked`. Set `camera_fixed: true` when only the subject should move.
8. **`avoid`**: anything this shot is especially likely to produce and must not (a reflection of the crew in a polished surface; a second object appearing). Seedance reads it inside the prompt; Kling receives it as a separate negative prompt. Write each item as a plain noun phrase, so it works both ways.
9. **`motion.provider`**: leave it empty to use the film's default. Set `"seedance"` when the shot depends on reference images, `"kling"` when its avoid list is long and strict, or `"seedance,kling"` when it is the hardest shot in the film and worth drafting twice.

## Camera vocabulary

Use these terms exactly. They are the ones video models follow most reliably.

| Move | Use it for |
| --- | --- |
| locked | Letting the subject's own motion carry the shot |
| slow push in / slow pull back | Raising or releasing attention |
| dolly left / dolly right | Revealing alongside a surface |
| slow arc left / right around the subject | Showing an object as a form |
| tracking alongside | Staying with a moving subject at its speed |
| crane up / crane down | Changing scale or status |
| tilt up / tilt down | Following height, from detail to whole |
| rack focus from foreground to background | Moving the eye without moving the camera |

Avoid handheld, whip pans and orbits of more than a quarter turn. They show generation artefacts first.

## Writing for distinction

- **Swap test:** if a competitor's reel could use this frame unchanged, the shot is generic. Tie it to the brief's `sign` until it couldn't.
- **Concrete over impressive:** a brass compass needle settling is a stronger image of purpose than "a glowing path into the future".
- **Real materials:** paper, enamel, wax, planed wood, brass and glass read as made. Unspecified surfaces become glossy plastic.
- **Leave out the AI furniture:** particles, lens flares, holograms, neon, chrome, teal and orange, keyboards and robots. They are in the brief's `avoid` list for a reason; add to it, never remove from it.
- **No words in frame:** never ask for text, logos, numbers or interface copy. Type is set in post. Abstract marks (a stripe, a circle) are fine.

## Continuity

- Shots that cut into each other on a match: set `motion.end_frame` to `"next"`.
- An object that must stay identical across shots: after its still is picked, add that `O-` ID to `motion.references` on the later shots, and mention it in the motion prompt as `@Image1`.
- A sequence that should feel like one camera: keep the same lens wording and the same light direction, and leave `film.seed` fixed.

## Before handing back

Run `fmotion validate`. Then show the person a table of shot, intent, seconds, super and directions, with the total running time. The person approves it before frames are generated.

## Example

See `examples/fastidious-film/` in this plugin: a 30-second film telling designers why Fastidious exists, using objects and materials (a scalpel trimming a hairline from a printed edge, a compass needle settling, a seal pressed into wax, a plane taking one shaving, an object turned under one light, the one distinct object in a row) rather than screens, people or metaphors from the product's own promotion.
