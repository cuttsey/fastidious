// Matte: a framed image never shows an empty band. When an image is fitted inside its box
// (object-fit: contain, or a fixed aspect frame) and the picture is opaque, the frame takes the
// picture's own edge colour, so letterboxing reads as more paper or more sky, not a white bar.
// Transparent cut-outs are left alone (they sit on the designed ground). Same-origin images only.
(() => {
  const SAMPLE = 48;
  const edgeColour = (img) => {
    const c = document.createElement('canvas'), w = SAMPLE, h = Math.max(1, Math.round(SAMPLE * img.naturalHeight / img.naturalWidth));
    c.width = w; c.height = h; const x = c.getContext('2d', { willReadFrequently: true });
    x.drawImage(img, 0, 0, w, h);
    let d; try { d = x.getImageData(0, 0, w, h).data; } catch { return null; }         // cross-origin: leave as designed
    let r = 0, g = 0, b = 0, n = 0, transparent = false;
    const take = (i) => { const k = i * 4; if (d[k + 3] < 250) transparent = true; r += d[k]; g += d[k + 1]; b += d[k + 2]; n++; };
    for (let i = 0; i < w; i++) { take(i); take((h - 1) * w + i); }
    for (let j = 1; j < h - 1; j++) { take(j * w); take(j * w + w - 1); }
    return transparent ? null : `rgb(${Math.round(r / n)}, ${Math.round(g / n)}, ${Math.round(b / n)})`;
  };
  const fitted = (img) => {
    const cs = getComputedStyle(img); if (!['contain', 'scale-down'].includes(cs.objectFit)) return false;
    const box = img.clientWidth / Math.max(1, img.clientHeight), pic = img.naturalWidth / Math.max(1, img.naturalHeight);
    return Math.abs(box / pic - 1) > 0.01;                                              // the picture doesn't fill its box
  };
  const apply = (img) => {
    if (!img.naturalWidth || img.dataset.matte === 'off' || !fitted(img)) return;
    if (!img.dataset.matteColour) { const col = edgeColour(img); img.dataset.matteColour = col || 'none'; }
    if (img.dataset.matteColour !== 'none') img.style.backgroundColor = img.dataset.matteColour;
  };
  const all = () => document.querySelectorAll('img').forEach((img) => { if (img.complete) apply(img); else img.addEventListener('load', () => apply(img), { once: true }); });
  all(); addEventListener('resize', all); addEventListener('load', all);
})();
