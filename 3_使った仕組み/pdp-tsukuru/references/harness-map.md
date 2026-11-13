# harness-map — pdp-tsukuru の入力・道具を、Seiyo の新ハーネスに読み替える表（2026-10-20。c906a23 の版。前は afb72a3）

友だちのスキル（リポジトリ `tokunaritakakura-code/pdp-tsukuru`。写した版 c906a23〈2026-10-20〉。前の写しは afb72a3〈2026-10-19 18:01〉）は、10/19 に**土台・検査の道具・ストア担当の審査の決まりを全部スキルの中へ入れた**（友だち「git の情報だけで pdp が動くようにしたい」）。だから、うちで足りない物はもう無い。残る違いは「商品の資料をどこから読むか」と「作業場をどこに作るか」だけで、それをこの表で読み替える。うちでは商品の事実は `newec_harness/<商品名>/` の Markdown にあるので、**そこから渡す**（Seiyo「俺らの Markdown を参照して作らせた方が互換性は良くなる」）。SKILL.md の手順はそのまま。

## 1. 入力（友だちの物 → うちの物）
| 友だちの SKILL.md が要る物 | うちのどこから | 項目 |
|---|---|---|
| 本人の決めたこと `$EC_ROOT/決めたこと.md` | `~/.agents/skills/ec-ad-ops/references/article/決めたこと.md`（友だちの決めの写し）。**うちの決め `ec-ad-ops/references/article.md` が上**（VSL のビジュアルを使わない・画像は Codex・公開は指示の時だけ） | — |
| 商品の事実 `ec/<商品>/product.md`（値段・原価・サイズ・保証日数・届く日数・在庫・評価と件数・仕組み・寸法・特長・付く面の条件・セット・色の数） | `00_入口.md`（呼び名・ブランド・売値・セット・仕入れの日数）・`01_商品理解の基盤/A_商品の事実.md`（一言で・仕組み・A-3 仕様〈寸法・素材・色・同梱〉・A-4 使い方・A-5 お手入れ・A-6 使えない人）・`02_損益分岐.md`（売値・原価・セットごとの利益）・`E_強みと唯一性.md`（特長）・`05_原稿の決まり.md`（結果の言い切りの上限・言わない事）。保証の日数は `ec-ad-ops/references/store-legal.md`（30日）。評価と件数は作らない（無ければ段ごと出さない。`決めた値.md` に理由） | 店の設計 4・6 |
| 客の資料（年代・性別・暮らし・声） | `01_商品理解の基盤/K_ペルソナ/<アングル>_<呼び名>.md`（その記事の動画の依頼票のペルソナ。K-1 だれか・K-5 口ぐせ・K-6 こわい事・K-8 こうなりたい）と `B_市場と悩みの地図.md` ④（原文） | 見た目の方向（2.5） |
| 記事の `index.html` と `01 移植表.md` の「見終わった人の状態」（どの記事から・段階・信じた事・残った疑い・今の気持ち） | `07_納品/記事/<名前>/index.html` と、同じフォルダの移植表（記事の道の手順3。`ec-ad-ops/references/article/15の対応表.md` 2章の6つの欄） | 店の設計 1 |
| 店直行の `VSLの塗り.md` | `08_店/VSLの塗り.md`（手順1で、台本の引き継ぎ票〈`vsl-script/references/記事と分ける.md` 5章〉と文字起こしから、15の対応表 2章のとおりに塗る） | 店の設計 1 |
| ブランドの色 `ec/<商品>/_入口.md` | `05_原稿の決まり.md` か `00_入口.md` に色の指定があればそれ。無ければ 2.5 で決める | 店の設計 2.5 |
| 商品写真（仕入先の商品欄の画像と `商品写真/照合.md`） | `00_入口.md` の仕入れ先の URL と `~/newec-dashboard/products/<id>/supplier/` の画像。照合は SKILL.md の手順7のとおり `08_店/<店>/商品写真/照合.md` | 店の設計 5 |
| 広告の文字（面の数字の「広告」） | その記事につながる広告の原稿（`06_原稿/<pack>/<票>/台本.md` の数字、静止画の `07_納品/Static Ads/…/ヘッドライン.txt`・`本文.txt`）。`scripts/面の数字.py --広告 <txt> --記事 <URL|file> --店 <URL|file>` に渡す | 店の設計 6 |

## 2. 置き場（友だちの物 → うちの物）
| 友だち | うち |
|---|---|
| `~/Desktop/ec/<商品>/09 店/01 <商品>_店_<型>_v1/` | `newec_harness/<商品名>/08_店/01_<商品名>_店_<型>_v1/`（`新規.sh` が作る。`EC_ROOT` で替えられる。既定 newec_harness） |
| `ec/<商品>/09 店/店の設計.md` | `newec_harness/<商品名>/08_店/店の設計.md` |
| 土台 `ec/構造/型/店/_土台_記事の飛び先.md` | **`pdp-tsukuru/references/土台.md`（スキルの中。10/19 に友だちが移した正本）**。道具は全部これを相対で読む |
| `ec/構造/型/_必ず入れる物.md` | `~/.agents/skills/ec-ad-ops/references/article/型/_必ず入れる物.md`（記事の分。店の分は SKILL.md の最終確認 T） |
| 役の手順書 `役/ストア担当.md` | `~/.agents/skills/ec-ad-ops/references/article/役/ストア担当.md`（うちが作った1枚。中身は `references/ストア担当の審査.md` を指す） |
| 審査を出す箱 `~/Claude Code/ec-harness/審査を回す.py` | 店だけの箱 `scripts/審査を回す.py`（c906a23 で入った。`claude -p` で書いた本人でない Opus に読ませる）。記事の箱 `~/.agents/skills/ec-ad-ops/tools/article/審査を回す.py` も、店のフォルダ（`店の印.json` がある）を渡せば `scripts/店の検査を回す.py` と `ストア担当の審査.md` の「## 審査の決まり」を使う（2026-10-20） |
| 非公開テーマに置く（`website-copy`） | `~/.agents/skills/website/references/shopify-integration.md`（うちの website スキル。商品は DRAFT・テーマは非公開。公開は Seiyo の指示の後） |
| 絵を作る（ChatGPT の画像 MCP） | Codex の image_gen（うちの決め） |

## 3. この Mac で回す時の要る物（全部そろっている。2026-10-19 に確かめた）
| 物 | うちでの場所・動かし方 |
|---|---|
| Python（`段ごとの画像の検査.py` の playwright・PIL、`設計の検査.py`・`印を書く.py`・`店の仕上がり検査.py`・`店の検査を回す.py`・`面の数字.py`） | `~/.agents/skills/_env/venv/bin/python scripts/<道具>.py …`（`python3` と書いてある所はこれに読み替える） |
| node の道具（`lint.mjs`・`出す前の検査.mjs`・`開いた文字.mjs`・`土台を作る.mjs`） | `node scripts/<道具>.mjs …`。playwright-core は `~/.agents/skills/surasura/scripts/node_modules` の物（`lib.mjs` の探す先に足した）。Chromium は `~/Library/Caches/ms-playwright/chromium-1223`（`lib.mjs` の既定。別の物を使う時は `HONE_CHROMIUM`） |
| `店の検査を回す.py` の lint は、その場で `http.server` を立てる | そのまま動く（統一ブラウザは使わない） |
| 店だけの審査の箱 `scripts/審査を回す.py` | `~/.agents/skills/_env/venv/bin/python scripts/審査を回す.py <店のフォルダ> [--待つ分 40] [--モデル opus]`。中で `claude -p` を呼ぶ（この Mac の `claude` は `~/.claude/local/claude`。PATH に無い時は通らない）。店の検査が全部0の時だけ出す |
| 絵を置く `scripts/絵を置く.py` | `~/.agents/skills/_env/venv/bin/python scripts/絵を置く.py <店のフォルダ>`（`_gen/` の絵を `img/` に置き、`絵と説明の一覧.tsv` を書く。PIL を使う） |
| 往復とカート `scripts/往復とカート.mjs` | `node scripts/往復とカート.mjs <URL> [--カートなし]`（playwright-core は `lib.mjs` の探す先＝surasura の物。カートは非公開テーマのプレビューでだけ） |
| 照らし合わせ `references/照らし合わせの指示文.md` | 指示文を Agent（Opus）に渡す。結果は店のフォルダの `照らし合わせ_<回>.txt` |
| 店の仕上がり検査 `scripts/店の仕上がり検査.py`・店の検査を回す `scripts/店の検査を回す.py` | `~/.agents/skills/_env/venv/bin/python scripts/<道具>.py <店のフォルダ>` |
| 店直行の文字起こし（手順1b） | `whisper-cli`（`/opt/homebrew/bin/whisper-cli`）とモデル `~/.cache/whisper/ggml-large-v3-turbo.bin`（どちらもこの Mac にある。2026-10-20 に確かめた） |
| 面の数字を店の検査に入れる | 店のフォルダに `面の数字の引数.txt`（`--広告 <06_原稿/…/台本.md>`・`--記事 <07_納品/記事/…/index.html>`）を置く。`店の検査を回す.py` が `--店` を足して回す（2026-10-20 うちで足した。Seiyo 未確認） |
| 直しの記録・見本 | `直しの記録.md`・`見本/`（c906a23 で入った。直しを入れたら1行足し、見本を検査と審査に通し直す） |
| 友だちの環境にしか無い物 | `店の木_ワンドライ×ここちドライ.html`・`06 店を作る.md`（読み物。無くてよい）。`役/ストア担当.md`（上の1枚で代える） |

## 4. 前後の工程（うち）
- 前：記事（`ec-ad-ops/references/article.md`・`article/05 記事を作る.md` の「一回で作る道」）。店直行は VSL（依頼票の着地が商品ページ）
- 後：Seiyo の「いいね」→ 非公開テーマ → Seiyo の指示で公開 → 出稿（`ec-ad-ops` 工程5）。流れの全体は `ec-ad-ops/references/flow.md`

## 5. 新しくする時
友だちの GitHub から取り直し（`gh repo clone tokunaritakakura-code/pdp-tsukuru`）、このファイルと、SKILL.md の頭の注・着手ゲートの5行・置き場の行（作業場・Shopify・絵）・`scripts/新規.sh` の置き場・`scripts/lib.mjs` の playwright-core の探す先・`references/見出しの指示文.md` 2・`見た目の方向.md` の客の資料・`~/.claude/skills/` のパスを、うちの物に戻す（2026-10-19 にした読み替えの7か所）。
2026-10-20（c906a23）で足した読み替え: SKILL.md の道具の表（作業場・絵を作る）と手順（1・3c・4・7・8c・11・14a・前後の工程）・`references/写真の指示文.md` の頭の1行（Codex に渡す）・`scripts/新規.sh` の `EC_ROOT`（友だちの「無ければ作る」を入れ、既定は newec_harness のまま）。
入れる前の写しは `~/ec-ads/harness-draft-20261015-zackd/_本物の前の版_20261019/pdp-tsukuru_<日付>/`（10/19）と `~/ec-ads/_gh/_控え_20261020/pdp-tsukuru/`（10/20）
