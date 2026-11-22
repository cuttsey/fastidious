/*!
 * interruptible-menu — Fastidious parts library
 * Adapted from "Ease Reverse Clip Menu" by Codrops (MIT), https://github.com/codrops/EaseReverseClipMenu
 * Copyright (c) 2009 - 2025 Codrops. See LICENSE.
 * Changes: rebuilt as a module around any toggle button and menu; the demo's controls, video and
 * cover images are removed; the scatter of page elements is optional; focus moves into the menu on
 * open and back to the toggle on close; reduced motion gets a short fade with no clip or scatter.
 * Kept: the idea that matters. A close that interrupts an opening reverses from wherever it is,
 * faster and with an adaptive ease (GSAP easeReverse), so the menu never makes the visitor wait.
 * Requires GSAP 3.15 or later for easeReverse.
 */
import { gsap } from 'gsap';

const DEFAULTS = {
  scatter: [],              // optional page elements that fly outwards as the menu opens
  scatterDistance: 600,
  openDuration: 0.8,
  openEase: 'expo',
  clipDelay: 0.3,           // menu clip starts after the scatter begins
  fullCloseEase: 'expo.in', // reverse ease when closing a fully open menu
  interruptSpeed: 2.5,      // time scale for a close that interrupts an opening
  itemSelector: 'a, button',
};

const centreOf = (el) => { const r = el.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; };

export function mountInterruptibleMenu({ toggle, menu, ...cfg }) {
  const o = { ...DEFAULTS, ...cfg };
  const items = [...menu.querySelectorAll(o.itemSelector)];
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let isOpen = false, tl;

  const sync = () => {
    toggle.setAttribute('aria-expanded', String(isOpen));
    menu.inert = !isOpen;
    menu.setAttribute('aria-hidden', String(!isOpen));
  };

  const build = (reverseEase) => {
    const closed = 'polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%)';
    gsap.set(menu, { clipPath: closed, visibility: 'visible' });
    gsap.set(o.scatter, { x: 0, y: 0, rotation: 0, opacity: 1 });
    const t = gsap.timeline({ paused: true, onReverseComplete: () => gsap.set(menu, { visibility: 'hidden' }) });
    if (reduced()) {
      gsap.set(menu, { clipPath: 'none' });
      return t.fromTo(menu, { opacity: 0 }, { opacity: 1, duration: 0.25, ease: 'none' });
    }
    t.to(menu, { clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)', duration: o.openDuration, ease: o.openEase, easeReverse: reverseEase }, o.clipDelay);
    t.from(items, { y: 30, opacity: 0, duration: 0.6, ease: o.openEase, stagger: 0.04, easeReverse: reverseEase }, o.clipDelay + 0.15);
    const vw = innerWidth / 2, vh = innerHeight / 2, max = Math.hypot(vw, vh);
    o.scatter.forEach((el) => {
      const c = centreOf(el), dx = c.x - vw, dy = c.y - vh, d = Math.hypot(dx, dy) || 1;
      t.to(el, {
        x: (dx / d) * o.scatterDistance, y: (dy / d) * o.scatterDistance, opacity: 0,
        rotation: gsap.utils.random(-30, 30), duration: 0.7, ease: o.openEase, easeReverse: reverseEase,
      }, 0.3 * (1 - Math.min(d / max, 1)));
    });
    return t;
  };

  const rebuild = (progress, reverseEase) => {
    tl && tl.revert();
    tl = build(reverseEase);
    tl.progress(progress).pause();
  };

  const setOpen = (next) => {
    if (next === isOpen) return;
    const p = tl.progress();
    isOpen = next;
    sync();
    if (isOpen) {
      gsap.set(menu, { visibility: 'visible' });
      tl.timeScale(1).play();
      items[0]?.focus({ preventScroll: true });
      return;
    }
    if (p >= 0.999) { rebuild(1, o.fullCloseEase); tl.timeScale(1).reverse(); }
    else { rebuild(p, true); tl.timeScale(o.interruptSpeed).reverse(); } // adaptive reverse from where it is
    toggle.focus({ preventScroll: true });
  };

  const onToggle = () => setOpen(!isOpen);
  const onKey = (e) => { if (e.key === 'Escape' && isOpen) setOpen(false); };
  toggle.setAttribute('aria-controls', menu.id);
  rebuild(0, o.fullCloseEase);
  gsap.set(menu, { visibility: 'hidden' });
  sync();
  toggle.addEventListener('click', onToggle);
  document.addEventListener('keydown', onKey);

  return {
    open: () => setOpen(true),
    close: () => setOpen(false),
    destroy() { toggle.removeEventListener('click', onToggle); document.removeEventListener('keydown', onKey); tl && tl.revert(); },
  };
}
