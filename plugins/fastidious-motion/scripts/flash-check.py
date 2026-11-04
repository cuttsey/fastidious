#!/usr/bin/env python3
"""
flash-check: screens a rendered video against WCAG 2.3.1, three flashes or below threshold.

General flash: a pair of opposing changes in relative luminance of 10% or more of the maximum, where the
darker state is below 0.80. Red flash: a pair of opposing transitions to or from saturated red
(R/(R+G+B) >= 0.8) that move more than 0.2 in CIE 1976 u'v' chromaticity. Either kind fails when more than
three flashes fall in any one second inside any 10 degree field, taken as a third of the frame's width
and height (WCAG's 341 x 256 at 1024 x 768), and the flashing pixels cover more than 25% of that field.

This is a screening check for the edit, not a certified test. A broadcast or regulated release still needs
a dedicated photosensitive epilepsy analyser.

Usage: python3 flash-check.py <video> [--width 192]
Exit code 1 if any second fails, so it can gate a render.
"""
import json, subprocess, sys
from collections import deque
import numpy as np

def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                          '-of', 'json', path], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)['streams'][0]; n, d = s['r_frame_rate'].split('/')
    return s['width'], s['height'], float(n) / float(d)

def main():
    path = sys.argv[1]; W = int(sys.argv[sys.argv.index('--width') + 1]) if '--width' in sys.argv else 192
    w0, h0, fps = probe(path); H = max(6, round(W * h0 / w0 / 2) * 2)
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={W}:{H}:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                            stdout=subprocess.PIPE)
    fw, fh = W // 3, H // 3; step_x, step_y = max(1, W // 12), max(1, H // 12)
    xs = list(range(0, W - fw + 1, step_x)); ys = list(range(0, H - fh + 1, step_y)); area = fw * fh
    span = int(round(fps))  # frames in one second
    ext_l = ref_uv = ref_red = dir_l = None
    hist = {k: [[deque() for _ in xs] for _ in ys] for k in ('general', 'red')}
    lastsign = {k: [[0 for _ in xs] for _ in ys] for k in ('general', 'red')}
    fails, i = [], 0
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    while True:
        buf = proc.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        s = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        lin = np.where(s <= .04045, s / 12.92, ((s + .055) / 1.055) ** 2.4)
        L = lin @ np.array([.2126, .7152, .0722], np.float32)
        XYZ = lin @ M.T.astype(np.float32); den = XYZ[..., 0] + 15 * XYZ[..., 1] + 3 * XYZ[..., 2] + 1e-9
        uv = np.stack([4 * XYZ[..., 0] / den, 9 * XYZ[..., 1] / den], -1)
        red = s[..., 0] / (s.sum(-1) + 1e-9) >= .8
        if ext_l is None:
            ext_l, dir_l, ref_uv, ref_red = L.copy(), np.zeros_like(L, np.int8), uv.copy(), red.copy()
            i += 1; continue
        # General: per-pixel state machine; a transition is a move of >= 0.1 from the last extreme, against the
        # previous direction, with the darker state below 0.8. Extremes follow the current direction.
        lo = np.minimum(L, ext_l) < .8
        up = (L - ext_l >= .1) & lo & (dir_l != 1); dn = (ext_l - L >= .1) & lo & (dir_l != -1)
        g = up | dn
        dir_l = np.where(up, 1, np.where(dn, -1, dir_l)).astype(np.int8)
        g_up, g_dn = up, dn
        ext_l = np.where(g, L, np.where((dir_l == 1) & (L > ext_l), L, np.where((dir_l == -1) & (L < ext_l), L, ext_l)))
        # Red: a move of more than 0.2 in u'v' from the last reference state, to or from saturated red.
        # Direction: towards saturated red (+1) or away from it (-1).
        r = (np.linalg.norm(uv - ref_uv, axis=-1) > .2) & (red | ref_red)
        r_up, r_dn = r & red & ~ref_red, r & ref_red & ~red
        ref_uv = np.where(r[..., None], uv, ref_uv); ref_red = np.where(r, red, ref_red)
        # A field registers a transition when more than 25% of it changes in the same direction in the same
        # frame. A flash is a pair of opposing transitions, so only a change of direction counts. Moving text
        # or patterns brighten and darken neighbouring pixels at once and do not register.
        for kind, mu, md in (('general', g_up, g_dn), ('red', r_up, r_dn)):
            Su = np.pad(mu.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
            Sd = np.pad(md.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
            box = lambda S, x, y: S[y + fh, x + fw] - S[y, x + fw] - S[y + fh, x] + S[y, x]
            for yi, y in enumerate(ys):
                for xi, x in enumerate(xs):
                    cu, cd = box(Su, x, y), box(Sd, x, y)
                    sign = 1 if cu > .25 * area and cu >= cd else -1 if cd > .25 * area else 0
                    q, last = hist[kind][yi][xi], lastsign[kind][yi][xi]
                    if sign and sign != last: q.append(i); lastsign[kind][yi][xi] = sign
                    while q and q[0] <= i - span: q.popleft()
                    if len(q) > 6:  # more than three flashes (pairs of opposing transitions) in one second
                        fails.append((kind, round(i / fps, 2)))
        i += 1
    proc.wait()
    seconds = sorted({(k, int(t)) for k, t in fails})
    if seconds:
        for k, t in seconds: print(f'FAIL {k} flash: more than three flashes in the second starting {t}s')
        print(f'flash-check: {path} fails WCAG 2.3.1 ({len(seconds)} second(s) affected, {i} frames at {fps:g}fps)')
        sys.exit(1)
    print(f'flash-check: {path} passes ({i} frames at {fps:g}fps)')

if __name__ == '__main__':
    main()
