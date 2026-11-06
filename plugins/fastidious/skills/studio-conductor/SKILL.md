---
name: studio-conductor
description: Orchestrates the design skill stack from framing to learning. Sequences skills through the double diamond, settles overlaps, runs gates and keeps a design rationale log. Use to start, resume or steer any multi-skill design project.
---

# Studio conductor

A stack of strong specialist skills does not make a design process. Without a conductor, each skill starts from whatever is in front of it, overlapping skills compete for the same request, decisions go unrecorded, and nobody notices when the work has drifted from its frame. Most of the stack's intelligence also sits in delivery, so the temptation is always to jump straight to building.

This skill holds the thread. It decides where the work currently is, which skill runs next, which skill leads when several could, what must be true before moving on, and why each decision was made. It does not do the specialist work itself. It calls the skills that do, checks their outputs, and keeps two files: `STUDIO-STATE.md` (where things stand) and `DESIGN-RATIONALE.md` (why).

The process follows the Design Council's double diamond, alternating divergence and convergence through discover, define, develop and deliver (Design Council, 2019), with a futures horizon before it and a learning loop after it.

## When to use it

- Starting a design project that will use more than one skill.
- Resuming a project: read `STUDIO-STATE.md` first and continue from there.
- Steering: when the person asks "what next?", when the work feels off, or when evidence contradicts an earlier decision.

For a single, self-contained task (one critique, one copy review), call the specialist skill directly; the conductor is not needed.

## Working rules

0. **The personality is the product.** Every phase serves it: the frame and positioning decide who the work is, the sign and brand systems define how that personality looks and sounds, and delivery expresses it in every detail. At each gate, ask whether the artefact makes the personality clearer or blurs it. Log it in `DESIGN-RATIONALE.md` when a decision trades personality for convenience.
1. **Agree context and communication goals first.** Before any skill runs, confirm the subject, the people it serves, what success looks like and what the person wants from this session.
2. **Diverge before converging, every time.** Each phase opens wide (sources, options, frames, concepts) and only then narrows. Never let a phase begin with a single option.
3. **Variants, then lock.** At every convergence point, the person chooses among variants. Record what was chosen and what was given up.
4. **Never improvise a missing skill silently.** If the pipeline calls for a skill that is not installed, say so, then either run a clearly labelled minimal version inline or ask the person whether to skip it.
5. **Respect sealed artefacts.** Never pass `.analogy-scout/` or any other sealed workings to another skill. Only public handoff files travel.
6. **Evidence can send work backwards.** If later evidence contradicts an earlier decision, return to the phase that made it rather than patching downstream.
7. **Write plainly.** British English, sentence case headings.

## Stage 0: take stock

At the start of every session:

1. **Inventory the skills** available in this session and match them to the phase map below. Mark each as installed or missing. If the job includes promotional film, run `python3 scripts/promo_stack.py check` from the `fastidious` skill's folder (a sibling of this skill's folder) and record the result: the promo stack is pinned, and a version that differs from the lock is a broken dependency.
2. **Inventory the artefacts** already in the project root (`FRAME.md`, `POSITIONING.md`, `BEAT-MAP.md`, `INTERACTION-BASELINE.md`, `TRANSFER-BRIEF.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md`, `REFERENCE-BOARD.md`, `WORLD-BIBLE.md`, `COPY-DECK.md`, `COMPONENT-INVENTORY.md`, `MOBILE-AUDIT.md`, `VERIFICATION-LOG.md`, and for film `BRIEF.md`, `NOTE.md` and the Gauntlet ledger, and so on), with their status (draft or locked) and date.
3. **Check handoff integrity.** For each installed skill, check that the skills and data files it depends on exist. Report any broken dependency before relying on that skill.
4. **Locate the work.** Decide which phase the project is in from the artefacts and the person's account.
5. **Choose a mode** with the person:
   - **Full:** every phase, for new or high-stakes work.
   - **Sprint:** frame, positioning, sign system, brand system, build, assure; for work with an established brief and research base.
   - **Repair:** enter at critique and assurance, then return upstream only where the findings point.
   - **Horizon:** futures and framing only, to explore before committing to anything.

Write the result to `STUDIO-STATE.md`.

## The phase map

Skills marked *(planned)* may not be installed yet; check Stage 0.

| Phase | Purpose | Skills, in order | Exit gate |
| --- | --- | --- | --- |
| **0. Horizon** (optional) | Sense what is changing and which futures matter | futures-cone *(planned)*, deep-research | Key signals and scenarios recorded |
| **1. Discover** | Understand people, context and system | design:user-research, deep-research, systems-mapper *(planned)*, design:research-synthesis | Insights evidenced and synthesised |
| **2. Define** | Choose the problem, the person and the core idea | frame-shifter, positioning-strategist, value-architect *(planned)*, then the route decision in narrative-architect (fit test) | `FRAME.md` and `POSITIONING.md` locked; route chosen; `BEAT-MAP.md` locked on the immersive route |
| **3. Develop: structure and meaning** | Generate and choose how it works and what it means | analogy-scout, morphological-explorer *(planned)*, sign-system-architect, consequence-scanner *(planned)* | `TRANSFER-BRIEF.md` and `SIGN-SYSTEM.md` locked |
| **4. Develop: system and direction** | Turn meaning into tokens, words and a visual direction | brand-system-architect (translating `SIGN-SYSTEM.md` into tokens), reference-curator, world-bible (when the work needs a series of pictures), then the art direction lead (see precedence), then copy-director | `BRAND-SYSTEM.md`, `REFERENCE-BOARD.md` and `COPY-DECK.md` locked, and `WORLD-BIBLE.md` with its anchor frames when there is one; direction chosen from variants |
| **5. Deliver** | Build it | Immersive route: motion-choreographer with gsap-core and gsap-scrolltrigger, render-engineer (only on escalation), asset-director. Conventional route: interaction-minimum-designer. Both routes: detail-craft (signature moments and the detail layer), component-librarian, design:ux-copy (error and empty states, under copy-director), emil-design-eng, design:design-system, design:design-handoff. Film route: showreel-director, directing the pinned promo stack (hyperframes, motionmaxxing, business-motion-film, the elevenlabs skills) and fastidious-motion for generated shots | Build complete end to end; for film, a rendered master |
| **5b. Explain** | Justify every detail before assurance | detail-craft stage F (six-register rationale: personality, persuasion, routes deprioritised, proof, inclusion, craft and cost; tags for meaning, journey, ethics, source) | `DESIGN-RATIONALE-DETAILS.md` complete for every detail; shared with the person |
| **6. Assure** | Check quality, access and performance | detail-craft's detail audit (stage E), design:design-critique, design:accessibility-review (static designs), mobile-auditor, scroll-verifier, accessibility-performance-auditor (final gate). Film: business-motion-film's Gauntlet with fresh critics, motionmaxxing's gates, HyperFrames' check, the flash screen and loudness | Auditor passes; critique and audit findings resolved or logged. Film: the Gauntlet reaches its quality bar and the flash screen passes |
| **7. Learn** | Test what matters and feed it back | the measurement plan from `DESIGN-RATIONALE-DETAILS.md` (register 4), experiment-designer *(planned)* | Assumptions tested; results fed back to the phase they affect |

**Routes.** narrative-architect's fit test decides the route for a website. A pass takes the immersive route; a fail or a plainly conventional site takes the conventional route through interaction-minimum-designer, whose own escalation trigger can still send the build to narrative-architect mid-way. A promotional film (launch or promo film, sizzle reel, hype or teaser) takes the film route. Phases 1 to 3 run as usual, narrative-architect writes the film's `BEAT-MAP.md` without a fit test, and showreel-director runs phases 5 and 6. A film can follow a site build and reuse its artefacts.

**Relationship to build-sequencer.** build-sequencer sequences the build-stage specialists when used alone. When this skill is installed, it owns sequencing and build-sequencer's order is adjusted: frame-shifter runs first, positioning-strategist before brand-system-architect, and sign-system-architect before brand-system-architect. build-sequencer's routing and sequencing rules still apply within the build stages.

Not every project needs every skill. Skip a skill only with a reason, and log the reason.

## Precedence rules

When more than one skill could take a request, this table decides who leads.

| Situation | Lead | Supporting | Not used |
| --- | --- | --- | --- |
| Art direction for a public page or site | design-taste-frontend | impeccable (critique and tuning commands) | frontend-design |
| Art direction for product UI or app screens | impeccable | design-taste-frontend (app-screen run) | frontend-design |
| Neither of the above installed | frontend-design | | |
| Static poster, print piece or artwork | canvas-design | sign-system-architect's brief | web skills |
| Motion for scroll-driven builds | motion-choreographer | gsap-scrolltrigger, gsap-core | |
| Signature moments and the detail layer (premium feel) | detail-craft | motion-choreographer, gsap-scrolltrigger, emil-design-eng | |
| Micro-interaction and component polish | emil-design-eng | gsap-core | |
| 3D or scrubbed video | render-engineer, only when motion-choreographer escalates | | |
| Critique of a design | design:design-critique | impeccable's critique | |
| Accessibility of a static design | design:accessibility-review | | |
| Accessibility and performance of a build | accessibility-performance-auditor (final gate) | | |
| Meaning and signs | sign-system-architect | | art direction and brand skills may not override it |
| Page, film and launch copy | copy-director (`COPY-DECK.md`) | design:ux-copy for error and empty states | |
| A series of pictures in one world (illustration, painting, photography, footage) | world-bible (`WORLD-BIBLE.md`, series critic) | fastidious-motion, asset-director, frame-critic | |
| Brand tokens (colour, type, spacing, motion vocabulary, voice) | brand-system-architect, translating `SIGN-SYSTEM.md` | | |
| The problem and the frame | frame-shifter | | |
| The person, pain and promise | positioning-strategist, inside `FRAME.md` | | |
| Interaction for conventional builds | interaction-minimum-designer | emil-design-eng | motion-choreographer |
| Structure borrowed from elsewhere | analogy-scout (public brief only) | | |
| Promotional film: direction, from brief to delivery | showreel-director | business-motion-film's brief and storyboard rules | |
| Film idea and beats | narrative-architect (`BEAT-MAP.md`) | motionmaxxing's idea kinds, HyperFrames' three storylines | |
| Rendering film | hyperframes, at the pinned version | gsap-core; reel-capture for live sites | video-shotcraft and Remotion, unless the person asks or the project already uses them |
| Motion timing and layout in film | motionmaxxing's craft laws | HyperFrames' motion reference, emil-design-eng | |
| Whose taste a film follows | taste-library (`REFERENCES.md`) | motionmaxxing's measured laws | motionmaxxing's `taste/verdicts.md` (another person's taste) |
| A brand's identity in film | brand-system-architect (`BRAND-SYSTEM.md`) | | motionmaxxing's `brand.mjs`, except when there is no brand system |
| Generated stills and footage | fastidious-motion | | HyperFrames' HeyGen generation, unless the person chooses it |
| Music, sound effects, voice | the elevenlabs skills | HyperFrames' `beats` and `normalize-audio`; business-motion-film's back-timing | |
| Review of a film | business-motion-film's Gauntlet (a fresh critic every round) | motionmaxxing's gates, frame-critic, `flash-check.py` | the builder |

Upstream files outrank downstream preferences. Where a downstream skill's defaults conflict with `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md`, `BRAND-SYSTEM.md` or `TRANSFER-BRIEF.md`, the upstream file wins unless the person decides otherwise, and the decision is logged.

## Running a phase

For each phase:

1. **Brief the skill.** Pass only the files it needs, plus the frame in one sentence. Never pass sealed workings.
2. **Hold the diverge.** Check that the skill produced genuinely different options, not variations of one. If not, send it back.
3. **Converge with the person.** Present the options side by side with their trade-offs. When there are many options against several criteria, use controlled convergence: score each against the criteria relative to a reference option, prune the weakest, combine strengths, and repeat until one or two remain (Pugh, 1991).
4. **Check the gate.** Confirm the phase's exit criteria are met before moving on.
5. **Log the decision** in `DESIGN-RATIONALE.md`.
6. **Update `STUDIO-STATE.md`.**

## The rationale log

`DESIGN-RATIONALE.md` records every significant decision using a questions, options and criteria structure (MacLean et al., 1991). It is what lets anyone, including a future session, understand why the work is as it is, and what to revisit if circumstances change.

```markdown
## D<number>: <decision in a few words>

- Date and phase:
- Question: what was being decided
- Options considered: including the null option
- Criteria: what mattered, and how much
- Chosen: and by whom
- Given up: what the rejected options offered
- Evidence: what supported the choice; what was assumed
- Reversible: yes, no, or at what cost
- Revisit if: the condition that would reopen this decision
- Produced by: the skill or session that generated the options
```

Log at least: the mode, the frame, the fit test result, the chosen transfer learnings, the sign system position, the art direction choice, any skipped skill, any backward step, and any override of an upstream file.

## Backward steps

When evidence contradicts a locked decision:

1. Name the decision (by its log number) and the evidence.
2. Identify the earliest phase affected.
3. Tell the person what would need to be redone, and what can stand.
4. With agreement, return to that phase, rerun it, and mark downstream artefacts as stale in `STUDIO-STATE.md` until they are revised.

Patching downstream to avoid revisiting a frame is the most common way a well-crafted build ends up solving the wrong problem.

## Output: STUDIO-STATE.md

```markdown
# Studio state: <project>

Mode: <full | sprint | repair | horizon> · Current phase: <n. name> · Updated: <date>

## Goal
Subject, people served, success, what this session is for.

## Skills
Installed and missing, against the phase map. Broken dependencies.

## Artefacts
File, status (draft, locked, stale), date, producing skill.

## Next
The next skill to run, what it needs, and what decision it feeds.

## Open questions and assumptions
Linked to rationale log entries.
```

## Anti-patterns

- **Jumping to build:** starting in deliver because the delivery skills are the strongest.
- **Single-option phases:** converging on the first idea a skill produces.
- **Silent substitution:** a missing skill quietly replaced by improvisation.
- **Precedence by accident:** whichever skill triggered first leads.
- **Unlogged overrides:** a downstream choice that contradicts an upstream file without a recorded decision.
- **Leaky handoffs:** passing sealed or irrelevant files between skills.
- **Patching instead of returning:** fixing symptoms downstream when the frame is wrong.

## References

- Design Council (2019) *Framework for Innovation: Design Council's Evolved Double Diamond*. London: Design Council.
- MacLean, A., Young, R. M., Bellotti, V. M. E. and Moran, T. P. (1991) 'Questions, options, and criteria: elements of design space analysis', *Human-Computer Interaction*, 6(3 and 4), pp. 201 to 250.
- Pugh, S. (1991) *Total Design: Integrated Methods for Successful Product Engineering*. Wokingham: Addison-Wesley.
