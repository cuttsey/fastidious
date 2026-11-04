# Materials. Two kinds:
#   wood_stick  procedural wood for turned or whole sticks: long grain streaks, fibres, knots, end grain, a hand-polished grip.
#               Reads the mesh attributes a builder writes: wear, knot, endgrain (0..1 per vertex).
#   pbr         image maps from a folder (Poly Haven / ambientCG naming): diff/albedo/color, rough, nor_gl/normal, disp.
# Every material is built in nodes from the spec so it can be rebuilt and, for glTF, baked to textures.
import bpy, os, glob


def _hex(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b), 1.0)


class G:
    """Tiny node-graph helper."""
    def __init__(self, mat):
        mat.use_nodes = True; self.nt = mat.node_tree; self.nt.nodes.clear(); self.x = 0
    def n(self, kind, **kw):
        node = self.nt.nodes.new(kind); node.location = (self.x, 0); self.x += 40
        for k, v in kw.items():
            if hasattr(node, k): setattr(node, k, v)
            else: self.set(node, k, v)
        return node
    def set(self, node, name, v):
        for s in node.inputs:
            if s.name == name and s.enabled is not False:
                s.default_value = v; return True
        return False
    def link(self, a, b):
        self.nt.links.new(a, b)


def _bsdf_in(bsdf, *names):
    for n in names:
        if n in bsdf.inputs: return bsdf.inputs[n]
    return None


def _ramp(g, stops):
    r = g.n('ShaderNodeValToRGB'); el = r.color_ramp.elements
    while len(el) > 1: el.remove(el[-1])
    el[0].position, el[0].color = stops[0][0], _hex(stops[0][1])
    for pos, col in stops[1:]:
        e = el.new(pos); e.color = _hex(col)
    return r


def _attr(g, name):
    a = g.n('ShaderNodeAttribute'); a.attribute_name = name; return a.outputs['Fac']


def _mix_col(g, fac, a, b, blend='MIX'):
    m = g.n('ShaderNodeMix'); m.data_type = 'RGBA'; m.blend_type = blend
    g.link(fac, m.inputs[0]) if not isinstance(fac, float) else setattr(m.inputs[0], 'default_value', fac)
    for sock, val in ((m.inputs[6], a), (m.inputs[7], b)):
        if isinstance(val, tuple): sock.default_value = val
        else: g.link(val, sock)
    return m.outputs[2]


def _mix_f(g, fac, a, b):
    m = g.n('ShaderNodeMix'); m.data_type = 'FLOAT'
    g.link(fac, m.inputs[0])
    for sock, val in ((m.inputs[2], a), (m.inputs[3], b)):
        if isinstance(val, (int, float)): sock.default_value = val
        else: g.link(val, sock)
    return m.outputs[0]


def wood_stick(p):
    mat = bpy.data.materials.new(p.get('name', 'wood')); g = G(mat)
    out = g.n('ShaderNodeOutputMaterial'); bsdf = g.n('ShaderNodeBsdfPrincipled')
    g.link(bsdf.outputs[0], out.inputs['Surface'])
    tc = g.n('ShaderNodeTexCoord')
    # Grain runs along the object's X axis (builders lay sticks along X): stretch noise along X.
    def stretched(sx, sy):
        m = g.n('ShaderNodeMapping'); m.inputs['Scale'].default_value = (sx, sy, sy); g.link(tc.outputs['Object'], m.inputs['Vector']); return m.outputs['Vector']
    gs = p.get('grain_scale', 1.0)
    streak = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(streak, 'Scale', 1.0); g.set(streak, 'Detail', 6.0); g.set(streak, 'Roughness', 0.62); g.set(streak, 'Distortion', 0.35)
    g.link(stretched(3 * gs, 70 * gs), streak.inputs['Vector'])
    fibre = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(fibre, 'Scale', 1.0); g.set(fibre, 'Detail', 10.0); g.set(fibre, 'Roughness', 0.7)
    g.link(stretched(14 * gs, 900 * gs), fibre.inputs['Vector'])
    # Large scale: the stain took unevenly, so broad patches run darker or lighter along the stick.
    blotch = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(blotch, 'Scale', 1.0); g.set(blotch, 'Detail', 4.0); g.set(blotch, 'Roughness', 0.55)
    g.link(stretched(7 * gs, 45 * gs), blotch.inputs['Vector'])
    pal = p.get('palette', ['#24110A', '#4A2412', '#7A4220', '#A0612F'])
    ramp = _ramp(g, [(0.30, pal[0]), (0.45, pal[1]), (0.58, pal[2]), (0.72, pal[3])])
    # Combine streaks with fibres so colour has both long figure and fine fibre.
    mixv = g.n('ShaderNodeMath', operation='MULTIPLY_ADD'); g.link(fibre.outputs['Fac'], mixv.inputs[0]); mixv.inputs[1].default_value = p.get('fibre_contrast', 0.6); g.link(streak.outputs['Fac'], mixv.inputs[2])
    sub = g.n('ShaderNodeMath', operation='SUBTRACT'); g.link(mixv.outputs[0], sub.inputs[0]); sub.inputs[1].default_value = 0.3
    g.link(sub.outputs[0], ramp.inputs['Fac'])
    bl = g.n('ShaderNodeMapRange'); g.link(blotch.outputs['Fac'], bl.inputs['Value']); bl.inputs['From Min'].default_value = 0.35; bl.inputs['From Max'].default_value = 0.65
    bl.inputs['To Min'].default_value = 0.0; bl.inputs['To Max'].default_value = p.get('mottle', 0.42)
    col = _mix_col(g, bl.outputs['Result'], ramp.outputs['Color'], _hex(p.get('stain', '#2A140A')), blend='MULTIPLY')
    # Knots: darker, denser.
    col = _mix_col(g, _mix_f(g, _attr(g, 'knot'), 0.0, 0.7), col, _hex(p.get('knot', '#2A140A')))
    # End grain: growth rings around the stick's axis, lighter where the cut is exposed.
    # Rings wander and the pith sits off-centre; a clean bullseye is the tell of a CG log.
    rings = g.n('ShaderNodeTexWave', wave_type='RINGS', rings_direction='X'); g.set(rings, 'Scale', p.get('ring_scale', 240.0)); g.set(rings, 'Distortion', 0.0)
    wander = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(wander, 'Scale', 55.0); g.set(wander, 'Detail', 2.0); g.set(wander, 'Roughness', 0.5)
    g.link(tc.outputs['Object'], wander.inputs['Vector'])
    wscale = g.n('ShaderNodeVectorMath', operation='SCALE'); g.link(wander.outputs['Color'], wscale.inputs[0]); g.set(wscale, 'Scale', p.get('ring_wander', 0.0075))
    offs = g.n('ShaderNodeVectorMath', operation='ADD'); g.link(tc.outputs['Object'], offs.inputs[0]); g.link(wscale.outputs[0], offs.inputs[1])
    pith = g.n('ShaderNodeMapping'); pith.inputs['Location'].default_value = (0.0, 0.0065, -0.0045); g.link(offs.outputs[0], pith.inputs['Vector'])
    g.link(pith.outputs['Vector'], rings.inputs['Vector'])
    rcol = _ramp(g, [(0.1, p.get('endgrain_dark', '#40281A')), (1.0, p.get('endgrain_light', '#54351F'))])
    g.link(rings.outputs['Fac'], rcol.inputs['Fac'])
    col = _mix_col(g, _attr(g, 'endgrain'), col, rcol.outputs['Color'])
    # Grip: hand oil darkens and polishes.
    wear = _attr(g, 'wear')
    col = _mix_col(g, _mix_f(g, wear, 0.0, p.get('grip_darken', 0.35)), col, _hex('#1A0C06'), blend='MULTIPLY')
    g.link(col, bsdf.inputs['Base Color'])
    # Roughness: varied, lower on the grip, higher on the end grain.
    rvar = g.n('ShaderNodeMapRange'); g.link(streak.outputs['Fac'], rvar.inputs['Value'])
    rvar.inputs['To Min'].default_value = p.get('roughness', 0.42) - 0.08; rvar.inputs['To Max'].default_value = p.get('roughness', 0.42) + 0.1
    rough = _mix_f(g, wear, rvar.outputs['Result'], p.get('grip_roughness', 0.26))
    rough = _mix_f(g, _attr(g, 'endgrain'), rough, 0.72)
    g.link(rough, bsdf.inputs['Roughness'])
    # Surface relief: fibres, small dents from use.
    dents = g.n('ShaderNodeTexVoronoi'); g.set(dents, 'Scale', p.get('dent_scale', 160.0)); g.set(dents, 'Randomness', 1.0)
    g.link(tc.outputs['Object'], dents.inputs['Vector'])
    dm = g.n('ShaderNodeMapRange'); g.link(dents.outputs['Distance'], dm.inputs['Value']); dm.inputs['From Max'].default_value = 0.35; dm.inputs['To Min'].default_value = -1; dm.inputs['To Max'].default_value = 0
    dclamp = g.n('ShaderNodeMath', operation='MULTIPLY'); g.link(dm.outputs['Result'], dclamp.inputs[0]); dclamp.inputs[1].default_value = p.get('dents', 0.25)
    h = g.n('ShaderNodeMath', operation='ADD'); g.link(fibre.outputs['Fac'], h.inputs[0]); g.link(dclamp.outputs[0], h.inputs[1])
    bump = g.n('ShaderNodeBump'); g.set(bump, 'Strength', p.get('bump', 0.55)); g.set(bump, 'Distance', 0.0004)
    g.link(h.outputs[0], bump.inputs['Height']); g.link(bump.outputs['Normal'], bsdf.inputs['Normal'])
    spec = _bsdf_in(bsdf, 'Specular IOR Level', 'Specular')
    if spec: spec.default_value = p.get('specular', 0.4)
    # Oiled finish: a thin coat.
    cw = _bsdf_in(bsdf, 'Coat Weight', 'Clearcoat')
    if cw: cw.default_value = p.get('coat', 0.12)
    cr = _bsdf_in(bsdf, 'Coat Roughness', 'Clearcoat Roughness')
    if cr: cr.default_value = p.get('coat_roughness', 0.35)
    return mat


def pbr(p, resolve):
    """Image-based PBR from a folder of maps (Poly Haven / ambientCG names). Box-projected in object space unless uv=True."""
    folder = resolve(p['folder']); mat = bpy.data.materials.new(p.get('name', os.path.basename(folder))); g = G(mat)
    out = g.n('ShaderNodeOutputMaterial'); bsdf = g.n('ShaderNodeBsdfPrincipled'); g.link(bsdf.outputs[0], out.inputs['Surface'])
    tc = g.n('ShaderNodeTexCoord'); mp = g.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (p.get('scale', 1.0),) * 3
    g.link(tc.outputs['UV' if p.get('uv') else 'Object'], mp.inputs['Vector'])
    def find(*keys):
        for k in keys:
            hits = sorted(glob.glob(os.path.join(folder, f'*{k}*')))
            if hits: return hits[0]
    def tex(path, colour):
        t = g.n('ShaderNodeTexImage'); t.image = bpy.data.images.load(path)
        if not colour: t.image.colorspace_settings.name = 'Non-Color'
        if not p.get('uv'): t.projection = 'BOX'; t.projection_blend = 0.25
        g.link(mp.outputs['Vector'], t.inputs['Vector']); return t
    if (d := find('diff', 'albedo', 'Color', 'col')): g.link(tex(d, True).outputs['Color'], bsdf.inputs['Base Color'])
    if (r := find('rough', 'Roughness')): g.link(tex(r, False).outputs['Color'], bsdf.inputs['Roughness'])
    if (n := find('nor_gl', 'NormalGL', 'normal')):
        nm = g.n('ShaderNodeNormalMap'); g.link(tex(n, False).outputs['Color'], nm.inputs['Color']); g.link(nm.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def steel(p):
    """Hand-finished steel with a used, oiled patina: not mirror polish, not museum rust. Long draw-filing along the blade, broad darker
    patches, bright sharpened edges, and a copper-alloy collar. Reads the attributes edge, ridge, latten."""
    mat = bpy.data.materials.new(p.get('name', 'steel')); g = G(mat)
    out = g.n('ShaderNodeOutputMaterial'); bsdf = g.n('ShaderNodeBsdfPrincipled'); g.link(bsdf.outputs[0], out.inputs['Surface'])
    tc = g.n('ShaderNodeTexCoord')
    def stretched(sx, sy):
        m = g.n('ShaderNodeMapping'); m.inputs['Scale'].default_value = (sx, sy, sy); g.link(tc.outputs['Object'], m.inputs['Vector']); return m.outputs['Vector']
    def noise(vec, detail=6.0, rough=0.6):
        n = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(n, 'Scale', 1.0); g.set(n, 'Detail', detail); g.set(n, 'Roughness', rough); g.link(vec, n.inputs['Vector']); return n.outputs['Fac']
    patch, mottle, file_, pits = noise(stretched(5, 22), 5.0), noise(stretched(60, 110), 6.0), noise(stretched(8, 900), 8.0, 0.65), noise(stretched(520, 520), 4.0, 0.5)
    ramp = _ramp(g, p.get('stops') and [tuple(x) for x in p['stops']] or [(0.34, '#2C2B28'), (0.5, '#55544F'), (0.66, '#7A7A75')])
    mix = g.n('ShaderNodeMath', operation='MULTIPLY_ADD'); g.link(mottle, mix.inputs[0]); mix.inputs[1].default_value = 0.5; g.link(patch, mix.inputs[2])
    sub = g.n('ShaderNodeMath', operation='SUBTRACT'); g.link(mix.outputs[0], sub.inputs[0]); sub.inputs[1].default_value = 0.25
    g.link(sub.outputs[0], ramp.inputs['Fac'])
    edge, ridge, latten = _attr(g, 'edge'), _attr(g, 'ridge'), _attr(g, 'latten')
    col = _mix_col(g, _mix_f(g, edge, 0.0, 0.85), ramp.outputs['Color'], _hex(p.get('edge_col', '#C9CAC6')))
    col = _mix_col(g, _mix_f(g, ridge, 0.0, 0.35), col, _hex('#A8A8A3'))
    col = _mix_col(g, latten, col, _hex(p.get('latten_col', '#B08D4A')))
    g.link(col, bsdf.inputs['Base Color'])
    bsdf.inputs['Metallic'].default_value = 1.0
    rr = g.n('ShaderNodeMapRange'); g.link(mottle, rr.inputs['Value']); rr.inputs['From Min'].default_value = 0.3; rr.inputs['From Max'].default_value = 0.7
    rr.inputs['To Min'].default_value = p.get('roughness', 0.3); rr.inputs['To Max'].default_value = p.get('roughness', 0.3) + 0.22
    rough = _mix_f(g, edge, rr.outputs['Result'], 0.24)
    g.link(rough, bsdf.inputs['Roughness'])
    h = g.n('ShaderNodeMath', operation='MULTIPLY_ADD'); g.link(file_, h.inputs[0]); h.inputs[1].default_value = 0.6; g.link(pits, h.inputs[2])
    bump = g.n('ShaderNodeBump'); g.set(bump, 'Strength', p.get('bump', 0.3)); g.set(bump, 'Distance', 0.0003)
    g.link(h.outputs[0], bump.inputs['Height']); g.link(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def leather(p):
    """Dark, hand-worn leather: fine grain, darker and shinier where it's held."""
    mat = bpy.data.materials.new(p.get('name', 'leather')); g = G(mat)
    out = g.n('ShaderNodeOutputMaterial'); bsdf = g.n('ShaderNodeBsdfPrincipled'); g.link(bsdf.outputs[0], out.inputs['Surface'])
    tc = g.n('ShaderNodeTexCoord')
    big = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(big, 'Scale', 340.0); g.set(big, 'Detail', 6.0); g.set(big, 'Roughness', 0.6); g.link(tc.outputs['Object'], big.inputs['Vector'])
    ramp = _ramp(g, [(0.3, p.get('dark', '#1A0F09')), (0.7, p.get('light', '#3A2315'))]); g.link(big.outputs['Fac'], ramp.inputs['Fac'])
    g.link(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    rr = g.n('ShaderNodeMapRange'); g.link(big.outputs['Fac'], rr.inputs['Value']); rr.inputs['To Min'].default_value = 0.36; rr.inputs['To Max'].default_value = 0.62; g.link(rr.outputs['Result'], bsdf.inputs['Roughness'])
    v = g.n('ShaderNodeTexVoronoi'); g.set(v, 'Scale', 1100.0); g.link(tc.outputs['Object'], v.inputs['Vector'])
    bump = g.n('ShaderNodeBump'); g.set(bump, 'Strength', 0.3); g.set(bump, 'Distance', 0.0003); g.link(v.outputs['Distance'], bump.inputs['Height']); g.link(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def wicker(h):
    """Willow rods. Base colour comes straight from the strand's colour attribute, so it survives glTF export;
    the fine fibre bump is render-only."""
    mat = bpy.data.materials.new('wicker'); g = G(mat)
    out = g.n('ShaderNodeOutputMaterial'); bsdf = g.n('ShaderNodeBsdfPrincipled'); g.link(bsdf.outputs[0], out.inputs['Surface'])
    ca = g.n('ShaderNodeVertexColor'); ca.layer_name = 'Col'
    g.link(ca.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = h.get('roughness', 0.58)
    spec = _bsdf_in(bsdf, 'Specular IOR Level', 'Specular')
    if spec: spec.default_value = 0.35
    tc = g.n('ShaderNodeTexCoord'); nz = g.n('ShaderNodeTexNoise', noise_dimensions='3D'); g.set(nz, 'Scale', 900.0); g.set(nz, 'Detail', 5.0); g.set(nz, 'Roughness', 0.6)
    g.link(tc.outputs['Object'], nz.inputs['Vector'])
    bump = g.n('ShaderNodeBump'); g.set(bump, 'Strength', 0.25); g.set(bump, 'Distance', 0.0003)
    g.link(nz.outputs['Fac'], bump.inputs['Height']); g.link(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def build(spec, resolve):
    t = spec.get('type', 'wood_stick')
    if t == 'wood_stick': return wood_stick(spec)
    if t == 'pbr': return pbr(spec, resolve)
    if t == 'steel': return steel(spec)
    raise ValueError('unknown material type ' + t)
