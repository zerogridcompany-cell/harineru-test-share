# 動画 → 記事の引き継ぎを機械で見る（審査2回目で同じ所が2回落ちた原因の止め。2026-10-16 針マット_ZackD_02 で作った）
# 1. VSL の場面の語（票の「記事で使わない物」と16コマから拾った語）が、ページの文に0か
# 2. 票の「動画が約束した事」の言葉が、見出し（h1〜h3・.sec-t・FAQ の h3）に全部あるか
# 3.（審査3回目で同じ所が2回落ちた原因の止め）売れ方・人の多さを言う文（「方が多」「注文が多」「選ばれ」など＝語の表の「売れ方の語」）は、
#    その文が 決めた値.md にあるか（無い値は編集長の関門4-2で落ちる。前の作業フォルダの テスト用に決めた値.md も受ける）
# 4. セットにだけ付く物（語の表の「セットだけに付く物」）を「付いている」「付く」と言う文に「セット」があるか
# 使い方: ~/.agents/skills/_env/venv/bin/python 引き継ぎの検査.py <index.html> <語の表.json> [<決めた値.md>]   終了コード 0 通った / 1 落ちた
#   3つ目の紙が無い時は、同じフォルダのもう1つの名前（決めた値.md ⇄ テスト用に決めた値.md）を探す
import html, json, os, re, sys
s = open(sys.argv[1], encoding="utf-8").read(); cfg = json.load(open(sys.argv[2], encoding="utf-8"))
s = re.sub(r"<!--.*?-->|<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S).replace("<wbr>", "")
txt = html.unescape(re.sub(r"<[^>]+>", " ", s))
heads = [html.unescape(re.sub(r"<[^>]+>", "", m)) for m in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>|<p class=\"sec-t\">(.*?)</p>", s, flags=re.S) for m in (m if isinstance(m, tuple) else (m,)) if m]
bad = []
for w in cfg["使わない語"]:
    for m in re.finditer(re.escape(w), txt):
        bad.append(f"VSL の場面の語「{w}」が文にある: …{txt[max(0, m.start()-15):m.end()+15].strip()}…")
for w in cfg["見出しに入れる約束"]:
    if not any(w in h for h in heads):
        bad.append(f"約束の言葉が見出しに無い: {w}")
if len(sys.argv) > 3:
    紙 = sys.argv[3]
    if not os.path.exists(紙):
        d, n = os.path.split(紙)
        別 = {"決めた値.md": "テスト用に決めた値.md", "テスト用に決めた値.md": "決めた値.md"}.get(n)
        if 別 and os.path.exists(os.path.join(d, 別)):
            紙 = os.path.join(d, 別)
    tv = re.sub(r"\s+", "", open(紙, encoding="utf-8").read())
    for sen in re.split(r"(?<=[。！？›])|\s{2,}", txt):
        sen = re.sub(r"\s+", "", sen)
        for w in cfg.get("売れ方の語", []):
            i = sen.find(w)
            if i >= 0 and sen[max(0, i - 6):i + len(w) + 4] not in tv:  # 語のまわり（前6字・後4字）が 決めた値.md にあるか
                bad.append(f"売れ方・人の多さの文が {os.path.basename(紙)} に無い: {sen[:60]}（探した字: {sen[max(0, i - 6):i + len(w) + 4]}）")
for sen in re.split(r"(?<=[。！？›])|\s{2,}", txt):
    sen = re.sub(r"\s+", "", sen)
    if re.search(r"付いている|付く", sen) and any(w in sen for w in cfg.get("セットだけに付く物", [])) and "セット" not in sen:
        bad.append(f"セットだけに付く物を、セットと言わずに付くと書いている: {sen[:60]}")
if bad:
    print(f"落ちた {len(bad)}件"); [print("  " + b) for b in bad]; sys.exit(1)
print("通った（VSL の場面の語0・約束の言葉が見出しに全部）")
