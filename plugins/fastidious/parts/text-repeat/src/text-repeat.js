/*!
 * text-repeat — Fastidious parts library
 * Adapted from "Text Repetition Scroll Effect" by Codrops (MIT), https://github.com/codrops/TextRepetitionEffect
 * Copyright (c) 2009 - 2022 Codrops. See LICENSE.
 * Changes: copies are made inside the part's own wrapper and hidden from screen readers, so the word
 * is read once; the host element's margin and padding are left alone; progress comes from one
 * ScrollTrigger scrub instead of an observer plus ticker; copies, spread, stagger, drift and fade
 * are inputs; reduced motion shows the single word; teardown restores the original markup.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';

gsap.registerPlugin(ScrollTrigger);

const DEFAULTS = {
  copies: 9,          // total layers including the word itself (odd numbers keep it centred)
  spread: 12,         // % of the word's height each layer steps away from the centre
  stagger: 0.1,       // outer layers start later, so the stack opens like a fan
  drift: 0,           // sideways drift as a share of spread (0.1 gives a slight slant)
  fade: false,        // outer layers fade as they spread
  ease: 'power1',
  start: 'top bottom',
  end: 'bottom top',
  scrub: true,
};

export function mountTextRepeat(target, cfg = {}) {
  const el = typeof target === 'string' ? document.querySelector(target) : target;
  const o = { ...DEFAULTS, ...cfg };
  const original = el.innerHTML;
  const half = Math.floor(o.copies / 2);
  const mm = gsap.matchMedia();

  mm.add({ motion: '(prefers-reduced-motion: no-preference)' }, () => {
    const layers = [];
    for (let i = 0; i < o.copies - 1; i++) {
      const up = i < half;                         // first half spreads upwards, the rest downwards
      const step = up ? half - i : i - half + 1;
      layers.push({ ty: (up ? -1 : 1) * step * o.spread, delay: (step - 1) * o.stagger });
    }
    el.innerHTML = `<span class="tr-stack">${layers.map(() => `<span class="tr-copy" aria-hidden="true">${original}</span>`).join('')}<span class="tr-word">${original}</span></span>`;
    el.classList.add('tr');
    const stack = el.querySelector('.tr-stack');
    const copies = [...el.querySelectorAll('.tr-copy')];
    // Room for the outermost layers, inside the part's own wrapper.
    const room = () => `${(half * o.spread) / 100 * el.querySelector('.tr-word').offsetHeight}px`;
    gsap.set(stack, { paddingBlock: room });

    const tl = gsap.timeline({
      defaults: { ease: o.ease, duration: 1 },
      scrollTrigger: {
        trigger: el, start: o.start, end: o.end, scrub: o.scrub, invalidateOnRefresh: true,
        onRefresh: () => gsap.set(stack, { paddingBlock: room() }),
      },
    });
    copies.forEach((c, i) => {
      const L = layers[i];
      tl.fromTo(c, { yPercent: 0, xPercent: 0, opacity: 1 },
        { yPercent: L.ty, xPercent: L.ty * o.drift, opacity: o.fade ? 0 : 1 }, L.delay);
    });
    return () => { tl.scrollTrigger?.kill(); tl.kill(); el.innerHTML = original; el.classList.remove('tr'); };
  });

  return { destroy: () => mm.revert() };
}
