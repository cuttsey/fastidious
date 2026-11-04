"""ffmpeg helpers: framing, contact sheets for review, palette measurement, assembly and checks."""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _run(args):
    subprocess.run(args, check=True)


def need_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required for this step.")


def _font():
    try:
        return subprocess.run(["fc-match", "-f", "%{file}", "sans:bold"], capture_output=True, text=True).stdout.strip() or None
    except FileNotFoundError:
        return None


def _label(text):
    font = _font()
    if not font:
        return ""
    safe = text.replace(":", r"\:").replace("'", "")
    return f",drawtext=fontfile='{font}':text='{safe}':x=12:y=12:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=8"


def crop_to_ratio(src, dst, ratio):
    """Centre-crops a still to the film's ratio, so the first frame Seedance animates is the frame you approved."""
    need_ffmpeg()
    w, h = (int(x) for x in ratio.split(":"))
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf",
          f"crop='if(gt(iw/ih,{w}/{h}),ih*{w}/{h},iw)':'if(gt(iw/ih,{w}/{h}),ih,iw*{h}/{w})'", dst])
    return dst


def sheet_stills(items, out, cols=3, width=640):
    """items: [(path, label)]. A labelled grid, so a reviewer can name options by ID."""
    need_ffmpeg()
    ins, fc = [], []
    ch = (width * 9 // 16) // 2 * 2
    for i, (p, label) in enumerate(items):
        ins += ["-i", p]
        fc.append(f"[{i}:v]scale={width}:{ch}:force_original_aspect_ratio=decrease,"
                  f"pad={width}:{ch}:(ow-iw)/2:(oh-ih)/2:color=0x111111,setsar=1,format=rgb24{_label(label)}[c{i}]")
    rows = (len(items) + cols - 1) // cols
    for k in range(len(items), rows * cols):  # blank cells keep the grid rectangular
        fc.append(f"color=c=0x111111:s={width}x{ch}:d=1,format=rgb24[c{k}]")
    layout = "|".join(f"{(k % cols) * width}_{(k // cols) * ch}" for k in range(rows * cols))
    if rows * cols == 1:
        fc.append("[c0]null[o]")
    else:
        fc.append("".join(f"[c{k}]" for k in range(rows * cols)) + f"xstack=inputs={rows * cols}:layout={layout}[o]")
    _run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[o]", "-frames:v", "1", out])
    return out


def strip_clip(path, out, label="", frames=6, width=320):
    """Six evenly spaced frames from a clip in one row: enough to judge motion, drift and artefacts."""
    need_ffmpeg()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                               capture_output=True, text=True).stdout.strip() or 5)
    fps = frames / max(dur, 0.1)
    _run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vf",
          f"fps={fps},scale={width}:-2,tile={frames}x1{_label(label)}", "-frames:v", "1", out])
    return out


# ---- palette measurement --------------------------------------------------------------------------------

def _lab(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = (lin(float(c)) for c in rgb)
    x = (r * .4124 + g * .3576 + b * .1805) / .95047
    y = (r * .2126 + g * .7152 + b * .0722)
    z = (r * .0193 + g * .1192 + b * .9505) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def palette_report(path, palette, tolerance=14.0, samples=8):
    """Share of pixels within a CIE76 distance of any brand colour, per colour and overall.

    Neutral pixels (very dark, very light or unsaturated) are counted separately: the brief allows neutral
    shadow and highlight, so they never count against the palette.
    """
    need_ffmpeg()
    is_video = os.path.splitext(path)[1].lower() in {".mp4", ".mov", ".webm"}
    vf = f"fps={samples}/5,scale=96:-2" if is_video else "scale=96:-2"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    tokens = {k: _lab(_hex(v)) for k, v in palette.items()}
    counts = {k: 0 for k in tokens}
    off = neutral = 0
    cache = {}
    for i in range(0, len(raw) - 2, 3):
        px = (raw[i] >> 2, raw[i + 1] >> 2, raw[i + 2] >> 2)  # quantise for speed
        if px not in cache:
            L, a, b = _lab(tuple(c * 4 + 2 for c in px))
            chroma = (a * a + b * b) ** .5
            if L < 12 or L > 94 or chroma < 8:
                cache[px] = "_neutral"
            else:
                best, d = min(((k, ((L - t[0]) ** 2 + (a - t[1]) ** 2 + (b - t[2]) ** 2) ** .5) for k, t in tokens.items()),
                              key=lambda kv: kv[1])
                cache[px] = best if d <= tolerance else "_off"
        hit = cache[px]
        if hit == "_neutral":
            neutral += 1
        elif hit == "_off":
            off += 1
        else:
            counts[hit] += 1
    total = max(1, sum(counts.values()) + off + neutral)
    chromatic = max(1, sum(counts.values()) + off)
    return {"on_palette_of_coloured": round(sum(counts.values()) / chromatic, 3),
            "off_palette_of_coloured": round(off / chromatic, 3),
            "neutral_share": round(neutral / total, 3),
            "per_token": {k: round(v / total, 3) for k, v in counts.items()}}


# ---- assembly and checks -------------------------------------------------------------------------------

def assemble(clips, out, width=1920, height=1080, fps=24, music=None, crf=18):
    """clips: [(path, seconds)]. Trims, conforms and concatenates; one encode for the whole film."""
    need_ffmpeg()
    ins, fc = [], []
    for i, (p, sec) in enumerate(clips):
        ins += ["-i", p]
        fc.append(f"[{i}:v]trim=0:{sec},setpts=PTS-STARTPTS,scale={width}:{height}:force_original_aspect_ratio=increase,"
                  f"crop={width}:{height},fps={fps},format=yuv420p,setsar=1[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=0[v]")
    total = sum(s for _, s in clips)
    args = ["ffmpeg", "-y", "-loglevel", "error", *ins]
    maps = ["-map", "[v]"]
    if music:
        args += ["-i", music]
        fc.append(f"[{len(clips)}:a]atrim=0:{total},afade=t=out:st={max(0, total - 2)}:d=2,"
                  "loudnorm=I=-14:TP=-2:LRA=11,aresample=48000[a]")
        maps += ["-map", "[a]", "-c:a", "aac", "-b:a", "160k"]
    tmp = out.replace(".mp4", ".part.mp4")
    _run(args + ["-filter_complex", ";".join(fc), *maps, "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
                 "-movflags", "+faststart", tmp])
    os.replace(tmp, out)
    return out


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    out = {}
    for line in r.splitlines():
        s = line.strip()
        if s.startswith("I:"):
            out["integrated_lufs"] = float(s.split()[1])
        if s.startswith("Peak:"):
            out["true_peak_dbtp"] = float(s.split()[1])
    return out


def flash_check(path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "..", "scripts", "flash-check.py"), path], capture_output=True, text=True)
    return {"passes": r.returncode == 0, "report": (r.stdout + r.stderr).strip()}


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,r_frame_rate",
                        "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout or "{}")
