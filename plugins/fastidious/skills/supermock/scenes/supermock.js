// supermock scene library: time-stepped rendering, keyframes, easing, frame sequences and corner pinning.
window.SM = (() => {
  const cfg = window.SUPERMOCK_CONFIG || {};
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ease = {
    linear: (t) => t,
    inOut: (t) => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    out: (t) => 1 - Math.pow(1 - t, 3),
    spring: (t) => { const c = 1.70158 * 1.2; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); },  // small overshoot
  };
  // Interpolate numeric keys across keyframes [{t, ...}] with optional per-key "ease".
  const keys = (frames, t) => {
    if (!frames || !frames.length) return {};
    if (t <= frames[0].t) return { ...frames[0] };
    for (let i = 0; i < frames.length - 1; i++) {
      const a = frames[i], b = frames[i + 1];
      if (t <= b.t) { const k = (ease[b.ease] || ease.inOut)((t - a.t) / (b.t - a.t)); const o = {};
        for (const n in b) if (typeof b[n] === 'number' && n !== 't') o[n] = (a[n] ?? b[n]) + (b[n] - (a[n] ?? b[n])) * k; return { ...a, ...o }; }
    }
    return { ...frames[frames.length - 1] };
  };
  const span = (t, t0, t1, e = 'inOut') => (ease[e] || ease.inOut)(clamp((t - t0) / (t1 - t0)));
  // Frame sequence: set an <img> to frame i of a captured sequence and wait until it is painted.
  const seq = (img, dir, count) => async (i) => {
    const n = Math.max(0, Math.min(count - 1, Math.round(i)));
    const src = `${dir}/f${String(n).padStart(4, '0')}.png`;
    if (img.dataset.src !== src) { img.dataset.src = src; img.src = src; try { await img.decode(); } catch {} }
  };
  const loadImg = (src) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => ok(i); i.src = src; });
  // Corner pin: CSS matrix3d that maps a w×h box (transform-origin 0 0) onto four points [tl, tr, br, bl].
  const pin = (w, h, q) => {
    const src = [[0, 0], [w, 0], [w, h], [0, h]], A = [], B = [];
    for (let i = 0; i < 4; i++) { const [x, y] = src[i], [u, v] = q[i];
      A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.push(u); A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); B.push(v); }
    for (let c = 0; c < 8; c++) { let p = c; for (let r = c + 1; r < 8; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      [A[c], A[p]] = [A[p], A[c]]; [B[c], B[p]] = [B[p], B[c]];
      for (let r = 0; r < 8; r++) if (r !== c) { const f = A[r][c] / A[c][c]; for (let k = c; k < 8; k++) A[r][k] -= f * A[c][k]; B[r] -= f * B[c]; } }
    const [a, b, c, d, e, f, g, hh] = B.map((v, i) => v / A[i][i]);
    return `matrix3d(${a},${d},0,${g},${b},${e},0,${hh},0,0,1,0,${c},${f},0,1)`;
  };
  let resolveReady; const ready = new Promise((r) => { resolveReady = r; });
  window.SUPERMOCK = { ready, renderAt: async () => {} };
  const scene = (setup, render) => { (async () => { await setup(cfg); window.SUPERMOCK.renderAt = (t) => render(t, cfg); await render(0, cfg); resolveReady(); })(); };
  // Preview in a normal browser (no render.mjs): play in real time.
  if (!window.SUPERMOCK_CONFIG) addEventListener('load', () => { const t0 = performance.now(), d = cfg.duration || 8; const tick = async () => { await window.SUPERMOCK.renderAt(((performance.now() - t0) / 1000) % d); requestAnimationFrame(tick); }; ready.then(tick); });
  return { cfg, clamp, ease, keys, span, seq, loadImg, pin, scene };
})();
