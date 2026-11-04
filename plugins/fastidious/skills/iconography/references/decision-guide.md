# Decision guide

## 1. Slot map: what each kind of place usually needs
| Slot | Default | Icon earns its place when | Never |
|---|---|---|---|
| Primary call to action | Word, plus the brand's arrow | — | an icon-only primary button |
| Navigation (desktop) | Words | — | icon rails for content sites |
| Navigation (mobile bar) | Icon plus label, at most 5 | it's an app used daily | unlabeled icons |
| Close, menu, search, back | Convention icon | always, with an accessible name | invented metaphors |
| External link, download, file type | Small convention icon after the word | it changes what the click does | — |
| Status (success, warning, error) | Shape plus colour plus word | dashboards and forms | colour alone |
| Levels and ratings | Encoded marks (dots, pins, bars) | comparing many items | stars for non-reviews |
| Categories and content types | Words or tags; pictograms if there are many | readers scan 10+ items by type | cliché metaphors |
| Feature lists (marketing) | Words, numbers or real pictures | — | tinted icon tiles |
| Empty states, errors, 404 | Voice plus one motif | — | stock illustration scenes |
| Section dividers, bullets | Motif | it comes from the subject | generic dots and lines |

## 2. Open libraries (check the current licence before shipping)
| Library | Style | Grid / stroke | Count | Licence | Good for |
|---|---|---|---|---|---|
| Lucide | outline, round caps | 24, 2px (adjustable) | ~1,500 | ISC | neutral UI; easy to restroke |
| Phosphor | 6 weights (thin to fill, duotone) | 24 (256 master) | ~1,200 × 6 | MIT | matching a type weight closely |
| Tabler | outline, round | 24, 2px | ~5,000 | MIT | breadth |
| Heroicons | outline 1.5 or solid | 24 / 20 / 16 | ~300 | MIT | Tailwind-style products |
| Material Symbols | variable (fill, weight, grade, optical size) | 24, axes | ~3,000 | Apache 2.0 | large apps, Android |
Rules: one library per product. Restroke it to the brand's stroke. Remove cliché glyphs from your local copy so nobody reaches for them.

## 3. Style specification (fill this in from the brand, not by taste)
| Property | Derive from | Typical values |
|---|---|---|
| Grid | UI density | 24 px (2 px margin, 20 px live area); 16 px dense |
| Stroke | Text face stem at body size (measure the "l" or "i" stem width ÷ font size × 24) | 1.5–2.25 px at 24 |
| Caps and joins | Shape tokens: pills and soft corners → round; cut corners → square or miter | round / round |
| Corner radius inside icons | Card radius scaled to the 24 grid | 1–3 px |
| Fill rule | States needed | outline at rest, fill when active |
| Optical sizes | Where icons sit | 16 (simplified), 20, 24, 32 |
| Colour | Colour roles | currentColor; accent only for state |
| Motion | Motion tokens | draw-on or nudge, 150–300 ms, brand easing |

## 4. Custom set brief (when drawing your own)
For each icon: name, meaning in the subject's words, source sign (from the sign inventory), the reduction (what detail is dropped at 16 px), and a test sentence ("A newcomer sees this beside 'Hip' and reads: a throw over the hip").
Draw on the grid. Keep every horizontal and vertical on whole or half pixels for the stroke. Same stroke everywhere. Check them all side by side at 16 px before finishing any one.

## 5. Accessibility
- Icon plus text: the icon is `aria-hidden="true"`.
- Icon-only control: `aria-label` names the action, plus a visible tooltip on hover and focus where possible, and a 44×44 px target.
- Essential graphics: 3:1 contrast against their ground (WCAG 1.4.11). Status is never shown by colour alone.
- Motion: confirmations only. Remove under `prefers-reduced-motion`.
