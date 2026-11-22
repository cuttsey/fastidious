/*!
 * sticky-stack — Fastidious parts library
 * Adapted from "Sticky Sections" (demos 1 and 7) by Codrops (MIT), https://github.com/codrops/StickySections
 * Copyright (c) 2009 - 2022 Codrops. See LICENSE.
 * Changes: the outgoing section is dimmed with an overlay's opacity instead of a brightness/contrast
 * filter (no repaint per frame); exit styles are an option; Lenis is no longer required; the last
 * section never animates out; reduced motion keeps the stacking (pure CSS) and drops the exit motion.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';

gsap.registerPlugin(ScrollTrigger);

const EXITS = {
  // The outgoing section drifts up a little and darkens as the next one covers it.
  drift: (el, o) => ({ yPercent: -o.drift }),
  // The outgoing section shrinks back and fades, like a card being put down.
  recede: (el, o) => ({ scale: o.scale, opacity: 0 }),
};

const DEFAULTS = {
  selector: '.ss-section',
  exit: 'drift',        // 'drift' or 'recede'
  drift: 15,            // percent of section height, for 'drift'
  scale: 0.6,           // final scale, for 'recede'
  dim: 0.45,            // overlay opacity reached by the outgoing section (0 to disable)
  mediaSelector: '.ss-media', // optional element inside a section that gets a secondary tilt
  tilt: 0,              // degrees of rotation for mediaSelector on exit (0 to disable)
};

export function mountStickyStack(root = document, cfg = {}) {
  const opts = { ...DEFAULTS, ...cfg };
  const sections = [...root.querySelectorAll(opts.selector)];
  const mm = gsap.matchMedia();

  mm.add('(prefers-reduced-motion: no-preference)', () => {
    sections.slice(0, -1).forEach((el) => {
      const tl = gsap.timeline({
        defaults: { ease: 'none' },
        scrollTrigger: {
          trigger: el,
          start: opts.exit === 'recede' ? 'center center' : 'top top',
          end: '+=100%',
          scrub: true,
        },
      });
      tl.to(el, EXITS[opts.exit](el, opts), 0);
      if (opts.dim > 0) tl.to(el, { '--ss-dim': opts.dim }, 0);
      const media = el.querySelector(opts.mediaSelector);
      if (media && opts.tilt) tl.to(media, { yPercent: -40, rotation: opts.tilt, ease: 'power1.in' }, 0);
    });
  });

  return { destroy: () => mm.revert() };
}
