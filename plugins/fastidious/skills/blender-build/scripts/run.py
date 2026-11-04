# blender-build runner. Executed inside Blender:  blender -b -P run.py -- <spec.json> [--preview|--draft] [--only stills,turntable,glb]
# A spec names an object builder (a Python module with build(params) -> object), a material, a studio and outputs.
# Everything is rebuilt from scratch each run, so the spec and the builder are the source of truth, never a .blend.
import bpy, sys, os, json, importlib.util

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
if not argv:
    raise SystemExit('usage: blender -b -P run.py -- <spec.json> [--preview|--draft] [--only stills,turntable,glb]')
spec_path = os.path.abspath(argv[0])
spec = json.load(open(spec_path))
PREVIEW = '--preview' in argv
DRAFT = '--draft' in argv   # Cycles at half size and 32 samples: real materials and shadows, quickly
ONLY = set(argv[argv.index('--only') + 1].split(',')) if '--only' in argv else None
BASE = os.path.dirname(spec_path)
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, 'lib'))
import studio, materials, export  # noqa: E402


def resolve(p):
    for c in (p, os.path.join(BASE, p), os.path.join(SKILL, p), os.path.join(SKILL, 'objects', p)):
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError(p)


def load_module(path):
    s = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


out_dir = os.path.join(BASE, spec.get('out', 'out'))
os.makedirs(out_dir, exist_ok=True)
name = spec.get('name', 'object')

studio.reset()
obj_spec = spec['object']
builder = load_module(resolve(obj_spec['builder']))
obj = builder.build({k: (resolve(v) if k in obj_spec.get('paths', []) else v) for k, v in obj_spec.get('params', {}).items()})
obj.name = name
if spec.get('material', {}).get('type') != 'keep':   # 'keep' leaves an imported scan's own materials
    mat = materials.build(spec.get('material', {'type': 'wood_stick'}), resolve)
    obj.data.materials.clear(); obj.data.materials.append(mat)
for part, part_spec in spec.get('parts', {}).items():   # children with their own material, e.g. a sword's grip
    child = next(c for c in obj.children if c.name.split('.')[0] == part)
    child.data.materials.clear(); child.data.materials.append(getattr(materials, part_spec['type'])(part_spec))

st = spec.get('studio', {})
studio.setup(st, obj, resolve, preview=PREVIEW, draft=DRAFT)

want = lambda k: (ONLY is None or k in ONLY) and k in spec.get('outputs', {})
outs = spec.get('outputs', {})
report = {'spec': spec_path, 'preview': PREVIEW, 'files': []}

SHOT = argv[argv.index('--shot') + 1] if '--shot' in argv else None   # render one named still only
if want('stills'):
    for shot in [x for x in outs['stills'] if not SHOT or x['name'] == SHOT]:
        studio.camera(shot, obj)
        path = os.path.join(out_dir, f"{name}-{shot['name']}{'-preview' if PREVIEW else '-draft' if DRAFT else ''}.png")
        studio.render_still(path, shot, preview=PREVIEW, draft=DRAFT)
        report['files'].append(path)
        if st.get('ground'):
            report['files'].append(studio.on_ground(path, st['ground']))

if want('turntable'):
    tt = outs['turntable']
    studio.camera(tt, obj)
    report['files'].append(studio.render_turntable(obj, os.path.join(out_dir, f'{name}-turntable'), tt, st.get('ground'), preview=PREVIEW))

if want('glb'):
    report['files'].append(export.glb(obj, os.path.join(out_dir, f'{name}.glb'), outs['glb'], preview=PREVIEW))

json.dump(report, open(os.path.join(out_dir, f'{name}-report.json'), 'w'), indent=1)
print('BLENDER-BUILD DONE', json.dumps(report))
