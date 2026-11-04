# glTF export. Procedural shaders do not survive export, so the material is first baked (Cycles) to
# base colour, roughness and tangent-space normal maps on the builder's UVs, then exported as a
# compressed GLB (Draco geometry, WebP textures where the exporter supports it).
import bpy, os


def _bake_image(name, w, h, colour):
    img = bpy.data.images.new(name, w, h, alpha=False, float_buffer=False)
    if not colour: img.colorspace_settings.name = 'Non-Color'
    return img


def bake(obj, size, samples=16):
    sc = bpy.context.scene
    prev_engine = sc.render.engine
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = False
    mat = obj.active_material; nt = mat.node_tree
    w, h = size
    maps = {}
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active = obj
    bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    for key, btype, colour in (('basecolor', 'EMIT', True), ('roughness', 'ROUGHNESS', False), ('normal', 'NORMAL', False)):
        img = _bake_image(f'{obj.name}_{key}', w, h, colour)
        node = nt.nodes.new('ShaderNodeTexImage'); node.image = img
        for n in nt.nodes: n.select = False
        node.select = True; nt.nodes.active = node
        kw = {'type': btype, 'margin': 8}
        if btype == 'NORMAL': kw['normal_space'] = 'TANGENT'
        em = None
        if btype == 'EMIT':
            # Bake base colour through emission: a diffuse bake is black on metal.
            em = nt.nodes.new('ShaderNodeEmission'); src = bsdf.inputs['Base Color']
            if src.links: nt.links.new(src.links[0].from_socket, em.inputs['Color'])
            else: em.inputs['Color'].default_value = src.default_value
            nt.links.new(em.outputs[0], out.inputs['Surface'])
        bpy.ops.object.bake(**kw)
        if em: nt.links.new(bsdf.outputs[0], out.inputs['Surface']); nt.nodes.remove(em)
        maps[key] = img; nt.nodes.remove(node)
    sc.render.engine = prev_engine
    return maps


def baked_material(obj, maps, coat=0.0, metallic=0.0):
    m = bpy.data.materials.new(obj.name + '_baked'); m.use_nodes = True; nt = m.node_tree
    bsdf = nt.nodes['Principled BSDF']
    def tex(img):
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; return t
    nt.links.new(tex(maps['basecolor']).outputs['Color'], bsdf.inputs['Base Color'])
    nt.links.new(tex(maps['roughness']).outputs['Color'], bsdf.inputs['Roughness'])
    nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tex(maps['normal']).outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Metallic'].default_value = metallic
    for n in ('Coat Weight', 'Clearcoat'):
        if n in bsdf.inputs: bsdf.inputs[n].default_value = coat; break
    return m


def glb(obj, path, opt, preview=False):
    size = opt.get('texture', [512, 4096]) if not preview else [128, 1024]
    tex_dir = os.path.splitext(path)[0] + '-maps'; os.makedirs(tex_dir, exist_ok=True)
    def bake_part(ob, sz, metallic, label):
        maps = bake(ob, sz, samples=opt.get('bake_samples', 16))
        for k, img in maps.items():
            img.filepath_raw = os.path.join(tex_dir, f'{label}-{k}.png'); img.file_format = 'PNG'; img.save()
        ob.data.materials.clear(); ob.data.materials.append(baked_material(ob, maps, opt.get('coat', 0.0), metallic))
        # Remove modelling attributes the web doesn't need.
        for a in [a.name for a in ob.data.attributes if a.name in ('wear', 'knot', 'endgrain', 't', 'edge', 'ridge', 'latten', 'wrap')]:
            ob.data.attributes.remove(ob.data.attributes[a])
    if opt.get('bake', True): bake_part(obj, size, opt.get('metallic', 0.0), 'main')   # bake: false keeps an image-mapped material as it is
    for name, part in opt.get('bake_parts', {}).items():
        child = next(c for c in obj.children if c.name.split('.')[0] == name)
        bake_part(child, part.get('texture', [512, 512]), part.get('metallic', 0.0), name)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    for c in obj.children: c.select_set(True)   # parts not baked keep their own vertex-colour materials
    kw = dict(filepath=path, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
    attempts = [dict(kw, export_draco_mesh_compression_enable=opt.get('draco', True), export_image_format='WEBP'),
                dict(kw, export_draco_mesh_compression_enable=opt.get('draco', True)), kw]
    for a in attempts:
        try:
            bpy.ops.export_scene.gltf(**a); break
        except (TypeError, RuntimeError) as e:
            print('glTF export retry without some options:', e)
    return path
