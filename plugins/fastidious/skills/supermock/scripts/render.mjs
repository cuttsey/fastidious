// supermock render: step a scene frame by frame and encode it.
// node render.mjs <scene.html> --config <config.json> --out <name> [--w 1920 --h 1080] [--fps 30] [--duration 8]
//                 [--still <t seconds>] [--gif] [--webm] [--keep]
// A scene exposes window.SUPERMOCK = { ready: Promise, renderAt: async (t) => {} } and reads window.SUPERMOCK_CONFIG.
import { mkdirSync, readFileSync, rmSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { resolve, dirname } from 'node:path';
import { Browser } from '../../design-taste-frontend/scripts/lib/cdp.mjs';
const a = process.argv.slice(2), scene = resolve(a[0]);
const opt = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : (a[i + 1] && !a[i + 1].startsWith('--') ? a[i + 1] : true); };
const cfgPath = opt('config'); const cfg = cfgPath ? JSON.parse(readFileSync(cfgPath, 'utf8')) : {};
const base = cfgPath ? dirname(resolve(cfgPath)) : process.cwd();
const fix = (v) => (typeof v === 'string' && /\.(png|jpe?g|webp|svg|avif)$/i.test(v) && !/^(https?|file|data):/.test(v)) ? pathToFileURL(resolve(base, v)).href
  : Array.isArray(v) ? v.map(fix) : (v && typeof v === 'object') ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, k === 'frames' && typeof x === 'string' ? pathToFileURL(resolve(base, x)).href : fix(x)])) : v;
const config = fix(cfg);
const W = Number(opt('w', cfg.w || 1920)), H = Number(opt('h', cfg.h || 1080)), fps = Number(opt('fps', cfg.fps || 30)), dur = Number(opt('duration', cfg.duration || 8));
const out = resolve(opt('out', 'supermock/out/clip')); mkdirSync(dirname(out), { recursive: true });
const b = await Browser.launch({ width: W, height: H });
const p = await b.newPage({ width: W, height: H, dsf: 1 });
await p.send('Page.addScriptToEvaluateOnNewDocument', { source: `window.SUPERMOCK_CONFIG = ${JSON.stringify({ ...config, w: W, h: H, fps, duration: dur })};` });
await p.goto(pathToFileURL(scene).href, { settleMs: 300 });
await p.eval('window.SUPERMOCK.ready.then(() => document.fonts.ready).then(() => true)');
const still = opt('still');
if (still !== undefined) {
  await p.eval(`window.SUPERMOCK.renderAt(${Number(still) || 0}).then(() => true)`);
  await p.screenshot({ path: out + '.png', format: 'png' }); await b.close(); console.log('still', out + '.png'); process.exit(0);
}
const fdir = out + '-frames'; rmSync(fdir, { recursive: true, force: true }); mkdirSync(fdir, { recursive: true });
const n = Math.round(dur * fps);
for (let i = 0; i < n; i++) {
  await p.eval(`window.SUPERMOCK.renderAt(${(i / fps).toFixed(4)}).then(() => true)`);
  await p.screenshot({ path: `${fdir}/f${String(i).padStart(4, '0')}.png`, format: 'png' });
  if (i % 30 === 0) process.stdout.write(`\r${i}/${n}`);
}
await b.close();
const ff = (args) => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args], { stdio: 'inherit' });
ff(['-framerate', String(fps), '-i', `${fdir}/f%04d.png`, '-c:v', 'libx264', '-preset', 'slow', '-crf', String(opt('crf', 20)), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out + '.mp4']);
ff(['-i', out + '.mp4', '-vf', `select=eq(n\\,${Math.round(n * 0.6)})`, '-frames:v', '1', '-q:v', '3', out + '-poster.jpg']);
if (opt('webm')) ff(['-i', out + '.mp4', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', out + '.webm']);
if (opt('gif')) ff(['-i', out + '.mp4', '-vf', 'fps=15,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse', out + '.gif']);
if (!opt('keep')) rmSync(fdir, { recursive: true, force: true });
console.log(`\nclip ${out}.mp4 (${n} frames, ${dur}s @ ${fps}fps, ${W}×${H})`);
process.exit(0);
