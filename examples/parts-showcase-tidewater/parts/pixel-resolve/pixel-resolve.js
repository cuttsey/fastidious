/*!
 * pixel-resolve — Fastidious parts library
 * Adapted from "On-Scroll Pixelated Image Loading" by Codrops (MIT), https://github.com/codrops/ImagePixelLoading
 * Copyright (c) 2009 - 2022 Codrops. (The demo credits a designer's site as its inspiration.)
 * Changes: enhances a real <img> (alt text, srcset and lazy loading kept) instead of a CSS background;
 * the canvas covers the image only while it resolves, then is removed; steps and timing are inputs;
 * one shared IntersectionObserver instead of a ScrollTrigger per image; reduced motion shows the image.
 * No dependencies.
 */
const DEFAULTS = {
  selector: 'img[data-pixel-resolve]',
  steps: [1, 2, 4, 9, 100],   // percent of full resolution at each step
  first: 300,                 // ms on the coarsest step
  each: 80,                   // ms on every other step
  threshold: 0.2,
};

export function mountPixelResolve(root = document, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return { destroy() {} };
  const imgs = [...root.querySelectorAll(o.selector)];
  const timers = new Set();

  const resolve = (img) => {
    const wrap = img.parentElement;
    const canvas = document.createElement('canvas');
    canvas.className = 'pr-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    const w = (canvas.width = Math.round(img.clientWidth));
    const h = (canvas.height = Math.round(img.clientHeight));
    wrap.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    // object-fit: cover crop of the source, so the pixels match the image underneath exactly.
    const ir = img.naturalWidth / img.naturalHeight, cr = w / h;
    const sw = ir > cr ? img.naturalHeight * cr : img.naturalWidth;
    const sh = ir > cr ? img.naturalHeight : img.naturalWidth / cr;
    const sx = (img.naturalWidth - sw) / 2, sy = (img.naturalHeight - sh) / 2;
    let i = 0;
    const draw = () => {
      const f = o.steps[i] / 100;
      if (f >= 1) { canvas.remove(); img.classList.add('pr-done'); return; }
      const tw = Math.max(1, Math.round(w * f)), th = Math.max(1, Math.round(h * f));
      ctx.imageSmoothingEnabled = false;
      ctx.clearRect(0, 0, w, h);
      ctx.drawImage(img, sx, sy, sw, sh, 0, 0, tw, th);
      ctx.drawImage(canvas, 0, 0, tw, th, 0, 0, w, h);
      if (i === 0) img.classList.add('pr-ready');
      const t = setTimeout(() => { timers.delete(t); i++; draw(); }, i === 0 ? o.first : o.each);
      timers.add(t);
    };
    draw();
  };

  imgs.forEach((img) => img.classList.add('pr-armed'));
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      const img = e.target;
      (img.complete && img.naturalWidth ? Promise.resolve() : img.decode().catch(() => {})).then(() => resolve(img));
    });
  }, { threshold: o.threshold });
  imgs.forEach((img) => io.observe(img));

  return { destroy() { io.disconnect(); timers.forEach(clearTimeout); root.querySelectorAll('.pr-canvas').forEach((c) => c.remove()); imgs.forEach((img) => img.classList.remove('pr-armed')); } };
}
