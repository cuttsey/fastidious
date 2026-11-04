"""Provider adapters. Each builds the exact request it will send, so --dry-run can write it to disk unsent.

images:  OpenAI Images API, gpt-image-2 (POST /images/generations, multipart POST /images/edits)
video:   Seedance 2.0 on BytePlus ModelArk (POST /contents/generations/tasks, GET /contents/generations/tasks/{id})
         Kling on the Kling API (POST /v1/videos/image2video, GET /v1/videos/image2video/{task_id})

Every video provider exposes the same three calls: create_request() builds the request, send() returns a
task ID, and result() returns {"status": "running" | "succeeded" | "failed", "video_url", "last_frame_url",
"error", "usage"}, so the command line never needs to know which provider made a clip.

OpenAI's own video API (Sora 2, /v1/videos) was shut down on 24 September 2026, so motion goes to Seedance.
"""
import base64
import hashlib
import hmac
import json
import mimetypes
import os
import time

from . import net as http


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


class OpenAIImages:
    def __init__(self, cfg, token=None):
        self.base, self.model, self.token = cfg["openai_base"], cfg["image_model"], token

    def generate_request(self, prompt, size, quality, n=1, background="opaque", output_format="png"):
        return {"url": f"{self.base}/images/generations", "json": {
            "model": self.model, "prompt": prompt, "size": size, "quality": quality, "n": n,
            "background": background, "output_format": output_format}}

    def edit_request(self, prompt, images, size, quality, n=1, output_format="png"):
        # Several reference images may be sent; repeated image[] fields carry them.
        return {"url": f"{self.base}/images/edits", "fields": {
            "model": self.model, "prompt": prompt, "size": size, "quality": quality, "n": str(n),
            "output_format": output_format}, "files": [("image[]", p) for p in images]}

    def send(self, req):
        if "json" in req:
            r = http.json_request("POST", req["url"], self.token, req["json"], timeout=300)
        else:
            r = http.multipart_request(req["url"], self.token, req["fields"], req["files"])
        return [base64.b64decode(d["b64_json"]) for d in r.get("data", [])]


class Seedance:
    name = "seedance"
    TERMINAL = {"succeeded", "failed", "expired", "cancelled"}

    def __init__(self, cfg, token=None, draft=False):
        self.base, self.token = cfg["ark_base"], token
        self.model = cfg["video_model_draft"] if draft else cfg["video_model"]

    def create_request(self, prompt, *, first_frame=None, last_frame=None, references=(), ratio="16:9",
                       resolution="1080p", duration=5, seed=-1, camera_fixed=False, generate_audio=False,
                       return_last_frame=False):
        content = [{"type": "text", "text": prompt}]
        # Order matters: reference images are bound in the prompt as @Image1, @Image2 ... by position.
        for p in references:
            content.append({"type": "image_url", "image_url": {"url": data_uri(p)}, "role": "reference_image"})
        if first_frame:
            content.append({"type": "image_url", "image_url": {"url": data_uri(first_frame)}, "role": "first_frame"})
        if last_frame:
            if not first_frame:
                raise ValueError("Seedance only accepts a last_frame together with a first_frame.")
            content.append({"type": "image_url", "image_url": {"url": data_uri(last_frame)}, "role": "last_frame"})
        body = {"model": self.model, "content": content, "ratio": ratio, "resolution": resolution,
                "duration": int(duration), "seed": int(seed), "camera_fixed": bool(camera_fixed),
                # Seedance 2.0 generates audio unless told not to. Sound is designed in post, so it is off.
                "generate_audio": bool(generate_audio), "watermark": False}
        if return_last_frame:
            body["return_last_frame"] = True
        return {"url": f"{self.base}/contents/generations/tasks", "json": body}

    def send(self, req):
        return http.json_request("POST", req["url"], self.token, req["json"])["id"]

    def get(self, task_id):
        return http.json_request("GET", f"{self.base}/contents/generations/tasks/{task_id}", self.token)

    def result(self, task_id):
        t = self.get(task_id)
        st = t.get("status")
        status = "succeeded" if st == "succeeded" else "failed" if st in self.TERMINAL else "running"
        c = t.get("content") or {}
        return {"status": status, "raw_status": st, "video_url": c.get("video_url"), "last_frame_url": c.get("last_frame_url"),
                "error": t.get("error"), "usage": t.get("usage")}


def jwt_hs256(access_key, secret_key, ttl=1800, now=None):
    """Kling's access-key authentication: a short-lived HS256 JWT with iss = access key."""
    now = int(now or time.time())
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d, separators=(",", ":")).encode()).rstrip(b"=")
    head = enc({"alg": "HS256", "typ": "JWT"}) + b"." + enc({"iss": access_key, "exp": now + ttl, "nbf": now - 5})
    sig = base64.urlsafe_b64encode(hmac.new(secret_key.encode(), head, hashlib.sha256).digest()).rstrip(b"=")
    return (head + b"." + sig).decode()


class Kling:
    """Kling image-to-video. Auth is either KLING_API_KEY (sent as a bearer token) or KLING_ACCESS_KEY and
    KLING_SECRET_KEY, from which a fresh 30-minute JWT is signed for every call.

    Differences from Seedance that matter to the shot list:
    - The output's aspect ratio follows the input image, which is why fmotion crops the first frame to the film ratio.
    - The avoid list goes in negative_prompt, a dedicated field, instead of the prompt.
    - An end frame (image_tail) generally needs mode "pro".
    - Reference images are not sent; continuity comes from the first and last frames.
    """
    name = "kling"

    def __init__(self, cfg, auth=None, draft=False):
        self.base, self.model, self.auth = cfg["kling_base"], cfg["kling_model"], auth
        self.mode = cfg["kling_mode_draft"] if draft else cfg["kling_mode_final"]
        self.cfg_scale = cfg.get("kling_cfg_scale")

    def token(self):
        if not self.auth:
            return None
        if self.auth.get("api_key"):
            return self.auth["api_key"]
        return jwt_hs256(self.auth["access_key"], self.auth["secret_key"])

    def create_request(self, prompt, *, first_frame, last_frame=None, negative_prompt="", duration=5, sound=False):
        if not first_frame:
            raise ValueError("fmotion animates approved stills, so Kling always gets a first frame.")
        body = {"model_name": self.model, "image": b64(first_frame), "prompt": prompt[:2500], "mode": self.mode,
                "duration": str(int(duration))}
        if negative_prompt:
            body["negative_prompt"] = negative_prompt[:2500]
        if last_frame:
            body["image_tail"] = b64(last_frame)
            body["mode"] = "pro"  # end-frame control generally needs pro mode
        if self.cfg_scale is not None and not self.model.startswith("kling-v2"):
            body["cfg_scale"] = self.cfg_scale  # v2.x models reject it
        if sound:
            body["sound"] = "on"
        return {"url": f"{self.base}/v1/videos/image2video", "json": body}

    def _check(self, r):
        if r.get("code", 0) != 0:
            raise http.ApiError(r.get("code"), json.dumps(r))
        return r["data"]

    def send(self, req):
        return self._check(http.json_request("POST", req["url"], self.token(), req["json"]))["task_id"]

    def result(self, task_id):
        d = self._check(http.json_request("GET", f"{self.base}/v1/videos/image2video/{task_id}", self.token()))
        st = d.get("task_status")
        status = "succeeded" if st in ("succeed", "succeeded") else "failed" if st == "failed" else "running"
        videos = (d.get("task_result") or {}).get("videos") or [{}]
        return {"status": status, "raw_status": st, "video_url": videos[0].get("url"), "last_frame_url": None,
                "error": d.get("task_status_msg"), "usage": None}


def kling_auth():
    if os.environ.get("KLING_API_KEY"):
        return {"api_key": os.environ["KLING_API_KEY"]}
    ak, sk = os.environ.get("KLING_ACCESS_KEY"), os.environ.get("KLING_SECRET_KEY")
    if ak and sk:
        return {"access_key": ak, "secret_key": sk}
    raise SystemExit("Set KLING_API_KEY, or KLING_ACCESS_KEY and KLING_SECRET_KEY, in your shell.")


def video(name, cfg, draft=False, dry_run=False):
    """Returns a video provider by name, authenticated from the environment unless this is a dry run."""
    from . import config
    if name == "seedance":
        return Seedance(cfg, None if dry_run else config.key("ARK_API_KEY"), draft=draft)
    if name == "kling":
        return Kling(cfg, None if dry_run else kling_auth(), draft=draft)
    raise SystemExit(f"Unknown video provider {name!r}. Use seedance or kling.")
