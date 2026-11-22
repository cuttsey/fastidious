/*!
 * index-to-detail / push — Fastidious parts library
 * Adapted from "Grid Item Push Animation" by Codrops (MIT), https://github.com/codrops/PushGridItems
 * Copyright (c) 2009 - 2024 Codrops. See LICENSE. Based on a concept by Rémi Clauss.
 * Changes: rebuilt on the index-to-detail markup contract shared with `echo-trail` and `flip`;
 * neighbours are pushed with transforms instead of re-placed in the CSS grid, so any grid layout
 * works; focus moves into the detail and back, Escape closes, reduced motion fades instead.
 */
import { gsap } from 'gsap';
import { Flip } from 'gsap/Flip.js';

gsap.registerPlugin(Flip);

const DEFAULTS = {
  items: '.et-item',
  chrome: [],
  duration: 0.9,
  ease: 'expo.out',
  gap: 24,          // px clear of the viewport edge once pushed
  onOpen: null,
};

// Where an item sits relative to the opened one decides which way it is pushed.
function pushVector(r, c, gap) {
  const vw = innerWidth, vh = innerHeight;
  if (r.bottom <= c.top) return { x: 0, y: -(r.bottom + gap) };      // above: off the top
  if (r.top >= c.bottom) return { x: 0, y: vh - r.top + gap };        // below: off the bottom
  if (r.right <= c.left) return { x: -(r.right + gap), y: 0 };        // left: off the left
  if (r.left >= c.right) return { x: vw - r.left + gap, y: 0 };       // right: off the right
  return { x: 0, y: 0 };
}

export function mountPush({ grid, panel, ...cfg }) {
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
  const done = () => { busy = false; open = true; closeBtn?.focus({ preventScroll: true }); };

  const openItem = (item) => {
    if (busy || open) return;
    busy = true; current = item; lock(true);
    const img = item.querySelector('img');
    panelImg.src = img.currentSrc || img.src; panelImg.alt = img.alt;
    o.onOpen?.(item, panel);
    interactive(true);

    if (reduced()) {
      gsap.set(panelImg, { clipPath: 'none' });
      gsap.to([...items, ...o.chrome], { opacity: 0, duration: 0.3 });
      gsap.fromTo(panel, { opacity: 0 }, { opacity: 1, pointerEvents: 'auto', duration: 0.4, delay: 0.15, onComplete: done });
      gsap.set(panelBody, { opacity: 1, y: 0 });
      return;
    }

    img.dataset.flipId = panelImg.dataset.flipId = 'et-shared';
    const state = Flip.getState(img);
    gsap.set(panel, { opacity: 1, pointerEvents: 'auto', backgroundColor: 'transparent' });
    gsap.set(panelImg, { clipPath: 'none' });
    gsap.set(panelBody, { opacity: 0, y: 20 });
    gsap.set(img, { opacity: 0 });
    const others = items.filter((el) => el !== item);
    const c = item.getBoundingClientRect();
    others.forEach((el) => { el._pgv = pushVector(el.getBoundingClientRect(), c, o.gap); });
    gsap.timeline()
      .call(done, null, o.duration * 0.8) // the panel is usable as soon as the picture has nearly landed
      .to(others, { x: (i, el) => el._pgv.x, y: (i, el) => el._pgv.y, duration: o.duration, ease: o.ease }, 0)
      .to(o.chrome, { opacity: 0, duration: 0.35 }, 0)
      .add(Flip.from(state, { targets: panelImg, duration: o.duration, ease: o.ease, scale: true }), 0.05)
      .to(panel, { backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--et-panel-bg').trim() || '#fff', duration: 0.45 }, o.duration * 0.75)
      .to(panelBody, { opacity: 1, y: 0, duration: 0.8, ease: 'expo' }, o.duration * 0.6);
  };

  const close = () => {
    if (busy || !open) return;
    busy = true;
    interactive(false);
    current.focus({ preventScroll: true });
    const img = current.querySelector('img');
    const back = () => {
      gsap.set(panel, { opacity: 0, pointerEvents: 'none', clearProps: 'backgroundColor' });
      gsap.set(panelImg, { clearProps: 'all' });
      gsap.set(img, { opacity: 1 });
      busy = false; open = false; lock(false);
    };
    if (reduced()) {
      gsap.timeline({ onComplete: back }).to(panel, { opacity: 0, duration: 0.3 }).to([...items, ...o.chrome], { opacity: 1, duration: 0.3 });
      return;
    }
    gsap.to(panelBody, { opacity: 0, y: 20, duration: 0.25, ease: 'power2.in', onComplete: () => {
      // Hand the picture back: capture where it is in the panel, hide the panel, fly the grid's own image home.
      const state = Flip.getState(panelImg);
      gsap.set(panel, { opacity: 0, pointerEvents: 'none', clearProps: 'backgroundColor' });
      gsap.set(img, { opacity: 1 });
      gsap.set(current, { position: 'relative', zIndex: 5 });
      gsap.timeline({ onComplete: () => { gsap.set(current, { clearProps: 'position,zIndex' }); back(); } })
        .add(Flip.from(state, { targets: img, duration: o.duration * 0.85, ease: o.ease, scale: true }), 0)
        .to(items.filter((el) => el !== current), { x: 0, y: 0, duration: o.duration, ease: o.ease }, 0)
        .to(o.chrome, { opacity: 1, duration: 0.4 }, 0.3);
    } });
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
