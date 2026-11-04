---
name: frame-shifter
description: Problem framing for design. Questions the brief, uncovers what the problem really is, and offers alternative frames before anything is designed. Produces FRAME.md for the rest of the pipeline.
---

# Frame shifter

Most failed design work answers the wrong question well. The brief arrives already framed, usually as a solution in disguise ("we need a new website", "make the onboarding shorter"), and every skill downstream inherits that frame without questioning it.

This skill does the questioning. It digs beneath the brief to the problem situation, finds the paradox that makes it hard, maps the wider field of people involved, and generates alternative frames: new ways of seeing the situation that open up new solutions. It tests each frame against evidence, then hands the chosen one forward as `FRAME.md`.

Framing is the core act of design, not a preliminary to it (Schön, 1983; Dorst, 2011). Design problems are typically wicked: they have no definitive formulation, and every formulation already implies a direction of solution (Rittel and Webber, 1973; Buchanan, 1992). So the choice of frame is a design decision, and should be made deliberately.

## Where it sits in the pipeline

Run it first in the define phase: after any discovery research and futures work, before `narrative-architect`, `analogy-scout`, `value-architect` or any concept work.

- **Reads:** the brief as given, research outputs (`research-synthesis`, `deep-research` reports), any futures or scenario files, and the person's own account of the situation.
- **Writes:** `FRAME.md` in the project root.
- **Hands to:** `narrative-architect` (the reframed brief and the one-sentence frame become its starting point), `analogy-scout` (the abstracted problem and its contradiction), `sign-system-architect` (the core tension often suggests the semiotic square's opposition), and `studio-conductor` (the decision and its assumptions for the rationale log).

Re-run it when evidence contradicts the frame, when a build keeps solving the wrong thing, or when the brief owner changes.

## Working rules

1. **Agree the situation before reframing.** Hear the person's account in full and confirm it back before generating anything. Do not proceed on a guess when the person is present to ask.
2. **Keep the original frame in play.** The brief as given is always one of the candidate frames (the null frame). Reframing is an offer, not an override; sometimes the original frame wins, and that is a legitimate result.
3. **Source widely before narrowing.** Gather definitions of the problem from several people and several categories before converging.
4. **Offer variants, then lock.** Present several frames; the person chooses. Only then write the final file.
5. **Separate evidence from assumption.** Every frame rests on claims. Mark each as evidenced, assumed or contradicted.
6. **Write plainly.** British English, sentence case headings, no method jargon in the output without a one-line gloss.

## The method

The stages adapt Dorst's frame creation model (Dorst, 2011, 2015) and Wedell-Wedellsborg's reframing practices (2017, 2020).

### Stage 1: archaeology of the brief

Reconstruct how the problem came to be stated this way.

- **The brief as given,** verbatim.
- **Who wrote it,** for whom, and what prompted it now.
- **Embedded solution:** what solution does the brief already assume? Rewrite the brief with that solution removed.
- **Previous attempts:** what has been tried, by whom, and why it did not work. Earlier failures often reveal the frame that keeps failing.
- **The stated objective,** and the objective behind it. Ask "why does that matter?" until the answer is a value a person would recognise, then ask "what stops us?" to find the obstacles that shape the problem (a laddering technique from Basadur's challenge mapping; Basadur, 1995).

### Stage 2: the paradox

State the core of the problem as a paradox: two needs or forces that cannot both be met under the current frame. Write it as "We need X, but X undermines Y."

The paradox is what makes the problem hard, and it is what any good frame must dissolve rather than split down the middle. If there is no paradox, the problem may not need design at all, only execution; say so.

### Stage 3: the wider field

Map the people and forces involved, beyond the obvious ones.

- **Core:** the people the brief names.
- **Context:** the people and organisations around them who shape or are shaped by the problem.
- **Field:** the wider world the problem sits in, including people who are absent, unheard or who bear consequences without a voice.

For each group, record **their own definition of the problem**, in their words where research allows. Collect definitions in writing before discussing them, so they are not flattened into consensus (Wedell-Wedellsborg, 2017).

Then look for **positive exceptions**: places, people or moments where the problem does not occur, despite similar conditions. What they do differently is often the best clue to a better frame (Pascale, Sternin and Sternin, 2010).

### Stage 4: themes

Look beneath the stated needs of each group for the deeper **themes**: the underlying human needs, motivations and experiences shared across the field, such as recognition, safety, belonging, mastery, fairness or meaning. Themes are where frames come from, because they connect the people in the field to one another (Dorst, 2015).

List four to eight themes, each with the evidence that supports it.

### Stage 5: generate frames

A frame is a proposition of the form:

> **If we approach the situation as if it were ___, then ___ becomes possible.**

It works by design abduction: when only the desired value is known, the designer proposes a way of seeing (the frame) and a working principle together, and tests whether they lead to that value (Dorst, 2011).

Generate five to seven frames, including:

- **The null frame:** the brief as given.
- **At least one frame from each of** a different category of problem (is this really a motivation problem, a trust problem, a timing problem, a status problem, an information problem?), a different stakeholder's definition, a positive exception, and a deep theme.
- **At least one frame that questions the objective itself:** what if the goal as stated is the wrong goal?

For each frame give:

- the "if we approach it as if…" statement
- the working principle it implies
- the value it would create, for whom
- how it dissolves the paradox
- the evidence for it, and what it assumes

### Stage 6: futures check

For each strong frame, ask how it holds up over time and across plausible futures. If a futures or scenario file exists, test each frame against the scenarios. A frame that only works in today's conditions is fragile; note it.

### Stage 7: evaluate and choose

Score each frame from 1 to 5:

| Criterion | Question |
| --- | --- |
| Value | Does it create real value for the people in the field, not just the brief owner? |
| Paradox | Does it dissolve the paradox rather than trade one side off against the other? |
| Evidence | How well do research and positive exceptions support it? |
| Generativity | Does it open up solutions the original frame could not reach? |
| Feasibility | Can the organisation act on it within its constraints? |
| Ownership | Would the brief owner recognise it and be willing to adopt it? |

Present the strongest three alongside the null frame. Ask the person to choose, combine or redirect. If the person is not available, choose the highest-scoring frame, keep the null frame as the documented alternative, and say so at the top of the file.

### Stage 8: transform the brief

Rewrite the brief through the chosen frame:

- **The frame,** in one sentence a stranger could repeat.
- **The reframed brief,** in a short paragraph.
- **How might we questions:** three to five, each opening a different line of solution, none so narrow it contains the answer nor so broad it gives no direction.
- **Success, restated:** what would show the frame was right.
- **Assumptions to test:** the riskiest claims the frame rests on, ranked by importance and weakness of evidence. These go to `experiment-designer` if installed, or to `studio-conductor`'s log if not.

## The tests

Run these on the chosen frame and record the result.

1. **Repeat test.** Can a stranger repeat the frame after hearing it once?
2. **Difference test.** Would designing to this frame produce clearly different work from designing to the null frame? If not, it is a restatement, not a reframe.
3. **Paradox test.** Is the paradox from Stage 2 dissolved, or merely split?
4. **Field test.** Does the frame serve people in the wider field, or only the brief owner?
5. **Evidence test.** Is every load-bearing claim either evidenced or listed as an assumption to test?

## Anti-patterns

- **Solution as problem:** accepting "we need an app" as the problem.
- **Reframing for its own sake:** a clever frame that the evidence does not support or the owner will not adopt.
- **Consensus flattening:** merging stakeholders' definitions into one bland statement and losing the tensions that matter.
- **Splitting the paradox:** a compromise frame that half-serves both needs.
- **The single frame:** generating one alternative and treating the choice as binary.
- **Lost null frame:** discarding the original brief so its strengths and the reasons for it are forgotten.

## Output: FRAME.md

```markdown
# Frame: <project>

Status: <locked | draft> · Chosen frame: <name> · Date: <date>

## The frame
One sentence.

## Reframed brief
Short paragraph.

## How might we
Three to five questions.

## Archaeology
Brief as given; embedded solution; previous attempts; objective ladder.

## Paradox
"We need X, but X undermines Y."

## Field
Core, context and field, each with their own definition of the problem. Positive exceptions.

## Themes
Each with evidence.

## Frames considered
Null frame and alternatives, each with statement, principle, value, paradox resolution, evidence, scores.

## Why this frame
The comparison, and what was given up.

## Success
What would show the frame was right.

## Assumptions to test
Ranked by importance and weakness of evidence.

## Test results
Repeat, difference, paradox, field, evidence.

## Handoff notes
- narrative-architect: <...>
- analogy-scout: <abstracted problem and contradiction>
- sign-system-architect: <core tension>
- studio-conductor: <decision and assumptions for the log>

## References
```

## References

- Basadur, M. (1995) *The Power of Innovation: How to Make Innovation a Way of Life and Put Creative Solutions to Work*. London: Pitman.
- Buchanan, R. (1992) 'Wicked problems in design thinking', *Design Issues*, 8(2), pp. 5 to 21.
- Dorst, K. (2011) 'The core of "design thinking" and its application', *Design Studies*, 32(6), pp. 521 to 532.
- Dorst, K. (2015) *Frame Innovation: Create New Thinking by Design*. Cambridge, MA: MIT Press.
- Pascale, R., Sternin, J. and Sternin, M. (2010) *The Power of Positive Deviance*. Boston: Harvard Business Press.
- Rittel, H. W. J. and Webber, M. M. (1973) 'Dilemmas in a general theory of planning', *Policy Sciences*, 4(2), pp. 155 to 169.
- Schön, D. A. (1983) *The Reflective Practitioner: How Professionals Think in Action*. New York: Basic Books.
- Wedell-Wedellsborg, T. (2017) 'Are you solving the right problems?', *Harvard Business Review*, 95(1), pp. 76 to 83.
- Wedell-Wedellsborg, T. (2020) *What's Your Problem? To Solve Your Toughest Problems, Change the Problems You Solve*. Boston: Harvard Business Review Press.
