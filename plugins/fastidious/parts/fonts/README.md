# Font registry

Fastidious keeps no font files. This folder says which typefaces a build may use and where to load each one from. The source list is the [Awwwards free fonts collection](https://www.awwwards.com/awwwards/collections/free-fonts/); all 287 entries are in `CATALOGUE.md` and `catalogue.json`.

## The rule

1. **Never a basic or generic face.** Arial, Helvetica, Helvetica Neue, Georgia, Times, Verdana, Tahoma, Segoe UI, Roboto, system-ui, -apple-system, ui-monospace, Menlo, Courier and the like are never the face of anything Fastidious makes: not a build, a part example, a mock-up or a test page. A generic keyword (`sans-serif`, `serif`, `monospace`) may appear only as the last fallback in a stack.
2. **Only fonts from this registry.** Use an entry whose status is `open`, `open-equivalent` or `fontshare`, by linking the stylesheet listed for it. An `unverified` entry may not be used until its licence has been read and its entry updated.
3. **Reference, never copy.** Load fonts from the links in the catalogue (jsDelivr for open fonts, the Fontshare API for Fontshare fonts). Do not download font files into Fastidious. A client project that must self-host takes its own copy from the official source under that font's licence.
4. **Inter and Geist read as defaults.** They are allowed, but pair them with a distinctive display face; never let them carry an identity alone.
5. **Three tokens.** Pages set `--fd-display`, `--fd-body` and `--fd-mono`. Parts read those tokens for any default type and never bring a face of their own.

## Using a font

Find the entry in `CATALOGUE.md`, link its stylesheets, set the tokens:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo@5.3.0/standard.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/geist-mono@5.3.0/wght.css">
<style>
  :root { --fd-display: 'Archivo Variable', sans-serif; --fd-mono: 'Geist Mono Variable', monospace; }
  html { font-synthesis: none; }
</style>
```

`font-synthesis: none` stops the browser faking bold or italic for single-weight faces. Three open fonts are not on Fontsource (Mattone, Absans, Junicode); `faces/` holds a small stylesheet for each that points at the font's own repository, pinned to a commit.

Variable fonts with a width axis, for `text-emphasis/axis-ramp`: Archivo (62–125), Trispace (75–125), Junicode (75–125).

## Statuses

- **`open` (17 entries, 20 families) and `open-equivalent` (3).** SIL Open Font Licence or Apache 2.0. HK Grotesk, Bitter Ht and Linux Libertine are used through their open successors: Hanken Grotesk, Bitter and Libertinus.
- **`fontshare` (5).** Satoshi, Clash Display, Cabinet Grotesk, Chillax, Ranade. The ITF Free Font License (version 2.0, read 22 November 2026) allows commercial use and the Fontshare API, but forbids redistribution, handing files to contractors, subsetting and format conversion. Link the API stylesheet; never copy the files.
- **`unverified` (255).** Behance, Gumroad, Pangram Pangram, Dirtyline Studio, Pixel Surplus, Fontfabric, Atipo and others. Many are free for personal use only. Read the licence on the source page; if it allows commercial web use, record the licence and the loading route in the catalogue and change the status.
- **`resource` (7).** Galleries, foundries and articles.
