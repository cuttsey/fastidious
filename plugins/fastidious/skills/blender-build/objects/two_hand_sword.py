# An English two-hand sword, built to the measurements of the Met's example, ca. 1400-50 (2023.580.1):
# 1461 mm overall, blade 1099 mm, guard 292 mm wide. A flattened-diamond blade with a central ridge, a straight rod guard
# swelling at the centre and ending in knobs, a faceted pear-shaped pommel on a copper-alloy collar. The original has lost its grip;
# the leather-over-wood grip here is a reconstruction.
#
# Lies along +X with the point at +X and the blade flat, centred on the origin. Parts: 'steel' (blade, guard, pommel, collar; the root
# object) and a child 'grip'. Both have UVs laid out for baking, and attributes the materials read: edge, ridge, latten.
import bpy, math, random

DEFAULTS = dict(
    overall=1.461, blade=1.099, guard=0.292, blade_w=0.054, blade_t=0.0105, guard_r=0.0072, knob_r=0.0125, centre_r=0.0125,
    grip_len=0.250, grip_w=0.0165, grip_t=0.0125, pommel_len=0.082, pommel_w=0.0215, collar_len=0.009, collar_r=0.0125,
    rest=False, seed=11,
)

def _smooth(a, b, x):
    x = max(0.0, min(1.0, (x - a) / (b - a))); return x * x * (3 - 2 * x)

class M:
    """Mesh under construction: verts, faces, per-face-loop UVs, per-vertex attributes."""
    def __init__(self, attrs): self.v, self.f, self.uv, self.flat, self.a = [], [], [], [], {k: [] for k in attrs}
    def vert(self, p, **at):
        self.v.append(p)
        for k in self.a: self.a[k].append(at.get(k, 0.0))
        return len(self.v) - 1
    def quad(self, a, b, c, d, uvs, flat=False): self.f.append((a, b, c, d)); self.uv.append(uvs); self.flat.append(flat)
    def tri(self, a, b, c, uvs, flat=False): self.f.append((a, b, c)); self.uv.append(uvs); self.flat.append(flat)
    def finish(self, name):
        me = bpy.data.meshes.new(name); me.from_pydata(self.v, [], self.f); me.update()
        uvl = me.uv_layers.new(name='UVMap')
        for poly, uvs, fl in zip(me.polygons, self.uv, self.flat):
            poly.use_smooth = not fl
            for li, uv in zip(poly.loop_indices, uvs): uvl.data[li].uv = uv
        for k, data in self.a.items():
            me.attributes.new(k, 'FLOAT', 'POINT').data.foreach_set('value', data)
        ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob

def _loft(m, xs, ring, n, rect, closed=True, flat=False, at=None):
    """Sweep a ring of n points along xs. ring(i, j) -> (x, y, z); rect = (u0, v0, u1, v1) in the atlas."""
    u0, v0, u1, v1 = rect; start = len(m.v); N = len(xs)
    for i in range(N):
        for j in range(n): m.vert(ring(i, j), **(at(i, j) if at else {}))
    for i in range(N - 1):
        va, vb = v0 + (v1 - v0) * i / (N - 1), v0 + (v1 - v0) * (i + 1) / (N - 1)
        for j in range(n if closed else n - 1):
            j2 = (j + 1) % n; ua, ub = u0 + (u1 - u0) * j / n, u0 + (u1 - u0) * (j + 1) / n
            a, b, c, d = start + i * n + j, start + i * n + j2, start + (i + 1) * n + j2, start + (i + 1) * n + j
            m.quad(a, b, c, d, ((ua, va), (ub, va), (ub, vb), (ua, vb)), flat)
    return start

def build(params):
    p = {**DEFAULTS, **params}; rng = random.Random(p['seed'])
    L, BL = p['overall'], p['blade']; x_guard = L / 2 - BL; x_tip = L / 2
    x_collar = x_guard - p['grip_len'] - 0.012; x_butt = -L / 2
    w0, t0 = p['blade_w'] / 2, p['blade_t'] / 2
    wob = [(rng.uniform(1.2, 3.4), rng.uniform(0, math.tau)) for _ in range(3)]
    def profile(s):
        # s 0 at the guard, 1 at the point: a straight, slightly convex taper, like the photographs.
        w = w0 * (1 - s) ** 0.9 * (1 + 0.012 * sum(math.sin(f * math.tau * s + ph) for f, ph in wob) / 3)
        t = t0 * (1 - s) ** 0.72 + 0.0002
        return max(w, 0.0004), t
    m = M(['edge', 'ridge', 'latten'])
    # --- Blade: four separate faces, so the ridge and edges stay crisp. Each face: ridge to edge, slightly hollow.
    S = 160; xs = [x_guard + BL * ((i / S) ** 1.0) for i in range(S + 1)]; cols = 7
    # atlas: faces in u 0..0.40 (0.10 each), v 0..1 along the blade
    for face, (sy, sz) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        rev = (sy * sz) < 0
        def ring(i, j):
            s = i / S; w, t = profile(s); q = j / (cols - 1)
            hollow = 1 - 0.14 * math.sin(q * math.pi)         # very slightly hollow ground
            # a soft, hand-filed ridge: don't quite meet at a line
            y = sy * (w * q + 0.0003 * (1 - q)); z = sz * (t * (1 - q) * hollow + 0.0002 * q)
            return (xs[i], y, z)
        def at(i, j):
            q = j / (cols - 1); return {'edge': _smooth(0.72, 1.0, q), 'ridge': _smooth(0.22, 0.0, q)}
        start = len(m.v)
        for i in range(S + 1):
            for j in range(cols): m.vert(ring(i, j), **at(i, j))
        u0 = face * 0.10; 
        for i in range(S):
            for j in range(cols - 1):
                a, b, c, d = start + i * cols + j, start + i * cols + j + 1, start + (i + 1) * cols + j + 1, start + (i + 1) * cols + j
                uv = ((u0 + 0.095 * j / (cols - 1), i / S), (u0 + 0.095 * (j + 1) / (cols - 1), i / S), (u0 + 0.095 * (j + 1) / (cols - 1), (i + 1) / S), (u0 + 0.095 * j / (cols - 1), (i + 1) / S))
                if rev: m.quad(a, b, c, d, uv)
                else: m.quad(a, d, c, b, (uv[0], uv[3], uv[2], uv[1]))
    # --- Guard: a rod along Y, swelling at the centre, knobs at the ends.
    G = p['guard'] / 2; n = 14; steps = 72; ys = [-G + 2 * G * i / steps for i in range(steps + 1)]
    def gr(y):
        a = abs(y); r = p['guard_r'] * (1 + 0.16 * (1 - a / G))
        r = max(r, p['centre_r'] * math.exp(-(a / 0.026) ** 2))
        d = (G - p['knob_r'] - a) / p['knob_r']
        if d < 1.0:
            neck = 0.82 * p['guard_r'] if d > 0.6 else 0
            rk = p['knob_r'] * math.sqrt(max(0.0, 1 - min(1.0, abs(min(d, 0) + 0.0) ) ** 2)) if d <= 0 else 0
            rk = p['knob_r'] * math.sqrt(max(0.001, 1 - (min(0.0, d) ** 2))) if d <= 0 else max(p['knob_r'] * (1 - d) ** 1.2, 0)
            r = max(r * (0.9 if 0.0 < d else 1), rk)
        return r
    def guard_ring(i, j):
        th = j / n * math.tau; r = gr(ys[i]); return (x_guard - 0.002 + r * 0.92 * math.cos(th), ys[i], r * math.sin(th))
    _loft(m, ys, guard_ring, n, (0.42, 0.0, 0.62, 0.30))
    for end, u in ((0, 0.42), (steps, 0.42)):   # close the knobs
        c = m.vert((x_guard - 0.002, ys[end], 0.0)); base = len(m.v) - 1 - (steps + 1) * n + end * n
        for j in range(n):
            a, b = base + j, base + (j + 1) % n
            uvp = (0.52, 0.0 if end == 0 else 0.30)
            if end == 0: m.tri(a, c, b, (uvp, uvp, uvp))
            else: m.tri(a, b, c, (uvp, uvp, uvp))
    # --- Collar (copper alloy) and pommel: faceted, pear-shaped, eight sides, flat shaded.
    n = 8; rows = 22; px = [x_collar - p['collar_len'] - p['pommel_len'] * i / rows for i in range(rows + 1)]
    def pr(q):
        # q 0 at the neck, 1 at the crown. Narrow neck, widest about two-thirds up, then a shallow faceted dome.
        widest = p['pommel_w']; neck = 0.56 * widest
        if q < 0.68: return neck + (widest - neck) * math.sin(q / 0.68 * math.pi / 2) ** 1.25
        return widest * math.cos((q - 0.68) / 0.32 * math.pi / 2) ** 0.55
    # Each facet is its own strip: crisp between facets, smooth along the pear's curve.
    for f in range(n):
        def pom_ring(i, j, f=f):
            th = (f + j + 0.5) / n * math.tau; r = max(pr(i / rows), 0.0012); return (px[i], r * math.cos(th), r * math.sin(th) * 0.82)
        u0 = 0.64 + 0.34 * f / n
        _loft(m, px, pom_ring, 2, (u0, 0.0, u0 + 0.34 / n * 2, 0.12), closed=False)
    # Tang end of the collar and its ring
    n = 16; rows = 8; cx = [x_collar - p['collar_len'] * i / rows for i in range(rows + 1)]
    def col_ring(i, j):
        th = j / n * math.tau; q = i / rows; r = p['collar_r'] * (0.86 + 0.14 * math.sin(q * math.pi)); return (cx[i], r * math.cos(th) * 1.05, r * math.sin(th) * 0.85)
    _loft(m, cx, col_ring, n, (0.64, 0.14, 0.98, 0.17), at=lambda i, j: {'latten': 1.0})
    ob = m.finish('steel')
    # --- Grip: a separate part, leather over wood, on a tapered oval, swelling a little in the middle.
    g = M(['wrap']); n = 28; rows = 90; gx = [x_guard - 0.008 - (p['grip_len'] + 0.004) * i / rows for i in range(rows + 1)]
    def grip_ring(i, j):
        q = i / rows; th = j / n * math.tau
        sw = 1 + 0.10 * math.sin(q * math.pi) - 0.14 * q
        # a slight lump every spiral turn of the leather seam
        seam = 0.0005 * max(0.0, math.cos(th - q * math.tau * 3)) ** 40
        return (gx[i], (p['grip_w'] * sw + seam) * math.cos(th), (p['grip_t'] * sw + seam) * math.sin(th))
    _loft(g, gx, grip_ring, n, (0.0, 0.0, 1.0, 1.0))
    grip = g.finish('grip'); grip.parent = ob
    if p['rest']:
        # On a floor: it lies flat on the guard's knob and the point.
        a = math.atan2(p['knob_r'] - 0.0004, x_tip - x_guard)
        ob.rotation_euler.y = a; ob.location.z = p['knob_r'] + x_guard * math.sin(a)
    return ob
