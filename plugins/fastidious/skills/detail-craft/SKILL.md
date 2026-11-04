---
name: detail-craft
description: The detail layer that separates a competent site from a premium one, learned from studied award-level sites. A catalogue of signature moments (scroll-built illustrations, pinned and horizontal scenes, preloaders, scrubbed reveals, depth layers, texture, masks, brand-shape systems, lazy video) plus the ambient details around them, and an immersive tier (entry rituals, sound systems, cinematic video, four routes to hero 3D (rendered sequences, light real-time, shader objects, full models), transitions between views), each tied to the site's idea, with recipes, budgets and fallbacks. Use after the sign system and brand tokens exist and before or during build, whenever a site risks reading as "basic", or when someone asks to make a site feel premium, crafted, award-level or worth £100k.
---

# Detail craft

A basic site and a £100k site often share the same layout. The difference is the detail layer: dozens of small, consistent decisions, plus one to three signature moments where the page does something only this subject could justify. The effects are not the value. **The value is that each effect acts out the site's idea.** The same scroll-built illustration is a gimmick on one site and the whole argument on another.

## The governing principle: the personality is the product

Every effect, gesture, line of copy and sound on a premium site is the personality made tangible. What people remember and pay for is not the technique but *who* the site feels like. So:

- **Name the personality before choosing any effect.** Three to five traits, each with what it permits and what it rules out (take them from `BRAND-SYSTEM.md`'s voice and `SIGN-SYSTEM.md`'s myth; if they're missing, stop and get them).
- **Every detail must sound like that personality,** including the ones nobody briefs: hover gestures, loaders, empty states, errors, the 404, the footer sign-off, alt text, the cookie notice, the email confirmation.
- **The swap test applies to behaviour, not just copy.** If a hover, transition or microcopy line could move unchanged to a competitor's site, it isn't personality yet.
- **Personality is not jokes.** A precise, evidence-led person has a personality too: it shows as rigour, exact figures and calm motion. Match the register, don't default to playful.
- **Technique serves personality, never the reverse.** Pick the cheapest technique that expresses the personality fully; spectacle without personality is a template with a bigger budget.

This skill holds what was learned from studying premium sites (see `references/exemplars.md`) and turns it into a method: choose signature moments from the idea, surround them with a consistent ambient layer, and prove every effect against budgets and fallbacks.

## Where it sits

- **Reads:** `FRAME.md`, `POSITIONING.md`, `SIGN-SYSTEM.md` (above all its myth and motion meanings), `BRAND-SYSTEM.md` (motion vocabulary, colour, shape), `BEAT-MAP.md` or `INTERACTION-BASELINE.md`.
- **Writes:** `DETAIL-PLAN.md`: the signature moments, the ambient layer, budgets and fallbacks; and, when the build is done, `DESIGN-RATIONALE-DETAILS.md`: the six-register rationale for every detail (Stage F).
- **Works with:** `interaction-minimum-designer` (conventional builds: this adds the layer above its floor), `motion-choreographer` and `gsap-scrolltrigger` (implementation of pinned and scrubbed moments), `render-engineer` (only for true 3D or scrubbed video), `emil-design-eng` (micro-interaction polish), `accessibility-performance-auditor` (final gate).
- Upstream files outrank this one. If `SIGN-SYSTEM.md` says stillness carries the meaning, a signature moment must still honour that (a slow, heavy move, not a flourish).

## The eight lessons

1. **One idea, performed.** Every signature moment is the site's idea made physical. A lab that builds products shows a structure being built, stage by stage, as you scroll. A film series opens with a loading screen, title card and credits, then plays as a horizontal reel. Test: describe the moment without the subject's name. If it fits any site, it's decoration.
2. **A world, not a theme.** Premium sites commit to a material world (papyrus and carved wood, a film reel, a social feed) and render every surface in it: backgrounds, dividers, icons, illustrations, loaders. Half-commitment reads as template.
3. **Texture breaks the screen's flatness.** Film grain, paper fibre, contour lines and wood grain sit on fixed or full-bleed layers at very low contrast. Flat colour reads as digital and cheap; a little texture reads as made.
4. **Edges are designed.** Sections don't just stack. They tear (masked paper edges), cut (polygon corners), fade (mask gradients) or change the whole field colour. Look at every transition between sections.
5. **One shape, everywhere.** A brand shape (a cut corner, a hexagon crop) repeats across buttons, image crops, cards and badges. Repetition makes it a signature instead of an accident.
6. **Depth without 3D.** Most "3D" on these sites is layered illustration, isometric drawing, lighting rays and parallax between foreground UI cards and background. True WebGL is the exception and must earn its cost.
7. **The interface speaks the story's units.** Premium sites give the UI itself a role in the world (a *diegetic* device: part of the story, not commentary on it). A scroll indicator becomes the distance to an asteroid, a progress bar becomes the brand's racing stripe, a loader counts in the subject's own measure. The reader feels the idea through a control they'd otherwise ignore.
8. **Pacing has rests.** Signature moments are separated by calm, readable sections. A site that is all spectacle is as forgettable as one that is all template.

## Stage C0: the version-one baseline (always, from the first build)

Three details ship in **version 1 of every site**, designed in `DETAIL-PLAN.md` before any build and never deferred to a polish pass. Each comes from the subject's world, and each gets its six-register entry in Stage F.

1. **A custom cursor.** A tool from the subject's world, not a generic dot-and-ring (a banknote checker's loupe for finance, a pen nib for an author, a viewfinder for a photographer).
   - A precise dot that tracks exactly, plus a follower that eases behind it, critically damped (no overshoot unless the personality is playful).
   - **Labels that say what a click will do** ("Check", "Read case", "Email", "Download"), and states that remember (e.g. "Checked").
   - `mix-blend-mode: difference` on the dot and follower (white, placed directly on `<body>` with no stacking wrapper) so it reads on every ground; state classes live on `<html>`.
   - Only when `(hover: hover) and (pointer: fine)`; touch, pens and script failure keep the native cursor. No lag under reduced motion. Never hide the pointer entirely, even over a hero object (step the follower aside, keep the dot).
2. **A custom scrollbar.** The brand's tokens on the scrollbar, in both themes: a thumb in ink (or the accent) on a paper track, a hover or active state in the accent, rounded to the brand's radius.
   - `scrollbar-color` and `scrollbar-width` for Firefox; `::-webkit-scrollbar`, `-thumb`, `-track` for Blink and WebKit.
   - At least 10px wide on desktop (thin enough to be quiet, wide enough to grab); leave phones and overlay scrollbars to the system.
   - Under `forced-colors: active`, defer to system colours. Never hide the scrollbar.
3. **Hover effects as a brand gesture.** One gesture from the subject's world (a marker swipe, a ledger rule, a brush, a stamp) for every interactive surface: buttons, nav, inline links, cards.
   - On work or product tiles, the hover **reveals new content** (a second image, a detail) rather than only lifting or scaling.
   - Arrows and CTAs get their own small move in the same voice.
   - Expressive in, fast out; identical on `:focus-visible`; gated behind `(hover: hover)`; a reduced-motion fallback (cross-fade or instant state).

A version 1 without all three is not finished.

## Stage A: find the moments in the idea

From `SIGN-SYSTEM.md`'s myth and `FRAME.md`'s frame, list what the subject *does*, *makes* or *proves*. For each, ask which device performs it:

| If the idea is about… | the moment could be… |
| --- | --- |
| building, process, stages | a structure assembling layer by layer on scroll (scrubbed, reversible) |
| time, history, a career | a timeline that draws itself; a ruler or tick track that moves with scroll |
| proof, evidence, verification | a claim that resolves from blur to sharp; a figure whose receipt unfolds; a counter that never animates (proof shouldn't perform) |
| volume, community, reach | a dense wall of real clips or faces that keeps moving |
| film, story, character | a preloader, title card, credits, a horizontal reel, chapter cards |
| transformation, before and after | a pinned scene that scrubs from one state to the other |
| place, material | the material as the ground (texture, light, grain), and one view that opens to full screen |
| services, a process, a journey | one line that draws itself down the page as you scroll, winding through each stop (a service, a phase), with the stop's label, a small icon and a note pinned where the line passes |
| the people behind it | the founders as illustrated characters in the hero (carrying the name, with their pets), whose style shifts as you scroll (collage to line drawing) so the page moves from "show" to "explain" |
| money, business case, outcomes | the product object at the centre with the exact figures arranged around it ("in exact figures"), each with its qualifier; options as stacked cards with identical metric sets |

Choose **one to three** signature moments. More dilutes them. Write each as: *"On this page, [the subject's own thing] becomes [the device]."* Apply the competitor test: if a direct competitor could use the same sentence, keep looking.

### Diegetic devices and the stakes arc

Two patterns that need no 3D and almost no budget, and often beat it:

- **A diegetic meter.** Find the quantity the subject's story is measured in (distance, time left, altitude, depth, temperature, money saved, risk) and bind it to scroll progress. Show it small and persistent in the navigation from the first screen, so it quietly changes while people read, then enlarge it into the climax scene. Rules: the number must be true to the world (real or the fiction's own facts); it moves monotonically with scroll; it uses tabular figures so it doesn't jitter; it has a text equivalent and doesn't announce every change to screen readers.
- **The stakes arc.** Order the page like a story rather than a brochure: calm proof and action first (so people who only want to act can act), rising tension through the middle (premise, manifesto, testimony), a single pinned climax near the end where the meter reaches its limit, then a deliberate silence (an empty field of the world's colour) before the resolution (the series title, the next work, the sign-up). The climax earns the call to action that follows it.
- **A manifesto with a turn.** A short run of very large lines in which the last line changes colour or weight, marking the turn (for example: two lines in white, the third in the accent).
- **Proof in the hero.** Put the strongest independent evidence in a strip along the bottom of the first screen (rankings, ratings, "for fans of"), in small labelled pairs. Premium sites don't save proof for a testimonials section.

## Stage B: specify each signature moment

For each moment, record in `DETAIL-PLAN.md`:

- **Meaning:** which sign or claim it performs (cite `SIGN-SYSTEM.md`).
- **Trigger:** load, scroll scrub (tied to progress, reversible), scroll enter (plays once), hover or pointer, or time.
- **Mechanics:** pin length (in viewport heights), what moves, which properties (transform, opacity, clip-path, mask-position only), easing from `BRAND-SYSTEM.md`.
- **Assets:** layered SVG or PNG, video, shader. Who makes them (`asset-director` if needed).
- **Static reading:** the single frame shown under `prefers-reduced-motion`, without JavaScript and on low-power devices. It must still carry the meaning: usually the finished state, not the first frame.
- **Phone version:** its own composition, usually shorter pins or none, with the end state shown.
- **Budget:** see Stage D.

## Stage C: the ambient layer

These are small details applied consistently across the whole site. Pick those that fit the world; each needs a reason.

- **Texture overlay:** a fixed, pointer-events-none grain or fibre layer (2–6% opacity, `mix-blend-mode: multiply` on light, `screen` on dark). Cheapest: a tiled noise PNG or SVG `feTurbulence` rendered once; avoid per-frame canvas noise unless the world needs it.
- **Section transitions:** torn or cut edges via `mask-image` (an SVG edge) or `clip-path: polygon()`; full-field colour changes at section boundaries; never a hairline.
- **Text reveals:** blur-to-sharp (`filter: blur(8px)` → 0 with opacity) for statements, line-by-line rise for headlines, colour fill on scroll for a single manifesto line. One method per text role, used everywhere.
- **Brand shape:** one `clip-path` polygon (cut corner, chamfer, hex) applied to buttons, image crops, tags and the nav action.
- **Navigation:** a fixed bar that stays minimal; a scroll progress indicator for long or horizontal pages; a menu that opens as a designed full-screen moment, not a dropdown.
- **Preloader:** only when the page genuinely loads heavy assets. Honest progress (real asset loading), brand mark, under ~2s typical; it must never block content longer than the load does.
- **Framed images fill their frame, on the focal point (always):**
  - **Plan A:** cover the tile (`object-fit: cover`) and position the crop on the picture's focal point (faces, hands, the action, the mark), with `object-position` set per image (for example `style="--focus: 50% 12%"`). Run `scripts/focus.py <image> --ratio 4:3 --preview crop.jpg` for a suggestion, then **look at the crop and decide**. The script finds detail; a designer decides what matters.
  - **Plan B, only when Plan A isn't viable:** the crop would cut text a reader needs (posters, covers, notices, templates), the whole object must show (products, documents), it's a transparent cut-out, or less than about 45% of the picture would remain and the crop no longer tells the story. Then fit the image and let `assets/matte.js` paint the frame in the picture's own edge colour. Cut-outs stay on the designed ground.
  - **Never** put a fixed white or brand-colour box behind an opaque picture.
- **Media behaviour:** muted, looping, `playsinline` video that plays only when on screen (IntersectionObserver) with `preload="metadata"` and a poster; images that subtly scale or drift; captions written like credits.
- **Hover as a brand gesture:** choose one gesture from the brand's world (a brush stroke, a stamp, a scan line, a fold) and make it the hover language for every interactive surface: buttons, nav links, cards. On cards, the gesture reveals a *second image* (the work in use, a detail, the result), so hovering rewards curiosity with new content, not just movement. Make the in-motion expressive and the out-motion fast.
- **Card entrance as an aperture:** work cards enter by opening from a small rounded window (clip-path inset to full, corners squaring off) while the card inside settles from a slight overscale and alternating 3D tilt to flat. It reads as the work being unveiled, not slid in.
- **Micro-interactions:** hover states that move (arrow nudge, underline draw, image scale inside a fixed frame), press feedback, focus rings in the brand colour.
- **Voice as a detail layer:** personality lives in microcopy as much as in visuals. Give every seam a line in the brand's voice: section labels, the link to more work ("We could keep going, but there's a whole page for that"), FAQ questions people actually think ("Can you start yesterday?"), the footer sign-off ("Okay, that's enough website"). Keep it to one consistent register, and keep the factual parts plain.
- **Marginalia stickers:** small tilted pills (a few degrees, in the accent colour) used as asides: notes on a headline, adjectives beside a paragraph, captions on the route of a line. They pop in with a slight overshoot as the reader reaches them. One shape, one size, used everywhere: they become a brand device.
- **Reading fill:** for one statement paragraph, scrub each character's colour from pale to full ink as the reader scrolls, with a short band of accent colour at the leading edge, so the text reads like it's being highlighted in time with the reader. Use it once per page.
- **Iconography and motifs (use the `iconography` skill):** run its need test before drawing any icon. Words first, conventions with labels, encoded marks for comparison, and two or three motifs from the subject's sign inventory, all drawn in the brand's stroke and grid, audited and specimened.
- **Icons inside words:** replace a space or letter in a display heading with a tiny icon of the thing (a palette in "Art direction", a box in "Packaging design"). Use sparingly, only where the icon is instantly readable.
- **Shopfront details:** small real-world facts in the chrome (opening hours, local time, city, "currently booking for March") make a studio feel like a place you could walk into.
- **Type roles that carry voice:** give each face one job and keep it. A bold display face for brand moments, a neutral text face, and, where the subject is a contract, terms or evidence, a typewriter or mono face for the "document" voice (honest figures, terms, labels). The face signals the register before the words are read.
- **Stacked option cards:** comparable options (formats, plans, tiers) as full-height cards that pin and stack over each other on scroll, numbered as a set (01/03), each with the same metric set in the same order.
- **Typographic events:** one oversized display moment (name, title) that bleeds or scales; vertical or rotated type for names and labels; a second display face only if the world demands it.
- **Smooth scroll:** Lenis or similar only when scrubbed scenes need it; never on text-heavy reading pages; always disabled under reduced motion.

## Stage C2: the immersive tier (audio, cinema, 3D, views)

Some award-level sites go further: they behave less like pages and more like an experience you enter. Use this tier only when `narrative-architect`'s fit test passes, or when the site is a pitch, launch or campaign that people are invited to (not one they search for answers in). Every element below still has to perform the idea.

**Entry ritual.** A first screen that asks for one deliberate action drawn from the subject's world (a car's start button, a film's play, a key turned). It earns the user gesture browsers require before audio can play, sets expectations, and lets heavy assets load behind it. Rules: one action, labelled in words; a visible "skip" or "enter without sound" path; never a gate on a page people need for information; the gate itself must be quick to get past (under 2s of motion after the press).

**Sound as a system, not a soundtrack.** Design a small sound map and keep it consistent:
| Layer | Purpose | Level |
| --- | --- | --- |
| Entry sound | confirms the ritual (an engine catching, a projector starting) | full, once |
| Ambient bed | sets the world; loops seamlessly | about 10% volume |
| Transitions | marks a chapter or view change | short, quiet |
| UI ticks | confirms controls (arrows, tabs) | very short, quiet |
| Voice | real people speaking: testimony, a founder's note | full, user-started only |
Rules: no sound before a user gesture; a persistent, always-visible sound toggle that remembers the choice; voice is always user-started, with a transcript or the quote in text beside it; total audio under ~1.5 MB (compressed, not WAV); nothing essential is carried by sound alone.

**Cinematic video.** Treat video as footage, not decoration: full-bleed or framed in a brand-shaped panel, colour-graded to the palette, cut to a rhythm. Patterns: a hero loop under the title, a "watch the film" action that opens a proper player, a scroll-scrubbed clip (pre-encoded with frequent keyframes) for one signature moment, short UI-prototype clips that show a product working. Budget: hero loop ≤ 3 MB, each section clip ≤ 2 MB, a separate lighter mobile loop, `preload="metadata"` and posters everywhere, and play only when on screen.

**3D, honestly.** Decide which kind the idea needs:
1. *Filmed or rendered footage* of the object (cheapest, most cinematic; often what "3D" sites really use).
2. *Line or wireframe geometry on a canvas* that morphs with the story (one line → five orbits → a sphere), drawn in 2D or with light WebGL.
3. *A real-time model* (glTF with Draco or Meshopt compression, KTX2 textures, ≤ 5 MB total) only when the reader must turn, configure or explore the object. Hand this to `render-engineer`.
A real-time model must have a poster image fallback and a reduced-motion still, and it must not block the first screen.

**Hero 3D assets: choose the production route.** The high-resolution 3D product heroes on award sites are made in one of three ways. Pick by what the visitor does with the object:

| Route | What it is | Best when | Cost and limits |
| --- | --- | --- | --- |
| **A. Pre-rendered image sequence** | A 3D scene rendered offline (Blender, Cinema 4D, Octane) to 120–200 frames, played on a canvas by scroll position | The object should *perform* a transformation on scroll (tip back, spill, open, explode, assemble) with film-quality light, materials, liquids and hair | ~1280×720 WebP at 15–30 KB a frame (dark or plain grounds compress well): about 3–5 MB per sequence. No interaction beyond scrubbing. |
| **B. Light real-time 3D** | three.js with simple geometry (boxes, planes, extruded shapes) wrapped in crisp, high-resolution *label art*, lit simply | The visitor should *handle* the object: drag to spin, turn it over to read the back, pick variants, play with it | ~100 KB JS for the scene plus textures (each face ~560×880 or larger); total 2–4 MB. Quality comes from the artwork and lighting, not polygons. |
| **D. Procedural shader object** | One WebGL2 fragment shader that draws the object as signed distance functions (blob, lens, prism, gem), lit and refracting the page's own headline (drawn to a 2D canvas and passed in as a texture) | The subject is a *material, phenomenon or abstract quality* (light, glass, liquid, data, trust), and the object should respond to the pointer and morph between states on scroll | No asset files: one inline script of ~25 KB. Needs real shader skill; tune quality per device (pixel ratio 1.5 on touch, 2 on desktop). |
| **C. Full model (glTF)** | A modelled, textured asset (Draco or Meshopt geometry, KTX2 textures, HDR environment) | The object's real form matters and it must be configured or explored freely (a car, a device, furniture) | 3–10 MB; needs `render-engineer`; heavier on phones. |

Rules for every route:
- **The figure is the idea.** The hero object is a character from the subject's world doing something that states the promise (a figure on a giant Enter key whose bowl spills as you scroll: ideas escaping into reality; a claw machine holding the product: pick the one you want).
- **Design every face.** A turnable object needs a real back, sides and details (ingredients, barcode, small jokes). An empty back breaks the spell the moment someone spins it.
- **One guide object, many chapters.** A single hero object can stay with the reader through the page (pinned near the centre while sections pass around it), changing state per chapter: turning to show a new face, taking on each section's ground colour, passing behind giant type, multiplying into a stack when the story turns to scale. It gives a long page continuity and turns sections into scenes.
- **Mix routes per moment.** One site can use a light real-time model for the guide (a ~400 KB glTF) and a pre-rendered sequence for the one moment real-time can't do well (many objects, complex light). Choose the route per moment, not per site.
- **Refract the page, not a picture.** The most integrated 3D heroes bend the site's own typography through the object (route D), so 3D and layout read as one surface instead of a canvas pasted on top.
- **Let the object teach.** When the subject is technical, each scroll chapter can change one real property of the object (the material, the value, the state) with a live readout of the numbers in a corner, like an instrument. The motion is the explanation.
- **Layer type and object.** Set giant display type behind the object and supporting copy beside it, so the object reads as standing in front of the words. As the object moves, step the headline back (dim, blur or scale) to hand attention over.
- **Show the first frame instantly.** Render frame one as a normal image (or the poster) so the hero is complete before anything else loads; then load the sequence progressively (every eighth frame, then fill the gaps).
- **Respect the device:** cap the canvas pixel ratio at 2, draw with "cover" fitting, pause rendering when off screen, and use a shorter sequence or a single still on phones.
- **Static reading:** under reduced motion, show the most meaningful single frame (often the end state), not the first.
- **Make the interaction legible:** label it in plain words ("Scroll to flip the bag", "Drag to spin"), give it keyboard controls (arrows to move, Enter to act) and buttons with real names, and add a little idle motion (a gentle sway) so it reads as alive before anyone touches it.

**Moving between views.** Award sites make changes of view feel continuous:
- a camera move into an element (zoom through the start button into the hero);
- a stage that opens over the page, with previous and next to move between items without closing it;
- shared-element transitions (the thumbnail becomes the stage) using the View Transitions API (`document.startViewTransition`, `view-transition-name`) with a plain swap fallback;
- a floating dock navigation of chapters that appears after the opening, with the current chapter marked.
Every view is reachable by URL or keyboard, focus moves into the new view and back out, and Escape closes it.

**Explaining in layers.** Pair what the user sees with what happens underneath, each in its own colour from the brand's palette (for example, red for the customer's view, blue for the system's). It suits products and services with an invisible engine.

## Stage D: budgets and fallbacks

A £100k site that stutters on a mid-range phone is worth less than a still one.

- **Animate only** transform, opacity, clip-path and mask-position. No layout properties, no animated `filter` on large areas except short blur reveals on text.
- **Frame budget:** scrubbed scenes hold 60fps on a 2021 mid-range Android; test it, don't assume.
- **Weight:** hero media ≤ 300 KB above the fold; lazy-load everything below; video ≤ 2 MB per loop, with a poster; total JS for effects ≤ 120 KB gzipped unless 3D is justified.
- **3D gate:** use true WebGL or three.js only when layered illustration, CSS 3D transforms, footage or pre-rendered frames can't carry the idea (`render-engineer` decides).
- **Immersive tier total:** first view interactive within 3s on 4G; total page weight under ~25 MB even for a campaign site (studied award sites have shipped ~78 MB, which is a cost, not a target); audio ≤ 1.5 MB; models ≤ 5 MB.
- **Reduced motion:** every moment has its static reading; smooth scroll and parallax are off; pinned scenes become stacked, finished states.
- **No JavaScript:** content is visible; nothing waits on a script to appear.
- **Keyboard and screen reader:** pinned and horizontal scenes keep reading order; decorative layers are `aria-hidden`; the preloader never traps focus.
- **Mobile:** each moment has a phone composition; horizontal scroll becomes vertical unless it's the core idea.

## Stage E: the detail audit

Before sign-off, walk the site and score each row 0 (absent), 1 (present but generic), 2 (present and of this world):

| Area | What to check |
| --- | --- |
| Personality | Could you name the personality from the site alone, and does every row below express it? (Score this first; a 0 here fails the audit.) |
| Idea | Do the signature moments perform the idea, and pass the competitor test? |
| World | Do all surfaces belong to one material world? |
| Taste (taste-lessons.md) | One colour temperature with a tinted dark? One face shouting, one accent word at most? Three devices or fewer, used everywhere? Every colour pairing passes contrast? |
| Texture | Is there a deliberate surface quality, not flat default colour? |
| Edges | Are section transitions designed? |
| Shape | Does one brand shape recur across components? |
| Type | Is there one unforgettable typographic event? |
| Motion grammar | Do all moves share one easing and duration vocabulary? |
| Media | Is video lazy, muted, looping and captioned; are images treated consistently? |
| Interaction | Does every control move on hover, press and focus, using one gesture from the brand's world? Do work cards reveal something new on hover? |
| Cursor (v1) | Is there a custom cursor from the subject's world, with action labels, visible on every ground, native on touch and on failure? |
| Scrollbar (v1) | Is the scrollbar styled in the brand's tokens in both themes, in both engines, at a usable width, with forced-colours respected? |
| Pacing | Are there rests between signature moments, and does the page build to one climax? |
| Diegetic UI | Does at least one interface element (progress, loader, cursor, counter) speak in the subject's own units? |
| Voice | Does every seam (labels, transitions, FAQ, footer) carry a line in the brand's voice, with the facts kept plain? |
| Sound (if used) | Is there a gesture-started sound map, a persistent toggle and text for every voice? |
| Views (if used) | Do view changes feel continuous, and are they reachable by URL, keyboard and Escape? |
| Fallbacks | Do reduced motion, no-JS and phone each carry the meaning? |
| Performance | Do scenes hold 60fps and meet the weight budget? |

Score only the rows that apply. A site scoring below two-thirds of its possible total is not premium yet; fix the lowest rows first. A site with idea or fallbacks at 0 fails regardless of total.

## Stage F: the detail rationale (required)

Every finished design ships with a rationale for **every detail**, written with `references/rationale-template.md`, in six registers plus three tags:

1. **Personality:** what the choice is (with exact values) and how it presents the product's personality. For motion, name the feeling it creates in the viewer (the joy of an overshoot, the confidence of an expo-out, the gravity of a slow, small move) and why that feeling belongs to this subject.
2. **Behavioural science and persuasion architecture:** why it works as a business asset (attention, trust, memory, action), the principle behind it, and the strength of the evidence.
3. **Routes deprioritised:** the alternatives considered and why each ranked lower on the way to the best possible product, with the condition that would bring each back.
4. **Proof:** a falsifiable hypothesis, the metric it moves, the instrument that would test it, and the result that would make us change it.
5. **Inclusion:** who it works for and who it fails (reduced motion, keyboard and screen reader, low-end devices, contrast, cognitive load, language), and the fallback that keeps the meaning.
6. **Craft and cost:** how it's built, what it weighs and costs at runtime, its dependencies, and who can maintain it.

Tags: **Meaning** (how insider, curious and sceptic read it), **Journey** (where it sits in the arc), **Ethics** (honest-persuasion check), and **Source** (what it draws on).

Signature moments get every register in full; small details answer registers 4–6 in a line each, but none are skipped. Close with a summary, a measurement plan (rolling the register-4 hypotheses into the few tests that matter, feeding the studio's Learn phase), an inclusion summary and a cost summary.

Write it as `DESIGN-RATIONALE-DETAILS.md` in the project, grouped by layer (concept, composition, motion, interaction, sound, words, fallbacks), and publish it as a page when it's for others. Do this at the end of every design or build without being asked. A design without its rationale is not finished.

## Recipes

Short, tested patterns. Use the brand's tokens for every value.

**Scroll-built illustration (layers assembling).** Draw the subject as 4–8 stacked SVG or PNG layers. Pin the section for 2–3 viewport heights and scrub each layer's `opacity` and `translateY` in sequence; a progress line or label updates with each stage.
```js
gsap.timeline({ scrollTrigger: { trigger: '.build', start: 'top top', end: '+=250%', pin: true, scrub: 0.6 } })
  .from('.build .layer', { yPercent: 12, opacity: 0, stagger: 0.25, ease: 'none' })
  .to('.build .stage-label', { textContent: 'Launch', snap: 'textContent' }, '<');
```
Reduced motion: show the final layer stack and all stage labels as a list.

**Horizontal reel.** Pin a track and translate it by its overflow width as the reader scrolls. Add a progress bar.
```js
const track = document.querySelector('.reel__track');
gsap.to(track, { x: () => -(track.scrollWidth - innerWidth), ease: 'none',
  scrollTrigger: { trigger: '.reel', pin: true, scrub: 1, end: () => '+=' + track.scrollWidth, invalidateOnRefresh: true } });
```
Phone and reduced motion: a vertical stack.

**Blur-to-sharp statement.**
```css
.reveal-blur { filter: blur(10px); opacity: 0; transition: filter 900ms var(--ease-out), opacity 700ms var(--ease-out); }
.reveal-blur.is-in { filter: none; opacity: 1; }
@media (prefers-reduced-motion: reduce) { .reveal-blur { filter: none; opacity: 1; transition: none; } }
```

**Torn or cut section edge.**
```css
/* edge-torn.svg: a 1440×40 black shape whose top edge is the tear; the gradient covers the rest of the section */
.section--torn {
  --edge: url(edge-torn.svg) top / 100% 40px no-repeat, linear-gradient(#000 0 0) 0 39px / 100% calc(100% - 39px) no-repeat;
  -webkit-mask: var(--edge); mask: var(--edge); margin-top: -40px;
}
.cut { clip-path: polygon(0 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%); }
```

**Grain overlay.**
```html
<svg class="grain" aria-hidden="true"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
```
```css
.grain { position: fixed; inset: 0; width: 100%; height: 100%; pointer-events: none; opacity: .05; mix-blend-mode: multiply; z-index: 50; }
```

**Reading fill with a leading edge.**
```js
// GSAP + SplitText + ScrollTrigger
const split = new SplitText('.statement', { type: 'chars' });
gsap.set(split.chars, { color: 'var(--ink-pale)' });
gsap.timeline({ scrollTrigger: { trigger: '.statement', start: 'top 70%', end: 'bottom 40%', scrub: true } })
  .to(split.chars, { color: 'var(--accent)', stagger: 0.02, duration: 0.1, ease: 'none' })
  .to(split.chars, { color: 'var(--ink)', stagger: 0.02, duration: 0.1, ease: 'none' }, 0.06);   // ink trails the accent
```
Keep the paragraph as real text (SplitText leaves it readable to screen readers via `aria-label`); under reduced motion, set the full ink and skip the timeline.

**Brush-stroke hover reveal (two coats).** Each work card holds the main image plus a hover image. On hover, a wide SVG stroke in the project's tint paints across the card, then a second stroke on a different path paints the hover image in through an SVG mask.
```html
<a class="card" href="/work/x" style="--tint:#FDE1FD">
  <div class="card__media">
    <img class="card__img" src="main.jpg" alt="…">
    <svg class="card__paint" viewBox="0 0 709 1012" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <path class="coat" d="M25 154C151-28 236 40 351 133-86 535 63 618 466-70 646 40" fill="none" stroke="var(--tint)" stroke-linecap="round" stroke-linejoin="round"/>
      <defs><mask id="m1" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1109" height="1412">
        <path class="reveal" d="M25 730C137 1066 290 969 507 832-165 175 90 45 315-71 463 560 616 515" fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round"/></mask></defs>
      <image href="hover.jpg" width="709" height="1012" preserveAspectRatio="xMidYMid slice" mask="url(#m1)"/>
    </svg>
  </div>
</a>
```
```js
document.querySelectorAll('.card').forEach((card) => {
  const coat = card.querySelector('.coat'), reveal = card.querySelector('.reveal');
  gsap.set([coat, reveal], { drawSVG: '0%', strokeWidth: 0 });
  const tl = gsap.timeline({ paused: true, defaults: { ease: 'power1.inOut' } })
    .to(coat, { drawSVG: '100%', strokeWidth: 1200, duration: 1.0 })          // the brush loads up as it travels
    .to(reveal, { drawSVG: '100%', strokeWidth: 1200, duration: 1.0 }, 0.35); // the image chases the colour
  card.addEventListener('pointerenter', (e) => e.pointerType === 'mouse' && tl.timeScale(1).play());
  card.addEventListener('pointerleave', () => tl.timeScale(6).reverse());     // out is near-instant
});
```
Without DrawSVG, animate `stroke-dasharray: L; stroke-dashoffset: L → 0` (`L = path.getTotalLength()`). Pair it with a damped wobble on the card's arrow (rotate about −30° → −45° → +20° → 0° over 0.6s). Rules: the hover image must add information (the work in use, a detail), never a duplicate; keyboard focus triggers the same reveal (`focus-visible`); on touch, show the main image only and let the tap go straight to the case; under reduced motion, cross-fade the two images instead.

**Aperture card entrance.**
```js
gsap.utils.toArray('.card-wrap').forEach((wrap, i) => {
  const card = wrap.firstElementChild, side = i % 2 ? 1 : -1;
  gsap.set(wrap, { clipPath: 'inset(42.5%)', borderRadius: 36 });
  gsap.set(card, { scale: 1.45, rotationX: 25, rotationY: 16 * side, rotationZ: 4 * side, transformPerspective: 800 });
  gsap.timeline({ scrollTrigger: { trigger: wrap, start: 'top 90%', end: 'top 40%', scrub: 0.6 } })
    .to(wrap, { clipPath: 'inset(0%)', borderRadius: 0, ease: 'power2.out' }, 0)
    .to(card, { scale: 1, rotationX: 0, rotationY: 0, rotationZ: 0, ease: 'power2.out' }, 0);
});
```
Reduced motion: no clip or tilt; cards simply present.

**A line that draws through the stops.** One SVG path down the section, `stroke-dasharray`/`stroke-dashoffset` (or GSAP DrawSVG) scrubbed by scroll; each stop is positioned in HTML along the path, and its label, icon and sticker reveal as the line reaches it. Phone: a straight vertical line on the left with stops beside it.

**Diegetic scroll meter.**
```html
<p class="meter" aria-label="Distance to impact"><span class="meter__label">Distance to impact</span> <span class="meter__value" data-meter>4,800,000</span> km</p>
```
```js
const el = document.querySelector('[data-meter]'), from = 4_800_000, to = 0, fmt = new Intl.NumberFormat('en-GB');
const end = document.querySelector('#impact');                    // the climax section: the meter reaches `to` at its end
const update = () => { const max = end.offsetTop + end.offsetHeight - innerHeight;
  const p = Math.min(1, Math.max(0, scrollY / max)); el.textContent = fmt.format(Math.round(from + (to - from) * p)); };
addEventListener('scroll', update, { passive: true }); update();
```
Style with `font-variant-numeric: tabular-nums`. In the climax, pin a stage, scale the approaching object (an image is enough) with the same progress, and repeat the number at display size. Under reduced motion, keep the number (it's information) and drop the scaling.

**Scroll-scrubbed image sequence (route A).** Pin a tall section; map its scroll progress to a frame index; draw to a canvas.
```html
<section class="seq" style="height: 400vh"><div class="seq__stage" style="position: sticky; top: 0; height: 100svh">
  <img class="seq__poster" src="frames/f_001.webp" alt="…" width="1280" height="720">
  <canvas class="seq__canvas" aria-hidden="true"></canvas></div></section>
```
```js
const N = 192, frames = [], canvas = document.querySelector('.seq__canvas'), ctx = canvas.getContext('2d');
const src = (i) => `frames/f_${String(i + 1).padStart(3, '0')}.webp`;
const load = (i) => frames[i] || (frames[i] = Object.assign(new Image(), { src: src(i), decoding: 'async' }));
for (let step of [8, 4, 2, 1]) for (let i = 0; i < N; i += step) load(i);          // progressive: coarse first, then fill
const size = () => { const d = Math.min(devicePixelRatio, 2); canvas.width = innerWidth * d; canvas.height = innerHeight * d; };
const draw = (i) => { let f = frames[i]; for (let k = i; !(f && f.complete) && k > 0; k--) f = frames[k - 1];   // nearest loaded frame
  if (!f?.complete) return; const s = Math.max(canvas.width / f.naturalWidth, canvas.height / f.naturalHeight);
  const w = f.naturalWidth * s, h = f.naturalHeight * s; ctx.drawImage(f, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h); };
let want = 0, shown = -1;
const onScroll = () => { const r = document.querySelector('.seq').getBoundingClientRect();
  const p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight))); want = Math.round(p * (N - 1)); };
(function tick() { if (want !== shown) { draw(want); shown = want; } requestAnimationFrame(tick); })();
addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', () => { size(); shown = -1; }); size(); onScroll();
```
Hide the poster once frame 0 has drawn. Under `prefers-reduced-motion`, skip the canvas and swap the poster for the chosen end frame. Encode frames with `cwebp -q 72`; check the total before shipping.

**Turnable product (route B).** A three.js scene with a box or extruded bag shape; materials use the label art as `map` with `colorSpace = SRGBColorSpace` and `anisotropy = renderer.capabilities.getMaxAnisotropy()`. Pointer drag sets angular velocity, which decays each frame (inertia) and eases back to the nearest face; arrow keys rotate by 90°; `setPixelRatio(Math.min(devicePixelRatio, 2))`; stop the render loop when the canvas is off screen or the tab is hidden.

**Shader object refracting the headline (route D), in outline.**
1. Draw each chapter's display word to an offscreen 2D canvas at the device pixel ratio; upload as textures `uTexA` and `uTexB`, cross-faded by `uMix`.
2. In a full-screen fragment shader, raymarch a scene SDF: `mix()` or a smooth minimum between the current and next shape (`sdBlob`, `sdLens`, `sdGem`…) by scroll progress, plus a pointer-driven bulge on the blob.
3. At the hit point, compute the normal; `refract()` the view ray three times with slightly different indices (n − Δn, n, n + Δn) and sample the text texture once per channel for R, G and B. That is the rainbow fringe.
4. Add a Fresnel-weighted reflection of a simple studio gradient, a soft contact shadow and a cheap caustic on the floor plane.
5. Map scroll to `{object, n, Δn, tint}` per chapter and ease between them; mirror the values in a DOM readout (`aria-live="off"`) so the numbers are text, not pixels.
6. Fallbacks: the headline is real HTML underneath; without WebGL2 or under reduced motion, show the text with a static image of the object.

**Custom cursor (labelled, difference-blended).**
```html
<!-- appended to <body> by script; no wrapper, so the blend reads the page -->
<div class="cur__ring" aria-hidden="true"><svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="15"/></svg></div>
<div class="cur__dot" aria-hidden="true"></div><div class="cur__label" aria-hidden="true"></div>
```
```css
.has-cursor, .has-cursor * { cursor: none !important; }
.cur__dot, .cur__ring, .cur__label { position: fixed; left: 0; top: 0; z-index: 200; pointer-events: none; opacity: 0; }
.cursor-on .cur__dot, .cursor-on .cur__ring { opacity: 1; }
.cur__dot { width: 6px; height: 6px; margin: -3px 0 0 -3px; border-radius: 50%; background: #fff; mix-blend-mode: difference; }
.cur__ring { width: 36px; height: 36px; margin: -18px 0 0 -18px; color: #fff; mix-blend-mode: difference; }
.cur__ring circle { fill: none; stroke: currentColor; stroke-width: 1.4; }
.cursor-target .cur__ring svg { transform: scale(1.55); transition: transform 220ms var(--ease-out); }
.cursor-on.cursor-target .cur__label:not(:empty) { opacity: 1; }
```
```js
if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
  /* insert the three elements, add .has-cursor to <html>; on pointermove (pointerType 'mouse') set the dot to the pointer,
     ease the ring toward it (k ≈ 0.28; k = 1 under reduced motion), set the label from the nearest
     'a[href], button, summary, [data-cursor]' (data-cursor wins; then infer from href: mailto → Email, .pdf → Download, …),
     and toggle .cursor-target on <html>. Sleep the rAF loop when the ring has caught up. */
}
```

**Custom scrollbar.**
```css
:root { --sb-thumb: color-mix(in srgb, var(--ink) 45%, transparent); --sb-thumb-hover: var(--accent); --sb-track: var(--paper); }
html { scrollbar-color: var(--sb-thumb) var(--sb-track); scrollbar-width: auto; }
::-webkit-scrollbar { width: 12px; height: 12px; }
::-webkit-scrollbar-track { background: var(--sb-track); }
::-webkit-scrollbar-thumb { background: var(--sb-thumb); border-radius: 999px; border: 3px solid var(--sb-track); }
::-webkit-scrollbar-thumb:hover, ::-webkit-scrollbar-thumb:active { background: var(--sb-thumb-hover); }
@media (forced-colors: active) { html { scrollbar-color: auto; } }
```

**Marker-swipe hover (buttons, nav).** Inject `<svg class="swipe" viewBox="0 0 100 40" preserveAspectRatio="none"><path pathLength="1" d="M-4 26C14 12 30 30 50 20S86 12 104 22"/></svg>` as the first child of each button or nav link (`position: relative; isolation: isolate`, the SVG at `z-index: -1`). The path starts at `stroke-dasharray: 1; stroke-dashoffset: 1; stroke-width: 0`; on `:hover` and `:focus-visible` it transitions to `stroke-dashoffset: 0; stroke-width: 52` (≈500ms in, 300ms out).

**Lazy video.**
```js
const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? e.target.play() : e.target.pause()), { threshold: 0.25 });
document.querySelectorAll('video[data-lazy]').forEach(v => io.observe(v));
```
With `muted loop playsinline preload="metadata" poster="…"`; no autoplay under reduced motion.

**Scroll progress bar.** Use CSS `animation-timeline: scroll()` on a fixed bar's `scaleX`, with no JavaScript; static where unsupported.

## Anti-patterns

- Effects chosen from a showreel, not from the idea.
- Every section animated the same way, or every section a different trick.
- A preloader with fake progress, or one longer than the load.
- Counters that count up to prove a number.
- Parallax on text people need to read.
- Smooth scroll on a reading page.
- WebGL for something an SVG stack could do.
- A signature moment with no static reading.
- Texture so strong it lowers text contrast below AA.
- Sound that starts without a gesture, or has no toggle; voice with no text.
- Shipping tens of megabytes of video because the footage is beautiful.
- Calling footage "3D" in a plan, then budgeting for a real-time model nobody needs.
- Shipping version 1 with the system cursor, the default scrollbar or default hovers (Stage C0 is not optional).
- Hover effects that only scale or lift a card (the category default) when a brand gesture could reveal new content.
- Lorem ipsum, "Learn more" and "Get in touch" at the seams where a line in the brand's voice belongs.
- A progress bar, loader or counter in generic units when the subject has its own measure.
- A beautiful 3D hero that says nothing about the subject (a generic floating blob, a stock render).
- A turnable object with a blank back, or an image sequence with no poster frame.

## References

- `references/exemplars.md`: annotated observations of the studied sites (what each does, how, and what to borrow or reject).
- `references/taste-lessons.md`: generalised taste principles (palette as one temperature, type roles, three repeated devices, qualified proof, layout varies but the system doesn't), each with how it fails.
- `references/rationale-template.md`: the six-register rationale template and tags, the motion-and-feeling table, persuasion principles with evidence levels, the ethics line, proof instruments, the inclusion checklist, craft-and-cost fields, and the criteria for ranking routes.
