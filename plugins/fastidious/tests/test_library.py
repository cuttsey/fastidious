"""Offline checks on taste-library's personal library script."""
import os
import subprocess
import sys
import tempfile
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(PLUGIN, "skills", "taste-library", "scripts")
sys.path.insert(0, SCRIPTS)
import library  # noqa: E402

HEAD = "| ID | Source | URL | Teaches | Pattern | Fit | Borrow | Reject | From | Status |\n|----|----|----|----|----|----|----|----|----|----|\n"


def write(d, rows, nxt):
    p = os.path.join(d, "REFERENCES.md")
    open(p, "w").write("# References\n\n" + HEAD + "".join(rows) + f"\nNext free ID: {nxt}\n")
    return p


class Library(unittest.TestCase):
    def test_template_is_a_valid_empty_library(self):
        rows, problems = library.check(library.TEMPLATE)
        self.assertEqual(rows, [])
        self.assertEqual(problems, [])

    def test_a_good_library_passes(self):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "references"))
        open(os.path.join(d, "references", "R-002.png"), "wb").write(b"x")
        p = write(d, ["| R-001 | Godly | https://godly.website | look | hero | aspirational | One-line hero copy | Its dark default | own | active |\n",
                      "| R-002 | Railway poster | | type | typography | direct | Condensed numerals | The clutter | own | active |\n"], "R-003")
        self.assertEqual(library.check(p)[1], [])

    def test_missing_notes_images_and_reused_ids_are_reported(self):
        d = tempfile.mkdtemp()
        p = write(d, ["| R-001 | A site | https://example.com | look | hero | direct | | | own | active |\n",
                      "| R-001 | Twice | https://example.org | look | hero | direct | b | r | own | active |\n",
                      "| R-002 | A scan | | type | typography | direct | b | r | own | active |\n"], "R-002")
        problems = " ".join(library.check(p)[1])
        self.assertIn("Borrow and a Reject", problems)
        self.assertIn("used twice", problems)
        self.assertIn("no URL and no image", problems)
        self.assertIn("Next free ID", problems)

    def test_retired_entries_need_no_notes(self):
        d = tempfile.mkdtemp()
        p = write(d, ["| R-001 | Old | https://example.com | look | hero | direct | | | own | retired |\n"], "R-002")
        self.assertEqual(library.check(p)[1], [])

    def test_init_never_overwrites(self):
        d = tempfile.mkdtemp()
        env = dict(os.environ, FASTIDIOUS_LIBRARY=d)
        run = lambda: subprocess.run([sys.executable, os.path.join(SCRIPTS, "library.py"), "init"], env=env, capture_output=True, text=True)
        run()
        p = os.path.join(d, "REFERENCES.md")
        open(p, "a").write("mine\n")
        self.assertIn("untouched", run().stdout)
        self.assertTrue(open(p).read().endswith("mine\n"))


if __name__ == "__main__":
    unittest.main()
