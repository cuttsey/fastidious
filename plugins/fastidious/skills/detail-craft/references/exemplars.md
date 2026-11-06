# Exemplars: studied sites

Observed 2026-10-27 at 1440 × 900 in a real browser, with page scripts and computed styles inspected. These are annotations of technique, not templates: take the principle, never their names, copy, illustrations or signature assets.

## ciuslabs.com (independent product lab)

**Idea performed:** the lab "builds, ships and runs" products, so the page *builds a structure*. An illustrated pyramid assembles stage by stage as you scroll (foundation → walls → stepped tiers → capstone with a rising sun), each stage labelled with a step of their process (Architect, Build, Launch, Run) and a hand-drawn line chart that draws across beside it. Building is the subject, and the scroll performs it.

**World:** carved dark wood (hero), then papyrus and parchment with fibre texture, hieroglyph-like icons, an Egyptian deity figure (Horus) as mascot, sun rays as light. Every surface belongs to that world.

**Details worth learning:**
- Hero: one light-weight statement, small two-column facts (Practice, Model, Capabilities, About) like a spec sheet, two actions, and a tick ruler along the bottom edge that reads as a timeline or measuring rule.
- Transition from wood to papyrus through a **torn paper edge** (mask image); there are ~33 masks on the page.
- **Blur-to-sharp text**: a paragraph first appears blurred and resolves as you arrive.
- **Light rays and glow**: radiating rays behind the capstone, rendered on canvas layers; the dark sections reuse the rays as a backdrop for the product list.
- **Grain everywhere**: a fixed full-screen canvas plus surface textures, blended with `screen` and `multiply`.
- Product list as a quiet ledger (name left, one-line description right in tiny caps, external-link mark), set inside the dramatic scene: drama around, plain information inside.
- Isometric line drawings for each discipline ("How the lab builds") with expandable details.
- Typography: one custom variable sans in very light weights (100–250) at large sizes: confident without bold.
- Motion grammar: expo-out easing (`cubic-bezier(.16,1,.3,1)` and `(.22,1,.36,1)`), 0.2s hovers, 0.36s UI, 1.2s reveals; Lenis smooth scroll; sticky stages for the pinned build.
- Stack: Next.js, a design-token system (`--ds-*`), 10 canvas layers, 188 inline SVGs. No three.js: the depth is illustrated, not modelled.

**Borrow:** the scroll-built structure as a metaphor for process; the torn-edge world change; blur-to-sharp statements; grain; a spec-sheet hero; expo easing with long reveals.
**Reject:** the specific Egyptian world and mascot; very light text weights where contrast suffers.

## later.com (influencer marketing platform, homepage)

**Idea performed:** "insight from creators at scale". The page shows *volume of real creator content* (a dense, moving wall of genuine UGC video clips in rows) and *data about people* (floating creator cards with GMV, impressions, ROI and sentiment charts, layered at different depths).

**Details worth learning:**
- **One brand shape**: a cut-corner polygon (`clip-path: polygon(...)`) on the primary button, the hero image (a hexagon-like crop), cards and badges. It is instantly recognisable.
- **Contour-line background**: subtle topographic wave lines on the off-white ground, giving texture and motion without imagery.
- **Field-colour chapters**: sections switch to full-bleed brand colour fields (purple; a purple → orange gradient) as chapter breaks; a large statement ("Go big. We've got you.") fills in as you scroll.
- **Pinned scrubbed scenes** (GSAP ScrollTrigger pin-spacers ~2700px): floating UI cards and stats drift at different speeds over a gradient field while a bold claim sits left ("Other brands are guessing. You don't have to.").
- **Video discipline**: 15 videos, all `muted loop playsinline preload="metadata"`, not autoplay; they're played by script when in view.
- Logo wall kept monochrome and evenly weighted, then immediately followed by real content (the UGC wall), so the proof is shown rather than claimed.
- Heavy, wide display face for headlines, plus a quiet text face; reduced motion handled in CSS.

**Borrow:** a single brand polygon used everywhere; proof by volume (real clips); depth from layered UI cards rather than 3D; disciplined lazy video; colour-field chapters.
**Reject:** heavy tracking-script load; consent UI that covers content for the whole visit.

## later.com/made-you-look (creator film series campaign page)

**Idea performed:** a film series, so the page *is* a film: a loader, a title sequence, opening credits, then a horizontal reel of characters.

**Details worth learning:**
- **Preloader**: brand bolt mark with an honest percentage ("Loading 0% … 100%") over a grainy, blurred gradient field ("aurora" mesh), and "Scroll down" as the only instruction.
- **Title card**: "Meet the creators redefining influence." centred over the aurora with a play button: the trailer is one click away.
- **Horizontal reel**: one long pinned scene (page height ~18,400px) translates the whole page sideways as you scroll vertically: title, credits, essay, character cards, then each creator's chapter.
- **Credits as copy**: "Produced by / Directed by / Photographed by / Filmed by" set like film credits: the voice of the medium.
- Huge, ultra-bold condensed display type ("MADE YOU LOOK") filling the column; **vertical rotated names** with gradient fill running up the screen as chapter markers.
- Character cards: photo in a saturated gradient frame, name large, handle and category tags small; consistent across all creators.
- Each creator chapter: big landscape still with play button over the aurora gradient, name in display type, one-line descriptor.
- Lazy YouTube embeds (iframe API) instead of self-hosted heavy video.

**Borrow:** stage the page as the medium it's about (film → loader, title, credits, reel); vertical type as chapter markers; consistent character cards; honest loader.
**Reject:** horizontal scroll for content people need to read closely; long pins on mobile.

## bmwf3.com (Format-3's pitch to BMW, "Next Move")

**Idea performed:** an agency's unsolicited pitch to a car brand, so the site *behaves like the car*. You start it with an engine button, it moves like a drive (speed blur, cinematic footage), and the proposal itself (an intelligence layer behind the showroom) is shown as one line that becomes five surfaces.

**Details worth learning:**
- **Entry ritual:** a full-screen radial red-white-blue glow (M colours) with "Next / Move" either side of a round **Start engine** button. Pressing it plays an engine start, unlocks audio, and the camera zooms *into* the button before cutting to the hero.
- **Sound system** (6 files): engine start, ambient bed looping at 10% volume, intro sting, section-switch sound on chapter change, UI tick on arrows, and the founder's quote as a **voice note player** (waveform, avatar, play). A persistent "Turn sound off" control.
- **Cinematic video** (≈11 clips): a drifting car in smoke inside a framed panel with a notch cut in its top edge; a headlight macro ("Feel the experience"); separate mobile loop; prototype clips for each product surface.
- **Type events:** wide extended display face; titles resolve through horizontal slices or a speed blur (a motion-blur that settles), matching the subject (velocity).
- **Scroll-typed line:** a monospace prompt types "What if the future of BMW's upgrading was…" with a cursor; then a pinned word cycler swaps Understanding → Personalization → … → Intelligence with blur cross-fades and a dot pager.
- **Progress bar as brand stripe:** the BMW M tricolour grows across the top as you scroll.
- **Evidence:** customer research quotes in a horizontal carousel (active card in M red, progress line under it); key words in quotes coloured by actor (customer red, dealership blue).
- **Morphing line geometry:** a full-screen canvas draws wireframe forms that change with the argument: a single vertical line ("One layer"), five orbits ("Five surfaces"), a sphere.
- **Views:** product surfaces shown as real UI with an "Explore surface" pill that follows the cursor; clicking opens a stage over the page with *What the customer sees* (red) beside *What's happening underneath* (blue), a prototype video, and previous/next arrows across the five surfaces. A floating dock nav (Statement, Opportunity, Solution, Questions, Schedule a call, sound) appears after the opening.
- Stack: a single Vite bundle (~284 KB JS), no three.js globals and **no 3D model files**. The "3D" is footage plus canvas line geometry; the View Transitions API is available in the browser.
- **Costs:** ≈78 MB transferred (≈36 MB video), and no `prefers-reduced-motion` handling found in its stylesheets.

**Borrow:** an entry ritual from the subject's own world that unlocks sound; a quiet, consistent sound map with a toggle; voice as proof; one line that morphs to match the argument; stages with previous and next; colour-coded "sees / underneath" explanation; the brand stripe as progress.
**Reject:** the page weight; no reduced-motion path; gating content that people may need quickly.

## goofymew.mintplayground.com (concept cat-food brand, "Good food for weird cats")

**Idea performed:** choosing a cat food becomes an *arcade claw machine*. The hero is a 3D claw holding the product bag over a tray of flavours.

**Details worth learning:**
- **Real-time 3D product (route B):** three.js with simple geometry (boxes, planes, shapes) wrapped in crisp 560×880 label art per face, `MeshStandardMaterial`, sRGB colour, anisotropic filtering, pixel ratio capped at 2, clipping planes. No model files; about 96 KB of app JS and ~3 MB in total.
- **Every face designed:** drag to spin with inertia; the back of the bag has the brand story, benefit icons, a feeding guide table, ingredients, a barcode and a cat in a speech bubble. Turning it over is like picking it up in a shop.
- **Idle life:** the bag sways gently on the claw before you touch it; motion lines radiate from it like a cartoon.
- **The picker is the game:** "Drop" releases the bag, which tumbles with physics into the pile; the camera pans to the tray; a control appears ("Move with the arrows, then grab a bag": ←, Grab, →); the claw descends on a telescoping arm and lifts the chosen flavour. Arrow keys work, and every button has a descriptive name ("Grab the bag under the claw").
- Giant pale display type ("DRY FOOD CAT") behind the object, shifting with the camera; one saturated brand blue field; rounded friendly type.
- Instructions in plain words in the corners ("Scroll to flip the bag", "Drag to spin"); reduced motion handled in the code.

**Borrow:** a turnable product with every face designed; a playful mechanic from the subject's world that *is* the navigation; idle sway; plain-language instructions; keyboard parity.
**Reject:** relying on the game alone to choose a product (keep a plain list too).

## mintplayground.com (Trang, UI/UX designer portfolio)

**Idea performed:** "helping founders transform their idea into reality". The hero is a surreal, high-resolution 3D render of the designer-as-character: a figure in white with a glass **fishbowl for a head** (betta fish inside), laptop on lap, sitting on a giant **Enter** keycap, in front of huge "PORTFOLIO" type.

**The scroll transition (route A):** a sticky canvas plays **192 pre-rendered WebP frames** (1280×720, ~22 KB each, ~4.2 MB in total) by scroll position:
1. The figure sits working; headline left ("Helping founders"), promise right ("Transform *their idea* into reality").
2. The figure tips back; the headline dims and steps back.
3. The bowl spills: water arcs out in ribbons, the fish escape and swim free, and the figure floats weightless.
4. The keycap's legend changes from **Enter** to **UIUX**; the figure drifts up out of frame.
5. Rendered tablets tilted in space show real project screens, with small white cut-out figures climbing on them; "Hello, I'm Trang".
The story is the promise made literal: pressing Enter releases the idea, and the idea becomes UI/UX work.

**Details worth learning:**
- Film-quality materials (glass, water, fabric, plastic keycap) that real-time 3D on the web can't match; the render does the heavy lifting, and the browser only swaps frames.
- Giant condensed display type set *behind* the figure; the figure overlaps it, so the scene has depth.
- After the hero: a client list in quiet text beside a huge "5EX" (five years' experience) with a cut-out figure; then "Welcome to my work" with sticker chips (My story, Experience, UI UX design) and a grain texture.
- Code is small (~10 KB): canvas `drawImage` with "cover" fitting, device pixel ratio handling, a sticky stage, IntersectionObserver and reduced-motion handling. Total page ~19 MB because of project imagery and three short videos.

**Borrow:** a hero character that is the designer's promise made literal; a scroll-scrubbed render that tells one short story in 4–5 beats; type layered behind the figure; the headline handing over to the figure as it moves; keeping the 3D language going into the project section.
**Reject:** typos in display type ("Tranform"); placeholder copy left in project cards ("This is some description"); total page weight from unoptimised project images.

## oavivo.github.io/dispersion (an explainer of optical dispersion)

**Idea performed:** the page *is* the phenomenon. A glass object sits over each chapter's huge headline and bends it, splitting the edges into rainbow fringes. Your pointer pulls at the glass; scrolling changes what it's made of.

**The sequence:** a soft blob over "Dispersion" → a water drop over "Water" (index 1.333) → a crown-glass sphere (1.517) → a dense-flint cube (1.785) with strong colour splitting → a cut diamond (2.417) with "fire". Each chapter has a short, exact paragraph of real physics (rainbows at 42° and 40°, Abbe numbers, why diamonds sparkle).

**Details worth learning:**
- **Zero assets:** one inline script (~26 KB, 612 lines), a single WebGL2 canvas and Google Fonts. Shapes are signed distance functions (`sdBlob`, `sdLens`, `sdPrism`, `sdGem`, `sdCrystal`, a smooth minimum to blend them).
- **It refracts the page's own type:** headlines are drawn to a canvas and passed in as textures (`uTexA`, `uTexB`, cross-faded by `uMix`), then refracted per colour channel with a refractive index and dispersion (`uN`, `uDn`), so the fringes are physically motivated rather than a filter.
- A small satellite droplet shows the text upside down, as a real drop would; a caustic shadow on the floor changes with each shape.
- **Live instrument readout** (bottom right): refractive index, Abbe number and spread, easing continuously between chapters, with a thin spectrum bar.
- Pale grey dotted-grid ground, black grotesque display type, small grey body copy: a lab notebook. The object is the only colour on the page.
- Pixel ratio 1.5 on touch devices and 2 on desktop; reduced motion handled.

**Borrow:** an object that demonstrates the subject's own principle; refracting real type through 3D; one changing property per chapter with a live readout; precise, factual copy; extraordinary quality from code alone.
**Reject:** nothing structural. Mind contrast on the small grey body text.

## hopenovel.com (Hope, a novel by G.D. Colwill)

**Idea performed:** the novel is set under an asteroid on a slow, unstoppable path to Earth, so **reading the page brings the asteroid closer.** The navigation carries "Distance to impact: 4,800,000 km", which falls as you scroll and reaches 0 km at the climax.

**The arc of the page:**
1. Hero: an extreme close-up of the heroine's face, "HOPE" in huge red-orange type, the series name above it, and a proof strip along the bottom (#1 Amazon free charts in two genres, Goodreads 4.40, "For fans of *The Road*, *Station Eleven*").
2. A red field with the tagline ("Humanity has its expiration date.") beside a "Read Hope free" email form, with Kindle and paperback links as the alternative.
3. The book: cover, synopsis, and a facts table (series, book, genre, rating, formats).
4. Trailer: a manifesto in condensed caps ("Denial consumed me. Acceptance redeemed me. **Transcendence will define me.**", the last line in red) beside a video still with an in-character caption ("I was born days after the asteroid was discovered.") and a tattoo reading 2055.
5. Readers: one large pull-quote ending "The asteroid is just the ticking clock." plus four short reviews with sources; a request for reviews.
6. **Climax:** a pinned stage (~6,300px) in space: the Moon on the left, the asteroid growing from a speck to fill the screen, and the distance repeated at display size: 2,021,545 → 1,436,607 → 705,435 KM → **0 km**, then black.
7. Silence, then "The Legacy of Grace" rising faintly out of the dark; the sign-up again; "All work 01—05" as an index table (number, title, series, form, status); the list's benefits numbered 1–3.

**Details worth learning:**
- Built with React (UMD from unpkg) and still images: no canvas, WebGL, video files or audio. About 4 MB. The premium feel comes from the concept, not the technology.
- Two typefaces with clear roles: Archivo (condensed caps for the display moments, grotesque for text) and Instrument Serif (italic for review pull-lines).
- One accent (a red-orange) used for the title, the tagline field, the turn line in the manifesto and the play button.
- The call to action appears early (for people ready to act) and again after the climax (when the story has earned it).
- No `prefers-reduced-motion` rules found; the meter is text, so it degrades well anyway.

**Borrow:** a diegetic scroll meter in the subject's own units, persistent in the nav; a page built as a stakes arc with one pinned climax and a silence after it; proof in the hero; a manifesto with a coloured turn; in-world captions.
**Reject:** nothing structural; add a reduced-motion path for the climax scaling.

## mrblack-case.dolganev.com (Mr.BLACK coffee franchise, a studio case)

**Idea performed:** selling a franchise is selling a business case, so the page is the **cup plus the numbers**. The brand's paper cup, printed with its mascot (a beard and a tie), is the guide through the whole page, surrounded by exact figures.

**Details worth learning:**
- **Hero:** a 3D cup with latte art over huge "Mr.BLACK" display type; the offer in one line ("Open a Mr.BLACK coffee shop in your city. $12,000 a year and up, at a 31% margin."), an "Apply now" link, and proof figures on the right ($12–36K net profit a year; $683K network revenue last year).
- **The cup as guide:** pinned at the centre and rotating with scroll to show its sides; it passes behind the giant type, takes on each section's ground colour (charcoal, sage, cream), and stays in view while "Business in exact figures" (revenue, payback 6 months, 12+ locations, 31% margin, each with a one-line qualifier) arrange around it.
- **Formats as stacked cards:** To go / Lounge / Specialty, each a full-height card (01/03 to 03/03) that pins and stacks: an interior render on the left and, on the right, a one-line description in typewriter caps plus the same three metrics (average profit, footprint, investment) with asterisked qualifiers.
- **Services:** the cup stays centred while numbered services (site search, training, equipment, purchasing) list on the left and branded product mockups (box, can) on the right.
- **Partnership climax:** a tower of stacked cups in four colours (a canvas image sequence, `cup-sequence`, alongside a 407 KB `cup.glb` for the guide), then a split screen: the image pinned left while "Terms & figures" scroll on the right ("Our financial model is fully transparent… no hidden fees"), starting with "$21,600 and up".
- **Type roles:** Unbounded (wide, bold display), Inter Tight (text), Courier Prime (typewriter for nav, labels and terms: the voice of a contract).
- Astro with Lenis smooth scroll; 13 sticky elements; a counting preloader; grain over a dark ground; one phone video; about 3.8 MB in total.

**Borrow:** a guide object that persists and changes per chapter; mixing a light model with one rendered sequence; exact figures with qualifiers around the product; stacked option cards with identical metrics; a typewriter voice for honest terms.
**Reject:** a cookie notice that blocks a corner for the whole visit; asterisked figures without the footnote close by.

## two26.studio (Two26, a boutique branding studio in Bucharest)

**Idea performed:** a small, two-person studio with a sense of humour: "Looking suspiciously good". The founders are the characters; the voice is the brand.

**Details worth learning:**
- **Hero:** a paper-collage illustration (a looping video) of the two founders walking, carrying signs that read "TWO" and "26", with their cat and dog; big rounded condensed headline; tilted black pill stickers on the headline ("Branding & design", "Independent studio", "No funny business"); orange loops drawn in SVG at the edges.
- **Style shift on scroll:** the same characters turn from collage into clean line drawing as you scroll on, moving the page from "show" to "explain".
- **Curved marquee:** a ribbon of text ("Let's make it make sense • Good looks included") flowing along a curved path.
- **Reading fill:** the "A bit about us" paragraph fills character by character from pale to black as you scroll, with an orange band at the leading edge; three stickers ("Professional overthinkers", "Nerding out on design", "Allergic to generic") pop in as the fill reaches them and stay as marginalia.
- **Work:** a sideways-moving strip of work images, then cards (image, client avatar, name, sector, round ↗ button); a handwritten "TWO 26" scrawl on the heading; the link onward is a joke with stickers ("The plot thickens", "There's more", "Very convenient").
- **Work card hover (two coats of paint):** each card holds the main image and an alternate (HeyGluco: a plush mascot, then the product worn on an arm). On hover, a very wide SVG brush stroke in the project's own tint (a pale pink for HeyGluco) paints across the card over ~1s, thickening from 0 to 1,200px as it travels, ease `power1.inOut`; ~350ms later a second stroke on a different zig-zag path paints the alternate image in through an SVG `<mask>`. The arrow button wobbles to rest (≈ −29° → −44° → +20° → 0° over 0.6s). On leave, both strokes reset in ~0.1s. The same draw-and-thicken stroke is the hover on the nav buttons (0.5s in, reversed 1.4× faster), so the brush is the site's hover language.
- **Card entrance:** each card opens from a small rounded aperture (`clip-path: inset(42.5%)`, 36px radius) to full size while the card inside settles from scale 1.45 and a 3D tilt (rotateX 25°, rotateY ±16°, rotateZ ±4°, alternating per card, perspective 800px) to flat.
- **Services as a route:** one orange line draws itself down the page (GSAP DrawSVG, scrubbed), winding through each service in big orange caps; small icons sit inside the words (a palette in "Art direction", a box in "Packaging design") with tilted sticker notes.
- **FAQ in voice:** "Can you start yesterday?", "What's with all the cats?". Footer: "Okay, that's enough website", "Handmade by humans. Well, digitally".
- **Shopfront chrome:** opening hours ("Monday–Friday 10:00–17:00") in the header beside a "Let's Talk" pill.
- Webflow, GSAP 3.15 (SplitText, ScrollTrigger, DrawSVG, CustomEase, CustomBounce), Lenis; ~160 KB inline script; reduced motion checked in script.

**Borrow:** a brand gesture (the brush) as the hover language, revealing a second image on work cards; the aperture card entrance; founders as characters; a style shift as a scroll transition; reading fill with a leading edge; marginalia stickers as a brand device; services as one drawn route; voice at every seam; shopfront facts in the chrome.
**Reject:** jokes that crowd out facts (keep pricing and process answers plain).

## primary.studio (Primary, a brand studio selling two-week "Brand Sprints")

**Idea performed:** speed. A productised two-week brand sprint, framed as a race, with the client's outcomes as the finish line.

**Details worth learning:**
- **One typeface** (Suisse Int'l), black and white, one **electric lime** accent that means speed, and a **lightning bolt** mark on the header button ("Reserve your spot · 1 slot left for December"), the marquee and the closing CTA.
- **Hero:** "Blazing fast brand sprints for startups" over a full-bleed photo of a client's business cards; then a full-width slideshow of client identities with outcome tags stepping down diagonally ("→ Look 10x bigger", "→ Get to market faster", "→ Stand out from the crowd").
- **Work grid:** large tiles with a small white label tab; on hover the tab grows into a full-width lime bar along the base. One tile carries a slowly rotating 3D emblem.
- **Argument as a chart:** "On your marks. Get set. Go-to-market." over a *Them* versus *You* bar (the lime bar long), then six plain outcome lines.
- **Testimonial:** one large quote on a black field, one named person and role (Head of Design, Lovable).
- **Lineage:** "Your journey is short because ours was long." Two decades at Pentagram and Milton Glaser, shown as a 2004 → Now timeline with past clients' logos (Apple, Asana, Peloton…).
- **Close:** a lime marquee of outcomes, then a giant pill CTA with the bolt: "Sprint past the competition", "Zero to full brand in two weeks. Let's get to work."
- Framer; ~8.5 MB; no custom cursor, no smooth scroll: the restraint is the point.

**Borrow:** a quiet frame that lets the work supply colour; an accent with one meaning plus a mark; one metaphor through name, copy, icon and action; outcomes as captions; argument as a simple chart; lineage with a turn of phrase; the label-to-bar hover; one big closing action.
**Reject:** a comparison chart without data behind it unless it's clearly illustrative; scarcity copy unless it's genuinely true and kept current.

## pear.no (Pear, an Oslo software and SEO firm paid by revenue share)

Observed 2026-11-06 at 1440 × 900 in a real browser, with its stylesheet, script and shaders read.

**Idea performed:** the name. "Pear makes you appear", and the firm is paid only from growth, so the page is an allegory of cultivation: figures from Renaissance paintings graft, grow, pick, peel, gild and finally raise a golden pear onto a plinth. Each labour carries one claim ("We build it." "We rank it." "We share in what it earns.").

**World:** Italian Renaissance oil painting throughout (blue fresco skies, velvet, marble, timber scaffolding, gold leaf), crossed with modern instruments: a holographic, prismatic trowel, lens flare, halftone dots and a surveyor's grid. Nothing on the page leaves that world.

**Details worth learning:**
- **One WebGL compositor** under a fixed HTML type layer. A hand-written fragment shader mixes films, frame sequences and plates, with a halftone dot screen (the pear is "printed" before it is gilded), a noisy burn edge between scenes, simulated paper (pulp, fibre, tooth, fleck), light rays and a reel move (zoom, spin, drift, motion blur). A second shader does chapter transitions: an iris opening from the centre broken by noise, a push, a wipe, a fade, a cut; incoming scenes "develop" from slightly desaturated to full colour.
- **Painted film, scrubbed by scroll:** four 10-second films (1080p H.264) and about 1,060 WebP frames in sequences of 89 to 483, with 768-px versions for phones. Frames load eight at a time by distance from the scroll position and decode three either side ahead.
- **Timeline in fractions:** one 48,150-px page; every scene, film and chapter link is placed in units out of 5,350. Chapter links jump to 1.2%, 23.2%, 40% and 62.8%.
- **Survey frame:** hairline rules at fixed percentages (header band 5.3vw; verticals at 5.3% and 85.6%), four-point stars where rules cross, a tick rail that is also the chapter indicator, mono labels on soft chips. Text stays in the frame; the paintings move beneath it.
- **Type:** Flecha in three optical sizes (L at 117 px, M at 77 px, S at 20 to 27 px), light weights for display; GT Standard for explanation; GT Standard Mono at 9 to 12 px, uppercase, tracked +0.16 to +0.2 em. Serif states, sans explains.
- **Colour:** press #0b0a09, paper #f2f1ed, ink #1d1c19, sky #015186; gold only inside the paintings, never as a UI colour.
- **Line reveals:** headings split into masked lines that slide up or across; the hero headline is split to characters. One easing, `cubic-bezier(.22,1,.36,1)`, with 0.26 to 0.82 s transitions.
- **The form is part of the world:** at the coda a robed figure on marble steps points at the night sky, and the three fields are tilted glass panels joined to the send button by constellation lines. The close returns to the start: two figures water and prune a young pear tree under the wordmark, so the story is a cycle of growth.
- **Text that focuses:** some statements arrive blurred and sharpen as they settle; incoming scenes start slightly grey and "develop" to full colour.
- **Copy:** antithesis as positioning ("Not an agency on the clock, a partner in the upside", opening and closing the page); "Full disclosure" chips; disqualification ("We say no more often than yes"); an FAQ ordered as a finance director's objections; an application, not a contact form.
- Stack: React, Vite, Tailwind 4, raw WebGL, two SVG filters (ink bleed, torn edge), adaptive pixel ratio on phones by frame time, Cloudflare Turnstile loaded on first focus of the form.

**Borrow:** the idea mined from the name and the payment model; claims staged as labours in one world; a survey frame over moving pictures; scenes that develop into colour; a halftone-to-gold "becoming visible" device; optical sizes matched to set size; disclosure and disqualification as trust.
**Reject:** wheel and key hijacking on desktop (it does turn off for reduced motion and touch); a DOM assembled in reverse, so assistive technology and search read the page bottom to top; unlabelled form fields; small text over moving paintings; 60 fps films for painted scenes; no still fallback when WebGL is missing; an unlabelled "40%".

## What they share

1. A single idea, performed by the signature moment.
2. A committed material world (wood and papyrus; contour and colour fields; aurora and film).
3. Texture over flat colour (grain, fibre, contour, blur).
4. Designed section transitions (torn edges, colour-field chapters, pinned scenes).
5. One display-type event, very large.
6. Depth from layers and light, almost never true 3D.
7. Quiet, plain information inside dramatic scenes (ledgers, credits, small facts).
8. Expo-out easing, long reveals (0.8–1.2s) and quick hovers (0.15–0.2s).
9. Media discipline: lazy, muted, looping, preloaded by metadata.
10. Reduced motion considered (except the BMW pitch, which is a lesson in what's lost).
11. The best ones make *entering* or *choosing* an act from the subject's world.
12. The hero object is a character that states the promise, and its scroll transition is a tiny story (setup, change, result).
13. The most refined one uses no assets at all: the subject's own principle, rendered in code.
14. One of the most memorable uses almost no technology: the interface speaks in the story's units (a distance to impact), and the page is ordered as a story with one climax.
15. Business pages can be just as crafted: the product as a guide object, with exact, qualified figures arranged around it.
16. Voice is a detail layer too: the funniest one puts a line in the brand's voice at every seam, and its devices (stickers, a drawn route, a reading fill) are cheap and repeatable.
17. Restraint can be the premium choice: the best studio site is one face, black, white and one meaningful accent, letting the work be the colour.
18. A whole page can be one allegory: the name becomes an image, and each claim becomes a labour in that image's world, played as a film under a quiet typographic frame.
