#!/bin/bash
# 店の土台を1本コピーして、新しい店の作業場と「店の設計.md」「店の印.json」の殻を作る。
# 使い方: ./新規.sh <商品のフォルダ名> <店の型の短い名前>
#   例:   ./新規.sh <商品のフォルダ名> オファーがすぐ見える店
set -e
SHOHIN="$1"; KATA="$2"
{ [ -z "$SHOHIN" ] || [ -z "$KATA" ]; } && { echo "使い方: ./新規.sh <商品> <店の型>"; exit 1; }
case "$SHOHIN$KATA" in *[/\\\"\'\`]*|*..*) echo "商品名と型に / \\ \" ' \` .. は使えない: $SHOHIN / $KATA"; exit 1;; esac
# 商品の書類（店の設計.md）と作業場を置く場所。2026-10-19 Seiyo の新ハーネス：既定は newec_harness/<商品名>/08_店/。EC_ROOT で替えられる（EC_ROOT の時は無ければ作る。友だちの c906a23）
if [ -n "$EC_ROOT" ]; then VAULT="$EC_ROOT"; mkdir -p "$VAULT"; else VAULT="$HOME/Desktop/claude code/newec_harness"; [ -d "$VAULT" ] || { echo "商品の置き場が無い: $VAULT（EC_ROOT で渡す）"; exit 1; }; fi
HERE0="$(cd "$(dirname "$0")" && pwd)"
DODAI="$HERE0/../references/土台.md"
[ -f "$DODAI" ] || { echo "土台が無い: $DODAI"; exit 2; }
export SHOHIN KATA DODAI
OUT="$VAULT/$SHOHIN/08_店/01_${SHOHIN}_店_${KATA}_v1"
MD="$VAULT/$SHOHIN/08_店"
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -e "$OUT/index.html" ] && { echo "もうある: $OUT（消さない。版を上げるなら v2 のフォルダ名で）"; exit 1; }
mkdir -p "$OUT" "$MD"
node "$HERE/土台を作る.mjs" "$OUT"
DATE=$(date +%Y-%m-%d)
[ -e "$MD/店の設計.md" ] || cat > "$MD/店の設計.md" <<EOF
# ${SHOHIN}｜店の設計（${KATA}・v1・${DATE}）

読む人: この店を作る・直す人と編集長。
読む時: index.html を触る前。
読まなくていい条件: 別の版の店をさわる回。

土台: \`pdp-tsukuru/references/土台.md\`。実物: \`$OUT/index.html\`。写真の比べる元: 段ごとに土台の説明の「段ごとの参考」の表（\`pdp-tsukuru/scripts/段ごとの画像の検査.py\`）。

## 0 商品の形（仕入先の写真で確かめた形。文と絵はこの言葉だけで商品の形を言う）

| 部品・形 | 数・位置・向き | どの写真のどこで見たか（商品写真/ のファイル名と写真の中の場所） |
|---|---|---|
| | | |

## 1 来た人（記事の移植表の「見終わった人の状態」をそのまま写す）

| 欄 | 中身 | 出どころ（記事の移植表の行） |
|---|---|---|
| どの記事から | | |
| 段階 | | |
| 信じた事 | | |
| 残った疑い | | |
| 今の気持ち | | |

## 2 店の型

| 欄 | 中身 |
|---|---|
| 型 | $KATA |
| 理由（残った疑いの中で件数が最多の物） | |

## 2.5 見た目の方向（references/見た目の方向.md の手順で決める）

| 欄 | 中身 | 客の資料のどの行から |
|---|---|---|
| 方向（1文） | | |
| 色（地・強調・ボタン） | | |
| 書体（見出し・本文） | | |
| 角と写真の調子 | | |
| 別の AI に当てさせた結果 | | |

## 3 狙う数字

| 欄 | 中身 |
|---|---|
| 最初に動かす数字（1つ） | |
| 守りの線 | 注文1件の利益 |

## 4 変数の値（土台の「変わる ◯」の行を全部。空欄・出どころ無しは0にする）

| 変数 | 値 | 出どころ | 理由（1行） |
|---|---|---|---|
$(python3 - <<'PY'
import os,re,sys
t=open(os.environ["DODAI"],encoding="utf-8").read()
m=re.search(r"^## 変数.*?$",t,re.M); body=t[m.end():].split("\n## ")[0] if m else ""
n=0
for l in body.splitlines():
    c=[x.strip() for x in l.strip().strip("|").split("|")]
    if len(c)==6 and c[2]=="◯": print(f"| {c[0]} | | | |"); n+=1
if n==0: print("土台の「## 変数」に ◯ の行が 0", file=sys.stderr); sys.exit(3)
PY
)

## 5 絵（段ごと。参考の絵が起こす気持ち → うちで起こす絵 → ある／作る）

| 段 | 参考の絵が起こす気持ち | うちで起こす絵 | ある／作る | 縦÷横 |
|---|---|---|---|---|

## 6 3つの面（広告・記事・商品の事実の数字を並べ、店に入れる数字を1つずつ決める）

| 数字 | 広告 | 記事 | 商品の事実 | 店に入れる数字 |
|---|---|---|---|---|
| 評価と件数 | | | | |
| 配送日数 | | | | |
| 値段 | | | | |
| 保証日数 | | | | |

## 7 わざと変える物の一覧（これに無い差が0になったら終わり）

-

EOF
grep -q "^| 題の型 | | | |$" "$MD/店の設計.md" || { echo "店の設計.md の 4 に変数の行が入らなかった（土台を読めていない）"; exit 3; }
[ -e "$OUT/店の印.json" ] || OUT="$OUT" DATE="$DATE" MDFILE="$MD/店の設計.md" python3 - <<'PY'
import json,os,re,sys
t=open(os.environ["DODAI"],encoding="utf-8").read()
m=re.search(r"^## 変数.*?$",t,re.M); body=t[m.end():].split("\n## ")[0] if m else ""
keys=[c[0] for c in ([x.strip() for x in l.strip().strip("|").split("|")] for l in body.splitlines()) if len(c)==6 and c[2]=="◯"]
if not keys: print("土台の ◯ の行が 0", file=sys.stderr); sys.exit(3)
json.dump({"商品":os.environ["SHOHIN"],"店の型":os.environ["KATA"],"版":1,"日付":os.environ["DATE"],"設計":os.environ["MDFILE"],"値":{k:"" for k in keys}},open(os.path.join(os.environ["OUT"],"店の印.json"),"w"),ensure_ascii=False,indent=1)
PY
echo "作った:"
echo "  店:   $OUT/index.html"
echo "  設計: $MD/店の設計.md"
echo "  印:   $OUT/店の印.json"
mkdir -p "$OUT/商品写真" "$OUT/_gen"
echo "  商品写真: $OUT/商品写真/（照合.md もここ）"
echo "次: SKILL.md の手順3から"
