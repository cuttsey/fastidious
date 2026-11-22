/*!
 * view-change / pixel-cover — Fastidious parts library
 * Adapted from "Pixel Transition" (demo 1) by Codrops (MIT), https://github.com/codrops/PixelTransition
 * Copyright (c) 2009 - 2026 Codrops. See LICENSE.
 * Changes: rebuilt with the same promise API as `type-curtain` (`await cover.play(swap)`), so a build
 * can swap one view-change for the other; the grid of cells builds itself; direction and cell counts
 * are inputs; reduced motion swaps behind a plain fade.
 */
import { gsap } from 'gsap';

const DEFAULTS = {
  rows: 8,
  columns: 14,
  direction: 'down',     // 'down' or 'up': which way the cells sweep in
  duration: 0.4,
  spread: 0.03,          // stagger per row
  jitter: 5,             // random rows of extra delay per cell, for the broken edge
};

export function mountPixelCover(cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const el = document.createElement('div');
  el.className = 'pxc';
  el.setAttribute('aria-hidden', 'true');
  el.style.setProperty('--pxc-columns', o.columns);
  el.style.setProperty('--pxc-rows', o.rows);
  const cells = [];
  for (let r = 0; r < o.rows; r++) for (let c = 0; c < o.columns; c++) {
    const cell = document.createElement('div');
    cell.dataset.row = r;
    el.appendChild(cell); cells.push(cell);
  }
  document.body.appendChild(el);
  gsap.set(el, { autoAlpha: 0 });
  let busy = false;

  const delay = (rev) => (i) => {
    const r = Number(cells[i].dataset.row);
    const row = rev ? o.rows - 1 - r : r;
    return o.spread * (row + gsap.utils.random(0, o.jitter));
  };

  const play = (swap) => new Promise((resolve) => {
    if (busy) return resolve(false);
    busy = true;
    const up = o.direction === 'up';
    const finish = () => { gsap.set(el, { autoAlpha: 0 }); busy = false; resolve(true); };
    if (reduced()) {
      gsap.set(cells, { scale: 1, opacity: 1 });
      gsap.timeline({ onComplete: finish })
        .fromTo(el, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.2 })
        .add(async () => { await swap?.(); })
        .to(el, { autoAlpha: 0, duration: 0.25 }, '+=0.1');
      return;
    }
    gsap.set(el, { autoAlpha: 1 });
    gsap.fromTo(cells, { scale: 0, opacity: 0, transformOrigin: up ? '50% 100%' : '50% 0%' }, {
      scale: 1.04, opacity: 1, duration: o.duration, ease: 'power3.inOut', stagger: delay(up), // slight overlap: no seams between cells
      onComplete: async () => {
        await swap?.();
        gsap.to(cells, { scale: 0, opacity: 0, transformOrigin: up ? '50% 0%' : '50% 100%', duration: o.duration, ease: 'power2', stagger: delay(up), onComplete: finish });
      },
    });
  });

  return { play, get busy() { return busy; }, destroy: () => el.remove() };
}
