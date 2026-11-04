# Contributing

Thank you for helping make Fastidious better. The most useful contribution is a report from a real project: [open a project report](../../issues/new?template=project-report.yml).

## Changing a skill

- One skill, one job. If a change makes a skill do a second job, propose a new skill instead.
- Keep the frontmatter `name` identical to the folder name, and keep the `description` under 1,024 characters. It decides when the skill is used, so say when to use it, not how good it is.
- Upstream files outrank downstream preferences. A skill that reads `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md` or `BRAND-SYSTEM.md` follows them unless the person decides otherwise.
- Cite sources a reader can check. Add them to the skill's references list.
- Write in British English with sentence case headings.

## Changing a pin

Follow "Moving a pin" in [CREW.md](plugins/fastidious/skills/fastidious/CREW.md) or [PROMO-STACK.md](plugins/fastidious/skills/fastidious/PROMO-STACK.md). Only MIT and Apache-2.0 packages are installed. Never copy a third-party skill into this repository; pin it instead.

## Before you open a pull request

```bash
python3 scripts/validate.py
python3 -m unittest discover plugins/fastidious/tests
python3 -m unittest discover plugins/fastidious-motion/tests
```

All three run offline. Never commit an API key, a `.env` file, client material or anything you do not have the right to publish.
