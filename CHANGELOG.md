# Changelog

All notable changes to this repository. Versions follow [Semantic Versioning](https://semver.org/).

## Fastidious 1.3.0: 2026-11-06

### Added

- `render-engineer` gains a scroll-film kit for rung 3. `scripts/make_sequence.py` turns a film or a folder of rendered frames into WebP sequences at two widths with a poster and a manifest. `assets/scroll-film.js` plays them on one WebGL canvas: frames blend so short sequences glide, scenes change through an iris, a grain dissolve, a push, a fade or a cut, scenes can develop from grey into colour or arrive as halftone, and frames load nearest the playhead first. It reads the native scroll position and never intercepts it, falls back to posters and copy without WebGL, and shows still posters with fades for reduced motion.
- `examples/hollow-lane`: an invented cider maker built end to end with `copy-director`, `world-bible` and the scroll-film kit, with its imagery rendered in code with Blender, two rounds of series review and contact sheets of the finished page.
- Tests for the kit's timeline, its loading order and its promise not to intercept scrolling.

## Fastidious 1.2.0: 2026-11-06

### Added

- `copy-director`: writes and edits every line of a site, film or brand book. It turns the positioning, beats and voice into a spine line, three-beat claims, terms stated early, disclosure asides, a fit statement that names who the work is not for, an FAQ ordered as a sceptic's objections and all the microcopy, with every factual line tied to its evidence. It writes `COPY-DECK.md`, and `scripts/copy_lint.py` fails copy on em dashes, the "not X, it's Y" shape and a shared cliche list.
- `world-bible`: builds one pictorial world for the imagery (medium, palette, light, lens, materials, cast, props and overlaid devices), stages the idea as a sequence of acts in that world, locks three anchor frames, and runs a series critic over the whole set. It writes `WORLD-BIBLE.md` and `SERIES-REVIEW.md`, and `scripts/series_check.py` measures palette share, key, contrast, chroma, warmth and light side across a series and draws a contact sheet.
- Both were prompted by the study of pear.no, the twelfth exemplar.

### Changed

- `studio-conductor` runs `world-bible` and `copy-director` in phase 4, and gives each the lead in its precedence table.
- `sign-system-architect` mines the name itself for signs; `narrative-architect` can write beats as acts in an allegory; `asset-director`, `motion-director` and `frame-critic` follow `WORLD-BIBLE.md` when there is one.
- fastidious-motion 0.2.2: `motion-director` takes its look, cast and shot list from `WORLD-BIBLE.md` when there is one, and `frame-critic` checks continuity against its anchor frames.
- `accessibility-performance-auditor` adds three checks: native scrolling kept, DOM order matching visual order, and a still poster and copy in the HTML for every chapter told on a canvas, with labelled form fields.

## Fastidious 1.1.1: 2026-11-06

### Added

- A twelfth exemplar, pear.no, studied in a real browser: a whole page as one allegory drawn from the company's name, played as a scroll-scrubbed painted film through a single WebGL compositor under a fixed typographic frame. Its annotation in `detail-craft/references/exemplars.md` covers what to borrow and what to reject, and it is registered as `L-101` in `reference-curator`.
- An eighteenth shared lesson in the exemplars: a page can be one allegory, with each claim staged as a labour in that world.

## Fastidious 1.1.0: 2026-11-04

### Added

- A personal reference library that follows the designer across projects: `~/.claude/fastidious/REFERENCES.md`, with images in `references/` beside it (or wherever `FASTIDIOUS_LIBRARY` points). `taste-library` proposes its entries first on every project, keeps their numbers, and offers to add each project's best finds back.
- `taste-library/scripts/library.py` (`init`, `check`, `list`, `path`) and a starter `templates/REFERENCES.md`.
- "Bring your own taste" in the README; the film "One shot at greatness" leads the README.
- `PRFAQ.md`: the press release, who it is for and not for, the FAQ and the rude FAQs.

### Changed

- `taste-library` and `reference-curator` no longer refer to an unpublished references page; a pasted references table is adopted as it is.

## Fastidious 1.0.0 and fastidious-motion 0.2.1: 2026-11-04

First public release, under the MIT Licence.

### Added

- The repository is a Claude Code plugin marketplace with two plugins: `fastidious` (27 skills) and `fastidious-motion` (3 skills, a command line and a `/film` command).
- `crew_stack.py` and `crew.lock.json` install the 19 third-party skills Fastidious works alongside at pinned commits, instead of bundling copies. Folders it did not install are never overwritten without `--force`.
- `showreel-director` and `promo_stack.py` for promotional film, with a pinned stack (HyperFrames, motionmaxxing, business-motion-film, ElevenLabs) and a smoke test that renders a three-second film and runs the motion gates on it.
- `taste-library`, `option-ledger` and `model-switcher` join the spine.
- `legibility-check.js` measures every line of text against the pixels actually behind it; `mobile-auditor`, `scroll-verifier` and `accessibility-performance-auditor` run it.
- `reference-curator` gives every source and design system a permanent ID (`L-005` to `L-100`, `DS-001` to `DS-235`), and starts from the person's own references.
- `fastidious-motion`: gpt-image-2 styleframes, Seedance 2.0 and Kling motion, blind review strips, a ledger of every option, and flash and loudness checks on every cut.
- Continuous integration runs both test suites and a repository validator without network access or keys.

### Changed

- The build-stage entry point is now `build-sequencer`.
- `install.sh` installs the crew from its lock, and `--force` backs up any older bundled copies first.

### Removed

- Bundled copies of third-party skills, and the private promotional page.
