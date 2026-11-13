// 横送りの写真を全枚往復できるか、セットを1つずつカートに入れて個数と金額が表示どおりかを数える（references/dame-list.md の G の2つ）。
//
// 使い方: node 往復とカート.mjs <URL> [--カートなし]
//   往復: 390px で開き、#galThumbs の小さい写しを順に押して、#galDots の印がその番号に移るかを全枚で見る（行きと帰り）
//   カート: 非公開テーマのプレビュー URL で回す（カートは Shopify の /cart.js でしか動かない）。ローカルの index.html は --カートなし
//          セット（#tiers の .tier）を1つずつ選んで #atc を押し、カートの合計（#kcTotal）がそのセットの値段（[data-price]）と同じかを見る。見たらカートを空にする
// 終了コード: 0 全部合った / 1 どれかが合わない / 2 引数が足りない / 3 ページが取れない / 4 実行環境が壊れている
const { 引く, EXE } = await import(new URL('./lib.mjs', import.meta.url));

const 引数 = process.argv.slice(2);
const URL_ = 引数.find(a => !a.startsWith('--'));
const カートなし = 引数.includes('--カートなし');
if (!URL_) { console.error('使い方: node 往復とカート.mjs <URL> [--カートなし]'); process.exit(2); }

const chromium = 引く();
const browser = await chromium.launch({ executablePath: EXE, headless: true });
const 落ち = [];
try {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  try { await page.goto(URL_, { waitUntil: 'load', timeout: 90000 }); } catch (e) { console.error('ページが取れない:', e.message); process.exit(3); }
  await page.waitForTimeout(800);

  // 往復: 小さい写しを 0→最後→0 の順に押し、印の番号が合うか
  const 枚 = await page.$$eval('#galThumbs img', xs => xs.length).catch(() => 0);
  if (!枚) 落ち.push('往復: #galThumbs に小さい写しが無い（横送りの写真が0枚か、空の型の作りが変わっている）');
  const 順 = [...Array(枚).keys()]; const 行き帰り = [...順, ...順.slice(0, -1).reverse()];
  for (const i of 行き帰り) {
    await page.evaluate(i => { const t = document.querySelector(`#galThumbs img[data-i="${i}"]`); t && t.click(); }, i);
    await page.waitForTimeout(700);
    const 印 = await page.$$eval('#galDots i', ds => ds.findIndex(d => d.classList.contains('on')));
    if (印 !== i) { 落ち.push(`往復: ${i + 1}枚目を押したのに印が ${印 + 1}枚目`); break; }
  }
  console.log(`往復: ${枚}枚を行き帰り ${行き帰り.length}回押した`);

  // カート: セットごとに入れて、合計がそのセットの値段と同じか
  if (!カートなし) {
    const セット = await page.$$eval('#tiers .tier', xs => xs.map(x => x.dataset.n));
    if (!セット.length) 落ち.push('カート: #tiers にセットが無い');
    for (const n of セット) {
      await page.evaluate(n => document.querySelector(`#tiers .tier[data-n="${n}"]`).click(), n);
      await page.waitForTimeout(400);
      const 値段 = await page.$eval('[data-price]', e => e.textContent.replace(/[^\d]/g, ''));
      await page.evaluate(() => document.querySelector('#atc').click());
      await page.waitForTimeout(3500);
      const 合計 = await page.$eval('#kcTotal', e => e.textContent.replace(/[^\d]/g, '')).catch(() => '');
      const 個数 = await page.$eval('#kcCount', e => e.textContent.trim()).catch(() => '');
      console.log(`カート: ${n}個のセット 値段 ${値段} → 合計 ${合計}（品数 ${個数}）`);
      if (!合計 || 合計 !== 値段) 落ち.push(`カート: ${n}個のセットの合計 ${合計 || '取れない'} が値段 ${値段} と違う`);
      // 空にする
      await page.evaluate(async () => { await fetch('/cart/clear.js', { method: 'POST' }); });
      await page.waitForTimeout(800);
    }
  }
} finally {
  await browser.close();
}
if (落ち.length) { console.log(`落ちた ${落ち.length}件`); 落ち.forEach(x => console.log(' - ' + x)); process.exit(1); }
console.log('通った');
