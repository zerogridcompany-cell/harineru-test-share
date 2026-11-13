// probe.mjs と lint.mjs が共通で使う土台。
// 帯の見つけ方・色の判定・可視判定は「1か所に書いて両方から引く」。
// 別々に書くと片方だけ古くなる（実測: lint と probe で帯の定義が食い違っていた 2026-08-29）。
import fs from 'node:fs';
import { createRequire } from 'node:module';

// 別のビルド番号・別のOSでは環境変数 HONE_CHROMIUM で差し替える。
// 既定は macOS arm64 / chromium-1223（2026-08-29 時点でこのマシンに入っている物）
// 2026-10-19 pdp-tsukuru に写した時: どちらも無ければ undefined にし、playwright が入れた Chromium をそのまま使う
const 既定 = `${process.env.HOME}/Library/Caches/ms-playwright/chromium-1223/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;
export const EXE = process.env.HONE_CHROMIUM || (fs.existsSync(既定) ? 既定 : undefined);

export function 引く() {
  const ROOTS = [`${process.env.HOME}/.agents/skills/surasura/scripts/package.json`,   // 2026-10-19 Seiyo の新ハーネス（surasura の playwright-core）
                 `${process.env.HOME}/Claude Code/package.json`, `${process.env.HOME}/package.json`, `${process.cwd()}/package.json`, import.meta.url];
  for (const r of ROOTS) {
    try { return createRequire(r)('playwright-core').chromium; } catch (e) { /* 次を試す */ }
  }
  console.error('環境が壊れている: playwright-core が見つからない。`cd ~/Claude\\ Code && npm i playwright-core`');
  process.exit(4);
}

// 終了コード: 0 合格 / 1 不合格 / 2 引数が足りない / 3 ページが取れない / 4 実行環境が壊れている
export async function 開く(url, { W = 390, timeout = 90000 } = {}) {
  const chromium = 引く();
  if (EXE && !fs.existsSync(EXE)) {
    console.error(`環境が壊れている: Chromium が ${EXE} に無い。\`npx playwright install chromium\` で入れるか、環境変数 HONE_CHROMIUM で場所を渡す`);
    process.exit(4);
  }
  let browser;
  try { browser = await chromium.launch({ executablePath: EXE, headless: true }); }
  catch (e) { console.error('環境が壊れている: Chromium を起動できない / ' + e.message); process.exit(4); }
  const isSP = W < 900;
  const ctx = await browser.newContext({
    viewport: { width: W, height: 844 }, deviceScaleFactor: 2, locale: 'ja-JP',
    isMobile: isSP, hasTouch: isSP,
    userAgent: isSP ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined,
  });
  const page = await ctx.newPage();
  try { await page.goto(url, { waitUntil: 'domcontentloaded', timeout }); }
  catch (e) { console.error('ページが取れない（0件ではない）: ' + e.message); await browser.close(); process.exit(3); }
  await page.waitForTimeout(3000);
  const 閉じた = await ポップアップを閉じる(page);
  if (閉じた.length) console.error('ポップアップを閉じた: ' + JSON.stringify(閉じた));
  // 遅延読み込みを全部起こす
  await page.evaluate(async () => {
    await new Promise((res) => { let y = 0; const t = setInterval(() => { window.scrollTo(0, y); y += 700; if (y > document.body.scrollHeight) { clearInterval(t); window.scrollTo(0, 0); res(); } }, 70); });
  });
  await page.waitForTimeout(2200);
  // 画像の読み込みを待つ。lazy のままだと naturalWidth が 0 で「原寸が取れない」になる（実測 2026-08-29）
  try {
    await page.evaluate(() => { document.querySelectorAll('img').forEach((im) => { im.loading = 'eager'; const d = im.getAttribute('data-src'); if (d && !im.src) im.src = d; }); });
    await page.waitForTimeout(600);
    await page.evaluate(() => Promise.all(Array.from(document.images).map((im) => im.complete ? null : new Promise((res) => { im.addEventListener('load', res, { once: true }); im.addEventListener('error', res, { once: true }); setTimeout(res, 4000); }))));
  } catch (e) { console.error('画像の読み込み待ちで例外（続行する）: ' + e.message); }
  await page.addScriptTag({ content: BROWSER });
  const ある = await page.evaluate(() => !!window.__hone);
  if (!ある) { console.error('環境が壊れている: 共通関数をページに入れられなかった（CSPの可能性）'); await browser.close(); process.exit(4); }
  return { browser, ctx, page };
}

async function ポップアップを閉じる(page) {
  const 閉じた = [];
  for (let i = 0; i < 4; i++) {
    const done = await page.evaluate(() => {
      const みえる = (el) => { const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return false; const r = el.getBoundingClientRect(); return r.width > 40 && r.height > 40; };
      const cover = Array.from(document.querySelectorAll('div,section,aside,dialog')).find((el) => {
        const s = getComputedStyle(el); if (!['fixed', 'absolute'].includes(s.position)) return false;
        const r = el.getBoundingClientRect();
        return みえる(el) && r.width >= innerWidth * 0.8 && r.height >= innerHeight * 0.6 && Number(s.zIndex || 0) >= 1;
      });
      if (!cover) return null;
      const btn = cover.querySelector('[aria-label*="close" i],[aria-label*="閉じ"],button.close,.close,[class*="close"],[data-close]')
        || Array.from(cover.querySelectorAll('button,a,span')).find((b) => /^(×|✕|✖|x|close|閉じる)$/i.test((b.textContent || '').trim()));
      const 名 = (cover.className || cover.tagName).toString().slice(0, 50);
      if (btn) { btn.click(); return 名; }
      cover.remove(); return 名 + '（閉じるボタンが無いので取り除いた）';
    });
    if (!done) break;
    閉じた.push(done);
    await page.waitForTimeout(450);
  }
  return 閉じた;
}

// ページの中で動く共通関数。window.__hone に載せる。
export const BROWSER = `
window.__hone = (() => {
  // shadow root の中まで潜る。潜らないと、web componentで組まれた帯が丸ごと消え、
  // 「その帯が無かった」のか「見えていない」のか区別できない（レビュー指摘 2026-08-29）
  const 全部 = (sel, root = document) => {
    const out = [];
    const walk = (r) => {
      out.push(...r.querySelectorAll(sel));
      r.querySelectorAll('*').forEach((e) => { if (e.shadowRoot) walk(e.shadowRoot); });
    };
    walk(root);
    return out;
  };
  const shadowの数 = () => Array.from(document.querySelectorAll('*')).filter((e) => e.shadowRoot).length;
  const みえる = (el) => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) return false;
    const r = el.getBoundingClientRect(); if (r.width <= 0 || r.height <= 0) return false;
    let n = el.parentElement;
    while (n && n !== document.documentElement) { const ps = getComputedStyle(n); if ((ps.overflow === 'hidden' || ps.overflowY === 'hidden') && n.clientHeight === 0) return false; n = n.parentElement; }
    return true;
  };
  const 不透明 = (c) => { const m = (c || '').match(/[\\d.]+/g); return !!(m && (m[3] === undefined || Number(m[3]) > 0.05)); };
  const 地色か = (c) => { const m = (c || '').match(/[\\d.]+/g); return !!(m && (m[3] === undefined || Number(m[3]) >= 0.85)); };
  const 明度 = (c) => { const m = (c || '').match(/[\\d.]+/g); if (!m) return 1; return (0.2126 * +m[0] + 0.7152 * +m[1] + 0.0722 * +m[2]) / 255; };
  const 相対輝度 = (c) => { const m = (c || '').match(/[\\d.]+/g); if (!m) return 1; const f = (v) => { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(+m[0]) + 0.7152 * f(+m[1]) + 0.0722 * f(+m[2]); };
  const 地 = (el) => { let n = el; while (n && n !== document.documentElement) { const c = getComputedStyle(n).backgroundColor; if (地色か(c)) return c; n = n.parentElement; } return 'rgb(255,255,255)'; };
  // 帯の色: 自分が透明なら、帯を塗っている「中の一番大きい子」を探す
  const 帯の色 = (el) => {
    const own = getComputedStyle(el).backgroundColor;
    if (不透明(own)) return own;
    const r = el.getBoundingClientRect();
    const 塗り手 = Array.from(el.querySelectorAll('*')).find((c) => { const cr = c.getBoundingClientRect(); return cr.width >= r.width * 0.9 && cr.height >= r.height * 0.6 && 不透明(getComputedStyle(c).backgroundColor); });
    if (塗り手) return getComputedStyle(塗り手).backgroundColor;
    return 地(el);
  };
  // 白は「無彩色かつ明るい」。色がついていれば薄。#fdf1f4 を白と呼ばないため
  const 濃薄白 = (c) => { const m = ((c || '').match(/[\\d.]+/g) || [255,255,255]).map(Number); const 彩り = Math.max(m[0],m[1],m[2]) - Math.min(m[0],m[1],m[2]); const l = 明度(c); return (l > 0.93 && 彩り < 6) ? '白' : l > 0.72 ? '薄' : '濃'; };
  // 帯: 画面幅の90%以上・高さ60px以上のうち一番外側。1.6画面より高いものは1段降りて割り直す（最大3段）
  const 帯たち = (VW, opt) => {
    const 割らない = opt && opt.割らない;
    const 帯か = (el) => { if (!みえる(el)) return false; const r = el.getBoundingClientRect(); return r.width >= VW * 0.9 && r.height >= 60; };
    const 子帯 = (el) => { const kids = Array.from(el.children).filter(帯か); if (kids.length >= 2) return kids; if (kids.length === 1) return 子帯(kids[0]); return []; };
    const 割る = (el, d) => { const r = el.getBoundingClientRect(); if (d >= 3 || r.height <= 844 * 1.6) return [el]; const kids = 子帯(el); if (kids.length < 2) return [el]; return kids.flatMap((k) => 割る(k, d + 1)); };
    let tops = 全部('section,[id*="shopify-section"],main>div,body>div,footer,header').filter(帯か);
    tops = tops.filter((el) => !tops.some((o) => o !== el && o.contains(el)));
    let bands = 割らない ? tops : tops.flatMap((el) => 割る(el, 0));
    bands = bands.filter((el) => !bands.some((o) => o !== el && o.contains(el)));
    bands.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
    return bands;
  };
  return { 全部, shadowの数, みえる, 不透明, 地色か, 明度, 相対輝度, 地, 帯の色, 濃薄白, 帯たち };
})();
`;
