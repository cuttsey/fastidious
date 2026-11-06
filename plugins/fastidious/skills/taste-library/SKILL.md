---
name: taste-library
description: Gathers, selects and keeps the person's own design references in REFERENCES.md with permanent R numbers, and feeds them into reference-curator and art direction. Use when the person shares inspiration, asks to add, review or prune references, or before reference-curator runs on a new build.
---

# Taste library

A designer's set of references is the schema for their personal style, and the bar it sets should keep rising. reference-curator finds references for one build from a scored registry. This skill holds what the person has chosen for themselves, across projects, annotated well enough that a model can check its own work against it, and makes sure every build starts from it rather than from adjectives.

## Files

There are two libraries, and the person owns both.

- **The personal library**, kept across every project: `~/.claude/fastidious/REFERENCES.md`, with images, screenshots and scans in `~/.claude/fastidious/references/`, or wherever `FASTIDIOUS_LIBRARY` points. This is the designer's own standard: the sites they love and the images they learn from. `python3 scripts/library.py init` creates it from `templates/REFERENCES.md`, and `python3 scripts/library.py check` confirms every entry has its notes and every image is where its ID says. Run the scripts from this skill's folder.
- **The project library**: `REFERENCES.md` in the project root, with stored items in `.references/R-xxx.<ext>`. It holds the references chosen for this job.

Every reference has a permanent `R-` ID, shared with option-ledger. A retired ID is never reused. When a personal library exists, it owns the numbering: a reference keeps its ID when it is copied into a project, and anything new takes the next free ID from the personal library, so an `R-` number means the same thing in every project.

```markdown
# References

Kept by taste-library. IDs are permanent: a retired ID is never reused.

| ID | Source | URL | Teaches | Pattern | Fit | Borrow | Reject | From |
|----|--------|-----|---------|---------|-----|--------|--------|------|
| R-001 | Godly | https://godly.website | look | hero | aspirational | Hero copy held to one line at display size | Its dark-mode default, its layouts | L-032 (registry) |
| R-002 | Timing screen at Silverstone | | type | data_visualisation | direct | Tabular numerals, yellow on black | The screen's density | own |

Next free ID: R-003
```

- **Teaches:** one of look, pattern, motion, type, structure, thinking.
- **Pattern:** a term from reference-curator's `pattern_taxonomy` where one fits (hero, cards, cta, motion, typography, dark_mode and so on).
- **Fit:** `direct` (similar industry, register and audience) or `aspirational`.
- **From:** `own`, the registry ID (`L-xxx`) when it came from the source registry, or the catalogue ID (`DS-xxx`) when it came from the design systems catalogue.

IDs follow reference-curator's data files, where each entry carries the same `fastidious_id`: L-001 to L-004 are reserved for the third-party skill packages, L-005 to L-089 are the 85 registry sources, L-090 to L-101 are the exemplar sites, and DS-001 to DS-235 are the production design systems. A design system is a structure reference: borrow how it organises and names components, never its values without fetching the live page. When the person pastes a references table of their own, in this format or close to it, adopt it as it is, keep their IDs and wording, and fill only the columns they left empty, saying which ones you filled.

## Start from the person's own library

Before gathering anything new, read the personal library if it exists.

1. Run `python3 scripts/library.py check`. Fix or flag anything it reports before relying on the library.
2. Pick the active entries that fit this job's frame, register and audience, look at each image and live page, and propose them first, as `O-` options, before any registry source.
3. Copy the chosen entries into the project's `REFERENCES.md` with their IDs and notes unchanged, and copy their images into `.references/`.
4. If there is no personal library, offer once to start one (`library.py init`), then carry on with the project library alone.

## Gather

1. **Agree what it is for.** Wait for `FRAME.md` and `POSITIONING.md`, or confirm the job, the person served and the register in one exchange. A reference earns its place against a stated job.
2. **Go wide and distinct.** Collect 15 to 30 candidates from at least three registry categories (product UI and UX, web design, design communities, branding, typography, motion and interaction, specialist collections), plus at least one from outside design entirely: a poster, a uniform, an instrument panel, a timetable. Five near-copies teach one thing.
3. **Take what the person gives you exactly.** Links, screenshots, files or names of things ("that railway poster"). Look at each one where you can. Record what you saw, store non-web items under `.references/`, and never invent or guess a URL.
4. **Annotate on capture.** For each candidate, write one pattern term, one sentence on the exact technique worth taking, and one sentence on what is not to be taken. A candidate that cannot be annotated is not a reference yet.

## Select

Show the candidates with option-ledger's showcase rules, each as an `O-` option, then let the person choose. Apply these criteria:

- **Adjacency first.** Similar industry, similar register (playful or austere), similar audience sophistication. A colour match alone is not adjacency.
- **One aspirational at most per build,** narrowed to a single named technique, never a composition to copy.
- **Production relevance** decides when the reference will settle a build question; mood sources (communities, galleries scored low on production relevance) are for sensing a direction only.
- **Spread what they teach.** Three to five references per build, covering different kinds (look, type, motion, structure) rather than five versions of one.
- **Rival check.** Compare against the competitor list in `POSITIONING.md`. Drop a direct competitor, or narrow it to structure only.

Each chosen candidate gets an `R-` ID in `REFERENCES.md`; the selection is recorded as a `D-` decision in the ledger.

## Put them to work in the stack

Order of play:

1. frame-shifter writes `FRAME.md`; positioning-strategist writes `POSITIONING.md`.
2. **taste-library** updates `REFERENCES.md` and names the three to five `R-` items for this build.
3. reference-curator starts `REFERENCE-BOARD.md` from those `R-` items, carrying their borrow and reject notes word for word, then fills any gap from the registry and the design systems catalogue. Anything it adds gets the next free `R-` ID, appended to `REFERENCES.md` with the note "build only" unless the person wants to keep it.
4. brand-system-architect and the art direction lead receive `REFERENCE-BOARD.md`, never bare links.
5. scroll-verifier and the critique skills check the build against the borrowed techniques by `R-` ID.

When briefing reference-curator, say so directly: "Start from R-004, R-009 and R-011 in REFERENCES.md; keep their annotations; fill gaps only."

## Keep the bar rising

At the end of each project:

- Offer to send the project's best new references back to the personal library, with their notes and images. Only the person decides what enters it.
- Retire the weakest reference and add the best thing met during the project. Retiring changes status; the ID stays taken.
- Any reference still missing its borrow or reject note gets annotated or retired.
- Keep the active library small enough to be a standard, around 40 entries, not an archive.
- Record the review as a `D-` decision so the reasons survive.

## Never

- Pass a bare link downstream.
- Invent a URL, a source, or a quote from one.
- Treat a design systems catalogue entry as a source of values; fetch the live page first.
- Let analogy-scout's sealed source domains into `REFERENCES.md`. Only its public learnings travel.
- Copy a direct competitor's styling.
