#!/usr/bin/env python3
"""copy_lint: checks copy against the Fastidious house style and the copy director's rules.

    python3 copy_lint.py COPY-DECK.md            # lint the Line column of a copy deck
    python3 copy_lint.py page.html notes.md      # lint the visible text of any page or document
    python3 copy_lint.py --json COPY-DECK.md     # machine-readable report

Fails (exit code 1) on em dashes, the "not X, it's Y" shape and words from the cliche list in
references/devices.md. Warns on sentences over 25 words, display lines over eight words, Title Case
headings, exclamation marks and body text with a Flesch reading ease below 50. Standard library only.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEVICES = os.path.join(os.path.dirname(HERE), "references", "devices.md")

SHAPES = [
    re.compile(r"\b(?:it|this|that|they|we|he|she)(?:'s| is| are| was|'re)? ?(?:not|n't|isn't|aren't|wasn't)\b(?: just| only| simply| merely)?[^.;:!?]{1,60}[,;] ?(?:it|this|that|they|we)(?:'s| is| are|'re)\b", re.I),
    re.compile(r"\b(?:isn't|aren't|wasn't|is not|are not|was not) (?:just|only|simply|merely)\b[^.;:!?]{1,60}[,;]? ?(?:it|this|that|they|but)\b", re.I),
    re.compile(r"\bnot (?:just|only|simply|merely)\b[^.;:!?]{1,60}\bbut\b", re.I),
    re.compile(r"\bmore than (?:just )?(?:a|an)\b[^.;:!?]{1,40}[,;] ?(?:it|this)(?:'s| is)\b", re.I),
]
DASHES = re.compile("[—]|(?<=\\w) – (?=\\w)|(?<=\\w) -- (?=\\w)")


def cliches(path=DEVICES):
    """(fail_patterns, warn_patterns) from the cliche list in devices.md, so the list lives in one place."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## The cli[cç]h[eé] list\s*\n(.*?)(?=^## )", text, re.S | re.M)
    if not m:
        raise SystemExit("copy_lint: could not find the cliche list in devices.md")
    body = [ln for ln in m.group(1).splitlines() if ln.strip() and not ln.startswith(("The ", "Each "))]
    items = [w.strip() for w in " ".join(body).split(",") if w.strip()]
    fail, warn = [], []
    for item in items:
        note = re.search(r"\(([^)]*)\)", item)
        word = re.sub(r"\s*\([^)]*\)", "", item).strip()
        if not word:
            continue
        if note and "verb" in note.group(1):
            fail.append((item, re.compile(rf"\b(?:to|we|you|they|can|will|and|helps?) {re.escape(word)}\b", re.I)))
        elif note:
            warn.append((item, re.compile(rf"\b{re.escape(word)}\b", re.I)))
        else:
            fail.append((item, re.compile(rf"\b{re.escape(word)}\b", re.I)))
    return fail, warn


def visible_text(raw, ext):
    """Return [(key, text, kind)] where kind is 'display' or 'body'."""
    if ext in (".html", ".htm"):
        raw = re.sub(r"<(script|style|svg|noscript)[\s\S]*?</\1>", " ", raw, flags=re.I)
        out = []
        for tag, inner in re.findall(r"<(h[1-6]|p|li|button|a|label|figcaption|td|th|blockquote|dt|dd)\b[^>]*>([\s\S]*?)</\1>", raw, re.I):
            inner = re.sub(r"<br\s*/?>|</(?:div|p|li)>", " ", inner, flags=re.I)
            inner = re.sub(r"</span>\s*(?=<span[^>]*class=\"[^\"]*\bln\b)", " ", inner)  # one set line per span
            t = html.unescape(re.sub(r"<[^>]+>", "", inner))  # inline tags join letters split for animation
            t = re.sub(r"\s+", " ", t).strip()
            if t:
                out.append((tag.lower(), t, "display" if tag.lower().startswith("h") else "body"))
        return out
    lines = raw.splitlines()
    # A copy deck: lint only the Line column of tables that have one.
    out, col, in_lint = [], None, False
    for ln in lines:
        if ln.startswith("## "):
            in_lint = ln.strip().lower() == "## lint"
            col = None
            continue
        if in_lint:
            continue
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if col is None and "Line" in cells:
                col = (cells.index("Key") if "Key" in cells else 0, cells.index("Line"))
                continue
            if col and not set(cells[0]) <= set("-: "):
                key, text = cells[col[0]], cells[col[1]] if len(cells) > col[1] else ""
                if text and not (text.startswith("<") and text.endswith(">")):
                    kind = "display" if re.search(r"(^|\.)(h\d?|spine|sub|close|claim|cta|button|q)$", key) else "body"
                    out.append((key, text.replace(" / ", " "), kind))
            continue
        if col is not None:
            continue
    if out:
        return out
    # Any other text: headings are display, everything else is body.
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if not s or s.startswith(("```", "|", "<!--", "---")):
            continue
        h = re.match(r"^#{1,6}\s+(.*)", s)
        if h:
            out.append((f"line {i}", h.group(1), "display"))
        else:
            out.append((f"line {i}", re.sub(r"^[-*>\d.]+\s+", "", s), "body"))
    return out


def strip_markup(t):
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"https?://\S+", " ", t)
    return re.sub(r"[*_]{1,2}", "", t)


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if re.search(r"[A-Za-z]", s)]


def words(t):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", t)


def syllables(w):
    w = w.lower().strip("'’")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def flesch(text):
    ss = sentences(text)
    ws = words(text)
    if len(ws) < 30 or not ss:
        return None
    syl = sum(syllables(w) for w in ws)
    return round(206.835 - 1.015 * (len(ws) / len(ss)) - 84.6 * (syl / len(ws)), 1)


def title_case(t):
    ws = [w for w in words(t) if w.isalpha()]
    if len(ws) < 3:
        return False
    rest = [w for w in ws[1:] if len(w) > 3]
    caps = [w for w in rest if w[0].isupper() and not w.isupper()]
    return len(rest) >= 2 and len(caps) >= max(2, len(rest) * 0.6)


def lint(items, fail_words, warn_words):
    fails, warns = [], []
    body = []
    for key, raw, kind in items:
        t = strip_markup(raw)
        if DASHES.search(raw):
            fails.append((key, "em dash: use a colon, comma or full stop", raw))
        quoted = re.sub(r"[\"“][^\"”]*[\"”]", " ", t)  # quoting a phrase is not using it
        for rx in SHAPES:
            m = rx.search(quoted)
            if m:
                fails.append((key, f"the \"not X, it's Y\" shape: \"{m.group(0)}\"", raw))
                break
        for name, rx in fail_words:
            if rx.search(quoted):
                fails.append((key, f"cliche: {name}", raw))
        for name, rx in warn_words:
            if rx.search(quoted):
                warns.append((key, f"check the use of: {name}", raw))
        if "!" in t:
            warns.append((key, "exclamation mark", raw))
        for s in sentences(t):
            n = len(words(s))
            if n > 25:
                warns.append((key, f"sentence of {n} words (25 at most)", s))
        if kind == "display":
            n = len(words(t))
            if n > 8 and not key.endswith((".a", ".sub")):
                warns.append((key, f"display line of {n} words (8 at most)", raw))
            if title_case(t):
                warns.append((key, "Title Case: use sentence case", raw))
        else:
            body.append(t)
    score = flesch(" ".join(body))
    if score is not None and score < 50:
        warns.append(("body", f"Flesch reading ease {score} (aim for 50 or more)", ""))
    return fails, warns, score


def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    fail_words, warn_words = cliches()
    report, bad = {}, False
    for p in paths:
        with open(p, encoding="utf-8") as f:
            raw = f.read()
        items = visible_text(raw, os.path.splitext(p)[1].lower())
        f, w, score = lint(items, fail_words, warn_words)
        bad = bad or bool(f)
        report[p] = {"lines": len(items), "fails": f, "warnings": w, "flesch": score}
    if as_json:
        print(json.dumps({p: {**r, "fails": [dict(zip(("key", "rule", "text"), x)) for x in r["fails"]],
                              "warnings": [dict(zip(("key", "rule", "text"), x)) for x in r["warnings"]]}
                          for p, r in report.items()}, indent=2, ensure_ascii=False))
    else:
        for p, r in report.items():
            print(f"{p}: {r['lines']} lines, {len(r['fails'])} failures, {len(r['warnings'])} warnings"
                  + (f", Flesch {r['flesch']}" if r["flesch"] is not None else ""))
            for key, rule, text in r["fails"]:
                print(f"  FAIL {key}: {rule}" + (f"\n       {text[:120]}" if text else ""))
            for key, rule, text in r["warnings"]:
                print(f"  WARN {key}: {rule}" + (f"\n       {text[:120]}" if text else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
