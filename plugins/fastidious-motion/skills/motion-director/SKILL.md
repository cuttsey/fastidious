---
name: motion-director
description: Directs generated stills and film for a Fastidious project through image and video model APIs (gpt-image-2 for frames, Seedance 2.0 or Kling for motion). Turns Fastidious artefacts into a brief, runs styleframes, motion and review loops, and assembles a checked cut. Use when a brand film, launch reel, hero loop or campaign visual needs imagery that cannot be captured or built.
---

# Motion director

Image and video models will render almost anything, which is exactly the problem: given a thin prompt they render the average of everything they have seen. The result looks expensive and means nothing. Fastidious already does the hard part, deciding what the work is for, what it should signify and what it should never look like. This skill carries those decisions into every API call, then holds every output to them.

The division of labour is fixed: **Fastidious decides, the models render, the critic chooses.** No prompt is written before the brief exists, and no output is used because it is the least bad.

## What it needs

- The `fmotion` command line in this plugin (Python 3.9 or later, standard library only) and `ffmpeg`. Throughout these skills, `fmotion` means `python3 <plugin root>/bin/fmotion`, where the plugin root is two folders above this skill's base directory. Run it from the project root, so the workspace lands in `./motion`.
- `OPENAI_API_KEY` for stills, and for motion `ARK_API_KEY` (Seedance on BytePlus ModelArk), `KLING_API_KEY` (or `KLING_ACCESS_KEY` and `KLING_SECRET_KEY`), or both. Keys come only from the environment. Never write them into a file, a prompt or the ledger.
- The Fastidious artefacts for the project: `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md` and `REFERENCES.md`, and `BEAT-MAP.md` if the film has a narrative. When the work is a series in one world, `WORLD-BIBLE.md` (from the world-bible skill) supplies the look, light, palette, cast, never list and prompt core, and its scene cards become the shot list. If one is missing, run the Fastidious skill that makes it (frame-shifter, positioning-strategist, sign-system-architect, brand-system-architect, taste-library) or ask the person. Do not invent a brief to get started.

OpenAI's own video API (Sora 2) was shut down on 24 September 2026, so OpenAI is used for stills only. Model IDs change often: check `fmotion/config.py` against the provider's model list before the first paid run, and override with `FMOTION_IMAGE_MODEL`, `FMOTION_VIDEO_MODEL`, `FMOTION_KLING_MODEL` or `motion/config.json`.

## Who does what

| Need | Skill or tool |
| --- | --- |
| Why the film exists, who it is for, the single idea | frame-shifter, positioning-strategist, narrative-architect (Fastidious) |
| What it should signify; palette, light, type | sign-system-architect, brand-system-architect (Fastidious) |
| The person's own references, with R- numbers | taste-library, reference-curator (Fastidious) |
| Shots, frame prompts, motion prompts | shot-writer (this plugin) |
| Judging every still and clip | frame-critic (this plugin) |
| IDs for every option, pick and cut | `fmotion`, compatible with option-ledger |
| Type, supers and end cards | set in post from `BRAND-SYSTEM.md`, in showreel-director's HyperFrames composition or the build's own type; never by the model |
| Model and effort per step | model-switcher: `opus` for the brief, shot list and critique; `sonnet` or `haiku` to run the commands |

## Stage 1: Brief

Run `fmotion init` in the project root. It creates `motion/` with `brief.json` and `shotlist.json`. Fill `brief.json` field by field:

| Field | From |
| --- | --- |
| `purpose` | `FRAME.md`: the reframed problem, and why a film is the right answer |
| `audience` | `POSITIONING.md`: the one person, their pain, and what they do after watching |
| `single_idea` | `BEAT-MAP.md` or `POSITIONING.md`: one sentence the whole film defends |
| `sign` | `SIGN-SYSTEM.md`: what every frame should signify, in a few words |
| `tokens` | `BRAND-SYSTEM.md`: palette as hex, then light, lens, texture, composition and mood in words a cinematographer would use |
| `references` | `REFERENCES.md`: images saved into `motion/refs/`, each with what to borrow and what to reject |
| `avoid` | The template's list of AI clichés, plus anything the sign system rules out |

Then show the person the brief in one screen and get a yes. Everything downstream inherits it, so a wrong brief costs every later call.

## Stage 2: Shot list

Hand the brief to **shot-writer**. It writes `shotlist.json`: one idea and one camera move per shot, a still a photographer could take, two to four genuinely different directions per shot, and the space reserved for type. Run `fmotion validate`. It refuses shot lists that ask the model for words, give only one direction, or set clips outside Seedance's 4 to 15 seconds.

Show the shot list as a table (shot, intent, seconds, super, directions). The person approves it before anything is spent. Record the approval as a `D-` with option-ledger if the project uses it.

## Stage 3: Styleframes

Stills first, motion second. A video model animating an approved frame is far more controllable than one inventing a scene from text, and a still costs a fraction of a clip.

1. `fmotion frames` generates every direction for every shot at draft quality and writes one labelled review sheet per shot in `motion/sheets/`.
2. **frame-critic** reviews each sheet, with `fmotion palette O-…` for the colour evidence. It recommends pick, edit or rewrite for each shot.
3. Show the person the sheets with the critic's recommendation. They pick: `fmotion pick O-004 --reason "…"`.
4. Small fixes go through `fmotion edit O-004 "lower the horizon; nothing else"`. Large ones go back to shot-writer: a frame that needs three edits needs a better prompt.
5. Regenerate each picked frame at final quality before animating it: `fmotion edit O-004 "keep everything exactly; final render" --final`, then pick the result.

## Stage 4: Motion

**Choose the motion model.** Set `film.video_provider` in the shot list, override it per shot with `motion.provider`, or per run with `--provider`.

| Shot needs | Lean towards |
| --- | --- |
| An object or material kept identical across shots | Seedance: approved stills go in as reference images |
| Drafts and finals that match frame for frame | Seedance: the seed carries over |
| A strict avoid list | Kling: it has a separate `negative_prompt` field |
| A precise landing on a known end frame | Either. Kling switches to `pro` mode for it |
| You cannot tell which will do better | Both: `--provider seedance,kling` on the draft |

Treat this table as a starting point and let the drafts decide. The models change quickly, and the critic's verdict on your own shot outweighs any general ranking. When both are drafted, the strips carry only `O-` IDs, so frame-critic judges them blind. Render the final on the provider whose draft won.

1. `fmotion animate --draft` sends every picked still, cropped to the film ratio, as the first frame. On Seedance that means the fast model at 480p. On Kling it means `std` mode. Fix `film.seed` so Seedance drafts and finals are comparable.
2. `fmotion status --wait` polls every provider and downloads each clip as soon as it finishes, because result links expire (Seedance's after 24 hours). It also writes a six-frame strip per clip for review.
3. **frame-critic** reviews each strip for motion faults: morphing, drift, flicker, extra objects, a second camera move, or physics that feels wrong.
4. When a draft passes, render the final on the same provider: `fmotion animate --shots S03 --provider seedance --seed 41` (or `--provider kling`, which renders in `pro` mode). Kling has no seed, so review its final as a new option, not a copy of the draft. Pick the final clip.

**Continuity tools**, set per shot in `shotlist.json`:

- `motion.end_frame: "next"` makes the clip land exactly on the next shot's approved frame, so a cut can become a match.
- `motion.references: ["O-012"]` passes approved stills as reference images (bound in the prompt as `@Image1`, `@Image2` in order), to keep a material or object identical across shots. Seedance only; Kling ignores them.
- `motion.camera_fixed: true` locks the camera for shots where only the subject should move.

## Stage 5: Assemble

**Inside a Fastidious promo (the usual case):** hand the picked clips to showreel-director by `O-` ID. They go into its HyperFrames composition as muted `<video>` clips, alongside the type, interface and captured footage, and are cut, timed and mixed there with the rest of the film. Its Gauntlet reviews the whole film; frame-critic's scores for each generated shot go with them as evidence.

**A film made only of generated shots:** `fmotion assemble --music path/to/track.mp3` trims each picked clip to its shot length, conforms everything to the film size and frame rate, and normalises the sound to about -14 LUFS. The cut gets an `A-` ID. Supers, titles and the end card are then set over it in a HyperFrames composition (showreel-director), or as part of the site build if the film is a hero loop.

Either way, type is never asked of the model. Models misspell text and invent letterforms, and type is part of the brand.

## Stage 6: Checks

Run `fmotion check A-…` on every cut. It runs the WCAG 2.3.1 flash screen, measures loudness and confirms the format. A flash failure blocks the cut: fix it in the edit, never by loosening the check.

Then a clean-context subagent runs **frame-critic** on the whole cut, given only the brief, the shot list and the rendered film. The maker does not grade their own work.

## Rules

- **Likeness:** do not generate real, identifiable people or send their photographs. Seedance rejects references that look like real faces in any case. Hands and bodies are where models fail most visibly, so prefer objects, materials and places unless people are the point.
- **Rights:** send only images the person has the right to use. Do not upload client or confidential material without their say-so. Check the provider's terms for commercial use of outputs before a client delivery, and record what was checked in the ledger.
- **Budget:** state the estimated number of stills and video seconds before each stage, and get a yes before final renders. `fmotion cost` reports what has been spent; set your prices under `rates` in `motion/config.json`.
- **Ledger:** every still and clip is an `O-`, every pick is a `D-` with a reason, every cut is an `A-`. Refer to them by ID in conversation, so "animate O-014" always means the same thing.

## Anti-patterns

- Prompting before the brief exists, or writing a brief from the prompt you wanted to write.
- One direction per shot, then choosing the least bad of four seeds of it.
- Text-to-video for anything that matters. Approve the frame first.
- Asking the model for words, logos or interface copy.
- Fixing a weak shot with more adjectives. Change the subject, the light or the camera instead.
- Keeping a beautiful clip that does not serve the single idea.
- Letting provider links expire before downloading.
