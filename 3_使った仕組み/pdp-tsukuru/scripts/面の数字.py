#!/usr/bin/env python3
"""--context を付けなければ契約なしで回る（必須の数字 評価・件数・保証日数は店だけに求め、広告・記事は出ている欄だけ比べる）。ec-harness では --context <job.json> --config <brands.json> を付ける。
結果はJSON。status=executableは検査材料の準備完了で、配信・公開の承認ではない。
旧資料のURLは実行前にブランド配下の版付きローカルartifactへ保存する。

旧入力形式の説明（上記の契約が優先）:
広告・記事・店の3つの面から、客が比べる数字を取って並べ、違っていたら落とす。2026-10-02 版。

使い方: python3 面の数字.py --広告 <文字のファイル>... --記事 <URL|file> --店 <URL|file>
  広告の文字は、本文・見出しを貼ったテキストか、`広告の中身.py` が出した文字起こし（.txt）。
  どの面も省略できる（あるものだけ並べる）。
  店直行（記事を通らずに店へ来る広告）は --記事なし を付ける。広告と店の2面で比べる（2026-10-18 本人）。

取る数字（日本語の決まった書き方だけ。取れなかった欄は「—」で、0とは書かない）:
  評価       4.7 / 4.8 など、★や「評価」の近くの小数1桁
  件数       「2,431件」「2431件のレビュー」の件数
  配送日数   「2〜4営業日」「5-8日」
  保証日数   「60日返金」「60日間の保証」
  値段       「12,800円」「¥12,800」（並べるだけ。記事は他社の値段も書くので落とす条件にしない）

落とす物（1つでもあれば終了コード1）:
  評価・件数・配送日数・保証日数で、2つ以上の面に出ていて値が違う物
どれに合わせるかは本人が決める。この道具は直さない。
"""
import hashlib, html as htmllib, os, re, subprocess, sys, time

ここ = os.path.dirname(os.path.abspath(__file__))

CACHE = os.path.expanduser("~/.cache/ec-harness/面の数字")


def 取る(src):
    """URL ならブラウザで開いて（1回120秒まで）3回まで取り直し・10分キャッシュ。ファイルならそのまま読む。"""
    if not re.match(r"https?://", src):
        return open(src, encoding="utf-8", errors="ignore").read()
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, hashlib.md5(src.encode()).hexdigest())
    if os.path.exists(p) and time.time() - os.path.getmtime(p) < 600:
        return open(p, encoding="utf-8").read()
    最後 = None
    for i in range(3):
        try:
            # 店は JS で転送・後から描くので、ブラウザで開いた後の文字を取る
            r = subprocess.run(["node", os.path.join(ここ, "開いた文字.mjs"), src], capture_output=True, text=True, timeout=120)
            if r.returncode != 0 or len(r.stdout.strip()) < 50:
                raise RuntimeError((r.stderr or "文字が取れない")[-200:])
            文 = r.stdout
            tmp = p + ".tmp"
            open(tmp, "w", encoding="utf-8").write(文)
            os.replace(tmp, p)
            return 文
        except Exception as e:
            最後 = e
            time.sleep(2 * (i + 1))
    sys.exit(f"取れなかった（合格でも不合格でもない）: {src} {最後}")


def 文字だけ(文):
    文 = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", 文)
    文 = re.sub(r"(?s)<[^>]+>", " ", 文)
    return re.sub(r"\s+", " ", htmllib.unescape(文))


def 数字を取る(文):
    t = 文字だけ(文) if "<" in 文 else 文
    t = t.replace("～", "〜").replace("~", "〜")
    out = {}
    評価 = re.findall(r"(?:★|評価|星)\s*([1-5]\.\d)|([1-5]\.\d)\s*(?=/\s*5|点|★|高評価|[｜|]\s*[\d,]+\s*件|[（(][\d,]+\s*件)", t)
    out["評価"] = sorted({a or b for a, b in 評価})
    out["件数"] = sorted({x.replace(",", "") for x in re.findall(r"([\d,]{2,})\s*件(?:の(?:レビュー|口コミ|評価)|のお客様)?", t)
                          if re.search(re.escape(x) + r"\s*件\s*の?(?:レビュー|口コミ|評価)", t)}, key=int)
    out["配送日数"] = sorted(set(re.sub(r"\s", "", m) for m in re.findall(r"(\d+\s*[〜\-]\s*\d+)\s*(?:営業)?日(?:で|以内に)?(?:お届け|発送|到着|届)", t)))
    out["保証日数"] = sorted(set(re.findall(r"(\d+)\s*日(?:間)?(?:の)?(?:全額)?(?:返金|返品|保証)", t)), key=int)
    out["値段"] = sorted({x.replace(",", "") for x in re.findall(r"([\d,]{3,})\s*円|[¥￥]\s*([\d,]{3,})", t) for x in [x[0] or x[1]]}, key=int)
    return out


def main(argv):
    面 = {"広告": [], "記事": [], "店": []}
    今 = None
    記事なし = False
    for a in argv[1:]:
        if a == "--記事なし":
            記事なし = True
            continue
        if a in ("--広告", "--記事", "--店"):
            今 = a[2:]
            continue
        if 今 is None:
            sys.exit(__doc__)
        面[今].append(a)
    if not any(面.values()):
        sys.exit(__doc__)
    取れた = {k: 数字を取る("\n".join(取る(s) for s in v)) for k, v in 面.items() if v}

    欄たち = ["評価", "件数", "配送日数", "保証日数", "値段"]
    print("| 欄 | " + " | ".join(取れた) + " |")
    print("|---|" + "---|" * len(取れた))
    for 欄 in 欄たち:
        print(f"| {欄} | " + " | ".join(" / ".join(取れた[k][欄]) or "—" for k in 取れた) + " |")

    落 = []
    for 欄 in 欄たち[:4]:
        出た = {k: tuple(取れた[k][欄]) for k in 取れた if 取れた[k][欄]}
        if len(set(出た.values())) > 1:
            落.append(f"{欄}が面で違う: " + "／".join(f"{k} {' / '.join(v)}" for k, v in 出た.items()))
    if 記事なし:
        if 面["記事"]: 落.append("--記事なし と --記事 は一緒に使えない")
        elif set(取れた) != {"広告", "店"}: 落.append("店直行は広告・店の2面が必要")
    elif len(取れた) != 3: 落.append("広告・記事・店の3面が必要")
    必須の面 = set(取れた)
    try:
        from 検査契約 import CURRENT_JOB, CURRENT_CONFIG
        必須 = (CURRENT_JOB.get("evidence") or {}).get("required_number_fields") or CURRENT_CONFIG.get("required_number_fields")
    except ImportError:   # 契約なし（pdp-tsukuru の中で回す時）: 必須の数字は店だけに求める。広告・記事は出ている欄だけ比べる
        必須 = ["評価", "件数", "保証日数"]; 必須の面 = {"店"} & set(取れた)
    if not isinstance(必須,list) or not 必須 or any(k not in 欄たち for k in 必須):
        sys.exit("この案件の必要な数字欄を required_number_fields に明示する")
    for 面名, 値 in 取れた.items():
        if 面名 not in 必須の面: continue
        for 欄 in 必須:
            if not 値[欄]: 落.append(f"{面名}: 必須数字 {欄} が取れない")
    if 落:
        print(f"\n落ちた {len(落)}件（どれに合わせるかは本人が決める）")
        for x in 落:
            print("  " + x)
        sys.exit(1)
    print("\n通った（2つ以上の面に出た数字は全部同じ）")


if __name__ == "__main__":
    if "--context" in sys.argv:   # ec-harness の中から案件の契約つきで呼ばれた時
        from 検査契約 import cli
        sys.exit(cli("数字", lambda args,job,cfg: main(args), sys.argv))
    main(sys.argv)
