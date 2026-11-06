#!/usr/bin/env python3
"""series_check: measures a series of images and films against a world bible and against each other.

    python3 series_check.py world/ --bible WORLD-BIBLE.md
    python3 series_check.py S01.png S02.png S03.mp4 --bible WORLD-BIBLE.md --sheet world/series-sheet.jpg
    python3 series_check.py world/ --bible WORLD-BIBLE.md --json > world/series-metrics.json

For every image (and a few frames of every film) it reports:
  palette   share of coloured pixels within a CIE76 distance of a bible colour (neutral pixels excluded)
  key       mean lightness, L* 0 to 100
  contrast  spread of lightness (standard deviation of L*)
  chroma    mean colourfulness (C*ab)
  warmth    mean b* (positive is yellower, negative bluer)
  light     mean L* of the left third minus the right third (positive: light from the left)

Two kinds of finding. A flag (palette share under the minimum, or light from the side the bible rules out)
breaks the bible, and makes the exit code 1. A look (key, contrast, chroma or warmth far from the series
median) is a frame the critic must open at full size: it may be a deliberate change of scene, or drift.
Needs ffmpeg. Python 3 standard library only.
"""
import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile

IMAGES = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
FILMS = {".mp4", ".mov", ".webm", ".m4v", ".mkv"}
WIDTH = 96
TOLERANCE = {"key": 18.0, "contrast": 12.0, "chroma": 14.0, "warmth": 14.0}
LIGHT_MIN = 4.0


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def srgb_to_lab(rgb):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def parse_bible(path):
    """Palette hexes from the '## Palette' section and the light direction from '## Light'."""
    with open(path, encoding="utf-8") as f:
        text = f.read()

    def section(name):
        m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
        return m.group(1) if m else ""
    palette = []
    for line in section("Palette").splitlines():
        if line.startswith("|"):
            palette += [h.lower() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", line)]
    light = None
    m = re.search(r"Direction:\s*(?:from (?:the )?)?(left|right|above|behind|front)", section("Light"), re.I)
    if m:
        light = m.group(1).lower()
    return {"palette": list(dict.fromkeys(palette)), "light": light}


def metrics(rgb_bytes, width, height, palette, tol=18.0):
    """Metrics for one frame of raw RGB24 pixels."""
    labs_pal = [srgb_to_lab(hex_rgb(h)) for h in palette]
    cache = {}
    Ls, Cs, Bs = [], [], []
    left, right = [], []
    coloured = on = 0
    third = max(1, width // 3)
    for i in range(0, width * height * 3 - 2, 3):
        px = (rgb_bytes[i] >> 2, rgb_bytes[i + 1] >> 2, rgb_bytes[i + 2] >> 2)
        if px not in cache:
            L, a, b = srgb_to_lab(tuple(c * 4 + 2 for c in px))
            C = (a * a + b * b) ** 0.5
            hit = None
            if not (L < 12 or L > 94 or C < 8):
                d = min((((L - p[0]) ** 2 + (a - p[1]) ** 2 + (b - p[2]) ** 2) ** 0.5 for p in labs_pal), default=1e9)
                hit = d <= tol
            cache[px] = (L, C, b, hit)
        L, C, b, hit = cache[px]
        Ls.append(L)
        Cs.append(C)
        Bs.append(b)
        x = (i // 3) % width
        if x < third:
            left.append(L)
        elif x >= width - third:
            right.append(L)
        if hit is not None:
            coloured += 1
            on += hit
    return {"palette": round(on / coloured, 3) if coloured and palette else None,
            "key": round(statistics.fmean(Ls), 1),
            "contrast": round(statistics.pstdev(Ls), 1),
            "chroma": round(statistics.fmean(Cs), 1),
            "warmth": round(statistics.fmean(Bs), 1),
            "light": round(statistics.fmean(left) - statistics.fmean(right), 1) if left and right else 0.0}


def average(ms):
    out = {}
    for k in ms[0]:
        vals = [m[k] for m in ms if m[k] is not None]
        out[k] = round(statistics.fmean(vals), 3 if k == "palette" else 1) if vals else None
    return out


def frames_of(path, samples=4):
    """Raw RGB24 frames of an image (one) or a film (several), scaled to WIDTH."""
    if not shutil.which("ffmpeg"):
        raise SystemExit("series_check: needs ffmpeg on the PATH")
    film = os.path.splitext(path)[1].lower() in FILMS
    vf = f"scale={WIDTH}:-2"
    if film:
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True).stdout.strip()
        fps = samples / max(0.5, float(dur or 1))
        vf = f"fps={fps:.4f}," + vf
    probe = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-frames:v", "1", "-f", "image2pipe",
                            "-vcodec", "ppm", "-"], capture_output=True, check=True).stdout
    w, h = (int(v) for v in probe.split(b"\n")[1].split())
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    size = w * h * 3
    return w, h, [raw[i:i + size] for i in range(0, len(raw) - size + 1, size)][:max(1, samples)]


def flag(items, bible, min_palette=0.75):
    """Add 'look' (outliers against the series median) and 'flags' (breaks the bible) to each item."""
    for k, tol in TOLERANCE.items():
        vals = [it["m"][k] for it in items]
        if len(vals) < 3:
            continue
        med = statistics.median(vals)
        for it in items:
            if abs(it["m"][k] - med) > tol:
                it["look"].append(f"{k} {it['m'][k]} against the series' {round(med, 1)}")
    for it in items:
        p = it["m"]["palette"]
        if p is not None and p < min_palette:
            it["flags"].append(f"palette {p:.0%} on the bible's colours (at least {min_palette:.0%})")
        side = it["m"]["light"]
        want = bible.get("light")
        if want == "left" and side < -LIGHT_MIN:
            it["flags"].append(f"light falls from the right ({side}); the bible says from the left")
        if want == "right" and side > LIGHT_MIN:
            it["flags"].append(f"light falls from the left ({side}); the bible says from the right")
    return items


def contact_sheet(paths, out, cols=4):
    tmp = tempfile.mkdtemp()
    try:
        for i, p in enumerate(paths):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-frames:v", "1", "-vf",
                            "scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:color=0x111111",
                            os.path.join(tmp, f"{i:03d}.png")], check=True)
        rows = (len(paths) + cols - 1) // cols
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", os.path.join(tmp, "%03d.png"), "-vf",
                        f"tile={cols}x{rows}:padding=6:margin=6:color=0x111111", "-frames:v", "1", out], check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def collect(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            for f in sorted(os.listdir(a)):
                if os.path.splitext(f)[1].lower() in IMAGES | FILMS and "sheet" not in f:
                    out.append(os.path.join(a, f))
        else:
            out.append(a)
    return out


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--bible", help="WORLD-BIBLE.md (palette and light direction)")
    ap.add_argument("--min-palette", type=float, default=0.75)
    ap.add_argument("--tolerance", type=float, default=18.0, help="CIE76 distance that counts as on palette")
    ap.add_argument("--sheet", help="write a contact sheet here, in the order measured")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    bible = parse_bible(a.bible) if a.bible else {"palette": [], "light": None}
    paths = collect(a.paths)
    if not paths:
        raise SystemExit("series_check: no images or films found")
    items = []
    for p in paths:
        w, h, frames = frames_of(p)
        items.append({"path": p, "m": average([metrics(f, w, h, bible["palette"], a.tolerance) for f in frames]),
                      "flags": [], "look": []})
    flag(items, bible, a.min_palette)
    if a.sheet:
        contact_sheet(paths, a.sheet)
    if a.json:
        print(json.dumps({"bible": bible, "items": items}, indent=2))
    else:
        print(f"Series of {len(items)} · bible palette {len(bible['palette'])} colours · light {bible['light'] or 'not set'}\n")
        print("| Item | Palette | Key | Contrast | Chroma | Warmth | Light | Breaks the bible | Look at full size |")
        print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for it in items:
            m = it["m"]
            pal = "n/a" if m["palette"] is None else f"{m['palette']:.0%}"
            print(f"| {os.path.basename(it['path'])} | {pal} | {m['key']} | {m['contrast']} | {m['chroma']} | {m['warmth']} | "
                  f"{m['light']} | {'; '.join(it['flags']) or 'none'} | {'; '.join(it['look']) or 'none'} |")
        n = sum(1 for it in items if it["flags"])
        k = sum(1 for it in items if it["look"])
        print(f"\n{n} of {len(items)} break the bible; {k} to look at." + (f" Contact sheet: {a.sheet}" if a.sheet else ""))
    return 1 if any(it["flags"] for it in items) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
