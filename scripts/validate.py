#!/usr/bin/env python3
"""validate: offline checks on the whole repository. Exit code 1 on any failure.

    python3 scripts/validate.py

Checks the marketplace and plugin manifests, every skill's frontmatter, that the README's roster names every
skill (ours and pinned), that no credential or retired name has crept in, and that the house style holds in
the repository's own documents.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []


def fail(msg):
    fails.append(msg)


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        k = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if k:
            out[k.group(1)] = k.group(2).strip().strip('"')
    return out


# Manifests
market = json.loads(read(".claude-plugin", "marketplace.json"))
for key in ("name", "owner", "plugins"):
    if key not in market:
        fail(f"marketplace.json: missing {key}")
plugins = {}
for entry in market["plugins"]:
    src = os.path.normpath(os.path.join(ROOT, entry["source"]))
    manifest = os.path.join(src, ".claude-plugin", "plugin.json")
    if not os.path.exists(manifest):
        fail(f"{entry['name']}: no plugin.json at {entry['source']}")
        continue
    pj = json.load(open(manifest))
    if pj["name"] != entry["name"]:
        fail(f"{entry['name']}: plugin.json name is {pj['name']}")
    if pj.get("version") != entry.get("version"):
        fail(f"{entry['name']}: version {pj.get('version')} in plugin.json, {entry.get('version')} in marketplace.json")
    if pj.get("license") != "MIT":
        fail(f"{entry['name']}: plugin.json licence should be MIT")
    plugins[entry["name"]] = src

# Skills
ours = []
for name, src in plugins.items():
    sk = os.path.join(src, "skills")
    for d in sorted(os.listdir(sk)):
        p = os.path.join(sk, d, "SKILL.md")
        if not os.path.isfile(p):
            fail(f"{name}/{d}: no SKILL.md")
            continue
        fm = frontmatter(open(p, encoding="utf-8").read())
        if not fm:
            fail(f"{name}/{d}: SKILL.md has no frontmatter")
            continue
        if fm.get("name") != d:
            fail(f"{name}/{d}: frontmatter name is {fm.get('name')!r}")
        desc = fm.get("description", "")
        if not desc or desc == ">-":
            # folded descriptions are fine; only an absent field fails
            if "description" not in fm:
                fail(f"{name}/{d}: no description")
        if len(desc) > 1024:
            fail(f"{name}/{d}: description is {len(desc)} characters (limit 1,024)")
        ours.append(d)

# Locks and roster
home = os.path.join(plugins["fastidious"], "skills", "fastidious")
pinned = []
for lock in ("crew.lock.json", "promo-stack.lock.json"):
    data = json.load(open(os.path.join(home, lock)))
    for pkg in data["packages"]:
        if not re.fullmatch(r"[0-9a-f]{40}", pkg["commit"]):
            fail(f"{lock}: {pkg['id']} is not pinned to a full commit")
        if not pkg["licence"].startswith(("MIT", "Apache-2.0")):
            fail(f"{lock}: {pkg['id']} has a non-permissive licence")
        pinned += [(lock, s["as"]) for s in pkg["skills"]]
crew = [n for lock, n in pinned if lock == "crew.lock.json"]
readme = read("README.md")
for n in ours + crew:
    if f"`{n}`" not in readme:
        fail(f"README.md does not list `{n}`")
count = len(os.listdir(os.path.join(plugins["fastidious"], "skills")))
for doc in ("README.md", os.path.join("plugins", "fastidious", ".claude-plugin", "plugin.json"),
            os.path.join(".claude-plugin", "marketplace.json"), os.path.join(home, "CREW.md")):
    text = read(doc)
    for claim in re.findall(r"\b(\d+) (?:design )?skills\b", text):
        if int(claim) not in (count, len(crew), len(os.listdir(os.path.join(plugins["fastidious-motion"], "skills")))):
            fail(f"{os.path.relpath(doc, ROOT) if os.path.isabs(doc) else doc}: claims {claim} skills; the plugin has {count}, the crew {len(crew)}")
if len(set(ours) & set(crew)):
    fail(f"pinned skills share names with ours: {set(ours) & set(crew)}")

# Whole-tree scans
SECRET = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|sk_[A-Za-z0-9]{24,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|xox[bp]-[A-Za-z0-9-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
RETIRED = re.compile(r"(?<![A-Za-z])[Ww]right(?![A-Za-z])")
TEXT = (".md", ".json", ".py", ".js", ".mjs", ".sh", ".yml", ".yaml", ".html", ".txt", ".toml")
for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
    for f in files:
        p = os.path.join(dirpath, f)
        rel = os.path.relpath(p, ROOT)
        if f in (".env",) or f.endswith((".key", ".pem")):
            fail(f"{rel}: credential file in the tree")
        if not f.endswith(TEXT) or rel == os.path.join("scripts", "validate.py"):
            continue
        text = open(p, encoding="utf-8", errors="replace").read()
        if SECRET.search(text):
            fail(f"{rel}: looks like it contains a credential")
        if RETIRED.search(text):
            fail(f"{rel}: uses a retired name")

# The copy lint on the repository's own front pages: Fastidious holds its own words to the bar it sets
sys.path.insert(0, os.path.join(plugins["fastidious"], "skills", "copy-director", "scripts"))
import copy_lint  # noqa: E402
_fw, _ww = copy_lint.cliches()
for doc in ("README.md", "PRFAQ.md"):
    items = copy_lint.visible_text(read(doc), ".md")
    for key, rule, text in copy_lint.lint(items, _fw, _ww)[0]:
        fail(f"{doc} {key}: {rule}")

# House style in the repository's own documents
for doc in ("README.md", "PRFAQ.md", "NOTICE.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md",
            os.path.join("plugins", "fastidious", "skills", "fastidious", "CREW.md")):
    text = read(doc)
    if "—" in text:
        fail(f"{doc}: contains an em dash")
    for h in re.findall(r"^#{2,6} (.+)$", text, re.M):
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", h)
        caps = [w for w in words[1:] if w[0].isupper() and not w.isupper()]
        allowed = {"Fastidious", "Claude", "Code", "GitHub", "FAQ", "FAQs", "Rude", "WCAG", "Seedance", "Kling", "OpenAI", "ElevenLabs", "HyperFrames", "Changelog"}
        if [w for w in caps if w not in allowed]:
            fail(f"{doc}: heading not in sentence case: {h!r}")

for f in fails:
    print("FAIL:", f)
print(f"validate: {len(ours)} skills, {len(crew)} crew, {len(pinned) - len(crew)} film stack; " + ("passed" if not fails else f"{len(fails)} problem(s)"))
sys.exit(1 if fails else 0)
