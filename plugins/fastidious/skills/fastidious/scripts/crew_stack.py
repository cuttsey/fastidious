#!/usr/bin/env python3
"""crew_stack: install and check the third-party skills Fastidious builds on (Impeccable, Taste, Emil Kowalski's
skills, GreenSock's GSAP skills and Anatomy), each at the exact commit in crew.lock.json.

    python3 scripts/crew_stack.py install [--dir ~/.claude/skills] [--force]
    python3 scripts/crew_stack.py check   [--dir ~/.claude/skills]
    python3 scripts/crew_stack.py names                                 one installed skill name per line
    python3 scripts/crew_stack.py outdated                              lists newer commits; changes nothing

It shares its installer with promo_stack.py: a .fastidious-pin.json is written beside each SKILL.md, and a folder
without one belongs to you and is never overwritten unless you pass --force. Standard library only; needs git.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promo_stack as base  # noqa: E402

LOCK = os.path.join(HERE, "..", "crew.lock.json")


def load_lock():
    return base.load_lock(LOCK)


def cmd_install(args):
    base.LOCK = LOCK
    args.with_ = None
    base.cmd_install(args)
    print("\nNext: python3 scripts/crew_stack.py check")


def cmd_check(args):
    lock = load_lock()
    problems = []
    for pkg in lock["packages"]:
        for s in pkg["skills"]:
            dst = os.path.join(args.dir, s["as"])
            if not os.path.exists(os.path.join(dst, "SKILL.md")):
                problems.append(f"{s['as']} ({pkg['id']}): not installed")
            elif not base.ours(dst):
                problems.append(f"{s['as']} ({pkg['id']}): present but not installed by Fastidious, so its version is unknown "
                                "(an older bundled copy, perhaps); run install --force to replace it with the pinned one")
            else:
                with open(os.path.join(dst, base.PIN)) as f:
                    pin = json.load(f)
                if pin.get("commit") != pkg["commit"]:
                    problems.append(f"{s['as']}: pinned at {pin.get('commit', '?')[:12]}, lock says {pkg['commit'][:12]}; run install")
    if not base.shutil.which("git"):
        problems.append("git is not on PATH")
    for p in problems:
        print(f"FAIL: {p}")
    print("crew: " + ("ready" if not problems else f"{len(problems)} problem(s)"))
    sys.exit(1 if problems else 0)


def cmd_names(args):
    for pkg in load_lock()["packages"]:
        for s in pkg["skills"]:
            print(s["as"])


def cmd_outdated(args):
    base.LOCK = LOCK
    base.cmd_outdated(args, doc="CREW.md")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    default = os.path.expanduser(os.environ.get("CLAUDE_SKILLS_DIR", "~/.claude/skills"))
    i = sub.add_parser("install"); i.add_argument("--dir", default=default); i.add_argument("--force", action="store_true")
    c = sub.add_parser("check"); c.add_argument("--dir", default=default)
    sub.add_parser("names")
    sub.add_parser("outdated")
    a = p.parse_args()
    {"install": cmd_install, "check": cmd_check, "names": cmd_names, "outdated": cmd_outdated}[a.cmd](a)


if __name__ == "__main__":
    main()
