/*!
 * live-status — Fastidious parts library. Original part (MIT), built from WANTED.md:
 * "a small line that shows something real changing, wired to a real source".
 * Two honest sources only: a published schedule (computed in the business's own time zone),
 * or a live data function. It never invents a value: if live data fails or goes stale, it says so.
 * No dependencies.
 */
const DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
const DAY_NAMES = { sun: 'Sunday', mon: 'Monday', tue: 'Tuesday', wed: 'Wednesday', thu: 'Thursday', fri: 'Friday', sat: 'Saturday' };

const DEFAULTS = {
  timeZone: 'Europe/London',
  schedule: null,     // { mon: [['07:00','19:00']], tue: [...], ... } in the business's time zone
  source: null,       // async () => ({ text, state: 'on' | 'off' | 'warn', at: Date }) for live data
  every: 60000,       // refresh interval in ms
  staleAfter: 15 * 60000,
  labels: {
    open: (close) => `Open now · closes ${close}`,
    closingSoon: (close) => `Closing soon · ${close}`,
    closed: (day, time) => `Closed · opens ${day} ${time}`,
    stale: (time) => `Last updated ${time}`,
    unavailable: 'Live status unavailable',
  },
  soonMinutes: 30,
};

// Current day and minutes-since-midnight in the business's time zone, whatever the visitor's zone.
const nowIn = (tz, date = new Date()) => {
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: tz, weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
    .formatToParts(date).map((p) => [p.type, p.value]));
  return { day: parts.weekday.slice(0, 3).toLowerCase(), mins: Number(parts.hour) * 60 + Number(parts.minute) };
};
const toMins = (hhmm) => { const [h, m] = hhmm.split(':').map(Number); return h * 60 + m; };

export function scheduleStatus(schedule, tz, labels, soon, date) {
  const { day, mins } = nowIn(tz, date);
  for (const [open, close] of schedule[day] || []) {
    if (mins >= toMins(open) && mins < toMins(close)) {
      return toMins(close) - mins <= soon ? { state: 'warn', text: labels.closingSoon(close) } : { state: 'on', text: labels.open(close) };
    }
  }
  const di = DAYS.indexOf(day);
  for (let k = 0; k < 8; k++) {
    const d = DAYS[(di + k) % 7];
    const next = (schedule[d] || []).map(([o]) => o).find((o) => k > 0 || toMins(o) > mins);
    if (next) return { state: 'off', text: labels.closed(k === 0 ? 'today' : k === 1 ? 'tomorrow' : DAY_NAMES[d], next) };
  }
  return { state: 'off', text: labels.closed('', '') };
}

export function mountLiveStatus(el, cfg = {}) {
  const o = { ...DEFAULTS, ...cfg, labels: { ...DEFAULTS.labels, ...(cfg.labels || {}) } };
  el.classList.add('ls');
  el.setAttribute('role', 'status');
  el.innerHTML = '<span class="ls-dot" aria-hidden="true"></span><span class="ls-text"></span>';
  const text = el.querySelector('.ls-text');
  let timer = 0;

  const render = ({ state, text: t }) => {
    if (text.textContent !== t) text.textContent = t; // only changes are announced
    el.dataset.state = state;
  };

  const update = async () => {
    if (o.source) {
      try {
        const r = await o.source();
        const age = Date.now() - new Date(r.at || Date.now()).getTime();
        const time = new Date(r.at || Date.now()).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: o.timeZone });
        render(age > o.staleAfter ? { state: 'off', text: o.labels.stale(time) } : r);
      } catch {
        render({ state: 'off', text: o.labels.unavailable });
      }
    } else if (o.schedule) {
      render(scheduleStatus(o.schedule, o.timeZone, o.labels, o.soonMinutes));
    }
  };

  update();
  timer = setInterval(update, o.every);
  const onVis = () => { if (!document.hidden) update(); };
  document.addEventListener('visibilitychange', onVis);
  return { update, destroy() { clearInterval(timer); document.removeEventListener('visibilitychange', onVis); } };
}
