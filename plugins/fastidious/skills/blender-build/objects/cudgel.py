# A Westcountry cudgel (singlestick): a whole stick of ash or hazel, about 34 in long, slightly tapered,
# never perfectly straight or round, with knots where twigs were trimmed, a hand-polished grip at the
# butt and domed, worn ends showing end grain.
#
# Lies along +X, centred on the origin, resting at its lowest point. Writes per-vertex attributes for the
# material: wear (grip), knot, endgrain, t (0 butt .. 1 tip); and UVs packed for baking into a tall
# texture (body strip, two end-grain discs at the bottom).
import bpy, math, random

DEFAULTS = dict(
    length=0.87,        # metres (about 34 in)
    radius=0.0135,      # butt radius (27 mm diameter)
    taper=0.82,         # tip radius as a fraction of the butt
    bend=0.007,         # metres of sweep along the length
    oval=0.04,          # out-of-round, fraction of radius
    wobble=0.025,       # slow thickness variation along the length
    knots=6,
    knot_height=0.0022,
    grip=(0.03, 0.27),  # grip region as fractions from the butt
    rings=180, segs=40, cap_rings=8, cap_depth=0.55,
    seed=7,
    hilt=None,          # dict for a woven "pot": see _pot()
    rest=False,         # tilt so the pot's rim and the tip both touch the floor
)


def _noise1(rng, n=6, lo=0.5, hi=3.5):
    """Smooth 1-D noise from a few random sines; lo..hi is the base frequency in cycles per stick."""
    waves = [(rng.uniform(lo, hi) * (i + 1), rng.uniform(0, math.tau), rng.uniform(0.4, 1.0) / (i + 1)) for i in range(n)]
    tot = sum(a for _, _, a in waves)
    return lambda t: sum(a * math.sin(f * math.tau * t + ph) for f, ph, a in waves) / tot


def _smooth(a, b, x):
    x = max(0.0, min(1.0, (x - a) / (b - a))); return x * x * (3 - 2 * x)


POT = dict(
    from_butt=0.16,     # metres from the butt to the crown of the dome, where the stick passes through
    radius=0.066,       # a hemisphere that closes over the fist
    stakes=20, rounds=15, weaver=0.0019, stake=0.0015, rim=0.0034,
    around=112, sides=6,
    palette=('#3A2312', '#5A3A1E', '#6E4A28'),
)


def _srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def _tube(path, radii, colours, sides, closed, verts, faces, cols):
    """Sweep a small circle along a path. path: [(x, y, z)], radii and colours per point."""
    n = len(path); start = len(verts)
    for i in range(n):
        a, b = path[(i - 1) % n if closed else max(i - 1, 0)], path[(i + 1) % n if closed else min(i + 1, n - 1)]
        t = [b[k] - a[k] for k in range(3)]; tl = math.sqrt(sum(x * x for x in t)) or 1; t = [x / tl for x in t]
        up = (1, 0, 0) if abs(t[0]) < 0.8 else (0, 0, 1)
        u = [t[1] * up[2] - t[2] * up[1], t[2] * up[0] - t[0] * up[2], t[0] * up[1] - t[1] * up[0]]
        ul = math.sqrt(sum(x * x for x in u)) or 1; u = [x / ul for x in u]
        v = [t[1] * u[2] - t[2] * u[1], t[2] * u[0] - t[0] * u[2], t[0] * u[1] - t[1] * u[0]]
        for j in range(sides):
            th = j / sides * math.tau; c, s_ = math.cos(th) * radii[i], math.sin(th) * radii[i]
            verts.append(tuple(path[i][k] + u[k] * c + v[k] * s_ for k in range(3))); cols.append(colours[i])
    for i in range(n if closed else n - 1):
        i2 = (i + 1) % n
        for j in range(sides):
            j2 = (j + 1) % sides
            faces.append((start + i * sides + j, start + i * sides + j2, start + i2 * sides + j2, start + i2 * sides + j))


def _pot(p, rng, stick_r, centre):
    """The wicker pot: stakes running from the stick out to the rim, weavers going over and under them,
    a rolled rim. Dome convex toward the tip, open toward the butt, so it closes over the hand."""
    h = {**POT, **(p['hilt'] if isinstance(p['hilt'], dict) else {})}
    L, R = p['length'], h['radius']; xa = -L / 2 + h['from_butt']
    t0 = h['from_butt'] / L; cy, cz = centre(t0)
    phi0 = math.asin(min(0.9, (stick_r(t0) + 0.002) / R)); phi1 = math.radians(82)
    def surf(phi, th, off=0.0):
        rr = R + off
        return (xa - R * (1 - math.cos(phi)) + off * math.cos(phi),
                cy + rr * math.sin(phi) * math.cos(th), cz + rr * math.sin(phi) * math.sin(th))
    pal = [_srgb(c) for c in h['palette']]
    def strand_col():
        a, b = rng.choice(pal), rng.choice(pal); m = rng.random(); return [a[k] * m + b[k] * (1 - m) for k in range(3)]
    verts, faces, cols = [], [], []
    # Stakes
    for k in range(h['stakes']):
        th = k / h['stakes'] * math.tau + rng.uniform(-0.012, 0.012); base = strand_col(); pts, rad, cc = [], [], []
        for i in range(19):
            q = i / 18; phi = phi0 + (phi1 - phi0) * q
            pts.append(surf(phi, th + 0.01 * math.sin(q * 5 + k))); rad.append(h['stake'] * (1.15 - 0.2 * q)); cc.append([x * (0.72 + 0.28 * q) for x in base])
        _tube(pts, rad, cc, 5, False, verts, faces, cols)
    # Weavers: each round passes over one stake and under the next; the next round is the reverse.
    A = h['around']; nh = h['stakes'] / 2
    for r in range(h['rounds']):
        q = (r + 0.5) / h['rounds']; phi = phi0 + (phi1 - phi0) * (0.04 + 0.95 * q); base = strand_col(); pts, rad, cc = [], [], []
        wob = rng.uniform(0, math.tau)
        for i in range(A):
            th = i / A * math.tau; w = math.sin(nh * th + (r % 2) * math.pi)
            off = w * (h['stake'] + h['weaver']) * 0.92
            ph = phi + 0.006 * math.sin(th * 3 + wob)
            pts.append(surf(ph, th, off)); rad.append(h['weaver'] * rng.uniform(0.94, 1.06))
            shade = 0.62 + 0.38 * (w * 0.5 + 0.5); cc.append([x * shade for x in base])
        _tube(pts, rad, cc, h['sides'], True, verts, faces, cols)
    # Rolled rim
    base = strand_col(); pts, rad, cc = [], [], []
    for i in range(A):
        th = i / A * math.tau; pts.append(surf(phi1 + 0.02, th)); rad.append(h['rim'] * (1 + 0.1 * math.sin(th * 11))); cc.append([x * 0.9 for x in base])
    _tube(pts, rad, cc, 8, True, verts, faces, cols)
    # Binding where the stick passes through the crown
    base = strand_col()
    for b in range(5):
        x = xa + 0.002 + 0.0034 * b; rr = stick_r(t0) + 0.0016
        pts = [(x, cy + rr * math.cos(i / 36 * math.tau), cz + rr * math.sin(i / 36 * math.tau)) for i in range(36)]
        _tube(pts, [0.0018] * 36, [[c * 0.85 for c in base]] * 36, 5, True, verts, faces, cols)
    me = bpy.data.meshes.new('pot'); me.from_pydata(verts, [], faces); me.update()
    for poly in me.polygons: poly.use_smooth = True
    ca = me.color_attributes.new('Col', 'FLOAT_COLOR', 'POINT')
    ca.data.foreach_set('color', [v for c in cols for v in (c[0], c[1], c[2], 1.0)])
    ob = bpy.data.objects.new('pot', me); bpy.context.scene.collection.objects.link(ob)
    import materials
    ob.data.materials.append(materials.wicker(h))
    return ob, xa - R * (1 - math.cos(phi1)), R * math.sin(phi1) + h['rim']


def build(params):
    p = {**DEFAULTS, **params}
    rng = random.Random(p['seed'])
    L, R, N, S = p['length'], p['radius'], p['rings'], p['segs']
    # A real stick has one or two long sweeps, not a wiggle: bends stay at very low frequency.
    thick, bendy, bendz = _noise1(rng, 4), _noise1(rng, 2, 0.4, 0.9), _noise1(rng, 2, 0.4, 0.9)
    phase = _noise1(rng, 3)
    knots = [(rng.uniform(0.12, 0.95), rng.uniform(0, math.tau), rng.uniform(0.6, 1.0) * p['knot_height'], rng.uniform(0.006, 0.012)) for _ in range(p['knots'])]

    def radius(t, th):
        r = R * (1 - (1 - p['taper']) * t) * (1 + p['wobble'] * thick(t))
        r *= 1 + p['oval'] * math.cos(2 * (th + 1.3 * phase(t)))
        k = 0.0
        for tk, thk, hk, wk in knots:
            dt = (t - tk) * L / wk; dth = math.atan2(math.sin(th - thk), math.cos(th - thk)) / 0.55
            g = math.exp(-(dt * dt + dth * dth)); r += hk * g; k = max(k, min(1.0, g * 1.15))
        return r, k

    def centre(t):
        return (p['bend'] * (math.sin(math.pi * t) + 0.5 * bendy(t)), p['bend'] * 0.5 * bendz(t))

    verts, wear, knotv, endg, tv = [], [], [], [], []
    ring_r = []
    for i in range(N + 1):
        t = i / N; x = (t - 0.5) * L; cy, cz = centre(t); rr = []
        for j in range(S):
            th = j / S * math.tau; r, k = radius(t, th); rr.append(r)
            verts.append((x, cy + r * math.cos(th), cz + r * math.sin(th)))
            g0, g1 = p['grip']
            wear.append(_smooth(g0 - 0.03, g0 + 0.02, t) * (1 - _smooth(g1 - 0.04, g1 + 0.03, t)))
            knotv.append(k); endg.append(0.0); tv.append(t)
        ring_r.append(rr)
    faces, face_uv = [], []
    body_v0, body_v1 = 0.065, 0.998
    for i in range(N):
        for j in range(S):
            a, b = i * S + j, i * S + (j + 1) % S
            faces.append((a, b, b + S, a + S))
            v0 = body_v0 + (body_v1 - body_v0) * i / N; v1 = body_v0 + (body_v1 - body_v0) * (i + 1) / N
            face_uv.append(((j / S, v0), ((j + 1) / S, v0), ((j + 1) / S, v1), (j / S, v1)))

    # Domed ends. Each end's faces map into a disc at the bottom of the texture (butt left, tip right).
    def cap(end):
        i_ring = 0 if end == 0 else N; t = i_ring / N; sign = -1 if end == 0 else 1
        x_end = (t - 0.5) * L; cy, cz = centre(t)
        r_end = sum(ring_r[i_ring]) / S; depth = r_end * p['cap_depth']
        uc = (0.25 if end == 0 else 0.75, 0.031); ur = (0.23, 0.029)
        def uv_of(y, z, rad):
            return (uc[0] + ur[0] * (y - cy) / rad, uc[1] + ur[1] * (z - cz) / rad * (1 if end else -1))
        prev = list(range(i_ring * S, i_ring * S + S)); K = p['cap_rings']
        for kq in range(1, K + 1):
            phi = kq / K * (math.pi / 2)
            if kq < K:
                start = len(verts)
                for j in range(S):
                    th = j / S * math.tau; r = ring_r[i_ring][j] * math.cos(phi)
                    verts.append((x_end + sign * depth * math.sin(phi), cy + r * math.cos(th), cz + r * math.sin(th)))
                    wear.append(0.0); knotv.append(0.0); endg.append(_smooth(0.15, 0.5, kq / K)); tv.append(t)
                cur = list(range(start, start + S))
                for j in range(S):
                    a, b, c, d = prev[j], prev[(j + 1) % S], cur[(j + 1) % S], cur[j]
                    faces.append((a, b, c, d) if end else (a, d, c, b))
                    q = [verts[v] for v in ((a, b, c, d) if end else (a, d, c, b))]
                    face_uv.append(tuple(uv_of(v[1], v[2], r_end) for v in q))
                prev = cur
            else:
                pole = len(verts); verts.append((x_end + sign * depth, cy, cz))
                wear.append(0.0); knotv.append(0.0); endg.append(1.0); tv.append(t)
                for j in range(S):
                    a, b = prev[j], prev[(j + 1) % S]
                    tri = (a, b, pole) if end else (a, pole, b)
                    faces.append(tri); face_uv.append(tuple(uv_of(verts[v][1], verts[v][2], r_end) for v in tri))
    cap(0); cap(1)

    me = bpy.data.meshes.new('cudgel'); me.from_pydata(verts, [], faces); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for poly, uvs in zip(me.polygons, face_uv):
        for li, uv in zip(poly.loop_indices, uvs): uvl.data[li].uv = uv
    for poly in me.polygons: poly.use_smooth = True
    for name, data in (('wear', wear), ('knot', knotv), ('endgrain', endg), ('t', tv)):
        at = me.attributes.new(name, 'FLOAT', 'POINT'); at.data.foreach_set('value', data)
    ob = bpy.data.objects.new('cudgel', me); bpy.context.scene.collection.objects.link(ob)
    zmin = min(v[2] for v in verts)
    if p['hilt']:
        stick_r = lambda t: R * (1 - (1 - p['taper']) * t)
        pot, xr, rr = _pot(p, rng, stick_r, centre)
        pot.parent = ob
        if p['rest']:
            # Lying on a floor, the stick is propped on its pot: rim and tip touch.
            xt = L / 2; rt = stick_r(1.0); a = math.atan2(rr - rt, xt - xr)
            ob.rotation_euler.y = a
            ob.location.z = rr * math.cos(a) + xr * math.sin(a)
            return ob
        ob.location.z = 0.0
        return ob
    # Rest on the floor at z = 0.
    ob.location.z = -zmin
    return ob
