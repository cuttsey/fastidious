// iconography specimen: one sheet showing every icon at 16/20/24/32, light and dark, beside a line of text.
// node specimen.mjs <dir> --out icons-specimen.html [--font "DM Sans"] [--fontcss <google css url>] [--ink #0E2318 --ground #F6F7F1 --dark-ink #EDF2EC --dark-ground #0C1711] [--accent #03A651]
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, relative, dirname, resolve } from 'node:path';
const a = process.argv.slice(2), dir = a[0], opt = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : a[i + 1]; };
const out = resolve(opt('out', 'icons-specimen.html')), font = opt('font', 'system-ui'), css = opt('fontcss', '');
const ink = opt('ink', '#111'), ground = opt('ground', '#fff'), dink = opt('dark-ink', '#eee'), dground = opt('dark-ground', '#111'), accent = opt('accent', '#06c');
const icons = readdirSync(dir).filter((f) => f.endsWith('.svg')).sort().map((f) => ({ name: f.replace(/\.svg$/, ''), svg: readFileSync(join(dir, f), 'utf8').replace(/<\?xml[^>]*>/, '').replace(/<svg\b[^>]*>/, (tag) => tag.replace(/\s(width|height)="[^"]*"/g, '')) }));
const sizes = [16, 20, 24, 32];
const cell = (i) => `<figure class="ic${/^motif-/.test(i.name) ? ' motif' : ''}"><div class="sizes">${sizes.map((s) => `<span style="width:${s}px;height:${s}px">${i.svg}</span>`).join('')}</div><figcaption>${i.name}</figcaption></figure>`;
const panel = (cls) => `<section class="panel ${cls}"><h2>${cls === 'dark' ? 'Dark' : 'Light'}</h2><div class="grid">${icons.map(cell).join('')}</div>
  <p class="line">Find a club <span class="inl">${(icons.find((i) => /arrow/.test(i.name)) || icons[0] || { svg: '' }).svg}</span> · beside text at body size, the icon should sit on the baseline and match the stem weight.</p>
  <div class="state"><span>Active state in the accent:</span>${icons.slice(0, 6).map((i) => `<span class="acc">${i.svg}</span>`).join('')}</div></section>`;
writeFileSync(out, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Icon specimen</title>
${css ? `<link rel="stylesheet" href="${css}">` : ''}
<style>*{box-sizing:border-box;margin:0}body{font:400 17px/1.5 "${font}",system-ui,sans-serif;background:${ground};color:${ink}}
header{padding:32px 24px 8px}h1{font-size:28px}header p{opacity:.75}
.panel{padding:24px}.panel h2{font-size:15px;text-transform:uppercase;letter-spacing:.08em;opacity:.7;margin-bottom:16px}
.light{background:${ground};color:${ink}}.dark{background:${dground};color:${dink}}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.ic{padding:14px;border-radius:12px;outline:1px solid color-mix(in srgb,currentColor 15%,transparent);outline-offset:-1px}
.sizes{display:flex;align-items:flex-end;gap:14px;min-height:40px}.sizes span{display:inline-grid}.sizes svg{width:100%;height:100%}
figcaption{margin-top:10px;font-size:13px;opacity:.75}.motif .sizes span:first-child{opacity:.25}.motif figcaption::after{content:' · motif: 24px and up'}
.line{margin-top:20px;font-size:17px}.inl{display:inline-grid;width:1em;height:1em;vertical-align:-.15em}.inl svg{width:100%;height:100%}
.state{margin-top:12px;display:flex;gap:12px;align-items:center;font-size:14px}.acc{display:inline-grid;width:24px;height:24px;color:${accent}}.acc svg{width:100%;height:100%}
</style></head><body><header><h1>Icon specimen</h1><p>${icons.length} icons from ${relative(dirname(out), resolve(dir)) || '.'} at 16, 20, 24 and 32 px. One hand, one weight, one grid?</p></header>
${panel('light')}${panel('dark')}</body></html>`);
console.log('specimen', out, icons.length, 'icons');
