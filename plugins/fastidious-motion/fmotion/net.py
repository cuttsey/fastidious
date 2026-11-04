"""Small HTTP layer on urllib: JSON, multipart, download, with retries on rate limits and server errors."""
import json
import os
import time
import urllib.error
import urllib.request
import uuid

RETRY_STATUS = {408, 409, 429, 500, 502, 503, 504}


class ApiError(Exception):
    def __init__(self, status, body):
        super().__init__(f"HTTP {status}: {body[:600]}")
        self.status, self.body = status, body


def _send(req, timeout=120, retries=4):
    delay = 2
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code in RETRY_STATUS and attempt < retries:
                wait = float(e.headers.get("Retry-After") or delay)
                time.sleep(wait)
                delay *= 2
                continue
            raise ApiError(e.code, body) from None
        except urllib.error.URLError:
            if attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise


def json_request(method, url, token, payload=None, timeout=120):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    return json.loads(_send(req, timeout) or b"{}")


def multipart_request(url, token, fields, files, timeout=300):
    """fields: {name: value}; files: [(field_name, path)]. Repeated field names are allowed (image[])."""
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    for name, path in files:
        ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
        with open(path, "rb") as f:
            blob = f.read()
        head = (f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{os.path.basename(path)}"\r\n'
                f"Content-Type: {mime}\r\n\r\n").encode()
        parts.append(head + blob + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(url, data=b"".join(parts), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    return json.loads(_send(req, timeout))


def download(url, path, timeout=600):
    """Provider result URLs expire (Seedance's after 24 hours), so results are copied locally at once."""
    tmp = path + ".part"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)
    os.replace(tmp, path)
    return path
