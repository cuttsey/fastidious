"""Offline checks on copy-director's lint and world-bible's series check (no ffmpeg needed)."""
import os
import sys
import tempfile
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN, "skills", "copy-director", "scripts"))
sys.path.insert(0, os.path.join(PLUGIN, "skills", "world-bible", "scripts"))
import copy_lint  # noqa: E402
import series_check  # noqa: E402

FAIL_WORDS, WARN_WORDS = copy_lint.cliches()


def lint_lines(*lines, kind="body"):
    return copy_lint.lint([(f"k{i}", t, kind) for i, t in enumerate(lines)], FAIL_WORDS, WARN_WORDS)


class CopyLint(unittest.TestCase):
    def test_the_cliche_list_is_read_from_devices(self):
        names = [n for n, _ in FAIL_WORDS]
        self.assertIn("elevate", names)
        self.assertIn("leverage (as a verb)", names)
        self.assertGreater(len(names), 30)

    def test_plain_specific_copy_passes(self):
        fails, warns, _ = lint_lines("We pick it. We press it. We wait.", "Eleven months in oak.")
        self.assertEqual(fails, [])
        self.assertEqual(warns, [])

    def test_em_dash_not_x_and_cliches_fail(self):
        fails, _, _ = lint_lines("Sold out — sorry.", "It's not just cider, it's a way of life.",
                                 "We help you leverage seamless solutions.")
        rules = " ".join(r for _, r, _ in fails)
        self.assertIn("em dash", rules)
        self.assertIn("not X", rules)
        self.assertIn("seamless", rules)
        self.assertIn("leverage", rules)

    def test_leverage_as_a_noun_is_allowed(self):
        fails, _, _ = lint_lines("The leverage in this deal is the land.")
        self.assertEqual(fails, [])

    def test_quoted_cliches_are_allowed(self):
        fails, _, _ = lint_lines('Other studios promise to "elevate your brand". We draw it.')
        self.assertEqual(fails, [])

    def test_display_warnings(self):
        _, warns, _ = lint_lines("Elegant Cider For Every Single Occasion You Can Imagine Today", kind="display")
        rules = " ".join(r for _, r, _ in warns)
        self.assertIn("Title Case", rules)
        self.assertIn("display line", rules)

    def test_copy_deck_reads_only_the_line_column(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "COPY-DECK.md")
        open(p, "w").write("# Deck\n\n## Lines\n\n| Key | Line | Job |\n| --- | --- | --- |\n"
                           "| hero.h1 | The long way / round, on purpose | Elevate the idea |\n\n## Lint\n\nseamless\n")
        items = copy_lint.visible_text(open(p).read(), ".md")
        self.assertEqual(items, [("hero.h1", "The long way round, on purpose", "display")])

    def test_html_joins_letters_split_for_animation(self):
        html = '<h1><span class="ln"><i><span class="ch">P</span><span class="ch">e</span>ar</i></span></h1>'
        self.assertEqual(copy_lint.visible_text(html, ".html")[0][1], "Pear")

    def test_template_deck_passes(self):
        tpl = os.path.join(PLUGIN, "skills", "copy-director", "templates", "COPY-DECK.md")
        self.assertEqual(copy_lint.main([tpl]), 0)


class SeriesCheck(unittest.TestCase):
    def test_lab_reference_points(self):
        L, a, b = series_check.srgb_to_lab((255, 255, 255))
        self.assertAlmostEqual(L, 100, delta=0.1)
        self.assertAlmostEqual(a, 0, delta=0.2)
        L, a, b = series_check.srgb_to_lab((0, 0, 0))
        self.assertAlmostEqual(L, 0, delta=0.1)
        L, a, b = series_check.srgb_to_lab((255, 0, 0))
        self.assertAlmostEqual(L, 53.2, delta=0.5)
        self.assertGreater(a, 75)

    def test_bible_parsing(self):
        tpl = os.path.join(PLUGIN, "skills", "world-bible", "templates", "WORLD-BIBLE.md")
        self.assertEqual(series_check.parse_bible(tpl), {"palette": [], "light": None})
        d = tempfile.mkdtemp()
        p = os.path.join(d, "WORLD-BIBLE.md")
        open(p, "w").write("## Palette\n\n| Role | Hex |\n| --- | --- |\n| Sky | #024794 |\n| Gold | #B8902E |\n\n"
                           "Never: #ff00ff.\n\n## Light\n\n- Direction: from the left\n")
        self.assertEqual(series_check.parse_bible(p), {"palette": ["#024794", "#b8902e"], "light": "left"})

    def test_metrics_on_a_synthetic_frame(self):
        w, h = 6, 2
        sky, white = bytes((2, 71, 148)), bytes((250, 250, 250))
        row = white * 2 + sky * 4  # bright on the left
        m = series_check.metrics(row * h, w, h, ["#024794"])
        self.assertEqual(m["palette"], 1.0)
        self.assertGreater(m["light"], 0)
        self.assertLess(m["warmth"], 0)

    def test_flags_and_looks(self):
        def item(key, light, pal=0.9):
            return {"path": "x", "m": {"palette": pal, "key": key, "contrast": 15, "chroma": 20, "warmth": 5,
                                       "light": light}, "flags": [], "look": []}
        items = series_check.flag([item(40, 6), item(42, 7), item(80, 5), item(41, -9, 0.5)], {"light": "left"})
        self.assertTrue(items[2]["look"])
        self.assertFalse(items[2]["flags"])
        self.assertEqual(len(items[3]["flags"]), 2)
        self.assertFalse(items[0]["flags"] or items[0]["look"])


if __name__ == "__main__":
    unittest.main()
