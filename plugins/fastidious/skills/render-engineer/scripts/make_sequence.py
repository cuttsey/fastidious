#!/usr/bin/env python3
"""make_sequence: turns a film or a folder of frames into a scroll-scrubbed WebP sequence for scroll-film.js.

    python3 make_sequence.py shot.mp4 site/frames/S02 --frames 48
    python3 make_sequence.py renders/S02/ site/frames/S02 --sizes 1600,768 --quality 78

Writes, inside the output folder:
  <size>/f_001.webp ...    one folder per width (default 1600 and 768 px), same frame count in each
  poster.jpg                the poster frame at the largest size, for the HTML fallback and for reduced motion
  manifest.json             {"count", "width", "height", "sizes", "pattern", "poster", "bytes"}

A film is sampled evenly to --frames frames; a folder of PNG or JPEG frames is used in name order. Phones get
the smallest size, so keep 768 unless the design needs more. Needs ffmpeg built with libwebp. Standard library only.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

FRAME_EXT = (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff")


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                          "stream=width,height,nb_read_packets:format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    s = j["streams"][0]
    return int(s["width"]), int(s["height"]), int(s.get("nb_read_packets") or 0), float(j["format"].get("duration") or 0)


def manifest(count, width, height, sizes, poster, total_bytes):
    """The manifest scroll-film.js reads. Kept as a pure function so it can be tested without ffmpeg."""
    sizes = sorted({int(s) for s in sizes}, reverse=True)
    return {"count": int(count), "width": int(width), "height": int(height), "sizes": sizes,
            "pattern": "{size}/f_{n}.webp", "pad": 3, "poster": int(poster), "bytes": int(total_bytes)}


def frames_from_source(src, n, work):
    """Return a sorted list of frame image paths, extracting from a film when src is a file."""
    if os.path.isdir(src):
        files = sorted(f for f in glob.glob(os.path.join(src, "*")) if f.lower().endswith(FRAME_EXT))
        if not files:
            raise SystemExit(f"make_sequence: no frames in {src}")
        if n and n < len(files):
            step = (len(files) - 1) / max(1, n - 1)
            files = [files[round(i * step)] for i in range(n)]
        return files
    w, h, packets, dur = probe(src)
    n = n or packets or 48
    fps = n / max(0.04, dur)
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"fps={fps:.5f}", "-frames:v", str(n),
         os.path.join(work, "x_%04d.png")])
    return sorted(glob.glob(os.path.join(work, "x_*.png")))


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="a film, or a folder of frames")
    ap.add_argument("out", help="the output folder, served next to the page")
    ap.add_argument("--frames", type=int, default=0, help="number of frames (default: all, or 48 for a film)")
    ap.add_argument("--sizes", default="1600,768", help="widths in px, largest first")
    ap.add_argument("--quality", type=int, default=78, help="WebP quality, 0 to 100")
    ap.add_argument("--poster", default="middle", help="'first', 'middle', 'last' or a frame number (1-based)")
    a = ap.parse_args(argv)
    if not shutil.which("ffmpeg"):
        raise SystemExit("make_sequence: needs ffmpeg with libwebp")
    sizes = sorted({int(s) for s in a.sizes.split(",")}, reverse=True)
    work = tempfile.mkdtemp()
    try:
        files = frames_from_source(a.src, a.frames, work)
        n = len(files)
        w0, h0, _, _ = probe(files[0])
        os.makedirs(a.out, exist_ok=True)
        total = 0
        for size in sizes:
            d = os.path.join(a.out, str(size))
            os.makedirs(d, exist_ok=True)
            for i, f in enumerate(files, 1):
                dst = os.path.join(d, f"f_{i:03d}.webp")
                run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", f"scale={size}:-2:flags=lanczos", "-c:v", "libwebp",
                     "-quality", str(a.quality), "-compression_level", "6", dst])
                total += os.path.getsize(dst)
        poster = {"first": 1, "middle": (n + 1) // 2, "last": n}.get(a.poster) or max(1, min(n, int(a.poster)))
        run(["ffmpeg", "-v", "error", "-y", "-i", files[poster - 1], "-vf", f"scale={sizes[0]}:-2:flags=lanczos",
             "-q:v", "3", os.path.join(a.out, "poster.jpg")])
        h = round(h0 * sizes[0] / w0 / 2) * 2
        m = manifest(n, sizes[0], h, sizes, poster, total)
        with open(os.path.join(a.out, "manifest.json"), "w") as fh:
            json.dump(m, fh, indent=1)
        print(f"make_sequence: {n} frames at {', '.join(map(str, sizes))} px, {total / 1e6:.1f} MB in all, poster {poster}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
