/*!
 * text-emphasis / char-rise — Fastidious parts library
 * Adapted from "On-Scroll Text Highlight Animations" (effect 1) by Codrops (MIT),
 * https://github.com/codrops/OnScrollTextHighlight — Copyright (c) 2009 - 2022 Codrops. See LICENSE.
 * Changes: Splitting.js replaced with GSAP SplitText (keeps an accessible label on the line);
 * fires at the reading line and plays once instead of resetting on every exit; depth, tilt,
 * stagger and easing are inputs; reduced motion gets a plain fade; split text is reverted on teardown.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';
import { SplitText } from 'gsap/SplitText.js';

gsap.registerPlugin(ScrollTrigger, SplitText);

const DEFAULTS = {
  selector: '[data-char-rise]',
  start: 'top 78%',
  depth: 260,          // px the characters travel forward from
  tilt: -50,           // degrees of rotationX at the start
  perspective: 520,
  duration: 0.9,
  stagger: 0.035,
  ease: 'power3.out',
};

export function mountCharRise(root = document, cfg = {}) {
  const opts = { ...DEFAULTS, ...cfg };
  const els = [...root.querySelectorAll(opts.selector)];
  const mm = gsap.matchMedia();

  mm.add(
    { motion: '(prefers-reduced-motion: no-preference)', reduced: '(prefers-reduced-motion: reduce)' },
    ({ conditions }) => {
      if (conditions.reduced) {
        els.forEach((el) =>
          gsap.from(el, { autoAlpha: 0, duration: 0.6, ease: 'none', scrollTrigger: { trigger: el, start: opts.start, once: true } }),
        );
        return;
      }
      const splits = els.map((el) => {
        const split = SplitText.create(el, { type: 'words,chars', wordsClass: 'cr-word', charsClass: 'cr-char', aria: 'auto' });
        gsap.set(el, { perspective: opts.perspective });
        gsap.set(split.words, { transformStyle: 'preserve-3d' });
        gsap.fromTo(
          split.chars,
          { autoAlpha: 0, z: opts.depth, rotationX: opts.tilt },
          {
            autoAlpha: 1, z: 0, rotationX: 0,
            duration: opts.duration, stagger: opts.stagger, ease: opts.ease,
            scrollTrigger: { trigger: el, start: opts.start, once: true },
          },
        );
        return split;
      });
      return () => splits.forEach((s) => s.revert());
    },
  );

  return { destroy: () => mm.revert() };
}
