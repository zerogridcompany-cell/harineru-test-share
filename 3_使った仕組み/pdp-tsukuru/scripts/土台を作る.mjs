// 店の作業場の元（空の型）を写す。
//   node 土台を作る.mjs <出力フォルダ>
// 出力: <出力フォルダ>/index.html と img/（中身は全部〔札〕と札の絵。埋めるまで検査 F12 で落ちる）
// 2026-10-19 本人: 元はここちドライの丸写しをやめ、空の型にした。空の型は、本人が「いいね」と言った
// 元は bath-step-over の店（v2 `~/Desktop/ec/bath-step-over/09 店/01 bath-step-over_店_オファーがすぐ見える店_v2/`）から
// 中身だけを抜いた物（../kata/）。段の並びはここちドライ、作りはワンドライ式、値段は割引なし。
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const KATA = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'kata');
const OUT = process.argv[2];
if (!OUT) { console.error('使い方: node 土台を作る.mjs <出力フォルダ>'); process.exit(1); }
if (!fs.existsSync(path.join(KATA, 'index.html'))) { console.error(`空の型が無い: ${KATA}`); process.exit(2); }
fs.mkdirSync(OUT, { recursive: true });
fs.cpSync(KATA, OUT, { recursive: true });
const n = fs.readdirSync(path.join(OUT, 'img'), { recursive: true }).length;
const 札 = (fs.readFileSync(path.join(OUT, 'index.html'), 'utf8').match(/〔/g) || []).length;
console.log(`空の型を写した: ${OUT}（画像 ${n}・札 ${札}）。出来の見本は段ごとの参考（土台の説明の「段ごとの参考」の表）`);
