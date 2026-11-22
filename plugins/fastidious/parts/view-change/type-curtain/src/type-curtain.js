/*!
 * type-curtain — Fastidious parts library
 * Adapted from "Kinetic Typography Page Transition" by Codrops (MIT),
 * https://github.com/codrops/KineticTypePageTransition — Copyright (c) 2009 - 2021 Codrops. See LICENSE.
 * Changes: rebuilt as a transition you call around any change of view (`await curtain.play(swap)`),
 * instead of being wired to one demo's articles; the words come from the brand, not the demo; the
 * wall builds itself from a word list; the "in" is about 40% faster than the source's 2.5 s; the
 * swap happens while the type covers the screen; reduced motion swaps behind a short fade.
 */
import { gsap } from 'gsap';

const DEFAULTS = {
  words: ['word'],      // the brand's own vocabulary; 3 to 8 words work best
  lines: 11,            // rows in the wall
  repeat: 3,            // words per row
  speed: 1.4,           // time scale; 1 matches the source (2.5 s), 1.4 is about 1.8 s
  rotate: -90,
  scale: 2.7,
  swapAt: 0.5,          // fraction of the cover when the view underneath is swapped
  ground: true,         // a solid layer under the type hides the swap completely
};

export function mountTypeCurtain(cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const wall = document.createElement('div');
  wall.className = 'tc-wall';
  wall.setAttribute('aria-hidden', 'true');
  for (let i = 0; i < o.lines; i++) {
    const line = document.createElement('div');
    line.className = 'tc-line';
    line.textContent = Array(o.repeat).fill(o.words[i % o.words.length]).join(' ');
    wall.appendChild(line);
  }
  const ground = document.createElement('div');
  ground.className = 'tc-ground';
  ground.setAttribute('aria-hidden', 'true');
  document.body.append(ground, wall);
  const lines = [...wall.children];
  let busy = false;

  const reset = () => {
    gsap.set(wall, { scale: 1, rotate: 0, autoAlpha: 0 });
    gsap.set(ground, { autoAlpha: 0 });
    gsap.set(lines, { x: '0%', opacity: 0 });
  };
  reset();

  /** Runs the curtain. `swap` changes what is underneath (may be async); resolves when the view is revealed. */
  const play = (swap) => new Promise((resolve) => {
    if (busy) return resolve(false);
    busy = true;
    const done = () => { reset(); busy = false; resolve(true); };

    if (reduced()) {
      gsap.timeline({ onComplete: done })
        .set(wall, { autoAlpha: 1, scale: 1, rotate: 0 })
        .to(lines, { opacity: 1, duration: 0.2 })
        .add(async () => { await swap?.(); })
        .to(lines, { opacity: 0, duration: 0.25 }, '+=0.15');
      return;
    }

    const tl = gsap.timeline({ onComplete: done });
    tl.set(wall, { autoAlpha: 1 })
      .to(wall, { duration: 1.4, ease: 'power2.inOut', scale: o.scale, rotate: o.rotate }, 0)
      .to(lines, { keyframes: [{ x: '20%', duration: 1, ease: 'power1.inOut' }, { x: '-200%', duration: 1.5, ease: 'power1.in' }], stagger: 0.04 }, 0)
      .to(lines, { keyframes: [{ opacity: 1, duration: 1, ease: 'power1.in' }, { opacity: 0, duration: 1.5, ease: 'power1.in' }] }, 0);
    const at = tl.duration() * o.swapAt;
    if (o.ground) tl.to(ground, { autoAlpha: 1, duration: 0.45, ease: 'power2.in' }, at - 0.5).to(ground, { autoAlpha: 0, duration: 0.7, ease: 'power2.out' }, at + 0.1);
    tl.call(() => { tl.pause(); Promise.resolve(swap?.()).then(() => tl.resume()); }, null, at);
    tl.timeScale(o.speed);
  });

  return { play, get busy() { return busy; }, destroy: () => wall.remove() };
}
