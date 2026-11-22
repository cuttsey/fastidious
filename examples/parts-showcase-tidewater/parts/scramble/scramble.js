/*!
 * text-emphasis / scramble — Fastidious parts library
 * Adapted from the scramble in "Scroll Text Motion" by Codrops (MIT), https://github.com/codrops/ScrollTextMotion
 * Copyright (c) 2009 - 2023 Codrops. See LICENSE. Built on GSAP's ScrambleTextPlugin.
 * Changes: the real words stay in the page for screen readers and search (a visually hidden copy),
 * while the scramble plays on an aria-hidden copy; plays once at the reading line instead of on every
 * pass; character set and timing are inputs; reduced motion shows the words directly.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';
import { ScrambleTextPlugin } from 'gsap/ScrambleTextPlugin.js';

gsap.registerPlugin(ScrollTrigger, ScrambleTextPlugin);

const DEFAULTS = {
  selector: '[data-scramble]',
  chars: 'upperCase',     // 'upperCase', 'lowerCase', 'upperAndLowerCase', or any string of characters
  duration: 1,            // per element; data-scramble-duration overrides
  revealDelay: 0.2,
  speed: 0.6,
  start: 'top 80%',
  once: true,
};

export function mountScramble(root = document, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const els = [...root.querySelectorAll(o.selector)];
  const mm = gsap.matchMedia();
  const built = els.map((el) => {
    const text = el.textContent.trim();
    el.textContent = '';
    const real = document.createElement('span');
    real.className = 'sc-real';
    real.textContent = text;
    const shown = document.createElement('span');
    shown.className = 'sc-shown';
    shown.setAttribute('aria-hidden', 'true');
    shown.textContent = text;
    el.append(real, shown);
    return { el, text, shown };
  });

  mm.add('(prefers-reduced-motion: no-preference)', () => {
    const triggers = built.map(({ el, text, shown }) => {
      const play = () => gsap.fromTo(shown, { scrambleText: { text: '', chars: '' } }, {
        scrambleText: { text, chars: o.chars, revealDelay: o.revealDelay, speed: o.speed },
        duration: Number(el.dataset.scrambleDuration ?? o.duration),
      });
      gsap.set(shown, { opacity: 0 });
      return ScrollTrigger.create({
        trigger: el, start: o.start, once: o.once,
        onEnter: () => { gsap.set(shown, { opacity: 1 }); play(); },
        onEnterBack: o.once ? undefined : play,
      });
    });
    return () => { triggers.forEach((t) => t.kill()); built.forEach(({ shown, text }) => { gsap.killTweensOf(shown); gsap.set(shown, { opacity: 1 }); shown.textContent = text; }); };
  });

  return { destroy: () => mm.revert() };
}
