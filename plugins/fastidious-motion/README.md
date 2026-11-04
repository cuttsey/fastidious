# fastidious-motion

Generated stills and film for projects run with [Fastidious](../fastidious). Fastidious decides what the work is for, what it should signify and what it must never look like. This plugin carries those decisions into every call to an image or video model, then holds every result to them.

It is a separate plugin on purpose. The Fastidious base skills need no API keys and spend nothing. This one calls paid APIs, so you install it only when a project needs imagery that cannot be captured or built.

## What it does

1. **Brief.** `motion-director` compiles `motion/brief.json` from your `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md` and `REFERENCES.md`. The brief holds the purpose, the audience, the single idea, what the work should signify, the palette, light, lens and texture, your references, and a list of AI clichés to avoid.
2. **Shots.** `shot-writer` writes `motion/shotlist.json`. Each shot has one idea and one camera move. Its prompts are written as photographs and camera directions, and it has two to four genuinely different directions to choose between.
3. **Styleframes.** gpt-image-2 renders every direction. You choose from labelled review sheets, with `frame-critic`'s scores and measured palette evidence alongside.
4. **Motion.** Seedance 2.0 or Kling animates the frames you approved, drafts first and finals after. For a hard shot, draft it on both and let `frame-critic` choose blind. Clips can land exactly on the next shot's frame, and on Seedance approved stills can be passed as references to keep materials identical across shots.
5. **Cut.** In a Fastidious promo, the picked clips go into showreel-director's HyperFrames composition and are cut with the type, interface and captured footage. For a film made only of generated shots, `fmotion` trims, conforms and joins the clips and normalises the sound. Either way, type is set in post, in your brand's own fonts.
6. **Checks.** A WCAG 2.3.1 flash screen, loudness, palette and format checks, and an independent review of the whole cut by a clean-context critic.

Every still and clip gets a permanent `O-` ID, every pick a `D-` with its reason, and every cut an `A-`, compatible with Fastidious's option-ledger.

## Providers

| Job | Provider | Model (default) | Key |
| --- | --- | --- | --- |
| Stills and edits | OpenAI Images API | `gpt-image-2` | `OPENAI_API_KEY` |
| Motion | BytePlus ModelArk (Seedance) | `dreamina-seedance-2-0-260128`; drafts on `dreamina-seedance-2-0-fast-260128` | `ARK_API_KEY` |
| Motion | Kling API | `kling-v3`; drafts in `std` mode, finals in `pro` | `KLING_API_KEY`, or `KLING_ACCESS_KEY` and `KLING_SECRET_KEY` |

OpenAI's video API (Sora 2) was shut down on 24 September 2026, so OpenAI is used for stills only.

### Seedance or Kling

Choose per film (`film.video_provider` in `shotlist.json`), per shot (`motion.provider`), or per run (`fmotion animate --provider kling`). `--provider seedance,kling` renders the same shot on both. The strips are labelled by `O-` ID only, so the critic judges them without knowing which model made which.

| | Seedance 2.0 | Kling |
| --- | --- | --- |
| First and last frame | Yes | Yes; the last frame (`image_tail`) switches the request to `pro` mode |
| Reference images for continuity | Yes, bound as `@Image1`, `@Image2` | Not sent; continuity comes from the first and last frames |
| Avoid list | Written into the prompt | Sent in a separate `negative_prompt` field |
| Aspect ratio | Set by `ratio` | Follows the input image, which `fmotion` crops to the film ratio |
| Seed | Yes, so drafts and finals match | No; pick the final, not the draft |
| Draft tier | Fast model at 480p | `std` mode |
| Auth | Bearer key | Bearer key, or a 30-minute HS256 JWT signed from access and secret keys |

Kling's access-key API takes `model_name` values up to `kling-v3`. Kling's newer endpoints (with IDs such as `kling-3.0-turbo` and `kling-v3-omni`) are not called by this adapter yet. Set `FMOTION_KLING_MODEL` to change the model, and `FMOTION_KLING_BASE` for a different region. Model IDs change often. Override them with `FMOTION_IMAGE_MODEL`, `FMOTION_VIDEO_MODEL`, `FMOTION_VIDEO_MODEL_DRAFT` and `FMOTION_ARK_BASE`, or in `motion/config.json`. For example, Volcengine Ark in China uses `https://ark.cn-beijing.volces.com/api/v3` and `doubao-seedance-2-0-260128`. Check the IDs against your account's model list before the first paid run.

Keys are read only from the environment, never from project files.

## Install

1. Install it from the Fastidious marketplace: `/plugin marketplace add cuttsey/fastidious`, then `/plugin install fastidious-motion@fastidious`.
2. You'll need Python 3.9 or later and `ffmpeg`. There are no Python packages to install.
3. Export your keys:

```bash
export OPENAI_API_KEY=...
export ARK_API_KEY=...        # Seedance
export KLING_API_KEY=...      # Kling (or KLING_ACCESS_KEY and KLING_SECRET_KEY)
```

You only need the keys for the providers you use.

Then, in a project that already has its Fastidious artefacts:

```text
/fastidious-motion:film a 30-second launch film for designers, for the README and LinkedIn
```

## The command line

`bin/fmotion` runs on its own too:

```bash
bin/fmotion init                         # creates ./motion with brief.json and shotlist.json to fill in
bin/fmotion validate                     # refuses briefs and shot lists that will waste money
bin/fmotion frames --dry-run             # writes every request to motion/requests/ without sending it
bin/fmotion frames                       # draft stills and a review sheet per shot
bin/fmotion pick O-004 --reason "..."
bin/fmotion edit O-004 "lower the horizon; nothing else" --final
bin/fmotion animate --draft              # drafts from the picked stills, on the film's video provider
bin/fmotion animate --shots S04 --draft --provider seedance,kling   # the same shot on both, judged blind
bin/fmotion status --wait                # downloads clips at once: Seedance links expire after 24 hours
bin/fmotion palette O-011                # share of coloured pixels on the brand palette
bin/fmotion assemble --music track.mp3
bin/fmotion check A-001                  # flash, loudness and format
bin/fmotion cost                         # stills and seconds spent, priced from rates in config.json
                                         # (keys like image_high, seedance_1080p_per_second, kling_pro_per_second)
```

## Example

`examples/fastidious-film/` holds a complete brief and a seven-shot list for a 30-second film. It tells designers why Fastidious exists, through objects and materials:

- a scalpel trimming a hairline from a printed edge;
- a compass needle settling;
- a seal pressed into wax;
- a plane taking one shaving;
- an object turned under one light;
- one distinct object in a row of grey ones.

Try it without spending anything:

```bash
bin/fmotion init
cp examples/fastidious-film/*.json motion/
bin/fmotion validate
bin/fmotion frames --dry-run
```

## Tests

```bash
python3 -m unittest discover tests
```

The tests run offline against mocked APIs. They check the request shapes, the ledger, the prompts, and the full pipeline from frames to checks.

## Limits

- **Request shapes are not yet tested against live APIs.** They follow published documentation and guides from 2026, but no live call was made while building this. Kling's full reference sits behind a developer login, so its adapter follows the widely documented `/v1/videos/image2video` API and is the most likely to need a field adjusted. Run `--dry-run`, then one draft still and one draft clip, before a full film.
- **Seedance refuses realistic human faces in reference images**, including AI-generated ones. The example uses objects and materials for this reason, and for craft.
- **The flash check is a screening tool.** A broadcast or regulated release still needs a dedicated photosensitive epilepsy analyser.
- **Check each provider's terms** for commercial use of outputs before a client delivery.
