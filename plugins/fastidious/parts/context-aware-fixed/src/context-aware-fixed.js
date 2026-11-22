/*!
 * context-aware-fixed — Fastidious parts library
 * Adapted from "Context-Aware Animation for Fixed Elements on Scroll" by Codrops (MIT),
 * https://github.com/codrops/ContextAwareLogoAnimationScroll — Copyright (c) 2009 - 2024 Codrops. See LICENSE.
 * Changes: the element is split or wrapped once at mount instead of rewriting innerHTML on every pass;
 * hide and show are counted across overlapping blocks so they never fight; trigger lines follow the
 * fixed element's real position on refresh; the blur effect was dropped (it repaints every frame);
 * focus brings the element back; SplitText keeps an accessible name; reduced motion fades.
 */
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger.js';
import { SplitText } from 'gsap/SplitText.js';

gsap.registerPlugin(ScrollTrigger, SplitText);

const DEFAULTS = {
  blocks: '[data-caf-block]',   // sections the fixed element should step aside for
  effect: 'slide',              // 'slide' | 'scale' | 'scatter' | 'shuffle'
  duration: 0.6,
  ease: 'power4',
  offsetStart: 30,              // px before the block reaches the element
  offsetEnd: 10,                // px after the block has passed it
};

const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

function effects(el, o) {
  const d = { duration: o.duration, ease: o.ease, overwrite: true };
  switch (o.effect) {
    case 'scale':
      gsap.set(el, { transformOrigin: '0% 50%' });
      return { hide: () => gsap.to(el, { scale: 0, autoAlpha: 0, ...d }), show: () => gsap.to(el, { scale: 1, autoAlpha: 1, ...d }), revert: () => gsap.set(el, { clearProps: 'transform,opacity,visibility' }) };
    case 'scatter':
    case 'shuffle': {
      const split = SplitText.create(el, { type: 'chars', charsClass: 'caf-char', aria: 'auto' });
      const chars = split.chars;
      if (o.effect === 'scatter') {
        return {
          hide: () => gsap.to(chars, { x: () => gsap.utils.random(-50, 50), y: () => gsap.utils.random(-40, 0), autoAlpha: 0, stagger: { amount: 0.03, from: 'random' }, ...d }),
          show: () => gsap.to(chars, { x: 0, y: 0, autoAlpha: 1, stagger: { amount: 0.03, from: 'random' }, ...d }),
          revert: () => split.revert(),
        };
      }
      const originals = chars.map((c) => c.textContent);
      let tl;
      return {
        hide: () => { tl?.kill(); chars.forEach((c, i) => (c.textContent = originals[i])); tl = gsap.timeline().to(chars, { autoAlpha: 0, duration: 0.02, ease: 'none', stagger: { amount: 0.25, from: 'end' } }); },
        show: () => {
          tl?.kill(); tl = gsap.timeline();
          chars.forEach((c, i) => {
            const at = i * 0.03;
            tl.set(c, { autoAlpha: 1, textContent: GLYPHS[(Math.random() * GLYPHS.length) | 0] }, at)
              .set(c, { textContent: GLYPHS[(Math.random() * GLYPHS.length) | 0] }, at + 0.03)
              .set(c, { textContent: originals[i] }, at + 0.06);
          });
        },
        revert: () => { tl?.kill(); split.revert(); },
      };
    }
    default: { // slide: the content slides up out of a mask and back in from below
      const inner = document.createElement('span');
      inner.className = 'caf-inner';
      while (el.firstChild) inner.appendChild(el.firstChild);
      const mask = document.createElement('span');
      mask.className = 'caf-mask';
      mask.appendChild(inner);
      el.appendChild(mask);
      return {
        hide: () => gsap.to(inner, { yPercent: -105, ...d }),
        show: () => gsap.fromTo(inner, { yPercent: 105 }, { yPercent: 0, ...d }),
        revert: () => { while (inner.firstChild) el.appendChild(inner.firstChild); mask.remove(); },
      };
    }
  }
}

export function mountContextAwareFixed(fixed, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const els = typeof fixed === 'string' ? [...document.querySelectorAll(fixed)] : [].concat(fixed);
  const blocks = [...document.querySelectorAll(o.blocks)];
  const mm = gsap.matchMedia();

  mm.add({ motion: '(prefers-reduced-motion: no-preference)', reduced: '(prefers-reduced-motion: reduce)' }, ({ conditions }) => {
    const cleanups = [];
    els.forEach((el) => {
      const fx = conditions.reduced
        ? { hide: () => gsap.to(el, { autoAlpha: 0, duration: 0.2, overwrite: true }), show: () => gsap.to(el, { autoAlpha: 1, duration: 0.2, overwrite: true }), revert: () => gsap.set(el, { clearProps: 'opacity,visibility' }) }
        : effects(el, o);
      let held = false;        // keyboard focus keeps it visible
      let hidden = false;
      let triggers = [];
      // Hidden while any block is under the element; state is read from the triggers, never counted.
      const update = () => {
        const want = !held && triggers.some((t) => t.isActive);
        if (want !== hidden) { hidden = want; want ? fx.hide() : fx.show(); }
      };
      const box = () => el.getBoundingClientRect();
      triggers = blocks.map((block) => ScrollTrigger.create({
        trigger: block,
        start: () => `top ${box().bottom + o.offsetStart}px`,
        end: () => `bottom ${box().top - o.offsetEnd}px`,
        invalidateOnRefresh: true,
        onToggle: () => requestAnimationFrame(update),
        onRefresh: () => requestAnimationFrame(update),
      }));
      requestAnimationFrame(update);
      const onFocus = () => { held = true; update(); };
      const onBlur = () => { held = false; update(); };
      el.addEventListener('focusin', onFocus);
      el.addEventListener('focusout', onBlur);
      cleanups.push(() => {
        triggers.forEach((t) => t.kill());
        el.removeEventListener('focusin', onFocus);
        el.removeEventListener('focusout', onBlur);
        gsap.killTweensOf(el); fx.revert();
      });
    });
    return () => cleanups.forEach((c) => c());
  });

  return { destroy: () => mm.revert() };
}
