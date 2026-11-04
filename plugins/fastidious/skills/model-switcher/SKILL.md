---
name: model-switcher
description: Keeps model costs low by running each step on the cheapest Claude model and effort that does it well, and switching only at sensible boundaries. Use at the start of a session, before delegating to subagents, when the kind of work changes, or when the person asks about cost.
---

# Model switcher

Most of a session's tokens go on work that does not need the strongest model: moving files, checking links, reading logs, applying a decided design. A small share goes on the decisions that do. Matching the model to each step, rather than to the whole session, is the largest single saving available, and it costs nothing in quality when the routing is right.

## What the models cost

List prices per million tokens, from the [Claude pricing page](https://platform.claude.com/docs/en/about-claude/pricing). Check that page before quoting figures to anyone; prices change.

| Model | Alias | Input | Output | Cache read |
| --- | --- | --- | --- | --- |
| Claude Haiku 5.5 (prompts up to 100k tokens) | `haiku` | $0.10 | $0.50 | $0.01 |
| Claude Haiku 5.5 (prompts over 100k tokens) | `haiku` | $0.50 | $2.50 | $0.05 |
| Claude Sonnet 5.5 | `sonnet` | $2 | $10 | $0.10 |
| Claude Opus 5.5 | `opus` | $4 | $20 | $0.20 |
| Claude Fable 5.1 | `fable` | $10 | $50 | $0.25 |

Rules of thumb that follow:

- Opus costs twice Sonnet, and Sonnet costs twenty times Haiku on short prompts. Haiku becomes five times dearer once a prompt passes 100k tokens, so keep Haiku work in small contexts.
- Output costs five times input on every model, and thinking is billed as output. Effort level moves cost as much as model choice.
- Batch API work is half price where nothing needs an immediate answer.
- On a subscription plan the same logic protects usage limits instead of money. Fable can bill to usage credits on some plans.

## The ladder

Classify the next step, then use the lowest rung that does it well.

| Rung | Work | Model | Effort |
| --- | --- | --- | --- |
| 1. Mechanical | Renaming and moving files, formatting, link and spelling checks, extracting or converting data, summarising logs or test output, taking screenshots, filling templates | `haiku` | `low` |
| 2. Routine build | Implementing a decided design, components, tests, copy edits, refactors with a clear spec, research summaries, most coding | `sonnet` | `medium` |
| 3. Judgement | Framing, positioning, meaning and art direction choices, architecture, a bug that has survived two attempts, final review gates | `opus` | `medium`, `high` when stakes are high |
| 4. Exceptional | Long, novel, very hard work where Opus has already fallen short | `fable` | only when the person asks for it by name |

Defaults for the Fastidious crew. Fastidious's build specialists already carry these in their own `model:` frontmatter; keep this list and those lines in step, and change a line only with evidence.

- Rung 3, `opus`: brand-system-architect and positioning-strategist (wrong calls here are the most expensive to unwind), narrative-architect, frame-shifter, sign-system-architect, studio-conductor's gates.
- Rung 2, `sonnet`: build-sequencer, interaction-minimum-designer, reference-curator, component-librarian, motion-choreographer, emil-design-eng and the build skills, design critique.
- Rung 1, `haiku`: mobile-auditor, scroll-verifier and accessibility-performance-auditor, which run fixed checklists and scripts such as `scripts/legibility-check.js`, plus link checks, ledger and reference bookkeeping and file conversions. A checklist agent that finds a failure reports it; deciding the fix goes back up to the stage that owns it.

Escalate on evidence, not unease: two failed attempts, or a decision that is hard to reverse, moves the step up one rung. Once the hard step is done, come back down.

## How to switch in Claude Code

All of these are documented in [model configuration](https://code.claude.com/docs/en/model-config), [subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills) and [the advisor tool](https://code.claude.com/docs/en/advisor).

- **The session:** `/model sonnet`, or `/model` and press `s` to switch for this session only without changing the saved default. At launch: `claude --model sonnet`.
- **A subagent:** `model: haiku` (or `sonnet`, `opus`, `fable`, `inherit`, or a full model ID) in its frontmatter. A per-invocation `model` parameter overrides it. `CLAUDE_CODE_SUBAGENT_MODEL` sets a fallback for subagents without one. Subagents set to `inherit` follow `/model` switches, so a switch to Opus makes them Opus too; pin cheap subagents explicitly.
- **A skill:** `model:` in SKILL.md frontmatter applies for the rest of the current turn and is not saved; `effort:` sets the effort while the skill is active; `context: fork` runs the skill in its own subagent.
- **Plan on Opus, build on Sonnet:** `/model opusplan` uses Opus in plan mode and Sonnet for execution.
- **Strong model only at decision points:** `/advisor opus` with a Sonnet or Haiku main model. Claude consults the advisor before committing to an approach, when an error recurs and before declaring work done. Haiku main with an Opus advisor is the documented lowest-cost pairing with strong planning.
- **Effort:** `/effort low|medium|high|xhigh|max`. Haiku, Sonnet and Opus 5.5 default to `medium`. `max` is prone to overthinking; test before relying on it. Thinking cannot be turned off on the 5.5 models or Fable, so lower the effort instead.

## Switch at boundaries, protect the cache

Changing the main model mid-session throws away the prompt cache, so the next request pays full price for the whole conversation. Turning the advisor on or off does not.

- Switch the main model at natural boundaries: a new task, or straight after `/clear`.
- For a one-off cheap step inside expensive context, delegate it to a Haiku subagent rather than flipping the main model there and back.
- For a one-off hard step inside cheap context, use the advisor or a single Opus subagent rather than switching the whole session.

## Spend fewer tokens in the first place

The cheapest token is the one never sent ([managing costs](https://code.claude.com/docs/en/costs)).

- `/clear` between unrelated tasks; it costs nothing. `/compact` is itself a large request, so use it for continuity, not as a reset.
- Keep `CLAUDE.md` under about 200 lines and move workflow detail into skills, which load only when used.
- Send verbose work (test runs, log reading, documentation fetching) to subagents so only the summary returns.
- Disable MCP servers that are not in use; prefer a CLI where one exists.
- Write specific prompts. "Add validation to the login form in auth.ts" reads two files; "improve the codebase" reads all of them.
- Check `/usage` at the end of a session. Its breakdown shows which skills and subagents used the most.

## Each time, in order

1. Name the rung for the next step.
2. If a cheaper rung fits, use it: delegate with a model set, or switch at the next boundary.
3. Tell the person in one line when switching, for example "Switching to Haiku for the link check."
4. Escalate on evidence; de-escalate when the hard part is done.
5. When studio-conductor is running, note which rung ran each phase in `STUDIO-STATE.md`, so costs can be reviewed later.

## Never

- Choose Fable unless the person asks for it by name.
- Override a model the person assigned to a step.
- Downgrade a hard-to-reverse decision to save money.
- Switch the main model back and forth every few turns; the lost cache costs more than the saving.
