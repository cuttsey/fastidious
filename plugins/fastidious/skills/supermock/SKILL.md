---
name: supermock
description: Present finished design work the way professional studios do, as physical artefacts in the world, preferably moving. Captures the real work (a site's scroll and interactions, posters, social posts, ads) and composes it into animated mockups. These include phones, tablets and laptops in CSS 3D, artwork corner-pinned into real photographs (billboards, bus shelters, Tube and station posters, shop windows, signage, screens), and animated display ads in IAB sizes. Renders frame-perfect MP4 clips with posters and a showreel. Use when work is finished and someone asks to "mock it up", "show it in context", "present the work", "make case-study visuals", "put it on a billboard or phone", or wants presentation videos for a pitch, case study, portfolio or social.
---

# Supermock

Clients and juries judge work by how it looks **in the world**. A flat screenshot says "a file"; the same work on a phone in a hand, on a 48-sheet on a real street, or running as a banner says "a campaign that exists". **Moving presentation beats static.** A scroll recorded inside a device, a poster being pasted onto a board, or a banner playing through its beats shows behaviour and craft that a still cannot.

**The personality is the product,** here too. The mockups carry the brand's world: its grounds, its light, its places. A Devon wrestling society belongs on a Bristol roadside board and a phone on a sky-blue ground, not in a generic glass-and-chrome showroom.

## Where it sits
- **After the work is finished and checked.** It presents real output, never a substitute for building it.
- **Reads:** the built site (URL), templates and artwork, `BRAND-SYSTEM.md` (grounds, tokens, fonts), and `SIGN-SYSTEM.md` (the brand's world: which places and situations fit).
- **Writes:** `supermock/` in the project: `capture/`, `art/`, `env/` (photos plus `credits.json`), `configs/`, `out/` (MP4, poster JPG, optional WebM/GIF, `reel.mp4`) and an `index.html` presentation page. Publish the page as an Artifact when it is meant to be shared.

## Tools (all local: Node 22, headless Chrome, ffmpeg)
| Script | Does |
|---|---|
| `scripts/capture.mjs <url> --device phone\|tablet\|laptop\|desktop --scroll <s> --to <selector\|end>` | Records the real page as a frame sequence while scrolling with easing and holds at both ends, so scroll-linked animation plays as a visitor sees it. Also `--still` and `--full`. For screens that are *used* rather than scrolled (a map, a configurator, an app), `--play <s> --steps steps.json` runs scripted actions (`[{"at": 1.2, "js": "…"}]`) on virtual time, so tweens and transitions advance exactly one frame per capture. |
| `scripts/shoot.mjs <art.html> --w --h --out art.png` | Renders artwork HTML at the format's exact pixel size: a poster, billboard or screen. |
| `scripts/render.mjs <scene.html> --config c.json --out out/name` | Steps a scene frame by frame (`renderAt(t)`) and encodes H.264 MP4 plus a poster frame. `--still <t>` gives one frame for checking; `--webm` and `--gif` give alternates. |
| `scripts/reel.mjs --out out/reel.mp4 a.mp4 b.mp4 …` | Joins clips with crossfades onto one 1920×1080 canvas. |

Scenes live in `scenes/` and share `supermock.js` (keyframes, easing, frame sequences, corner-pin homography):
- **`device.html`** draws a phone, tablet or laptop in CSS 3D on a seamless studio ground, with a soft contact shadow and a moving screen glare. The captured sequence plays on the screen while the camera orbits (`camera` keyframes: `rx`, `ry`, `rz`, `s`, `x`, `y`; laptop `lid`).
- **`pin.html`** corner-pins artwork into a real photograph. Each quad takes `corners` [tl, tr, br, bl] in photo pixels and a still `art`, `slides` (for digital screens) or a `frames` sequence (a moving DOOH screen). It matches the light with `haze`, a `shade` multiply tint, `filter` and `sheen`, and can show a `paste` reveal for paper sites. Camera `zoom`, `fx` and `fy` give a slow push-in, and `debug: true` outlines the quad so you can check the corners.
- **`ad.html`** builds animated display ads in IAB sizes from brand tokens: two beats (headline, sub, figure) and an end frame (logo, line, CTA, URL). Pass `css` in the config so the headline follows the brand's own type, not the scene's default. It adapts its layout to box, wide and tall formats. Formats are listed in `references/formats.md`.

## The method

### 1. Choose the set (plan before you render)
Pick four to eight artefacts that tell the work's story, mixing scales: one or two **devices** for the product, one or two **out-of-home** placements for presence, **display or social** for reach, and one **close-up** detail. Choose places from the brand's world, such as the brand's own region, its audience's commute, or its own premises. Write one line per artefact: *what it shows* and *why this place*.

### 2. Capture the real work
- **Sites:** `capture.mjs` at the device's real viewport, scrolling through the page's best sequence: its hero interaction, a meter, a reveal. Use `--hover` for fine-pointer states. 6–8 seconds at 30fps, holding at both ends.
- **Used screens (maps, tools, apps):** `capture.mjs --play` with a steps file. Drive the page through its real controls (dispatch the clicks, key presses or Ctrl+wheel events a visitor would make), not its internals. Space steps 2–3 seconds apart so each state reads, and fire a smooth zoom as a run of small wheel events, one per frame.
- **Static artwork:** build it at the format's **true ratio** (`references/formats.md`) and render it with `shoot.mjs`. Never squash a 16:9 design onto a 2:1 billboard. Billboard copy is seven words or fewer, readable at 50 metres.

### 3. Source environments honestly
- Search open collections with `design-taste-frontend/scripts/assets.mjs "blank billboard <city>"`, then "bus shelter", "station poster" and "shop window". Prefer CC0 or public domain; CC BY is fine with a credit. Avoid BY-SA unless the client accepts share-alike on the composite.
- **Reject photos with other brands' live adverts or prominent logos** in or near the surface. Never place work where it impersonates a real campaign, venue or media owner's endorsement.
- Look at every photo. Pick surfaces seen roughly front-on to about 35°, with clear edges, even light, and no people crossing them.

### 4. Pin and match
1. Read the four inner corners of the surface (the printable area, not the frame) from the image at full resolution. Order them tl, tr, br, bl, in original pixels.
2. Render with `"debug": true` and `--still`, check the magenta outline sits exactly on the edges, and adjust.
3. Match the light. Use haze for backlit or hazy scenes (0.05–0.15), a `shade` tint toward the scene's light colour, and a slightly lowered contrast and saturation. Add `sheen` for glass-fronted panels. Work sitting brighter or sharper than its photo is the most common tell of a cheap mockup.
4. Use motion that belongs to the medium: paper sites **paste** on, digital screens **change slides or play**, and the camera **pushes in slowly** (zoom 1.0 to about 1.25 over the clip). Frame out distracting signage with the camera.

### 5. Render, check, reel
- Check a `--still` at three moments for each clip before rendering the full clip. Fix collisions, overflow and wrong light at the still stage.
- Render 6–10 second clips at 1920×1080 and 30fps. Join them with `reel.mjs` in story order: product → presence → reach → detail.
- Watch the poster frames. A clip whose poster frame is weak gets a better moment (`render.mjs` takes the poster at 60% of the clip; re-pick if needed).

### 6. Present
Build `supermock/index.html`, the "work in the world" page, as a real piece of design (`artifact-design` and the brand's tokens). It opens on the reel, then shows each clip as a muted, looping, `playsinline` video with its poster, a caption (format, place, what it shows), and the photo credits. Publish it as an Artifact, with the videos as files (each under 15 MB; re-encode with a higher CRF if not).

## Rules
- **Real work only.** Everything inside the frame is the actual build or artwork. Don't improve the work in the mockup.
- **Label concept placements as concepts** ("Concept: 48-sheet, Bristol") unless the campaign actually ran there.
- **Credit every photograph** (from `env/credits.json`) on the presentation page.
- **Respect motion preferences** on the presentation page: show posters and controls under reduced motion, with no forced autoplay.
- **No fake people or testimonials** in scenes. Use hands or devices only with real, licensed photography.

## Extending
A new environment is a photo plus a config, not new code. A new device or format belongs in `device.html` or `ad.html`, or as a new scene following the `SUPERMOCK` contract (`ready`, `renderAt(t)` and `window.SUPERMOCK_CONFIG`).
