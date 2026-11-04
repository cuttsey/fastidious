# Changelog

All notable changes to this repository. Versions follow [Semantic Versioning](https://semver.org/).

## Fastidious 1.1.0: 2026-11-04

### Added

- A personal reference library that follows the designer across projects: `~/.claude/fastidious/REFERENCES.md`, with images in `references/` beside it (or wherever `FASTIDIOUS_LIBRARY` points). `taste-library` proposes its entries first on every project, keeps their numbers, and offers to add each project's best finds back.
- `taste-library/scripts/library.py` (`init`, `check`, `list`, `path`) and a starter `templates/REFERENCES.md`.
- "Bring your own taste" in the README; the film "One shot at greatness" leads the README.

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
