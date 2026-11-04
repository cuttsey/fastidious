#!/usr/bin/env node
/*
  legibility-check: measures every line of rendered text against the pixels actually behind its letters.

  Why: rule-based checkers (axe-core's color-contrast and the hooks built on it) compare text with the
  CSS background of its ancestors. They do not flag text over background images, overlapping elements or
  pseudo-elements, so white text crossing a white stripe drawn by ::after passes them. This check renders
  each screen three times: with all text forced black, forced white, and transparent. Where the black and
  white renders differ is exactly where the letters are, even where the real text has vanished into a
  same-coloured backdrop. It then computes WCAG contrast between the real text colour and the transparent
  render (the true backdrop) at those pixels. Runs with reduced motion so the page is at rest.

  Fails a line when more than 3% of its glyph pixels sit on a backdrop below 4.5:1, or 3:1 for large text
  (24px and up, or 18.66px and up at weight 700). Exit code 1 on any failure, so it can gate a hook or CI.

  Usage: node legibility-check.js <url> [--widths 390,1110,1440] [--heights 700,900] [--full] [--setup "<js run before each pass>"]
  Each --setup expression may change the page state (for example, switch a theme); separate several with ' ;; '.
*/
const {chromium} = require('playwright');
const {PNG} = require('pngjs');

const args = process.argv.slice(2);
const url = args[0];
const opt = (k, d) => { const i = args.indexOf(k); return i < 0 ? d : args[i + 1]; };
const widths = opt('--widths', '390,1110,1440').split(',').map(Number);
const heights = opt('--heights', '700,900').split(',').map(Number);
const full = args.includes('--full');
const setups = (opt('--setup', '') || '').split(' ;; ').filter(Boolean);
if (!url) { console.error('Usage: node legibility-check.js <url> [--widths ...] [--full] [--setup "..."]'); process.exit(2); }

const paint = c => `*,*::before,*::after{color:${c}!important;-webkit-text-fill-color:${c}!important;text-shadow:none!important;text-decoration-color:transparent!important;caret-color:transparent!important}`;
const HIDE = paint('transparent'), BLACK = paint('#000'), WHITE = paint('#fff');

function lum(r, g, b) { const f = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); }
function ratio(a, b) { return (Math.max(a, b) + .05) / (Math.min(a, b) + .05); }

async function runs(page) {
  return page.evaluate(() => {
    const out = [], vw = innerWidth, vh = innerHeight;
    const bars = [...document.querySelectorAll('body *')].filter(e => { const p = getComputedStyle(e).position; return (p === 'fixed' || p === 'sticky') && e.offsetWidth; }).map(e => ({ el: e, r: e.getBoundingClientRect() }));
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => n.textContent.trim() ? 1 : 2 });
    let n;
    while ((n = w.nextNode())) {
      const el = n.parentElement; if (!el || el.closest('script,style,noscript,[hidden]')) continue;
      const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
      const m = cs.color.match(/[\d.]+/g).map(Number); if (m.length > 3 && m[3] < .99) continue;
      const fs = parseFloat(cs.fontSize), big = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) {
        if (r.width < 2 || r.height < 2 || r.top < 0 || r.left < 0 || r.bottom > vh || r.right > vw) continue;
        // Pixels of text scrolled underneath a fixed or sticky bar are covered on purpose and skipped;
        // the bar's own text is checked as text in its own right.
        const skip = bars.filter(b => !b.el.contains(el)).map(b => b.r).filter(b => b.right > r.left && b.left < r.right && b.bottom > r.top && b.top < r.bottom).map(b => [b.left, b.top, b.right, b.bottom]);
        out.push({ t: n.textContent.trim().slice(0, 48), x: Math.floor(r.left), y: Math.floor(r.top), w: Math.ceil(r.width), h: Math.ceil(r.height), c: m.slice(0, 3), need: big ? 3 : 4.5, skip });
      }
    }
    return out;
  });
}

// k1: text forced black, k2: text forced white, b: text transparent. Glyph pixels are where k1 and k2 differ,
// which finds the letters even where the real text colour matches its backdrop and they have vanished.
function analyse(k1, k2, b, list) {
  const bad = [];
  for (const r of list) {
    const L = lum(...r.c); let n = 0, low = 0, worst = 99;
    for (let y = r.y; y < Math.min(r.y + r.h, b.height); y++) for (let x = r.x; x < Math.min(r.x + r.w, b.width); x++) {
      if (r.skip.some(s => x >= s[0] && x < s[2] && y >= s[1] && y < s[3])) continue;
      const i = (b.width * y + x) << 2;
      if (Math.abs(k1.data[i] - k2.data[i]) + Math.abs(k1.data[i + 1] - k2.data[i + 1]) + Math.abs(k1.data[i + 2] - k2.data[i + 2]) < 240) continue;
      n++; const c = ratio(L, lum(b.data[i], b.data[i + 1], b.data[i + 2]));
      if (c < r.need) { low++; if (c < worst) worst = c; }
    }
    if (n >= 30 && low / n > .03) bad.push(`${r.t} | ${Math.round(100 * low / n)}% of glyphs below ${r.need}:1, worst ${worst.toFixed(2)}:1`);
  }
  return bad;
}

(async () => {
  const browser = await chromium.launch(); let failures = 0, passes = 0;
  for (const w of widths) for (const vh of heights) {
    const page = await browser.newPage({ viewport: { width: w, height: vh }, reducedMotion: 'reduce' });
    await page.goto(url, { waitUntil: 'load' }); await page.waitForTimeout(1200);
    for (const setup of (setups.length ? setups : [''])) {
      if (setup) { await page.evaluate(setup); await page.waitForTimeout(900); }
      const H = await page.evaluate(() => document.documentElement.scrollHeight);
      // Screens overlap by half, so a line that straddles one screen's edge is whole on the next.
      const step = Math.floor(vh / 2), stops = full ? Array.from({ length: Math.ceil(H / step) }, (_, i) => i * step) : [0];
      const found = [];
      for (const y of stops) {
        await page.evaluate(y => { document.documentElement.style.scrollBehavior = 'auto'; scrollTo(0, y); }, y);
        await page.waitForTimeout(250);
        const list = await runs(page);
        // Wait two animation frames after each style change, or the screenshot can capture the previous paint.
        const frames = () => page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
        const shot = async css => { const st = await page.addStyleTag({ content: css }); await frames(); const p = PNG.sync.read(await page.screenshot({ animations: 'disabled' })); await st.evaluate(e => e.remove()); await frames(); return p; };
        const k1 = await shot(BLACK), k2 = await shot(WHITE), b = await shot(HIDE);
        found.push(...analyse(k1, k2, b, list));
      }
      const label = `${w}×${vh}${setup ? ' · ' + setup : ''}`;
      if (found.length) { failures++; console.log(`FAIL ${label}`); [...new Set(found)].slice(0, 6).forEach(f => console.log('   ' + f)); }
      else passes++;
    }
    await page.close();
  }
  console.log(`legibility-check: ${passes} passed, ${failures} failed`);
  await browser.close(); process.exit(failures ? 1 : 0);
})();
