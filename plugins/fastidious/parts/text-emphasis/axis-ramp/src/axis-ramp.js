/*!
 * text-emphasis / axis-ramp — Fastidious parts library
 * Original work, MIT, Copyright (c) 2026 Jamie Acutt (Fastidious). See LICENSE.
 * Built from a written description of the technique (variable-font axes carrying meaning),
 * not from any site's code.
 *
 * Moves a display word along a variable font's weight and width axes so the type itself
 * carries the story: a friendship thinning, dough rising, a signal fading.
 *
 * Modes
 *   intro  letters settle from a start state to a per-letter ramp once the font has loaded
 *   enter  the same, played once when the word reaches the reading line
 *   scrub  the whole word travels between two states, bound to scroll progress
 *
 * Changing font axes reflows the text, so the part locks the element's box at the widest
 * state it will reach: nothing around it moves. Keep it to display words (maxChars).
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';
import { SplitText } from 'gsap/SplitText.js';

gsap.registerPlugin(ScrollTrigger, SplitText);

const DEFAULTS = {
  mode: 'enter',               // 'intro' | 'enter' | 'scrub'
  // intro / enter
  startState: { wght: 900, wdth: 100 },
  ramp: { wght: [900, 100], wdth: null }, // per-letter targets, interpolated first to last letter
  duration: 1.4,
  stagger: 0.07,
  ease: 'expo.out',
  delay: 0,
  start: 'top 85%',
  // scrub
  from: { wght: 900, wdth: 125, opacity: 1 },
  to: { wght: 120, wdth: 70, opacity: 0.4 },
  trigger: null,               // element whose scroll range drives the scrub (defaults to the word)
  scrubStart: 'top top',
  scrubEnd: 'bottom bottom',
  scrub: 0.4,
  // shared
  maxChars: 14,
  lockBox: true,
  fontTimeout: 3000,           // ms to wait for the variable font before giving up on motion
  reducedSteps: 3,             // scrub under reduced motion: jump between this many states
};

const lerp = (a, b, t) => a + (b - a) * t;
const pick = (pair, i, n, fallback) => {
  if (!pair) return fallback;
  if (typeof pair === 'number') return pair;
  return n < 2 ? pair[1] : lerp(pair[0], pair[1], i / (n - 1));
};

function applyState(el, s) {
  if (s.wght != null) el.style.setProperty('--ar-w', s.wght);
  if (s.wdth != null) el.style.setProperty('--ar-s', s.wdth);
  if (s.opacity != null) el.style.setProperty('--ar-o', s.opacity);
}

async function fontReady(el, timeout) {
  if (!document.fonts) return true;
  const cs = getComputedStyle(el);
  const spec = `900 ${cs.fontSize} ${cs.fontFamily}`;
  const load = document.fonts.load(spec).then((faces) => faces.length > 0).catch(() => false);
  const late = new Promise((r) => setTimeout(() => r(false), timeout));
  return Promise.race([load, late]);
}

export function mountAxisRamp(target, cfg = {}) {
  const el = typeof target === 'string' ? document.querySelector(target) : target;
  if (!el) throw new Error('axis-ramp: target not found');
  const o = {
    ...DEFAULTS, ...cfg,
    startState: { ...DEFAULTS.startState, ...cfg.startState },
    ramp: { ...DEFAULTS.ramp, ...cfg.ramp },
    from: { ...DEFAULTS.from, ...cfg.from },
    to: { ...DEFAULTS.to, ...cfg.to },
  };
  const text = (el.textContent || '').trim();
  const kept = { style: el.getAttribute('style') };
  el.classList.add('ar');
  const isBlock = /^(block|flex|grid|list-item|table)$/.test(getComputedStyle(el).display);
  if (!isBlock) el.classList.add('ar-inline');

  const baseWdth = () => o.startState.wdth ?? 100;
  let split = null;
  let chars = [];
  let mm = null;
  let resizeObs = null;
  let destroyed = false;
  let played = false;       // intro / enter only play once, even across a rebuild

  // Per-letter finishing states for intro / enter.
  const finals = () => chars.map((_, i) => ({
    wght: pick(o.ramp.wght, i, chars.length, o.startState.wght),
    wdth: pick(o.ramp.wdth, i, chars.length, baseWdth()),
  }));

  // Lock the box at the widest of the states the word will pass through.
  function lock(states) {
    if (!o.lockBox) return;
    el.style.inlineSize = '';
    el.style.blockSize = '';
    let w = 0, h = 0;
    for (const apply of states) {
      apply();
      const r = el.getBoundingClientRect();
      w = Math.max(w, r.width);
      h = Math.max(h, r.height);
    }
    // A block already owns its row, so only its height can disturb neighbours.
    // Inline words also lock their width, so the words beside them stay put.
    if (!isBlock) el.style.inlineSize = `${Math.ceil(w)}px`;
    else el.style.blockSize = `${Math.ceil(h)}px`;
  }

  function setChars(states) { chars.forEach((c, i) => applyState(c, states[i])); }

  function buildLetters() {
    if (text.length > o.maxChars) {
      console.warn(`axis-ramp: "${text.slice(0, 20)}…" is ${text.length} characters (max ${o.maxChars}); shown at its final ramp without motion.`);
    }
    split = SplitText.create(el, { type: 'chars', charsClass: 'ar-char', tag: 'span', aria: 'auto' });
    chars = split.chars;
    const startStates = chars.map(() => ({ ...o.startState }));
    lock([() => setChars(startStates), () => setChars(finals())]);
    return startStates;
  }

  async function run() {
    const ok = await fontReady(el, o.fontTimeout);
    if (destroyed) return;
    el.classList.add('ar-ready');

    mm = gsap.matchMedia();
    mm.add(
      { motion: '(prefers-reduced-motion: no-preference)', reduced: '(prefers-reduced-motion: reduce)' },
      ({ conditions }) => {
        const still = played || conditions.reduced || !ok || text.length > o.maxChars;

        if (o.mode === 'scrub') {
          lock([() => applyState(el, o.from), () => applyState(el, o.to)]);
          const state = { ...o.from };
          applyState(el, state);
          if (!ok) { applyState(el, o.from); return; }
          const st = {
            trigger: o.trigger || el, start: o.scrubStart, end: o.scrubEnd,
          };
          if (conditions.reduced) {
            const n = Math.max(2, o.reducedSteps);
            const t = ScrollTrigger.create({
              ...st,
              onRefresh: (self) => self.vars.onUpdate(self),
              onUpdate: (self) => {
                const q = Math.round(self.progress * (n - 1)) / (n - 1);
                applyState(el, {
                  wght: lerp(o.from.wght, o.to.wght, q),
                  wdth: lerp(o.from.wdth, o.to.wdth, q),
                  opacity: lerp(o.from.opacity, o.to.opacity, q),
                });
              },
            });
            return () => t.kill();
          }
          const tw = gsap.to(state, {
            ...o.to, ease: 'none',
            onUpdate: () => applyState(el, state),
            scrollTrigger: { ...st, scrub: o.scrub },
          });
          return () => { tw.scrollTrigger?.kill(); tw.kill(); };
        }

        // intro / enter
        buildLetters();
        const end = finals();
        if (still) { setChars(end); return () => split?.revert(); }

        const proxies = chars.map(() => ({ ...o.startState }));
        setChars(proxies);
        const tl = gsap.timeline({
          delay: o.mode === 'intro' ? o.delay : 0,
          paused: o.mode === 'enter',
          onStart: () => { played = true; },
        });
        proxies.forEach((p, i) => {
          tl.to(p, {
            wght: end[i].wght, wdth: end[i].wdth,
            duration: o.duration, ease: o.ease,
            onUpdate: () => applyState(chars[i], p),
          }, i * o.stagger);
        });
        let trig = null;
        if (o.mode === 'enter') {
          trig = ScrollTrigger.create({ trigger: el, start: o.start, once: true, onEnter: () => tl.play() });
        }
        return () => { trig?.kill(); tl.kill(); split?.revert(); split = null; chars = []; };
      },
    );

    // Re-measure the locked box when the layout changes size.
    if (o.lockBox && 'ResizeObserver' in window && el.parentElement) {
      let last = el.parentElement.clientWidth;
      resizeObs = new ResizeObserver(() => {
        const w = el.parentElement.clientWidth;
        if (Math.abs(w - last) < 2) return;
        last = w;
        mm?.revert();
        run.rebuild?.();
      });
      resizeObs.observe(el.parentElement);
    }
  }

  // A rebuild is a fresh mount of the same element with the same options.
  run.rebuild = () => {
    if (destroyed) return;
    resizeObs?.disconnect();
    el.style.inlineSize = ''; el.style.blockSize = '';
    run();
  };

  const ready = run();

  return {
    ready,
    destroy() {
      destroyed = true;
      resizeObs?.disconnect();
      mm?.revert();
      split?.revert();
      kept.style == null ? el.removeAttribute('style') : el.setAttribute('style', kept.style);
      el.classList.remove('ar', 'ar-ready', 'ar-inline');
    },
  };
}
