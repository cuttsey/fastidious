/*!
 * process-curve — Fastidious parts library. Original part (MIT), built from WANTED.md:
 * "a single process curve (a roast, a tide, a build) that draws as the reader scrolls, with one live readout".
 * The curve is drawn from the business's real data points; nothing is smoothed into a shape the data
 * does not have. A hidden table carries the same data for screen readers.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';

gsap.registerPlugin(ScrollTrigger);

const DEFAULTS = {
  data: [],                 // [[x, y], ...] in real units, x increasing
  xLabel: 'Time', yLabel: 'Value',
  formatX: (x) => String(x),
  formatY: (y) => String(y),
  marks: [],                // [{ x, label }] moments worth naming (first crack, high tide)
  width: 1000, height: 420, pad: 28,
  start: 'top 70%', end: 'bottom 40%',
  scrub: 0.4,
  title: '',
};

export function mountProcessCurve(el, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  if (o.data.length < 2) throw new Error('process-curve needs at least two real data points');
  const xs = o.data.map((d) => d[0]), ys = o.data.map((d) => d[1]);
  const [x0, x1] = [Math.min(...xs), Math.max(...xs)], [y0, y1] = [Math.min(...ys), Math.max(...ys)];
  const W = o.width, H = o.height, P = o.pad;
  const sx = (x) => P + ((x - x0) / (x1 - x0 || 1)) * (W - P * 2);
  const sy = (y) => H - P - ((y - y0) / (y1 - y0 || 1)) * (H - P * 2);
  const d = o.data.map(([x, y], i) => `${i ? 'L' : 'M'}${sx(x).toFixed(1)},${sy(y).toFixed(1)}`).join(' ');
  const yAt = (x) => { // straight-line interpolation between real points only
    for (let i = 1; i < o.data.length; i++) {
      const [ax, ay] = o.data[i - 1], [bx, by] = o.data[i];
      if (x <= bx) return ay + (by - ay) * ((x - ax) / (bx - ax || 1));
    }
    return ys[ys.length - 1];
  };

  el.classList.add('pc');
  el.innerHTML = `
    <div class="pc-readout" aria-hidden="true"><span class="pc-y"></span><span class="pc-x"></span></div>
    <svg class="pc-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.title || `${o.yLabel} over ${o.xLabel}`}">
      <line class="pc-axis" x1="${P}" y1="${H - P}" x2="${W - P}" y2="${H - P}"/>
      ${o.marks.map((m) => `<g class="pc-mark"><line x1="${sx(m.x)}" y1="${P}" x2="${sx(m.x)}" y2="${H - P}"/><text x="${sx(m.x) + 6}" y="${P + 12}">${m.label}</text></g>`).join('')}
      <path class="pc-ghost" d="${d}"/>
      <path class="pc-line" d="${d}"/>
      <circle class="pc-dot" r="6" cx="${sx(xs[0])}" cy="${sy(ys[0])}"/>
    </svg>
    <table class="pc-table"><caption>${o.title || ''}</caption><thead><tr><th scope="col">${o.xLabel}</th><th scope="col">${o.yLabel}</th></tr></thead>
      <tbody>${o.data.map(([x, y]) => `<tr><td>${o.formatX(x)}</td><td>${o.formatY(y)}</td></tr>`).join('')}</tbody></table>`;

  const line = el.querySelector('.pc-line'), dot = el.querySelector('.pc-dot');
  const ry = el.querySelector('.pc-y'), rx = el.querySelector('.pc-x');
  const len = line.getTotalLength();
  const marks = [...el.querySelectorAll('.pc-mark')];
  const show = (p) => {
    const x = x0 + (x1 - x0) * p, y = yAt(x);
    line.style.strokeDashoffset = String(len * (1 - p));
    dot.setAttribute('cx', sx(x).toFixed(1));
    dot.setAttribute('cy', sy(y).toFixed(1));
    ry.textContent = o.formatY(y);
    rx.textContent = o.formatX(x);
    marks.forEach((m, i) => m.classList.toggle('pc-on', x >= o.marks[i].x));
  };
  line.style.strokeDasharray = String(len);

  const mm = gsap.matchMedia();
  mm.add({ motion: '(prefers-reduced-motion: no-preference)', reduced: '(prefers-reduced-motion: reduce)' }, ({ conditions }) => {
    if (conditions.reduced) { show(1); return; }
    show(0);
    const st = ScrollTrigger.create({ trigger: el, start: o.start, end: o.end, scrub: o.scrub, onUpdate: (s) => show(s.progress) });
    return () => st.kill();
  });
  return { show, destroy: () => mm.revert() };
}
