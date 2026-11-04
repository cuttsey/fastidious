---
name: showreel-director
description: Directs promotional film in Fastidious (launch and promo films, sizzle reels, hype and teaser cuts) from brief to checked delivery. Fastidious sets purpose and meaning; a pinned stack does the craft, with HyperFrames rendering, motionmaxxing judging motion, business-motion-film running fresh critics, ElevenLabs making sound and fastidious-motion making generated shots.
---

# Showreel director

A promotional film succeeds when a stranger, with the sound off, knows what the thing is, believes one thing about it, and knows what to do next. Most AI-made promos fail in the same ways: a deck of headlines, a held frame with nothing alive in it, house-style effects, invented proof, and a builder who certifies their own work.

Fastidious already decides what the work is for and what it should mean. This skill carries that into film and directs a small, pinned stack of specialist skills. Each package does one job, and this skill decides which leads when they overlap. It adds only what none of them covers:

1. **Selects** across a body of work, for sizzle reels.
2. **Frame-exact capture** of live web work (`scripts/reel-capture.js`).
3. **Sizzle and promo structure**, tied to Fastidious's beat map and option IDs.
4. **Versions** from one master.
5. **The flash screen** (`scripts/flash-check.py`).

## The stack

Each package is pinned to an exact commit in `promo-stack.lock.json`, kept in the `fastidious` skill's folder (a sibling of this skill's folder), and installed by `scripts/promo_stack.py install`.

| Job | Skill | Pinned |
| --- | --- | --- |
| Render: HTML compositions to MP4, identical on every render | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | HyperFrames v0.8.231 (`f0b2dd0c`), CLI `hyperframes@0.8.231` |
| Motion judgement: measured craft laws, precedent library, gates G0 to G5 | `motionmaxxing` | commit `8c8ec0f2` |
| Independent review: the Gauntlet, critic prompts, quality bar, frozen-time and loudness scripts, music back-timing | `business-motion-film` | commit `e4b1c000` |
| Music, sound effects, voice, transcripts | `elevenlabs-music`, `elevenlabs-sound-effects`, `elevenlabs-text-to-speech`, `elevenlabs-speech-to-text` | commit `503d4e9f` |
| Watching a reference film or a cut (optional) | `watch` | commit `03ceb42f` |
| Generated footage | fastidious-motion plugin (`motion-director`, `shot-writer`, `frame-critic`) | plugin 0.2.x |

### Stage 0: check the stack

Run `python3 scripts/promo_stack.py check` from the `fastidious` skill's folder (a sibling of this skill's folder) at the start of every promo job, and `smoke` after any install or pin change. Then work with what is there:

| Missing | Do instead |
| --- | --- |
| HyperFrames | Stop and offer to install it. Do not fall back to a renderer the person has not chosen. |
| motionmaxxing | Judge G1 to G5 by eye from contact sheets, and say in `NOTE.md` that the gates were not computed. |
| business-motion-film | Run the Gauntlet by hand with clean-context subagents (rules in Stage 7). |
| ElevenLabs key or skills | Use the licensed local library (video-shotcraft's `assets/audio`, Mixkit licence) or a track the person supplies. Say so in one line. |
| fastidious-motion or its keys | Build every shot in code or from captures. Never fake generated footage with stock that looks like it. |

Keep the pins pinned: export `HYPERFRAMES_SKIP_SKILLS=1` and `HYPERFRAMES_NO_UPDATE_CHECK=1`, run the CLI as `npx hyperframes@0.8.231` (or the project's own `npm run` scripts, which `init` pins), and never run `hyperframes skills update` or `npx skills add` for these packages inside a job. Moving a pin is a separate, deliberate change (`PROMO-STACK.md`).

## Kinds of promotional film

| Kind | Job | Typical length | Shape |
| --- | --- | --- | --- |
| Launch or promo film | One product, one idea, one action | 15 to 45 s | Hook, the product performing its claim, proof, one action |
| Sizzle reel | Range across a body of work | 30 to 60 s | Cold open, build, breath, peak, resolve |
| Hype or teaser | A feeling and a date, little explanation | 6 to 20 s | One image that grows, the reveal, the date |
| Feature reveal | One feature, shown working | 8 to 20 s | The problem in a frame, the feature acting, the result |

Pick the kind in the brief. A sizzle reel proves range; a promo proves one thing. Mixing them makes a film that proves neither.

## Who leads

| Decision | Lead | Supporting | Does not decide |
| --- | --- | --- | --- |
| Why the film exists, who it is for, the single action | frame-shifter, positioning-strategist | business-motion-film's brief rules (truth list, mute test) | motionmaxxing's PAGE, HyperFrames' story step |
| What it should signify; palette, type, voice | sign-system-architect, brand-system-architect | | motionmaxxing's `brand.mjs` (used only when there is no `BRAND-SYSTEM.md`, for example for a client's existing site) |
| The idea and the beats | narrative-architect, writing `BEAT-MAP.md` | motionmaxxing's idea kinds and cover-the-logo test; HyperFrames' three storylines | |
| Whose taste | taste-library (`REFERENCES.md`) | motionmaxxing's measured craft laws | motionmaxxing's `taste/verdicts.md`, which records another person's taste: calibration, not a brief |
| Timing, eases, transitions, layout | motionmaxxing craft laws | HyperFrames `references/motion.md`, emil-design-eng, gsap-core | |
| Building and rendering | HyperFrames | gsap-core; reel-capture for live sites | video-shotcraft and Remotion, unless the person asks for them or the project already uses them |
| Generated shots | fastidious-motion | | HyperFrames `media-use` HeyGen generation, unless the person chooses HeyGen |
| Music, effects, voice | ElevenLabs skills | HyperFrames `beats` and `normalize-audio`; business-motion-film's `backtime-music.py` | |
| Review | business-motion-film's Gauntlet | motionmaxxing gates, HyperFrames `check`, fastidious-motion's frame-critic, `flash-check.py` | the builder |

Upstream Fastidious files outrank downstream defaults. Where a package's default conflicts with `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md` or `REFERENCES.md`, the file wins unless the person decides otherwise, and the decision is logged as a `D-`.

## Stage 1: Brief

Write `BRIEF.md` from the Fastidious artefacts:

- **Purpose** from `FRAME.md`: why a film, and why now.
- **Audience** from `POSITIONING.md`: the one person, where they will see it (README, feed, event screen) and the single action afterwards.
- **Kind and length**, from the table above.
- **Truth list:** every name, number, claim and screen that may appear, each with its source. Nothing outside the list appears on screen. A concept film says it is a concept.
- **The mute test:** what a viewer must understand with the sound off.
- **Brand:** palette, type and voice from `BRAND-SYSTEM.md`; references by `R-` number from `REFERENCES.md`.
- **Never claim:** from positioning and the person.

Get a yes on the brief before any idea work.

## Stage 2: Idea

1. Write three films that are three different kinds, using motionmaxxing's idea kinds (`references/idea.md`) and HyperFrames' storylines (`references/story.md`): a documentary of one real task, a typographic essay, a real-output montage, a single held shot that breaks, and so on. A transformation chain is the most over-used kind; offer it only with a reason.
2. Test each one: cover the logo, and would a competitor's film still work? Does every beat "buy" a belief ("Buys: the viewer believes ___")?
3. Show them as option cards (option-ledger `O-`). The person picks; record a `D-`.
4. narrative-architect writes the chosen film as `BEAT-MAP.md`: beats with roles (hook, turn, proof, action), what each buys, and the hero moment worth a screenshot.

## Stage 3: Sources

Gather the picture for each beat, and label each source as real, rebuilt or generated in the truth list.

- **Live web work:** `scripts/reel-capture.js` for scroll and motion that is the work itself; `npx hyperframes@0.8.231 capture <url>` to rebuild a page's screens and fonts as editable HTML.
- **Product interface:** rebuilt in HTML from real screens, with real copy. Never an invented dashboard.
- **Generated shots:** fastidious-motion's styleframes, then motion, each picked by frame-critic and the person, arriving as clips with `O-` IDs.
- **Existing footage:** only with the rights recorded.
- **For a sizzle reel:** gather about three times what the master needs, as `O-` cards with a still and a length; the person picks.

## Stage 4: Storyboard and spec

1. **Storyboard** (business-motion-film's rules): one row per beat with time, what the viewer sees, what it buys, and the transition out, including which object survives it. Aim for 12 to 15 distinct compositions in 30 seconds, and vary the scale. The lead subject fills most of the usable frame in feature beats.
2. **Spec** (HyperFrames' `SPEC.md`): every adjective as a number. Durations, eases, type sizes as a share of the frame height, the defaults banned by name. Take the numbers from motionmaxxing's craft laws: median move about 10 frames; words 2 to 12 frames apart; land decelerating, leave accelerating; one hero per frame; nothing grows from zero.
3. **Music** is chosen now, before the build, so the beats can land on it (Stage 6).
4. **Storyboard critic:** a fresh critic checks chronology, truth and variety before anything is built.

## Stage 5: Build in HyperFrames

- **Start pinned:** `npx hyperframes@0.8.231 init film --skip-skills`. The scaffold pins the CLI in `package.json`, so `npm run check` and `npm run render` stay on the pinned version.
- **No network at render:** vendor GSAP and every font into `assets/`; replace the scaffold's CDN script tag with `assets/gsap.min.js`. A render that fetches can break on a network that blocks it, and is no longer reproducible.
- **Brand as variables:** palette, type and copy from `BRAND-SYSTEM.md` become CSS variables and `data-var-*` values, so a client can change them in the HyperFrames desktop app.
- **Hardest beat first:** build the hero moment and its hardest handoff, then take stills with `snapshot` and look. If it does not read at speed, fix the idea, not the polish.
- **Follow the contract** in the `hyperframes` skill: timed elements are `.clip`s with a size, tweens go on children, nothing reads the wall clock, `check --json` passes before every review.
- **Generated clips** go in as `<video>` clips, muted unless their sound is wanted. Grades go through `media-treatment`, never CSS filters.
- **Supers** sit on a plate or scrim in the brand's type, at most six words, held long enough to read twice. HyperFrames' contrast audit must pass.

## Stage 6: Sound

- **Music:** `elevenlabs-music`, written from the brief's mood and the beat map's length, or a licensed track the person supplies. Back-time it with business-motion-film's `backtime-music.py`, so its own ending lands on the end card. Read the beat grid with `npx hyperframes@0.8.231 beats`. Cuts land on beats; the turn lands on a downbeat.
- **Effects:** `elevenlabs-sound-effects` for the few events that deserve sound, chosen from the render's own event list. Silence comes before the hit. One to three hero hits in a film.
- **Voice**, if the brief calls for it: `elevenlabs-text-to-speech` at about 2.5 to 3 words a second; on-screen words land just before they are heard.
- **Mix and loudness:** about -14 LUFS integrated, true peak at or below -1 dBTP, music ducked while the viewer reads. Measure with business-motion-film's `loudness.sh`.
- Render versions with and without music from the same timeline.

## Stage 7: Review (the Gauntlet)

The builder never judges their own work. Every review round goes to a fresh, clean-context subagent that sees only the render, the brief, the beat map, the references and, in verification rounds, the previous critic's report. Use business-motion-film's `references/critic-prompts.md` for the storyboard, component, full-film and verification rounds.

Before each full-film critic, run and attach the measurements:

| Check | Tool | Bar |
| --- | --- | --- |
| Render exists, no empty frames, end hold | motionmaxxing `look.py film.mp4 --expect <s> --expect-audio` (G0, G2, G3) | Pass |
| No page chrome | motionmaxxing `lint.mjs index.html` (G5) | Pass, unless `BRAND-SYSTEM.md` specifies the element (then a logged `D-`) |
| Proof readable, one hero per frame | Judged on the contact sheet (G1, G4) | Pass |
| Composition contract, layout, contrast | `npm run check -- --json` | No errors |
| Frozen time | business-motion-film `frozen-time.sh` | Every still stretch is a designed breath, not a stall |
| Loudness | business-motion-film `loudness.sh` | About -14 LUFS, at or below -1 dBTP |
| Photosensitive safety | `scripts/flash-check.py` | Pass, always; a failure is fixed in the edit |
| Generated shots | fastidious-motion `frame-critic` | Picked, not least bad |

Fix the largest gap first. The next round goes to a new critic, which checks each previous finding as fixed, partly fixed or still present, and looks for regressions. Stop at the quality bar (`references/quality-bar.md`), at diminishing returns, or when the person says stop. Keep the round ledger.

## Stage 8: Versions and delivery

- **Lengths:** cut down from the master's timeline, never re-edited from scratch. Shorten the build first, then the peak, and keep the opening and the resolve. A 6-second version is the hook plus the mark.
- **Aspects:** 16:9, 1:1, 4:5 and 9:16. Re-capture live work at phone size for vertical; never crop desktop footage to 9:16.
- **Render:** `npm run render -- --quality delivery -o <name>.mp4`; `render --batch` for variants from variables.
- **Deliver:** master and versions, poster frame, contact sheet, editable source, `NOTE.md` (the idea and why; what each beat buys; what is real, rebuilt or generated; the gate numbers quoted from the scripts; honest limits), and the ledgers (generation, Gauntlet, option IDs). Each version is an `A-`.

## Rules where the packages disagree

- **End card:** a film that ends on an address holds the card for 2 to 3.5 seconds with one living element, so it reads twice. The picture may not sit unchanged for more than 1.4 seconds (motionmaxxing's G3).
- **Labels and chrome:** motionmaxxing's G5 fails tracked-caps labels, counters and corner marks. They are out by default. If the brand system specifies one (a race label, a lap counter), keep it only with a logged `D-` and a reason, and never as decoration.
- **Paid media:** HyperFrames' `media-use` offers HeyGen credits. Use them only if the person chooses HeyGen; otherwise sound comes from ElevenLabs and generated shots from fastidious-motion.
- **Telemetry:** HyperFrames collects anonymous usage data unless it is turned off. Tell the person once and offer `npx hyperframes@0.8.231 telemetry disable`.
- **Story:** HyperFrames and motionmaxxing both generate ideas. Their options feed Stage 2; narrative-architect's `BEAT-MAP.md` is the one that is built.

## Anti-patterns

- Starting in HyperFrames before the brief and beat map exist.
- A deck: a held headline, then a screenshot, then the next headline.
- A frame with nothing alive in it, longer than a designed breath.
- Invented proof, stats or interfaces; a concept film presented as real.
- Effects as style: glows, typewriter text, colour-flood wipes, bounce.
- Music chosen after the edit; a mix that is a flat wall of sound.
- The builder grading their own film, or a critic told what was fixed.
- Updating a pinned package in the middle of a job.

## Scripts

These ship in the `scripts/` folder of the `fastidious` skill's folder (a sibling of this skill's folder), the single source for each:

- `reel-capture.js` films a live page frame by frame by taking over its clock. Needs `playwright` and `ffmpeg`. Usage: `node scripts/reel-capture.js <url> <out.mp4> [--w 1920] [--h 1080] [--fps 30] [--from 0] [--to 0] [--dur 4] [--hold 0.5] [--setup "<js>"]`.
- `flash-check.py` screens a render against WCAG 2.3.1 and exits 1 on a failure. Needs `numpy` and `ffmpeg`. Usage: `python3 scripts/flash-check.py <film.mp4>`.
- `promo_stack.py` installs, checks and smoke-tests the pinned stack (`install`, `check`, `smoke`, `outdated`).

If that folder is not available, ask for it rather than rewriting a script from memory.
