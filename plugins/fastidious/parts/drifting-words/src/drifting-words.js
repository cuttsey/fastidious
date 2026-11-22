/*!
 * drifting-words — Fastidious parts library
 * Adapted from "Scroll Text Motion" by Codrops (MIT), https://github.com/codrops/ScrollTextMotion
 * Copyright (c) 2009 - 2023 Codrops. See LICENSE. (The demo credits satto.studio as its inspiration.)
 * Changes: the drift between columns is computed as a transform from each word's column numbers,
 * instead of swapping layout classes and Flipping them, so nothing reflows while scrolling;
 * ScrollSmoother is no longer required; the page's own scroll stays native; reduced motion keeps
 * every word at rest in its home column.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';

gsap.registerPlugin(ScrollTrigger);

const DEFAULTS = {
  selector: '[data-dw]',
  columns: 10,          // must match the grid's column count (CSS --dw-columns)
  ease: 'expo.inOut',
  scrub: true,
};

export function mountDriftingWords(root, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const words = [...root.querySelectorAll(o.selector)];
  root.style.setProperty('--dw-columns', o.columns);
  // Each word rests in its home column when centred, and arrives from / leaves towards its away column.
  words.forEach((w) => w.style.setProperty('--dw-home', w.dataset.dwHome || 1));
  const shift = (w) => {
    const cs = getComputedStyle(root);
    const padL = parseFloat(cs.paddingLeft), padR = parseFloat(cs.paddingRight);
    const inner = root.clientWidth - padL - padR;
    const raw = (Number(w.dataset.dwAway || w.dataset.dwHome || 1) - Number(w.dataset.dwHome || 1)) * (inner / o.columns);
    // Keep every word inside the field: never drift past either edge (matters most on small screens).
    const left = w.offsetLeft - padL;
    return Math.max(-left, Math.min(raw, inner - left - w.offsetWidth));
  };
  const mm = gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    words.forEach((w) => {
      const ease = w.dataset.dwEase || o.ease;
      gsap.fromTo(w, { x: () => shift(w) }, { x: 0, ease, immediateRender: true,
        scrollTrigger: { trigger: w, start: 'clamp(bottom bottom-=10%)', end: 'clamp(center center)', scrub: o.scrub, invalidateOnRefresh: true } });
      gsap.fromTo(w, { x: 0 }, { x: () => shift(w), ease, immediateRender: false,
        scrollTrigger: { trigger: w, start: 'clamp(center center)', end: 'clamp(top top)', scrub: o.scrub, invalidateOnRefresh: true } });
    });
  });
  return { destroy: () => mm.revert() };
}
