# hero-slideshow

**Job.** A full-bleed opening that shows a small set of objects or places one at a time, each arriving with a transition that has its own character, and each slide's words leaving and landing on cue.

| Field | Value |
|---|---|
| Beat intents | `hold`, `manipulate` |
| Rung | 2 (GSAP core) |
| Role | `signature` when the brand's idea is its objects (a range, a collection, a set of places); otherwise `supporting` |
| Cost band | Low: 2.8 KB module + GSAP core (shared) |
| Licence | MIT (Codrops), see `LICENSE`; GSAP under its own no-charge licence, not bundled |

## Transitions

Four, chosen from the source's 32 as the most distinct and all transform-only. Pick one per site.

| `transition` | What happens | Register |
|---|---|---|
| `push` | Slides push vertically; pictures move slower inside them, in parallax | Calm, editorial |
| `recede` | The current slide steps back and fades as the next rises over it | Quiet, deliberate |
| `card` | The next picture flies in as a small stretched card, then grows to fill the frame | Expressive |
| `camera` | The view pulls back, pans to the next picture and pushes in | Cinematic |

## Inputs

| Input | Default | Notes |
|---|---|---|
| markup | `.hs` > `.hs-slide` > `.hs-img` > `<img>` | Optional `.hs-text` with `.hs-line > span` inside each slide for words; `.hs-prev`, `.hs-next` buttons |
| `transition` | `'push'` | See above |
| `label` | `'Slideshow'` | Accessible name of the carousel |
| `swipe` | `true` | Horizontal swipes on touch; vertical page scroll stays native |
| `wheel` | `false` | Only for a site that is nothing but the slideshow; never capture page scroll on a normal page |
| `textDelay` | per transition | When the next slide's words rise in |
| `onChange(i, slide)` | none | For counters or anything outside the slides |

## Cost (measured)

Clean-room example, headless Chrome: 60 fps, 0 ms of long tasks on desktop and mobile, all four transitions; no overflow.

## Fallbacks and access

- **Reduced motion:** a 0.5 s crossfade; words appear without motion.
- **Keyboard:** arrow keys move slides only while the slideshow has focus (the source listened to the whole page). Buttons are real buttons.
- **Screen readers:** carousel semantics, hidden slides are `aria-hidden` and inert, and a polite live region announces "Slide 2 of 4". Tested.
- **No autoplay.** Deliberately left out: autoplaying heroes take control away from the visitor. If a brief truly needs it, it must come with a visible pause button.

## Provenance

- Source: [Fullscreen Image Slideshow Animations, Codrops](https://github.com/codrops/SlideshowAnimations), demos 1, 4, 8 and 24, MIT.
- Admitted: 22 November 2026, intake run 003.
- Changed: one engine instead of 32 demos; no wheel capture by default; focus-scoped keys; swipe; carousel semantics and live region; filters removed from `card`; word choreography added inside slides (the source had none); demo imagery removed.
- Clean-room test: restyled as an invented chandlery with original still-life artwork. Passed on all four transitions.
