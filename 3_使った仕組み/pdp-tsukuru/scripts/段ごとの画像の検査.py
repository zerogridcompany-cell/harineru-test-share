#!/usr/bin/env python3
"""店の写真を、段ごとに「その段が良い方を取った参考の同じ段」と比べる（最終確認 A2。2026-10-19 本人
「いいとこ取りしているそのセクションを、その参考にしているセクションと比較する」「bath を参考にしない」「構造的に直して」）。

使い方: python3 段ごとの画像の検査.py <店のフォルダ> [--幅 390]
比べる元: 土台の説明（references/土台.md）の「## 段ごとの参考」の表。
  K ＝ ここちドライの商品ページ（references/参考_ここちドライの商品ページ/index.html。土台を作った元の写し）
  W ＝ ワンドライのプレミアムLP（references/デザインの参考_wandry_2026-10-17.html）
  表の「参考」が「K・1枚目W」の段は、横送りの1枚目だけワンドライの最初の写真と比べ、残りはここちドライと比べる。
見る物（段ごと）: 見えている写真の枚数・1枚ずつの縦横比と本文の幅に対する横幅（差 0.06 まで）・動く絵か止まりか・
  1枚ずつの写真の中身（主役と、写真の中の文字の有無。表の「参考の写真」と、店の 画像の置き場.md の「主役」「文字」列を比べる）。
  段の切れ目はページの <!-- ===== 段の名前 ===== --> の印（土台と同じ順・同じ数）。
数えない物（わざと変える物。表の「わざと変える差」に決めの日付つきで書いてある物だけ）:
  表の「わざと変える差」に「動画→静止画を許す」とある段の、動画と静止画の違い／data-tasu の枠の中（足した写真。例: レビュー全部に写真 2026-10-18 本人）／ .colors の中（色の札は商品の色の数で決まる）
終了コード: 0 差が0 ／ 1 差がある ／ 2 比べる元か表が無い
"""
import os, re, sys
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")
参考の店 = {"K": os.path.join(REF, "参考_ここちドライの商品ページ", "index.html"),
           "W": os.path.join(REF, "デザインの参考_wandry_2026-10-17.html")}
土台 = os.path.join(REF, "土台.md")

JS = r"""
() => {
  const root = document.querySelector('#kpdp') || document.body;
  const cw = root.getBoundingClientRect().width || innerWidth;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_COMMENT | NodeFilter.SHOW_ELEMENT);
  let 段 = -1, 名 = [], out = [];
  while (w.nextNode()) {
    const n = w.currentNode;
    if (n.nodeType === 8) { const m = n.textContent.match(/={6,}\s*(.+?)\s*={6,}/); if (m) { 段++; 名.push(m[1]); } continue; }
    if (!/^(IMG|VIDEO)$/.test(n.tagName)) continue;
    if (n.closest('[data-tasu],.colors,[id^="kc"],.thumbs')) continue;  // .thumbs は横送りの写真の小さな写し（PC の幅だけ出る。同じ写真を二度数えない）
    const r = n.getBoundingClientRect();
    if (r.width < 60 || r.height < 40) continue;
    let e = n, vis = true; while (e) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || e.hidden) { vis = false; break; } e = e.parentElement; }
    if (!vis) continue;
    out.push({段, src: decodeURIComponent(n.currentSrc || n.src || n.poster || ''), 縦横: +(r.height / r.width).toFixed(2), 幅: +(r.width / cw).toFixed(2)});
  }
  return {名, 絵: out};
}
"""

def 表を読む():
    t = open(土台, encoding="utf-8").read()
    m = re.search(r"^## 段ごとの参考.*?$", t, re.M)
    if not m: return None
    行 = []
    for l in t[m.end():].splitlines():
        if l.startswith("## "): break
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if l.startswith("|") and c and c[0].isdigit(): 行.append({"番": int(c[0]), "段": c[1], "参考": c[2], "写真": c[3] if len(c) > 3 else "", "許す": c[4] if len(c) > 4 else ""})
    return 行


def 参考の写真を割る(文):
    """「1 商品・○／2〜5 イラスト・×／短い声9件 人の顔と商品・×／なし」を [(主役, 文字)] に開く"""
    out = []
    if not 文 or 文.startswith("なし"): return out
    for 片 in 文.split("／"):
        片 = re.sub(r"（.*?）", "", 片).strip()
        m = re.match(r"(?:(\d+)(?:〜(\d+))?|短い声(\d+)件)\s*(\S+?)(?:・([○×]))?$", 片)
        if not m: continue
        if m.group(3): n = int(m.group(3))
        else: n = (int(m.group(2)) - int(m.group(1)) + 1) if m.group(2) else 1
        out += [(m.group(4), m.group(5) or "")] * n
    return out

def うちの写真の中身(店):
    """画像の置き場.md の「主役」「文字」を、ページで使う画像の名前（拡張子なし）から引けるようにする"""
    p = os.path.join(店, "画像の置き場.md")
    if not os.path.exists(p): return None
    頭, 表 = None, {}
    for l in open(p, encoding="utf-8"):
        if not l.startswith("|"): continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if "主役" in c: 頭 = c; continue
        if not 頭 or set("".join(c)) <= set("-: "): continue
        r = dict(zip(頭, c)); 中 = (r.get("主役", ""), r.get("文字", "")[:1])
        名 = set(re.findall(r"img/([^\s（）/]+?)\.(?:png|webp|jpg|svg)", r.get("作った画像", "")))
        名 |= set(re.findall(r"([\w\-]+?)\.png に", r.get("作った画像", "")))
        if r.get("元の画像"): 名.add(r["元の画像"].split("（")[0].strip())
        for n in 名: 表.setdefault(n, 中)
        for n in re.findall(r"([\w\-]+?)\.png に", r.get("作った画像", "")): 表[n] = 中
    return 表

def 動くか(src):
    p = src.replace("file://", "")
    try:
        im = Image.open(p); return "動く" if getattr(im, "n_frames", 1) > 1 else "止まり"
    except Exception:
        return "動画" if p.endswith((".mp4", ".webm")) else "?"

def 測る(pg, path, 幅):
    pg.set_viewport_size({"width": 幅, "height": 844 if 幅 < 700 else 800})
    pg.goto("file://" + path, wait_until="networkidle", timeout=120000)
    pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}scrollTo(0,0)}")
    pg.wait_for_timeout(800)
    return pg.evaluate(JS)

def ワンドライの1枚目(pg, 幅):
    pg.set_viewport_size({"width": 幅, "height": 844 if 幅 < 700 else 800})
    pg.goto("file://" + 参考の店["W"], wait_until="networkidle", timeout=120000)
    return pg.evaluate("""() => { const im=[...document.images].find(i=>/gallery/.test(i.src) && i.getBoundingClientRect().width>200); const cw=document.body.getBoundingClientRect().width; if(!im) return null; const r=im.getBoundingClientRect(); return {src:im.src, 縦横:+(r.height/r.width).toFixed(2), 幅:+(r.width/cw).toFixed(2)}; }""")

def main(a):
    if len(a) < 2: print(__doc__); return 2
    店 = os.path.abspath(a[1]); うち = os.path.join(店, "index.html") if os.path.isdir(店) else 店
    幅 = int(a[a.index("--幅") + 1]) if "--幅" in a else 390
    for p in list(参考の店.values()) + [うち, 土台]:
        if not os.path.exists(p): print("無い:", p); return 2
    表 = 表を読む()
    if not 表: print("土台の説明に「## 段ごとの参考」の表が無い:", 土台); return 2
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        k = 測る(pg, 参考の店["K"], 幅); u = 測る(pg, うち, 幅); w1 = ワンドライの1枚目(pg, 幅); b.close()
    差 = []
    中身 = うちの写真の中身(os.path.dirname(うち))
    if 中身 is None: 差.append("画像の置き場.md が無い（主役と文字を比べられない）")
    if not (len(k["名"]) == len(u["名"]) == len(表)):
        差.append(f"段の数: 表 {len(表)} / ここちドライ {len(k['名'])} / うち {len(u['名'])}（土台と同じ段の印にする）")
    print(f"幅 {幅}")
    for i, 名 in enumerate(u["名"]):
        r = 表[i] if i < len(表) else {"参考": "K", "段": "?", "許す": ""}
        kk = [x for x in k["絵"] if x["段"] == i]; uu = [x for x in u["絵"] if x["段"] == i]
        参名 = "ここちドライ「" + (k["名"][i] if i < len(k["名"]) else "?") + "」"
        if "1枚目W" in r["参考"] and uu:
            if not w1: 差.append(f"段{i+1}: ワンドライの最初の写真が測れない");
            else:
                for 欄 in ("縦横", "幅"):
                    if abs(uu[0][欄] - w1[欄]) > 0.06: 差.append(f"段{i+1}「{名}」1枚目（参考 ワンドライの最初の写真）: {欄} 参考 {w1[欄]} / うち {uu[0][欄]}")
            kk, uu, 足 = kk[1:], uu[1:], 1
        else:
            足 = 0
        print(f"  段{i+1}「{名}」 参考 {r['参考']}（{参名}） {len(kk)+足}枚 ／ うち {len(uu)+足}枚")
        参写 = 参考の写真を割る(r.get("写真", ""))
        全 = [x for x in u["絵"] if x["段"] == i]
        if 中身 is not None and 参写:
            if len(参写) != len(全): 差.append(f"段{i+1}「{名}」: 表の参考の写真 {len(参写)}枚 / うち {len(全)}枚（表か写真の数を直す）")
            for j, (x, (主, 字)) in enumerate(zip(全, 参写)):
                if 主 == "動画": continue
                n0 = os.path.splitext(os.path.basename(x["src"]))[0]
                う = 中身.get(n0)
                if not う: 差.append(f"段{i+1}「{名}」{j+1}枚目 {n0}: 画像の置き場.md に主役と文字の行が無い"); continue
                ok = う[0] == 主 or ("声の写真は商品でよい" in r.get("許す", "") and 主 == "人の顔と商品" and う[0] in ("商品", "手と商品"))
                if not ok: 差.append(f"段{i+1}「{名}」{j+1}枚目 {n0}: 主役 参考 {主} / うち {う[0]}")
                if 字 and う[1] and 字 != う[1]: 差.append(f"段{i+1}「{名}」{j+1}枚目 {n0}: 写真の中の文字 参考 {字} / うち {う[1]}")
        if len(kk) != len(uu): 差.append(f"段{i+1}「{名}」（参考 {参名}）: 写真の数 参考 {len(kk)+足} / うち {len(uu)+足}")
        for j, (x, y) in enumerate(zip(kk, uu)):
            n = os.path.basename(x["src"])
            for 欄 in ("縦横", "幅"):
                if abs(x[欄] - y[欄]) > 0.06: 差.append(f"段{i+1}「{名}」{j+1+足}枚目（参考 {参名} の {n}）: {欄} 参考 {x[欄]} / うち {y[欄]}")
            a1, a2 = 動くか(x["src"]), 動くか(y["src"])
            if (a1, a2) == ("動画", "止まり") and "動画→静止画を許す" in r.get("許す", ""): continue
            if "?" not in (a1, a2) and a1 != a2: 差.append(f"段{i+1}「{名}」{j+1+足}枚目（参考 {参名} の {n}）: 参考は「{a1}」/ うちは「{a2}」（同じ種類で作る）")
    for d in 差: print("- " + d)
    print("差 0" if not 差 else f"差 {len(差)}")
    return 0 if not 差 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
