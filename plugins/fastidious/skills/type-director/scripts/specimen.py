#!/usr/bin/env python3
"""specimen: sets candidate type pairings with the project's real copy, side by side, and renders them.

    python3 specimen.py --pair "IM Fell English|Cabin" --pair "Libre Caslon Display:400|Source Serif 4" \\
        --copy COPY-DECK.md --bg "#1f1b17" --fg "#f0e6d1" --out type/specimen.png

Each --pair is "Display family[:weight]|Text family[:weight]" (a third "|Utility family" is optional). Font files
come from Fontsource on the npm registry (@fontsource/<family>, the Google Fonts files under their own licences),
cached in ~/.cache/fastidious/fonts, so the specimen renders offline and exactly. Copy comes from COPY-DECK.md
(spine, hero.sub, the first detail lines and a label) or from --head/--body. Renders a PNG with Playwright for
Python when it is installed; otherwise writes the HTML next to --out for a browser.
"""
import argparse
import glob
import html
import os
import re
import subprocess
import sys
import tarfile
import tempfile

CACHE = os.path.join(os.path.expanduser("~"), ".cache", "fastidious", "fonts")


def slug(family):
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def fetch(family):
    """Return {(weight, style): path} for a family's latin woff2 files, downloading from Fontsource once."""
    s = slug(family)
    d = os.path.join(CACHE, s)
    if not glob.glob(os.path.join(d, "files", "*.woff2")):
        os.makedirs(CACHE, exist_ok=True)
        tmp = tempfile.mkdtemp()
        subprocess.run(["npm", "pack", f"@fontsource/{s}", "--silent", "--pack-destination", tmp], check=True,
                       capture_output=True, timeout=180)
        tgz = glob.glob(os.path.join(tmp, "*.tgz"))[0]
        with tarfile.open(tgz) as t:
            members = [m for m in t.getmembers() if m.name.startswith("package/files/") and "-latin-" in m.name
                       and m.name.endswith(".woff2") and "-ext-" not in m.name]
            for m in members:
                m.name = m.name.replace("package/", "", 1)
            kw = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}
            t.extractall(d, members=members, **kw)
    out = {}
    for p in glob.glob(os.path.join(d, "files", "*.woff2")):
        m = re.search(r"-latin-(\d+)-(normal|italic)\.woff2$", p)
        if m:
            out[(int(m.group(1)), m.group(2))] = p
    if not out:
        raise SystemExit(f"specimen: no latin files for {family} on Fontsource")
    return out


def parse_face(spec):
    name, _, w = spec.partition(":")
    return name.strip(), int(w) if w else None


def font_face_css(family, files):
    rules = []
    for (w, style), p in sorted(files.items()):
        rules.append(f"@font-face{{font-family:'{family}';src:url('file://{p}') format('woff2');font-weight:{w};font-style:{style};font-display:block}}")
    return "\n".join(rules)


def nearest(files, want, style="normal"):
    ws = sorted({w for (w, s) in files if s == style}) or sorted({w for (w, s) in files})
    return min(ws, key=lambda w: abs(w - (want or 400)))


def copy_from_deck(path):
    text = open(path, encoding="utf-8").read()
    rows = {}
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.match(r"^[a-z0-9.]+$", cells[0]):
                rows[cells[0]] = cells[1].replace(" / ", "\n")
    head = rows.get("hero.h1") or rows.get("spine") or "The quick brown fox"
    sub = rows.get("hero.sub", "")
    body = " ".join(v for k, v in rows.items() if k.endswith(".detail"))[:420] or rows.get("ask.body", "")
    label = next((v for k, v in rows.items() if k.startswith("faq.") and k.endswith(".q")), "Label")
    return head, sub, body, label


def page(pairs, head, sub, body, label, bg, fg, accent):
    css, panels = [], []
    for i, p in enumerate(pairs):
        faces = [parse_face(x) for x in p.split("|")]
        names = []
        for fam, w in faces:
            files = fetch(fam)
            css.append(font_face_css(fam, files))
            names.append((fam, nearest(files, w), files))
        (dfam, dw, dfiles), (tfam, tw, tfiles) = names[0], names[1]
        ufam = names[2][0] if len(names) > 2 else tfam
        has_italic = any(s == "italic" for (_, s) in tfiles)
        h = html.escape(head).replace("\n", "<br>")
        panels.append(f"""<section style="--d:'{dfam}';--t:'{tfam}';--u:'{ufam}';--dw:{dw};--tw:{tw}">
  <p class="tag">{chr(65 + i)} · {html.escape(dfam)} with {html.escape(tfam)}{(' and ' + html.escape(ufam)) if ufam != tfam else ''}</p>
  <div class="grid"><div>
    <p class="label">{html.escape(label)}</p>
    <h1>{h}</h1>
    <p class="sub">{html.escape(sub)}</p>
    <p class="body">{html.escape(body)}</p>
    <p class="figs">4,000 bottles · £84 · 11 months · 1720 · 0123456789</p>
  </div><div class="phone">
    <p class="label">{html.escape(label)}</p>
    <h2>{h}</h2>
    <p class="body">{html.escape(body)}</p>
    {'<p class="body"><i>Italic: the long way round, on purpose.</i></p>' if has_italic else '<p class="note">No italic in this text face.</p>'}
  </div></div>
</section>""")
    return f"""<!doctype html><meta charset="utf-8"><style>{''.join(css)}
body{{margin:0;background:{bg};color:{fg};-webkit-font-smoothing:antialiased}}
section{{padding:56px 64px;border-bottom:1px solid color-mix(in srgb,{fg} 18%,transparent)}}
.tag{{font:500 13px/1.4 ui-monospace,Menlo,monospace;letter-spacing:.06em;opacity:.65;margin:0 0 28px}}
.grid{{display:grid;grid-template-columns:1fr 360px;gap:64px;align-items:start}}
h1{{font-family:var(--d);font-weight:var(--dw);font-size:88px;line-height:.98;letter-spacing:-.015em;margin:0 0 22px;text-wrap:balance}}
h2{{font-family:var(--d);font-weight:var(--dw);font-size:44px;line-height:1;margin:0 0 14px}}
.sub{{font-family:var(--t);font-weight:var(--tw);font-size:26px;line-height:1.35;margin:0 0 18px;max-width:34em}}
.body{{font-family:var(--t);font-weight:var(--tw);font-size:19px;line-height:1.55;margin:0 0 14px;max-width:36em}}
.phone .body{{font-size:17px}}
.label{{font-family:var(--u);font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:{accent};margin:0 0 14px}}
.figs{{font-family:var(--t);font-size:22px;font-variant-numeric:oldstyle-nums;opacity:.85;margin:0}}
.note{{font:13px ui-monospace,monospace;opacity:.6}}
</style>{''.join(panels)}"""


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pair", action="append", required=True)
    ap.add_argument("--copy", help="COPY-DECK.md to take the lines from")
    ap.add_argument("--head", default="")
    ap.add_argument("--body", default="")
    ap.add_argument("--bg", default="#f4f2ee")
    ap.add_argument("--fg", default="#1b1a18")
    ap.add_argument("--accent", default="currentColor")
    ap.add_argument("--out", default="specimen.png")
    a = ap.parse_args(argv)
    head, sub, body, label = copy_from_deck(a.copy) if a.copy else (a.head or "The quick brown fox", "", a.body, "Label")
    if a.head:
        head = a.head
    if a.body:
        body = a.body
    doc = page(a.pair, head, sub, body, label, a.bg, a.fg, a.accent)
    html_path = os.path.splitext(a.out)[0] + ".html"
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(doc)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(f"specimen: wrote {html_path}; install Playwright for Python to render a PNG")
        return 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        pg.goto("file://" + os.path.abspath(html_path))
        pg.wait_for_timeout(400)
        pg.screenshot(path=a.out, full_page=True)
        b.close()
    print(f"specimen: {len(a.pair)} pairings, {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
