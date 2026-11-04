"""Offline checks on the crew and promo-stack locks and their installer. Run: python3 -m unittest discover plugins/fastidious/tests"""
import json
import os
import re
import sys
import tempfile
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(PLUGIN, "skills", "fastidious")
sys.path.insert(0, os.path.join(HOME, "scripts"))
import promo_stack  # noqa: E402
import crew_stack  # noqa: E402

PERMISSIVE = ("MIT", "Apache-2.0")


def skill(name):
    return open(os.path.join(PLUGIN, "skills", name, "SKILL.md")).read()


class Locks(unittest.TestCase):
    def setUp(self):
        self.promo = promo_stack.load_lock()
        self.crew = crew_stack.load_lock()

    def test_every_package_is_pinned_to_a_full_commit(self):
        for lock in (self.promo, self.crew):
            for p in lock["packages"]:
                self.assertRegex(p["commit"], r"^[0-9a-f]{40}$", p["id"])
                self.assertEqual(p["repo"].count("/"), 1, p["id"])

    def test_only_permissive_licences_are_installed(self):
        for lock in (self.promo, self.crew):
            for p in lock["packages"]:
                self.assertTrue(p["licence"].startswith(PERMISSIVE), f"{p['id']}: {p['licence']}")

    def test_installed_names_are_unique_across_both_locks_and_the_plugin(self):
        names = [s["as"] for lock in (self.promo, self.crew) for p in lock["packages"] for s in p["skills"]]
        self.assertEqual(len(names), len(set(names)))
        ours = set(os.listdir(os.path.join(PLUGIN, "skills")))
        self.assertFalse(ours & set(names), "a pinned third-party skill shares a name with a Fastidious skill")

    def test_generic_promo_names_are_prefixed(self):
        for p in self.promo["packages"]:
            if p["id"] == "elevenlabs":
                self.assertTrue(all(s["as"].startswith("elevenlabs-") and s.get("rename") for s in p["skills"]))

    def test_crew_skills_are_never_renamed(self):
        for p in self.crew["packages"]:
            self.assertFalse(any(s.get("rename") for s in p["skills"]), p["id"])

    def test_hyperframes_cli_matches_its_skills(self):
        hf = next(p for p in self.promo["packages"] if p["id"] == "hyperframes")
        self.assertEqual(hf["cli"], "hyperframes@" + hf["ref"].lstrip("v"))

    def test_showreel_director_names_the_pinned_versions(self):
        text = skill("showreel-director")
        for p in self.promo["packages"]:
            self.assertIn(p["commit"][:8], text, p["id"])
        hf = next(p for p in self.promo["packages"] if p["id"] == "hyperframes")
        self.assertIn(hf["cli"], text)

    def test_studio_conductor_routes_to_every_core_crew_package(self):
        text = skill("studio-conductor")
        for name in ("impeccable", "design-taste-frontend", "emil-design-eng", "gsap-core", "gsap-scrolltrigger"):
            self.assertIn(name, text)


class Installer(unittest.TestCase):
    def test_rename_changes_only_the_name_line(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "SKILL.md")
        open(p, "w").write("---\nname: music\ndescription: makes music; name: not this one\n---\nbody name: music\n")
        promo_stack.rename_skill(p, "elevenlabs-music")
        text = open(p).read()
        self.assertIn("name: elevenlabs-music\n", text)
        self.assertEqual(len(re.findall(r"^name:", text, re.M)), 1)
        self.assertIn("body name: music", text)

    def test_a_folder_without_a_pin_is_not_ours(self):
        d = tempfile.mkdtemp()
        self.assertFalse(promo_stack.ours(d))
        open(os.path.join(d, promo_stack.PIN), "w").write("{}")
        self.assertTrue(promo_stack.ours(d))

    def test_crew_check_fails_on_an_unpinned_copy_and_passes_on_a_pinned_one(self):
        d = tempfile.mkdtemp()
        lock = crew_stack.load_lock()

        class A:
            dir = d
        for p in lock["packages"]:
            for s in p["skills"]:
                os.makedirs(os.path.join(d, s["as"]))
                open(os.path.join(d, s["as"], "SKILL.md"), "w").write("---\nname: x\n---\n")
        with self.assertRaises(SystemExit) as e:
            crew_stack.cmd_check(A)
        self.assertEqual(e.exception.code, 1)
        for p in lock["packages"]:
            for s in p["skills"]:
                json.dump({"commit": p["commit"]}, open(os.path.join(d, s["as"], promo_stack.PIN), "w"))
        with self.assertRaises(SystemExit) as e:
            crew_stack.cmd_check(A)
        self.assertEqual(e.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
