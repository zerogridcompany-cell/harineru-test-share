// 店を本番に出す前の最終ゲート（ダメなことリスト G）を、どのブランドでも1回で数字にする。2026-10-02 版。
// 正本: ../references/dame-list.md（pdp-tsukuru の中の写し） の G
//
// 使い方: node 出す前の検査.mjs <ブランド名> <URL> [<URL> ...]
//   例:   node 出す前の検査.mjs アルコット https://arukoto.shop/ https://arukoto.shop/pages/ar-insole
//   URL ごとに 390px と 1280px の2通りで開く。
//
// 機械で数える物（どれか1つでも0でなければ終了コード1）:
//   覆われて押せないボタン・リンク / JSエラー / 4xx・5xx のリンク / 外の店へのリンク / blur の残り（画面の1割より大きい物。飾りの細い線は数えない） /
//   読み込み直後の scrollY / <title> にブランド名が無い / 1画面目の動画が再生されていない
// 機械で見ない物（毎回「目で見る」に出す）: カルーセルの往復・全プランをカートに入れた個数と金額・打ち消し価格
// 評価の件数が面ごとに同じかは `面の数字.py` で見る。
const { 引く, EXE } = await import(new URL('./lib.mjs', import.meta.url));

const [ブランド, ...URLたち] = process.argv.slice(2);
if (!ブランド || !URLたち.length) { console.error('使い方: node 出す前の検査.mjs <ブランド名> <URL> [<URL> ...]'); process.exit(2); }
const 外でよい = /(^|\.)(shopify\.com|shopifycdn\.com|shop\.app|instagram\.com|facebook\.com|line\.me|x\.com|twitter\.com|youtube\.com|google\.com|apple\.com|paypal\.com)$/;

const chromium = 引く();
const browser = await chromium.launch({ executablePath: EXE, headless: true });
const 結果 = [];
const リンクの状態 = new Map();

async function 状態を見る(href) {
  if (リンクの状態.has(href)) return リンクの状態.get(href);
  let 状態 = 0;
  for (let i = 0; i < 2 && !状態; i++) {
    try {
      const r = await fetch(href, { method: 'GET', redirect: 'follow', signal: AbortSignal.timeout(15000), headers: { 'User-Agent': 'Mozilla/5.0' } });
      状態 = r.status;
    } catch (e) { 状態 = 0; }
  }
  リンクの状態.set(href, 状態);
  return 状態;
}

for (const url of URLたち) {
  const 本家 = new URL(url).host;
  for (const W of [390, 1280]) {
    const isSP = W < 900;
    const ctx = await browser.newContext({ viewport: { width: W, height: 844 }, locale: 'ja-JP', isMobile: isSP, hasTouch: isSP });
    const page = await ctx.newPage();
    const JSエラー = [];
    page.on('pageerror', (e) => JSエラー.push(e.message.slice(0, 120)));
    try { await page.goto(url, { waitUntil: 'load', timeout: 60000 }); }
    catch (e) { 結果.push({ url, W, 取れない: e.message.slice(0, 120) }); await ctx.close(); continue; }
    await page.waitForTimeout(3000);
    const 直後 = await page.evaluate(() => window.scrollY);
    const r = await page.evaluate(({ 本家 }) => {
      const 見える = (el) => { const b = el.getBoundingClientRect(); const s = getComputedStyle(el); return b.width > 4 && b.height > 4 && s.visibility !== 'hidden' && s.display !== 'none' && Number(s.opacity) > 0.05; };
      // 覆われて押せない: 1画面目に見えているボタン・リンクの真ん中に、別の要素が乗っている
      const 覆われ = [];
      document.querySelectorAll('a[href], button, [role=button], input[type=submit]').forEach((el) => {
        if (!見える(el)) return;
        const b = el.getBoundingClientRect();
        if (b.top < 0 || b.bottom > innerHeight || b.left < 0 || b.right > innerWidth) return;
        const cx = b.left + b.width / 2, cy = b.top + b.height / 2;
        // 飛ばしリンク（キーボード用）と、はみ出しを隠す箱の外にある物（客にも見えない）は数えない
        if (/skip/i.test(el.className + '') || /^#Main/i.test(el.getAttribute('href') || '')) return;
        for (let p = el.parentElement; p; p = p.parentElement) {
          if (/(hidden|clip|auto|scroll)/.test(getComputedStyle(p).overflow)) { const q = p.getBoundingClientRect(); if (cx < q.left || cx > q.right || cy < q.top || cy > q.bottom) return; }
        }
        const 上 = document.elementFromPoint(cx, cy);
        if (上 && 上 !== el && !el.contains(上) && !上.contains(el)) 覆われ.push(((el.innerText || el.getAttribute('aria-label') || el.tagName) + '').trim().slice(0, 30) + ' ← ' + (上.className || 上.tagName).toString().slice(0, 40));
      });
      const blur = Array.from(document.querySelectorAll('body *')).filter((el) => { const s = getComputedStyle(el); const b = el.getBoundingClientRect(); return /blur/.test(s.filter + s.backdropFilter) && 見える(el) && b.width * b.height > innerWidth * innerHeight * 0.1; }).map((el) => (el.className || el.tagName).toString().slice(0, 40));
      // 同じページの中へ飛ぶ印（#reviews など）は、ページが開けている時点で壊れていないので数えない（2026-10-18。プレビューURLは cookie 無しの fetch で404になり、誤って落ちていた）
      const 今 = location.href.split('#')[0];
      const リンク = Array.from(document.querySelectorAll('a[href]')).map((a) => a.href).filter((h) => /^https?:/.test(h) && !(h.includes('#') && h.split('#')[0] === 今));
      const 動画 = Array.from(document.querySelectorAll('video')).filter((v) => { const b = v.getBoundingClientRect(); return b.top < innerHeight && b.bottom > 0 && 見える(v); }).map((v) => ({ 再生中: !v.paused && v.readyState >= 2, src: (v.currentSrc || '').slice(-40) }));
      return { 覆われ, blur, リンク: [...new Set(リンク)], 動画, title: document.title };
    }, { 本家 });
    const 外 = r.リンク.filter((h) => { const host = new URL(h).host; return host !== 本家 && !外でよい.test(host); });
    const 壊れ = [];
    for (const h of r.リンク.filter((h) => new URL(h).host === 本家)) {
      const s = await 状態を見る(h.split('#')[0]);
      if (s === 0 || s >= 400) 壊れ.push(`${s || '応答なし'} ${h}`);
    }
    結果.push({
      url, W,
      覆われて押せない: r.覆われ, JSエラー, 壊れたリンク: 壊れ, 外の店へのリンク: 外, blurの残り: r.blur,
      直後のscrollY: 直後, titleにブランド名が無い: r.title.includes(ブランド) ? [] : [r.title],
      止まっている動画: r.動画.filter((v) => !v.再生中).map((v) => v.src),
    });
    await ctx.close();
  }
}
await browser.close();

const 欄 = ['覆われて押せない', 'JSエラー', '壊れたリンク', '外の店へのリンク', 'blurの残り', 'titleにブランド名が無い', '止まっている動画'];
let 落ちた = 0;
for (const x of 結果) {
  if (x.取れない) { console.log(`取れない ${x.W}px ${x.url}: ${x.取れない}`); 落ちた++; continue; }
  const 数 = 欄.map((k) => `${k} ${x[k].length}`).concat(`直後のscrollY ${x.直後のscrollY}`);
  const 悪い = 欄.filter((k) => x[k].length).length + (x.直後のscrollY ? 1 : 0);
  落ちた += 悪い;
  console.log(`${悪い ? '落ちた' : '通った'} ${x.W}px ${x.url}\n  ${数.join(' / ')}`);
  欄.filter((k) => x[k].length).forEach((k) => x[k].slice(0, 5).forEach((v) => console.log(`    ${k}: ${v}`)));
}
console.log('\n目で見る（機械で見ていない）: カルーセルを矢印・サムネイル・ドットで全枚数往復できるか / 全プランをカートに入れて個数と金額が表示どおりか / 打ち消し価格が全段そろっているか');
process.exit(落ちた ? 1 : 0);
