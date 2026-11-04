"""Offline tests: providers build the documented requests, the CLI runs end to end against mocked APIs."""
import base64
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from fmotion import cli, config, ledger, prompts, providers  # noqa: E402

EXAMPLE = os.path.join(ROOT, "examples", "fastidious-film")
HAS_FFMPEG = shutil.which("ffmpeg") is not None


def png(path, colour="0x1F4BFF", size="1536x1024"):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c={colour}:s={size}", "-frames:v", "1", path], check=True)
    return path


class Providers(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load("/nonexistent")
        self.tmp = tempfile.mkdtemp()

    def test_image_generate_request(self):
        r = providers.OpenAIImages(self.cfg).generate_request("a quiet frame", "1536x1024", "low")
        self.assertTrue(r["url"].endswith("/images/generations"))
        self.assertEqual(r["json"]["model"], "gpt-image-2")
        self.assertEqual(r["json"]["size"], "1536x1024")

    def test_image_edit_sends_every_reference(self):
        r = providers.OpenAIImages(self.cfg).edit_request("x", ["a.png", "b.png"], "1024x1024", "high")
        self.assertEqual([f[0] for f in r["files"]], ["image[]", "image[]"])

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg")
    def test_seedance_request_roles_and_order(self):
        a, b, c = (png(os.path.join(self.tmp, n)) for n in ("ref.png", "first.png", "last.png"))
        r = providers.Seedance(self.cfg).create_request("p", first_frame=b, last_frame=c, references=[a], duration=6.0)
        roles = [i.get("role") for i in r["json"]["content"]]
        self.assertEqual(roles, [None, "reference_image", "first_frame", "last_frame"])
        self.assertTrue(r["json"]["content"][1]["image_url"]["url"].startswith("data:image/png;base64,"))
        self.assertEqual(r["json"]["duration"], 6)
        self.assertFalse(r["json"]["generate_audio"])
        self.assertTrue(r["url"].endswith("/contents/generations/tasks"))

    def test_last_frame_needs_first(self):
        with self.assertRaises(ValueError):
            providers.Seedance(self.cfg).create_request("p", last_frame="x.png")

    def test_draft_uses_fast_model(self):
        self.assertIn("fast", providers.Seedance(self.cfg, draft=True).model)


class KlingProvider(unittest.TestCase):
    def setUp(self):
        self.cfg = config.load("/nonexistent")
        self.tmp = tempfile.mkdtemp()

    def test_jwt_is_valid_hs256(self):
        import hashlib, hmac
        tok = providers.jwt_hs256("ak", "sk", now=1_800_000_000)
        head, body, sig = tok.split(".")
        pad = lambda x: x + "=" * (-len(x) % 4)
        claims = json.loads(base64.urlsafe_b64decode(pad(body)))
        self.assertEqual(json.loads(base64.urlsafe_b64decode(pad(head))), {"alg": "HS256", "typ": "JWT"})
        self.assertEqual(claims, {"iss": "ak", "exp": 1_800_001_800, "nbf": 1_799_999_995})
        good = base64.urlsafe_b64encode(hmac.new(b"sk", f"{head}.{body}".encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
        self.assertEqual(sig, good)

    def test_api_key_wins_over_access_keys(self):
        k = providers.Kling(self.cfg, {"api_key": "K"})
        self.assertEqual(k.token(), "K")

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg")
    def test_request_shape(self):
        a, b = png(os.path.join(self.tmp, "a.png")), png(os.path.join(self.tmp, "b.png"))
        k = providers.Kling(self.cfg, draft=True)
        r = k.create_request("p", first_frame=a, negative_prompt="lens flares, text", duration=6)
        self.assertTrue(r["url"].endswith("/v1/videos/image2video"))
        j = r["json"]
        self.assertEqual((j["model_name"], j["mode"], j["duration"]), ("kling-v3", "std", "6"))
        self.assertFalse(j["image"].startswith("data:"))  # Kling wants raw base64, no data: prefix
        self.assertEqual(j["negative_prompt"], "lens flares, text")
        self.assertIn("cfg_scale", j)
        r2 = k.create_request("p", first_frame=a, last_frame=b)
        self.assertEqual(r2["json"]["mode"], "pro")  # an end frame needs pro mode
        self.assertIn("image_tail", r2["json"])

    def test_v2_models_get_no_cfg_scale(self):
        cfg = dict(self.cfg, kling_model="kling-v2-5-turbo")
        p = os.path.join(self.tmp, "x.png")
        open(p, "wb").write(b"x")
        self.assertNotIn("cfg_scale", providers.Kling(cfg).create_request("p", first_frame=p)["json"])

    def test_result_normalised(self):
        k = providers.Kling(self.cfg, {"api_key": "K"})
        done = {"code": 0, "data": {"task_id": "t", "task_status": "succeed", "task_result": {"videos": [{"url": "https://v/x.mp4"}]}}}
        with mock.patch("fmotion.net.json_request", return_value=done):
            r = k.result("t")
        self.assertEqual((r["status"], r["video_url"]), ("succeeded", "https://v/x.mp4"))
        with mock.patch("fmotion.net.json_request", return_value={"code": 1301, "message": "risk"}):
            with self.assertRaises(Exception):
                k.result("t")


class Prompts(unittest.TestCase):
    def test_brand_and_guards_in_every_prompt(self):
        brief = json.load(open(os.path.join(EXAMPLE, "brief.json")))
        shot = json.load(open(os.path.join(EXAMPLE, "shotlist.json")))["shots"][0]
        f = prompts.frame_prompt(brief, shot)
        self.assertIn("#1F4BFF", f)
        self.assertIn("No text", f)
        self.assertIn("Avoid:", f)
        self.assertIn("upper left third", f)
        m = prompts.motion_prompt(brief, shot, n_refs=2)
        self.assertIn("@Image1, @Image2", m)
        self.assertIn("One move only", m)


class Ledger(unittest.TestCase):
    def test_ids_are_permanent_and_sequential(self):
        d = tempfile.mkdtemp()
        led = ledger.Ledger(d)
        self.assertEqual(led.new("O", shot="S01"), "O-001")
        self.assertEqual(led.new("O", shot="S01"), "O-002")
        self.assertEqual(ledger.Ledger(d).new("O"), "O-003")  # survives reload
        self.assertEqual(led.new("D", shot="S01", option="O-001"), "D-001")
        self.assertTrue(os.path.exists(os.path.join(d, "LEDGER.md")))


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg")
class EndToEnd(unittest.TestCase):
    """frames -> pick -> animate -> status -> pick -> assemble -> check, with both APIs mocked."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.ws = os.path.join(self.dir, "motion")
        cli.main(["--dir", self.ws, "init"])
        shutil.copy(os.path.join(EXAMPLE, "brief.json"), self.ws)
        shots = json.load(open(os.path.join(EXAMPLE, "shotlist.json")))
        shots["shots"] = shots["shots"][:2]
        json.dump(shots, open(os.path.join(self.ws, "shotlist.json"), "w"))
        os.environ["OPENAI_API_KEY"] = os.environ["ARK_API_KEY"] = os.environ["KLING_API_KEY"] = "test"
        self.blob = open(png(os.path.join(self.dir, "img.png")), "rb").read()
        clip = os.path.join(self.dir, "clip.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x0E1454:s=1280x720:r=24:d=5",
                        "-pix_fmt", "yuv420p", clip], check=True)
        self.clip = clip

    def fake_json(self, method, url, token, payload=None, timeout=120):
        if url.endswith("/images/generations"):
            return {"data": [{"b64_json": base64.b64encode(self.blob).decode()}]}
        if url.endswith("/contents/generations/tasks"):
            return {"id": "cgt-test-" + str(len(payload["content"]))}
        if url.endswith("/v1/videos/image2video"):
            self.assertIn("negative_prompt", payload)
            return {"code": 0, "data": {"task_id": "kling-1", "task_status": "submitted"}}
        if "/v1/videos/image2video/" in url:
            return {"code": 0, "data": {"task_id": "kling-1", "task_status": "succeed",
                                        "task_result": {"videos": [{"url": "https://example.invalid/k.mp4"}]}}}
        if "/contents/generations/tasks/" in url:
            return {"id": url.rsplit("/", 1)[1], "status": "succeeded", "content": {"video_url": "https://example.invalid/v.mp4"}}
        raise AssertionError(url)

    def fake_download(self, url, path, timeout=600):
        shutil.copy(self.clip, path)
        return path

    def test_pipeline(self):
        out = io.StringIO()
        with mock.patch("fmotion.net.json_request", self.fake_json), mock.patch("fmotion.net.download", self.fake_download), \
                mock.patch("sys.stdout", out):
            cli.main(["--dir", self.ws, "frames"])
            led = ledger.Ledger(self.ws)
            stills = led.find(type="still")
            self.assertEqual(len(stills), 4)  # two directions for each of two shots
            self.assertTrue(os.path.exists(os.path.join(self.ws, "sheets", "S01-frames.png")))
            cli.main(["--dir", self.ws, "pick", "O-001", "--reason", "edge light is cleaner"])
            cli.main(["--dir", self.ws, "pick", "O-003"])
            cli.main(["--dir", self.ws, "animate", "--draft", "--provider", "seedance,kling"])
            cli.main(["--dir", self.ws, "status"])
            led = ledger.Ledger(self.ws)
            clips = led.find(type="clip")
            self.assertEqual([c["provider"] for c in clips], ["seedance", "kling", "seedance", "kling"])
            self.assertEqual({c["status"] for c in clips}, {"succeeded"})
            clips = [c for c in clips if c["provider"] == "seedance"]
            cli.main(["--dir", self.ws, "pick", clips[0]["id"]])
            cli.main(["--dir", self.ws, "pick", clips[1]["id"]])
            cli.main(["--dir", self.ws, "assemble"])
            cut = ledger.Ledger(self.ws).find(kind="A")[0]
            self.assertTrue(os.path.exists(cut["file"]))
            cli.main(["--dir", self.ws, "check", cut["id"]])
            report = ledger.Ledger(self.ws).get(cut["id"])["checks"]
            self.assertTrue(report["flash"]["passes"])
            cli.main(["--dir", self.ws, "palette", "O-001"])
            pal = ledger.Ledger(self.ws).get("O-001")["palette"]
            self.assertGreater(pal["per_token"]["cobalt"], 0.9)

    def test_dry_run_spends_nothing(self):
        os.environ.pop("OPENAI_API_KEY")
        with mock.patch("sys.stdout", io.StringIO()):
            cli.main(["--dir", self.ws, "frames", "--dry-run"])
        reqs = os.listdir(os.path.join(self.ws, "requests"))
        self.assertEqual(len(reqs), 4)
        body = json.load(open(os.path.join(self.ws, "requests", sorted(reqs)[0])))
        self.assertEqual(body["json"]["model"], "gpt-image-2")


class Validate(unittest.TestCase):
    def test_flags_text_requests_and_single_direction(self):
        d = tempfile.mkdtemp()
        shutil.copy(os.path.join(EXAMPLE, "brief.json"), d)
        shots = json.load(open(os.path.join(EXAMPLE, "shotlist.json")))
        shots["shots"][0]["frame"]["prompt"] += " with a headline across the top"
        shots["shots"][0]["frame"]["directions"] = ["only one"]
        json.dump(shots, open(os.path.join(d, "shotlist.json"), "w"))
        out = io.StringIO()
        with mock.patch("sys.stdout", out), self.assertRaises(SystemExit):
            cli.main(["--dir", d, "validate"])
        self.assertIn("headline", out.getvalue())
        self.assertIn("one direction is not a choice", out.getvalue())


if __name__ == "__main__":
    unittest.main()
