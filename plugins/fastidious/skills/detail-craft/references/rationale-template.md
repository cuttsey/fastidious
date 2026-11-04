# Detail rationale: six registers and three tags

Every finished design ships with this rationale. It covers **every detail**, not just the headline moments: the easing of a hover, the delay before a reveal, the words on a button, the colour of a focus ring. Each detail is explained in six registers, plus three short tags.

- **Registers:** 1 Personality · 2 Persuasion · 3 Routes deprioritised · 4 Proof · 5 Inclusion · 6 Craft and cost
- **Tags:** Meaning (how audiences read it) · Journey (where it sits in the arc) · Ethics (honest persuasion check)

Scale the depth to the detail: signature moments get every register in full; small details (a focus ring, a label) can answer registers 4–6 in a line each, but none are skipped.

## How to write it

For each detail, one block:

```markdown
### <Detail name> · <where it lives>

**The choice.** Exactly what it is, with values: curve, duration, delay, distance, colour, words.

**1 · Personality.** How this presents the product's personality. Name the trait it expresses (from the named personality) and, for motion, the feeling the viewer has: joy, confidence, calm, weight, curiosity, relief. Say why that feeling belongs to *this* subject and not any other.

**2 · Behavioural science and persuasion.** Why it works as a business asset: the attention, trust, memory or action it serves, and the principle behind it. State evidence strength honestly: *established*, *supported* or *practitioner heuristic*.

**3 · Routes deprioritised.** One to three alternatives that were considered, what each would have offered, why it ranked lower against the criteria, and the condition that would bring it back.

**4 · Proof.** How we'll know it works. A falsifiable hypothesis ("If X, then Y moves by Z"), the metric it moves (contact rate, receipts opened, scroll depth to the climax, time to first action, recall in a five-second test), the instrument (analytics event, A/B test, five-second test, session recording, interview) and what result would make us remove or change it.

**5 · Inclusion.** Who it works for and who it fails: vestibular sensitivity (its reduced-motion reading), screen-reader and keyboard users (what's announced, what's focusable), low-end and slow devices, low vision and contrast, cognitive load and attention, non-native readers. State the fallback that keeps the meaning.

**6 · Craft and cost.** How it's built (technique, library, properties animated), what it costs (KB, frame budget, requests, battery), its dependencies, and who can maintain it after launch (can a content edit break it?).

**Tags.**
- *Meaning:* how the insider, the curious and the sceptic each read it; the likely oppositional reading ("playful" read as "unserious") and what pre-empts it.
- *Journey:* where it sits in the arc (setup, rising, peak, rest, end), what comes before and after, and why the sequence makes it land.
- *Ethics:* ✔ persuades honestly, or ✘ with what was changed. Note anything that could read as manipulation.
- *Source:* the exemplar or reference it draws on, if any, and what was made original.
```

Group blocks by layer: **Concept** (the idea, the signature moments) → **Composition** (layout, type, colour) → **Motion** (every curve and timing) → **Interaction** (hover, focus, press, gestures) → **Sound** (if any) → **Words** (microcopy at every seam) → **Fallbacks** (reduced motion, no JS, phone). Finish with a short **summary**: the trade-offs that shaped the whole; a **measurement plan** that rolls up every register-4 hypothesis into the few metrics and tests that matter most (and feeds the studio's Learn phase); an **inclusion summary** of the fallbacks; and a **cost summary** (total weight, frame-budget risks, maintenance notes).

## Motion and feeling

Easing is emotion over time. Use this to name what a curve makes people feel, then check that the feeling belongs to the subject.

| Curve family | Example | What the viewer feels | Belongs to subjects that are… | Wrong for… |
| --- | --- | --- | --- | --- |
| **Overshoot / back-out** | `cubic-bezier(.34,1.56,.64,1)`, GSAP `back.out(1.7)` | Joy, playfulness, eagerness: the thing is pleased to arrive | playful, youthful, consumer, celebratory | grave, clinical, financial loss |
| **Bounce / elastic** | GSAP `bounce.out`, `elastic.out(1,.4)`, low-damping springs | Delight, comedy, physicality (a thing with weight landing) | characterful, toy-like, humorous brands; success moments | serious errors, regulated warnings |
| **Expo-out** | `cubic-bezier(.16,1,.3,1)` | Confidence, arrival, "it knew where it was going" | premium, assured, editorial | anything meant to feel tentative |
| **Quart/quint-out** | `cubic-bezier(.23,1,.32,1)` | Crisp competence, responsiveness | product UI, tools, precise brands | lavish storytelling (feels curt) |
| **Ease-in-out (sine)** | `cubic-bezier(.37,0,.63,1)` | Calm, breath, continuity | wellness, ambient, long transitions | quick feedback (feels sluggish) |
| **Linear** | `linear` | Mechanical, time-like, inevitable | progress, countdowns, scrubbed scroll, marquees | anything that should feel alive |
| **Slow, heavy, small travel** | 600–1200ms, ≤ 8% scale | Gravity, seriousness, weight | luxury, monuments, high-stakes trust | playful brands (feels pompous) |
| **Fast in, faster out** | 150ms in, 100ms out | Attentive, out of the way | controls, menus, dismissals | signature moments (feels cheap) |
| **Damped wobble** | rotate −30° → −45° → +20° → 0° in 600ms | A friendly nudge, "come on, click me" | arrows and CTAs on characterful brands | formal or regulated contexts |

**Asymmetry carries meaning.** A slow, expressive in-motion and a near-instant out-motion says "I'm glad you're here, and I won't keep you" (generous and respectful). Equal in and out reads as mechanical.

**Delay is character.** A 50–90ms stagger reads as a crowd arriving with personality; zero stagger as a block; over 150ms as hesitation.

## Persuasion architecture: principles to draw on

Use the principle that actually explains the detail; don't decorate with theory. Evidence levels are a guide; check context.

| Principle | What it says | Typical detail it explains | Evidence |
| --- | --- | --- | --- |
| Aesthetic-usability effect | People perceive attractive designs as easier to use and forgive more | overall polish, consistent motion grammar | supported |
| Processing fluency | Information that's easy to process feels truer and more likeable | clear hierarchy, plain words, tabular figures | established |
| First impressions (thin slicing) | Judgements of credibility form within about 50ms to a few seconds | the first screen, the hero | established |
| Peak-end rule | Experiences are remembered by their peak and their end | one signature moment, a crafted footer | established |
| Von Restorff (isolation) effect | The distinct item is remembered | one accent colour, one display moment | established |
| Costly signalling | Effort that's visibly expensive signals quality and commitment | hand-crafted details, bespoke illustration | supported |
| Social proof | People follow what similar others do and endorse | proof strip in the hero, testimonials | established |
| Authority | Credentials and independent validation increase compliance | named partners, published features | established |
| Specificity and precision | Precise numbers are judged more credible than round ones | "−74% month on month", qualifiers | supported |
| Curiosity gap | A small, open question pulls people forward | hover reveals, "Receipt +", teasers | supported |
| Goal-gradient effect | Effort accelerates as the goal comes into view | progress meters, chapter counters | supported |
| Zeigarnik effect | Unfinished tasks are remembered | multi-step reveals, "01/03" | practitioner heuristic (mixed replication) |
| Labour illusion | Showing work being done raises perceived value | preloaders that show real work, building scenes | supported |
| Self-reference and agency | Interaction people control feels owned and memorable | drag to spin, choose a variant, live calculators | supported |
| Reciprocity | A gift first raises willingness to return the favour | free chapter, free tool, useful content | established |
| Friction as safeguard | A deliberate pause improves decisions at high stakes | confirmations, "are you sure" in money flows | supported |
| Cognitive load | Fewer simultaneous demands improves comprehension | restraint calls, one moment at a time | established |
| Affect heuristic | Feelings toward something colour judgements of its risk and benefit | joyful motion on a brand, calm motion on risk | established |

**Ethics line.** Persuasion architecture serves the visitor's real interest. Never manufacture urgency, hide costs, fake scarcity or social proof, or make the exit harder than the entrance. If a detail only works by misleading, it's removed, and the removal is logged in register 3.

## Proof: instruments and metrics (register 4)

| Question | Instrument | Typical metric |
| --- | --- | --- |
| Do people get it in seconds? | Five-second test, first-click test | correct recall of who / what / why |
| Do they engage with the detail? | Analytics event | open rate (e.g. receipts opened), hover-to-click rate |
| Does it move the outcome? | A/B or before/after with a holdout | contact, sign-up or purchase rate |
| Does it slow anything? | Real-user monitoring | LCP, INP, CLS, frame drops on the scene |
| Is it remembered? | Next-day recall interview | unaided mention of the moment or the personality |
| Does it exclude anyone? | Assistive-tech and device testing | task success with VoiceOver, keyboard, reduced motion, mid-range Android |

Small samples are fine for qualitative proof (five to eight people); say so rather than claiming significance.

## Inclusion checklist (register 5)

- Reduced motion: the static reading still carries the meaning.
- Keyboard: reachable, visible focus, same reveal on focus as on hover.
- Screen reader: meaningful name, no noise from decorative layers, state changes announced only when useful.
- Contrast: text over texture or imagery at least 4.5:1 (3:1 for large type and UI).
- Devices: holds 60fps (or degrades gracefully) on a mid-range phone; works without hover.
- Cognition: one new thing at a time; no time limits; nothing flashes more than three times a second.
- Language: plain words; idioms and jokes still make sense in translation or have a plain fallback.

## Craft and cost (register 6)

Record: technique and library; properties animated (transform, opacity, clip-path, mask-position only, unless justified); weight (KB of JS, CSS, media); requests; frame-budget risk; dependencies and licences; who maintains it; what a content edit can break.

## Criteria for "Earth's best" (register 3)

When ranking routes, score against:

1. **Personality fit:** does it express the named personality more clearly than the alternatives?
2. **Clarity:** does the visitor understand faster?
3. **Business effect:** does it move the outcome that matters (contact, purchase, shortlist)?
4. **Inclusion:** does it work with reduced motion, keyboard, screen readers and on a mid-range phone?
5. **Performance:** does it fit the weight and frame budgets?
6. **Durability:** will it still be right in two years, and can the team maintain it?
7. **Cost:** is the expense proportionate to the gain?

A route is deprioritised, not deleted: name what it would have given, and the condition under which it would come back.
