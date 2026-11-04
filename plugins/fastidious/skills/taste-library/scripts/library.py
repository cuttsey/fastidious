#!/usr/bin/env python3
"""library: the designer's own reference library, kept across projects.

    python3 scripts/library.py init                 create the personal library from the template
    python3 scripts/library.py path                 print where the personal library lives
    python3 scripts/library.py check [FILE]         check a REFERENCES.md (default: the personal library)
    python3 scripts/library.py list [--active]      one line per reference: ID, teaches, source

The personal library lives in ~/.claude/fastidious/ (REFERENCES.md, with images in references/), or wherever
FASTIDIOUS_LIBRARY points. Each project keeps its own REFERENCES.md, which taste-library fills from this one.
Standard library only.
"""
import argparse
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "REFERENCES.md")
COLS = ["ID", "Source", "URL", "Teaches", "Pattern", "Fit", "Borrow", "Reject", "From", "Status"]
TEACHES = {"look", "pattern", "motion", "type", "structure", "thinking"}


def home():
    return os.path.expanduser(os.environ.get("FASTIDIOUS_LIBRARY", "~/.claude/fastidious"))


def library_file():
    return os.path.join(home(), "REFERENCES.md")


def parse(path):
    """Rows of the references table as dicts, plus the 'Next free ID' number (or None)."""
    rows, header, nxt = [], None, None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r"^Next free ID:\s*R-(\d+)", line)
        if m:
            nxt = int(m.group(1))
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        row = dict(zip(header, cells + [""] * (len(header) - len(cells))))
        row.setdefault("Status", "active")
        rows.append(row)
    return rows, nxt


def check(path):
    rows, nxt = parse(path)
    base = os.path.dirname(os.path.abspath(path))
    problems, seen = [], set()
    for r in rows:
        rid = r.get("ID", "")
        if not re.fullmatch(r"R-\d{3,}", rid):
            problems.append(f"{rid or '(no ID)'}: IDs look like R-001")
            continue
        if rid in seen:
            problems.append(f"{rid}: used twice; a retired ID is never reused")
        seen.add(rid)
        if (r.get("Status") or "active").lower() == "retired":
            continue
        if not r.get("Borrow") or not r.get("Reject"):
            problems.append(f"{rid}: needs both a Borrow and a Reject note, or it is only a link")
        if r.get("Teaches") and r["Teaches"].lower() not in TEACHES:
            problems.append(f"{rid}: Teaches should be one of {', '.join(sorted(TEACHES))}")
        if not r.get("URL"):
            folders = [os.path.join(base, d) for d in ("references", ".references")]
            found = any(n.startswith(rid + ".") for d in folders if os.path.isdir(d) for n in os.listdir(d))
            if not found:
                problems.append(f"{rid}: no URL and no image named {rid}.* in references/")
    ids = [int(r["ID"][2:]) for r in rows if re.fullmatch(r"R-\d+", r.get("ID", ""))]
    if ids and (nxt is None or nxt <= max(ids)):
        problems.append(f"'Next free ID' should be R-{max(ids) + 1:03d}")
    return rows, problems


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init"); sub.add_parser("path")
    c = sub.add_parser("check"); c.add_argument("file", nargs="?")
    l = sub.add_parser("list"); l.add_argument("--active", action="store_true")
    a = p.parse_args()
    if a.cmd == "path":
        print(library_file())
    elif a.cmd == "init":
        os.makedirs(os.path.join(home(), "references"), exist_ok=True)
        if os.path.exists(library_file()):
            print(f"Already there, left untouched: {library_file()}")
        else:
            shutil.copy(TEMPLATE, library_file())
            print(f"Created {library_file()}; put images in {os.path.join(home(), 'references')}")
    elif a.cmd == "check":
        path = a.file or library_file()
        if not os.path.exists(path):
            sys.exit(f"No library at {path}. Run: python3 scripts/library.py init")
        rows, problems = check(path)
        for x in problems:
            print("FIX:", x)
        print(f"{path}: {len(rows)} references, " + ("ready" if not problems else f"{len(problems)} to fix"))
        sys.exit(1 if problems else 0)
    elif a.cmd == "list":
        if not os.path.exists(library_file()):
            sys.exit(f"No library at {library_file()}. Run: python3 scripts/library.py init")
        for r in parse(library_file())[0]:
            if a.active and (r.get("Status") or "active").lower() == "retired":
                continue
            print(f"{r['ID']}  {r.get('Teaches', ''):10} {r.get('Source', '')}  {r.get('URL', '')}")


if __name__ == "__main__":
    main()
