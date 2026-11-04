#!/usr/bin/env python3
"""promo_stack: install, check and smoke-test the third-party skills Fastidious uses for promotional film.

    python3 scripts/promo_stack.py install [--dir ~/.claude/skills] [--with watch] [--force]
    python3 scripts/promo_stack.py check   [--dir ~/.claude/skills]
    python3 scripts/promo_stack.py smoke   [--dir ~/.claude/skills]   renders a 3-second film end to end
    python3 scripts/promo_stack.py outdated                            lists newer commits; changes nothing

Every package is fetched at the exact commit in promo-stack.lock.json, verified, and copied into the skills
directory with a .fastidious-pin.json beside its SKILL.md. A folder without that file belongs to you and is never
overwritten unless you pass --force. Nothing here updates itself; moving a pin is a deliberate edit to the lock.
Standard library only; needs git, and node 22+, ffmpeg and python3 for the skills themselves.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(HERE, "..", "promo-stack.lock.json")
PIN = ".fastidious-pin.json"
SKIP = {".git", ".github", "node_modules"}


def load_lock(path=None):
    with open(path or LOCK) as f:
        return json.load(f)


def run(args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw)


def wanted(lock, extra):
    groups = {"core"} | set(extra or [])
    return [p for p in lock["packages"] if p["group"] in groups]


def fetch(pkg, workdir):
    """Fetch exactly one commit, and only the paths the lock names."""
    repo = os.path.join(workdir, pkg["id"])
    os.makedirs(repo)
    g = lambda *a: run(["git", "-C", repo, *a])
    g("init", "-q")
    g("remote", "add", "origin", f"https://github.com/{pkg['repo']}")
    paths = sorted({s["src"] for s in pkg["skills"]})
    if "." not in paths:
        g("sparse-checkout", "set", "--no-cone", *[p.rstrip("/") + "/" for p in paths])
    env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
    run(["git", "-C", repo, "fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", pkg["commit"]], env=env)
    run(["git", "-C", repo, "checkout", "-q", "FETCH_HEAD"], env=env)
    head = g("rev-parse", "HEAD").stdout.strip()
    if head != pkg["commit"]:
        raise SystemExit(f"{pkg['id']}: fetched {head}, expected {pkg['commit']}. Refusing to install.")
    return repo


def rename_skill(skill_md, new_name):
    """Prefix a generic skill name (music, sound-effects) so it cannot collide with another publisher's."""
    with open(skill_md) as f:
        text = f.read()
    text, n = re.subn(r"^name:\s*.+$", f"name: {new_name}", text, count=1, flags=re.M)
    if not n:
        raise SystemExit(f"{skill_md} has no name field to rename.")
    with open(skill_md, "w") as f:
        f.write(text)


def ours(path):
    return os.path.exists(os.path.join(path, PIN))


def cmd_install(args):
    lock = load_lock()
    os.makedirs(args.dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as work:
        for pkg in wanted(lock, args.with_):
            print(f"{pkg['id']}: {pkg['repo']} @ {pkg['commit'][:12]} ({pkg['ref']})")
            repo = fetch(pkg, work)
            for s in pkg["skills"]:
                src = os.path.normpath(os.path.join(repo, s["src"]))
                dst = os.path.join(args.dir, s["as"])
                if not os.path.exists(os.path.join(src, "SKILL.md")):
                    raise SystemExit(f"{pkg['id']}: {s['src']}/SKILL.md is missing at this commit.")
                if os.path.exists(dst) and not ours(dst) and not args.force:
                    print(f"  skip {s['as']}: a skill of that name already exists and is not managed by Fastidious (use --force)")
                    continue
                tmp = dst + ".installing"
                shutil.rmtree(tmp, ignore_errors=True)
                shutil.copytree(src, tmp, ignore=lambda d, names: [n for n in names if n in SKIP])
                if s.get("rename"):
                    rename_skill(os.path.join(tmp, "SKILL.md"), s["as"])
                with open(os.path.join(tmp, PIN), "w") as f:
                    json.dump({"package": pkg["id"], "repo": pkg["repo"], "commit": pkg["commit"], "ref": pkg["ref"],
                               "src": s["src"], "licence": pkg["licence"], "locked": lock["locked"]}, f, indent=2)
                shutil.rmtree(dst, ignore_errors=True)
                os.replace(tmp, dst)
                print(f"  installed {s['as']}")
    hf = next((p for p in lock["packages"] if p["id"] == "hyperframes"), None)
    if hf:
        print("\nNext: python3 scripts/promo_stack.py check, then smoke. Keep pinned skills pinned with:\n"
              "  export HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1\n"
              "Optional: npx " + hf["cli"] + " telemetry disable")


def _version(cmd, pattern):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True).stdout + subprocess.run(cmd, capture_output=True, text=True).stderr
    except FileNotFoundError:
        return None
    m = re.search(pattern, out)
    return m.group(1) if m else None


def cmd_check(args):
    lock = load_lock()
    problems, notes = [], []
    node = _version(["node", "-v"], r"v(\d+)")
    if not node or int(node) < 22:
        problems.append("Node 22 or later is required (HyperFrames, motionmaxxing)")
    for tool in ("git", "ffmpeg", "ffprobe", "python3"):
        if not shutil.which(tool):
            problems.append(f"{tool} is not on PATH")
    chrome = os.environ.get("CHROME_PATH") or next((shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
    if not chrome:
        notes.append("No Chrome on PATH: HyperFrames will fetch its own with `npx hyperframes browser ensure`; motionmaxxing needs CHROME_PATH")
    for pkg in lock["packages"]:
        installed = []
        for s in pkg["skills"]:
            dst = os.path.join(args.dir, s["as"])
            if not os.path.exists(dst):
                continue
            installed.append(s["as"])
            if not ours(dst):
                problems.append(f"{s['as']}: present but not installed by Fastidious, so its version is unknown")
                continue
            with open(os.path.join(dst, PIN)) as f:
                pin = json.load(f)
            if pin["commit"] != pkg["commit"]:
                problems.append(f"{s['as']}: pinned at {pin['commit'][:12]}, lock says {pkg['commit'][:12]}; run install")
        missing = [s["as"] for s in pkg["skills"] if s["as"] not in installed]
        if missing and pkg["group"] == "core":
            problems.append(f"{pkg['id']}: not installed ({', '.join(missing)})")
        elif missing:
            notes.append(f"{pkg['id']} (optional) not installed")
        for var in pkg.get("needs_env", []):
            if not os.environ.get(var):
                notes.append(f"{var} is not set: {pkg['id']} cannot make sound; films fall back to the local library")
    for k in ("HYPERFRAMES_SKIP_SKILLS", "HYPERFRAMES_NO_UPDATE_CHECK"):
        if os.environ.get(k) != "1":
            notes.append(f"{k}=1 is not set, so the HyperFrames CLI may suggest or install newer skills than the pin")
    for n in notes:
        print(f"note: {n}")
    for p in problems:
        print(f"FAIL: {p}")
    print("promo stack: " + ("ready" if not problems else f"{len(problems)} problem(s)"))
    sys.exit(1 if problems else 0)


def cmd_smoke(args):
    """A 3-second HyperFrames film, rendered with the pinned CLI, then motionmaxxing's look.py on the result."""
    lock = load_lock()
    cli = next(p for p in lock["packages"] if p["id"] == "hyperframes")["cli"]
    look = os.path.join(args.dir, "motionmaxxing", "scripts", "look.py")
    env = dict(os.environ, HYPERFRAMES_SKIP_SKILLS="1", HYPERFRAMES_NO_UPDATE_CHECK="1")
    if os.environ.get("CHROME_PATH") and not os.environ.get("HYPERFRAMES_BROWSER_PATH"):
        env["HYPERFRAMES_BROWSER_PATH"] = os.environ["CHROME_PATH"]  # one Chrome for HyperFrames and motionmaxxing
    with tempfile.TemporaryDirectory() as work:
        proj = os.path.join(work, "smoke")
        os.makedirs(proj)
        # GSAP is copied in from motionmaxxing's vendored runtime: renders must never fetch from a CDN.
        gsap = next((os.path.join(r, f) for r, _, fs in os.walk(os.path.join(args.dir, "motionmaxxing", "runtime"))
                     for f in fs if f == "gsap.min.js"), None)
        if not gsap:
            raise SystemExit("smoke: motionmaxxing's vendored gsap.min.js is missing; run install first.")
        os.makedirs(os.path.join(proj, "assets"))
        shutil.copy(gsap, os.path.join(proj, "assets", "gsap.min.js"))
        # The composition follows the HyperFrames contract: root id "main", one paused timeline registered on
        # window.__timelines, and the tween on a child of the timed .clip, never on the clip itself.
        # A .clip with no size renders nothing, so the lane fills the frame.
        html = ('<!doctype html><html><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script>'
                '<style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#0E1454}#root{width:100%;height:100%;position:relative}'
                '#lane{position:absolute;inset:0}#bar{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#1F4BFF}</style></head>'
                '<body><div id="root" data-composition-id="main" data-start="0" data-duration="3" data-width="1920" data-height="1080">'
                '<div id="lane" class="clip" data-layout-allow-overflow data-start="0" data-duration="3" data-track-index="0"><div id="bar"></div></div></div>'
                '<script>const tl=gsap.timeline({paused:true});tl.fromTo("#bar",{x:-1920},{x:0,duration:3,ease:"none"},0);'
                'window.__timelines["main"]=tl;tl.seek(0);</script></body></html>')
        with open(os.path.join(proj, "index.html"), "w") as f:
            f.write(html)
        out = os.path.join(work, "smoke.mp4")
        print(f"rendering with npx {cli} ...")
        r = subprocess.run(["npx", "-y", cli, "render", "--quality", "draft", "-o", out], cwd=proj, env=env, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            print(r.stdout[-1500:], r.stderr[-1500:])
            raise SystemExit("smoke: HyperFrames render failed; see the output above, then `npx " + cli + " doctor`.")
        print("rendered", out)
        failed = []
        r = subprocess.run([sys.executable, look, out, "--out", os.path.join(work, "look"), "--expect", "3"], capture_output=True, text=True)
        gates = os.path.join(work, "look", "gates.json")
        if not os.path.exists(gates):
            failed.append("look.py produced no gates.json: " + (r.stderr or r.stdout)[-300:])
        else:
            with open(gates) as f:
                for g in json.load(f)["gates"]:
                    print(f"  look.py {g['id']}: {g['status']}")
                    if g["id"] in ("G0", "G2") and g["status"] == "FAIL":
                        failed.append(f"look.py {g['id']}: {g['detail']}")
        lint = os.path.join(args.dir, "motionmaxxing", "scripts", "lint.mjs")
        # motionmaxxing's page-chrome gate, run on a HyperFrames composition. On Linux as root, Chrome needs
        # --no-sandbox: point CHROME_PATH at a small wrapper script that adds it.
        r = subprocess.run(["node", lint, os.path.join(proj, "index.html"), "--duration", "3"], capture_output=True, text=True, env=env)
        print("  lint.mjs:", (r.stdout.strip().splitlines() or [r.stderr.strip()[:200] or "(no output)"])[-1])
        if r.returncode != 0:
            failed.append("lint.mjs could not run or failed; check CHROME_PATH")
        if args.keep:
            shutil.copy(out, args.keep)
            print("kept", args.keep)
        if failed:
            raise SystemExit("smoke: FAILED\n- " + "\n- ".join(failed))
    print("smoke: passed (pinned HyperFrames rendered; motionmaxxing's look.py and lint.mjs ran on the result)")


def cmd_outdated(args, doc="PROMO-STACK.md"):
    lock = load_lock()
    for pkg in lock["packages"]:
        r = subprocess.run(["git", "ls-remote", f"https://github.com/{pkg['repo']}", "HEAD"], capture_output=True, text=True)
        head = (r.stdout.split() or ["?"])[0]
        state = "pinned commit is HEAD" if head == pkg["commit"] else f"HEAD is now {head[:12]} (pinned {pkg['commit'][:12]})"
        print(f"{pkg['id']:22} {state}")
    print(f"Nothing was changed. To move a pin, follow 'Moving a pin' in {doc}.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    default = os.path.expanduser("~/.claude/skills")
    i = sub.add_parser("install"); i.add_argument("--dir", default=default); i.add_argument("--with", dest="with_", action="append", choices=["watch"]); i.add_argument("--force", action="store_true")
    c = sub.add_parser("check"); c.add_argument("--dir", default=default)
    s = sub.add_parser("smoke"); s.add_argument("--dir", default=default); s.add_argument("--keep")
    sub.add_parser("outdated")
    a = p.parse_args()
    {"install": cmd_install, "check": cmd_check, "smoke": cmd_smoke, "outdated": cmd_outdated}[a.cmd](a)


if __name__ == "__main__":
    main()
