// 소품 · 배경 스프라이트(SVG → PNG) 생성: node tools/make_sprites.js
const sharp = require('sharp'), path = require('path');
const OUT = path.join(__dirname, '..', 'resource');
const S = {};
const shadow = (cx, y, rx) => `<ellipse cx="${cx}" cy="${y}" rx="${rx}" ry="4" fill="#000" opacity=".18"/>`;

// ---- 책상 위 (바닥선 = 높이) ----
S.monitor = [188, 118, `
  ${shadow(94,115,50)}
  <rect x="64" y="108" width="60" height="8" rx="3" fill="#3a3d55"/>
  <rect x="88" y="86" width="12" height="24" fill="#4a4e69"/>
  <rect x="4" y="2" width="180" height="88" rx="6" fill="#1f2133"/>
  <defs><linearGradient id="sc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a1d6e"/><stop offset="1" stop-color="#b03a8c"/></linearGradient></defs>
  <rect x="10" y="8" width="168" height="74" rx="2" fill="url(#sc)"/>
  <rect x="18" y="16" width="60" height="5" rx="2" fill="#f2a541"/><rect x="18" y="27" width="92" height="5" rx="2" fill="#9fd3c7"/>
  <rect x="30" y="38" width="70" height="5" rx="2" fill="#e9e4f0"/><rect x="30" y="49" width="48" height="5" rx="2" fill="#e76f51"/>
  <rect x="18" y="60" width="80" height="5" rx="2" fill="#9fd3c7"/>
  <path d="M120 8 L178 8 L178 40 Z" fill="#fff" opacity=".08"/>`];
S.keyboard = [88, 26, `${shadow(44,24,40)}<rect x="2" y="6" width="84" height="16" rx="4" fill="#c9ccd6"/>
  ${[0,1].map(r=>[...Array(9)].map((_,c)=>`<rect x="${7+c*9}" y="${9+r*6}" width="6" height="4" rx="1" fill="#f7f7fa"/>`).join('')).join('')}`];
S.gaming_kb = [88, 28, `<defs><linearGradient id="rgb" x1="0" x2="1"><stop offset="0" stop-color="#ff4d8d"/><stop offset=".5" stop-color="#7b5cff"/><stop offset="1" stop-color="#2ee6d6"/></linearGradient></defs>
  <rect x="0" y="20" width="88" height="6" rx="3" fill="url(#rgb)" opacity=".7"/>
  <rect x="2" y="6" width="84" height="16" rx="4" fill="#1f2133"/>
  ${[0,1].map(r=>[...Array(9)].map((_,c)=>`<rect x="${7+c*9}" y="${9+r*6}" width="6" height="4" rx="1" fill="url(#rgb)"/>`).join('')).join('')}`];
const lamp = (shade, glow) => [88, 104, `
  <path d="M60 30 L88 104 L20 104 Z" fill="${glow}" opacity=".22"/>
  ${shadow(28,101,22)}<ellipse cx="28" cy="98" rx="20" ry="5" fill="#3a3d55"/>
  <rect x="25" y="40" width="6" height="58" fill="#4a4e69"/>
  <path d="M28 44 L56 22" stroke="#4a4e69" stroke-width="6" stroke-linecap="round"/>
  <path d="M40 8 L76 22 L66 40 L34 24 Z" fill="${shade}"/>
  <circle cx="58" cy="33" r="5" fill="${glow}"/>`];
S.lamp_warm = lamp('#f2a541', '#ffd27a');
S.lamp_cool = lamp('#a9d6ea', '#e8f8ff');
S.book = [88, 62, `${shadow(44,60,40)}
  <rect x="8" y="44" width="72" height="14" rx="2" fill="#5b8db8"/><rect x="8" y="44" width="72" height="3" fill="#fff" opacity=".5"/>
  <rect x="14" y="30" width="62" height="14" rx="2" fill="#e76f51"/><rect x="14" y="30" width="62" height="3" fill="#fff" opacity=".5"/>
  <rect x="10" y="16" width="66" height="14" rx="2" fill="#6a9c78"/><rect x="10" y="16" width="66" height="3" fill="#fff" opacity=".5"/>
  <rect x="58" y="2" width="12" height="14" rx="1" fill="#f2a541" transform="rotate(12 64 9)"/>`];
S.mug = [88, 52, `${shadow(40,50,22)}
  <path d="M34 4 q-6 6 0 12 q6 6 0 12" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/>
  <path d="M46 2 q-6 6 0 12 q6 6 0 12" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>
  <rect x="22" y="20" width="38" height="30" rx="5" fill="#fafafa" stroke="#d5d8e0" stroke-width="2"/>
  <path d="M60 26 q14 0 14 10 q0 10 -14 10" stroke="#d5d8e0" stroke-width="5" fill="none"/>
  <rect x="22" y="30" width="38" height="6" fill="#e76f51"/>`];
S.mini_plant = [88, 76, `${shadow(44,74,24)}
  <path d="M44 44 C30 30 20 34 14 20 C30 20 40 28 44 44" fill="#6a9c78"/>
  <path d="M44 44 C58 28 70 32 76 16 C58 18 48 28 44 44" fill="#5a8a68"/>
  <path d="M44 46 C40 26 46 12 44 2 C52 14 50 30 44 46" fill="#7fb38b"/>
  <path d="M28 46 L60 46 L55 74 L33 74 Z" fill="#d9774f"/><rect x="26" y="44" width="36" height="7" rx="2" fill="#e88b62"/>`];
S.mic = [88, 100, `${shadow(44,98,26)}<ellipse cx="44" cy="95" rx="24" ry="5" fill="#2b2d42"/>
  <rect x="41" y="50" width="6" height="46" fill="#4a4e69"/>
  <rect x="30" y="8" width="28" height="46" rx="14" fill="#2b2d42"/>
  ${[0,1,2,3,4].map(i=>`<rect x="34" y="${14+i*7}" width="20" height="2" fill="#8d99ae"/>`).join('')}
  <rect x="52" y="44" width="10" height="4" rx="2" fill="#e76f51"/>`];

// ---- 벽 (밴드 안 가운데) ----
S.shelf = [188, 74, `
  <rect x="20" y="10" width="14" height="44" rx="3" fill="#e76f51"/><rect x="36" y="16" width="14" height="38" rx="3" fill="#5b8db8"/>
  <rect x="52" y="6" width="14" height="48" rx="3" fill="#f2a541"/><rect x="68" y="18" width="12" height="36" rx="3" fill="#6a9c78" transform="rotate(-12 74 36)"/>
  <path d="M130 54 q-14 -2 -12 -22 q2 -18 14 -22 q12 4 14 22 q2 20 -12 22 Z" fill="#c9ada7"/>
  <path d="M132 14 q-8 -10 -2 -14 M134 14 q6 -10 12 -8" stroke="#6a9c78" stroke-width="3" fill="none"/>
  <rect x="160" y="34" width="18" height="20" rx="3" fill="#2b2d42"/>
  <rect x="0" y="54" width="188" height="9" rx="2" fill="#8b5e3c"/><rect x="0" y="54" width="188" height="3" fill="#a8774f"/>
  <path d="M24 63 L24 74 L38 63 Z M150 63 L164 74 L164 63 Z" fill="#6b4429"/>`];
S.frame = [88, 84, `<rect x="6" y="4" width="76" height="76" rx="3" fill="#8b5e3c"/><rect x="14" y="12" width="60" height="60" fill="#f7efe6"/>
  <rect x="14" y="12" width="60" height="34" fill="#bfd7ea"/><circle cx="58" cy="26" r="7" fill="#f2a541"/>
  <path d="M14 56 L32 34 L46 50 L56 40 L74 58 L74 72 L14 72 Z" fill="#6a9c78"/>`];
S.rgb_bar = [188, 40, `<defs><linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#ff4d8d"/><stop offset=".5" stop-color="#7b5cff"/><stop offset="1" stop-color="#2ee6d6"/></linearGradient>
  <filter id="b" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="6"/></filter></defs>
  <rect x="8" y="14" width="172" height="12" rx="6" fill="url(#bar)" filter="url(#b)" opacity=".9"/>
  <rect x="8" y="16" width="172" height="8" rx="4" fill="url(#bar)"/>`];
S.wall_light = [88, 80, `<defs><radialGradient id="wg"><stop offset="0" stop-color="#ffe2a0" stop-opacity=".9"/><stop offset="1" stop-color="#ffe2a0" stop-opacity="0"/></radialGradient></defs>
  <circle cx="44" cy="44" r="40" fill="url(#wg)"/>
  <rect x="36" y="20" width="16" height="44" rx="4" fill="#8b5e3c"/>
  <path d="M26 22 L62 22 L56 4 L32 4 Z" fill="#f7efe6"/><circle cx="44" cy="26" r="6" fill="#fff6d6"/>`];
S.hanging_plant = [88, 92, `<path d="M44 0 L30 30 M44 0 L58 30" stroke="#8b5e3c" stroke-width="2"/>
  <path d="M26 30 L62 30 L56 52 L32 52 Z" fill="#f7efe6" stroke="#c9ada7"/>
  <path d="M32 50 q-8 20 -4 40 M40 52 q-2 16 2 30 M52 52 q6 18 2 34 M58 48 q12 14 10 30" stroke="#5a8a68" stroke-width="4" fill="none" stroke-linecap="round"/>
  ${[[28,70],[30,84],[42,76],[54,74],[56,88],[66,66],[66,78]].map(([x,y])=>`<ellipse cx="${x}" cy="${y}" rx="6" ry="4" fill="#7fb38b"/>`).join('')}
  <path d="M28 30 q8 -14 16 -2 q8 -14 16 2" fill="#6a9c78"/>`];

// ---- 바닥 (바닥선 = 높이) ----
S.rug = [288, 34, `<ellipse cx="144" cy="18" rx="140" ry="15" fill="#e7a08c"/><ellipse cx="144" cy="18" rx="118" ry="11" fill="none" stroke="#f7efe6" stroke-width="3" stroke-dasharray="10 6"/>
  <ellipse cx="144" cy="18" rx="80" ry="6" fill="#d9846e"/>`];
S.big_plant = [88, 150, `${shadow(44,148,30)}
  <path d="M44 100 C20 80 6 90 2 60 C26 64 38 78 44 100" fill="#5a8a68"/><path d="M44 100 C70 76 82 86 86 54 C62 60 50 76 44 100" fill="#6a9c78"/>
  <path d="M44 100 C30 60 40 30 30 4 C50 26 54 66 44 100" fill="#7fb38b"/><path d="M44 100 C56 60 70 46 66 20 C50 40 42 70 44 100" fill="#5a8a68"/>
  <path d="M22 100 L66 100 L60 148 L28 148 Z" fill="#e9e4f0" stroke="#c9ada7" stroke-width="2"/><rect x="20" y="98" width="48" height="8" rx="3" fill="#f7f4fa"/>`];
const chair = (seat, back, accent) => [188, 160, `${shadow(94,157,52)}
  ${[30,94,158].map(x=>`<circle cx="${x}" cy="152" r="6" fill="#2b2d42"/>`).join('')}
  <path d="M30 150 L94 132 L158 150" stroke="#3a3d55" stroke-width="7" fill="none"/>
  <rect x="88" y="104" width="12" height="30" fill="#4a4e69"/>
  <rect x="28" y="90" width="132" height="20" rx="9" fill="${seat}"/>
  <rect x="44" y="4" width="100" height="92" rx="16" fill="${back}"/>
  ${accent}`];
S.chair = chair('#8d99ae', '#a3adbf', `<rect x="58" y="16" width="72" height="6" rx="3" fill="#c3cad6"/>`);
S.gaming_chair = chair('#2b2d42', '#2b2d42', `<path d="M60 8 L80 8 L74 96 L66 96 Z M128 8 L108 8 L114 96 L122 96 Z" fill="#c8323c"/>
  <rect x="64" y="20" width="60" height="16" rx="8" fill="#c8323c"/><rect x="18" y="80" width="18" height="10" rx="4" fill="#c8323c"/><rect x="152" y="80" width="18" height="10" rx="4" fill="#c8323c"/>`);

// ---- PC 케이스 ----
const tower = (body, panel, inner) => [84, 196, `${shadow(42,194,40)}
  <rect x="2" y="2" width="80" height="190" rx="6" fill="${body}"/>
  <rect x="10" y="12" width="58" height="160" rx="4" fill="${panel}"/>${inner}
  <rect x="72" y="16" width="5" height="5" rx="2" fill="#6be675"/>`];
const fans = c => [40, 80, 120].map(y => `<circle cx="39" cy="${y}" r="16" fill="none" stroke="${c}" stroke-width="4"/><circle cx="39" cy="${y}" r="4" fill="${c}"/>`).join('');
S.case1 = tower('#2b2d42', '#3a3d55', fans('#5b6078'));
S.case2 = tower('#f2f3f7', '#dfe3ec', fans('#b9c0cf'));
S.case3 = tower('#1a1b29', '#262840', fans('#ff4d8d').replace(/#ff4d8d/g, 'url(#rgb)') + `<defs><linearGradient id="rgb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff4d8d"/><stop offset=".5" stop-color="#7b5cff"/><stop offset="1" stop-color="#2ee6d6"/></linearGradient></defs>`);
S.case_empty = [84, 196, `<rect x="2" y="2" width="80" height="190" rx="6" fill="none" stroke="#8d99ae" stroke-width="3" stroke-dasharray="8 6"/>`];

// ---- 부품 아이콘 ----
S.part_CPU = [64, 64, `<rect x="10" y="10" width="44" height="44" rx="4" fill="#4a4e69"/><rect x="20" y="20" width="24" height="24" rx="2" fill="#c9ccd6"/>
  ${[16,26,36,46].map(v=>`<rect x="${v}" y="2" width="3" height="8" fill="#f2a541"/><rect x="${v}" y="54" width="3" height="8" fill="#f2a541"/><rect x="2" y="${v}" width="8" height="3" fill="#f2a541"/><rect x="54" y="${v}" width="8" height="3" fill="#f2a541"/>`).join('')}`];
S.part_GPU = [64, 64, `<rect x="2" y="16" width="60" height="30" rx="4" fill="#2b2d42"/><circle cx="20" cy="31" r="10" fill="#4a4e69"/><circle cx="44" cy="31" r="10" fill="#4a4e69"/>
  <circle cx="20" cy="31" r="3" fill="#8d99ae"/><circle cx="44" cy="31" r="3" fill="#8d99ae"/><rect x="8" y="46" width="30" height="5" fill="#f2a541"/>`];
S.part_RAM = [64, 64, `<rect x="4" y="20" width="56" height="20" rx="2" fill="#6a9c78"/>${[10,22,34,46].map(x=>`<rect x="${x}" y="24" width="8" height="10" fill="#2b2d42"/>`).join('')}
  <rect x="6" y="40" width="52" height="4" fill="#f2a541"/>`];
S.part_PSU = [64, 64, `<rect x="6" y="12" width="52" height="40" rx="4" fill="#3a3d55"/><circle cx="28" cy="32" r="13" fill="none" stroke="#8d99ae" stroke-width="3"/>
  <path d="M46 22 L50 30 L45 30 L49 40" stroke="#f2a541" stroke-width="3" fill="none"/>`];
S.part_CASE = [64, 64, `<rect x="16" y="4" width="32" height="56" rx="4" fill="#4a4e69"/><rect x="20" y="10" width="20" height="44" rx="2" fill="#5b6078"/><circle cx="30" cy="22" r="6" fill="none" stroke="#2ee6d6" stroke-width="2"/>`];

// ---- 사이버 도시 (창밖 · 타이틀) ----
function city(w, h, seed, scale = 1) {
  let r = seed; const rnd = () => (r = (r * 16807) % 2147483647) / 2147483647;
  const neon = ['#ff4d8d', '#2ee6d6', '#7b5cff', '#ffd65c'];
  let out = '', x = -10;
  for (const layer of [{c: '#3a2470', hMin: .35, hMax: .7, win: .25}, {c: '#241446', hMin: .2, hMax: .55, win: .5}]) {
    x = -10;
    while (x < w) {
      const bw = (30 + rnd() * 60) * scale, bh = h * (layer.hMin + rnd() * (layer.hMax - layer.hMin));
      out += `<rect x="${x}" y="${h - bh}" width="${bw}" height="${bh}" fill="${layer.c}"/>`;
      for (let wy = h - bh + 8 * scale; wy < h - 6; wy += 10 * scale)
        for (let wx = x + 5 * scale; wx < x + bw - 6 * scale; wx += 9 * scale)
          if (rnd() < layer.win) out += `<rect x="${wx}" y="${wy}" width="${4 * scale}" height="${4 * scale}" fill="${rnd() < .7 ? '#ffd65c' : '#2ee6d6'}" opacity=".85"/>`;
      if (rnd() < .45) {
        const c = neon[Math.floor(rnd() * 4)], sy = h - bh + 12 * scale;
        out += `<rect x="${x + bw * .2}" y="${sy}" width="${bw * .6}" height="${12 * scale}" fill="none" stroke="${c}" stroke-width="${3 * scale}"/>`;
      }
      if (rnd() < .3) out += `<rect x="${x + bw / 2 - scale}" y="${h - bh - 20 * scale}" width="${2 * scale}" height="${20 * scale}" fill="${layer.c}"/><rect x="${x + bw / 2 - 2 * scale}" y="${h - bh - 22 * scale}" width="${4 * scale}" height="${4 * scale}" fill="#ff4d8d"/>`;
      x += bw + rnd() * 6 * scale;
    }
  }
  return out;
}
const sky = (id) => `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b0f3d"/><stop offset=".6" stop-color="#5a2a7a"/><stop offset="1" stop-color="#c4467e"/></linearGradient>`;
const stars = (w, h, n, seed) => { let r = seed, o = ''; const rnd = () => (r = (r * 48271) % 2147483647) / 2147483647;
  for (let i = 0; i < n; i++) o += `<rect x="${rnd() * w}" y="${rnd() * h}" width="3" height="3" fill="#fff" opacity="${.4 + rnd() * .6}"/>`; return o; };

// ---- 방 배경 (x 270~1280, y 0~650 영역 = 1010 x 650) ----
const W = 1010, H = 650, floorH = 190;
S.room_bg = [W, H, `<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22123f"/><stop offset="1" stop-color="#341c5c"/></linearGradient>
  ${sky('sky')}</defs>
  <rect width="${W}" height="${H}" fill="url(#wall)"/>
  ${[...Array(14)].map((_, i) => `<rect x="${i * 76}" y="0" width="2" height="${H - floorH}" fill="#4a2c7c" opacity=".6"/>`).join('')}
  <rect x="0" y="0" width="${W}" height="6" fill="#2ee6d6"/><rect x="0" y="6" width="${W}" height="6" fill="#2ee6d6" opacity=".25"/>
  <g transform="translate(868 40)"><rect x="-10" y="-10" width="142" height="330" fill="#120a26"/>
    <rect width="122" height="310" fill="url(#sky)"/>${stars(122, 150, 14, 7)}
    <circle cx="88" cy="46" r="13" fill="#ffe9a8"/>
    <g transform="translate(0 130)">${city(122, 180, 11, .8)}</g>
    <rect x="59" y="0" width="4" height="310" fill="#120a26"/><rect x="0" y="150" width="122" height="4" fill="#120a26"/>
    <rect x="-10" y="-10" width="142" height="330" fill="none" stroke="#ff4d8d" stroke-width="3"/></g>
  <rect y="${H - floorH - 8}" width="${W}" height="8" fill="#120a26"/><rect y="${H - floorH - 4}" width="${W}" height="3" fill="#ff4d8d"/>
  <rect y="${H - floorH}" width="${W}" height="${floorH}" fill="#170d2e"/>
  ${[...Array(6)].map((_, i) => `<rect y="${H - floorH + 10 + i * 32}" width="${W}" height="2" fill="#2ee6d6" opacity="${.15 + i * .05}"/>`).join('')}
  ${[...Array(13)].map((_, i) => `<rect x="${i * 84}" y="${H - floorH}" width="2" height="${floorH}" fill="#2ee6d6" opacity=".18"/>`).join('')}`];

// 책상 (상판 + 다리 + 서랍) 820 x 272
S.desk = [820, 272, `<rect x="0" y="0" width="820" height="22" fill="#2a2350"/><rect x="0" y="0" width="820" height="4" fill="#2ee6d6"/>
  <rect x="14" y="22" width="22" height="250" fill="#1d1838"/><rect x="784" y="22" width="22" height="250" fill="#1d1838"/>
  <rect x="600" y="22" width="184" height="70" fill="#231c44"/><rect x="606" y="28" width="172" height="58" fill="#2c2454"/>
  <rect x="672" y="52" width="40" height="6" fill="#ff4d8d"/>
  <rect x="36" y="22" width="564" height="10" fill="#1d1838"/><rect x="36" y="30" width="564" height="2" fill="#7b5cff"/>`];

// 타이틀 배경 1280 x 720
S.title_bg = [1280, 720, `<defs>${sky('tsky')}</defs><rect width="1280" height="720" fill="url(#tsky)"/>${stars(1280, 360, 80, 3)}
  <circle cx="1040" cy="150" r="46" fill="#ffe9a8"/>
  <g transform="translate(0 300)">${city(1280, 420, 5, 1.6)}</g>
  <rect y="660" width="1280" height="60" fill="#120a26"/><rect y="660" width="1280" height="4" fill="#2ee6d6"/>
  <rect x="100" y="150" width="700" height="250" fill="#120a26" opacity=".55"/>`];

(async () => {
  for (const [name, [w, h, body]] of Object.entries(S)) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${body}</svg>`;
    const f = w > 500 ? 4 : 3;  // 도트 느낌: 작게 줄였다가 nearest로 다시 키움
    const small = await sharp(Buffer.from(svg)).resize(Math.ceil(w / f), Math.ceil(h / f), { kernel: 'nearest' }).png().toBuffer();
    await sharp(small).resize(w, h, { kernel: 'nearest' }).png().toFile(path.join(OUT, name + '.png'));
  }
  console.log(Object.keys(S).length, 'sprites');
})();
