#!/usr/bin/env python3
"""Fetch CC0 assets from Poly Haven into the skill's cache, with a credit record.

  polyhaven.py search <words> [--type hdris|textures|models]
  polyhaven.py get <asset-id> [--res 1k|2k|4k] [--out DIR]

HDRIs land as <id>_<res>.hdr; textures as their diffuse, roughness, normal (GL) and displacement maps,
ready for materials.pbr. Downloads use curl (some Python installs on macOS lack root certificates).
"""
import json, os, subprocess, sys

API = 'https://api.polyhaven.com'
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache', 'polyhaven')


def get_json(url):
    return json.loads(subprocess.run(['curl', '-fsSL', url], check=True, capture_output=True).stdout)


def download(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    subprocess.run(['curl', '-fsSL', '-o', path, url], check=True)
    return path


def search(words, kind):
    assets = get_json(f'{API}/assets?t={kind}')
    words = [w.lower() for w in words]
    hits = []
    for aid, a in assets.items():
        hay = ' '.join([aid, a.get('name', ''), *a.get('tags', []), *a.get('categories', [])]).lower()
        if all(w in hay for w in words):
            hits.append((a.get('download_count', 0), aid, a.get('name', '')))
    for n, aid, name in sorted(hits, reverse=True)[:25]:
        print(f'{aid:40s} {name}  ({n} downloads)')


def get(aid, res, out):
    info = get_json(f'{API}/info/{aid}')
    files = get_json(f'{API}/files/{aid}')
    folder = out or os.path.join(CACHE, aid); saved = []
    if 'hdri' in files:
        f = files['hdri'][res]['hdr']; saved.append(download(f['url'], os.path.join(folder, f'{aid}_{res}.hdr')))
    else:
        for key in ('Diffuse', 'Rough', 'nor_gl', 'Displacement', 'AO'):
            if key in files and res in files[key]:
                fmt = 'jpg' if 'jpg' in files[key][res] else next(iter(files[key][res]))
                url = files[key][res][fmt]['url']; saved.append(download(url, os.path.join(folder, os.path.basename(url))))
    credit = {'id': aid, 'name': info.get('name'), 'authors': list(info.get('authors', {}).keys()),
              'licence': 'CC0 1.0', 'source': f'https://polyhaven.com/a/{aid}', 'files': [os.path.basename(s) for s in saved]}
    json.dump(credit, open(os.path.join(folder, 'credit.json'), 'w'), indent=1)
    print(json.dumps(credit, indent=1)); print(folder)


if __name__ == '__main__':
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    if not a: print(__doc__); sys.exit(1)
    if a[0] == 'search': search([w for w in a[1:] if not w.startswith('--') and w not in (opt('--type', ''),)], opt('--type', 'all'))
    elif a[0] == 'get': get(a[1], opt('--res', '1k'), opt('--out', None))
