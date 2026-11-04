// supermock capture: record a finished page as stills or a scroll frame sequence, at a device's viewport.
// node capture.mjs <url> --out <dir> [--device phone|tablet|laptop|desktop|WxH] [--dsf 2]
//                  [--scroll <seconds>] [--fps 30] [--to <px|end|selector>] [--from <px|selector>] [--hold 0.6]
//                  [--still] [--full] [--hover]
//                  [--play <seconds> --steps <steps.json>]
// --play records a page that is used, not scrolled (a map, a configurator, an app screen): steps.json is
// [{ "at": seconds, "js": "code run in the page" }, …]. Time is virtual, so tweens, timers and CSS
// transitions advance exactly one frame per capture and the clip is smooth whatever the machine's speed.
// --scroll records frames while scrolling (scroll-linked animation plays, as a visitor would see it).
// --still saves one fold screenshot; --full saves a full-page image (for a long scroll inside a device).
import { mkdirSync, writeFileSync } from 'node:fs';
import { Browser, sleep } from '../../design-taste-frontend/scripts/lib/cdp.mjs';
const a = process.argv.slice(2), url = a[0];
const opt = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : (a[i + 1] && !a[i + 1].startsWith('--') ? a[i + 1] : true); };
const DEV = { phone: [390, 844, 3, true], tablet: [834, 1194, 2, true], laptop: [1440, 900, 2, false], desktop: [1920, 1080, 1, false] };
let [w, h, dsf, mobile] = DEV[opt('device', 'laptop')] || [...String(opt('device')).split('x').map(Number), 1, false];
dsf = Number(opt('dsf', dsf)); const out = opt('out', 'supermock/capture'); mkdirSync(out, { recursive: true });
const b = await Browser.launch();
const p = await b.newPage({ width: w, height: h, dsf, mobile });
if (opt('hover')) await p.send('Emulation.setEmulatedMedia', { features: [{ name: 'hover', value: 'hover' }, { name: 'pointer', value: 'fine' }] });
await p.goto(url, { settleMs: 1200 });
await p.eval(`document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); document.fonts.ready.then(() => 1)`); await sleep(800);
const pos = async (v, dflt) => { if (v === undefined || v === true) return dflt; if (v === 'end') return p.eval('document.documentElement.scrollHeight - innerHeight');
  if (/^\d+$/.test(v)) return Number(v); return p.eval(`(() => { const e = document.querySelector(${JSON.stringify(v)}); return e ? Math.round(e.getBoundingClientRect().top + scrollY - 72) : 0 })()`); };
const meta = { url, w, h, dsf };
if (opt('still')) { await p.screenshot({ path: `${out}/still.png`, format: 'png' }); meta.still = 'still.png'; }
if (opt('full')) { await p.screenshot({ path: `${out}/full.png`, format: 'png', fullPage: true }); meta.full = 'full.png'; meta.fullHeight = await p.eval('document.documentElement.scrollHeight'); }
const secs = Number(opt('scroll', 0));
if (secs) {
  const fps = Number(opt('fps', 30)), hold = Number(opt('hold', 0.6)), n = Math.round(secs * fps);
  const y0 = await pos(opt('from'), 0), y1 = await pos(opt('to'), 'end' === 'end' ? await p.eval('document.documentElement.scrollHeight - innerHeight') : 0);
  const ease = (t) => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  mkdirSync(`${out}/frames`, { recursive: true });
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1), hn = hold / secs;                       // hold still at both ends
    const k = t < hn ? 0 : t > 1 - hn ? 1 : ease((t - hn) / (1 - 2 * hn));
    await p.eval(`scrollTo(0, ${Math.round(y0 + (y1 - y0) * k)}); null`);
    await sleep(70);                                              // let scroll handlers and transitions settle a frame
    await p.screenshot({ path: `${out}/frames/f${String(i).padStart(4, '0')}.png`, format: 'png' });
  }
  Object.assign(meta, { frames: 'frames', count: n, fps });
}
const play = Number(opt('play', 0));
if (play) {
  const fps = Number(opt('fps', 30)), n = Math.round(play * fps), dt = 1000 / fps;
  const steps = JSON.parse((await import('node:fs')).readFileSync(opt('steps'), 'utf8')).sort((x, y) => x.at - y.at);
  mkdirSync(`${out}/frames`, { recursive: true });
  const advance = (ms) => new Promise((res) => { const off = b.on(p.sessionId, 'Emulation.virtualTimeBudgetExpired', () => { off(); res(); });
    p.send('Emulation.setVirtualTimePolicy', { policy: 'advance', budget: ms }); });
  await p.send('Emulation.setVirtualTimePolicy', { policy: 'pause' });
  let s = 0;
  for (let i = 0; i < n; i++) {
    const t = i / fps;
    while (s < steps.length && steps[s].at <= t) await p.eval(`(() => { ${steps[s++].js} })(); null`);
    await advance(dt);
    // A frame can stall while paused (an image decoding after a step); let real time run briefly, then retry.
    let shot = null;
    for (let k = 0; !shot && k < 6; k++) {
      shot = await b.send('Page.captureScreenshot', { format: 'png' }, p.sessionId, 2500).catch(() => null);
      if (!shot) { await p.send('Emulation.setVirtualTimePolicy', { policy: 'advance' }); await sleep(250); await p.send('Emulation.setVirtualTimePolicy', { policy: 'pause' }); }
    }
    if (!shot) throw new Error('frame ' + i + ' would not capture');
    writeFileSync(`${out}/frames/f${String(i).padStart(4, '0')}.png`, Buffer.from(shot.data, 'base64'));
  }
  Object.assign(meta, { frames: 'frames', count: n, fps, steps: steps.length });
}
writeFileSync(`${out}/capture.json`, JSON.stringify(meta, null, 2));
await b.close(); console.log(JSON.stringify(meta)); process.exit(0);
