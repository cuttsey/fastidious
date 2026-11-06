"""Offline checks on render-engineer's scroll-film kit and sequence script."""
import json
import os
import shutil
import subprocess
import sys
import unittest

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(PLUGIN, "skills", "render-engineer")
sys.path.insert(0, os.path.join(KIT, "scripts"))
import make_sequence  # noqa: E402

NODE_TEST = r"""
const k = require(process.argv[1]);
const scenes = [{id:'A',at:0,len:0.5,out:{type:'iris',len:0.2}},{id:'B',at:0.5,len:0.5}];
const r = [k.locate(scenes,0), k.locate(scenes,0.45), k.locate(scenes,0.75), k.locate(scenes,1)];
const pr = k.priority([4,4], 0, 2, 1000).slice(0, 5);
console.log(JSON.stringify({r, pr, modes: k.MODES}));
"""


class SequenceScript(unittest.TestCase):
    def test_manifest_shape(self):
        m = make_sequence.manifest(24, 960, 540, [480, 960], 12, 123456)
        self.assertEqual(m["sizes"], [960, 480])
        self.assertEqual(m["pattern"], "{size}/f_{n}.webp")
        self.assertEqual((m["count"], m["poster"], m["pad"]), (24, 12, 3))


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class ScrollFilm(unittest.TestCase):
    def run_node(self):
        out = subprocess.run(["node", "-e", NODE_TEST, os.path.join(KIT, "assets", "scroll-film.js")],
                             capture_output=True, text=True, check=True).stdout
        return json.loads(out)

    def test_locate_and_transition(self):
        r = self.run_node()["r"]
        self.assertEqual((r[0]["id"], r[0]["t"], r[0]["trans"]), ("A", 0, 0))
        self.assertEqual(r[1]["id"], "A")
        self.assertAlmostEqual(r[1]["trans"], 0.5, places=6)  # 0.45 is t=0.9: halfway through the last 20%
        self.assertEqual((r[2]["id"], r[2]["trans"]), ("B", 0))
        self.assertEqual((r[3]["id"], r[3]["t"]), ("B", 1))

    def test_priority_is_nearest_first(self):
        pr = self.run_node()["pr"]
        self.assertEqual(pr[0], [0, 2])
        self.assertEqual(sorted(map(tuple, pr[1:3])), [(0, 1), (0, 3)])
        self.assertTrue(all(s == 0 for s, _ in pr[:4]))

    def test_no_scroll_interception(self):
        src = open(os.path.join(KIT, "assets", "scroll-film.js")).read()
        code = "\n".join(l for l in src.splitlines() if not l.strip().startswith(("//", "*", "/*")))
        for bad in ("preventDefault", "'wheel'", '"wheel"', "touchmove", "keydown"):
            self.assertNotIn(bad, code)


if __name__ == "__main__":
    unittest.main()
