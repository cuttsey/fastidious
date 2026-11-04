// supermock shoot: render an HTML artwork (poster, billboard, screen) to an exact-size PNG.
// node shoot.mjs <file.html|url> --w 2400 --h 1200 --out art.png
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { Browser, sleep } from '../../design-taste-frontend/scripts/lib/cdp.mjs';
const a = process.argv.slice(2), opt = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : a[i + 1]; };
const src = /^https?:/.test(a[0]) ? a[0] : pathToFileURL(resolve(a[0])).href, W = Number(opt('w', 1920)), H = Number(opt('h', 1080));
const b = await Browser.launch({ width: W, height: H }); const p = await b.newPage({ width: W, height: H, dsf: 1 });
await p.goto(src, { settleMs: 600 }); await p.eval('document.fonts.ready.then(() => true)'); await sleep(500);
await p.screenshot({ path: resolve(opt('out', 'art.png')), format: 'png' }); await b.close(); console.log('art', opt('out', 'art.png')); process.exit(0);
