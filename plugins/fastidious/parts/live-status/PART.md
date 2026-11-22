# live-status

**Job.** One small line that tells the truth about now (open, closing soon, closed until Tuesday), so a page feels like a living business rather than a brochure.

| Field | Value |
|---|---|
| Beat intents | `rest` (detail) |
| Rung | 1 (no dependencies) |
| Role | `supporting` |
| Cost band | Very low: 1.8 KB module, updates once a minute |
| Licence | MIT (Fastidious, original), see `LICENSE` |

## Honest sources only

- **`schedule`**: the published hours from `FACTS.md`, computed in the business's own time zone, so a visitor abroad still sees the right state. Handles closing soon, closed today, tomorrow and later in the week.
- **`source`**: an async function returning live data (`{ text, state, at }`). If it fails, the line says live status is unavailable; if the data is older than `staleAfter`, it shows when it was last updated. It never makes a value up.

## Inputs

| Input | Default | Notes |
|---|---|---|
| `timeZone` | `Europe/London` | The business's zone, not the visitor's |
| `schedule` | none | `{ mon: [['07:00','19:00']], ... }` |
| `source` | none | For live data |
| `labels` | English defaults | Write them in the brand's voice |
| `soonMinutes` | `30` | |
| `every`, `staleAfter` | 60 s, 15 min | |
| CSS `--ls-on`, `--ls-warn`, `--ls-off`, `--ls-font` | | |

## Cost and checks

60 fps, 0 ms long tasks. Schedule logic unit-tested across weekdays, weekend, closing soon, after hours and British Summer Time.

## Fallbacks and access

`role="status"`, and only real changes update the text, so screen readers are not spammed. Reduced motion stops the breathing dot.

## Provenance

Original Fastidious part, built 22 November 2026 (intake run 003) from `WANTED.md`, prompted by the live roaster status on Profitize Build's demo pages.
