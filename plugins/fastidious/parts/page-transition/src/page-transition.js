/*!
 * page-transition — Fastidious parts library
 * Original Fastidious part (MIT). The shared-element idea (a picture, title or price morphing from
 * an index card into its own page) follows Codrops' "Animating Multi-Page Navigations with Browser
 * View Transitions and Astro" (MIT, https://github.com/codrops/astro-shop-view-transitions);
 * no code from that Astro demo is used.
 *
 * A framework-neutral shell for moving between pages:
 *   1. View Transitions API where the browser has it (same-document swap, with shared elements);
 *   2. otherwise any view-change part (`type-curtain`, `pixel-cover`) through `await cover.play(swap)`;
 *   3. otherwise a plain swap.
 * Same-origin links only; everything else navigates normally. History, focus, title and an
 * announcement for screen readers are handled. A failed fetch falls back to a normal page load.
 */

const DEFAULTS = {
  container: '[data-pt-container]',  // the part of the page that changes; everything outside it stays
  links: 'a[href]',
  cover: null,                       // optional view-change part instance with play(swap)
  useViewTransitions: true,
  prefetch: true,                    // fetch on hover or focus, so the swap is instant
  onLeave: null,                     // (oldContainer) => void: destroy parts mounted in the old page
  onEnter: null,                     // (newContainer, url) => void: mount parts in the new page
};

export function mountPageTransition(cfg = {}) {
  const o = { ...DEFAULTS, ...cfg };
  const cache = new Map();
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  let busy = false;

  const live = document.createElement('p');
  live.className = 'pt-announce';
  live.setAttribute('aria-live', 'polite');
  document.body.appendChild(live);

  const sameSite = (a) => {
    if (!a || a.target && a.target !== '_self' || a.hasAttribute('download') || a.dataset.ptSkip != null) return false;
    const u = new URL(a.href, location.href);
    if (u.origin !== location.origin) return false;
    if (u.pathname === location.pathname && u.search === location.search && u.hash) return false; // in-page anchor
    return true;
  };

  const load = (url) => {
    if (!cache.has(url)) {
      cache.set(url, fetch(url, { credentials: 'same-origin' })
        .then((r) => (r.ok ? r.text() : Promise.reject(r.status)))
        .then((html) => new DOMParser().parseFromString(html, 'text/html'))
        .catch((e) => { cache.delete(url); throw e; }));
    }
    return cache.get(url);
  };

  // Shared elements: inside the clicked link and inside the new page's matching group,
  // elements marked data-pt-name get the same view-transition-name, so the browser morphs them.
  const name = (group, n) => `pt-${group}-${n}`.replace(/[^a-zA-Z0-9_-]/g, '-');
  const tagShared = (root, group) => {
    if (!root || !group) return [];
    const els = [...root.querySelectorAll('[data-pt-name]')];
    els.forEach((el) => { el.style.viewTransitionName = name(group, el.dataset.ptName); });
    return els;
  };
  const untag = (els) => els.forEach((el) => { el.style.viewTransitionName = ''; });

  async function go(url, { push = true, from = null } = {}) {
    if (busy) return;
    busy = true;
    let doc;
    try { doc = await load(url); } catch { location.href = url; return; }
    const next = doc.querySelector(o.container);
    const current = document.querySelector(o.container);
    if (!next || !current) { location.href = url; return; }
    const group = from?.closest('[data-pt-group]')?.dataset.ptGroup || null;

    const swap = () => {
      o.onLeave?.(current);
      const fresh = document.importNode(next, true);
      current.replaceWith(fresh);
      document.title = doc.title;
      if (push) history.pushState({ pt: true }, '', url);
      window.scrollTo(0, 0);
      const target = fresh.querySelector('h1') || fresh;
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
      live.textContent = doc.title;
      o.onEnter?.(fresh, url);
      return fresh;
    };

    try {
      if (o.useViewTransitions && document.startViewTransition && !reduced()) {
        const old = tagShared(from?.closest('[data-pt-group]'), group);
        const vt = document.startViewTransition(() => {
          untag(old);
          const fresh = swap();
          const pageGroup = fresh.querySelector(`[data-pt-group="${CSS.escape(group || '')}"]`) || (fresh.dataset.ptGroup === group ? fresh : null);
          const neu = tagShared(pageGroup, group);
          vt.finished.finally(() => untag(neu));
        });
        await vt.finished;
      } else if (o.cover && !reduced()) {
        await o.cover.play(swap);
      } else {
        swap();
      }
    } finally {
      busy = false;
    }
  }

  const onClick = (e) => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest(o.links);
    if (!sameSite(a)) return;
    e.preventDefault();
    go(a.href, { from: a });
  };
  const onIntent = (e) => {
    if (!o.prefetch) return;
    const a = e.target.closest?.(o.links);
    if (sameSite(a)) load(a.href).catch(() => {});
  };
  const onPop = () => go(location.href, { push: false });

  document.addEventListener('click', onClick);
  document.addEventListener('pointerover', onIntent, { passive: true });
  document.addEventListener('focusin', onIntent);
  window.addEventListener('popstate', onPop);
  history.replaceState({ pt: true }, '');

  return {
    go: (url) => go(new URL(url, location.href).href),
    destroy() {
      document.removeEventListener('click', onClick);
      document.removeEventListener('pointerover', onIntent);
      document.removeEventListener('focusin', onIntent);
      window.removeEventListener('popstate', onPop);
      live.remove();
    },
  };
}
