#!/usr/bin/env python3
"""palette: sources, builds and checks colour palettes in OKLab, the perceptual space (Ottosson, 2020).

    python3 palette.py extract world/S01.jpg world/S04.jpg --k 8           # the colours of the subject's own world
    python3 palette.py wada --near "#a86b2b,#5c6e30" --size 3 --top 6      # historic combinations from Sanzo Wada
    python3 palette.py scale "#5c6e30" --steps 11                           # a tonal ramp in OKLCH
    python3 palette.py check tokens.json                                    # contrast, value, chroma, cliches
    python3 palette.py sheet tokens.json --out colour/sheet.html            # a swatch sheet with text samples

tokens.json is {"colours": {"name": "#hex", ...}, "pairs": [["text", "ground"], ...], "large": [["display", "ground"]]}.
extract samples images and films with ffmpeg. Everything else is the Python 3 standard library.
"""
import argparse
import json
import math
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WADA = os.path.join(os.path.dirname(HERE), "references", "wada-colours.json")


# Colour maths -------------------------------------------------------------------------------------------------

def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def to_lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def from_lin(c):
    c = max(0.0, min(1.0, c))
    return 255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def rgb_oklab(rgb):
    r, g, b = (to_lin(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklab_lin(lab):
    L, a, b = lab
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklab_rgb(lab):
    return tuple(from_lin(c) for c in oklab_lin(lab))


def in_gamut(lab, eps=1e-4):
    return all(-eps <= c <= 1 + eps for c in oklab_lin(lab))


def oklch(lab):
    L, a, b = lab
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def from_oklch(L, C, h):
    """OKLCH to an in-gamut sRGB hex, reducing chroma until it fits."""
    lo, hi = 0.0, C
    lab = (L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h)))
    if in_gamut(lab):
        return rgb_hex(oklab_rgb(lab))
    for _ in range(24):
        mid = (lo + hi) / 2
        t = (L, mid * math.cos(math.radians(h)), mid * math.sin(math.radians(h)))
        if in_gamut(t):
            lo = mid
        else:
            hi = mid
    return rgb_hex(oklab_rgb((L, lo * math.cos(math.radians(h)), lo * math.sin(math.radians(h)))))


def de(a, b):
    """Distance in OKLab, roughly 0.02 just noticeable, 0.1 clearly different."""
    return math.dist(a, b)


def luminance(rgb):
    r, g, b = (to_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(h1, h2):
    a, b = luminance(hex_rgb(h1)), luminance(hex_rgb(h2))
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


# Sourcing -----------------------------------------------------------------------------------------------------

def pixels(path, width=64):
    """RGB tuples of an image or the first frame of a film, scaled small, through ffmpeg."""
    if not shutil.which("ffmpeg"):
        raise SystemExit("palette: extract needs ffmpeg")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-frames:v", "1", "-vf", f"scale={width}:-2",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return [tuple(raw[i:i + 3]) for i in range(0, len(raw) - 2, 3)]


def kmeans(points, k, iters=20, seed=7):
    """k-means++ in OKLab. Returns [(centre_lab, share)] sorted by share."""
    rnd = random.Random(seed)
    cents = [rnd.choice(points)]
    while len(cents) < k:
        d = [min(de(p, c) ** 2 for c in cents) for p in points]
        tot = sum(d) or 1
        r, acc = rnd.random() * tot, 0
        for p, w in zip(points, d):
            acc += w
            if acc >= r:
                cents.append(p)
                break
    for _ in range(iters):
        groups = [[] for _ in cents]
        for p in points:
            groups[min(range(len(cents)), key=lambda i: de(p, cents[i]))].append(p)
        cents = [tuple(sum(c[j] for c in g) / len(g) for j in range(3)) if g else cents[i] for i, g in enumerate(groups)]
    n = len(points)
    return sorted(((c, len(g) / n) for c, g in zip(cents, groups) if g), key=lambda x: -x[1])


def extract(paths, k=8):
    pts = []
    for p in paths:
        pts += [rgb_oklab(px) for px in pixels(p)]
    random.Random(1).shuffle(pts)
    return [(rgb_hex(oklab_rgb(c)), share, oklch(c)) for c, share in kmeans(pts[:6000], k)]


def wada_combos(path=WADA):
    with open(path, encoding="utf-8") as f:
        colours = json.load(f)
    combos = {}
    for c in colours:
        for n in c["combinations"]:
            combos.setdefault(n, []).append(c)
    return combos


def wada_near(anchors, size=None, top=6, path=WADA):
    """Combinations from Wada's dictionary ranked by how closely they contain the anchor colours."""
    alabs = [rgb_oklab(hex_rgb(h)) for h in anchors]
    out = []
    for n, cs in wada_combos(path).items():
        if size and len(cs) != size:
            continue
        labs = [rgb_oklab(tuple(c["rgb"])) for c in cs]
        score = sum(min(de(a, l) for l in labs) for a in alabs) / max(1, len(alabs))
        out.append((score, n, cs))
    out.sort(key=lambda x: x[0])
    return [(n, round(s, 3), [(c["name"], c["hex"]) for c in cs]) for s, n, cs in out[:top]]


# Building ------------------------------------------------------------------------------------------------------

def scale(hexc, steps=11, lmax=0.97, lmin=0.18):
    """A tonal ramp in OKLCH on the colour's hue: lightness evenly spaced, chroma peaking in the middle."""
    L0, C0, h = oklch(rgb_oklab(hex_rgb(hexc)))
    out = []
    for i in range(steps):
        L = lmax - (lmax - lmin) * i / (steps - 1)
        C = C0 * math.sin(math.pi * min(1, max(0, (L - 0.05) / 0.95))) ** 0.8
        out.append(from_oklch(L, C, h))
    return out


# Checking ------------------------------------------------------------------------------------------------------

def cliches(colours):
    """Palettes that read as defaults of templates and AI-built pages. Returns a list of findings."""
    lch = {n: oklch(rgb_oklab(hex_rgb(h))) for n, h in colours.items()}
    vals = list(lch.values())
    found = []
    cream = [v for v in vals if 0.9 <= v[0] <= 0.98 and v[1] < 0.045 and 60 <= v[2] <= 100]
    terra = [v for v in vals if 0.45 <= v[0] <= 0.7 and 0.09 <= v[1] <= 0.2 and 25 <= v[2] <= 55]
    if cream and terra:
        found.append("warm cream with a terracotta accent: the most common template palette")
    dark = [v for v in vals if v[0] < 0.22]
    acid = [v for v in vals if v[1] > 0.17 and (110 <= v[2] <= 150 or 25 <= v[2] <= 40)]
    if dark and acid:
        found.append("near-black with one acid green or vermilion pop")
    if any(v[1] > 0.12 and 270 <= v[2] <= 310 for v in vals) and any(v[1] > 0.12 and 230 <= v[2] < 270 for v in vals):
        found.append("purple-to-blue: the gradient-hero palette")
    if any(v[1] > 0.08 and 180 <= v[2] <= 220 for v in vals) and any(v[1] > 0.1 and 45 <= v[2] <= 75 for v in vals):
        found.append("teal and orange: the default cinematic grade")
    hued = [v for v in vals if v[1] > 0.02]
    if len(hued) >= 3:
        hs = sorted(v[2] for v in hued)
        gaps = [(hs[(i + 1) % len(hs)] - hs[i]) % 360 for i in range(len(hs))]
        if 360 - max(gaps) < 45 and max(v[1] for v in hued) < 0.15:
            found.append("one temperature, low chroma: every colour sits in one muddy hue family with no counterweight (add a cool or a clean colour)")
    if vals and all(v[1] < 0.006 for v in vals):
        found.append("pure greys only: neutrals with no hue bias read as unconsidered")
    return found


def check(tokens):
    colours = tokens["colours"]
    report = {"pairs": [], "large": [], "findings": []}
    for fg, bg in tokens.get("pairs", []):
        r = contrast(colours[fg], colours[bg])
        report["pairs"].append((fg, bg, round(r, 2), r >= 4.5))
    for fg, bg in tokens.get("large", []):
        r = contrast(colours[fg], colours[bg])
        report["large"].append((fg, bg, round(r, 2), r >= 3))
    lch = {n: oklch(rgb_oklab(hex_rgb(h))) for n, h in colours.items()}
    Ls = [v[0] for v in lch.values()]
    if Ls and max(Ls) - min(Ls) < 0.55:
        report["findings"].append(f"value range {max(Ls) - min(Ls):.2f} in OKLab lightness: too little light and dark to build hierarchy (aim for 0.6 or more)")
    loud = [n for n, v in lch.items() if v[1] > 0.13]
    if len(loud) > 2:
        report["findings"].append(f"{len(loud)} high-chroma colours ({', '.join(loud)}): keep one, two at most, and let the rest support")
    report["findings"] += ["cliche: " + c for c in cliches(colours)]
    report["ok"] = all(p[3] for p in report["pairs"] + report["large"]) and not any(f.startswith("cliche") for f in report["findings"])
    return report


def sheet(tokens, out):
    c = tokens["colours"]
    sw = "".join(f'<div class="sw" style="background:{h}"><span style="color:{"#000" if luminance(hex_rgb(h)) > 0.2 else "#fff"}">{n}<br>{h}</span></div>' for n, h in c.items())
    pairs = "".join(f'<div class="pair" style="background:{c[bg]};color:{c[fg]}"><b>{fg} on {bg}</b> · {contrast(c[fg], c[bg]):.1f}:1<br>The long way round, on purpose. 0123456789</div>' for fg, bg in tokens.get("pairs", []) + tokens.get("large", []))
    doc = f'<!doctype html><meta charset="utf-8"><style>body{{margin:0;font:16px/1.4 system-ui;background:#888}}.row{{display:flex;flex-wrap:wrap}}.sw{{flex:1 1 140px;height:160px;display:flex;align-items:flex-end;padding:12px;font:12px ui-monospace,monospace}}.pair{{padding:22px 28px;font-size:20px}}</style><div class="row">{sw}</div>{pairs}'
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return out


# Command line --------------------------------------------------------------------------------------------------

def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("paths", nargs="+"); e.add_argument("--k", type=int, default=8)
    w = sub.add_parser("wada"); w.add_argument("--near", required=True); w.add_argument("--size", type=int); w.add_argument("--top", type=int, default=6)
    s = sub.add_parser("scale"); s.add_argument("hex"); s.add_argument("--steps", type=int, default=11)
    c = sub.add_parser("check"); c.add_argument("tokens")
    h = sub.add_parser("sheet"); h.add_argument("tokens"); h.add_argument("--out", default="palette-sheet.html")
    a = ap.parse_args(argv)
    if a.cmd == "extract":
        for hx, share, (L, C, hue) in extract(a.paths, a.k):
            print(f"{hx}  {share:5.1%}  L {L:.2f}  C {C:.3f}  h {hue:3.0f}")
    elif a.cmd == "wada":
        for n, s_, cs in wada_near([x for x in a.near.split(",") if x], a.size, a.top):
            print(f"Combination {n} (distance {s_}): " + ", ".join(f"{name} {hx}" for name, hx in cs))
    elif a.cmd == "scale":
        print(" ".join(scale(a.hex, a.steps)))
    elif a.cmd in ("check", "sheet"):
        with open(a.tokens, encoding="utf-8") as f:
            tokens = json.load(f)
        if a.cmd == "sheet":
            print("palette: wrote", sheet(tokens, a.out))
            return 0
        r = check(tokens)
        for fg, bg, ratio, ok in r["pairs"]:
            print(f"{'pass' if ok else 'FAIL'}  {fg} on {bg}: {ratio}:1 (text, 4.5 needed)")
        for fg, bg, ratio, ok in r["large"]:
            print(f"{'pass' if ok else 'FAIL'}  {fg} on {bg}: {ratio}:1 (large text, 3 needed)")
        for f in r["findings"]:
            print("note  " + f)
        return 0 if r["ok"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
