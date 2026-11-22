/*!
 * travelling-object — Fastidious parts library
 * Adapted from "One Element Scroll" by Codrops (MIT), https://github.com/codrops/OneElementScroll
 * Copyright (c) 2009 - 2024 Codrops. See LICENSE.
 * Changes: rebuilt as a self-contained module with token inputs, a reduced-motion
 * branch, a mobile branch, explicit teardown, and demo content removed.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';
import { Flip } from 'gsap/Flip.js';

gsap.registerPlugin(ScrollTrigger, Flip);

const DEFAULTS = {
  ease: 'sine.inOut',   // easing between slots
  hold: 0.5,            // pause between slots, as a fraction of one move
  scrub: true,          // true, or a number of seconds of smoothing
  mode: 'size',         // 'size' (true crop per slot) or 'scale' (transform only, slots must share an aspect ratio)
  mobileQuery: '(max-width: 47.99em)',
  mobile: 'static',     // 'static' shows the object in every slot; 'travel' keeps the journey on small screens
};

/**
 * Carries one object (usually the hero image) through a sequence of slots as the page scrolls.
 * @param {object} cfg
 * @param {HTMLElement} cfg.object  the travelling element; must be out of flow (position: absolute)
 * @param {HTMLElement[]} cfg.slots ordered slot elements the object should occupy
 */
export function mountTravellingObject(cfg) {
  const opts = { ...DEFAULTS, ...cfg };
  const { object, slots } = opts;
  if (!object || !slots?.length) throw new Error('travelling-object: object and slots are required');

  const mm = gsap.matchMedia();
  let ctx;
  const clones = [];

  const showStatic = () => {
    // The object stays still in its stage, and every slot gets its own still copy.
    // Copies are decorative repeats, so they are hidden from assistive tech.
    slots.forEach((slot) => {
      const c = object.cloneNode(true);
      c.removeAttribute('id');
      c.setAttribute('aria-hidden', 'true');
      c.classList.remove('to-object');
      c.classList.add('to-still');
      c.style.cssText = '';
      slot.appendChild(c);
      clones.push(c);
    });
  };

  const build = () => {
    ctx && ctx.revert();
    ctx = gsap.context(() => {
      const states = slots.map((s) => Flip.getState(s));
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: object.parentElement,
          start: 'clamp(center center)',
          endTrigger: slots[slots.length - 1],
          end: 'clamp(center center)',
          scrub: opts.scrub,
          invalidateOnRefresh: true,
        },
      });
      states.forEach((state, i) => {
        tl.add(
          Flip.fit(object, state, {
            duration: 1,
            ease: i === 0 ? 'none' : opts.ease,
            scale: opts.mode === 'scale',
          }),
          i ? `+=${opts.hold}` : 0,
        );
      });
    });
  };

  const onResize = () => build();

  mm.add(
    {
      motion: '(prefers-reduced-motion: no-preference)',
      reduced: '(prefers-reduced-motion: reduce)',
      small: opts.mobileQuery,
    },
    ({ conditions }) => {
      if (conditions.reduced || (conditions.small && opts.mobile === 'static')) {
        showStatic();
        return () => {
          clones.splice(0).forEach((c) => c.remove());
        };
      }
      build();
      window.addEventListener('resize', onResize);
      return () => {
        window.removeEventListener('resize', onResize);
        ctx && ctx.revert();
      };
    },
  );

  return { destroy: () => mm.revert(), refresh: () => ScrollTrigger.refresh() };
}
