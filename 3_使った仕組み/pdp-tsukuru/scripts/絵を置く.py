#!/usr/bin/env python3
"""作った絵を img/ に置き、切り抜きを切り直し、ページの絵と 画像の置き場.md と説明（alt）を突き合わせる（2026-10-19 本人「置く・切り抜く・説明をそろえるを1つの道具に」）。
絵を作り直したら毎回これを回す。img/ に書くのはこの道具だけ（絵を作る係は _gen/ にだけ書く）。

使い方: python3 絵を置く.py <店のフォルダ>
決まり:
  - 作った絵の生の出力は <店>/_gen/<名前>.png。同じ名前は新しい方が勝つ。動く絵は _gen/<名前>_コマ1.png・_コマ2.png… をこの順で回す
  - 画像の置き場.md の各行の「作った画像」の先頭 img/<名前>.png に置く。大きさは、今の img/<名前>.png（空の型の枠＝土台の大きさ）があればそれ、無ければ行の「幅×高さ」
  - 「（<別名>.png に切り抜き）」と書いた行は、置いた後の img/<名前>.png から img/<別名>.png を、今の <別名>.png の大きさで切り直す（短い声・声のカード・専門家の顔など）
  - 透ける絵は白地に重ねる
確かめる物（落ちたら終了コード 1）:
  - ページ（index.html。JS の文字列も）が使う img/ の絵が全部、画像の置き場.md のどこかの行にある
  - 画像の置き場.md の行の絵が img/ に全部ある
  - 生成した絵の行（切り抜き・札の写し・作らない行を除く）に「見えるべき物」が書いてあり、「合う」が ○（references/写真の指示文.md「形・数・向き・姿勢を描かせる時」）
書く物: <店>/絵と説明の一覧.tsv（タブ区切り。ページの絵ごとに 置き場の作る絵・主役・文字・見えるべき物・ページの alt を1行。照らし合わせと編集長が読む）
"""
import os, re, sys
from PIL import Image, ImageOps


def 表を読む(p):
    頭, 行 = None, []
    for l in open(p, encoding="utf-8"):
        if not l.startswith("|"): continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if "主役" in c and "作った画像" in c: 頭 = c; continue
        if 頭 and not set("".join(c)) <= set("-: ") and len(c) == len(頭): 行.append(dict(zip(頭, c)))
    return 行


def 白地(im):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); return bg.convert("RGB")
    return im.convert("RGB")


def 大きさ(店, 名, 行):
    p = os.path.join(店, "img", 名 + ".png")
    if os.path.exists(p):
        try: return Image.open(p).size
        except Exception: pass
    m = re.search(r"(\d+)\s*[×x]\s*(\d+)", 行.get("幅×高さ", ""))
    return (int(m.group(1)), int(m.group(2))) if m else None


def main(a):
    if len(a) < 2: print(__doc__); return 2
    店 = os.path.abspath(a[1]); gen = os.path.join(店, "_gen"); img = os.path.join(店, "img")
    置き場 = os.path.join(店, "画像の置き場.md")
    if not os.path.exists(置き場): print("画像の置き場.md が無い"); return 2
    行たち = 表を読む(置き場)
    if not 行たち: print("画像の置き場.md に「主役」「作った画像」の列を持つ表が無い"); return 2
    置いた, 切った, 落ち = [], [], []
    # 1 置く
    for r in 行たち:
        m = re.search(r"img/([^\s（）/]+?)\.png", r.get("作った画像", ""))
        if not m: continue
        名 = m.group(1); sz = 大きさ(店, 名, r)
        コマ = sorted([f for f in os.listdir(gen) if re.fullmatch(re.escape(名) + r"_コマ\d+\.png", f)], key=lambda f: int(re.findall(r"\d+", f)[-1])) if os.path.isdir(gen) else []
        src = os.path.join(gen, 名 + ".png")
        if コマ and sz:
            fs = [ImageOps.fit(白地(Image.open(os.path.join(gen, f))), sz, Image.LANCZOS) for f in コマ]
            fs[0].save(os.path.join(img, 名 + ".png"), save_all=True, append_images=fs[1:], duration=800, loop=0); 置いた.append(名 + f"（{len(fs)}コマ）")
        elif os.path.exists(src) and sz:
            out = os.path.join(img, 名 + ".png")
            if not os.path.exists(out) or os.path.getmtime(src) > os.path.getmtime(out):
                ImageOps.fit(白地(Image.open(src)), sz, Image.LANCZOS).save(out); 置いた.append(名)
    # 2 切り抜き（置いた後の元から）
    for r in 行たち:
        m = re.search(r"img/([^\s（）/]+?)\.png", r.get("作った画像", ""))
        for 別 in re.findall(r"([\w\-]+?)\.png に切り抜き", r.get("作った画像", "")):
            if not m: continue
            元 = os.path.join(img, m.group(1) + ".png"); sz = 大きさ(店, 別, r)
            if os.path.exists(元) and sz:
                cy = 0.25 if r.get("主役") == "専門家" else 0.5
                ImageOps.fit(白地(Image.open(元)), sz, Image.LANCZOS, centering=(0.5, cy)).save(os.path.join(img, 別 + ".png")); 切った.append(別)
    # 3 突き合わせ
    html = open(os.path.join(店, "index.html"), encoding="utf-8").read()
    使う = set(re.findall(r"img/([\w\-぀-ヿ一-鿿]+?)\.png", html))
    for x in re.findall(r"(?:KDIMG|setImg)\(\s*'([\w\-]+?)\.png'", html): 使う.add(x)
    for x in re.findall(r"\['(mini-\d+|rev\d+)',", html): 使う.add(x)
    for x in re.findall(r"'(rev\d+)',\d\]", html): 使う.add(x)
    if "setImg(" in html:
        # 2026-10-20 うちで直した: セットの絵は TIERS にあるセットの数だけ（2セットの店で set-3 を求めて落ちた）
        mt = re.search(r"var TIERS\s*=\s*\[(.*?)\];", html, re.S)
        ns = re.findall(r"\{\s*n\s*:\s*(\d+)", mt.group(1)) if mt else []
        使う |= {f"set-{n}" for n in ns} if ns else {"set-1", "set-2", "set-3"}
    書いた名 = {}
    for r in 行たち:
        for n in re.findall(r"img/([^\s（）/]+?)\.png", r.get("作った画像", "")) + re.findall(r"([\w\-]+?)\.png に切り抜き", r.get("作った画像", "")) + [r.get("元の画像", "").split("（")[0].strip()]:
            if n: 書いた名.setdefault(n, r)
    for n in sorted(使う):
        if n.startswith(("partner-none", "medal-30.")) or n == "medal-30": continue
        if n not in 書いた名: 落ち.append(f"ページの絵 {n}.png が 画像の置き場.md に無い")
        elif not os.path.exists(os.path.join(img, n + ".png")): 落ち.append(f"{n}.png が img/ に無い")
    for r in 行たち:
        作 = r.get("作った画像", "")
        if "作らない" in 作 or ("切り抜き" in 作 and r.get("見えるべき物", "") in ("", "—")): continue   # 作らない行と、元の絵を別の行で確かめる切り抜きの行は見ない
        if r.get("主役") in ("ロゴ", "札"): continue
        if "見えるべき物" in r and (not r["見えるべき物"] or r["見えるべき物"] == "—") or "見えるべき物" not in r:
            落ち.append(f"#{r.get('#','?')} {r.get('元の画像','')}: 「見えるべき物」が無い（写真の指示文「形・数・向き・姿勢を描かせる時」の②を書く）"); continue
        if not r.get("合う", "").startswith("○"): 落ち.append(f"#{r.get('#','?')} {r.get('元の画像','')}: 「合う」が ○ でない（絵を見て、見えるべき物が写っているかを ○× で書く。× は作り直す）")
    # 4 絵と説明の一覧
    alt = {}
    for m in re.finditer(r'<img[^>]*src="img/([^"]+?)\.png"[^>]*alt="([^"]*)"', html): alt.setdefault(m.group(1), m.group(2))
    L = ["\t".join(["絵", "置き場の作る絵", "主役", "文字", "見えるべき物", "ページの alt"])]
    for n in sorted(使う):
        r = 書いた名.get(n, {})
        L.append("\t".join([n, r.get("作る絵", "（行が無い）"), r.get("主役", ""), r.get("文字", ""), r.get("見えるべき物", ""), alt.get(n, "（JS で出す絵）")]))
    open(os.path.join(店, "絵と説明の一覧.tsv"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"置いた {len(置いた)}・切り直した {len(切った)}・ページの絵 {len(使う)}")
    for x in 落ち: print("- " + x)
    return 0 if not 落ち else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
