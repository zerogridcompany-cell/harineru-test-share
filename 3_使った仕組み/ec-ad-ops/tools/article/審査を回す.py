#!/usr/bin/env python3
"""記事の審査を1回ぶん回す道具（仮ハーネス版。2026-10-16）。
元は「部屋」（team-room のサーバー http://127.0.0.1:3200）に出して編集長の判定を待つ道具だった。
仮ハーネスでは部屋を立てない。編集長は、回ごとに新しく呼ぶサブエージェントにする（作った会話を知らない、まっさらな目）。
この道具は ①出す前の関門 ②機械の検査 ③サブエージェントに渡す束（頼み_<回>.md）を作る と、
④サブエージェントが書いた 判定_<回>.json から 審査_<回>.md を書く、の2つだけをする。
回し方の正本: ec-ad-ops/references/article/審査の回し方.md
店（pdp-tsukuru が作った商品ページ。フォルダに 店の印.json がある）を渡した時は、記事の検査ではなく pdp-tsukuru の
scripts/店の検査を回す.py を回し、決まりは pdp-tsukuru の references/ストア担当の審査.md の「## 審査の決まり」を使う
（友だちの e809ba0・af6a82a。店だけの審査の箱は pdp-tsukuru の scripts/審査を回す.py にもある）。

使い方:
  ~/.agents/skills/_env/venv/bin/python 審査を回す.py <記事のフォルダ> <案件ID> [--役 記事ライター]
      → 関門と機械の検査を通れば、記事のフォルダに 審査_束_<回>/頼み_<回>.md を作って終了コード4。
        Claude は頼み_<回>.md の全文をそのまま、新しいサブエージェント（Agent ツール。毎回新しく呼ぶ）に渡す。
        サブエージェントは 記事のフォルダ/判定_<回>.json を書いて終わる
  ~/.agents/skills/_env/venv/bin/python 審査を回す.py <記事のフォルダ> <案件ID> --書く
      → 判定_<回>.json を読んで 審査_<回>.md を書き、審査の記録.jsonl に1行足す
  ~/.agents/skills/_env/venv/bin/python 審査を回す.py <記事のフォルダ> <案件ID> --検査だけ
      → 機械の検査だけ回して 検査の結果.md を書く（終了コード3の後、書き方の指摘を直した時）

判定の決め方（元の部屋の「審査の収束」と同じ）: 編集長は、ずれを1件ずつ「決定を変える／書き方／本人の決まりに反する」に分ける。
  決定を変える が1件でもあれば FAIL。書き方 だけなら PASS（書き方の指摘あり）。本人の決まりに反する は捨てる。
  分けられない・迷う物は 決定を変える に倒す（戻す方が安全）。

終了コード:
  0 PASS（指摘なし）
  1 FAIL（審査_<回>.md を書いた。全部直し、直し_<回>.md を書いて、もう一度この道具を走らせる）
  2 出せなかった（機械の検査が落ちた・直し_<前の回>.md が足りない・判定_<回>.json が無いか壊れている）
  3 PASS だが書き方の指摘あり（審査_<回>.md を直し、--検査だけ を通して終わり。再審査には出さない）
  4 束を作った。頼み_<回>.md をサブエージェントに渡し、終わったら --書く を走らせる
"""
import hashlib, json, os, re, shutil, subprocess, sys, time

ここ = os.path.dirname(os.path.abspath(__file__))
仮 = os.path.dirname(os.path.dirname(os.path.dirname(ここ)))       # スキルの根（~/.agents/skills）。ここ＝ec-ad-ops/tools/article（2026-10-20 一つ上がり足りず役/編集長.md が見つからなかったのを直した）
記事の知識 = os.path.join(仮, "ec-ad-ops", "references", "article")
編集長の役 = os.path.join(記事の知識, "役", "編集長.md")
PDP = os.path.join(仮, "pdp-tsukuru")
決めた値の名 = ("決めた値.md", "テスト用に決めた値.md")   # 2026-10-20 に「決めた値.md」へ名前を替えた。前の作業フォルダの古い名前も受ける
決まり = ("{役} の手順書（{知}/役/{役}.md）の関門と、本人の直しの台帳（{知}/毎日の制作/_直しの台帳.md）の {役} の節で照らす。"
        "加えて {知}/05 記事を作る.md の「一回で作る道」、{知}/型/_買うまでの15の事.md（見終わった人の状態・入れる手段・好奇心の穴をつなぐ）と "
        "{知}/15の対応表.md（15の言い方は vsl-script の 15の心の声 の言葉を正とする）、{知}/決めたこと.md の 2026-10-15 の行、"
        "そしてこちら（Seiyo）の決め {仮}/ec-ad-ops/references/article.md の鉄則（VSL のビジュアル・場面・登場人物・「動画で見た」の文が画像にも文にも無い／"
        "画像は Codex で作った物）。"
        "こちらの決めと元の決めが食い違う所は、こちらの決めを取る。見た目はここちドライの記事の質（{知}/資料/針マット/ここちドライの手本/）と比べる。"
        "題は {知}/型/_題の型.md の関門・崩れ方・声の決まりで見る（役/編集長.md の関門10）。"
        "残った疑いの重さ1は、移植表の | 疑い | 重さ | … | の表の答える段で、値段の段より前に、読み手が次に何をすればいいかまで答え切っているか（役/編集長.md の関門11）。"
        "画像は 画像の置き場.md と index.html の画像が1対1か。"
        "【毎回全部を見る】2回目以降も前回の指摘だけを見ない。毎回、{知}/資料/記事の最終確認_ひな形.md の全項目と、編集長の関門 7-1・7-2 を全部の段で上から順に見て、"
        "ずれを全部書く。前回○だった所も見直す。名前・数字・場面が記事の中と移植表で食い違っていないかを全文で照らす。"
        "機械の検査は 検査の結果.md（index.html の指紋つき）を読み、指紋が今の index.html と違えば、それだけで 決定を変える のずれにする。"
        "【絵の見方（2026-10-18）】絵は 絵の一覧_<n>.jpg（画像の置き場.md の # の番号つきで16枚ずつ並べた1枚）を先に全部見る。1枚ずつ開くのは一覧で気になった絵だけにする。"
        "【審査の中でしない】rm など消す操作・戻せない操作はしない。作業の画像は /tmp に新しい名前で書き、消さずに置く")
束に入れる = ["index.html", "検査の結果.md", "画像の置き場.md", "報告.md", "最終確認.md", "決めた値.md", "テスト用に決めた値.md", "予測した事.md",
          "商品の形.md", "動く素材.md", "値段の段.html", "コメント欄.html", "画像の置き方の引数.txt", "絵と説明の一覧.tsv"]


def 引数(argv, 名, 既定):
    return argv[argv.index(名) + 1] if 名 in argv else 既定


def 指紋(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]


def 中身の指紋(d):
    """index.html と img/ の中身の指紋。絵だけを直した回も「直した」と数える（友だちの 2026-10-18 bath-step-over: 指摘が絵と md だけで、
    index.html の指紋が前と同じため「まだ直していない」と出し直しを止められた）"""
    h = hashlib.sha256(open(os.path.join(d, "index.html"), "rb").read())
    for 根, _, fs in sorted(os.walk(os.path.join(d, "img"))):
        for f in sorted(fs):
            q = os.path.join(根, f); h.update(os.path.relpath(q, d).encode()); h.update(open(q, "rb").read())
    return h.hexdigest()[:12]


def 決めた値の紙(記事):
    """記事のフォルダの決めた値の紙の名前（新しい名前が先。無ければ古い名前。どちらも無ければ新しい名前）"""
    for n in 決めた値の名:
        if os.path.exists(os.path.join(記事, n)):
            return n
    return 決めた値の名[0]


def 店か(記事):
    return os.path.exists(os.path.join(記事, "店の印.json"))


def 店の機械の検査(店):
    """店の機械の検査は pdp-tsukuru が持つ（友だちの 2026-10-19「店だけの物は pdp に入れる」）。
    ここは pdp-tsukuru の scripts/店の検査を回す.py を呼ぶだけ。検査の結果.md もそちらが書く。全部0なら True"""
    道 = os.path.join(PDP, "scripts", "店の検査を回す.py")
    if not os.path.exists(道):
        open(os.path.join(店, "検査の結果.md"), "w", encoding="utf-8").write(f"# 機械の検査の結果\n\n- pdp-tsukuru が無い: {道}\n")
        return False
    r = subprocess.run([sys.executable, 道, 店], capture_output=True, text=True, timeout=3600)
    return r.returncode == 0


def 店の決まり():
    """店を審査する時の決まり。pdp-tsukuru の references/ストア担当の審査.md の「## ストア担当の関門」と「## 審査の決まり」の2節をそのまま渡す
    （審査の決まりが「上の関門」を指すので両方。pdp-tsukuru の scripts/審査を回す.py と同じ渡し方）"""
    p = os.path.join(PDP, "references", "ストア担当の審査.md")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    節 = []
    for 名 in ("ストア担当の関門", "審査の決まり"):
        m = re.search(r"^## " + 名 + r"\s*$(.*?)(?=^## |\Z)", t, re.M | re.S)
        if m:
            節.append(f"【{名}】" + " ".join(l.strip() for l in m.group(1).splitlines() if l.strip()))
    return " ".join(節) or None


def 絵を並べる(記事, 束):
    """画像の置き場.md の絵を、番号つきで16枚ずつ並べた1枚（絵の一覧_<n>.jpg）にして束に置く。
    絵が多い店・記事で、審査役が1枚ずつ読んで途中で止まらないように、並べた1枚を先に渡す（友だちの 2026-10-18）"""
    md = os.path.join(記事, "画像の置き場.md")
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
        if not m or m.group(1) in 見た or not os.path.exists(os.path.join(記事, m.group(1))):
            continue
        見た.add(m.group(1)); 絵.append((c[0], m.group(1)))
    if not 絵:
        return []
    字 = None
    for f in ("~/Library/Fonts/NotoSansJP.ttf", "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"):
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
            im = Image.open(os.path.join(記事, f)).convert("RGB"); im.thumbnail((W - 8, W - 8))
            x, y = (i % 列) * W, (i // 列) * (W + 30)
            sh.paste(im, (x + 4, y + 4)); d.text((x + 6, y + W), f"#{番} {os.path.basename(f)[:28]}", fill="black", font=字)
        名 = f"絵の一覧_{k // (列 * 段) + 1}.jpg"
        sh.save(os.path.join(束, 名), quality=82); out.append(名)
    return out


def 記録(記事):
    p = os.path.join(記事, "審査の記録.jsonl")
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def 機械の検査(記事):
    """記事の検査・仕上がり検査・画像の置き方を今の index.html で回し、検査の結果.md に指紋（sha256 の頭12字）つきで書く。全部0なら True"""
    if 店か(記事):
        # 店（pdp-tsukuru が作った商品ページ）は記事の検査ではなく店の検査を回す（友だちの 2026-10-17: 記事の検査を店に当てて終了コード2で止まった）
        return 店の機械の検査(記事)
    html = os.path.join(記事, "index.html")
    移植表 = sorted(f for f in os.listdir(記事) if f.startswith("移植表") and f.endswith(".md"))
    結果 = []
    if not 移植表:
        結果.append(("記事の検査", 2, "移植表*.md が無い"))
    else:
        r = subprocess.run([sys.executable, os.path.join(ここ, "記事の検査.py"), os.path.join(記事, 移植表[0]), html], capture_output=True, text=True)
        結果.append(("記事の検査", r.returncode, (r.stdout + r.stderr).strip()))
    r = subprocess.run([sys.executable, os.path.join(ここ, "記事の仕上がり検査.py"), 記事], capture_output=True, text=True)
    結果.append(("記事の仕上がり検査", r.returncode, (r.stdout + r.stderr).strip()))
    引数の紙 = os.path.join(記事, "画像の置き方の引数.txt")
    if not os.path.exists(引数の紙):
        結果.append(("画像の置き方", 2, "画像の置き方の引数.txt が無い。1行目に参考の URL、2行目から --移植表 <移植表> などの引数を1つずつ書く（うちの記事は index.html を自動で渡す）"))
    else:
        a = [l.strip() for l in open(引数の紙, encoding="utf-8") if l.strip() and not l.startswith("#")]
        r = subprocess.run([sys.executable, os.path.join(ここ, "画像の置き方.py"), a[0], html] + a[1:], capture_output=True, text=True, cwd=記事, timeout=900)
        結果.append(("画像の置き方", r.returncode, (r.stdout + r.stderr).strip()))
    行 = ["# 機械の検査の結果（審査を回す.py が書いた。手で直さない）", "",
          "読む人: 編集長（審査のサブエージェント）と、記事を直す Claude。", "読む時: 審査の前。", "読まなくていい条件: なし。", "",
          f"- index.html の指紋: `{指紋(html)}`（この指紋の index.html で回した結果。index.html を変えたら無効）",
          f"- 回した時刻: {time.strftime('%Y-%m-%d %H:%M')}", ""]
    for 名, 終, 出 in 結果:
        行 += [f"## {名}: 終了コード {終}", "", "```", "\n".join(出.splitlines()[-25:]), "```", ""]
    open(os.path.join(記事, "検査の結果.md"), "w", encoding="utf-8").write("\n".join(行))
    return all(終 == 0 for _, 終, _ in 結果)


def 段たち(文):
    return set(re.findall(r"sec-\d+|段\s?\d+", 文))


def 束を作る(記事, 案件, 役):
    if not os.path.exists(os.path.join(記事, "index.html")):
        print("index.html が無い:", 記事); return 2
    前 = 記録(記事)
    回 = len(前) + 1
    if 前:
        d = 前[-1]
        # 直していない記事を出し直さない（元の道具の 2026-10-15 実測: 同じ記事を次の回に出し、同じ5件で落ちた）
        if d["指紋"] in (指紋(os.path.join(記事, "index.html")), 中身の指紋(記事)) and d["判定"] != "PASS":
            print(f"{d['回']}回目の判定（{d['判定']}）の後、index.html が変わっていない。審査_{d['回']}.md を直してから出す"); return 2
        if d["判定"] == "PASS" and not d["指摘"]:
            print(f"もう PASS（{d['回']}回目）。出し直さない"); return 0
        # 出す前の関門1: 前の回の FAIL を全部、同じ事を全体から探して直したか
        if d["判定"] == "FAIL":
            件 = len(d["指摘"])
            直し = os.path.join(記事, f"直し_{d['回']}.md")
            探した = sum(1 for l in open(直し, encoding="utf-8") if "探した語" in l) if os.path.exists(直し) else 0
            if 探した < 件:
                print(f"直し_{d['回']}.md に「探した語」の行が {探した} 行（{d['回']}回目の指摘は {件} 件）。指摘1件ごとに、名前・数字・場面の語を "
                      f"`grep -n <語> index.html 移植表*.md 報告.md 画像の置き場.md {決めた値の紙(記事)}` で全部探してそろえ、"
                      f"「探した語: <語>／見つかった所: <数>／全部そろえた」を書いてから出す"); return 2
    # 出す前の関門2: 機械の検査を今の index.html で回し、結果を指紋つきで書く
    if not 機械の検査(記事):
        print(f"機械の検査が落ちた。審査には出さない。{os.path.join(記事, '検査の結果.md')} を見て直す"); return 2
    束 = os.path.join(記事, f"審査_束_{回}")
    if os.path.isdir(束):
        shutil.rmtree(束)
    os.makedirs(束)
    名 = [f for f in 束に入れる if os.path.exists(os.path.join(記事, f))] + \
        sorted(f for f in os.listdir(記事) if (f.startswith("移植表") and f.endswith(".md")) or (f.startswith("見比べ") and f.endswith((".jpg", ".png"))))
    for f in (f"直し_{回 - 1}.md", f"照らし合わせ_{回 - 1}.txt"):
        if 回 > 1 and os.path.exists(os.path.join(記事, f)):
            名.append(f)
    for f in 名:
        shutil.copy2(os.path.join(記事, f), os.path.join(束, f))
    if os.path.isdir(os.path.join(記事, "img")):
        shutil.copytree(os.path.join(記事, "img"), os.path.join(束, "img"))
    名 = 絵を並べる(記事, 束) + 名
    役の文 = open(編集長の役, encoding="utf-8").read()
    出す先 = os.path.join(記事, f"判定_{回}.json")
    頼み = f"""# 審査の頼み {回}回目（{案件}）

あなたは「編集長」。記事を作った会話は知らない。作った役の言い分（報告.md の「通った」など）は信じず、渡した物と決まりだけで判定する。
記事は作らない・直さない。読むだけ。最後に1つのファイルだけを書く。

## あなたの役（{編集長の役} の全文）

{役の文}

## この仮ハーネスでの読み替え

- 「部屋」「JEV（判断の層）」「review-converge.mjs」は無い。ずれを1件ずつ、下の3つのどれかに自分で分ける。迷ったら「決定を変える」
  - 決定を変える: 直さないと記事の結論・約束・順位・事実が変わる。こちらの決め・本人の直しの台帳の行に反する。参考との差の検査が0でない。VSL のビジュアルが記事に入っている
  - 書き方: 直しても結論は変わらない表記のずれ。印、版の番号、言い回し、ファイル同士の写し違い、体裁
  - 本人の決まりに反する: 本人が指摘しないと決めた指摘（薬機法・景表法の言い換えの指摘、{決めた値の紙(記事)} に載っている値を「本物でない」と落とす指摘）。これは捨てる側
- 手順の 7 の画像の置き方の検査・機械の検査は、もう道具が回して `検査の結果.md` に書いてある。自分で走らせなくてよい（index.html の指紋を `shasum -a 256 index.html` の頭12字と照らす）
- 当てる決まり: {(店の決まり() if 店か(記事) else None) or 決まり.format(役=役, 知=記事の知識, 仮=仮)}

## 見る物

記事のフォルダ（読むだけ）: {記事}
この回の束（同じ物の写し）: {束}
束の中: {", ".join(名)}{"、img/" if os.path.isdir(os.path.join(記事, "img")) else ""}
前の回の審査: {", ".join(f"審査_{x['回']}.md（{x['判定']}）" for x in 前) or "なし（1回目）"}（記事のフォルダにある。前回○だった所も、もう一度全部見る）
画面で見る時は、共通 Chrome（surasura。CDP 9222）に自分のタブを1枚だけ開いて file:// で開き、幅1280 と 390 で見る。ほかのタブには触らない。終わったら自分のタブを閉じる。
画像は Read で開いて目で見る。

## 書く物（これだけ）

{出す先} に、次の形の JSON を1つ書く（UTF-8）。ずれは全部書く。1つ見つけて止めない。1件1行「どこが・何が・どう直すか」。

```json
{{"判定の元": "PASS か FAIL（あなたの見立て）",
  "ずれ": [{{"文": "<どこが・何が・どう直すか。段の番号（sec-3 や 段3）を必ず入れる>", "種類": "決定を変える|書き方|本人の決まりに反する"}}],
  "台帳の照らし": [{{"行": "<直しの台帳の行の文>", "守れた": true}}],
  "読んだ物": ["<実際に開いたファイル>"]}}
```

書いたら、返事は1行だけ: `判定_{回}.json を書いた（ずれ N 件・決定を変える N 件）`
"""
    open(os.path.join(束, f"頼み_{回}.md"), "w", encoding="utf-8").write(頼み)
    print(f"{回}回目の束を作った: {os.path.join(束, f'頼み_{回}.md')}")
    print(f"次: この頼みの全文を、新しいサブエージェント（毎回新しく呼ぶ。前の回のエージェントに続けて頼まない）に渡す。"
          f"終わったら `審査を回す.py {記事} {案件} --書く`")
    return 4


def 書く(記事, 案件):
    前 = 記録(記事)
    回 = len(前) + 1
    p = os.path.join(記事, f"判定_{回}.json")
    try:
        j = json.load(open(p, encoding="utf-8"))
        ずれ = [x for x in j["ずれ"] if x.get("文")]
    except Exception as e:
        print(f"判定_{回}.json が読めない: {e}"); return 2
    決定 = [x["文"] for x in ずれ if x.get("種類") not in ("書き方", "本人の決まりに反する")]
    書き方 = [x["文"] for x in ずれ if x.get("種類") == "書き方"]
    捨てた = [x["文"] for x in ずれ if x.get("種類") == "本人の決まりに反する"]
    判定 = "FAIL" if 決定 else "PASS"
    指摘 = 決定 + [f"[書き方・1回直したら再審査なしで次へ] {x}" for x in 書き方]
    前の段 = 段たち(" ".join(前[-1]["指摘"])) if 前 and 前[-1]["判定"] == "FAIL" else set()
    at = time.strftime("%Y-%m-%dT%H:%M")
    if 判定 == "PASS":
        if 指摘:
            行 = [f"# 編集長の審査 {回}回目（合格）の書き方の指摘（{at}・{案件}）", "", "読む人: この記事を直す Claude。",
                  "読む時: 合格の後、書き方の指摘を記事に入れる時。", "読まなくていい条件: なし。", "",
                  f"判定: PASS。下の {len(指摘)} 件は書き方の指摘。全部直し、直し_{回}.md に「探した語: <語>／見つかった所: <数>／全部そろえた」で書く。再審査には出さない。"
                  f"直した後は機械の検査だけ回す（`審査を回す.py <記事のフォルダ> {案件} --検査だけ` が終了コード0）。", ""]
            行 += [f"{i}. {x}" for i, x in enumerate(指摘, 1)]
        else:
            行 = [f"# 編集長の審査 {回}回目（合格）（{at}・{案件}）", "", "判定: PASS（指摘なし）。"]
    else:
        行 = [f"# 編集長の審査 {回}回目（{at}・{案件}）", "",
              "読む人: この記事を直す Claude。", "読む時: 直す前に全部。", "読まなくていい条件: なし。", "",
              f"判定: FAIL（{len(指摘)}件）。全部直して 直し_{回}.md に1行ずつ書き、もう一度 `審査を回す.py` を走らせる（機械の検査はこの道具が回す）。回数の上限は無い。", "",
              f"直す時は指摘1件ごとに、名前・数字・場面の語を `grep -n <語> index.html 移植表*.md 報告.md 画像の置き場.md {決めた値の紙(記事)}` で全部探してそろえる。"
              "直し_<回>.md の各行に「探した語: <語>／見つかった所: <数>／全部そろえた」を入れる。入っていないと道具は次の回を出さない。", ""]
        同じ = 0
        for i, x in enumerate(決定, 1):
            重 = 段たち(x) & 前の段
            同じ += bool(重)
            行.append(f"{i}. [決定を変える]{' [前の回と同じ所で落ちた: ' + '・'.join(sorted(重)) + '。記事だけでなく原因の手順か道具を直す]' if 重 else ''} {x}")
        for i, x in enumerate(書き方, len(決定) + 1):
            行.append(f"{i}. [書き方] {x}")
    if 捨てた:
        行 += ["", f"（本人の決まりに反するので捨てた指摘 {len(捨てた)} 件）"] + [f"- {x}" for x in 捨てた]
    open(os.path.join(記事, f"審査_{回}.md"), "w", encoding="utf-8").write("\n".join(行) + "\n")
    with open(os.path.join(記事, "審査の記録.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"回": 回, "at": at, "案件": 案件, "判定": 判定, "指摘": 指摘, "捨てた": 捨てた,
                            "指紋": 中身の指紋(記事)}, ensure_ascii=False) + "\n")
    if 判定 == "FAIL":
        print(f"FAIL（{回}回目・{len(指摘)}件）。{os.path.join(記事, f'審査_{回}.md')} を直してから、もう一度走らせる"); return 1
    if 指摘:
        print(f"PASS（{回}回目）。書き方の指摘 {len(指摘)} 件を 審査_{回}.md に書いた。直して --検査だけ を通すまで終わりではない"); return 3
    print(f"PASS（{回}回目）"); return 0


def main(argv):
    if len(argv) < 3:
        print(__doc__); return 2
    記事, 案件 = os.path.abspath(argv[1]), argv[2]
    if "--書く" in argv:
        return 書く(記事, 案件)
    if "--検査だけ" in argv:
        ok = 機械の検査(記事)
        print("機械の検査: " + ("全部0" if ok else "落ちた。検査の結果.md を見る")); return 0 if ok else 2
    return 束を作る(記事, 案件, 引数(argv, "--役", "記事ライター"))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
