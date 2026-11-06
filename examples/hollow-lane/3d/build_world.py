"""Hollow Lane: a miniature Somerset orchard, built in code with Blender (bpy).

    python3 build_world.py --scene S01 --frames 1-36 --out ../world/S01      # render a scene's frames
    python3 build_world.py --scene S01 --still 1 --out ../world/anchors     # one frame

World (from WORLD-BIBLE.md): a hand-made tabletop diorama of turned wood, felt and painted clay, seen through a
long lens, lit by one low autumn sun from the left. The through-line object is one russet apple.
"""
import argparse
import math
import os
import random

import bpy
from mathutils import Vector

R = random.Random(7)
PAL = {
    "felt": (0.47, 0.53, 0.25), "felt2": (0.36, 0.43, 0.19), "lane": (0.85, 0.77, 0.60), "oak": (0.54, 0.38, 0.22),
    "oakdark": (0.30, 0.20, 0.12), "cream": (0.94, 0.90, 0.82), "slate": (0.17, 0.15, 0.13), "red": (0.71, 0.26, 0.16),
    "russet": (0.66, 0.42, 0.17), "straw": (0.88, 0.80, 0.58), "glass": (0.30, 0.42, 0.25), "cider": (0.79, 0.60, 0.23),
    "bark": (0.33, 0.25, 0.18), "chalk": (0.97, 0.96, 0.92), "table": (0.22, 0.15, 0.10),
}


def srgb(c):
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (1.0,)


def mat(name, col, rough=0.8, noise=0.15, scale=40.0, sheen=0.0, transmission=0.0, ior=1.45, bump=0.15):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = scale
    tex.inputs["Detail"].default_value = 8.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    c = srgb(col)
    lo = tuple(max(0, v * (1 - noise)) for v in c[:3]) + (1,)
    hi = tuple(min(1, v * (1 + noise)) for v in c[:3]) + (1,)
    ramp.color_ramp.elements[0].color = lo
    ramp.color_ramp.elements[1].color = hi
    nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    if "Sheen Weight" in b.inputs:
        b.inputs["Sheen Weight"].default_value = sheen
    if transmission:
        b.inputs["Transmission Weight"].default_value = transmission
        b.inputs["IOR"].default_value = ior
    bm = nt.nodes.new("ShaderNodeBump")
    bm.inputs["Strength"].default_value = bump
    nt.links.new(tex.outputs["Fac"], bm.inputs["Height"])
    nt.links.new(bm.outputs["Normal"], b.inputs["Normal"])
    return m


def obj_mat(o, m):
    o.data.materials.clear()
    o.data.materials.append(m)
    return o


def smooth(o, level=1):
    mod = o.modifiers.new("s", "SUBSURF")
    mod.levels = level
    mod.render_levels = level
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def cyl(r, h, loc, m, verts=24, name="c"):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts, location=loc)
    o = bpy.context.object
    o.name = name
    return obj_mat(o, m)


def sphere(r, loc, m, sub=2, name="s"):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=sub, location=loc)
    o = bpy.context.object
    o.name = name
    for p in o.data.polygons:
        p.use_smooth = True
    return obj_mat(o, m)


def box(size, loc, m, name="b", bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = size
    o.name = name
    if bevel:
        b = o.modifiers.new("bv", "BEVEL")
        b.width = bevel
        b.segments = 3
    return obj_mat(o, m)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    # Table and diorama base
    box((14, 10, 0.1), (0, 0, -0.38), mat("table", PAL["table"], 0.5, 0.25, 6, bump=0.05), "table")
    box((4.2, 3.2, 0.3), (0, 0, -0.18), mat("base", PAL["oak"], 0.45, 0.2, 9, bump=0.08), "base", bevel=0.03)
    # Felt ground with gentle hills
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.02))
    g = bpy.context.object
    g.scale = (4.1, 3.1, 1)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=60)
    bpy.ops.object.mode_set(mode="OBJECT")
    t = bpy.data.textures.new("hills", "CLOUDS")
    t.noise_scale = 0.9
    d = g.modifiers.new("d", "DISPLACE")
    d.texture = t
    d.strength = 0.07
    d.mid_level = 0.0
    obj_mat(g, mat("felt", PAL["felt"], 0.95, 0.18, 120, sheen=0.6, bump=0.3))
    for p in g.data.polygons:
        p.use_smooth = True
    # The lane: the long way round, an S through the orchard
    cu = bpy.data.curves.new("lane", "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("BEZIER")
    pts = [(-1.9, -1.4), (-0.9, -0.9), (-1.3, 0.1), (-0.1, 0.4), (0.9, -0.3), (1.6, 0.5), (1.1, 1.3)]
    sp.bezier_points.add(len(pts) - 1)
    for bp, (x, y) in zip(sp.bezier_points, pts):
        bp.co = (x, y, 0.035)
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    cu.extrude = 0.004
    cu.bevel_depth = 0.0
    lane = bpy.data.objects.new("lane", cu)
    sc.collection.objects.link(lane)
    lane.data.materials.append(mat("lane", PAL["lane"], 0.9, 0.2, 200, bump=0.4))
    # Give the lane width with an offset solidify via geometry: use a second curve bevel object
    bpy.ops.curve.primitive_bezier_curve_add()
    prof = bpy.context.object
    prof.name = "laneprofile"
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.curve.select_all(action="SELECT")
    bpy.ops.transform.resize(value=(0.11, 0.11, 0.11))
    bpy.ops.object.mode_set(mode="OBJECT")
    prof.hide_render = True
    cu.bevel_mode = "OBJECT"
    cu.bevel_object = prof
    # Orchard: trees right of the lane
    leaf = mat("leaf", PAL["felt2"], 0.95, 0.25, 60, sheen=0.5, bump=0.4)
    bark = mat("bark", PAL["bark"], 0.8, 0.3, 30, bump=0.5)
    red = mat("red", PAL["red"], 0.45, 0.15, 25, bump=0.05)
    russet = mat("russet", PAL["russet"], 0.6, 0.45, 70, bump=0.35)
    trees = []
    for i, (x, y) in enumerate([(0.3, 1.1), (0.9, 1.0), (1.5, 1.2), (0.0, -0.6), (0.6, -0.9), (1.2, -1.1),
                                 (1.8, -0.6), (1.4, 0.0), (0.4, 0.95 - 1.2), (-0.6, 1.2), (-0.2, 1.4), (1.9, 1.1)]):
        x += R.uniform(-0.08, 0.08)
        y += R.uniform(-0.08, 0.08)
        h = R.uniform(0.22, 0.3)
        cyl(0.022, h, (x, y, h / 2), bark, 10, f"trunk{i}")
        top = h + 0.05
        for k in range(6):
            a = R.uniform(0, 6.28)
            rr = R.uniform(0.0, 0.08)
            sphere(R.uniform(0.07, 0.11), (x + rr * math.cos(a), y + rr * math.sin(a), top + R.uniform(-0.03, 0.06)), leaf, 3, f"leaf{i}_{k}")
        for k in range(R.randint(6, 10)):
            a = R.uniform(0, 6.28)
            z = top + R.uniform(-0.07, 0.05)
            sphere(0.017, (x + 0.12 * math.cos(a), y + 0.12 * math.sin(a), z), red, 2, f"apple{i}_{k}")
        trees.append((x, y, top))
    # The russet apple on the hero tree (tree 1), facing the camera
    hx, hy, ht = trees[3]
    sphere(0.022, (hx - 0.13, hy - 0.02, ht - 0.04), russet, 3, "the_apple")
    # Barn, back left
    cream = mat("cream", PAL["cream"], 0.85, 0.08, 18, bump=0.1)
    slate = mat("slate", PAL["slate"], 0.7, 0.2, 30, bump=0.2)
    box((0.8, 0.45, 0.36), (-1.25, 0.95, 0.16), cream, "barn", bevel=0.01)
    for s in (-1, 1):
        r = box((0.86, 0.27, 0.012), (-1.25, 0.95 + s * 0.115, 0.4), slate, "roof")
        r.rotation_euler = (math.radians(-s * 32), 0, 0)
    door = box((0.22, 0.01, 0.26), (-1.25, 0.72, 0.11), mat("door", PAL["oakdark"], 0.7, 0.2, 15), "door")
    # Barrels in front of the barn, with chalk tallies: eleven months
    oak = mat("oak", PAL["oak"], 0.55, 0.3, 14, bump=0.3)
    band = mat("band", (0.22, 0.21, 0.2), 0.35, 0.1, 30)
    chalk = mat("chalk", PAL["chalk"], 0.95, 0.05, 50)
    for k in range(5):
        x = -1.62 + k * 0.17
        y = 0.55
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.16, vertices=24, location=(x, y, 0.06))
        b = bpy.context.object
        b.rotation_euler = (math.radians(90), 0, 0)
        obj_mat(b, oak)
        for p in b.data.polygons:
            p.use_smooth = True
        for dz in (-0.05, 0.05):
            bpy.ops.mesh.primitive_torus_add(major_radius=0.061, minor_radius=0.004, location=(x, y + dz, 0.06))
            tb = bpy.context.object
            tb.rotation_euler = (math.radians(90), 0, 0)
            obj_mat(tb, band)
        if k == 2:  # eleven marks on the middle barrel head
            for m in range(11):
                group, pos = divmod(m, 5)
                if pos == 4:
                    bx = box((0.05, 0.004, 0.006), (x - 0.03 + group * 0.035, y - 0.088, 0.06), chalk, "tally")
                    bx.rotation_euler = (0, math.radians(30), 0)
                else:
                    box((0.006, 0.004, 0.05), (x - 0.045 + group * 0.035 + pos * 0.008, y - 0.083, 0.06), chalk, "tally")
    # The press, beside the barn door
    for s in (-1, 1):
        box((0.03, 0.03, 0.34), (PX + s * 0.12, PY, 0.15), oak, "post", bevel=0.004)
    box((0.3, 0.05, 0.04), (PX, PY, 0.33), oak, "beam", bevel=0.004)
    cyl(0.012, 0.16, (PX, PY, 0.24), band, 16, "screw")
    box((0.3, 0.3, 0.03), (PX, PY, 0.02), mat("tray", PAL["oakdark"], 0.6, 0.2, 12), "tray", bevel=0.005)
    straw = mat("straw", PAL["straw"], 0.95, 0.2, 90, sheen=0.4, bump=0.5)
    for k in range(4):
        box((0.2, 0.2, 0.03), (PX, PY, 0.055 + k * 0.034), straw, "cheese", bevel=0.008)
    box((0.22, 0.22, 0.02), (PX, PY, 0.2), oak, "platen", bevel=0.004)
    cyl(0.12, 0.004, (PX, PY, 0.037), mat("juice", PAL["cider"], 0.08, 0.05, 10), 32, "juice")
    cyl(0.04, 0.07, (PX + 0.23, PY - 0.13, 0.035), mat("jug", PAL["cream"], 0.4, 0.1, 20), 24, "jug")
    # Lane's end, front right: a crate, a bottle and a glass
    box((0.24, 0.16, 0.1), (1.55, -1.25, 0.05), oak, "crate", bevel=0.006)
    glass = mat("bottle", PAL["glass"], 0.05, 0.02, 10, transmission=0.9, ior=1.5)
    cyl(0.028, 0.11, (1.5, -1.25, 0.155), glass, 32, "bottle")
    cyl(0.011, 0.05, (1.5, -1.25, 0.235), glass, 24, "neck")
    cyl(0.025, 0.06, (1.61, -1.22, 0.13), mat("glass", (0.9, 0.9, 0.88), 0.03, 0.0, 10, transmission=1.0), 32, "glass")
    cyl(0.022, 0.04, (1.61, -1.22, 0.122), mat("cider", PAL["cider"], 0.15, 0.05, 10, transmission=0.6, ior=1.34), 32, "cider")
    sphere(0.022, (1.43, -1.18, 0.12), russet, 3, "apple_end")
    # Fence posts along the lane for scale
    for k, (x, y) in enumerate([(-1.6, -1.05), (-1.25, -0.75), (-1.05, -0.2), (-0.45, 0.35), (0.55, -0.05)]):
        box((0.015, 0.015, 0.08), (x + 0.14, y - 0.1, 0.04), oak, f"fence{k}")
    # Light: one low autumn sun from the left, a dim warm studio
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 5.5
    sun.angle = math.radians(3)
    sun.color = (1.0, 0.83, 0.64)
    so = bpy.data.objects.new("sun", sun)
    sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(72), 0, math.radians(-95))
    w = bpy.data.worlds.new("w")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = srgb((0.16, 0.14, 0.12))
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    return sc


PX, PY = -0.62, 0.6

SCENES = {
    # name: (camera from, camera to, look from, look to, lens, focus distance object)
    "S01": ((-3.4, -4.2, 2.4), (-2.9, -3.6, 2.0), (0.0, 0.1, 0.05), (0.0, 0.1, 0.05), 70, None),
    "S02": ((-0.75, -1.5, 0.4), (-0.5, -1.58, 0.33), (-0.08, -0.64, 0.25), (-0.12, -0.64, 0.24), 100, "the_apple"),
    "S03": ((-1.27, -0.4, 0.6), (-1.05, -0.15, 0.48), (PX, PY, 0.15), (PX, PY, 0.15), 75, "screw"),
    "S04": ((-1.95, -0.4, 0.32), (-1.15, -0.35, 0.28), (-1.75, 0.55, 0.07), (-1.3, 0.55, 0.07), 80, "tally"),
    "S05": ((0.95, -2.1, 0.34), (1.12, -1.98, 0.52), (1.55, -1.24, 0.14), (1.55, -1.24, 0.16), 80, "bottle"),
    "S06": ((-2.9, -3.6, 2.0), (-0.5, -2.2, 4.6), (0.0, 0.1, 0.05), (0.1, 0.2, 0.0), 70, None),
}


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * t)


def place_camera(sc, name, t):
    a, b, la, lb, lens, focus = SCENES[name]
    e = ease(t)
    pos = Vector(a).lerp(Vector(b), e)
    look = Vector(la).lerp(Vector(lb), e)
    cam = sc.camera
    cam.location = pos
    cam.rotation_euler = (look - pos).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    if focus and focus in bpy.data.objects:
        cam.data.dof.focus_distance = (bpy.data.objects[focus].matrix_world.translation - pos).length
        cam.data.dof.aperture_fstop = 2.2
    else:
        cam.data.dof.focus_distance = (look - pos).length
        cam.data.dof.aperture_fstop = 4.0


def setup_render(sc, w, h, samples):
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 4
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Base Contrast" if "AgX - Base Contrast" in [i.name for i in type(sc.view_settings).bl_rna.properties["look"].enum_items] else "None"
    cd = bpy.data.cameras.new("cam")
    co = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(co)
    sc.camera = co


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True)
    ap.add_argument("--frames", default="1-36")
    ap.add_argument("--count", type=int, default=36)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="960x540")
    ap.add_argument("--samples", type=int, default=24)
    a = ap.parse_args()
    sc = build()
    w, h = (int(v) for v in a.size.split("x"))
    setup_render(sc, w, h, a.samples)
    lo, hi = (int(v) for v in a.frames.split("-")) if "-" in a.frames else (int(a.frames), int(a.frames))
    os.makedirs(a.out, exist_ok=True)
    for f in range(lo, hi + 1):
        place_camera(sc, a.scene, (f - 1) / max(1, a.count - 1))
        sc.render.filepath = os.path.join(a.out, f"f_{f:03d}.png")
        bpy.ops.render.render(write_still=True)
        print("rendered", a.scene, f, flush=True)


if __name__ == "__main__":
    main()
