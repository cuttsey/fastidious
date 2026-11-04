# Studio: colour management, light, an optional HDRI, a shadow-catching floor, cameras and rendering.
# Renders are transparent PNGs with the floor's shadow kept in the alpha, so the same render sits on any
# brand ground. on_ground() composites onto the brand colour with ffmpeg (exact hex, untouched by the view transform).
import bpy, math, os, shutil, subprocess
from mathutils import Vector


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _hex(h, a=1.0):
    h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (lin(r), lin(g), lin(b), a)


def _eevee_name():
    for n in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
        try:
            bpy.context.scene.render.engine = n; return n
        except TypeError:
            continue
    return 'BLENDER_WORKBENCH'


def _look_at(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def setup(st, obj, resolve, preview=False, draft=False):
    sc = bpy.context.scene
    r = sc.render
    r.resolution_x, r.resolution_y = st.get('size', [1600, 1000])
    r.resolution_percentage = 50 if preview or draft else 100
    r.film_transparent = True
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGBA'
    vs = sc.view_settings
    if st.get('view'):   # e.g. 'Standard' when brand colours must render exactly
        vs.view_transform = st['view']; vs.look = 'None'
    for vt, look in () if st.get('view') else (('AgX', 'AgX - Medium High Contrast'), ('Filmic', 'Medium High Contrast')):
        try:
            vs.view_transform = vt
            try: vs.look = look
            except TypeError: pass
            break
        except TypeError:
            continue

    if preview:
        _eevee_name()
    else:
        r.engine = 'CYCLES'
        c = sc.cycles
        c.samples = 32 if draft else st.get('samples', 96); c.use_denoising = True
        try: c.denoiser = 'OPENIMAGEDENOISE'
        except TypeError: pass
        c.device = st.get('device', 'CPU')
        c.max_bounces = 8
        if c.device == 'GPU':
            try:
                p = bpy.context.preferences.addons['cycles'].preferences
                p.compute_device_type = st.get('gpu', 'METAL'); p.get_devices()
                for d in p.devices: d.use = True
            except Exception as e:
                print('GPU unavailable, using CPU:', e); c.device = 'CPU'

    # World: an HDRI gives believable reflections; without one, a soft neutral fill.
    w = bpy.data.worlds.new('World'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']
    hdri = st.get('hdri')
    if hdri:
        env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(resolve(hdri))
        mp = nt.nodes.new('ShaderNodeMapping'); tc = nt.nodes.new('ShaderNodeTexCoord')
        mp.inputs['Rotation'].default_value[2] = math.radians(st.get('hdri_rotation', 0))
        nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
        nt.links.new(env.outputs['Color'], bg.inputs['Color'])
        bg.inputs['Strength'].default_value = st.get('hdri_strength', 0.6)
    else:
        bg.inputs['Color'].default_value = (0.6, 0.62, 0.6, 1); bg.inputs['Strength'].default_value = 0.35

    # Three-point area lights, aimed at the object.
    c = obj.location
    for name, loc, power, size, kelvin_rgb in st.get('lights', [
        ('key', (-1.3, -1.6, 2.1), 70, 0.9, (1.0, 0.93, 0.84)),
        ('fill', (1.9, -0.8, 0.9), 10, 2.0, (0.86, 0.92, 1.0)),
        ('rim', (0.6, 2.2, 1.5), 40, 0.5, (1.0, 0.97, 0.92)),
    ]):
        ld = bpy.data.lights.new(name, 'AREA'); ld.energy = power; ld.size = size; ld.color = kelvin_rgb
        lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo); lo.location = loc; _look_at(lo, c)

    # Floor: a large plane under the object's lowest point that catches shadows only.
    fl = st.get('floor', True)
    if fl:
        bpy.context.view_layer.update()   # matrix_world is stale until the scene updates
        zmin = min((o.matrix_world @ Vector(v)).z for o in [obj, *obj.children] for v in o.bound_box)
        bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, zmin - fl.get('gap', 0.0) if isinstance(fl, dict) else zmin))
        floor = bpy.context.active_object; floor.name = 'floor'
        try: floor.is_shadow_catcher = True
        except AttributeError: pass
        # EEVEE has no shadow catcher: hide the floor in previews rather than render it white.
        if preview: floor.hide_render = True


def camera(shot, obj):
    sc = bpy.context.scene
    cam = sc.camera
    if cam is None:
        cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = shot.get('loc', (0.0, -1.8, 0.9))
    target = shot.get('target', list(obj.location))
    _look_at(cam, target)
    cd = cam.data; cd.lens = shot.get('lens', 60); cd.sensor_width = 36
    cd.dof.use_dof = bool(shot.get('fstop'))
    if cd.dof.use_dof:
        cd.dof.focus_distance = shot.get('focus', (Vector(target) - cam.location).length)
        cd.dof.aperture_fstop = shot['fstop']
    if 'size' in shot:
        sc.render.resolution_x, sc.render.resolution_y = shot['size']


def render_still(path, shot, preview=False, draft=False):
    sc = bpy.context.scene
    if not preview and not draft and 'samples' in shot and sc.render.engine == 'CYCLES':
        sc.cycles.samples = shot['samples']
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def _ffmpeg():
    for c in (shutil.which('ffmpeg'), '/usr/local/bin/ffmpeg', '/opt/homebrew/bin/ffmpeg'):
        if c and os.path.exists(c): return c
    return None


def on_ground(png, ground):
    """Composite a transparent render (its shadow in the alpha) onto a brand colour: <name>-ground.jpg."""
    ff = _ffmpeg(); out = png[:-4] + '-ground.jpg'
    if not ff: print('ffmpeg not found; skipped', out); return png
    col = ground.lstrip('#')
    subprocess.run([ff, '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'color=c=0x{col}:s=16x16', '-i', png,
                    '-filter_complex', '[0][1]scale2ref[bg][fg];[bg][fg]overlay=format=auto', '-frames:v', '1', '-q:v', '2', out], check=True)
    return out


def render_turntable(obj, stem, tt, ground, preview=False):
    """One full turn about the vertical axis; PNG frames, then an MP4 on the brand ground."""
    sc = bpy.context.scene
    n = tt.get('frames', 120); sc.frame_start, sc.frame_end = 1, n
    sc.render.fps = tt.get('fps', 30)
    if not preview and sc.render.engine == 'CYCLES':
        sc.cycles.samples = tt.get('samples', 48)
    # Spin a pivot, not the object, so the object's own pose is kept.
    piv = bpy.data.objects.new('pivot', None); sc.collection.objects.link(piv); piv.location = obj.location
    obj.parent = piv; obj.matrix_parent_inverse = piv.matrix_world.inverted()
    # Linear keys at frame 1 (0°) and n+1 (full turn); frames 1..n then loop without a repeated frame.
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
    piv.rotation_euler = (0, 0, 0); piv.keyframe_insert('rotation_euler', frame=1)
    piv.rotation_euler = (0, 0, math.radians(tt.get('degrees', 360))); piv.keyframe_insert('rotation_euler', frame=n + 1)
    fdir = stem + '-frames'; os.makedirs(fdir, exist_ok=True)
    sc.render.filepath = os.path.join(fdir, 'f')
    bpy.ops.render.render(animation=True)
    ff = _ffmpeg()
    if not ff: return fdir
    col = (ground or '#FFFFFF').lstrip('#')
    w, h = sc.render.resolution_x * sc.render.resolution_percentage // 100, sc.render.resolution_y * sc.render.resolution_percentage // 100
    subprocess.run([ff, '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'color=c=0x{col}:s={w}x{h}:r={sc.render.fps}',
                    '-framerate', str(sc.render.fps), '-i', os.path.join(fdir, 'f%04d.png'),
                    '-filter_complex', '[0][1]overlay=format=auto:shortest=1', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', stem + '.mp4'], check=True)
    return stem + '.mp4'
