#!/usr/bin/env node
/*
  reel-capture: films a live web page as frame-exact footage for a reel.

  Screen recording drops frames and stutters. This takes over the page's clock instead: JavaScript time
  (requestAnimationFrame, timers, performance.now, so GSAP and Lenis too) is advanced exactly one frame
  at a time, CSS animations and transitions are stepped through the Web Animations API, and videos are
  seeked, so every frame is rendered on schedule and the result is identical on every run.

  Usage:
    node reel-capture.js <url> <out.mp4> [--w 1920] [--h 1080] [--dpr 1] [--fps 60] [--dur 4]
      [--from 0] [--to 0] [--ease inout|linear|out] [--settle 0] [--hold 0] [--setup "<js>"]

  --from/--to   scroll positions in px; a CSS selector also works (its top edge). Equal values film a still scroll.
  --settle ms   time to run before frame 0, so intro animations can finish (or 0 to film the intro).
  --hold s      extra seconds held at the end of the move, still advancing time.
  --setup js    run after load, before filming (switch a theme, open a panel, hide a cookie banner).
  Writes to a temporary name and renames on success, so a stopped run never leaves a playable partial file.
  Not covered: sound, cross-origin iframes, and anything driven by a clock other than the page's own
  (a live data feed, a server-sent stream). Needs playwright and ffmpeg.
*/
const {chromium} = require('playwright');
const {spawn} = require('child_process');
const fs = require('fs');

const a = process.argv.slice(2), url = a[0], out = a[1];
const o = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : a[i + 1]; };
if (!url || !out) { console.error('Usage: node reel-capture.js <url> <out.mp4> [options]'); process.exit(2); }
const W = +o('w', 1920), H = +o('h', 1080), DPR = +o('dpr', 1), FPS = +o('fps', 60);
const DUR = +o('dur', 4), HOLD = +o('hold', 0), SETTLE = +o('settle', 0), EASE = o('ease', 'inout'), SETUP = o('setup', '');
const ease = { linear: t => t, out: t => 1 - Math.pow(1 - t, 3), inout: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 }[EASE];
const dt = 1000 / FPS;

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  const page = await ctx.newPage();
  // The faked clock still runs in real time until paused; pause it so JavaScript time moves only when stepped.
  const T0 = Date.UTC(2026, 0, 1);
  await page.clock.install({ time: T0 }); await page.clock.pauseAt(T0 + 1000);
  await page.goto(url, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  // Decode every image before filming, so no frame catches one half-decoded or at draft quality.
  await page.evaluate(() => Promise.all([...document.images].map(i => { i.loading = 'eager'; return i.decode().catch(() => {}); })));
  await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
  if (SETUP) await page.evaluate(SETUP);
  // CSS animations and transitions run on the browser's real timeline. Claim each one the first time it is
  // seen, wind it back to its start and pause it; from then on it moves only when stepped, one frame at a time.
  const claim = () => page.evaluate(() => { const s = window.__reelSeen || (window.__reelSeen = new WeakSet());
    for (const an of document.getAnimations()) if (!s.has(an)) { s.add(an); an.pause(); an.currentTime = 0; } });
  await claim();
  const step = ms => page.evaluate(ms => { const s = window.__reelSeen;
    for (const an of document.getAnimations()) { if (!s.has(an)) { s.add(an); an.pause(); an.currentTime = 0; } an.currentTime = (an.currentTime || 0) + ms; }
    for (const v of document.querySelectorAll('video')) { v.pause(); v.currentTime = (v.currentTime || 0) + ms / 1000; }
  }, ms);
  // Scroll reveals use IntersectionObserver, whose callbacks follow the browser's real rendering, not the
  // faked clock. After each scroll, wait out two rendering updates (seen through a fresh observer's first
  // callback), so every reveal the scroll triggered has run and its transition starts on this frame.
  const scrollTo = y => page.evaluate(async y => { scrollTo(0, y);
    const update = () => new Promise(r => { const io = new IntersectionObserver(() => { io.disconnect(); r(); }); io.observe(document.documentElement); });
    await update(); await update(); }, y);
  const pos = v => isNaN(+v) ? page.evaluate(s => { const e = document.querySelector(s); return e ? e.getBoundingClientRect().top + scrollY : 0; }, v) : +v;
  const from = await pos(o('from', '0')), to = await pos(o('to', String(o('from', '0'))));
  await scrollTo(from);
  for (let t = 0; t < SETTLE; t += dt) { await page.clock.runFor(dt); await step(dt); }

  const tmp = out.replace(/\.mp4$/, '') + '.part.mp4';
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-vf', `scale=${W * DPR}:${H * DPR}:flags=lanczos,format=yuv420p`, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-g', String(FPS), '-r', String(FPS), '-movflags', '+faststart', tmp],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg exited ' + c))));
  const n = Math.max(1, Math.round(DUR * FPS)), total = n + Math.round(HOLD * FPS);
  for (let i = 0; i < total; i++) {
    const t = Math.min(1, n === 1 ? 1 : i / (n - 1));
    await scrollTo(from + (to - from) * ease(t));
    await page.clock.runFor(dt); await step(dt);
    const jpg = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(jpg)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await done; fs.renameSync(tmp, out);
  console.log(`reel-capture: ${out} · ${total} frames · ${W * DPR}x${H * DPR} at ${FPS}fps`);
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
