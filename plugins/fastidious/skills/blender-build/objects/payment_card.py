# A payment card to ISO/IEC 7810 ID-1: 85.60 x 53.98 x 0.76 mm, corner radius 3.18 mm. Stands upright (portrait by default) on z = 0,
# front facing -Y. The artwork is an atlas: front on the left half, back on the right. One material: base colour, plus a
# glTF-style metal/rough map (G rough, B metal), so foil really is metal and it exports without baking. Scale is real, in metres.
import bpy, math, os

DEFAULTS = dict(w=0.05398, h=0.0856, t=0.00076, r=0.00318, bevel=0.00012, corner_segs=10, portrait=True, centred=False, art='', mr='', rough=0.42)

def _outline(w, h, r, segs):
    pts = []
    for cx, cy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
        for i in range(segs + 1):
            a = math.radians(a0 + 90 * i / segs); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def build(params):
    p = {**DEFAULTS, **params}; w, h, t, b = p['w'], p['h'], p['t'], p['bevel']
    verts, faces, uvs = [], [], []
    out = _outline(w, h, p['r'], p['corner_segs']); inner = _outline(w - 2*b, h - 2*b, p['r'] - b, p['corner_segs']); n = len(out)
    def uv_f(x, z): return (0.5 * (x / w + 0.5), z / h + 0.5)            # front: left half of the atlas
    def uv_b(x, z): return (0.5 + 0.5 * (0.5 - x / w), z / h + 0.5)      # back: right half, mirrored so it reads from behind
    # y: -t/2 is the front. rings: front flat, front edge, back edge, back flat
    rings = [(inner, -t/2, 'f'), (out, -t/2 + b, 'f'), (out, t/2 - b, 'b'), (inner, t/2, 'b')]
    start = []
    for loop, y, _ in rings:
        start.append(len(verts))
        for x, z in loop: verts.append((x, y, z))
    ring_uv = lambda ri, i: (uv_f if rings[ri][2] == 'f' else uv_b)(rings[ri][0][i][0], rings[ri][0][i][1])
    for ri in range(3):
        for i in range(n):
            j = (i + 1) % n; a, b_, c, d = start[ri]+i, start[ri]+j, start[ri+1]+j, start[ri+1]+i
            faces.append((a, b_, c, d)); uvs.append((ring_uv(ri, i), ring_uv(ri, j), ring_uv(ri+1, j), ring_uv(ri+1, i)))
    faces.append(tuple(start[0] + i for i in range(n))); uvs.append(tuple(ring_uv(0, i) for i in range(n)))
    faces.append(tuple(start[3] + i for i in reversed(range(n)))); uvs.append(tuple(ring_uv(3, i) for i in reversed(range(n))))
    me = bpy.data.meshes.new('card'); me.from_pydata(verts, [], faces); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for poly, u in zip(me.polygons, uvs):
        poly.use_smooth = False
        for li, uv in zip(poly.loop_indices, u): uvl.data[li].uv = uv
    me.validate(); 
    ob = bpy.data.objects.new('card', me); bpy.context.scene.collection.objects.link(ob)
    # Material: base colour and metal/rough images
    mat = bpy.data.materials.new('card'); mat.use_nodes = True; nt = mat.node_tree; bsdf = nt.nodes['Principled BSDF']
    t1 = nt.nodes.new('ShaderNodeTexImage'); t1.image = bpy.data.images.load(p['art'])
    nt.links.new(t1.outputs['Color'], bsdf.inputs['Base Color'])
    t2 = nt.nodes.new('ShaderNodeTexImage'); t2.image = bpy.data.images.load(p['mr']); t2.image.colorspace_settings.name = 'Non-Color'
    sep = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(t2.outputs['Color'], sep.inputs[0])
    nt.links.new(sep.outputs['Green'], bsdf.inputs['Roughness']); nt.links.new(sep.outputs['Blue'], bsdf.inputs['Metallic'])
    ob.data.materials.append(mat)
    ob.location.z = 0 if p['centred'] else h / 2   # centred: for the web, turning about its own middle
    if not p['portrait']: ob.rotation_euler.y = math.radians(90); ob.location.z = w / 2
    return ob
