/*!
 * text-emphasis / marker-sweep — Fastidious parts library
 * Adapted from "On-Scroll Text Highlight Animations" (effects 6 and 7) by Codrops (MIT),
 * https://github.com/codrops/OnScrollTextHighlight — Copyright (c) 2009 - 2022 Codrops. See LICENSE.
 * Changes: the marker now sweeps with a transform (scaleX) instead of animating width or height;
 * it fires at the reading line rather than at the bottom edge of the viewport; it plays once
 * instead of resetting on every exit; marks in one block run in reading order; text is never
 * split, so screen readers hear the sentence unchanged; reduced motion shows the marks at rest.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';

gsap.registerPlugin(ScrollTrigger);

const DEFAULTS = {
  selector: '[data-emphasis]',
  start: 'top 72%',     // the reading line, not the bottom edge of the viewport
  duration: 0.65,
  ease: 'power3.out',
  stagger: 0.18,        // gap between marks inside the same block
  blockSelector: 'p, li, blockquote, h1, h2, h3, h4, figcaption',
};

export function mountMarkerSweep(root = document, cfg = {}) {
  const opts = { ...DEFAULTS, ...cfg };
  const marks = [...root.querySelectorAll(opts.selector)];
  const mm = gsap.matchMedia();

  // Group marks by their block so marks in one sentence sweep in reading order.
  const groups = new Map();
  marks.forEach((m) => {
    const block = m.closest(opts.blockSelector) || m.parentElement;
    if (!groups.has(block)) groups.set(block, []);
    groups.get(block).push(m);
  });

  mm.add('(prefers-reduced-motion: no-preference)', () => {
    groups.forEach((group, block) => {
      group.forEach((m) => m.classList.add('ms-armed'));
      ScrollTrigger.create({
        trigger: block,
        start: opts.start,
        once: true,
        onEnter: () => {
          gsap.to(group, {
            '--ms-scale': 1,
            duration: opts.duration,
            ease: opts.ease,
            stagger: opts.stagger,
          });
        },
      });
    });
    return () => marks.forEach((m) => { m.classList.remove('ms-armed'); m.style.removeProperty('--ms-scale'); });
  });

  return { destroy: () => mm.revert() };
}
