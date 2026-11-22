/*!
 * lagging-columns — Fastidious parts library
 * Adapted from "Elastic Grid Scroll" (demo 1) by Codrops (MIT), https://github.com/codrops/ElasticGridScroll
 * Copyright (c) 2009 - 2026 Codrops. See LICENSE.
 * Changes: no ScrollSmoother, so the page keeps native scrolling; the grid's DOM is never rebuilt into
 * column wrappers, so reading and tab order stay row by row; each item follows the scroll with a
 * per-column lag computed from where it actually sits; the loop sleeps when nothing is moving;
 * reduced motion turns it off. No GSAP dependency.
 */
const DEFAULTS = {
  baseLag: 0.1,        // follow speed of the centre column (0 to 1 per frame; lower lags more)
  lagStep: 0.025,      // how much slower each column away from the centre follows
  maxOffset: 140,      // px cap on how far a column may trail
  itemSelector: ':scope > *',
};

export function mountLaggingColumns(grid, cfg = {}) {
  const opts = { ...DEFAULTS, ...cfg };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let items = [], factors = [], offsets = [], lastY = window.scrollY, raf = 0, running = false;

  const measure = () => {
    items = [...grid.querySelectorAll(opts.itemSelector)];
    items.forEach((el) => (el.style.transform = ''));
    // Group items into columns by their resting left edge, so any grid template works.
    const lefts = [...new Set(items.map((el) => Math.round(el.offsetLeft)))].sort((a, b) => a - b);
    const mid = (lefts.length - 1) / 2;
    factors = items.map((el) => {
      const col = lefts.indexOf(Math.round(el.offsetLeft));
      return Math.max(0.02, opts.baseLag - Math.abs(col - mid) * opts.lagStep);
    });
    offsets = items.map(() => 0);
  };

  const tick = () => {
    const y = window.scrollY;
    const dy = y - lastY;
    lastY = y;
    let moving = false;
    items.forEach((el, i) => {
      // Each item is pushed back by the scroll delta, then eases home at its column's speed.
      offsets[i] = Math.max(-opts.maxOffset, Math.min(opts.maxOffset, (offsets[i] + dy) * (1 - factors[i])));
      if (Math.abs(offsets[i]) > 0.1) moving = true; else offsets[i] = 0;
      el.style.transform = offsets[i] ? `translate3d(0, ${offsets[i].toFixed(2)}px, 0)` : '';
    });
    if (moving || dy !== 0) raf = requestAnimationFrame(tick);
    else running = false;
  };

  const wake = () => {
    if (reduced.matches || running) return;
    running = true;
    raf = requestAnimationFrame(tick);
  };

  const onResize = () => { measure(); lastY = window.scrollY; };
  const onPref = () => { if (reduced.matches) { cancelAnimationFrame(raf); running = false; measure(); } };

  measure();
  window.addEventListener('scroll', wake, { passive: true });
  window.addEventListener('resize', onResize);
  reduced.addEventListener('change', onPref);

  return {
    refresh: onResize,
    destroy() {
      cancelAnimationFrame(raf);
      window.removeEventListener('scroll', wake);
      window.removeEventListener('resize', onResize);
      reduced.removeEventListener('change', onPref);
      items.forEach((el) => (el.style.transform = ''));
    },
  };
}
