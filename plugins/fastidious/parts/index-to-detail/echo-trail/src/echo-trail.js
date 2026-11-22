/*!
 * index-to-detail / echo-trail — Fastidious parts library
 * Adapted from "Repeating Image Transition" by Codrops (MIT), https://github.com/codrops/RepeatingImageTransition
 * Copyright (c) 2009 - 2026 Codrops. See LICENSE.
 * Changes: rebuilt as a module that takes its grid, items and panel from the host; images read from
 * <img> elements instead of inline background styles; the WebGL "silk" and "ink" surfaces are removed
 * (flat echoes only, rung 2); timings, steps and path are inputs; the keyboard, focus, inert and
 * reduced-motion behaviour of the original is kept; scroll locking no longer assumes Lenis.
 */
import { gsap } from 'gsap';

const CLIPS = {
  'top-bottom': { from: 'inset(100% 0% 0% 0%)', reveal: 'inset(0% 0% 0% 0%)', hide: 'inset(0% 0% 100% 0%)' },
  'bottom-top': { from: 'inset(0% 0% 100% 0%)', reveal: 'inset(0% 0% 0% 0%)', hide: 'inset(100% 0% 0% 0%)' },
  'left-right': { from: 'inset(0% 100% 0% 0%)', reveal: 'inset(0% 0% 0% 0%)', hide: 'inset(0% 0% 0% 100%)' },
  'right-left': { from: 'inset(0% 0% 0% 100%)', reveal: 'inset(0% 0% 0% 0%)', hide: 'inset(0% 100% 0% 0%)' },
};

const DEFAULTS = {
  items: '.et-item',            // clickable items inside the grid; each holds an <img> and a caption
  chrome: [],                   // elements to fade while the panel is open (header, filters)
  direction: 'top-bottom',
  steps: 6,                     // echoes between the item and the panel
  stepDuration: 0.35,
  stepInterval: 0.05,
  pause: 0.14,                  // how long each echo holds before it wipes away
  path: 'linear',               // 'linear' or 'sine'
  sineAmplitude: 50,
  enterEase: 'sine.in',
  exitEase: 'sine',
  revealEase: 'sine.inOut',
  revealFactor: 2,
  staggerFactor: 0.3,           // other items fade out by distance from the clicked one
  onOpen: null,                 // (item, panel) => void — fill the panel's content from the item
};

const lerp = (a, b, t) => a + (b - a) * t;
const centre = (r) => ({ x: r.left + r.width / 2, y: r.top + r.height / 2 });

export function mountEchoTrail({ grid, panel, ...cfg }) {
  const o = { ...DEFAULTS, ...cfg };
  const items = [...grid.querySelectorAll(o.items)];
  const panelImg = panel.querySelector('.et-panel-img');
  const panelBody = panel.querySelector('.et-panel-body');
  const closeBtn = panel.querySelector('.et-close');
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let busy = false, open = false, current = null;

  panel.inert = true;
  const lock = (on) => document.documentElement.classList.toggle('et-locked', on);
  const interactive = (on) => { panel.inert = !on; grid.inert = on; o.chrome.forEach((el) => (el.inert = on)); };

  const delays = (clicked) => {
    const c = centre(clicked.getBoundingClientRect());
    const d = items.map((el) => { const e = centre(el.getBoundingClientRect()); return Math.hypot(e.x - c.x, e.y - c.y); });
    const max = Math.max(...d) || 1;
    return d.map((v) => (v / max) * o.staggerFactor);
  };

  const pathBetween = (a, b) => {
    const pts = [], n = o.steps + 2, ca = centre(a), cb = centre(b);
    for (let i = 0; i < n; i++) {
      const t = i / (n - 1), w = lerp(a.width, b.width, t), h = lerp(a.height, b.height, t);
      const s = o.path === 'sine' ? Math.sin(t * Math.PI) * o.sineAmplitude : 0;
      pts.push({ left: lerp(ca.x, cb.x, t) - w / 2, top: lerp(ca.y, cb.y, t) - h / 2 + s, width: w, height: h });
    }
    return pts.slice(1, -1);
  };

  const done = () => { busy = false; open = true; closeBtn?.focus({ preventScroll: true }); };

  const openItem = (item) => {
    if (busy || open) return;
    busy = true; current = item; lock(true);
    const img = item.querySelector('img');
    panelImg.src = img.currentSrc || img.src; panelImg.alt = img.alt;
    o.onOpen?.(item, panel);
    interactive(true);
    const clip = CLIPS[o.direction];

    if (reduced()) {
      gsap.to([...items, ...o.chrome], { opacity: 0, duration: 0.4 });
      gsap.set(panelImg, { clipPath: clip.reveal }); gsap.set(panelBody, { opacity: 1, y: 0 });
      gsap.fromTo(panel, { opacity: 0 }, { opacity: 1, duration: 0.4, delay: 0.2, onComplete: done });
      return;
    }

    const ds = delays(item);
    gsap.to(o.chrome, { opacity: 0, duration: 0.5, ease: 'sine.inOut' });
    gsap.to(items, {
      opacity: 0,
      scale: (i, el) => (el === item ? 1 : 0.8),
      clipPath: (i, el) => (el === item ? clip.from : 'none'),
      duration: (i, el) => (el === item ? o.stepDuration * 2 : 0.3),
      ease: 'sine',
      delay: (i) => ds[i],
    });

    const src = `url("${panelImg.src}")`;
    const movers = pathBetween(item.querySelector('img').getBoundingClientRect(), panelImg.getBoundingClientRect()).map((s, i) => {
      const m = document.createElement('div');
      m.className = 'et-mover';
      m.setAttribute('aria-hidden', 'true');
      gsap.set(m, { position: 'fixed', left: s.left, top: s.top, width: s.width, height: s.height, backgroundImage: src, clipPath: clip.from, zIndex: 1000 + i });
      document.body.appendChild(m);
      gsap.timeline({ delay: i * o.stepInterval, onComplete: () => m.remove() })
        .fromTo(m, { opacity: 0.4, clipPath: clip.hide }, { opacity: 1, clipPath: clip.reveal, duration: o.stepDuration, ease: o.enterEase })
        .to(m, { clipPath: clip.from, duration: o.stepDuration, ease: o.exitEase }, `+=${o.pause}`);
      return m;
    });

    gsap.set(panelBody, { opacity: 0 });
    gsap.set(panel, { opacity: 1, pointerEvents: 'auto' });
    const wait = movers.length * o.stepInterval;
    gsap.timeline({ defaults: { duration: o.stepDuration * o.revealFactor, ease: o.revealEase } })
      .fromTo(panelImg, { clipPath: clip.hide }, { clipPath: clip.reveal, delay: wait })
      .fromTo(panelBody, { y: 25 }, { duration: 1, ease: 'expo', opacity: 1, y: 0, delay: wait, onComplete: done }, '<-=.2');
  };

  const close = () => {
    if (busy || !open) return;
    busy = true;
    interactive(false);
    current.focus({ preventScroll: true });
    const ds = delays(current);
    gsap.timeline({ defaults: { duration: o.stepDuration, ease: 'expo' }, onComplete: () => { busy = false; open = false; lock(false); } })
      .to(panel, { opacity: 0 })
      .to(o.chrome, { opacity: 1, duration: 0.5 }, 0)
      .set(panel, { pointerEvents: 'none' })
      .set(panelImg, { clipPath: 'inset(0% 0% 100% 0%)' })
      .set(items, { clipPath: 'none', opacity: 0, scale: reduced() ? 1 : 0.8 }, 0)
      .to(items, { opacity: 1, scale: 1, delay: (i) => ds[i] }, '>');
  };

  const onKey = (e) => { if (e.key === 'Escape' && open && !busy) close(); };
  items.forEach((item) => {
    if (!item.matches('a, button')) { item.tabIndex = 0; item.setAttribute('role', 'button'); }
    item.addEventListener('click', (e) => { e.preventDefault(); openItem(item); });
    item.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openItem(item); } });
  });
  closeBtn?.addEventListener('click', (e) => { e.preventDefault(); close(); });
  document.addEventListener('keydown', onKey);

  return { open: openItem, close, destroy: () => document.removeEventListener('keydown', onKey) };
}
