/*
  scroll-film.js: one WebGL compositor for scroll-scrubbed frame sequences, with signature transitions.
  Part of Fastidious (render-engineer). MIT licence. No dependencies.

  Plays a sequence of scenes (folders made by make_sequence.py) on one full-screen canvas as the page scrolls:
  frames blend into each other so a short sequence still glides; scenes change through an iris, a grain dissolve,
  a push, a fade or a cut; incoming scenes can "develop" from grey to full colour; halftone, paper and film grain
  are optional devices. Native scrolling is never intercepted: the film follows the browser's own scroll position.

  Usage:
    <script src="scroll-film.js"></script>
    const film = ScrollFilm.mount({
      canvas: document.querySelector('canvas.film'),
      track: document.querySelector('main'),          // the element whose scroll range drives the film
      scenes: [
        { id: 'S01', src: 'frames/S01', at: 0.00, len: 0.20, out: { type: 'iris', len: 0.25, origin: [0.5, 0.45] } },
        { id: 'S02', src: 'frames/S02', at: 0.20, len: 0.20, develop: true, halftone: 0.8, focus: [0.6, 0.5] },
      ],
      grain: 0.04, paper: 0.0, ease: 0.14,
      onFrame: (state) => {}                          // optional: drive text from the film's state
    });

  at and len are fractions of the track's scroll range. out.len is a fraction of the scene's own length.
  focus is the focal point in the image (x, y from the top left, 0 to 1), kept in view when the screen crops it.

  The page must also carry, in its HTML, a poster image and the copy for every scene (see render-engineer's
  SKILL.md), so the story survives without WebGL or JavaScript. The kit adds `film-live` to <html> when it runs
  and `film-static` when it cannot (no WebGL); style posters by those classes. Elements with
  data-film-scene="<id>" get `is-active` while their scene plays and a --film-t custom property from 0 to 1.
  With prefers-reduced-motion, each scene shows its poster frame and changes by a fade: no scrubbing, no grain.
*/
(function (root) {
  'use strict';

  const MODES = { fade: 0, iris: 1, dissolve: 2, push: 3, cut: 4 };

  const VERT = 'attribute vec2 p;varying vec2 uv;void main(){uv=p*.5+.5;gl_Position=vec4(p,0.,1.);}';
  const FRAG = `precision mediump float;
uniform sampler2D tA,tB,tC;uniform vec2 res,imA,imC,focA,focC,origin;
uniform float mixAB,trans,mode,grain,time,develop,halftone,paper,dpr;varying vec2 uv;
vec2 cover(vec2 p,vec2 im,vec2 foc){float ca=res.x/res.y,ia=im.x/im.y;vec2 q=p;vec2 f=vec2(foc.x,1.-foc.y);
 if(ca>ia){float s=ia/ca;q.y=(p.y-.5)*s+.5+(f.y-.5)*(1.-s);}else{float s=ca/ia;q.x=(p.x-.5)*s+.5+(f.x-.5)*(1.-s);}return q;}
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float vnoise(vec2 x){vec2 i=floor(x),f=fract(x);float a=hash(i),b=hash(i+vec2(1,0)),c=hash(i+vec2(0,1)),d=hash(i+vec2(1,1));
 vec2 u=f*f*(3.-2.*f);return mix(a,b,u.x)+(c-a)*u.y*(1.-u.x)+(d-b)*u.x*u.y;}
vec3 sat(vec3 c,float s){float l=dot(c,vec3(.2126,.7152,.0722));return mix(vec3(l),c,s);}
vec3 dots(sampler2D t,vec2 p,vec2 im,vec2 foc){float cell=7.*dpr;vec2 g=floor(gl_FragCoord.xy/cell)*cell+cell*.5;
 vec3 c=texture2D(t,cover(g/res,im,foc)).rgb;float l=dot(c,vec3(.299,.587,.114));
 float r=sqrt(1.-l)*.62*cell;float d=length(gl_FragCoord.xy-g);return mix(vec3(.95,.93,.88),c*.92,1.-smoothstep(r-1.,r+1.,d));}
vec3 shotA(vec2 p){vec3 a=texture2D(tA,cover(p,imA,focA)).rgb,b=texture2D(tB,cover(p,imA,focA)).rgb;vec3 c=mix(a,b,mixAB);
 if(halftone>0.)c=mix(c,dots(tA,p,imA,focA),halftone);return c;}
void main(){vec2 p=uv;vec3 A,C;float k=0.;
 if(mode>2.5&&mode<3.5){A=shotA(vec2(p.x,p.y-trans));C=texture2D(tC,cover(vec2(p.x,p.y+1.-trans),imC,focC)).rgb;k=step(p.y,trans);}
 else{A=shotA(p);C=texture2D(tC,cover(p,imC,focC)).rgb;
  if(mode<.5)k=trans;
  else if(mode<1.5){vec2 asp=vec2(res.x/res.y,1.);float n=vnoise(p*res/(180.*dpr)+time*.05);
   float d=length((p-origin)*asp);k=1.-smoothstep(-.04,.04,d+n*.14-trans*1.6);}
  else if(mode<2.5){float n=hash(floor(gl_FragCoord.xy/(2.*dpr)));float m=vnoise(p*res/(260.*dpr));
   k=step(n*.35+m*.65,trans*1.3-.12);}
  else k=step(.5,trans);}
 vec3 col=mix(A,C,k);col=sat(col,1.-develop);
 if(paper>0.)col*=1.-paper*(vnoise(gl_FragCoord.xy/(3.*dpr))*.5+vnoise(gl_FragCoord.xy/(40.*dpr))*.5);
 if(grain>0.)col+=(hash(gl_FragCoord.xy+fract(time)*97.)-.5)*grain;
 gl_FragColor=vec4(col,1.);}`;

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const smooth = t => t * t * (3 - 2 * t);

  // Pure: which scene plays at progress p, its local time, and the transition into the next. Exported for tests.
  function locate(scenes, p) {
    let i = 0;
    for (let k = 0; k < scenes.length; k++) if (p >= scenes[k].at) i = k;
    const s = scenes[i];
    const t = clamp((p - s.at) / s.len, 0, 1);
    let trans = 0;
    const next = scenes[i + 1];
    if (s.out && next && s.out.type !== 'none') {
      const ol = clamp(s.out.len || 0.2, 0.01, 1);
      trans = clamp((t - (1 - ol)) / ol, 0, 1);
    }
    return { index: i, id: s.id, t, trans, next: next ? i + 1 : -1 };
  }

  // Pure: the order to fetch frames in, nearest to what is on screen first. Exported for tests.
  function priority(counts, index, frame, window) {
    const out = [];
    counts.forEach((n, s) => {
      for (let f = 0; f < n; f++) {
        const sceneGap = s === index ? 0 : s === index + 1 ? 1 : Math.abs(s - index) + 1;
        const d = s === index ? Math.abs(f - frame) : sceneGap * (window || 1000) + f;
        out.push([d, s, f]);
      }
    });
    return out.sort((a, b) => a[0] - b[0]).map(x => [x[1], x[2]]);
  }

  function mount(opts) {
    const html = document.documentElement;
    const canvas = opts.canvas;
    const scenes = opts.scenes.map(s => Object.assign({ focus: [0.5, 0.5] }, s));
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const small = matchMedia('(max-width: 820px)').matches;
    const gl = canvas && (canvas.getContext('webgl', { antialias: false, alpha: false, preserveDrawingBuffer: false }) ||
      canvas.getContext('experimental-webgl'));
    if (!gl) { html.classList.add('film-static'); return null; }

    const prog = gl.createProgram();
    for (const [type, src] of [[gl.VERTEX_SHADER, VERT], [gl.FRAGMENT_SHADER, FRAG]]) {
      const sh = gl.createShader(type);
      gl.shaderSource(sh, src);
      gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) { console.error(gl.getShaderInfoLog(sh)); html.classList.add('film-static'); return null; }
      gl.attachShader(prog, sh);
    }
    gl.linkProgram(prog);
    gl.useProgram(prog);
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'p');
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    const U = {};
    for (const n of ['tA', 'tB', 'tC', 'res', 'imA', 'imC', 'focA', 'focC', 'origin', 'mixAB', 'trans', 'mode', 'grain', 'time', 'develop', 'halftone', 'paper', 'dpr'])
      U[n] = gl.getUniformLocation(prog, n);
    const tex = [0, 1, 2].map(unit => {
      const t = gl.createTexture();
      gl.activeTexture(gl.TEXTURE0 + unit);
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      for (const [p, v] of [[gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE], [gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR]])
        gl.texParameteri(gl.TEXTURE_2D, p, v);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([20, 18, 16, 255]));
      t.src = null;
      return t;
    });
    gl.uniform1i(U.tA, 0); gl.uniform1i(U.tB, 1); gl.uniform1i(U.tC, 2);

    function upload(unit, img) {
      if (!img || tex[unit].src === img) return;
      gl.activeTexture(gl.TEXTURE0 + unit);
      gl.bindTexture(gl.TEXTURE_2D, tex[unit]);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
      tex[unit].src = img;
    }

    // Loading: manifest, then the poster, then frames nearest the playhead first, six at a time.
    const state = { p: 0, target: 0, scene: null, ready: false };
    let active = 0;
    const MAX = 6;
    scenes.forEach(s => {
      s.frames = [];
      s.requested = new Set();
      s.count = 0;
      fetch(s.src.replace(/\/$/, '') + '/manifest.json').then(r => r.json()).then(m => {
        s.m = m;
        s.count = reduced ? 0 : m.count;
        s.size = small ? m.sizes[m.sizes.length - 1] : m.sizes[0];
        const poster = new Image();
        poster.decoding = 'async';
        poster.onload = () => { s.poster = poster; };
        poster.src = s.src.replace(/\/$/, '') + '/poster.jpg';
      }).catch(() => {});
    });
    const frameURL = (s, f) => s.src.replace(/\/$/, '') + '/' + s.m.pattern.replace('{size}', s.size)
      .replace('{n}', String(f + 1).padStart(s.m.pad || 3, '0'));
    function pump(loc) {
      if (active >= MAX) return;
      const order = priority(scenes.map(s => s.count || 0), loc.index, Math.round(loc.t * Math.max(0, (scenes[loc.index].count || 1) - 1)), 1000);
      for (const [si, f] of order) {
        if (active >= MAX) break;
        const s = scenes[si];
        if (!s.m || s.requested.has(f)) continue;
        s.requested.add(f);
        active++;
        const img = new Image();
        img.decoding = 'async';
        img.onload = () => { (img.decode ? img.decode() : Promise.resolve()).catch(() => {}).then(() => { s.frames[f] = img; active--; }); };
        img.onerror = () => { active--; };
        img.src = frameURL(s, f);
      }
    }
    function nearest(s, f) {
      for (let d = 0; d < (s.count || 1); d++) {
        if (s.frames[f - d]) return s.frames[f - d];
        if (s.frames[f + d]) return s.frames[f + d];
      }
      return s.poster || null;
    }
    function shot(s, t) {
      if (!s.m) return [null, null, 0];
      if (reduced || !s.count) return [s.poster, s.poster, 0];
      const x = t * (s.count - 1), f = Math.floor(x);
      return [nearest(s, f), nearest(s, Math.min(s.count - 1, f + 1)), x - f];
    }

    // Track progress from the native scroll position. Nothing here prevents or replaces scrolling.
    const track = opts.track || html;
    function nativeProgress() {
      const r = track.getBoundingClientRect();
      const range = Math.max(1, r.height - innerHeight);
      return clamp(-r.top / range, 0, 1);
    }
    const marks = Array.from(document.querySelectorAll('[data-film-scene]'));
    let dprCap = small ? 1.5 : 2, slow = 0, lastT = 0, raf = 0;
    const t0 = performance.now();
    function frame(now) {
      raf = requestAnimationFrame(frame);
      const dt = lastT ? now - lastT : 16.7;
      lastT = now;
      if (dt > 28) slow++; else slow = Math.max(0, slow - 1);
      if (slow > 120 && dprCap > 1) { dprCap = Math.max(1, dprCap - 0.25); slow = 0; }
      const dpr = Math.min(devicePixelRatio || 1, dprCap);
      const w = Math.round(canvas.clientWidth * dpr), h = Math.round(canvas.clientHeight * dpr);
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; gl.viewport(0, 0, w, h); }
      state.target = nativeProgress();
      state.p = reduced ? state.target : state.p + (state.target - state.p) * (opts.ease || 0.14);
      if (Math.abs(state.target - state.p) < 1e-5) state.p = state.target;
      const L = locate(scenes, state.p);
      state.scene = L;
      pump(L);
      const s = scenes[L.index], n = L.next >= 0 ? scenes[L.next] : null;
      const [a, b, mx] = shot(s, L.t);
      upload(0, a); upload(1, b);
      if (n) upload(2, shot(n, 0)[0] || a);
      const im = img => img ? [img.naturalWidth || 16, img.naturalHeight || 9] : [16, 9];
      const mode = reduced ? MODES.fade : MODES[(s.out && s.out.type) || 'fade'];
      gl.uniform2f(U.res, w, h);
      gl.uniform2fv(U.imA, im(a)); gl.uniform2fv(U.imC, im(n ? tex[2].src : a));
      gl.uniform2fv(U.focA, s.focus); gl.uniform2fv(U.focC, n ? n.focus : s.focus);
      gl.uniform2fv(U.origin, (s.out && s.out.origin) || [0.5, 0.5]);
      gl.uniform1f(U.mixAB, mx);
      gl.uniform1f(U.trans, L.trans);
      gl.uniform1f(U.mode, mode);
      gl.uniform1f(U.grain, reduced ? 0 : (opts.grain || 0));
      gl.uniform1f(U.paper, opts.paper || 0);
      gl.uniform1f(U.time, reduced ? 0 : (now - t0) / 1000);
      gl.uniform1f(U.dpr, dpr);
      gl.uniform1f(U.develop, s.develop && !reduced ? 0.45 * (1 - smooth(clamp(L.t / 0.35, 0, 1))) : 0);
      gl.uniform1f(U.halftone, s.halftone && !reduced ? s.halftone * (1 - smooth(clamp(L.t / 0.6, 0, 1))) : 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (a && !state.ready) { state.ready = true; html.classList.add('film-ready'); }
      for (const el of marks) {
        const on = el.dataset.filmScene === L.id;
        el.classList.toggle('is-active', on);
        if (on) el.style.setProperty('--film-t', L.t.toFixed(4));
      }
      if (opts.onFrame) opts.onFrame(state);
    }
    html.classList.add('film-live');
    raf = requestAnimationFrame(frame);
    return {
      state,
      destroy() { cancelAnimationFrame(raf); html.classList.remove('film-live', 'film-ready'); }
    };
  }

  const api = { mount, locate, priority, MODES };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.ScrollFilm = api;
})(typeof window !== 'undefined' ? window : globalThis);
