# Intake log

Every candidate considered, whether admitted or not, so nothing is reconsidered by accident. Gates: 1 licence, 2 craft, 3 clean room, 4 performance and access, 5 best in class.

## Run 001: 22 November 2026, Codrops, 30 candidates

**Source.** The 30 most recently updated scroll, typography and transition demos in the [codrops GitHub organisation](https://github.com/orgs/codrops/repositories), shallow-cloned and run headless in Chrome (desktop 1440 × 900, mobile 390 × 844, reduced motion), with captures at six scroll positions.

**Gate 1 findings that apply to every candidate.**
- Code: all 30 repositories carry the MIT licence in the repository itself. Pass.
- Imagery: none of it can ship. Demo images are Midjourney output, Unsplash, Pexels or named third-party artists, credited in each README. Stripped from every admitted part.
- Fonts: most demos load Codrops' own Adobe Fonts kit, which is licensed to Codrops, not to us. Stripped.
- Libraries: GSAP (no-charge standard licence, a dependency, never bundled), Lenis (MIT), three.js (MIT), Splitting (MIT), imagesLoaded (MIT).

**Limits of this run.** Craft (gate 2) was judged from captured frames and the code, not from a hands-on motion review; performance figures are headless software rendering, a floor check rather than a device measurement. Candidates that need clicks, hover, a cursor or WebGPU to judge were held, not rejected.

| # | Candidate | Gate reached | Verdict | Reason |
|---|---|---|---|---|
| 1 | OneElementScroll | 5 | **Admitted** as `travelling-object` | One object carried through the story; strongest signature candidate in the run. Rebuilt with fallbacks. |
| 2a | OnScrollTextHighlight (effects 6, 7) | 5 | **Admitted** as `text-emphasis/marker-sweep` | Puts weight on facts in running copy; pairs with the premium bar. Rebuilt transform-only. |
| 2b | OnScrollTextHighlight (effect 1) | 5 | **Admitted** as `text-emphasis/char-rise` | Same concept, different brief (display lines, expressive register). Kept as a variant. |
| 2c | OnScrollTextHighlight (effects 2 to 5, 8 to 13) | 2 | Rejected | Remaining effects are colour, glow or filter flourishes; several animate `filter` or `color`, and none does a job the two variants do not. |
| 3 | ImageExpansionTypography (effect 1) | 5 | **Admitted** as `inline-image-expand` | Image and sentence arrive as one thought. Rebuilt so the layout never reflows while scrolling. |
| 4 | ScrollBlurTypography | 5 | Retired | Same concept as `text-emphasis`. Compared side by side: blur repaints every frame (1,130 ms long tasks, 46.8 fps headless, against 0 ms and 60 fps) and hides copy until reached. The admitted variants are better. |
| 5 | StickySections | 4 | Held for run 002 | Promising supporting part (15 exit variations). Needs a variation-by-variation review to pick one or two. |
| 6 | ScrollTextMotion | 2 | Held for run 002 | Strong typographic motion, 60 fps. The demo credits a named studio's site as inspiration; check that the result does not read as that studio's signature before admitting. |
| 7 | ElasticGridScroll | 2 | Held for run 002 | Column lag on a grid, 57 fps. Needs a clean-room test with non-portrait content. |
| 8 | TextClipScroll | 3 | Held for run 002 | Imagery inside letterforms; impact depends heavily on the image. Clean-room test with original artwork pending. 1,125 ms long tasks to investigate. |
| 9 | RepeatingImageTransition | 2 | Held for run 002 | Page transition; needs click capture. Only candidate with a reduced-motion branch already. |
| 10 | KineticTypePageTransition | 2 | Held for run 002 | Page transition; needs click capture. |
| 11 | GridToSlider | 2 | Held for run 002 | Click-driven layout switch; needs interaction capture. |
| 12 | EaseReverseClipMenu | 2 | Held for run 002 | Menu; needs interaction capture. |
| 13 | MotionTrailAnimations | 2 | Held for run 002 | Cursor-driven; needs pointer capture. |
| 14 | DoubleImageHoverEffects | 2 | Held for run 002 | Stuck on its loader headless; hover effects need pointer capture. |
| 15 | PixelTransition | 2 | Held for run 002 | Pixel image transitions within type; compare with `inline-image-expand` at gate 5 when reviewed. |
| 16 | ConnectedGrid | 3 | Held for run 002 | Grid connection on scroll; reads strongly of its imagery. Clean-room test pending. |
| 17 | CinemaSeatPreview | 2 | Held for run 002 | WebGPU and TSL; cannot run in headless software rendering. Needs a GPU review. |
| 18 | SlideshowAnimations | 2 | Held for run 002 | WebGPU variants; needs a GPU review. |
| 19 | OnScrollColumnsRows | 2 | Held for run 002 | WebGPU variants; needs a GPU review. |
| 20 | interlude | 1 | Held for run 002 | Astro starter for WebGL page transitions; needs a build. |
| 21 | 3DCarousel | 4 | Rejected | 27.7 fps and 2,965 ms long tasks headless; the effect is the fashion imagery. |
| 22 | 3DStackMotion | 4 | Rejected | 27.1 fps and 2,675 ms long tasks; the fanned card stack is a well-worn trend. |
| 23 | OnScrollSVGFilterText | 4 | Rejected | SVG filters on scroll: 21.1 fps, 1,627 ms long tasks. |
| 24 | OnScrollLayoutFormations | 4 | Rejected | 2,082 ms long tasks on a 38,000 px page; too heavy for a supporting part. |
| 25 | OnScrollShapeMorph | 3 | Rejected | Reads as its neon imagery; 40.9 fps. |
| 26 | Staggered3DGridAnimations | 3 | Rejected | Depends on its illustration set; 1,081 ms long tasks. |
| 27 | RotatingOnScrollAnimations | 4 | Rejected | Horizontal overflow on mobile; reads as the portfolio it was inspired by. |
| 28 | LoopScrolling | 3 | Rejected | A recreation of a named studio's signature loop; would read as that site in client work. |
| 29 | ImagePixelLoading | 3 | Rejected | Recreation of a named designer's site effect; 933 ms long tasks. |
| 30 | TypeShuffleAnimation | 2 | Rejected | Recreation of a named site's text shuffle; scramble text has become a common AI-site look. |

OnScrollTextHighlight holds 13 effects, so it has three rows (2a to 2c); the run covered 30 repositories.

**Result.** From 30 repositories: 3 admitted (as three parts, one with two variants), 1 retired at gate 5, 16 held for run 002, 10 rejected.

## Run 002: 22 November 2026, the 16 candidates held in run 001

**Method added.** Click, hover and cursor demos were driven headlessly and captured as frame sequences during the motion. WebGPU demos were run in a secure context with Chrome's software WebGPU adapter, which works for checking that a scene renders but not for judging its speed. Craft was still judged from frames and code, not a hands-on review.

| # | Candidate | Gate reached | Verdict | Reason |
|---|---|---|---|---|
| 1 | StickySections | 5 | **Admitted** as `sticky-stack` | Demos 1 and 7 cover the two distinct exits (drift, recede); the other 13 demos are close variations and were not kept. Filter dimming replaced with an overlay. |
| 2 | ElasticGridScroll | 5 | **Admitted** as `lagging-columns` | Works on any grid once restyled with product cards. Rebuilt without ScrollSmoother and without restructuring the DOM, fixing the source's column-by-column reading order. |
| 3 | RepeatingImageTransition | 5 | **Admitted** as `index-to-detail/echo-trail` | Clear job, and the best-built candidate in both runs: keyboard, inert and reduced-motion handling already present. WebGL surfaces dropped to keep it at rung 2. |
| 4 | EaseReverseClipMenu | 5 | **Admitted** as `interruptible-menu` | The value is the interrupted close (0.3 s against 1.2 s for a full close), a craft detail most menus get wrong. Demo trappings removed. |
| 5 | GridToSlider | 5 | Decided: variant `flip` of `index-to-detail` | Same concept as echo-trail, meaningfully different expression (calm, no echoes); a real brief exists for each. Normalisation queued for run 003. |
| 6 | KineticTypePageTransition | 3 | Queued for run 003 | A wall of rotating display type covers the screen between views. Survives a brand swap because it is all type. Strong signature candidate for type-led brands; needs normalising from its Parcel build. |
| 7 | OnScrollColumnsRows | 2 | Held for run 003 | Same family as `lagging-columns` but more spectacle (18 variations, some WebGPU). Compare variation by variation at gate 5. |
| 8 | SlideshowAnimations | 2 | Held for run 003 | WebGPU scene renders; slide changes need drag or button capture, not done this run. |
| 9 | TextClipScroll | 3 | Held for run 003 | Clean-room test with original artwork still to do; 1,125 ms long tasks to investigate. |
| 10 | ScrollTextMotion | 2 | Held for run 003 | Reference check against the studio site it credits was inconclusive from a text fetch; needs a look at the live site. |
| 11 | PixelTransition | 2 | Rejected | Pixel-block wipes are a recognisable trend look, and the effect depends on its photography. |
| 12 | MotionTrailAnimations | 4 | Rejected | Cursor image trails are a well-worn trend, and the effect has no touch or keyboard equivalent. |
| 13 | DoubleImageHoverEffects | 4 | Rejected | Hover-only with no focus or touch equivalent; 600 ms long tasks; depends on its imagery. |
| 14 | ConnectedGrid | 2 | Rejected | Photos drifting into a connected layout, with no job for the visitor beyond decoration. |
| 15 | CinemaSeatPreview | 3 | Rejected as a part | A complete product feature (pick a cinema seat, preview the view), not a reusable part. Logged in `WANTED.md` as a spatial preview idea. |
| 16 | interlude | 3 | Rejected as a part | An Astro site starter for page transitions, not a part; Fastidious is not tied to one framework. Logged in `WANTED.md`. |

**Result.** From 16 held candidates: 4 admitted (one as the first variant of a new concept), 1 decided as a second variant pending normalisation, 5 still held for run 003, 6 rejected. The library now holds 7 parts in 8 modules (two parts are concepts with variants).

## Run 003: 22 November 2026, the remaining held candidates, the wanted list, and a composition test

**Bar raised.** The question for every candidate was no longer "is it good and safe?" but "would it make a page memorable?". Parts that only tidy a page were not enough on their own.

| # | Candidate | Gate reached | Verdict | Reason |
|---|---|---|---|---|
| 1 | SlideshowAnimations | 5 | **Admitted** as `hero-slideshow` | The strongest craft in all three runs. Four of 32 transitions kept (push, recede, card, camera): the most distinct, all transform-only. The source captured the whole page's wheel and arrow keys; the part does neither. Word choreography added. |
| 2 | KineticTypePageTransition | 5 | **Admitted** as `type-curtain` | A real moment for type-led brands. Made 40% faster, and given a ground layer because the source let the swap show through the gaps. |
| 3 | GridToSlider | 3 | Not ported; `flip` built as an original | Its job is a grid-to-slider mode switch with a hue-shift hover gimmick, not index-to-detail. The calm variant was built from the concept description with GSAP Flip instead. |
| 4 | OnScrollColumnsRows | 5 | Rejected | 18 variations of image-wall motion; every one depends on dozens of matched photographs, and `lagging-columns` already does the transferable job. Spectacle without a job for the visitor. |
| 5 | TextClipScroll | 3 | Rejected | Imagery inside letterforms reads as its marbled artwork, and it carried 1,125 ms of long tasks. Below the raised bar. |
| 6 | ScrollTextMotion | 2 | Still held | The demo credits a named studio's site; whether it copies that studio's signature needs a person to look at the live site. One look settles it. |

**Wanted list, built as originals from written descriptions:** `grain-light`, `live-status` and `process-curve`. Each passed the same gates as a sourced part.

**Composition test.** A whole page was built from eight parts under one sign system (invented ropemaker, sample figures labelled on the page): `travelling-object` as the only signature, `grain-light`, `char-rise`, `marker-sweep`, `process-curve`, `flip`, `interruptible-menu`, `live-status`. It caught two defects that single-part tests could not:

1. `grain-light` set `overflow: hidden` on its host and clipped the travelling coil. Fixed: its layers now clip themselves.
2. `char-rise` used the generic class names `word` and `char`, which collided with the page's own `.word` wordmark style and shrank the hero headline. Fixed: generated classes are namespaced (`cr-word`, `cr-char`).

Result: 60 fps on mobile and 56.7 fps on desktop in software rendering, no errors, no overflow; menu, detail view, focus and Escape tested inside the page.

**Result.** 2 admitted from sources, 4 originals built (one as a concept variant), 2 rejected, 1 still held. The library now holds 12 parts in 14 modules (two parts are concepts with variants), and every module was re-verified after the composition fixes.

## Run 004: 22 November 2026, reconsidering everything turned away for resemblance

**Principle changed.** A site is unique because of its combination of parts, set in its own sign system around its own idea and facts, not because each part is unseen. From this run on, no part is rejected or retired because the same effect appears on other sites, because a demo credits a site as its inspiration, or because a technique is fashionable. Parts are judged only on job, craft, licence, cost and access. Earlier verdicts that leaned on resemblance are revised below; the earlier rows are kept as history.

| # | Candidate | Earlier verdict | Gate reached | New verdict | Reason |
|---|---|---|---|---|---|
| 1 | ScrollTextMotion | Held (run 003: credits a studio's site) | 5 | **Admitted** as `drifting-words` and `text-emphasis/scramble` | Two jobs in one demo: a drifting typographic field, and decoding text. Drift rebuilt as transforms, without ScrollSmoother. |
| 2 | TypeShuffleAnimation | Rejected (run 001: recreation, trend) | 5 | Retired on engineering | Same job as `scramble`, which is better built (shared ticker, accessible copy) than per-character timers writing `innerHTML`. Its typewriter cascade is noted as a future `scramble` mode. |
| 3 | PixelTransition | Rejected (run 002: trend) | 5 | **Admitted** as `view-change/pixel-cover` | A second view-change with the same API as `type-curtain`; cells now overlap so no seam shows the swap. |
| 4 | ImagePixelLoading | Rejected (run 001: recreation; 933 ms long tasks) | 5 | **Admitted** as `pixel-resolve` | Rebuilt on real `<img>` elements with one shared observer: 0 ms long tasks. |
| 5 | MotionTrailAnimations | Rejected (run 002: trend; no touch equivalent) | 5 | **Admitted** as `image-trail` | The touch concern was wrong: the engine uses pointer events. Scoped to its own area, paused off screen. |
| 6 | LoopScrolling | Rejected (run 001: recreation) | 5 | **Admitted** as `endless-loop` | A real page architecture for indexes. Clones made inert, reduced motion gets a finite page, and the scroll wrap was tested. |
| 7 | 3DStackMotion | Rejected (run 001: 27 fps, long tasks, trend) | 4 | Held for a real-GPU review | Its WebGL cost was measured with software rendering, which is unfair to any 3D part. Needs a measurement on a real device. |
| 8 | RotatingOnScrollAnimations | Rejected (run 001: mobile overflow; reads as its inspiration) | 4 | Held for a real-GPU review | Same measurement problem for its WebGL variations; the mobile overflow is fixable in normalisation. |

**Composition test 2.** A second whole page (an invented swim club) was built from seven parts with a different signature (`drifting-words`), to show that the same library makes a different site when the combination changes. It caught two defects:

1. On small screens, `drifting-words` let a word drift past the left edge. Fixed: drift is now clamped inside the field.
2. A `pixel-cover` in the same orange as the section it left was invisible. Not a code defect: the part's PART.md now says the cover colour must contrast with both views.

Result: 60 fps on desktop and mobile in software rendering, no errors, no overflow; view change, focus return and menu tested.

**Result.** 6 admitted as 7 modules (`view-change` is a new concept holding `type-curtain` and `pixel-cover`), 1 retired on engineering, 2 held for a real-GPU review. The library now holds 16 parts in 20 modules.

## Run 005: 22 November 2026, text effects from the Overdue example

**Source.** The Overdue example page on Muzli, reviewed for its text effects. It uses no animation library: one small inline script and CSS keyframes on Archivo's weight and width axes. Its code was not used. Three techniques were written up in words and added to `WANTED.md`; one was built.

| # | Candidate | Gate reached | Verdict | Reason |
|---|---|---|---|---|
| 1 | Variable-axis type (intro decay, scroll-bound weight and width, on-enter ramp) | 5 | **Built as an original**: `text-emphasis/axis-ramp` | No part in the library uses font axes. Rebuilt with a locked box, a font gate, reduced-motion steps and an accessible name, which fixes the gaps found in the review (no font gate, `aria-label` on a plain span). |
| 2 | Story counter tied to scroll | n/a | Wanted | Logged in `WANTED.md`. |
| 3 | Re-ranking list | n/a | Wanted | Logged in `WANTED.md`. |

**Rule added.** `README.md` now allows variable font axes as the one exception to "transform and opacity only", under conditions: display words, a locked box, a frame-rate check.

**Result.** 1 original built. The library now holds 17 parts in 21 modules.


## Font repo: 22 November 2026

Added the `fonts/` registry, cataloguing all 287 entries of the Awwwards free fonts collection. No font files are kept: 17 open entries (20 families) and 3 open successors are loaded by reference from jsDelivr, 5 Fontshare fonts through the Fontshare API, 255 await a licence check and 7 are not fonts. Every example and both composition tests were moved off generic faces onto repo fonts through the `--fd-display`, `--fd-body` and `--fd-mono` tokens, and all 21 modules passed the headless check again (desktop, mobile, reduced motion: about 60 fps, no errors, no overflow).

## Run 006: 22 November 2026, the Codrops Creative Hub

**Source.** The full [Codrops Creative Hub](https://tympanus.net/codrops/hub/all/codrops/) list (555 demos) was surveyed; see `HUB-SURVEY.md` for the queue. Ten new candidates were cloned and licence-checked (all MIT). Four became parts; six are queued for run 007.

**Font registry changed.** Fastidious keeps no font files. `fonts/` is now a registry: it says which fonts may be used and links each one (jsDelivr for open fonts, the Fontshare API for Fontshare fonts). Every example and both composition tests load fonts by reference, and all 21 earlier modules were re-checked (about 60 fps, no errors, no overflow).

| # | Candidate | Gate reached | Verdict | Reason |
|---|---|---|---|---|
| 1 | PushGridItems | 5 | **Admitted** as `index-to-detail/push` | A third index-to-detail variant with its own register (bold). Rebuilt on the shared markup contract, with transforms instead of grid re-placement. |
| 2 | TextRepetitionEffect | 5 | **Admitted** as `text-repeat` | A new typographic job. Copies hidden from screen readers; host box untouched; drift clipped after the first check showed overflow. |
| 3 | ContextAwareLogoAnimationScroll | 5 | **Admitted** as `context-aware-fixed` | A new courtesy job for fixed elements. The first build counted blocks and got stuck hidden after a jump in scroll; rebuilt to read state from the triggers, then passed a 14-position check. Blur effect dropped. |
| 4 | astro-shop-view-transitions | 5 | **Built as an original**: `page-transition` | Fills the wanted page-transition shell, framework-neutral, with shared elements, history, focus and announcements; falls back to any `view-change` part. |
| 5 to 10 | TextCharacterAnimations, LineTextHoverAnimations, HoverPreviewMiniMap, SlicedTextEffect, IntroGridMotionTransition, Codrops-GSAP-Scroll | 1 | Queued | Licences read (MIT); gating in run 007. |

**Result.** 4 parts added (3 admitted, 1 original). The library now holds 21 parts in 25 modules.
