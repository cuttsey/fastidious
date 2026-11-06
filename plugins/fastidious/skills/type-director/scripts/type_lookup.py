#!/usr/bin/env python3
"""type_lookup: finds typefaces for a brief in the curated catalogue, and checks them against Google Fonts live.

    python3 type_lookup.py --genre "old style" --voice rustic,english
    python3 type_lookup.py --category serif --max-overuse 1
    python3 type_lookup.py --family "IM Fell English" --live        # weights, styles, axes, subsets from Google
    python3 type_lookup.py --overused                              # the faces to justify before using

Ranks faces by how many of the words given appear in their genre, lineage, voice and good_for fields, then
by lowest overuse. --live asks Google's public metadata for the family (no key), falling back to the
google-font-metadata package on the npm registry, so availability and features are confirmed, not assumed.
Standard library only.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOGUE = os.path.join(os.path.dirname(HERE), "references", "typefaces.json")


def load(path=CATALOGUE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def score(face, words):
    """How many of the query words appear in the face's descriptive fields."""
    hay = " ".join(str(face.get(k, "")) for k in ("genre", "lineage", "voice", "good_for", "family")).lower()
    return sum(1 for w in words if w and re.search(r"\b" + re.escape(w.lower()), hay))


def search(cat, genre=None, voice=None, category=None, max_overuse=3, source=None):
    words = [w.strip() for w in (genre or "").split(",") + (voice or "").split(",") if w.strip()]
    out = []
    for f in cat["faces"]:
        if f["overuse"] > max_overuse:
            continue
        if category and f["category"] != category:
            continue
        if source and f["source"] != source:
            continue
        s = score(f, words) if words else 0
        if words and s == 0:
            continue
        out.append((s, f))
    out.sort(key=lambda x: (-x[0], x[1]["overuse"], x[1]["family"]))
    return [f for _, f in out]


def slug(family):
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def live(family):
    """Weights, styles, subsets and axes for a Google family, or None if it cannot be found."""
    try:
        with urllib.request.urlopen("https://fonts.google.com/metadata/fonts", timeout=15) as r:
            text = r.read().decode("utf-8")
        data = json.loads(text[text.index("{"):])
        for f in data.get("familyMetadataList", []):
            if f["family"].lower() == family.lower():
                return {"source": "fonts.google.com", "category": f.get("category"), "popularity_rank": f.get("popularity"),
                        "styles": sorted(f.get("fonts", {}).keys()), "axes": [a["tag"] for a in f.get("axes", [])],
                        "subsets": f.get("subsets"), "designers": f.get("designers")}
    except Exception:
        pass
    try:
        tmp = tempfile.mkdtemp()
        subprocess.run(["npm", "pack", "google-font-metadata", "--silent", "--pack-destination", tmp], check=True,
                       capture_output=True, timeout=180)
        tgz = [f for f in os.listdir(tmp) if f.endswith(".tgz")][0]
        subprocess.run(["tar", "xzf", tgz, "package/data/google-fonts-v2.json", "package/data/variable.json"], cwd=tmp,
                       check=True, capture_output=True)
        v2 = json.load(open(os.path.join(tmp, "package/data/google-fonts-v2.json")))
        var = json.load(open(os.path.join(tmp, "package/data/variable.json")))
        f = v2.get(slug(family))
        if f:
            return {"source": "google-font-metadata (npm)", "weights": f["weights"], "styles": f["styles"],
                    "subsets": f["subsets"], "axes": sorted(var.get(slug(family), {}).get("axes", {}).keys())}
    except Exception:
        pass
    return None


def show(f):
    flag = {0: "rare", 1: "seen", 2: "common", 3: "template default"}[f["overuse"]]
    print(f"{f['family']}  [{f['category']}, {f['source']}, overuse: {flag}]")
    print(f"  {f['genre']}. {f['lineage']}.")
    print(f"  Voice: {f['voice']}. Good for: {f['good_for'] or 'n/a'}.")
    if f.get("features"):
        print(f"  Features: {', '.join(f['features'])}.")
    if f.get("pair_with"):
        print(f"  Pairs with: {f['pair_with']}.")
    if f.get("cautions"):
        print(f"  Caution: {f['cautions']}")


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--genre")
    ap.add_argument("--voice")
    ap.add_argument("--category", choices=["serif", "sans-serif", "monospace", "display"])
    ap.add_argument("--source", choices=["google", "fontshare"])
    ap.add_argument("--max-overuse", type=int, default=2)
    ap.add_argument("--family")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--overused", action="store_true")
    ap.add_argument("--commercial", action="store_true", help="list commercial faces worth proposing to a client")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    cat = load()
    if a.commercial:
        for c in cat["commercial"]:
            print(f"{c['family']} ({c['foundry']}): {c['genre']}; {c['voice']}")
        return 0
    if a.overused:
        faces = [f for f in cat["faces"] if f["overuse"] == 3]
    elif a.family:
        faces = [f for f in cat["faces"] if f["family"].lower() == a.family.lower()]
        if not faces:
            print(f"{a.family} is not in the catalogue.")
    else:
        faces = search(cat, a.genre, a.voice, a.category, a.max_overuse, a.source)
    if a.json:
        print(json.dumps(faces, indent=1, ensure_ascii=False))
    else:
        for f in faces[:12]:
            show(f)
            print()
    if a.live and a.family:
        info = live(a.family)
        print("Live:", json.dumps(info, ensure_ascii=False) if info else "not found on Google Fonts, or offline")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
