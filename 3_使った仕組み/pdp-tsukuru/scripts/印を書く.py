#!/usr/bin/env python3
"""店の設計.md の 4（変数の値）を、店の印.json の 値 に写す。手で2か所に書いて食い違うのを防ぐ。

使い方: python3 印を書く.py <店の設計.md> <店のフォルダ>
終了コード: 0 書いた / 1 設計の 4 に値の無い変数がある（その変数名を出す。印は書かない） / 2 ファイルが無い
2026-10-17 作成。
"""
import sys, os, json, re

def main(a):
    if len(a) < 3: print(__doc__); return 2
    設計, 店 = a[1], a[2]
    印p = os.path.join(店, "店の印.json")
    for p in (設計, 印p):
        if not os.path.exists(p): print("無い:", p); return 2
    text = open(設計, encoding="utf-8").read()
    m = re.search(r"^## 4 .*?$", text, re.M)
    if not m: print("設計に「## 4」が無い"); return 1
    値 = {}
    for l in text[m.end():].splitlines():
        if l.startswith("## "): break
        if not l.startswith("|"): continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 2 or c[0] in ("変数", "") or set("".join(c)) <= set("-: "): continue
        値[c[0]] = c[1]
    try: 印 = json.load(open(印p, encoding="utf-8")); 印["値"]
    except Exception as e: print(f"店の印.json が読めない（{e}）"); return 2
    if not 印["値"]: print("店の印.json の 値 が空（変数 0）。新規.sh が土台を読めていない"); return 2
    # 土台に後から足された ◯ の変数を印に足す（2026-10-18: 土台に4つ足した後、前に作った印に入らず設計の検査が落ち続けた）
    土台 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "土台.md")
    if os.path.exists(土台):
        t = open(土台, encoding="utf-8").read(); m2 = re.search(r"^## 変数.*?$", t, re.M)
        for l in (t[m2.end():].split("\n## ")[0].splitlines() if m2 else []):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) == 6 and c[2] == "◯" and c[0] not in 印["値"]: 印["値"][c[0]] = ""
    空 = [k for k in 印["値"] if not 値.get(k)]
    if 空:
        print(f"設計の 4 に値が無い変数 {len(空)}: " + "、".join(空)); return 1
    for k in 印["値"]: 印["値"][k] = 値[k]
    余り = [k for k in 値 if k not in 印["値"]]
    印["設計"] = os.path.abspath(設計)   # 店の検査を回す.py が、検査の前にこの設計を 移植表_店の設計.md に写す
    json.dump(印, open(印p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"書いた: {印p}（{len(印['値'])} 個）" + (f"。設計にあって印に無い変数 {len(余り)}: {'、'.join(余り)}（土台に無い変数。土台を直すか行を消す）" if 余り else ""))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
