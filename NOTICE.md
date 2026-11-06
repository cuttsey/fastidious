# Notice

Fastidious is released under the MIT Licence (see `LICENSE`). This file lists everything it uses that belongs to someone else.

## Installed at pinned commits, not bundled

These skills are fetched from their authors' repositories by `crew_stack.py` and `promo_stack.py`, at the exact commits in `crew.lock.json` and `promo-stack.lock.json`, and copied unchanged except where a lock says a skill is renamed. Each stays under its own licence, which travels with its folder. None of these projects is affiliated with Fastidious or has endorsed it.

| Skills | Source | Licence |
| --- | --- | --- |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 |
| `design-taste-frontend` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | MIT |
| `emil-design-eng`, `animate`, `animate-expo`, `animation-performance`, `animation-vocabulary`, `apple-design`, `ask-sonner`, `break-ui`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `pick-ui-library`, `prototype`, `review-animations` | [emilkowalski/skills](https://github.com/emilkowalski/skills) | MIT |
| `gsap-core`, `gsap-scrolltrigger` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | MIT |
| `anatomy` | [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | MIT |
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` (optional film stack) | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 |
| `motionmaxxing` (optional film stack) | [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | Apache-2.0; its vendored GSAP runtime is under the GreenSock Standard License |
| `business-motion-film` (optional film stack) | [echris6/motion-video-kit](https://github.com/echris6/motion-video-kit) | MIT |
| `elevenlabs-music`, `elevenlabs-sound-effects`, `elevenlabs-text-to-speech`, `elevenlabs-speech-to-text` (optional film stack, renamed) | [elevenlabs/skills](https://github.com/elevenlabs/skills) | MIT |
| `watch` (optional) | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | MIT |

## Included in this repository

- `blender-build/cache/polyhaven/studio_small_09/studio_small_09_1k.hdr`: "Studio Small 09" by Sergej Majboroda, from [Poly Haven](https://polyhaven.com/a/studio_small_09), CC0 1.0.
- `assets/fastidious-film.mp4`, `assets/fastidious-teaser.gif` and `assets/fastidious-social-preview.png`: the film's music is "Cat Walk" by Arulo, from [Mixkit](https://mixkit.co/free-stock-music/), under the Mixkit Stock Music Free License. Type is [Archivo](https://fonts.google.com/specimen/Archivo) and [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono); the invented sites in the film also use Instrument Serif, Fredoka, Bricolage Grotesque, Big Shoulders Display and Inter, all under the SIL Open Font License. The four businesses in the film are invented.
- `colour-director/references/wada-colours.json`: the colours and combinations of Sanzo Wada's *A Dictionary of Color Combinations*, from [mattdesl/dictionary-of-colour-combinations](https://github.com/mattdesl/dictionary-of-colour-combinations) by Matt DesLauriers, after Dain Blodorn Kim's dataset, under the MIT licence (`wada-colours.LICENSE.md`). The book is published by Seigensha.
- `examples/hollow-lane`: the page uses the IM Fell types, digitised by Igino Marini, and Source Serif 4 by Frank Griesshammer for Adobe, under the SIL Open Font License, loaded from Google Fonts.
- `type-director/references/typefaces.json` describes typefaces by name for selection; the faces belong to their designers and foundries, and `specimen.py` downloads them from Fontsource under their own licences.
- `reference-curator` data files index public design sources and published design systems by name and address only. Those sources and systems, and any trademarks in them, belong to their owners.
- `detail-craft/references/exemplars.md` annotates publicly visible websites for study. Those sites and any trademarks they contain belong to their owners.

## Fetched at run time

Fonts, photographs, footage, music and other assets that the skills fetch or generate keep their own licences and terms. `asset-director`, `supermock` and `showreel-director` record the licence of every item they use. Outputs from image and video model APIs used by `fastidious-motion` are subject to each provider's terms.
