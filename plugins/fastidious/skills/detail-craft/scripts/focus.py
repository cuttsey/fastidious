"""Suggest a focal crop (CSS object-position) for an image filling a frame of a given aspect ratio.

Usage: python3 focus.py <image> --ratio 4:3 [--preview out.jpg] [--bias 0.35]
Scores every crop window of the frame's ratio by detail (edge energy), lightly pulled toward the centre,
and prints the CSS object-position, the share of the picture kept, and Plan A or Plan B advice.
Always look at the preview: the script finds detail, a designer decides what matters (faces, hands, the action).
"""
import sys
from PIL import Image, ImageFilter, ImageOps
a = sys.argv[1:]
def opt(k, d=None):
    return a[a.index('--' + k) + 1] if '--' + k in a else d
src = Image.open(a[0]); rw, rh = map(float, opt('ratio', '4:3').split(':')); R = rw / rh
bias = float(opt('bias', 0.35))
has_alpha = src.mode in ('RGBA', 'LA') and src.getchannel('A').getextrema()[0] < 250
im = src.convert('L'); W, H = im.size; S = 160 / max(W, H); sm = im.resize((max(1, int(W * S)), max(1, int(H * S))))
E = sm.filter(ImageFilter.FIND_EDGES); px = E.load(); w, h = sm.size
if W / H > R: cw, ch = int(round(h * R)), h
else: cw, ch = w, int(round(w / R))
best, bx, by = -1, 0, 0
for y in range(0, h - ch + 1):
    for x in range(0, w - cw + 1):
        s = sum(px[i, j] for j in range(y, y + ch, 2) for i in range(x, x + cw, 2))
        cxn = ((x + cw / 2) / w - .5); cyn = ((y + ch / 2) / h - .5)
        s *= 1 - bias * (cxn * cxn + cyn * cyn) * 4
        if s > best: best, bx, by = s, x, y
posx = 50 if w == cw else round(100 * bx / (w - cw)); posy = 50 if h == ch else round(100 * by / (h - ch))
kept = (cw * ch) / (w * h)
plan = 'B (matte): transparent cut-out' if has_alpha else ('A (cover)' if kept >= 0.45 else 'B (matte) unless the crop still tells the story')
print(f'object-position: {posx}% {posy}%;  kept {kept:.0%} of the picture;  plan {plan}')
if opt('preview'):
    full = src.convert('RGB'); k = W / w
    full.crop((int(bx * k), int(by * k), int((bx + cw) * k), int((by + ch) * k))).save(opt('preview'), quality=85)
