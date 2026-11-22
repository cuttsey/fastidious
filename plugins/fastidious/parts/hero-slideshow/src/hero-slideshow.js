/*!
 * hero-slideshow — Fastidious parts library
 * Adapted from "Fullscreen Image Slideshow Animations" (demos 1, 4, 8 and 24) by Codrops (MIT),
 * https://github.com/codrops/SlideshowAnimations — Copyright (c) 2009 - 2026 Codrops. See LICENSE.
 * Changes: one engine with four curated transitions instead of 32 separate demos; the page's own
 * scroll is never captured (no wheel hijack unless asked for); arrow keys work only while the
 * slideshow has focus; swipe on touch; carousel semantics and a live region announce each slide;
 * filters removed from the "card" transition (transform only); reduced motion crossfades.
 */
import { gsap } from 'gsap';

const NEXT = 1;
const TRANSITIONS = {
  // The slides push vertically while their pictures move slower, in parallax. Calm, editorial.
  push(cur, curIn, up, upIn, dir) {
    return gsap.timeline({ defaults: { duration: 1.3, ease: 'power4.inOut' } })
      .to(cur, { yPercent: -dir * 100 }, 0)
      .to(curIn, { yPercent: dir * 30 }, 0)
      .fromTo(up, { yPercent: dir * 100 }, { yPercent: 0 }, 0)
      .fromTo(upIn, { yPercent: -dir * 30 }, { yPercent: 0 }, 0);
  },
  // The current slide steps back and fades as the next rises over it. Quiet, deliberate.
  recede(cur, curIn, up, upIn, dir) {
    return gsap.timeline({ defaults: { duration: 1.2, ease: 'power4.inOut' }, onStart: () => gsap.set(up, { zIndex: 3 }), onComplete: () => gsap.set(up, { zIndex: '' }) })
      .to(cur, { duration: 0.4, ease: 'sine', scale: 0.9, autoAlpha: 0.2 }, 0)
      .to(cur, { yPercent: -dir * 20, autoAlpha: 0 }, 0.1)
      .fromTo(up, { autoAlpha: 1, scale: 1, yPercent: dir * 100 }, { yPercent: 0 }, 0.1)
      .fromTo(upIn, { yPercent: -dir * 50 }, { yPercent: 0 }, 0.1);
  },
  // The next picture flies in as a small, stretched card, then grows to fill the frame. Expressive.
  card(cur, curIn, up, upIn, dir) {
    return gsap.timeline({ onStart: () => gsap.set(up, { zIndex: 3 }), onComplete: () => gsap.set(up, { zIndex: '' }) })
      .fromTo(up, { autoAlpha: 1, scale: 0.1, xPercent: dir * 100 }, { duration: 0.7, ease: 'expo', scale: 0.4, xPercent: 0 }, 0)
      .fromTo(upIn, { transformOrigin: dir === NEXT ? '100% 50%' : '0% 50%', scaleX: 4 }, { duration: 0.7, ease: 'expo', scaleX: 1 }, 0)
      .to(up, { duration: 1, ease: 'power4.inOut', scale: 1 }, 0.6)
      .to(cur, { duration: 1, ease: 'power4.inOut', scale: 0.98, autoAlpha: 0 }, 0.6);
  },
  // The view pulls back, pans across to the next picture and pushes in. Cinematic.
  camera(cur, curIn, up, upIn, dir) {
    const cam = { zoom: 1, pan: 0 }, spacing = 106, ZOOM = 0.6;
    const place = () => {
      [[cur, curIn, 0], [up, upIn, dir * spacing]].forEach(([s, i, at]) => {
        const x = (at - cam.pan) * cam.zoom;
        gsap.set(s, { xPercent: x, scale: cam.zoom, autoAlpha: 1 });
        gsap.set(i, { xPercent: -x * 0.1, scale: 1 + (1 - cam.zoom) * 0.6 });
      });
    };
    return gsap.timeline({ onUpdate: place, onComplete: () => gsap.set([cur, up, curIn, upIn], { clearProps: 'transform' }) })
      .to(cam, { duration: 0.8, ease: 'power3.inOut', zoom: ZOOM }, 0)
      .to(cam, { duration: 1.1, ease: 'power3.inOut', pan: dir * spacing }, 0.35)
      .to(cam, { duration: 0.8, ease: 'power3.inOut', zoom: 1 }, 1.05);
  },
};

const DEFAULTS = {
  transition: 'push',     // 'push', 'recede', 'card' or 'camera'
  label: 'Slideshow',
  swipe: true,
  wheel: false,           // only for a full-page slideshow that is the whole site
  onChange: null,         // (index, slide) => void, for counters and anything outside the slides
  textDelay: { push: 0.55, recede: 0.6, card: 0.9, camera: 1.2 }, // when the next slide's words rise in
};

export function mountHeroSlideshow(root, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const slides = [...root.querySelectorAll('.hs-slide')];
  const inners = slides.map((s) => s.querySelector('.hs-img'));
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let current = 0, busy = false;

  root.setAttribute('role', 'region');
  root.setAttribute('aria-roledescription', 'carousel');
  root.setAttribute('aria-label', o.label);
  if (!root.hasAttribute('tabindex')) root.tabIndex = 0;
  const live = document.createElement('p');
  live.className = 'hs-live';
  live.setAttribute('aria-live', 'polite');
  root.appendChild(live);

  const mark = () => slides.forEach((s, i) => {
    s.classList.toggle('hs-current', i === current);
    s.setAttribute('aria-hidden', String(i !== current));
    s.inert = i !== current;
    s.setAttribute('aria-roledescription', 'slide');
    s.setAttribute('aria-label', `${i + 1} of ${slides.length}`);
  });
  mark();

  const go = (dir) => {
    if (busy || slides.length < 2) return false;
    busy = true;
    const prev = current;
    current = (current + dir + slides.length) % slides.length;
    const [cur, curIn, up, upIn] = [slides[prev], inners[prev], slides[current], inners[current]];
    const finish = () => {
      gsap.set([cur, up, curIn, upIn], { clearProps: 'transform,opacity,visibility,zIndex' });
      gsap.set(cur.querySelectorAll('.hs-line > *'), { clearProps: 'transform' });
      mark();
      live.textContent = `Slide ${current + 1} of ${slides.length}`;
      o.onChange?.(current, up);
      busy = false;
    };
    up.classList.add('hs-current');
    // Words inside each slide (.hs-line > *) leave first and arrive after the picture has landed.
    const curWords = cur.querySelectorAll('.hs-line > *'), upWords = up.querySelectorAll('.hs-line > *');
    if (!reduced()) {
      gsap.to(curWords, { yPercent: -110, duration: 0.45, ease: 'power3.in', stagger: 0.04 });
      gsap.fromTo(upWords, { yPercent: 110 }, { yPercent: 0, duration: 1, ease: 'expo.out', stagger: 0.06, delay: o.textDelay[o.transition] ?? 0.6 });
    }
    if (reduced()) {
      gsap.timeline({ defaults: { duration: 0.5, ease: 'power1.inOut' }, onComplete: finish })
        .fromTo(up, { opacity: 0 }, { opacity: 1 }, 0).to(cur, { opacity: 0 }, 0);
    } else {
      TRANSITIONS[o.transition](cur, curIn, up, upIn, dir).eventCallback('onComplete', finish);
    }
    return true;
  };

  const onKey = (e) => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); go(1); }
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); go(-1); }
  };
  root.addEventListener('keydown', onKey);
  root.querySelector('.hs-next')?.addEventListener('click', () => go(1));
  root.querySelector('.hs-prev')?.addEventListener('click', () => go(-1));

  let x0 = null;
  const down = (e) => { if (e.pointerType !== 'mouse') x0 = e.clientX; };
  const up = (e) => { if (x0 === null) return; const dx = e.clientX - x0; x0 = null; if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1); };
  if (o.swipe) { root.addEventListener('pointerdown', down); root.addEventListener('pointerup', up); }

  let lastWheel = 0;
  const onWheel = (e) => { const now = performance.now(); if (now - lastWheel > 400 && Math.abs(e.deltaY) > 10) go(e.deltaY > 0 ? 1 : -1); lastWheel = now; };
  if (o.wheel) root.addEventListener('wheel', onWheel, { passive: true });

  return {
    next: () => go(1),
    prev: () => go(-1),
    get index() { return current; },
    destroy() { root.removeEventListener('keydown', onKey); root.removeEventListener('pointerdown', down); root.removeEventListener('pointerup', up); root.removeEventListener('wheel', onWheel); live.remove(); },
  };
}
