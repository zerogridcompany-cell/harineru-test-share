#!/usr/bin/env python3
"""店の機械の検査を全部回し、店のフォルダに 検査の結果.md（index.html の指紋つき）を書く（最終確認 A2・C1・C2・D1）。
審査の箱（scripts/審査を回す.py）が出す前にこれを呼ぶ。手で回してもよい。
検査の前に、店の印.json の「設計」が指す 店の設計.md を、店のフォルダの 移植表_店の設計.md に写す（審査役が読む写し）。

使い方: python3 店の検査を回す.py <店のフォルダ>
回す物: 面の数字.py（店のフォルダの 面の数字の引数.txt があれば）・絵を置く.py（突き合わせ）・他社の計測タグ・横送りの往復・出し直す前の照らし合わせ（いちばん新しい 直し_<回>.md の回の審査が FAIL の時だけ。照らし合わせ_<回>.txt の1行目が「食い違い 0件」）・設計の検査（店の設計の写し 移植表_店の設計.md と 店の印.json）・店の仕上がり検査・
        段ごとの画像の検査（390・1280。段ごとに参考の段と比べる）・lint（390・1440。scripts/lint.mjs。その場で http.server を立てる）
終了コード: 0 全部0 ／ 1 どれかが落ちた ／ 2 index.html か 移植表_店の設計.md が無い
"""
import functools, hashlib, http.server, os, socket, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
HONE = os.path.join(HERE, "lint.mjs")   # hone スキルの lint.mjs の写し（2026-10-19。GitHub だけで回るように）


def main(a):
    if len(a) < 2: print(__doc__); return 2
    店 = os.path.abspath(a[1]); html = os.path.join(店, "index.html")
    if not os.path.exists(html): print("index.html が無い:", 店); return 2
    指紋 = hashlib.sha256(open(html, "rb").read()).hexdigest()[:12]
    結果 = []
    import json as _json, re as _re, shutil as _shutil
    # 店の設計の写し: 店の印.json の「設計」が指す 店の設計.md を 移植表_店の設計.md に写す
    try:
        元 = _json.load(open(os.path.join(店, "店の印.json"), encoding="utf-8")).get("設計", "")
    except Exception:
        元 = ""
    if 元 and os.path.exists(元): _shutil.copyfile(元, os.path.join(店, "移植表_店の設計.md"))
    # 出し直す前の照らし合わせ（references/照らし合わせの指示文.md）: いちばん新しい 直し_<回>.md の回の審査が FAIL なら、
    # 同じ番号の 照らし合わせ_<回>.txt が直しより新しく、1行目が「食い違い 0件」
    直し = sorted((int(m.group(1)), f) for f in os.listdir(店) for m in [_re.fullmatch(r"直し_(\d+)\.md", f)] if m)
    def _FAIL(回):
        p = os.path.join(店, f"審査_{回}.md")
        return os.path.exists(p) and any(l.startswith("判定: FAIL") for l in open(p, encoding="utf-8"))
    if 直し and _FAIL(直し[-1][0]):
        回, f = 直し[-1]; 照 = os.path.join(店, f"照らし合わせ_{回}.txt")
        if not os.path.exists(照):
            結果.append(("照らし合わせ", 1, f"照らし合わせ_{回}.txt が無い（references/照らし合わせの指示文.md の指示文を別の AI に渡し、結果を書く）"))
        elif os.path.getmtime(照) < os.path.getmtime(os.path.join(店, f)):
            結果.append(("照らし合わせ", 1, f"照らし合わせ_{回}.txt が 直し_{回}.md より古い（直しを足したらもう一度照らす）"))
        else:
            頭 = open(照, encoding="utf-8").readline().strip()
            結果.append(("照らし合わせ", 0 if 頭 == "食い違い 0件" else 1, f"照らし合わせ_{回}.txt の1行目: {頭}"))
    設計 = os.path.join(店, "移植表_店の設計.md")
    if not os.path.exists(設計):
        結果.append(("設計の検査", 2, "移植表_店の設計.md が無い（店の印.json に「設計」が無い。印を書く.py を回すと入る）"))
    else:
        r = subprocess.run([sys.executable, os.path.join(HERE, "設計の検査.py"), 設計, 店], capture_output=True, text=True)
        結果.append(("設計の検査", r.returncode, (r.stdout + r.stderr).strip()))
    r = subprocess.run([sys.executable, os.path.join(HERE, "絵を置く.py"), 店], capture_output=True, text=True)
    結果.append(("絵を置く（ページの絵・画像の置き場・説明の突き合わせ）", r.returncode, (r.stdout + r.stderr).strip()))
    本文 = open(html, encoding="utf-8").read()
    タグ = [t for t in ("gtag", "fbq", "klaviyo", "tiktok", "clarity") if t in 本文.lower()]
    結果.append(("他社の計測タグ（C2）", 1 if タグ else 0, "残っている: " + "・".join(タグ) if タグ else "0"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "店の仕上がり検査.py"), 店], capture_output=True, text=True)
    結果.append(("店の仕上がり検査", r.returncode, (r.stdout + r.stderr).strip()))
    for w in ("390", "1280"):
        r = subprocess.run([sys.executable, os.path.join(HERE, "段ごとの画像の検査.py"), 店, "--幅", w], capture_output=True, text=True, timeout=900)
        結果.append((f"段ごとの画像の検査 {w}", r.returncode, (r.stdout + r.stderr).strip()))
    # 面の数字（最終確認 A4）: 店のフォルダに 面の数字の引数.txt（1行に1つ「--広告 <path>」「--記事 <path|URL>」か「--記事なし」）があれば、
    # --店 にこの index.html を足して回す（2026-10-20 うち〈Seiyo の新ハーネス〉で足した。審査役が「面の数字の結果が検査の結果に無い」で落としたため）
    引 = os.path.join(店, "面の数字の引数.txt")
    if os.path.exists(引):
        a2 = []
        for l in open(引, encoding="utf-8"):
            l = l.strip()
            if not l or l.startswith("#"): continue
            k, _, v = l.partition(" ")
            a2 += [k] + ([v.strip()] if v.strip() else [])
        r = subprocess.run([sys.executable, os.path.join(HERE, "面の数字.py")] + a2 + ["--店", html], capture_output=True, text=True, timeout=600)
        結果.append(("面の数字（A4。面の数字の引数.txt）", r.returncode, (r.stdout + r.stderr).strip()))
    else:
        結果.append(("面の数字（A4）", 2, "面の数字の引数.txt が無い（「--広告 <台本か広告の文字>」「--記事 <記事の index.html>」を1行ずつ書く。店直行は「--記事なし」）"))
    with socket.socket() as sk:
        sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]
    class 静か(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x, **k): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(静か, directory=店))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        for w in ("390", "1440"):
            if not os.path.exists(HONE):
                結果.append((f"lint {w}", 2, f"hone スキルの lint.mjs が無い: {HONE}")); continue
            r = subprocess.run(["node", HONE, f"http://127.0.0.1:{port}/index.html", "--w", w], capture_output=True, text=True, timeout=600)
            結果.append((f"lint {w}", r.returncode, (r.stdout + r.stderr).strip()))
        r = subprocess.run(["node", os.path.join(HERE, "往復とカート.mjs"), f"http://127.0.0.1:{port}/index.html", "--カートなし"], capture_output=True, text=True, timeout=600)
        結果.append(("横送りの往復（カートは手順14b でプレビューに回す）", r.returncode, (r.stdout + r.stderr).strip()))
    finally:
        srv.shutdown()
    行 = ["# 機械の検査の結果（店の検査を回す.py が書いた。手で直さない）", "",
          "読む人: 編集長と、店を直す Claude。", "読む時: 審査の前。", "読まなくていい条件: なし。", "",
          f"- index.html の指紋: `{指紋}`（この指紋の index.html で回した結果。index.html を変えたら無効）",
          f"- 回した時刻: {time.strftime('%Y-%m-%d %H:%M')}", ""]
    for 名, 終, 出 in 結果:
        行 += [f"## {名}: 終了コード {終}", "", "```", "\n".join(出.splitlines()[-25:]), "```", ""]
    open(os.path.join(店, "検査の結果.md"), "w", encoding="utf-8").write("\n".join(行))
    for 名, 終, _ in 結果: print(f"{名}: 終了コード {終}")
    return 0 if all(終 == 0 for _, 終, _ in 結果) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
