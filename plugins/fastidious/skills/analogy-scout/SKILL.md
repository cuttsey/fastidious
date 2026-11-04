---
name: analogy-scout
description: Cross-domain inspiration for design. Finds mature source domains, extracts their structural learnings and hands on only source-free lessons in TRANSFER-BRIEF.md. Sources stay sealed unless the person asks.
---

# Analogy scout

Immature domains rarely need new inventions. They need structures a mature domain has already proven: how it sequences discovery, admits newcomers, proves value, builds belonging, paces effort and reward. Analogy is how those structures are found.

This is an **inspiration skill, not a content skill.** The source domains it consults are where learnings come from. They are not material for the work. Nothing from a source, whether its name, vocabulary, imagery, examples or tone, may enter the build context unless the person expressly asks for it. What travels forward is the lesson, restated entirely in the target's own terms, as if it had been thought of from inside the target.

The reason is practical as well as principled. Once a source is in the context, every downstream step is primed by it: copy borrows its words, art direction borrows its look, and the work becomes a costume of the source. Exposure to an example makes designers reproduce its features, even unwanted ones (Jansson and Smith, 1991). Sealing the sources is how this skill gets the benefit of analogy without the fixation.

## The two governing principles

1. **Transfer relations, not attributes.** A productive analogy maps the relations between things (A enables B, A earns access to B, A precedes and prepares for B), not their surface features. Mappings that carry a connected system of relations are stronger than isolated matches (Gentner, 1983; Gentner and Markman, 1997).
2. **Seal the sources.** Sources are consulted, never carried. The only output other skills see is a source-free brief.

## Where it sits in the pipeline

Run it after `narrative-architect` has produced `BEAT-MAP.md` (or after the brief is agreed) and before `sign-system-architect`.

- **Reads:** the brief, `BEAT-MAP.md` if present, research about the subject and its audiences.
- **Writes, sealed:** `.analogy-scout/WORKINGS.md` (sources, mappings, scores, lexicon). No other skill reads this folder.
- **Writes, public:** `TRANSFER-BRIEF.md` in the project root. Source-free.
- **Hands to:** `narrative-architect`, `sign-system-architect`, `motion-choreographer` and the build skills, through `TRANSFER-BRIEF.md` only.

## Sealing rules

These rules override everything else in this file.

1. **Isolate the search.** When a subagent or task tool is available, run Stages 2 to 6 inside a separate agent and have it return only what Stage 7 needs. The sources then never enter the main context at all. When no subagent is available, do the work, write it to the sealed workings file, and do not echo source material in replies.
2. **Never name a source in the public brief,** in handoff notes, in replies that feed the build, or in any file another skill reads. This includes indirect identifiers: the source's jargon, characteristic objects, famous examples, people and places.
3. **No quarantine lists for other skills.** Telling a downstream skill what not to use names it, and naming primes. Leak prevention is this skill's own job (Stage 8 and audit mode).
4. **Present choices by learning, not by source.** When offering variants, describe what each would change in the target. The person may ask to see the sources behind any variant; show them only then.
5. **Express permission is specific.** If the person asks to reveal a source, to credit it, or to use one visible metaphor from it, do exactly that and no more. Record the permission and its scope at the top of the workings file and in the brief's status line. Permission for one source or one use does not unseal the rest.
6. **This file's examples are illustrations, not candidates.** Never reuse an example from this skill as a source in a real run.

## Working rules

1. **Agree the problem before searching.** Confirm what is immature about the target and what the person most wants to change.
2. **Source widely before narrowing.** Retrieval must reach far domains, not just neighbours.
3. **Offer variants, then lock.** Three learnings sets at different distances; the person chooses or combines.
4. **Be accurate about the source.** Learnings must rest on mechanisms that really work in the source. Verify with research tools where available; mark unverified claims in the workings.
5. **Name where it breaks.** Every analogy fails somewhere; the brief must carry the design response, stated in target terms.
6. **Write plainly.** British English, sentence case headings, a one-line gloss for any technical term.

## The method

Stages 1 and 7 to 9 are visible. Stages 2 to 6 are sealed.

### Stage 1: frame the target and its maturity gap (visible)

Write, in the person's words where possible:

- **Target:** the domain and the thing being designed.
- **Maturity gap:** what the target does poorly that mature domains do well. Typical gaps: explaining invisible value, admitting newcomers, sequencing learning, proving credibility, building belonging, sustaining return visits, earning money without losing soul, handing down knowledge.
- **Audience shift:** who should move from what to what.
- **Constraints:** what cannot change.

Choose the one to three gaps that matter most.

### Stage 2: abstract the problem (sealed)

People rarely retrieve useful distant analogies unprompted, because memory favours surface similarity. They succeed far more often when the problem is re-described abstractly, or when they compare several cases and extract a shared schema (Gick and Holyoak, 1980, 1983).

For each gap, climb an abstraction ladder, writing each rung with **no nouns from the target domain**:

1. **Concrete:** the problem as the target describes it.
2. **Functional:** what must be achieved.
3. **Relational:** the structure of the problem, for example "a practice whose value is felt by participants but invisible to observers until they are shown how to notice".
4. **Contradiction:** the tension to resolve, in the manner of TRIZ (Altshuller, 1984), for example "legible to newcomers without being simplified for experts".

Write at least three relational statements and two contradictions per gap.

### Stage 3: retrieve at three distances (sealed)

Find domains that are **mature in that exact relation**, with evidence that their mechanism works.

| Distance | Definition | Strength | Risk |
| --- | --- | --- | --- |
| **Near** | adjacent categories in the same broad field | high fit | low novelty |
| **Middle** | different field, similar kind of human activity | balance of fit and freshness | hard to spot without abstraction |
| **Far** | unrelated field | highest originality | weaker fit |

The evidence on distance is mixed: far-field analogies have produced more original designs (Dahl and Moreau, 2002), while engineering design studies suggest near and moderate analogies can be more workable (Christensen and Schunn, 2007; Fu et al., 2013). Generate across all three.

Force breadth with these lenses, at least one candidate per lens:

- **Direct:** where else is this exact function performed? (Gordon, 1961)
- **Personal:** become the person or element in the problem; what would you need, and who provides it? (Gordon, 1961)
- **Symbolic:** compress the contradiction into a two-word paradox and ask which domains live inside it. (Gordon, 1961)
- **Fantasy:** remove a constraint; which real domain is closest to that world? (Gordon, 1961)
- **Biological:** how does nature solve this relation? (Benyus, 1997)
- **Historical:** which older practice faced this, and how did it survive or revive?
- **Institutional:** which institution turned this into a repeatable system?

At least 15 candidates per gap, at least 5 far.

### Stage 4: map structurally and score (sealed)

For the strongest 6 to 8 candidates, build a relation table (source element, relation in source, target element, relation in target, holds or not). Apply the mapping constraints (Gentner, 1983; Holyoak and Thagard, 1995): one-to-one correspondence, parallel connectivity, systematicity (chains of relations over single matches) and purpose (it must serve the gap).

Score 1 to 5 on systematicity, structural consistency, purpose fit, source maturity, novelty and transferability. Reject anything that matches only on attributes.

### Stage 5: stress-test (sealed)

- **Candidate inferences:** what does the source predict about the target that nobody has considered? These are the main payoff (Gentner and Markman, 1997).
- **Verification:** mark each inference true, false or unknown for the target. Unknowns become research questions.
- **Breaking points:** where the analogy fails (stakes, ethics, scale, audience, risk, culture), and the design response.
- **Baggage:** connotations of the source that must not cross over.

### Stage 6: extract the schema (sealed)

When analogies from different sources share structure, write the common schema in plain, source-free language. A schema abstracted from several sources transfers more reliably than any single analogy (Gick and Holyoak, 1983), and it is naturally sealed, because it belongs to no one source. Prefer schemas over single sources. Where two sources combine into structure neither has alone, record the blend (Fauconnier and Turner, 2002).

Then build the **leak lexicon**: every word, name, object, image type, colour association and phrase that identifies any consulted source. Store it in the workings file.

### Stage 7: translate into learnings (visible)

Restate every transferable mechanism as a **learning in the target's own terms**, written as if it had been discovered from inside the target. A good learning has four parts:

- **Learning:** the mechanism, in target vocabulary.
- **Why it works:** the relation it exploits, stated abstractly.
- **Where it applies:** which gap, audience and beats.
- **Limit:** the breaking point and the design response, in target terms.

Mechanisms worth looking for: sequence and pacing of discovery, thresholds of belonging, roles and movement between them, vocabulary of noticing, proof structures, progression and mastery, wayfinding, participation models, rhythm of return, economic model.

Also write the **open questions**: the unknown inferences from Stage 5, restated as research questions about the target.

### Stage 8: leak check (visible result)

Before anything is shown or written publicly, check the draft brief:

1. **Lexicon scan.** Search the brief for every term in the leak lexicon, case-insensitively, including plurals and near forms. Any hit is a leak; rewrite it.
2. **Identifiability test.** Read the brief cold. Could a reader guess the source domain? If yes, the phrasing still carries its fingerprint; abstract further.
3. **Noun test.** If removing a learning's nouns leaves no mechanism, it was surface, not structure; return to Stage 4.
4. **Insider test.** Would a practitioner of the target recognise each learning as true to their practice?

Record pass or fail for each test in the workings and the brief.

### Stage 9: variants and lock (visible)

Present three learning sets, ideally drawn from one near, one middle and one far schema. Describe each only by what it would change in the target: the learnings, the beats it would reshape, its risk. Offer, in one line, to reveal the sources behind any variant if the person wants them.

Lock the chosen set, write `TRANSFER-BRIEF.md`, and run Stage 8 again on the final file.

## Audit mode

Invoke later with "audit" to check downstream artefacts for leakage: `BEAT-MAP.md`, `SIGN-SYSTEM.md`, copy decks, component names, alt text and the built pages. Scan each against the sealed leak lexicon, report hits by file and line, and propose target-native rewrites. The audit report names the matched terms only to this skill's sealed workings; the public report lists file, line and suggested rewrite.

## Anti-patterns

- **Source in the brief:** any source name, jargon or famous example in a file other skills read.
- **"X for Y":** borrowing a brand's name instead of a mechanism.
- **Theme parks:** dressing the target in the source's costume.
- **Attribute matching:** sources chosen for a shared surface trait.
- **Immature sources:** mechanisms that do not actually work in their own domain.
- **Single-source fixation:** locking onto the first analogy found (Jansson and Smith, 1991).
- **Priming by prohibition:** warning other skills about a source's look, which names it.
- **Analogy as copy:** writing the comparison into headlines instead of building the mechanism into the experience.

## Outputs

### TRANSFER-BRIEF.md (public, source-free)

```markdown
# Transfer brief: <project>

Status: <locked | draft> · Sources: sealed <or: revealed by request, scope> · Date: <date>

## Maturity gap
Target, gaps chosen, audience shift, constraints.

## Learnings
For each: learning, why it works, where it applies, limit and design response.

## Schema
The structure behind the learnings, in one or two plain sentences.

## Open questions
Research questions about the target.

## Beat implications
What changes in BEAT-MAP.md, in target terms.

## Leak check
Lexicon scan, identifiability, noun, insider: pass or fail.
```

### .analogy-scout/WORKINGS.md (sealed)

Abstractions, all candidates with distance and lens, mapping tables, scores, inferences and their status, breaking points, baggage, schema derivation, leak lexicon, and any express permissions with their scope. Suggest adding `.analogy-scout/` to `.gitignore` and to any build or deploy exclusion, unless the person wants it kept.

## References

- Altshuller, G. (1984) *Creativity as an Exact Science: The Theory of the Solution of Inventive Problems*. New York: Gordon and Breach.
- Benyus, J. M. (1997) *Biomimicry: Innovation Inspired by Nature*. New York: William Morrow.
- Christensen, B. T. and Schunn, C. D. (2007) 'The relationship of analogical distance to analogical function and preinventive structure: the case of engineering design', *Memory and Cognition*, 35(1), pp. 29 to 38.
- Dahl, D. W. and Moreau, P. (2002) 'The influence and value of analogical thinking during new product ideation', *Journal of Marketing Research*, 39(1), pp. 47 to 60.
- Fauconnier, G. and Turner, M. (2002) *The Way We Think: Conceptual Blending and the Mind's Hidden Complexities*. New York: Basic Books.
- Fu, K., Chan, J., Cagan, J., Kotovsky, K., Schunn, C. and Wood, K. (2013) 'The meaning of "near" and "far": the impact of structuring design databases and the effect of distance of analogy on design output', *Journal of Mechanical Design*, 135(2).
- Gentner, D. (1983) 'Structure-mapping: a theoretical framework for analogy', *Cognitive Science*, 7(2), pp. 155 to 170.
- Gentner, D. and Markman, A. B. (1997) 'Structure mapping in analogy and similarity', *American Psychologist*, 52(1), pp. 45 to 56.
- Gick, M. L. and Holyoak, K. J. (1980) 'Analogical problem solving', *Cognitive Psychology*, 12(3), pp. 306 to 355.
- Gick, M. L. and Holyoak, K. J. (1983) 'Schema induction and analogical transfer', *Cognitive Psychology*, 15(1), pp. 1 to 38.
- Gordon, W. J. J. (1961) *Synectics: The Development of Creative Capacity*. New York: Harper and Row.
- Hofstadter, D. and Sander, E. (2013) *Surfaces and Essences: Analogy as the Fuel and Fire of Thinking*. New York: Basic Books.
- Holyoak, K. J. and Thagard, P. (1995) *Mental Leaps: Analogy in Creative Thought*. Cambridge, MA: MIT Press.
- Jansson, D. G. and Smith, S. M. (1991) 'Design fixation', *Design Studies*, 12(1), pp. 3 to 11.
