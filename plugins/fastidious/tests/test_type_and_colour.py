"""Offline checks on type-director's lookup and colour-director's palette tools."""
import json
import os
import sys
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN, "skills", "type-director", "scripts"))
sys.path.insert(0, os.path.join(PLUGIN, "skills", "colour-director", "scripts"))
import palette  # noqa: E402
import type_lookup  # noqa: E402


class TypeLookup(unittest.TestCase):
    def test_catalogue_is_well_formed(self):
        cat = type_lookup.load()
        self.assertGreater(len(cat["faces"]), 60)
        for f in cat["faces"]:
            self.assertIn(f["overuse"], (0, 1, 2, 3))
            self.assertIn(f["source"], ("google", "fontshare"))
            self.assertTrue(f["genre"] and f["voice"])
        names = [f["family"] for f in cat["faces"]]
        self.assertEqual(len(names), len(set(names)))

    def test_search_ranks_by_meaning_and_hides_defaults(self):
        hits = type_lookup.search(type_lookup.load(), "seventeenth-century", "rustic,english", max_overuse=1)
        self.assertTrue(hits[0]["family"].startswith("IM Fell"))
        self.assertFalse(any(f["overuse"] > 1 for f in hits))

    def test_overused_list_names_the_template_faces(self):
        over = {f["family"] for f in type_lookup.load()["faces"] if f["overuse"] == 3}
        self.assertTrue({"Inter", "Space Grotesk", "Playfair Display"} <= over)


class Palette(unittest.TestCase):
    def test_round_trip_and_contrast(self):
        for h in ("#18222a", "#c9802f", "#f1e3c3", "#ffffff", "#000000"):
            self.assertEqual(palette.rgb_hex(palette.oklab_rgb(palette.rgb_oklab(palette.hex_rgb(h)))), h)
        self.assertAlmostEqual(palette.contrast("#000000", "#ffffff"), 21.0, places=1)

    def test_scale_runs_light_to_dark_in_gamut(self):
        ramp = palette.scale("#6b7140", 9)
        Ls = [palette.oklch(palette.rgb_oklab(palette.hex_rgb(h)))[0] for h in ramp]
        self.assertEqual(Ls, sorted(Ls, reverse=True))

    def test_wada_finds_combinations_near_anchors(self):
        res = palette.wada_near(["#bb7125", "#6b7140"], size=4, top=3)
        self.assertEqual(res[0][0], 243)
        self.assertEqual(len(res[0][2]), 4)

    def test_cliche_detection(self):
        self.assertTrue(any("terracotta" in c for c in palette.cliches({"bg": "#f4f1ea", "accent": "#c4623f", "ink": "#222"})))
        self.assertTrue(any("muddy" in c for c in palette.cliches({"a": "#f0e6d1", "b": "#8a6138", "c": "#a86b2b", "d": "#2b2621"})))
        self.assertEqual(palette.cliches({"slate": "#18222a", "buff": "#f1e3c3", "olive": "#6b7140", "sienna": "#c9802f"}), [])

    def test_check_reports_failing_pairs(self):
        r = palette.check({"colours": {"a": "#777777", "b": "#888888"}, "pairs": [["a", "b"]]})
        self.assertFalse(r["ok"])


if __name__ == "__main__":
    unittest.main()
