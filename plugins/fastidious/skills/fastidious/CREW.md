# The crew

Fastidious is 31 skills of its own working alongside 19 skills by other people. The 19 are installed by `scripts/crew_stack.py`, each at an exact commit recorded in `crew.lock.json`, and copied unchanged. They are not bundled in this repository, so each stays under its author's licence, is fetched from its author's repository, and moves only when the lock is deliberately edited.

## What is installed

| Package | Skills | Job in Fastidious | Pinned at | Licence |
| --- | --- | --- | --- | --- |
| [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus | `impeccable` | Design rules, critique and tuning; leads art direction for product UI | `skill-v4.8.0` (`414603bf`) | Apache-2.0 |
| [Taste](https://github.com/leonxlnx/taste-skill) by Leonxlnx | `design-taste-frontend` | Art direction for public pages | `v2.1.5` (`12af471f`) | MIT |
| [Emil Kowalski's skills](https://github.com/emilkowalski/skills) | `emil-design-eng`, `animate`, `animate-expo`, `animation-performance`, `animation-vocabulary`, `apple-design`, `ask-sonner`, `break-ui`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `pick-ui-library`, `prototype`, `review-animations` | Interface and animation craft | `2d228630` | MIT |
| [GSAP skills](https://github.com/greensock/gsap-skills) by GreenSock | `gsap-core`, `gsap-scrolltrigger` | Animation and scroll-linked animation | `aed9cfd3` | MIT |
| [Anatomy](https://github.com/wheresryan22/anatomy) by Ryan | `anatomy` | Explanatory isometric figures | `1482e846` | MIT |

Impeccable is installed as its Claude Code skill folder only, without the upstream plugin's hooks and agents. None of these projects is affiliated with Fastidious or has endorsed it.

## Install and check

You need git and Python 3.

```bash
python3 scripts/crew_stack.py install     # into ~/.claude/skills, or --dir elsewhere
python3 scripts/crew_stack.py check
```

Each installed folder gets a `.fastidious-pin.json` recording the package, commit and licence. A folder without that file is yours, perhaps an older copy you installed by hand, and is skipped unless you pass `--force`. `check` reports such folders, because their version is unknown.

## Moving a pin

1. `python3 scripts/crew_stack.py outdated` lists packages whose upstream has moved. It changes nothing.
2. Read the upstream changes since the pinned commit. Prefer a release tag, or a commit at least a week old.
3. Check that every skill path in the lock still exists at the new commit, and that the skill's `name` is unchanged.
4. Check the licence at the new commit. Only MIT and Apache-2.0 are installed.
5. Edit `commit` and `ref` in `crew.lock.json`, then run `install`, `check` and the plugin tests.
6. Run one real job through `studio-conductor` before releasing the change, and note it in `CHANGELOG.md`.
