// URL をヘッドレスの Chromium で開き、JS が動いた後の文字を標準出力に出す（転送・後から描く店のため）。
// 使い方: node 開いた文字.mjs <URL>
// 閉じた <details> の中も拾うため、innerText でなく文字の塊を全部集める（script・style は除く）
const { 開く } = await import(new URL('./lib.mjs', import.meta.url));
const url = process.argv[2];
const { browser, page } = await 開く(url, { W: 390, timeout: 60000 });
await page.waitForTimeout(2500);
const 文 = await page.evaluate(() => {
  // 文字の塊ごとに空白で区切る（textContent のままだと隣の数字がくっつく。6,900円760円 → 6900760）
  const 出 = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode, 親 = n.parentElement;
    if (親 && ['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(親.tagName)) continue;
    const t = n.textContent.trim(); if (t) 出.push(t);
  }
  return 出.join(' ');
});
await browser.close();
process.stdout.write(文);
