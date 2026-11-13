#!/usr/bin/env python3
"""店を編集長の審査に出し、店のフォルダに 審査_<回>.md を書く。部屋（team-room）も advertorial-automation も要らない。
pdp-tsukuru と Claude Code（`claude` コマンド）だけで回る（2026-10-19 本人「それぞれで作ったら良くない？」）。

使い方: python3 審査を回す.py <店のフォルダ> [--待つ分 40] [--モデル opus]

出す前に道具が自分で確かめる物（通らなければ出さずに終了コード2）:
  - 前の回が FAIL なら、直し_<前の回>.md に「探した語」の行が指摘の件数以上ある（1か所だけ直して別の所と食い違うのを止める）
  - 前の回から index.html も img/ も変わっていなければ出し直さない
  - scripts/店の検査を回す.py が全部0（検査の結果.md を指紋つきで書く）
審査のしかた: 書いた本人でない Claude（既定 Opus）を `claude -p` で1つ起こし、references/ストア担当の審査.md の「## 審査の決まり」で
  店のフォルダの物を読ませる。読むだけで、店の物は書き換えさせない（Edit・Write・Bash・Agent を使わせない）。
回し方（SKILL.md の手順11。回数の上限は無い）:
  1. この道具を走らせる。PASS なら終了コード0で終わり
  2. FAIL なら終了コード1。審査_<回>.md を全部直し、直し_<回>.md に1行ずつ書く。直した所を書いた本人でない Opus に照らし合わせさせ（references/照らし合わせの指示文.md）、照らし合わせ_<回>.txt が「食い違い 0件」になったら 1 へ
終了コード: 0 PASS（指摘なし）／ 3 PASS だが書き方の指摘あり（審査_<回>.md を直して機械の検査を通す）／ 1 FAIL ／ 2 出せなかった
"""
import hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDP = os.path.dirname(HERE)
決まりの書類 = os.path.join(PDP, "references", "ストア担当の審査.md")


def 引数(argv, 名, 既定):
    return argv[argv.index(名) + 1] if 名 in argv and argv.index(名) + 1 < len(argv) else 既定


def 決まり():
    """ストア担当の審査.md の「## ストア担当の関門」と「## 審査の決まり」の2節（審査の決まりが関門を指すので両方渡す）"""
    t = open(決まりの書類, encoding="utf-8").read()
    節 = []
    for 名 in ("ストア担当の関門", "審査の決まり"):
        m = re.search(r"^## " + 名 + r"\s*$(.*?)(?=^## |\Z)", t, re.M | re.S)
        if m: 節.append(f"### {名}\n" + m.group(1).strip())
    return "\n\n".join(節)


def 同じ所(理由, 前の理由):
    """前の回の指摘と同じ箱（A2・F7 のような番号）か同じ書き出しの指摘に印を付ける。同じ所で2回落ちたら、直す前に手順か道具を直す"""
    def 箱(x): return set(re.findall(r"\b[A-FT]\d{1,2}\b", x))
    out = []
    for x in 理由:
        同じ = any((箱(x) & 箱(y)) or x[:20] == y[:20] for y in 前の理由)
        out.append(("【前の回も同じ所】" if 同じ else "") + x)
    return out


def 指紋(店):
    """index.html と img/ の中身の指紋。絵だけを直した回も「直した」と数える"""
    h = hashlib.sha256(open(os.path.join(店, "index.html"), "rb").read())
    for 根, _, fs in sorted(os.walk(os.path.join(店, "img"))):
        for f in sorted(fs):
            q = os.path.join(根, f); h.update(os.path.relpath(q, 店).encode()); h.update(open(q, "rb").read())
    return h.hexdigest()[:16]


def 前の回(店):
    回たち = sorted(int(m.group(1)) for f in os.listdir(店) for m in [re.fullmatch(r"審査_(\d+)\.md", f)] if m)
    if not 回たち:
        return 0, None, 0, None
    n = 回たち[-1]
    t = open(os.path.join(店, f"審査_{n}.md"), encoding="utf-8").read()
    判 = "FAIL" if re.search(r"^判定: FAIL", t, re.M) else "PASS"
    件 = len(re.findall(r"^\d+\. ", t, re.M))
    紋 = re.search(r"^指紋: (\w+)", t, re.M)
    return n, 判, 件, 紋.group(1) if 紋 else None


def 絵を並べる(店):
    """画像の置き場.md の絵を、番号つきで 16 枚ずつ並べた1枚（絵の一覧_<n>.jpg）にする。審査役は先にこれを全部見る"""
    md = os.path.join(店, "画像の置き場.md")
    if not os.path.exists(md):
        return []
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return []
    絵, 見た = [], set()
    for l in open(md, encoding="utf-8"):
        if not l.startswith("|"):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        m = re.search(r"(img/[^\s（|]+\.(?:png|jpe?g|webp))", " ".join(c))
        if not m or m.group(1) in 見た or not os.path.exists(os.path.join(店, m.group(1))):
            continue
        見た.add(m.group(1)); 絵.append((c[0], m.group(1)))
    字 = None
    for f in ("~/Library/Fonts/NotoSansJP.ttf", "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
        try:
            字 = ImageFont.truetype(os.path.expanduser(f), 20); break
        except Exception:
            pass
    字 = 字 or ImageFont.load_default()
    W, 列, 段 = 340, 4, 4
    out = []
    for k in range(0, len(絵), 列 * 段):
        組 = 絵[k:k + 列 * 段]
        sh = Image.new("RGB", (列 * W, ((len(組) + 列 - 1) // 列) * (W + 30)), "white"); d = ImageDraw.Draw(sh)
        for i, (番, f) in enumerate(組):
            im = Image.open(os.path.join(店, f)).convert("RGB"); im.thumbnail((W - 8, W - 8))
            x, y = (i % 列) * W, (i // 列) * (W + 30)
            sh.paste(im, (x + 4, y + 4)); d.text((x + 6, y + W), f"#{番} {os.path.basename(f)[:28]}", fill="black", font=字)
        名 = f"絵の一覧_{k // (列 * 段) + 1}.jpg"
        sh.save(os.path.join(店, 名), quality=82); out.append(名)
    return out


def 頼む文(店, 回, 一覧):
    # 照らし合わせは、前の回の審査が FAIL の時だけ見せる（PASS で書き方だけ直した回は照らし合わせを回さない）
    前p = os.path.join(店, f"審査_{回 - 1}.md")
    前がFAIL = os.path.exists(前p) and any(l.startswith("判定: FAIL") for l in open(前p, encoding="utf-8"))
    読む = ["index.html", "検査の結果.md"] + 一覧 + sorted(f for f in os.listdir(店) if f.startswith("移植表") and f.endswith(".md")) + \
        [f for f in ("画像の置き場.md", "決めた値.md", "絵と説明の一覧.tsv", "報告.md", f"直し_{回 - 1}.md") + ((f"照らし合わせ_{回 - 1}.txt",) if 前がFAIL else ()) if os.path.exists(os.path.join(店, f))]
    return f"""あなたは編集長。店（商品ページ）を作った本人ではない。この店の {回} 回目の審査をする。
店のフォルダ（今いる所）: {店}
読む物（全部読む。絵は 絵の一覧_<n>.jpg を先に全部見て、気になった絵だけ img/ を1枚ずつ開く）: {"、".join(読む)}
スキルの置き場（決まりの書類が指す SKILL.md・references/ はここ）: {PDP}

## 審査の決まり
{決まり()}

## 答え方
店の物は1つも書き換えない。読んで照らすだけ。
最後に、次の形の JSON を1つだけ書いて終わる（前後に説明を書いてよいが、JSON は最後に1つ）:
{{"decision": "PASS" か "FAIL", "reasons": ["指摘1件を1文で。どの段・どの文や絵・何がどう違うか・何に合わせるか", ...]}}
FAIL: 最終確認 A〜E・T・F の箱に理由の無い × が1つでもある、数字・名前・場面が書類の間で食い違う、決まりに外れた絵や文がある時。
PASS で reasons が空: 直す所が無い。PASS で reasons あり: 合格だが書き方だけ直す所がある（再審査は要らない程度の物だけ）。"""


def 審査役(店, 文, 分, モデル):
    r = subprocess.run(
        ["claude", "-p", 文, "--model", モデル, "--output-format", "json", "--add-dir", PDP,
         "--allowedTools", "Read", "Glob", "Grep",
         "--disallowedTools", "Edit", "Write", "NotebookEdit", "Bash", "Agent", "WebFetch", "WebSearch"],
        cwd=店, capture_output=True, text=True, timeout=分 * 60)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip()[-600:])
    結果 = json.loads(r.stdout).get("result", "")
    候補 = re.findall(r"\{[^{}]*\"decision\"[^{}]*\[.*?\][^{}]*\}", 結果, re.S)
    if not 候補:
        raise RuntimeError("審査役が判定の JSON を書かなかった: " + 結果[-400:])
    d = json.loads(候補[-1])
    if d.get("decision") not in ("PASS", "FAIL"):
        raise RuntimeError("判定が PASS か FAIL でない: " + 候補[-1][:200])
    return d["decision"], [str(x) for x in d.get("reasons") or []], 結果


def 書く(店, 回, 判, 理由, 紋):
    頭 = ["読む人: この店を直す Claude。", "読む時: 直す前に全部。", "読まなくていい条件: なし。", "", f"指紋: {紋}", ""]
    探す = ("指摘1件ごとに、名前・数字・場面の語を `grep -n <語> index.html 移植表*.md 画像の置き場.md 決めた値.md` で全部探してそろえ、"
          f"直し_{回}.md の各行に「探した語: <語>／見つかった所: <数>／全部そろえた」を書く。")
    if 判 == "FAIL":
        行 = [f"# 編集長の審査 {回}回目"] + [""] + 頭 + [f"判定: FAIL（{len(理由)}件）。全部直してから、もう一度 `審査を回す.py` を走らせる。回数の上限は無い。", "", 探す, ""]
    else:
        行 = [f"# 編集長の審査 {回}回目（合格）"] + [""] + 頭 + [f"判定: PASS。" + (f"下の {len(理由)} 件は書き方の指摘。全部直し、機械の検査（`scripts/店の検査を回す.py`）だけ通す。再審査には出さない。" if 理由 else "直す所なし。"), ""] + ([探す, ""] if 理由 else [])
    前p = os.path.join(店, f"審査_{回 - 1}.md")
    前の理由 = [re.sub(r"^\d+\.\s*(【前の回も同じ所】)?", "", l).strip() for l in open(前p, encoding="utf-8") if re.match(r"^\d+\.\s", l)] if os.path.exists(前p) else []
    理由 = 同じ所(理由, 前の理由)
    if any(x.startswith("【前の回も同じ所】") for x in 理由):
        行 += ["【前の回も同じ所】の付いた指摘は、直す前に、その箱を作る手順に「やる事」を1行入れて止める検査か見本に結ぶ（SKILL.md「直しの入れ方」）。", ""]
    行 += [f"{i}. {x}" for i, x in enumerate(理由, 1)]
    open(os.path.join(店, f"審査_{回}.md"), "w", encoding="utf-8").write("\n".join(行) + "\n")


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    店 = os.path.abspath(argv[1]); 分 = int(引数(argv, "--待つ分", "40")); モデル = 引数(argv, "--モデル", "opus")
    if not os.path.exists(os.path.join(店, "index.html")):
        print("index.html が無い:", 店); return 2
    if not os.path.exists(決まりの書類):
        print("審査の決まりが無い:", 決まりの書類); return 2
    前, 前の判, 前の件, 前の紋 = 前の回(店)
    回 = 前 + 1; 紋 = 指紋(店)
    if 前 and 前の紋 == 紋:
        print(f"{前}回目から index.html も img/ も変わっていない。出し直さない（審査_{前}.md を直す）"); return 2
    if 前の判 == "FAIL":
        直し = os.path.join(店, f"直し_{前}.md")
        探した = sum(1 for l in open(直し, encoding="utf-8") if "探した語" in l) if os.path.exists(直し) else 0
        if 探した < 前の件:
            print(f"直し_{前}.md に「探した語」の行が {探した} 行（{前}回目の指摘は {前の件} 件）。指摘1件ごとに書いてから出す"); return 2
    r = subprocess.run([sys.executable, os.path.join(HERE, "店の検査を回す.py"), 店], capture_output=True, text=True, timeout=3600)
    if r.returncode != 0:
        print(f"機械の検査が落ちた。審査には出さない。{os.path.join(店, '検査の結果.md')} を見て直す"); return 2
    一覧 = 絵を並べる(店)
    print(f"{回}回目を審査役（{モデル}）に出した。判定を待つ（最大 {分} 分）")
    try:
        判, 理由, 全文 = 審査役(店, 頼む文(店, 回, 一覧), 分, モデル)
    except subprocess.TimeoutExpired:
        print(f"{分} 分の間に判定が出なかった。--待つ分 を延ばしてもう一度走らせる"); return 2
    except Exception as e:
        print("審査役が判定を出せなかった:", e); return 2
    open(os.path.join(店, f"審査_{回}_全文.md"), "w", encoding="utf-8").write(全文 + "\n")
    書く(店, 回, 判, 理由, 紋)
    if 判 == "FAIL":
        print(f"FAIL（{回}回目・{len(理由)}件）。{os.path.join(店, f'審査_{回}.md')} を直してから、もう一度走らせる"); return 1
    if 理由:
        print(f"PASS（{回}回目）。書き方の指摘 {len(理由)} 件を 審査_{回}.md に書いた。直して機械の検査を通すまで終わりではない"); return 3
    print(f"PASS（{回}回目）"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
