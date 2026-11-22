/*!
 * inline-image-expand — Fastidious parts library
 * Adapted from "On-Scroll Expanding Image Animation within Typography" (effect 1) by Codrops (MIT),
 * https://github.com/codrops/ImageExpansionTypography — Copyright (c) 2009 - 2024 Codrops. See LICENSE.
 * Changes: the original grew the image's width with Flip, reflowing the headline on every frame.
 * This version reserves the image's space in the layout from the start and closes it with
 * transforms, so the final state is the natural layout: no reflow while scrolling, nothing
 * hidden without JavaScript, and reduced motion simply shows the open state.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';

gsap.registerPlugin(ScrollTrigger);

const DEFAULTS = {
  selector: '[data-ie]',
  start: 'top 85%',
  end: 'top 30%',
  scrub: 0.6,
  ease: 'power2.inOut',
  zoom: 1.35,          // how far the picture inside the window starts zoomed in
};

export function mountInlineImageExpand(root = document, cfg = {}) {
  const opts = { ...DEFAULTS, ...cfg };
  const blocks = [...root.querySelectorAll(opts.selector)];
  const mm = gsap.matchMedia();

  mm.add('(prefers-reduced-motion: no-preference)', () => {
    blocks.forEach((block) => {
      const win = block.querySelector('.ie-window');
      const pic = block.querySelector('.ie-window > img');
      const after = block.querySelectorAll('.ie-after');
      if (!win) return;

      // Distance the following words travel: the window's width plus the space around it.
      const shift = () => {
        // If the following words have wrapped onto another line, sliding them would look broken: reveal only.
        if (after[0] && Math.abs(after[0].getBoundingClientRect().top - win.getBoundingClientRect().top) > win.offsetHeight) return 0;
        const cs = getComputedStyle(win);
        return win.offsetWidth + parseFloat(cs.marginLeft) + parseFloat(cs.marginRight);
      };

      const r = getComputedStyle(win).getPropertyValue('--ie-radius').trim() || '999px';
      const tl = gsap.timeline({
        defaults: { ease: opts.ease },
        scrollTrigger: { trigger: block, start: opts.start, end: opts.end, scrub: opts.scrub, invalidateOnRefresh: true },
      });
      tl.fromTo(win, { clipPath: `inset(0% 50% 0% 50% round ${r})` }, { clipPath: `inset(0% 0% 0% 0% round ${r})` }, 0)
        .fromTo(pic, { scale: opts.zoom }, { scale: 1 }, 0)
        .fromTo(after, { x: () => -shift() }, { x: 0 }, 0)
        .fromTo(win, { x: () => -shift() / 2 }, { x: 0 }, 0);
    });
    return () => {};
  });

  return { destroy: () => mm.revert() };
}
