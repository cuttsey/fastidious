---
name: copy-director
description: Writes and edits the words of a site, film or brand book so they sell plainly and sound like no one else. Turns the positioning, beats and voice into a spine line, three-beat claims, honest disclosures, a fit statement, an FAQ ordered as objections and every piece of microcopy, then lints the result. Produces COPY-DECK.md. Use for any page copy, headline, call to action, FAQ or launch text in a Fastidious project.
---

# Copy director

Most generated copy fails in the same three ways. It is general where it should be specific ("innovative solutions for modern businesses"), it is inflated where it should be calm ("elevate", "unlock", "seamless"), and it hides the terms a careful reader is looking for. Readers notice within a line. The words are often the first part of a site to read as machine-made, and the last part anyone fixes.

The best pages in the exemplar set do the opposite. They say one thing in a line a stranger could repeat, they state the terms early, they say who the offer is not for, and they answer objections in the order a sceptic raises them. Their pictures do the feeling; their words do the selling.

This skill writes those words. It does not invent the promise (that is `positioning-strategist`), the story (`narrative-architect`) or the voice (`brand-system-architect`). It turns all three into lines, checks every line against the facts, and hands the build a deck it can set without rewriting.

## Where it sits in the pipeline

- **Runs:** after `BRAND-SYSTEM.md` holds the voice and `BEAT-MAP.md` holds the beats, and before the build sets any text. On the conventional route, after `POSITIONING.md` and `BRAND-SYSTEM.md`.
- **Reads:** `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md` (its Copy channel and anchorage lines), `BRAND-SYSTEM.md` (voice), `BEAT-MAP.md`, `WORLD-BIBLE.md` if there is one, and the facts the person supplies.
- **Writes:** `COPY-DECK.md` in the project root, from `templates/COPY-DECK.md`.
- **Hands to:** the build (every line by key), `motion-choreographer` and `detail-craft` (line breaks, which line lands on which beat), `showreel-director` (supers), `world-bible` (the claim each scene carries), and `detail-craft` stage F (the persuasion register of the rationale).
- **Leads:** all page, film and launch copy. `design:ux-copy` supports it for error messages and empty states.

## Working rules

1. **Every claim is true and can be shown.** Each factual line in the deck points to its evidence in the proof inventory. No invented numbers, clients, quotes, ratings, awards or deadlines. If a line needs a fact the project does not have, ask for it or cut the line.
2. **Scarcity, urgency and social proof only when real.** "A few partners at a time" is fine if it is true and stays true. A countdown that resets is a lie. Name the source of any number.
3. **Specific beats general.** A concrete noun, a number with its unit, a named method. If a line would survive the swap test (put a competitor's name in it and it still reads true), rewrite it.
4. **Calm beats loud.** No exclamation marks, no superlatives without evidence, no words from the cliché list in `references/devices.md`. Confidence comes from plain statements of what happens.
5. **The house style holds.** British English, sentence case, no em dashes, and none of the "it isn't X, it's Y" shape: say what the thing is. Prefer short sentences; most should be under 20 words, and none over 25 ([GOV.UK](https://www.gov.uk/guidance/content-design/writing-for-gov-uk) uses 25 as its ceiling).
6. **Variants, then lock.** The spine and the hero are chosen by the person from three variants that differ in device, not in wording. Record the choice with `option-ledger` (`O-` for each variant, `D-` for the decision).
7. **Write for the beat, not the page.** Each line is written for where it lands: the scene under it, the time it is on screen, the width it is set at.

## Stage 1: Gather

Build three lists in the deck before writing a line.

- **The promise**, from `POSITIONING.md`: the one person, their pain and the promise a competitor could not copy.
- **The proof inventory:** every fact the copy may use, each with its source. Terms (price, model, guarantee, what the client keeps), method, credentials, numbers, people. Mark each as verified, supplied by the person, or missing.
- **The objection ledger:** the doubts the reader brings, in the order they will raise them. Get them from research where it exists; otherwise walk the decision through each person who has a say (the user, the buyer, whoever signs off, whoever pays) and write what each fears. Typical order for a service: what does it cost, what exactly do I get, why this model, how is it measured, how long, what if it goes wrong, why you.

## Stage 2: The spine

The spine is the line that opens and closes the work. It states the idea and the position in one breath. Write three variants, each using a different device from `references/devices.md`:

- **Antithesis:** what this is set against what the category is ("a partner in the upside" set against "an agency on the clock").
- **The turn:** a familiar phrase turned at the end so it says something new.
- **The name:** a line that makes the name mean the promise. Use it once, and only when the name genuinely carries it.

Test each against the swap test, read it aloud, and check it against the sign system's myth. The person chooses. The chosen spine appears as the first statement and returns, unchanged or answered, at the close.

## Stage 3: Claims and beats

For each beat in `BEAT-MAP.md`, write the claim it carries, in the voice, at the length the beat allows.

- **Three-beat claims** carry a model or a method: three short parallel sentences, each a verb the reader can picture. They read best one per scene.
- **One sentence of detail** follows the beats: the whole offer in plain words, terms included.
- **Display lines** are written with their line breaks. Mark the breaks in the deck with ` / ` so the build sets them as written; never let a heading break where the browser chooses.
- **Labels** are small and literal: a section's job in two or three words, set in the voice's quietest register.

## Stage 4: Trust surfaces

These are the parts generated copy skips. Each gets its own entry in the deck.

- **Terms, early.** What it costs, how it is paid, what the client keeps. State them before the reader has to look.
- **Disclosure asides.** One or two short, labelled asides for the facts a cautious reader wants: what you own, what happens if it fails, the limit of the offer.
- **Fit statement.** Who this is for, then who it is not for, by situation rather than by insult. A real "no" makes the "yes" worth more, so name situations you would genuinely turn away.
- **FAQ as objections.** One question per item in the objection ledger, in its order, each answered in the first sentence and evidenced in the second. Question text in the reader's words, not yours.
- **The ask.** One action, named for what happens ("Send the application", not "Submit"), with the response time if there is one. If the ask qualifies people, say what you will ask for and why.

## Stage 5: Microcopy and the close

Write every remaining string: navigation, buttons, field labels and hints (visible labels, never placeholders alone), validation and error messages that say what to do next, empty, loading and success states, the cookie line if any, alt text for every meaningful image (what it shows and why it is there), the footer and the legal line. Use `design:ux-copy` for the error and empty states if it is installed. The close answers the opening: the spine again, or its resolution.

## Stage 6: Edit and lint

1. **Cut.** Take a fifth out of every draft. Keep the line that a stranger would repeat.
2. **Swap test** on every headline and claim.
3. **Read aloud** in order, at the pace of the scroll. Fix any line that is hard to say.
4. **Lint:** `python3 scripts/copy_lint.py COPY-DECK.md` (or the built HTML). It fails on em dashes, the "not X, it's Y" shape and cliché words, and warns on long sentences, Title Case headings, exclamation marks and low reading ease. Fix every failure; justify any warning you keep in the deck.
5. **Fit:** set the display lines at their real widths with the build or `scroll-verifier`, and rebreak any line that wraps badly. Check every line on a 390-px phone.

## Output: COPY-DECK.md

Use `templates/COPY-DECK.md`. Every line has a stable key (`hero.h1`, `beat3.claim`, `faq.2.q`) that the build uses, so a later edit changes one row and nothing else. Each row records the line, its job, the device, the evidence it rests on and its status (draft, chosen, set).

## The tests

- **Swap test:** a competitor's name in the line leaves it false or absurd.
- **Stranger test:** someone who saw the page once can repeat the spine.
- **Sceptic test:** each objection in the ledger is answered on the page, in order, before the ask.
- **Evidence test:** every factual line points to the proof inventory.
- **Ear test:** the deck reads aloud without a stumble.

## Anti-patterns

- Headlines that describe the category instead of the offer.
- Inflated verbs and empty intensifiers (see the cliché list).
- Terms hidden behind "contact us".
- A fit statement that excludes no one.
- FAQs that answer questions nobody asked, or answer in the second paragraph.
- Fake scarcity, invented proof, unnamed numbers.
- Copy written once for the page and never fitted to the beats or the phone.

## Files

- `references/devices.md`: the devices, when each works and fails, and the cliché list.
- `templates/COPY-DECK.md`: the deck.
- `scripts/copy_lint.py`: the lint (Python 3, standard library only).

## References

- Aristotle (c. 330 BCE) *Rhetoric*, Book III, on style: antithesis and the periodic sentence.
- Cialdini, R. B. (2021) *Influence, New and Expanded: The Psychology of Persuasion*. New York: Harper Business.
- Flesch, R. (1948) 'A new readability yardstick', *Journal of Applied Psychology*, 32(3), pp. 221 to 233.
- Government Digital Service (no date) [*Writing for GOV.UK*](https://www.gov.uk/guidance/content-design/writing-for-gov-uk). London: GDS.
- Ogilvy, D. (1983) *Ogilvy on Advertising*. London: Pan.
- Orwell, G. (1946) 'Politics and the English language', *Horizon*, 13(76), pp. 252 to 265.
