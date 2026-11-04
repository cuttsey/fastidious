---
name: option-ledger
description: Showcases options with permanent ID numbers and keeps a ledger of options, decisions and outputs, so any choice can be revisited or rolled into new work by reference. Use when presenting alternatives, recording a choice, or when an ID such as O-012, D-004, A-007 or R-003 is mentioned.
---

# Option ledger

Design work produces far more than it keeps. Options are shown, one is chosen, the rest vanish, and three sessions later nobody can say what "the second blue one" was, or bring back the hero from last Tuesday's version without rebuilding it from memory. This skill gives every option, decision, output and reference a permanent ID, shows options in a way that makes them easy to compare and cite, and keeps a ledger with snapshots so any of them can be called back, reopened or rolled into new work by number.

It does not make design decisions. It makes them findable.

## The ID scheme

| Prefix | What it names | Example |
| --- | --- | --- |
| `O-` | An option shown to the person | O-032 Aubergine partner |
| `D-` | A decision: the question, the options offered and what was chosen | D-007 Partner colour for the lead |
| `A-` | An output: a version of a deliverable that was shown or delivered | A-019 Livery tokens, version 2 |
| `R-` | A reference, shared with taste-library's `REFERENCES.md` | R-004 Godly, hero rhythm |

Rules:

1. Numbers are per project, sequential within each prefix, and zero-padded to three digits.
2. An ID is never reused and never renumbered. Retired, declined and superseded items keep their ID and change status.
3. Options belong to the decision they serve: D-007 offered O-031 to O-036. A decision can be open (options shown, nothing chosen) or decided.
4. When studio-conductor is installed, `D-` numbers are the same numbers as its `DESIGN-RATIONALE.md` entries. One numbering, two files: the rationale log holds the reasoning, the ledger holds the items and snapshots.
5. The ledger is the source of truth. Never describe a past option or output from conversation memory; read it from the ledger and its snapshot.

## Files

- `OPTIONS-LEDGER.md` in the project root: the index of every ID.
- `.ledger/<ID>/`: a snapshot for every `O-` and `A-` item. A snapshot is whatever is needed to show or rebuild it exactly: the files themselves, a screenshot, the tokens, or a git commit hash plus the paths. Text options can live entirely in the ledger row.

```markdown
# Options ledger: <project>

Next free: O-037 · D-008 · A-021 · R-012

| ID | Type | Title | Status | Part of | Built from | Snapshot |
| --- | --- | --- | --- | --- | --- | --- |
| D-007 | decision | Partner colour for the lead | decided: O-032 | | | DESIGN-RATIONALE.md#d-007 |
| O-031 | option | Racing green (current) | declined | D-007 | | .ledger/O-031/ |
| O-032 | option | Aubergine | chosen | D-007 | R-004 | .ledger/O-032/ |
| A-019 | output | Livery tokens v2 | current | | A-012, O-032 | .ledger/A-019/ |
```

Statuses: `open`, `chosen`, `declined`, `current`, `superseded`, `stale`, `retired`. Keep the "Next free" line up to date so IDs are never guessed.

## Showcasing options

Whenever alternatives are put in front of the person, from any skill:

1. **Snapshot first.** Write each option to `.ledger/O-xxx/` and add its row before showing it.
2. **Badge every option.** The ID comes first on every card or row, in the same place, in a plain monospace or label style the person can read and type.
3. **Make them genuinely different.** Two to six options that differ in kind, not degree. When something already exists, include it as the null option ("keep as is") with its own ID.
4. **Compare like with like.** Show every option at the same scale, with the same content, in the same context it will be used in. A swatch on its own misleads; a swatch on the real layout does not.
5. **Say what each costs.** For each option: what it is in a few words, what it is best at, what it gives up, and how hard it is to reverse.
6. **Choose the format by the material.**
   - Visual options (colour, layout, type, motion, imagery): a showcase page, one card per option in a grid, each with its ID badge, a scale model, notes and contrast or other measured checks where they apply. Publish it where the person can return to it.
   - Strategic or written options (positioning lines, structures, naming): a table with an ID column, then the trade-offs.
   - Mixed: the table first, then the showcase for the visual parts.
7. **End with one line on how to choose:** "Reply with an ID, or combine them, for example O-032 with O-035's labels."

## Recording a decision

When the person chooses:

- Mark the chosen option `chosen` and the rest `declined`. Nothing is deleted.
- Write or update the `D-` row, and, with studio-conductor installed, its rationale entry: question, options, criteria, chosen and by whom, given up, reversible, revisit if.
- Never record a choice the person did not make. If the work ran unattended and Claude had to pick, record it as `chosen by Claude, provisional` and say so at the top of the next reply.

## Recording outputs

Every version of a deliverable that is shown to the person or delivered gets an `A-` ID and a snapshot. Fill in the lineage:

- **Built from:** the `A-`, `O-` and `R-` items it draws on.
- **Decided by:** the `D-` items that shaped it.

Edits inside a single turn before anything is shown do not need new IDs. The previous version becomes `superseded`, never overwritten.

## Working by reference

| The person says | Do this |
| --- | --- |
| "Show me O-021" or "What was D-004?" | Read the row and snapshot and show it again in the showcase format. If the snapshot is missing, say so plainly; do not rebuild it from memory and present it as the original. |
| "Go back to D-004" | Reopen it. Show its options again, then walk the lineage forward: list every later `D-` and `A-` that depends on it and mark them `stale`. Confirm with the person before redoing anything. With studio-conductor installed, follow its backward-step procedure. |
| "Roll A-012's hero into the new version" or "use O-033" | Load the named snapshot, take only the named part, and build the new output as a new `A-` with Built from filled in. If it is unclear which part was meant, ask one short question first. |
| "Compare A-012 and A-019" | Show them side by side under the showcase rules. |
| "Retire O-018" | Set its status to `retired`. The ID stays taken. |

IDs may be combined freely in one instruction ("A-019 with O-035's type and R-004's rhythm"); resolve each one from the ledger before building.

## Handoffs

- **studio-conductor:** shares `D-` numbers. Its gates can require that every converge step produced a ledger entry.
- **taste-library and reference-curator:** `R-` IDs are shared with `REFERENCES.md`. When `REFERENCE-BOARD.md` cites a reference, it uses the same `R-` ID.
- **Assurance skills** (mobile-auditor, scroll-verifier, accessibility-performance-auditor): record which `A-` they checked, so findings point at an exact version.

## Anti-patterns

- Options shown without IDs, or with IDs added afterwards.
- Renumbering a list because one option was dropped.
- Reusing a retired ID.
- Describing a past option from memory instead of its snapshot.
- Rolling in a whole output when the person named one part of it.
- A decision recorded that the person never made.
