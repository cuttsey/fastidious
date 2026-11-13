#!/usr/bin/env python3
"""precedents: searches the studied startup identities for ones that answer the same question as yours.

    python3 precedents.py --register trust
    python3 precedents.py --source name                 # ideas mined from the name
    python3 precedents.py --structure "colour kit"
    python3 precedents.py --brand heron --json

Fields: brand, url, business, register (trust, warm, expressive), idea_source (name, verb, promise, product,
reference, category), idea, mark, structure, palette, type, material, verdict. Standard library only.
"""
import argparse
import json
import os
import sys

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "precedents.json")


def load(path=DATA):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["cases"]


def search(cases, register=None, source=None, structure=None, brand=None, text=None):
    out = []
    for c in cases:
        if register and c["register"] != register:
            continue
        if source and c["idea_source"] != source:
            continue
        if structure and c["structure"] != structure:
            continue
        if brand and c["brand"].lower() != brand.lower():
            continue
        if text and text.lower() not in json.dumps(c).lower():
            continue
        out.append(c)
    return out


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--register", choices=["trust", "warm", "expressive"])
    ap.add_argument("--source", choices=["name", "verb", "promise", "product", "reference", "category"])
    ap.add_argument("--structure")
    ap.add_argument("--brand")
    ap.add_argument("--text", help="any word in the record, for example 'payments' or 'serif'")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    found = search(load(), a.register, a.source, a.structure, a.brand, a.text)
    if a.json:
        print(json.dumps(found, indent=1, ensure_ascii=False))
        return 0
    for c in found:
        print(f"{c['brand']} ({c['business']}) [{c['register']}, idea from the {c['idea_source']}]")
        print(f"  Idea: {c['idea']}. Mark: {c['mark']}.")
        print(f"  Colour: {c['structure']}; " + ", ".join(f"{k} {v}" for k, v in c["palette"].items()) + ".")
        print(f"  Type: {c['type']}. Material: {c['material']}. Verdict: {c['verdict']}.")
        print(f"  {c['url']}")
    if not found:
        print("No precedent matches; widen the search.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
