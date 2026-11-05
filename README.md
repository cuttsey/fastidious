<p align="center">
  <a href="https://code.claude.com/docs/en/plugins"><img src="https://img.shields.io/badge/Claude_Code-plugin-171717?style=flat-square&logo=claude&logoColor=white" alt="Claude Code plugin"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent_Skills-compatible-171717?style=flat-square" alt="Agent Skills compatible"></a>
  <a href="#install"><img src="https://img.shields.io/badge/runs_on-Python_3_%C2%B7_Node_22-171717?style=flat-square&logo=python&logoColor=white" alt="Runs on Python 3 and Node 22"></a>
  <a href="https://github.com/cuttsey/fastidious/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/cuttsey/fastidious/ci.yml?branch=main&style=flat-square&label=CI&color=171717" alt="CI status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-171717?style=flat-square" alt="MIT licence"></a>
</p>

<p align="center"><a href="assets/fastidious-film.mp4"><img src="assets/fastidious-teaser.gif" alt="A generic AI website, then an invented ferry site whose tide dial turns as the page scrolls, ending on One shot at greatness. Fastidious." width="100%"></a></p>

<p align="center"><a href="assets/fastidious-film.mp4"><b>Watch the film: One shot at greatness (56 seconds)</b></a> &middot; <a href="PRFAQ.md"><b>Read the press release and FAQ</b></a></p>

# Fastidious

**One shot at greatness.** Design skills for Claude Code that will not settle for good.

The best designers are always dissatisfied. They know the work could be better, and they keep going until it is. They are fastidious. This is Fastidious.

Any designer can build a strong harness for Claude Code: good prompts, good skills, good tools. Getting great output from it consistently takes something more, a system of context: what the work is for, what it should mean, whose taste it follows, and which decisions were made and why. Fastidious is that system. It gathers the context a senior designer carries in their head, writes it down in plain files and works from it at every step, so great output becomes the norm rather than the lucky run, and it aims to get there from one brief, in one shot.

Fastidious is a set of design skills for Claude Code that takes a brief to finished, presented work. It questions the brief, decides what the work should mean and how it should feel, builds it, measures it in a real browser, looks at its own screenshots, writes down why every detail is as it is, and then puts the work out in the world so people can judge it. It asks you at every fork. You drive; it holds the bar.

## Four disciplines, one standard

Most AI design tools are strong at one thing, usually the build. Fastidious covers the four places where good work becomes great work, and each is grounded in published practice rather than taste alone.

| Discipline | What it settles | Skills | Grounded in |
| --- | --- | --- | --- |
| **Purpose** | Why the work exists, who it is for, and the one idea it defends | `frame-shifter`, `positioning-strategist`, `analogy-scout`, `narrative-architect` | Problem framing (Rittel and Webber, 1973; Schön, 1983; Dorst, 2015) and analogical transfer (Gentner, 1983) |
| **Identity** | What the work signifies, its personality, and the tokens that hold it | `sign-system-architect`, `brand-system-architect`, `brand-book`, `iconography`, `taste-library`, `reference-curator` | Semiotics (Barthes, 1977; Chandler, 2017; Kress and van Leeuwen, 2021), with 235 production design systems and 96 ranked sources on file |
| **Craft** | The dozens of small loops that move a product from good to great | `detail-craft`, `interaction-minimum-designer`, `component-librarian`, `motion-choreographer`, `render-engineer`, `asset-director`, `blender-build`, then `mobile-auditor`, `scroll-verifier` and `accessibility-performance-auditor` | Exemplar sites taken apart in a real browser, and [WCAG 2.2](https://www.w3.org/TR/WCAG22/) measured against rendered pixels |
| **Presentation** | Showing the work as it will live: in place, in motion, in public | `supermock`, `showreel-director`, and the separate `fastidious-motion` plugin | Frame-exact capture, an independent critic for every film, and a [WCAG 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html) flash screen |

A spine of five skills runs through all four. `fastidious` holds the house rules, `studio-conductor` sequences the work through the [Design Council's double diamond](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/) and logs every decision with its options and criteria (MacLean et al., 1991), `build-sequencer` runs the build stages, `option-ledger` gives every option and decision a permanent ID, and `model-switcher` keeps each step on the cheapest model that does it well.

### Selection with a bias towards distinction

Every phase opens wide and then narrows, and you choose. Options are scored against the frame and the positioning, the weakest are pruned, and the strongest are combined (Pugh, 1991). The bias is deliberate: anything that could sit unchanged on a competitor's site is rejected, however polished. The personality is the product, so every effect, word and transition is checked against it.

## What you stop letting slide

- **Every brief gets questioned first.** You see alternative frames before anyone opens a colour picker, and you choose.
- **Every page gets checked in a real browser.** Pages are measured at phone, tablet and desktop widths, and every line of text is tested against the pixels actually behind it.
- **Every site starts with its own details.** Cursor, scrollbar and hover gesture ship in version 1, drawn from the subject's world.
- **Every detail comes with its reason.** The rationale covers six registers: personality, persuasion, routes dropped, proof, inclusion, and craft and cost.
- **Every decision gets written down.** A numbered log records what was chosen, what was given up and what would reopen it.
- **Every piece of work gets presented.** Mock-ups in place, animated display ads and a film, so the work is judged as people will meet it.

## Install

You need Claude Code, git, Python 3, Node 22 or later and Chrome. `blender-build` also needs Blender, and `supermock` and the film work need ffmpeg.

### As a plugin

```text
/plugin marketplace add cuttsey/fastidious
/plugin install fastidious@fastidious
/plugin install fastidious-motion@fastidious
```

`fastidious-motion` is optional. On the first run, the `fastidious` skill checks for the third-party skills it works alongside and offers to install them at their pinned commits.

### As plain skills

```bash
git clone https://github.com/cuttsey/fastidious.git
cd fastidious
./install.sh
```

The installer copies the Fastidious skills into `~/.claude/skills`, then installs the third-party crew at the exact commits in [`crew.lock.json`](plugins/fastidious/skills/fastidious/crew.lock.json). It never overwrites a skill you already have; `./install.sh --force` replaces them after moving yours to a backup. Add `--with-film` for the pinned promotional film stack. Restart Claude Code afterwards.

## Use it

Start in an empty folder:

```text
/fastidious a site for a small ferry between two islands that only runs when the tide allows
```

As a plugin, the same command is `/fastidious:fastidious`. It asks you to choose at each fork and writes its working files into the project as it goes. Run it again in the same folder to resume from `STUDIO-STATE.md`.

For one job, call a specialist directly:

```text
/impeccable critique this page
/detail-craft plan the signature moments for this site
/supermock put this site on a phone and a billboard
/showreel-director a 30-second launch film for this product
```

A full project runs many stages and can use a good part of your Claude allowance, so try it on a real brief when you have time to engage with it.

## Bring your own taste

Fastidious starts from your references, not a house style. Keep the sites you admire and the images you learn from in a personal library, and every project begins there before it looks anywhere else.

```bash
python3 plugins/fastidious/skills/taste-library/scripts/library.py init
```

That creates `~/.claude/fastidious/REFERENCES.md`, with a `references/` folder beside it for screenshots, photographs and scans named by ID (`R-003.png`). Or skip the file and hand them over in Claude Code:

```text
/fastidious:taste-library add these to my library: https://example.com, https://example.org and the three screenshots attached. For each, note what to borrow and what to reject.
```

Every reference gets a permanent number and two notes: what to borrow and what to reject. A link without both is not yet a reference. On each project, `taste-library` proposes the entries that fit the brief, copies the ones you choose into the project with their numbers unchanged, and `reference-curator` builds the reference board from them first, reaching into the 235 design systems and 96 ranked sources only to fill the gaps. At the end it offers to add the project's best finds back to your library, and only you decide what goes in. `library.py check` confirms every entry has its notes and every image is where its number says.

Images you want used in the work itself, such as a logo, photography or product shots, belong in the project's assets, where `asset-director` handles them. The library is for learning from.

## What you get back

Alongside the work, a full run leaves the reasoning in the project:

| File | What it holds |
| --- | --- |
| `FRAME.md` | The problem, the frames considered and the one chosen |
| `POSITIONING.md` | One specific person, their pain and a promise a competitor could not copy |
| `SIGN-SYSTEM.md` | What the work should signify, and the personality behind it |
| `BRAND-SYSTEM.md` | Tokens for colour, type, spacing and motion, plus voice |
| `REFERENCE-BOARD.md` | Annotated references, each stating what was borrowed and what was rejected |
| `DETAIL-PLAN.md` | Signature moments, cursor, scrollbar, hover, budgets and fallbacks |
| `DESIGN-RATIONALE.md` | The numbered decision log |
| `DESIGN-RATIONALE-DETAILS.md` | The six-register reason for every detail |
| `VERIFICATION-LOG.md` | What was checked, at which widths and in which states |
| `STUDIO-STATE.md` | Where the project stands and what is next |

## What is inside

This repository is a Claude Code plugin marketplace with two plugins.

**`plugins/fastidious`**: 27 skills.

| Group | Skills |
| --- | --- |
| Spine | `fastidious`, `studio-conductor`, `build-sequencer`, `option-ledger`, `model-switcher` |
| Purpose | `frame-shifter`, `positioning-strategist`, `analogy-scout`, `narrative-architect` |
| Identity | `sign-system-architect`, `brand-system-architect`, `brand-book`, `iconography`, `taste-library`, `reference-curator` |
| Craft | `detail-craft`, `interaction-minimum-designer`, `component-librarian`, `motion-choreographer`, `render-engineer`, `asset-director`, `blender-build` |
| Checks | `mobile-auditor`, `scroll-verifier`, `accessibility-performance-auditor` |
| Presentation | `supermock`, `showreel-director` |

**`plugins/fastidious-motion`**: generated stills and film through image and video model APIs (gpt-image-2 for frames, Seedance 2.0 or Kling for motion), driven by the Fastidious artefacts. It adds `motion-director`, `shot-writer` and `frame-critic`, a standard-library command line and a `/film` command. API keys are read from the environment only. See its [README](plugins/fastidious-motion/README.md).

**The crew**: 19 skills by other people, installed at pinned commits and never edited. See [CREW.md](plugins/fastidious/skills/fastidious/CREW.md).

| Package | Skills |
| --- | --- |
| [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus | `impeccable` |
| [Taste](https://github.com/leonxlnx/taste-skill) by Leonxlnx | `design-taste-frontend` |
| [Emil Kowalski's skills](https://github.com/emilkowalski/skills) | `emil-design-eng`, `animate`, `animate-expo`, `animation-performance`, `animation-vocabulary`, `apple-design`, `ask-sonner`, `break-ui`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `pick-ui-library`, `prototype`, `review-animations` |
| [GSAP skills](https://github.com/greensock/gsap-skills) by GreenSock | `gsap-core`, `gsap-scrolltrigger` |
| [Anatomy](https://github.com/wheresryan22/anatomy) by Ryan | `anatomy` |

**The promotional film stack** (optional): HyperFrames, motionmaxxing, business-motion-film and ElevenLabs' skills, pinned the same way and directed by `showreel-director`. See [PROMO-STACK.md](plugins/fastidious/skills/fastidious/PROMO-STACK.md).

## Scripts

| Script | What it does | Needs |
| --- | --- | --- |
| `crew_stack.py` | Installs and checks the crew at its pinned commits | git |
| `promo_stack.py` | Installs, checks and smoke-tests the film stack | git, Node 22, ffmpeg |
| `legibility-check.js` | Renders each screen with text forced black, forced white and transparent, then measures WCAG contrast against the real backdrop. Exit code 1 on failure, so it can gate a hook or CI | `playwright`, `pngjs` |
| `reel-capture.js` | Films a live page frame by frame by taking over its clock, so scroll reveals and animation are captured without dropped frames | `playwright`, `ffmpeg` |
| `flash-check.py` | Screens a rendered video against WCAG 2.3.1. A screening check, not a certified test | `numpy`, `ffmpeg` |

They live in [`plugins/fastidious/skills/fastidious/scripts`](plugins/fastidious/skills/fastidious/scripts).

## Fair questions

The short version is below. The [press release and FAQ](PRFAQ.md) covers who Fastidious is for and who it is not for, and answers the rude questions too.


**Will it replace a designer?** No. It needs someone who can tell a good answer from a plausible one, and it leaves the last word with you.

**Can it be wrong?** Yes. Passing every check means nothing banned was measured; it does not mean the work is good. That is why it also critiques its own screenshots, and why you choose at every fork.

**Is it faster?** Much faster than doing it all by hand. Slower than a prompt box, because it stops and asks you things.

## Tell us how it went

Run it on a real brief, then [open a project report](../../issues/new?template=project-report.yml). "What still looked like AI made it?" is the question that matters most. Be fastidious about it.

## References

The skills carry their full reading lists. These are the works cited above.

- Barthes, R. (1977) 'Rhetoric of the image', in *Image, Music, Text*. Trans. S. Heath. London: Fontana, pp. 32 to 51.
- Chandler, D. (2017) *Semiotics: The Basics*. 3rd edn. London: Routledge.
- Design Council (2019) [*Framework for Innovation: Design Council's Evolved Double Diamond*](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/). London: Design Council.
- Dorst, K. (2015) *Frame Innovation: Create New Thinking by Design*. Cambridge, MA: MIT Press.
- Gentner, D. (1983) ['Structure-mapping: a theoretical framework for analogy'](https://doi.org/10.1207/s15516709cog0702_3), *Cognitive Science*, 7(2), pp. 155 to 170.
- Kress, G. and van Leeuwen, T. (2021) [*Reading Images: The Grammar of Visual Design*](https://www.routledge.com/Reading-Images-The-Grammar-of-Visual-Design/Kress-vanLeeuwen/p/book/9780415672573). 3rd edn. London: Routledge.
- MacLean, A., Young, R. M., Bellotti, V. M. E. and Moran, T. P. (1991) ['Questions, options, and criteria: elements of design space analysis'](https://dblp.org/rec/journals/hhci/MacLeanYBM91.html), *Human-Computer Interaction*, 6(3 and 4), pp. 201 to 250.
- Pugh, S. (1991) *Total Design: Integrated Methods for Successful Product Engineering*. Wokingham: Addison-Wesley.
- Rittel, H. W. J. and Webber, M. M. (1973) ['Dilemmas in a general theory of planning'](https://doi.org/10.1007/BF01405730), *Policy Sciences*, 4(2), pp. 155 to 169.
- Schön, D. A. (1983) *The Reflective Practitioner: How Professionals Think in Action*. New York: Basic Books.
- W3C (2023) [*Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/). W3C Recommendation.

## Licence and credits

Fastidious is released under the [MIT Licence](LICENSE). The crew and the film stack are fetched from their authors' repositories at install time and stay under their own licences; none of those projects is affiliated with Fastidious or has endorsed it. See [NOTICE.md](NOTICE.md).
