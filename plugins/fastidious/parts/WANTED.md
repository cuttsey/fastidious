# Wanted parts

Techniques seen on the reference shelf that the library lacks. Describe the technique in words only; fill it from the parts shelf or build an original from this description, never from the reference's code.

| Wanted | What the visitor sees and does | Intent | Seen at | Status |
|---|---|---|---|---|
| Living status line | A small line that shows something real changing (open now, today's batch, water temperature), wired to a real source | rest (no motion), detail | Profitize Build demo landing pages | Filled: [`live-status`](live-status/PART.md), original, run 003 |
| Data-as-story curve | A single process curve (a roast, a tide, a build) that draws as the reader scrolls, with one live readout | manipulate | Profitize Build demo landing pages | Filled: [`process-curve`](process-curve/PART.md), original, run 003 |
| Grain and light texture | Film grain and soft light over a section, at negligible cost, as depth without 3D | depth | Profitize Build shader library (grain, glass) | Filled: [`grain-light`](grain-light/PART.md), original, run 003 |
| Page transition shell | A framework-neutral way to run transitions between pages (View Transitions API first, script fallback), that any part can hook into | manipulate | Codrops interlude (Astro starter) | Filled: [`page-transition`](page-transition/PART.md), original, run 006 |
| Spatial preview | Let the visitor see a choice from where they would be (a seat, a room, a view) before committing | manipulate | Codrops CinemaSeatPreview | Open: only for briefs where position is the decision |
| Type that changes shape with meaning | A display word gets heavier, lighter, wider or narrower as the story moves (a name thinning as days pass, a word filling as something rises) | reveal, manipulate | Overdue example page on Muzli | Filled: [`text-emphasis/axis-ramp`](text-emphasis/axis-ramp/PART.md), original, run 005 |
| Story counter | A big figure that counts with scroll progress through a pinned story (days since, hours left, metres climbed), in a monospace or tabular face so it never jitters, with a short label that changes with the beat | manipulate | Overdue example page on Muzli | Open |
| Re-ranking list | A short list whose rows slide into a new order as a value changes, with the row that matters picking up a state label as it crosses a threshold | manipulate, detail | Overdue example page on Muzli | Open |
