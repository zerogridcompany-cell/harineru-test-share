#!/usr/bin/env python3
"""店のページ（index.html）と画像の置き場.md だけを見て、本人に出す前に機械で落とす（2026-10-18 本人「数える物は文ではなく道具に」）。

使い方: python3 店の仕上がり検査.py <店のフォルダ>
終了コード: 0 全部通った / 1 落ちた所がある（行ごとに出す） / 2 読めなかった

見る物（references/デザインの参考.md の「写真と部品の変数」のうち、機械で数えられる物。SKILL.md の最終確認 F の番号）:
  F2 画像の置き場.md の1行目（1枚目の写真）の「主役」が 商品 か 手と商品 で、「文字」が ○
  F3 画像の置き場.md に「主役」が 札 の行（保証の札の絵）が2種以上（「作った画像」で数える）
  F4 最初の画面（id="buy" の中）のボタン（class に btn を持つ a・button）が1つで、その文に値段（円か¥）がある（2段）。
     段ごとの CTA（class に btn と sway を持つ物）の文が全部同じ
  F5 支払いロゴ（class="pay" の中）が文字の札でない（img か svg がある）
  F6 「営業日」が画面に出るのは、ボタンの下の灰の1行（class="sub" か "gline"）と FAQ の答え（details の中・1回まで）だけ。
     最初の画面のボタンの下の1行に1回ある
  F7 声のカード（class="people" の段の class="card"）が全部 img を持つ
  F8 CTA 帯の上の行（class="stockline"）に「営業日」が無い。「在庫」は data-zaiko（在庫の実数）がある時だけ
  F9 画面の字に絵文字（U+1F300〜1FAFF）が0（アイコンは線の絵）・class="ico i-◯◯" の名前が CSS にある
  F10 .wrap の左右の padding が 15〜16px（参考 15・土台 16。中身の幅 358〜360）
  F4 追記: 買うボタン（.btn.pri）の最後の box-shadow が none でない、または CTA（.sway / .final .btn.pri）の :after に矢印が残っていたら落とす
  F7 追記: レビュー一覧の JS（var REV = [...]）がある時は、各行の5番目（写真）が null の件数を数える
  F11 最初の画面の h1 が20字以内（空白・記号の飾りを除く）で、問いの文（？）でない（見出しの指示文.md）
  F12 空の型の名残: 〔札〕が0・画面の文のダッシュ（—）が0・この店に無い 直し_<回>.md を指すコメントが0・打ち消し線と OFF が0・仮の四角（_todo/）と札の絵（img/_kata/）が0・
     画面の字にここちドライ／bath-step-over の商品名が0・noindex がある・フォルダに 決めた値.md がある
2026-10-18 足した: F4 追記・F7 追記・F11（今の店を新しい検査にかけて、本人の言った事②③⑤を拾えていなかったため）
"""
import os, re, sys
from html.parser import HTMLParser

VOID = {"img", "br", "hr", "input", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track", "param"}


class 木(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.棚 = []          # 開いている要素 [(tag, attrs)]
        self.字 = []          # (text, 祖先の写し)
        self.要素 = []        # (tag, attrs, 祖先の写し, 番号)
        self.飛ばす = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag in ("script", "style", "noscript", "template"):
            self.飛ばす += 1
        if self.飛ばす:
            if tag in ("script", "style", "noscript", "template"):
                self.棚.append((tag, a))
            return
        self.要素.append((tag, a, list(self.棚), len(self.要素)))
        if tag not in VOID:
            self.棚.append((tag, a))

    def handle_startendtag(self, tag, attrs):
        if self.飛ばす:
            return
        self.要素.append((tag, {k: (v or "") for k, v in attrs}, list(self.棚), len(self.要素)))

    def handle_endtag(self, tag):
        for i in range(len(self.棚) - 1, -1, -1):
            if self.棚[i][0] == tag:
                del self.棚[i:]
                break
        if tag in ("script", "style", "noscript", "template") and self.飛ばす:
            self.飛ばす -= 1

    def handle_data(self, d):
        if self.飛ばす or not d.strip():
            return
        self.字.append((d, list(self.棚)))


def 組(a):
    return a.get("class", "").split()


def 中(祖先, cls=None, id_=None, tag=None):
    for t, a in 祖先:
        if (cls is None or cls in 組(a)) and (id_ is None or a.get("id") == id_) and (tag is None or t == tag):
            return True
    return False


def 表を読む(md):
    """画像の置き場.md の表（「主役」列を持つ物）を [{列名: 値}] で返す。無ければ None"""
    行 = open(md, encoding="utf-8").read().splitlines()
    for i, l in enumerate(行):
        if l.startswith("|") and "主役" in l:
            名 = [x.strip() for x in l.strip().strip("|").split("|")]
            out = []
            for m in 行[i + 2:]:
                if not m.startswith("|"):
                    break
                c = [x.strip() for x in m.strip().strip("|").split("|")]
                if len(c) == len(名):
                    out.append(dict(zip(名, c)))
            return out
    return None


def 写真の札(店):  # F2・F3
    md = os.path.join(店, "画像の置き場.md")
    if not os.path.exists(md):
        return ["F2 画像の置き場.md が無い（1枚目の写真と保証の札を数えられない）"]
    表 = 表を読む(md)
    if 表 is None:
        return ["F2 画像の置き場.md に「主役」列が無い（土台の説明の「主役の言葉」から1つずつ書く。「文字」列に ○×）"]
    語 = 主役の言葉()
    外れ = sorted({r.get("主役", "") for r in 表 if r.get("主役", "") and 語 and r.get("主役", "") not in 語})
    if 外れ:
        return [f"F2 画像の置き場.md の「主役」に、土台の説明の「主役の言葉」に無い言葉がある: {'・'.join(外れ)}"]
    見た, 商品, 顔, 文字 = set(), 0, 0, 0
    for r in 表:
        主 = r.get("主役", "")
        if 主 not in ("商品", "手と商品", "人の体と商品", "人の体", "人の顔", "人の顔と商品", "場面", "物"):
            continue
        鍵 = (r.get("作った画像", "") or r.get("元の画像", "")).split("（")[0].split()[0:1]
        鍵 = 鍵[0] if 鍵 else id(r)
        if 鍵 in 見た:
            continue
        見た.add(鍵)
        商品 += 主 in ("商品", "手と商品")
        顔 += 主 == "人の顔"
        文字 += r.get("文字", "").startswith("○")
    n = len(見た)
    bad = []
    写 = [r for r in 表 if r.get("主役", "") in ("商品", "手と商品", "人の体と商品", "人の体", "人の顔", "人の顔と商品", "場面", "物")]
    if 写 and not (写[0].get("主役") in ("商品", "手と商品") and 写[0].get("文字", "").startswith("○")):
        bad.append("F2 1枚目の写真の主役が商品でないか、写真の中に文字（見出し・吹き出し3つ・保証の札）が無い")
    札 = {(r.get("作った画像", "") or r.get("元の画像", "")).split("（")[0].strip() for r in 表 if r.get("主役", "") == "札"}
    if len(札) < 2:
        bad.append(f"F3 保証の札の絵が {len(札)}種（写真の中用と段の中用の2種を絵で作り、主役 札 で書く）")
    return bad


def 頁(店, s):
    t = 木()
    t.feed(s)
    bad = []
    # F4 最初の画面のボタン
    btn = [(a, i) for tag, a, 祖, i in t.要素 if tag in ("a", "button") and "btn" in 組(a) and 中(祖, id_="buy")]
    if not any(True for tag, a, 祖, i in t.要素 if a.get("id") == "buy"):
        bad.append("F4 最初の画面（id=\"buy\"）が見つからない")
    elif len(btn) != 1:
        bad.append(f"F4 最初の画面のボタンが {len(btn)}つ（1つにする。2段: 言葉＋値段）")
    else:
        a0, i0 = btn[0]
        字 = "".join(d for d, 祖 in t.字 if any(x[1] is a0 for x in 祖))
        if not re.search(r"[¥￥]|円", 字):
            bad.append(f"F4 最初の画面のボタンに値段が無い（2段にする。今の文: {字.strip()[:30]}）")
    cta = {}
    for tag, a, 祖, i in t.要素:
        if tag in ("a", "button") and "btn" in 組(a) and "sway" in 組(a):
            cta["".join(d for d, 祖2 in t.字 if any(x[1] is a for x in 祖2)).strip()] = 1
    if len(cta) > 1:
        bad.append(f"F4 段ごとの CTA の言葉が {len(cta)}種（全部同じ言葉にする）: {' / '.join(list(cta)[:3])}")
    絵 = re.findall("[\U0001F300-\U0001FAFF]", "".join(d for d, _ in t.字))
    if 絵:
        bad.append(f"F9 絵文字が {len(絵)}字（線の絵のアイコンに替える）: {''.join(sorted(set(絵)))[:10]}")
    使うアイコン = set(re.findall(r'class="ico (i-[\w-]+)"', s))
    無いアイコン = sorted(x for x in 使うアイコン if not re.search(r'\.' + re.escape(x) + r'\b', s))
    if 無いアイコン:
        bad.append(f"F9 線の絵の定義が無いアイコンの名前: {'・'.join(無いアイコン)}（CSS にある .i-◯◯ の名前を使う）")
    m = re.search(r"\.wrap\{[^}]*padding:\s*0\s+(\d+)px", s)
    if m and not 15 <= int(m.group(1)) <= 16:
        bad.append(f"F10 .wrap の左右の余白が {m.group(1)}px（15〜16px にする）")
    # F4 追記: 影と矢印（CSS の最後の宣言で見る）
    css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", s, re.S))
    影 = None
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        sels = [x.strip() for x in sel.split(",")]
        if any(re.fullmatch(r"(#\w+\s+)?\.btn\.pri", x) for x in sels):
            m2 = re.findall(r"box-shadow:\s*([^;]+)", body)
            if m2:
                影 = m2[-1].strip()
    if 影 and 影 != "none":
        bad.append(f"F4 買うボタンに影が残っている（box-shadow: {影[:40]}）。無地・影なしにする")
    矢 = None
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(r"(\.sway|\.final \.btn\.pri):after", sel):
            if re.search(r"content:\s*none|display:\s*none", body):
                矢 = None
            elif "content" in body:
                矢 = sel.strip()[:40]
    if 矢:
        bad.append(f"F4 CTA の右に矢印が残っている（{矢}）。矢印なしにする")
    # F11 h1
    h1 = [a for tag, a, 祖, i in t.要素 if tag == "h1"]
    if h1:
        字 = "".join(d for d, 祖 in t.字 if any(x[1] is h1[0] for x in 祖))
        数 = len(re.sub(r"[\s「」『』“”\"、。，．・！!]", "", 字))
        if 数 > 20:
            bad.append(f"F11 h1 が {数}字（20字以内にする。見出しの指示文.md）: {字.strip()[:30]}")
        if re.search(r"[？?]", 字):
            bad.append(f"F11 h1 が問いの文（疑いへの答えは最初の画面のすぐ下の段が持つ）: {字.strip()[:30]}")
    # F7 追記: レビュー一覧の写真
    m3 = re.search(r"var REV\s*=\s*\[(.*?)\n\];", s, re.S)
    if m3:
        行 = [l for l in m3.group(1).splitlines() if l.strip().startswith("[")]
        無写 = [l for l in 行 if re.search(r",\s*null\s*,\s*\d\s*\]\s*,?\s*$", l)]
        if 無写:
            bad.append(f"F7 写真の無いレビューが {len(無写)}/{len(行)} 件（レビュー一覧の REV の5番目に写真を入れる）")
    # F5 支払いロゴ
    for tag, a, 祖, i in t.要素:
        if "pay" in 組(a):
            子 = [x for x in t.要素 if any(y[1] is a for y in x[2])]
            if not any(x[0] in ("img", "svg") for x in 子):
                bad.append("F5 支払いロゴが文字の札（本物の色のロゴの img か svg にする）")
    # F6 営業日 / F8 CTA 帯の上
    # 2026-10-20 うち（Seiyo の新ハーネス）で足した: 届く日数は「営業日」の語のほかに「2〜4日でお届け／届きます」の書き方も同じに数える
    #（記事の決めた値が「2〜4日」の時、店だけ「営業日」に言い換えると記事と食い違うため。後頭部ほぐし台の通しテストで落ちた）
    届く = re.compile(r"営業日|\d+\s*[〜~～\-]\s*\d+\s*日で(?:お)?届")
    最初 = 0
    faq = 0
    for d, 祖 in t.字:
        if "stockline" in [c for _, a in 祖 for c in 組(a)]:
            if 届く.search(d):
                bad.append(f"F8 CTA 帯の上の行に届く日数: {d.strip()[:40]}")
            if "在庫" in d and not any("data-zaiko" in a for _, a in 祖):
                bad.append(f"F8 CTA 帯の上に実数の無い在庫の行: {d.strip()[:40]}（data-zaiko が無い）")
            continue
        if not 届く.search(d):
            continue
        if 中(祖, cls="sub") or 中(祖, cls="gline"):
            最初 += 中(祖, id_="buy")
            continue
        if 中(祖, tag="details"):
            faq += 1
            if faq <= 1:
                continue
        bad.append(f"F6 「営業日」がボタンの下の灰の1行と FAQ の答えの外にある: {d.strip()[:40]}")
    if 最初 < 1:
        bad.append("F6 最初の画面のボタンの下の灰の1行（class=\"sub\"）に届く日数が無い（保証・送料無料と同じ行に入れる）")
    # F7 声のカード
    カード = [(a, i) for tag, a, 祖, i in t.要素 if "card" in 組(a) and 中(祖, cls="people")]
    if not カード:
        bad.append("F7 声のカード（class=\"people\" の中の class=\"card\"）が見つからない")
    無し = [i for a, i in カード if not any(x[0] == "img" and any(y[1] is a for y in x[2]) for x in t.要素)]
    if 無し:
        bad.append(f"F7 写真の無い声のカードが {len(無し)}/{len(カード)} 枚（全部に「その家で撮った」風の写真を付ける）")
    return bad


def 主役の言葉():
    """主役の言葉の正本は references/土台.md の「主役の言葉」の1行。（）の説明を外して返す"""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "土台.md")
    m = re.search(r"^主役の言葉[^:：]*[:：](.*?)。\s*文字", open(p, encoding="utf-8").read(), re.M)
    return {re.sub(r"（.*?）", "", x).strip() for x in m.group(1).split("／")} if m else set()


def 名残(店, s):
    bad = []
    本文 = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->", "", s, flags=re.S)
    札 = re.findall(r"〔[^〕]{0,20}〕", s)
    if 札:
        bad.append(f"F12 空の型の札が {len(札)} 個残っている（例: {'・'.join(sorted(set(札))[:5])}）")
    if re.search(r"line-through|<del\b|<s>", 本文) or "OFF" in 本文:
        bad.append("F12 割引の打ち消し線か OFF がある（値段は割引なし・いちばん人気・1日あたり）")
    if "—" in re.sub(r"<[^>]+>", " ", 本文):
        bad.append(f"F12 画面の文にダッシュ（—）が {re.sub(r'<[^>]+>', ' ', 本文).count('—')} 個ある（読点か句点で言い直す）")
    if "img/_kata/" in s:
        bad.append(f"F12 空の型の札の絵（img/_kata/）が {s.count('img/_kata/')} か所（手順8の絵の名前を指す）")
    if "_todo/" in s:
        bad.append(f"F12 仮の四角（img/_todo/）が {s.count('_todo/')} か所（絵は全部作る）")
    字 = re.sub(r"<[^>]+>", " ", 本文)
    for w, 商品 in (("ここちドライ", "ここちドライ"), ("ラクマタギ", "bath-step-over")):
        if w in 字 and 商品 not in os.path.abspath(店):
            bad.append(f"F12 画面の字に別の商品の名前「{w}」が残っている")
    # 空の型や別の店の直しの記録（コメント）が残っていないか。この店のフォルダに無い 直し_<回>.md を指すコメントを落とす
    for m in re.finditer(r"<!--[^>]*?(直し_(\d+)\.md)[^>]*?-->", s):
        if not os.path.exists(os.path.join(店, m.group(1))):
            bad.append(f"F12 この店に無い {m.group(1)} を指すコメントが残っている（空の型か別の店の記録）: {m.group(0)[:60]}")

    if "noindex" not in s:
        bad.append("F12 noindex が無い")
    if not os.path.exists(os.path.join(店, "決めた値.md")):
        bad.append("F12 決めた値.md が無い（Claude が決めた数字・人・声を書く）")
    return bad


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    店 = argv[1] if os.path.isdir(argv[1]) else os.path.dirname(os.path.abspath(argv[1]))
    try:
        s = open(os.path.join(店, "index.html"), encoding="utf-8", errors="ignore").read()
    except Exception as e:
        print(f"読めなかった: {e}")
        return 2
    bad = 写真の札(店) + 頁(店, s) + 名残(店, s)
    if bad:
        数 = {}
        for x in bad:
            数[x] = 数.get(x, 0) + 1
        print("\n".join("- " + x + (f"（×{n}か所）" if n > 1 else "") for x, n in 数.items()))
        return 1
    print("通った")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
