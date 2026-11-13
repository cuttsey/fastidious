"""Offline checks on identity-director's precedents and colour-director's fit check."""
import json
import os
import sys
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN, "skills", "colour-director", "scripts"))
sys.path.insert(0, os.path.join(PLUGIN, "skills", "identity-director", "scripts"))
import palette  # noqa: E402
import precedents  # noqa: E402


class Precedents(unittest.TestCase):
    def test_records_are_complete(self):
        cases = precedents.load()
        self.assertEqual(len(cases), 14)
        for c in cases:
            self.assertIn(c["register"], palette.REGISTERS)
            self.assertTrue(c["url"].startswith("https://www.primary.studio/work/"))
            for h in c["palette"].values():
                palette.hex_rgb(h)

    def test_fit_recognises_every_precedent_structure(self):
        for c in precedents.load():
            r = palette.fit({"colours": c["palette"], "gradient": c.get("gradient", False)}, c["register"])
            self.assertEqual(r["structure"], c["structure"], c["brand"])

    def test_search_by_source(self):
        names = [c["brand"] for c in precedents.search(precedents.load(), source="name")]
        self.assertIn("Paper", names)
        self.assertNotIn("Heron", names)


class Fit(unittest.TestCase):
    TRUST = {"colours": {"navy": "#132B4D", "cream": "#F8F5EE", "orange": "#FE802C"}}

    def test_trust_palette_passes(self):
        r = palette.fit(self.TRUST, "trust")
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["structure"], "deep ground, warm light, one signal")

    def test_signal_near_a_competitor_fails(self):
        r = palette.fit(self.TRUST, "trust", ["#ff7a30"])
        self.assertFalse(r["ok"])
        self.assertTrue(r["breaks"][0].startswith("ownership"))

    def test_neon_kit_breaks_trust_and_quiet_breaks_expressive(self):
        kit = {"colours": {"blue": "#3448FB", "lime": "#DFFF82", "pink": "#F673FE", "black": "#121212", "white": "#FFFFFF"}}
        self.assertFalse(palette.fit(kit, "trust")["ok"])
        quiet = {"colours": {"stone": "#8a8478", "paper": "#f2efe8", "ink": "#222"}}
        self.assertFalse(palette.fit(quiet, "expressive")["ok"])

    def test_notes_white_and_hueless_dark(self):
        r = palette.fit({"colours": {"black": "#111111", "white": "#ffffff", "blue": "#2255ff"}}, "expressive")
        self.assertTrue(any("pure white" in n for n in r["notes"]))
        self.assertTrue(any("no hue" in n for n in r["notes"]))


if __name__ == "__main__":
    unittest.main()
