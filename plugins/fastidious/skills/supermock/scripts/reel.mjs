// supermock reel: join clips into one showreel with crossfades, scaled onto one canvas.
// node reel.mjs --out reel.mp4 [--w 1920 --h 1080] [--fade 0.6] [--bg 0E2318] clip1.mp4 clip2.mp4 ...
import { execFileSync } from 'node:child_process';
const a = process.argv.slice(2); const opt = (k, d) => { const i = a.indexOf('--' + k); return i < 0 ? d : a[i + 1]; };
const clips = a.filter((x, i) => x.endsWith('.mp4') && a[i - 1] !== '--out');
const W = Number(opt('w', 1920)), H = Number(opt('h', 1080)), F = Number(opt('fade', 0.6)), bg = opt('bg', '0E2318'), out = opt('out', 'reel.mp4');
const dur = clips.map((c) => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', c]).toString()));
let f = clips.map((_, i) => `[${i}:v]scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:color=${bg},fps=30,format=yuv420p,setsar=1[v${i}]`).join(';');
let last = 'v0', t = dur[0];
for (let i = 1; i < clips.length; i++) { f += `;[${last}][v${i}]xfade=transition=fade:duration=${F}:offset=${(t - F).toFixed(3)}[x${i}]`; last = `x${i}`; t += dur[i] - F; }
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...clips.flatMap((c) => ['-i', c]), '-filter_complex', f, '-map', `[${last}]`, '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: 'inherit' });
console.log('reel', out, t.toFixed(1) + 's');
