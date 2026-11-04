# The promo stack

Fastidious makes promotional film with five third-party packages, each doing one job, and directs them with `showreel-director`. This page covers installing them, keeping them stable and moving a pin.

## What is installed

| Package | Skills it adds | Job | Pinned at | Licence |
| --- | --- | --- | --- | --- |
| [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen) | `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | Renders HTML compositions to MP4, identically on every render | v0.8.231 (`f0b2dd0c`), CLI `hyperframes@0.8.231` | Apache-2.0 |
| [motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | `motionmaxxing` | Measured motion craft laws, a precedent library, gates computed on the render | `8c8ec0f2` | Apache-2.0 |
| [Motion Video Kit](https://github.com/echris6/motion-video-kit) | `business-motion-film` | The Gauntlet: fresh critics every round, critic prompts, quality bar, frozen-time and loudness scripts | `e4b1c000` | MIT |
| [ElevenLabs skills](https://github.com/elevenlabs/skills) | `elevenlabs-music`, `elevenlabs-sound-effects`, `elevenlabs-text-to-speech`, `elevenlabs-speech-to-text` | Music, sound effects, voice and transcripts | `503d4e9f` | MIT |
| [claude-video](https://github.com/bradautomates/claude-video) (optional) | `watch` | Lets Claude watch a reference film or a cut | `03ceb42f` | MIT |

Generated footage comes from the separate fastidious-motion plugin (Seedance and Kling for motion, gpt-image-2 for frames).

The ElevenLabs skills are renamed with an `elevenlabs-` prefix on install, because names such as `music` would collide with other publishers' skills. Nothing else in any package is changed.

## Install

You'll need git, Node 22 or later, ffmpeg, Python 3 and Chrome.

```bash
python3 scripts/promo_stack.py install            # core packages into ~/.claude/skills
python3 scripts/promo_stack.py install --with watch
python3 scripts/promo_stack.py check              # versions, requirements, keys
python3 scripts/promo_stack.py smoke              # renders a 3-second film and runs the gates on it
```

Each package is fetched at its exact commit, verified, and copied with a `.fastidious-pin.json` beside its `SKILL.md`. A folder of the same name without that file belongs to you and is never overwritten unless you pass `--force`. `--dir` installs somewhere other than `~/.claude/skills`.

Then add these to your shell profile:

```bash
export HYPERFRAMES_SKIP_SKILLS=1         # the HyperFrames CLI never installs newer skills over the pin
export HYPERFRAMES_NO_UPDATE_CHECK=1     # and never nags about them
export ELEVENLABS_API_KEY=...            # for music, effects and voice
```

HyperFrames sends anonymous usage data by default. To turn it off, run `npx hyperframes@0.8.231 telemetry disable`. HyperFrames and motionmaxxing both need a Chrome. If yours is somewhere unusual, set `CHROME_PATH`; HyperFrames also reads `HYPERFRAMES_BROWSER_PATH`. On Linux as root, Chrome needs `--no-sandbox`, so point `CHROME_PATH` at a two-line wrapper script that adds it.

## Why these, and not others

- **HyperFrames over Remotion:** Remotion needs a company licence once a business has more than three employees, and making it a Fastidious dependency would pass that cost to every user. HyperFrames is Apache-2.0, works in plain HTML with GSAP (already in Fastidious), and renders the same file identically every time. Remotion and video-shotcraft stay available for projects that already use them.
- **Not bundled:** OpenMontage (AGPL-3.0), onetake (PolyForm Noncommercial) and the charlie947 motion-graphics pack, which overlaps brand-system-architect and showreel-director. The first two are studied, not shipped.
- **One job each:** HyperFrames renders, motionmaxxing judges motion, business-motion-film judges the film, ElevenLabs makes sound. Where two of them could decide the same thing, `showreel-director` and `studio-conductor` name the lead.

## What was verified when the lock was written

On 4 November 2026, in a Linux container:

- `install` fetched all five packages at their pinned commits in about seven seconds.
- `check` passed. It refused to overwrite a folder that wasn't installed by Fastidious.
- `smoke` rendered a 3-second film with the pinned HyperFrames CLI, then ran motionmaxxing's `look.py` (G0, G2 and G3 passed) and `lint.mjs` (G5 passed) on the result.
- business-motion-film's `loudness.sh` and `frozen-time.sh` ran on an existing reel.
- No ElevenLabs call was made, because no key was available, so sound generation is not yet tested end to end.

## Moving a pin

Pins move only by a deliberate edit, never during a job.

1. Run `python3 scripts/promo_stack.py outdated` to see which packages have moved. It changes nothing.
2. Read the package's changes since the pinned commit. For HyperFrames, prefer a release that has stood for two weeks; the 0.9 line began on 2 November 2026 and was patched ten times in its first two days.
3. Update `commit`, `ref`, the date in `locked` and, for HyperFrames, `cli` in `promo-stack.lock.json`.
4. Run `install`, `check` and `smoke`, then render one real film's draft and compare it with its last render.
5. Check whether any skill name, file path or command referenced in `showreel-director` has changed: `hyperframes/references/story.md`, `spec.md` and `motion.md`; `motionmaxxing/references/idea.md`; `scripts/look.py` and `lint.mjs`; `business-motion-film/references/critic-prompts.md`, `gauntlet.md` and `quality-bar.md`; and `scripts/loudness.sh`, `frozen-time.sh` and `backtime-music.py`.
6. Record the change in the release notes.
