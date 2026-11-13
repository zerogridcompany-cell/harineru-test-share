#!/usr/bin/env python3
"""店の設計.md と 店の印.json が、組む前・出す前の線を越えているかを数える。

使い方: python3 設計の検査.py <店の設計.md> <店のフォルダ>
終了コード: 0 通った / 1 落ちた（落ちた行を全部出す） / 2 ファイルが無い
見る物:
  1. 設計の 1・2・2.5・3 の欄に空欄が0
  2. 2.5 の4欄それぞれに「客の資料のどの行から」がある
  3. 4 の表: 土台の「変わる ◯」の変数が全部あり、値・出どころ・理由の空欄が0
  4. 7 の「わざと変える物」が1つ以上
  5. 店の印.json の 値 に、◯ の変数が全部あり、空が0（設計の 4 と同じ値）
  6. index.html がある（出す前の検査は別の道具。ここでは有無だけ）
限界: 欄の中に半角の | があると列がずれる（全角｜を使う）。中身が正しいかは見ない。
2026-10-17 作成。同日、別の目のレビューで 行の有無・「当たった」・5と6の有無・変数0・壊れた json を足した。
"""
import sys, os, json, re

土台 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "土台.md")

def 表(text, 見出し):
    """見出しの直後の表を [[欄...]] で返す（ヘッダと区切り行は除く）"""
    m = re.search(r"^## " + re.escape(見出し) + r".*?$", text, re.M)
    if not m: return None
    rows = []
    for l in text[m.end():].splitlines():
        if l.startswith("## "): break
        if l.startswith("|"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if set("".join(c)) <= set("-: "): continue
            rows.append(c)
    return rows[1:] if rows else []

def main(a):
    if len(a) < 3:
        print(__doc__); return 2
    設計, 店 = a[1], a[2]
    for p in (設計, 土台):
        if not os.path.exists(p): print("無い:", p); return 2
    text = open(設計, encoding="utf-8").read()
    変数 = [c[0] for c in (表(open(土台, encoding="utf-8").read(), "変数") or []) if len(c) == 6 and c[2] == "◯"]
    if not 変数:
        print("土台の「## 変数」に ◯ の行が 0。土台の表の形（6列・◯）が変わっている。土台を直す"); return 2
    落ち = []
    # 1〜2
    要る行 = {"1 来た人": ["どの記事から", "段階", "信じた事", "残った疑い", "今の気持ち"], "2 店の型": ["型", "理由"],
              "3 狙う数字": ["最初に動かす数字", "守りの線"], "2.5 見た目の方向": ["方向", "色", "書体", "角と写真の調子", "別の AI に当てさせた結果"]}
    for 見出し, 欄数 in (("1 来た人", 3), ("2 店の型", 2), ("3 狙う数字", 2)):
        rows = 表(text, 見出し)
        if rows is None: 落ち.append(f"{見出し}: 節が無い"); continue
        for 名 in 要る行[見出し]:
            if not any(r[0].startswith(名) for r in rows): 落ち.append(f"{見出し}: 行「{名}」が無い")
        for r in rows:
            if len(r) < 欄数 or any(not x for x in r[1:欄数]): 落ち.append(f"{見出し}: 「{r[0]}」に空欄")
    rows = 表(text, "2.5 見た目の方向")
    if rows is None: 落ち.append("2.5 見た目の方向: 節が無い")
    else:
        for 名 in 要る行["2.5 見た目の方向"]:
            if not any(r[0].startswith(名) for r in rows): 落ち.append(f"2.5: 行「{名}」が無い")
        for r in rows:
            if r[0] == "別の AI に当てさせた結果":
                if len(r) < 2 or "当たった" not in r[1]: 落ち.append("2.5: 別の AI に当てさせた結果に「当たった」が無い（外れたら 3 からやり直す）")
            elif len(r) < 3 or not r[1] or not r[2]: 落ち.append(f"2.5: 「{r[0]}」に値か出どころが無い")
    # 3
    rows = 表(text, "4 変数の値") or []
    ある = {r[0]: r for r in rows}
    for v in 変数:
        r = ある.get(v)
        if not r: 落ち.append(f"4: 変数「{v}」の行が無い")
        elif len(r) < 4 or not r[1] or not r[2] or not r[3]: 落ち.append(f"4: 「{v}」の値・出どころ・理由に空欄")
    # 0 商品の形: 部品ごとに数・位置・向きと、仕入先の写真のどこで見たかがある。写真は店のフォルダの 商品写真/ にある（2026-10-19 本人「商品の形を写真で確かめる関門」）
    rows0 = 表(text, "0 商品の形")
    if not rows0 or not any(r and r[0] for r in rows0): 落ち.append("0 商品の形: 行が 0（部品・形／数・位置・向き／どの写真のどこで見たか を仕入先の写真を見て書く）")
    else:
        写真 = set(os.listdir(os.path.join(店, "商品写真"))) if os.path.isdir(os.path.join(店, "商品写真")) else set()
        for r in rows0:
            if not r or not r[0]: continue
            if len(r) < 3 or not r[1] or not r[2]: 落ち.append(f"0 商品の形: 「{r[0]}」に数・位置・向きか、写真のどこで見たかが無い"); continue
            if not any(f in r[2] for f in 写真): 落ち.append(f"0 商品の形: 「{r[0]}」の見た写真が 商品写真/ のファイル名で書かれていない（{r[2][:30]}）")
    # 5 絵・6 面（行があるか。中身の正しさは別の道具）
    rows5 = 表(text, "5 絵")
    if not rows5: 落ち.append("5 絵: 行が 0")
    rows6 = 表(text, "6 3つの面")
    if rows6 is None or len(rows6) < 4: 落ち.append("6 3つの面: 行が 4 未満（評価と件数・配送日数・値段・保証日数）")
    else:
        for r in rows6:
            if len(r) < 2 or not r[-1] or r[-1] in ("—", "-"): 落ち.append(f"6 3つの面: 「{r[0]}」の店に入れる数字（右端の欄）が空")
    # 4
    m = re.search(r"^## 7 .*?$", text, re.M)
    本文 = text[m.end():] if m else ""
    if not any(l.strip().startswith("- ") and len(l.strip()) > 2 for l in 本文.splitlines()): 落ち.append("7: わざと変える物が0")
    # 5
    印p = os.path.join(店, "店の印.json")
    if not os.path.exists(印p): 落ち.append("店の印.json が無い")
    else:
        try: 値 = json.load(open(印p, encoding="utf-8"))["値"]
        except Exception as e: print(f"店の印.json が読めない（{e}）"); return 2
        for v in 変数:
            if v not in 値: 落ち.append(f"印: 「{v}」が無い")
            elif not str(値[v]).strip(): 落ち.append(f"印: 「{v}」が空")
            elif v in ある and len(ある[v]) > 1 and str(値[v]).strip() != ある[v][1]: 落ち.append(f"印: 「{v}」が設計の値と違う（印 {値[v]!s:.30} / 設計 {ある[v][1]:.30}）")
    # 6
    if not os.path.exists(os.path.join(店, "index.html")): 落ち.append("index.html が無い")
    if 落ち:
        print(f"落ちた {len(落ち)} 件（変数 {len(変数)} 個を見た）")
        for x in 落ち: print(" -", x)
        return 1
    print(f"通った（変数 {len(変数)} 個。見たのは 1・2・2.5・3 の行と空欄、4 の値・出どころ・理由、5・6 の行の有無、7 の有無、印の一致。中身の正しさは見ていない）"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
