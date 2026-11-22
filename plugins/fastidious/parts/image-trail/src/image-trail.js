/*!
 * image-trail — Fastidious parts library
 * Adapted from "Motion Trail Animations" (demo 1 and the shared trail engine) by Codrops (MIT),
 * https://github.com/codrops/MotionTrailAnimations — Copyright (c) 2009 - 2025 Codrops. See LICENSE.
 * Changes: listens only inside its own area instead of the whole window; the pool of images comes
 * from the host's <img> elements; spacing, lag and the image's show/hide motion are inputs; pauses
 * when off screen; touch draws a trail while dragging without blocking vertical page scroll;
 * reduced motion places still images (no travel, no scale).
 */
import { gsap } from 'gsap';

const DEFAULTS = {
  pool: 20,          // how many image elements to cycle through (sources repeat to fill it)
  threshold: 80,     // px the pointer travels before the next image appears
  lag: 0.1,          // how far behind the pointer the image starts (0 to 1)
  maxPerFrame: 4,
  show: 0.4, hide: 0.4,
  endScale: 0.2,
};

export function mountImageTrail(area, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const sources = [...area.querySelectorAll('.it-img')];
  sources.forEach((s) => s.setAttribute('aria-hidden', 'true'));
  for (let i = sources.length; i < o.pool; i++) area.appendChild(sources[i % sources.length].cloneNode(true));
  const imgs = [...area.querySelectorAll('.it-img')];
  const wrap = gsap.utils.wrap(0, imgs.length);
  let pointer = null, trailing = null, last = null, count = 0, z = 1, visible = true;
  let rect = area.getBoundingClientRect();

  const local = (e) => ({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  const reset = (e) => { rect = area.getBoundingClientRect(); pointer = local(e); trailing = { ...pointer }; last = { ...pointer }; };
  const onMove = (e) => { if (!pointer) return reset(e); rect = area.getBoundingClientRect(); pointer = local(e); };
  const onLeave = () => { pointer = null; };

  const showAt = (at) => {
    const img = imgs[wrap(count++)];
    const lead = { x: pointer.x - trailing.x, y: pointer.y - trailing.y };
    const w = img.offsetWidth, h = img.offsetHeight;
    const to = { x: at.x - w / 2, y: at.y - h / 2 };
    gsap.killTweensOf(img);
    if (reduced.matches) {
      gsap.timeline().set(img, { x: to.x, y: to.y, zIndex: ++z, scale: 1, opacity: 1 }).to(img, { opacity: 0, duration: 0.6, delay: 0.3 });
      return;
    }
    gsap.timeline()
      .fromTo(img, { opacity: 1, scale: 1, zIndex: ++z, x: to.x - lead.x, y: to.y - lead.y }, { duration: o.show, ease: 'power1', x: to.x, y: to.y }, 0)
      .to(img, { duration: o.hide, ease: 'power3', opacity: 0, scale: o.endScale }, o.show);
  };

  const tick = () => {
    if (!pointer || !visible) return;
    const f = 1 - Math.pow(1 - o.lag, gsap.ticker.deltaRatio(60));
    trailing.x += (pointer.x - trailing.x) * f;
    trailing.y += (pointer.y - trailing.y) * f;
    let dx = pointer.x - last.x, dy = pointer.y - last.y, d = Math.hypot(dx, dy);
    if (d < o.threshold) return;
    const step = { x: (dx / d) * o.threshold, y: (dy / d) * o.threshold };
    for (let n = 0; d >= o.threshold && n < o.maxPerFrame; n++) {
      last = { x: last.x + step.x, y: last.y + step.y };
      d -= o.threshold;
      showAt(last);
    }
    if (d >= o.threshold) last = { ...pointer };
  };

  const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; });
  io.observe(area);
  area.addEventListener('pointermove', onMove);
  area.addEventListener('pointerdown', reset);
  area.addEventListener('pointerleave', onLeave);
  area.addEventListener('pointercancel', onLeave);
  gsap.ticker.add(tick);

  return {
    destroy() {
      gsap.ticker.remove(tick); io.disconnect();
      area.removeEventListener('pointermove', onMove); area.removeEventListener('pointerdown', reset);
      area.removeEventListener('pointerleave', onLeave); area.removeEventListener('pointercancel', onLeave);
    },
  };
}
