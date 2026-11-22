/*!
 * grain-light — Fastidious parts library. Original part (MIT), built from WANTED.md:
 * "film grain and soft light over a section, at negligible cost, as depth without 3D".
 * Grain: one small noise tile drawn once to a canvas, then shifted in steps with a CSS transform.
 * Light: a soft radial glow that drifts towards the pointer (or on its own on touch screens).
 * No WebGL, no per-frame painting. No dependencies.
 */
const DEFAULTS = {
  tile: 160,            // px size of the noise tile
  grainOpacity: 0.12,   // overall strength, also settable with --gl-grain-opacity
  light: true,
  follow: 0.06,         // how quickly the light drifts towards the pointer (0 to 1 per frame)
  drift: 0.00025,       // idle drift speed when there is no pointer
};

let tileURL = null;
const makeTile = (size) => {
  if (tileURL) return tileURL;
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const img = ctx.createImageData(size, size);
  // Light and dark specks on a transparent tile: reads as grain over any colour with no blend mode,
  // which keeps the cost close to zero even without a GPU.
  for (let i = 0; i < img.data.length; i += 4) {
    const light = Math.random() > 0.5;
    img.data[i] = img.data[i + 1] = img.data[i + 2] = light ? 255 : 0;
    img.data[i + 3] = Math.random() * 255;
  }
  ctx.putImageData(img, 0, 0);
  tileURL = c.toDataURL('image/png');
  return tileURL;
};

export function mountGrainLight(section, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const fine = window.matchMedia('(pointer: fine)');
  section.classList.add('gl-host');

  const grain = document.createElement('div');
  grain.className = 'gl-grain';
  grain.setAttribute('aria-hidden', 'true');
  grain.style.backgroundImage = `url(${makeTile(o.tile)})`;
  grain.style.backgroundSize = `${o.tile}px ${o.tile}px`;
  if (cfg.grainOpacity != null) section.style.setProperty('--gl-grain-opacity', o.grainOpacity);

  let light = null, raf = 0, visible = false;
  const pos = { x: 0.7, y: 0.3 }, target = { x: 0.7, y: 0.3 };
  if (o.light) {
    light = document.createElement('div');
    light.className = 'gl-light';
    light.setAttribute('aria-hidden', 'true');
  }
  // Layers live in their own clipping box, so the host is never clipped (other parts may travel out of it).
  const layer = document.createElement('div');
  layer.className = 'gl-layer';
  layer.setAttribute('aria-hidden', 'true');
  layer.append(...[light, grain].filter(Boolean));
  section.appendChild(layer);

  const onMove = (e) => {
    const r = section.getBoundingClientRect();
    target.x = (e.clientX - r.left) / r.width;
    target.y = (e.clientY - r.top) / r.height;
  };
  const tick = (t) => {
    if (!fine.matches) { target.x = 0.5 + Math.cos(t * o.drift) * 0.3; target.y = 0.4 + Math.sin(t * o.drift * 1.3) * 0.2; }
    pos.x += (target.x - pos.x) * o.follow;
    pos.y += (target.y - pos.y) * o.follow;
    light.style.transform = `translate3d(${(pos.x * 100).toFixed(2)}%, ${(pos.y * 100).toFixed(2)}%, 0)`;
    if (visible) raf = requestAnimationFrame(tick);
  };
  // Only run the light while the section is on screen.
  const io = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting && !reduced.matches && !!light;
    cancelAnimationFrame(raf);
    if (visible) raf = requestAnimationFrame(tick);
  });
  io.observe(section);
  section.addEventListener('pointermove', onMove);

  return {
    destroy() { io.disconnect(); cancelAnimationFrame(raf); section.removeEventListener('pointermove', onMove); layer.remove(); section.classList.remove('gl-host'); },
  };
}
