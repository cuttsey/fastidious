# Fastidious parts library

A small, curated library of interaction and experience parts that Fastidious is allowed to ship. Managed by the `parts-librarian` skill; chosen per beat by `motion-choreographer`.

- `INDEX.md` lists every admitted part.
- `INTAKE-LOG.md` records every candidate considered and the verdict, so nothing is reconsidered by accident.
- `WANTED.md` lists techniques seen in references that the library lacks.
- `_retired/` holds parts that lost a best-in-class comparison.
- `_example/` holds original artwork used by clean-room examples.

Every part folder holds `src/` (the module and its CSS), `PART.md` (job, intents, rung, role, inputs, measured cost, fallbacks, provenance), `LICENSE` (the source's notice, kept intact), `example.html` (the clean-room restyle) and `preview/` (poster and clip of the restyled version, never the original demo).

## Using a part

Parts are ES modules that import GSAP by bare specifier. In a bundled project, `npm i gsap` and import the part's `src/*.js`. In a plain HTML page, add an import map:

```html
<script type="importmap">
{ "imports": { "gsap": "https://cdn.jsdelivr.net/npm/gsap@3.15.1/index.js",
               "gsap/": "https://cdn.jsdelivr.net/npm/gsap@3.15.1/" } }
</script>
```

Every part takes its look from tokens (CSS custom properties and options), never from the demo it came from, and every part has a reduced-motion state.

## Where uniqueness comes from

A site is memorable because of its combination of parts, set in its own sign system around its own idea and facts, not because each part is unseen. Parts are never rejected for resembling effects on other sites; they are judged on job, craft, licence, cost and access. What a build must never copy is another site's whole combination.

## Type comes from the font registry

Every typeface is chosen from [`fonts/`](fonts/README.md), which catalogues the Awwwards free fonts collection and says how to load each usable font. Fastidious keeps no font files: pages link the stylesheets listed there. Never use a basic or generic face (Arial, Helvetica, Georgia, system-ui, Menlo and the like) anywhere, examples included; a generic keyword may appear only as the last fallback. Pages set `--fd-display`, `--fd-body` and `--fd-mono`; parts read those tokens and never bring a face of their own.

## Rules every part follows (learned from the composition test)

- **Namespace everything a part generates.** Class names, custom properties and data attributes carry the part's prefix (`cr-`, `gl-`, `hs-`), never generic words like `word` or `char`.
- **Never change the host's box.** A part may add children and classes, but must not set `overflow`, `position` or `z-index` on an element it does not own; clip inside your own layer.
- **Animate transform and opacity; variable font axes are the one exception.** Weight, width and other font axes reflow text, so they may be animated only on display words (about 14 characters or fewer), inside a box whose size is locked at the widest state it will reach, and only after a frame-rate check. `text-emphasis/axis-ramp` is the reference for doing this safely. Locking that box is the only case where a part sets a size on the host element, and it removes the size on teardown.
- **One signature per page.** Signature parts are marked in `INDEX.md`; everything else on the page is supporting.
- **Colours that cover must contrast with what they cover.** A view-change or overlay takes a colour distinct from both the view it leaves and the view it reveals.
- **Facts come from the build.** Parts that show numbers (`live-status`, `process-curve`) take them from `FACTS.md`; examples using sample figures say so on the page.

`../showcase/` and `../showcase-2/` hold the composition tests: two different sites built from the same library with different combinations and signatures, published for review.
