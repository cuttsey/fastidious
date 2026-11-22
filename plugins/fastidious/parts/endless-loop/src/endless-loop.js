/*!
 * endless-loop — Fastidious parts library
 * Adapted from "Infinite Loop Scrolling" by Codrops (MIT), https://github.com/codrops/LoopScrolling
 * Copyright (c) 2009 - 2022 Codrops. See LICENSE. (The demo credits Bureau DAM's site as its inspiration.)
 * Changes: rebuilt as a module around any sequence of panels; the clones that make the seam invisible
 * are hidden from assistive tech and inert; the panel scale-in and scale-out at the seam are optional;
 * reduced motion and keyboard users get an ordinary, finite page; Lenis (MIT) is a dependency.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);

const DEFAULTS = {
  selector: ':scope > *',
  clones: 1,          // how many panels from the start are repeated at the end to hide the seam
  seamScale: true,    // the first panel shrinks away as you leave it, and grows back as you arrive
  lerp: 0.1,
};

export function mountEndlessLoop(container, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) return { lenis: null, destroy() {} };

  const panels = [...container.querySelectorAll(o.selector)];
  const clones = panels.slice(0, o.clones).map((p) => {
    const c = p.cloneNode(true);
    c.setAttribute('aria-hidden', 'true');
    c.inert = true;
    c.classList.add('el-clone');
    c.querySelectorAll('[id]').forEach((n) => n.removeAttribute('id'));
    container.appendChild(c);
    return c;
  });

  const lenis = new Lenis({ infinite: true, lerp: o.lerp, syncTouch: true });
  lenis.on('scroll', ScrollTrigger.update);
  const raf = (t) => lenis.raf(t * 1000);
  gsap.ticker.add(raf);
  gsap.ticker.lagSmoothing(0);

  const tweens = [];
  if (o.seamScale) {
    const first = panels[0], seam = clones[0];
    tweens.push(gsap.fromTo(first, { scale: 1, transformOrigin: '50% 100%' }, { scale: 0.86, ease: 'none',
      scrollTrigger: { trigger: first, start: 'center center', end: 'bottom top', scrub: true } }));
    if (seam) tweens.push(gsap.fromTo(seam, { scale: 0.86, transformOrigin: '50% 0%' }, { scale: 1, ease: 'none',
      scrollTrigger: { trigger: seam, start: 'top bottom', end: 'top top', scrub: true } }));
  }

  // Keyboard users who tab past the last real panel would land in an inert clone: send focus back to the start.
  const onFocus = (e) => { if (clones.some((c) => c.contains(e.target))) { lenis.scrollTo(0, { immediate: true }); } };
  document.addEventListener('focusin', onFocus);

  return {
    lenis,
    destroy() {
      document.removeEventListener('focusin', onFocus);
      tweens.forEach((t) => { t.scrollTrigger?.kill(); t.revert(); });
      gsap.ticker.remove(raf);
      lenis.destroy();
      clones.forEach((c) => c.remove());
    },
  };
}
