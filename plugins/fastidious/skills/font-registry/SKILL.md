---
name: font-registry
description: Use whenever Fastidious chooses or sets type: any build, page, part example, mock-up, test page or showcase. Picks fonts only from the registry and never uses basic or generic faces.
---

# Font registry

Every typeface Fastidious uses comes from this registry, which is drawn from the [Awwwards free fonts collection](https://www.awwwards.com/awwwards/collections/free-fonts/). Fastidious keeps no font files: it loads each font by reference. The full catalogue of all 287 entries, with each one's licence status, is `parts/fonts/CATALOGUE.md` and `parts/fonts/catalogue.json` in the parts library.

## Non-negotiable

1. **Never a basic or generic face.** Arial, Helvetica, Helvetica Neue, Georgia, Times, Verdana, Tahoma, Segoe UI, Roboto, Open Sans, system-ui, -apple-system, ui-monospace, Menlo, Courier and similar system or default faces are never the face of anything: not a build, a part example, a mock-up, a test page or a quick sketch. A generic keyword (`sans-serif`, `serif`, `monospace`) may appear only as the last fallback in a stack.
2. **Only registry fonts.** Use a font from the tables below. Any other entry in the catalogue is `unverified` and may not be used until its licence has been read on its source page and the catalogue updated (status, licence, loading route).
3. **Reference, never copy.** Link the stylesheets below. Do not download font files into Fastidious, the parts library or a skill. A client project that must self-host takes its own copy from the official source, under that font's licence.
4. **Inter and Geist read as defaults.** Allowed, but always paired with a distinctive display face; never the identity on their own.
5. **Three tokens.** Every page sets `--fd-display`, `--fd-body` and `--fd-mono` and adds `html { font-synthesis: none; }`. Parts read the tokens and never bring a face of their own.
6. **Choose for meaning.** Pick the face whose features carry the meaning set in `SIGN-SYSTEM.md` (`sign-system-architect` describes type by its features; this registry supplies the face). Vary faces between builds: the combination makes a site memorable.

## Open fonts (load from jsDelivr)

All SIL Open Font Licence 1.1 except Redressed (Apache 2.0). Hanken Grotesk, Bitter and Libertinus stand in for HK Grotesk, Bitter Ht and Linux Libertine, which are not openly licensed.

| Family (CSS name) | Axes or weights | Stylesheet |
|---|---|---|
| 'Geist Variable' | wght 100–900 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/geist@5.3.0/wght.css` (+ `wght-italic.css`) |
| 'Geist Mono Variable' | wght 100–900 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/geist-mono@5.3.0/wght.css` (+ `wght-italic.css`) |
| 'Inter Variable' | opsz 14–32, wght 100–900 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/inter@5.3.0/standard.css` (+ `standard-italic.css`) |
| 'Archivo Variable' | wght 100–900, wdth 62–125 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo@5.3.0/standard.css` (+ `standard-italic.css`) |
| 'Archivo Narrow Variable' | wght 400–700 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo-narrow@5.3.0/wght.css` (+ `wght-italic.css`) |
| 'Trispace Variable' | wght 100–800, wdth 75–125 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/trispace@5.3.0/standard.css` |
| 'Aleo Variable' | wght 100–900 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/aleo@5.3.0/wght.css` (+ `wght-italic.css`) |
| 'Bitter Variable' | wght 100–900 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/bitter@5.3.0/wght.css` (+ `wght-italic.css`) |
| 'Hanken Grotesk Variable' | wght 100–900 | `https://cdn.jsdelivr.net/npm/@fontsource-variable/hanken-grotesk@5.3.0/wght.css` (+ `wght-italic.css`) |
| 'Spectral' | static 200–800 | `https://cdn.jsdelivr.net/npm/@fontsource/spectral@5.3.0/400.css`, one file per weight (`300.css`, `400-italic.css`, `600.css` …) |
| 'Libertinus Serif' | static 400, 600, 700 | `https://cdn.jsdelivr.net/npm/@fontsource/libertinus-serif@5.3.0/400.css` (+ `400-italic.css`, `600.css`, `700.css`) |
| 'Libertinus Sans' | static 400, 700 | `https://cdn.jsdelivr.net/npm/@fontsource/libertinus-sans@5.3.0/400.css` (+ `400-italic.css`, `700.css`) |
| 'Bebas Neue' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/bebas-neue@5.3.0/400.css` |
| 'Poetsen One' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/poetsen-one@5.3.0/400.css` |
| 'Oranienbaum' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/oranienbaum@5.3.0/400.css` |
| 'Grand Hotel' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/grand-hotel@5.3.0/400.css` |
| 'Redressed' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/redressed@5.3.0/400.css` |
| 'Norwester' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/norwester@5.3.0/400.css` |
| 'Bagnard' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/bagnard@5.3.0/400.css` |
| 'Bagnard Sans' | static 400 | `https://cdn.jsdelivr.net/npm/@fontsource/bagnard-sans@5.3.0/400.css` |

Three open fonts are not on Fontsource; write an `@font-face` that points at the font's own repository, pinned to a commit (the parts library keeps these in `parts/fonts/faces/`):

| Family | Weights | Files |
|---|---|---|
| 'Mattone' | 400, 700, 900 | `https://cdn.jsdelivr.net/gh/collletttivo/mattone@b1dc55dc6a432708ab00329d452d8f6907c6e570/fonts/Mattone-{Regular,Bold,Black}.woff2` |
| 'Absans' | 400 | `https://cdn.jsdelivr.net/gh/collletttivo/absans@e1ba5d9a2359934df024b4ebef4c1be76e0db263/fonts/Absans-Regular.woff2` |
| 'Junicode VF' | wght 300–700, wdth 75–125 | `https://cdn.jsdelivr.net/gh/psb1558/Junicode-font@6978714c2bb053861a68489c052b1c88e7596bfb/webfiles/JunicodeVF-{Roman,Italic}.woff2` (about 1 MB each: use for display only) |

Width axes, for type that changes shape (`text-emphasis/axis-ramp`): Archivo, Trispace, Junicode.

## Fontshare fonts (load through the Fontshare API only)

Satoshi, Clash Display, Cabinet Grotesk, Chillax and Ranade. Licence: the ITF Free Font License (version 2.0), or the OFL for some fonts; check the font page. Commercial use and the API are allowed. Redistribution, giving files to contractors, subsetting and format conversion are not. So load them only by linking the API, for example:

`https://api.fontshare.com/v2/css?f[]=satoshi@1,2&display=swap` (likewise `clash-display`, `cabinet-grotesk`, `chillax`, `ranade`).

## Example

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/bagnard@5.3.0/400.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/hanken-grotesk@5.3.0/wght.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/trispace@5.3.0/standard.css">
<style>
  :root {
    --fd-display: 'Bagnard', serif;
    --fd-body: 'Hanken Grotesk Variable', sans-serif;
    --fd-mono: 'Trispace Variable', monospace;
  }
  html { font-synthesis: none; }
</style>
```

## Checking before sign-off

Search the build's HTML, CSS and JavaScript for basic faces (Arial, Helvetica, Georgia, Times, system-ui, -apple-system, Segoe, Roboto, Menlo, ui-monospace, Courier). Any hit that is not the generic keyword at the end of a stack fails the build. In a browser, confirm with `document.fonts` that every visible text style renders in a registry face.

## Adding a font to the registry

1. Open the entry's source page from the catalogue and read its licence.
2. Only a licence that allows commercial web use qualifies. Personal-use-only, unclear or missing licences stay `unverified`.
3. Record the licence, the CSS family name and a loading route that does not copy files into Fastidious (Fontsource on jsDelivr, the font's own repository on jsDelivr, or the foundry's own API).
4. Update `catalogue.json`, `CATALOGUE.md` and the tables above.