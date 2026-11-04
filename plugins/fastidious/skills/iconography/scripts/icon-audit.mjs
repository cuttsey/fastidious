// iconography audit: check a folder of SVG icons for one consistent hand.
// node icon-audit.mjs <dir> [--grid 24] [--stroke 2] [--json]
// Checks: viewBox matches the grid; stroke widths are uniform (and match --stroke if given); caps/joins consistent;
// colour only via currentColor; no transforms, raster images, inline styles or ids left in; file size; kebab-case names.
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
const a = process.argv.slice(2), dir = a[0], opt = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : a[i + 1]; };
const grid = Number(opt('grid', 24)), want = opt('stroke') ? Number(opt('stroke')) : null;
const files = readdirSync(dir).filter((f) => f.endsWith('.svg')).sort();
const rows = [], strokes = new Map(), caps = new Map(), joins = new Map();
for (const f of files) {
  const s = readFileSync(join(dir, f), 'utf8'), issues = [], warn = [];
  const vb = (s.match(/viewBox="([^"]+)"/) || [])[1];
  if (!vb) issues.push('no viewBox'); else if (vb.trim() !== `0 0 ${grid} ${grid}`) issues.push(`viewBox "${vb}" (want 0 0 ${grid} ${grid})`);
  for (const m of s.matchAll(/stroke-width="([\d.]+)"/g)) strokes.set(m[1], (strokes.get(m[1]) || 0) + 1);
  const sw = [...new Set([...s.matchAll(/stroke-width="([\d.]+)"/g)].map((m) => m[1]))];
  if (sw.length > 1) issues.push(`mixed stroke widths ${sw.join(', ')}`);
  if (want && sw.length && sw.some((w) => Math.abs(Number(w) - want) > 0.01)) issues.push(`stroke ${sw.join(', ')} (want ${want})`);
  const cp = (s.match(/stroke-linecap="(\w+)"/) || [])[1], jn = (s.match(/stroke-linejoin="(\w+)"/) || [])[1];
  if (cp) caps.set(cp, (caps.get(cp) || 0) + 1); if (jn) joins.set(jn, (joins.get(jn) || 0) + 1);
  const colours = [...s.matchAll(/(?:fill|stroke|stop-color|color)="([^"]+)"/g)].map((m) => m[1]).filter((v) => !/^(none|currentColor|inherit|transparent)$/i.test(v));
  if (colours.length) issues.push(`hard-coded colour ${[...new Set(colours)].join(', ')}`);
  if (/transform=/.test(s)) warn.push('transform left in (flatten it)');
  if (/<image|data:image/.test(s)) issues.push('raster image inside');
  if (/style="/.test(s)) warn.push('inline style');
  if (/\sid="/.test(s)) warn.push('id attribute (clashes in a sprite)');
  if (!/stroke="currentColor"|fill="currentColor"/.test(s)) issues.push('does not inherit currentColor');
  const kb = statSync(join(dir, f)).size / 1024; if (kb > 2) warn.push(`${kb.toFixed(1)} KB (simplify paths)`);
  if (!/^[a-z0-9]+(-[a-z0-9]+)*\.svg$/.test(f)) warn.push('name not kebab-case');
  rows.push({ file: f, issues, warn });
}
if (caps.size > 1) rows.push({ file: '(set)', issues: [`mixed linecaps ${[...caps.keys()].join(', ')}`], warn: [] });
if (joins.size > 1) rows.push({ file: '(set)', issues: [`mixed linejoins ${[...joins.keys()].join(', ')}`], warn: [] });
if (strokes.size > 1) rows.push({ file: '(set)', issues: [`set uses ${strokes.size} stroke widths: ${[...strokes.keys()].join(', ')}`], warn: [] });
const fails = rows.reduce((n, r) => n + r.issues.length, 0), warns = rows.reduce((n, r) => n + r.warn.length, 0);
if (a.includes('--json')) console.log(JSON.stringify({ files: files.length, fails, warns, rows }, null, 2));
else {
  console.log(`ICON AUDIT · ${dir} · ${files.length} icons · grid ${grid}${want ? ` · stroke ${want}` : ''}`);
  for (const r of rows) { if (!r.issues.length && !r.warn.length) continue; console.log(`  ${r.file}`); r.issues.forEach((i) => console.log(`    FAIL ${i}`)); r.warn.forEach((w) => console.log(`    warn ${w}`)); }
  console.log(`RESULT: ${fails} FAIL, ${warns} WARN`);
}
process.exit(fails ? 1 : 0);
