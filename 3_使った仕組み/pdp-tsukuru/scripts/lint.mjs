#!/usr/bin/env node
// 出来上がったページを機械で検収する。目で見て「大丈夫そう」をやめる。
// 使い方: node lint.mjs <URL|file> [--skin skin.json] [--w 390]
// 皮（skin.json）は任意。無ければ禁止色・表記ゆれ・図の欄を見ずに、横あふれ・文字の大きさ・CTAの濃さ・帯の並びだけを見る
// 終了コード: 0 合格 / 1 不合格 / 2 引数が足りない / 3 ページが取れない / 4 実行環境が壊れている
import fs from 'node:fs';
import path from 'node:path';
import { 開く } from './lib.mjs';

const args = process.argv.slice(2);
const target = args[0];
const getArg = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
if (!target || target.startsWith('--')) { console.error('usage: lint.mjs <URL|file> [--skin skin.json] [--w 390]'); process.exit(2); }
const W = Number(getArg('--w', 390));
const skinPath = getArg('--skin', '');
let skin = {};
if (skinPath) {
  if (!fs.existsSync(skinPath)) { console.error(`皮が読めない（合格でも不合格でもない）: ${skinPath}`); process.exit(3); }
  try { skin = JSON.parse(fs.readFileSync(skinPath, 'utf8')); }
  catch (e) { console.error(`皮が壊れている（合格でも不合格でもない）: ${e.message}`); process.exit(3); }
}

const cfg = {
  禁止色: (skin.禁止色 || []).map((c) => c.toLowerCase()),
  表記ゆれ: skin.表記ゆれ || [],
  最小文字px: skin.最小文字px ?? 9,
  注意文字px: skin.注意文字px ?? 12,
  最小タップpx: skin.最小タップpx ?? 40,
  文字の除外: skin.文字の除外セレクタ || [],
  図: (skin.図 || []).map((f) => ({ 名: String(f.名 || '').toLowerCase(), 最小文字px: f.最小文字px || 0 })),
  VW: W,
};

const url = /^https?:\/\//.test(target) ? target : 'file://' + path.resolve(target);
const { browser, page } = await 開く(url, { W });

const r = await page.evaluate((cfg) => {
  const H = window.__hone;
  const { 禁止色, 表記ゆれ, 最小文字px, 注意文字px, 最小タップpx, 文字の除外, 図, VW } = cfg;
  const hex = (c) => { const m = (c || '').match(/\d+/g); if (!m) return ''; return '#' + m.slice(0, 3).map((n) => Number(n).toString(16).padStart(2, '0')).join(''); };

  // ── 文字を集める。innerText を使わない。
  //    innerText は閉じた <details> の中身を返さないので、アコーディオンの中の表記ゆれを拾えない（レビュー実測 2026-08-29）
  const 見えている文字 = [];
  H.全部('*').forEach((el) => {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(el.tagName)) return;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return;   // 折りたたみは「出る文字」として数える
    Array.from(el.childNodes).forEach((n) => { if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' ').trim(); if (t) 見えている文字.push(t); } });
  });
  const 全文 = 見えている文字.join('\n');
  const ゆれ = 表記ゆれ.map((grp) => ({ 組: grp, 出た語: grp.filter((w) => 全文.includes(w)) })).filter((x) => x.出た語.length > 1);

  // ── 禁止色。その要素で色が「変わった」ときだけ見る（継承した既定の黒を拾わないため）
  const 色違反 = []; const 見た = new Set();
  H.全部('*').filter(H.みえる).forEach((el) => {
    if (['HTML', 'BODY'].includes(el.tagName)) return;
    const s = getComputedStyle(el);
    const 親 = el.parentElement ? getComputedStyle(el.parentElement) : null;
    const 自前の文字 = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim());
    const 色を変えた = !親 || s.color !== 親.color;
    const 枠あり = parseFloat(s.borderTopWidth) > 0;
    [['文字', (自前の文字 && 色を変えた) ? s.color : null], ['背景', s.backgroundColor], ['枠', 枠あり ? s.borderTopColor : null]].forEach(([k, c]) => {
      if (!c || !H.不透明(c)) return;
      const h = hex(c).toLowerCase();
      if (禁止色.includes(h) && !見た.has(k + h)) { 見た.add(k + h); 色違反.push({ 場所: k, 色: h, 例: (el.className || el.tagName).toString().slice(0, 50) }); }
    });
  });

  // ── 文字サイズ
  const 小さい文字 = [];
  H.全部('*').filter(H.みえる).forEach((el) => {
    if (!Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim())) return;
    if ((文字の除外 || []).some((sel) => { try { return el.closest(sel); } catch (e) { return false; } })) return;
    const px = parseFloat(getComputedStyle(el).fontSize);
    if (px < 注意文字px) 小さい文字.push({ px: Math.round(px * 10) / 10, 不合格: px > 0 && px < 最小文字px, 注: px === 0 ? '0px。疑似要素で置き換えている可能性' : '', 文: el.textContent.replace(/\s+/g, ' ').trim().slice(0, 40) });
  });

  // ── 図（文字を焼き込んだ画像）。img と背景画像の両方。名前は大小文字を無視する
  const 図を見る = (src, 幅, 出し方) => {
    const s = (src || '').toLowerCase();
    const reg = 図.find((f) => f.名 && s.includes(f.名));
    return reg ? { reg, 出し方 } : null;
  };
  const 読めない図 = []; const 判定できない図 = [];
  H.全部('img').filter(H.みえる).forEach((im) => {
    const r = im.getBoundingClientRect();
    const src = (im.currentSrc || im.src || im.getAttribute('data-src') || '').split('/').pop();
    const hit = 図を見る(src, r.width, 'img'); if (!hit || r.width < 120) return;
    const nw = im.naturalWidth || 0;
    if (!nw) { 判定できない図.push({ src, 理由: '原寸が取れない（遅延読込のまま）' }); return; }
    const 率 = r.width / nw;
    const 実効px = hit.reg.最小文字px ? Math.round(hit.reg.最小文字px * 率 * 10) / 10 : null;
    const x = { src, 出し方: 'img', 原寸: nw, 表示: Math.round(r.width), 率: Math.round(率 * 1000) / 1000, 焼いた最小文字px: hit.reg.最小文字px || null, 実効px, 不合格: 実効px !== null && 実効px < 10 };
    if (実効px === null ? x.率 < 0.25 : 実効px < 12) 読めない図.push(x);
  });
  H.全部('*').filter(H.みえる).forEach((el) => {
    const bi = getComputedStyle(el).backgroundImage;
    if (!bi || bi === 'none' || !bi.includes('url(')) return;
    const src = (bi.match(/url\(["']?([^"')]+)/) || [])[1] || ''; const name = src.split('/').pop();
    const r = el.getBoundingClientRect();
    const hit = 図を見る(name, r.width, 'bg'); if (!hit || r.width < 120) return;
    判定できない図.push({ src: name, 出し方: 'background-image', 理由: '背景画像は原寸が取れない。img で出すか、実効pxを手で確かめる' });
  });

  // ── タップ領域（高さと幅の両方）
  const 小さいタップ = H.全部('a,button,summary,[role="tab"]').filter(H.みえる).map((el) => { const r = el.getBoundingClientRect(); return { h: Math.round(r.height), w: Math.round(r.width), 文: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 30) }; }).filter((x) => (x.h > 0 && x.h < 最小タップpx) || (x.w > 0 && x.w < 24));

  // ── コントラスト。CTA（a/button）と短い文字も見る
  const 低コントラスト = [];
  H.全部('p,li,span,b,strong,em,small,td,th,a,button,h1,h2,h3,h4').filter(H.みえる).forEach((el) => {
    if (!Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim())) return;
    const s = getComputedStyle(el);
    const L1 = H.相対輝度(s.color), L2 = H.相対輝度(H.地(el));
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const 本文 = el.textContent.replace(/\s+/g, ' ').trim();
    const CTA = ['A', 'BUTTON'].includes(el.tagName);
    if ((CTA || 本文.length >= 4) && ratio < 4.5) 低コントラスト.push({ 比: Math.round(ratio * 10) / 10, 文字: s.color, CTA, 文: 本文.slice(0, 34) });
  });

  // ── 帯の並び。色のリズムは「設計上の帯」で見るので、1.6画面での割り直しはしない
  // ヘッダーとフッター、0.15画面に満たない細い帯はリズムの対象外（内容の帯ではない）
  const 帯要素 = H.帯たち(VW, { 割らない: true }).filter((el) => {
    if (['HEADER', 'FOOTER'].includes(el.tagName)) return false;
    if (el.closest('header,footer')) return false;
    return el.getBoundingClientRect().height >= 844 * 0.15;
  });
  const 帯 = 帯要素.map((el) => H.濃薄白(H.帯の色(el)));
  const 帯の連続 = 帯.map((b, i) => (i > 0 && b === 帯[i - 1] ? { i, 色: b } : null)).filter(Boolean);

  // 折り返さない文字（white-space:nowrap）が画面の右を越える所。外の枠が overflow:hidden だとページ全体の横あふれには出ないので、文字の箱で数える
  const 切れる文字 = [...document.querySelectorAll('body *')].filter((el) => {
    if (!el.textContent.trim() || el.children.length > 3) return false;
    const st = getComputedStyle(el); if (st.whiteSpace !== 'nowrap' || st.display === 'none' || st.visibility === 'hidden') return false;
    if (el.closest('[hidden],[aria-hidden="true"],.track,.ticker,marquee,[class*="marq"],[class*="tick"]')) return false;
    const r = el.getBoundingClientRect(); return r.width > 0 && r.right > VW + 1 && r.left < VW;
  }).slice(0, 10).map((el) => ({ 字: el.textContent.trim().slice(0, 30), 右: Math.round(el.getBoundingClientRect().right) }));
  return {
    横あふれ: document.documentElement.scrollWidth > VW + 1 ? { 幅: document.documentElement.scrollWidth, 画面: VW } : null,
    切れる文字,
    色違反, 表記ゆれ: ゆれ, 小さい文字: 小さい文字.slice(0, 15), 読めない図, 判定できない図,
    小さいタップ: 小さいタップ.slice(0, 12), 低コントラスト: 低コントラスト.slice(0, 12),
    帯の並び: 帯.join(' '), 帯の連続, 全高: document.body.scrollHeight, shadowを持つ要素: H.shadowの数(),
  };
}, cfg);

await browser.close();

const 落ちた = [];
if (r.横あふれ) 落ちた.push('横あふれ');
if (r.切れる文字.length) 落ちた.push('折り返さない文字が画面の右で切れる');
if (r.色違反.length) 落ちた.push('禁止色');
if (r.表記ゆれ.length) 落ちた.push('表記ゆれ');
if (r.読めない図.some((x) => x.不合格)) 落ちた.push('図が読めない');
if (r.小さい文字.some((x) => x.不合格)) 落ちた.push('文字が小さい');
if (r.帯の連続.length) 落ちた.push('帯の色が続いている');
// CTA は 3.0 未満で不合格（大きい太字の下限）。3.0〜4.5 は注意にとどめる
if (r.低コントラスト.some((x) => x.CTA && x.比 < 3.0)) 落ちた.push('CTAが読めない');

const 見ていないもの = ['hover / focus のときの色', '画像に焼き込まれた文字の中身', 'クリックやスクロールで初めて出る要素の中身'];
if (r.判定できない図.length) 見ていないもの.push('背景画像・遅延読込の図の実効文字px（判定できない図に出した）');

console.log(JSON.stringify({ 判定: 落ちた.length ? '不合格' : '合格', 落ちた, 幅: W, ...r, 見ていないもの }, null, 1));
process.exit(落ちた.length ? 1 : 0);
