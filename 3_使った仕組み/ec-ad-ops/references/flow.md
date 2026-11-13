# 通しの流れ（新ハーネス）— プロダクトリサーチから出稿・運用まで、1本の線（2026-10-19）

Seiyo「プロダクトリサーチから全部流れで通せるようになったはずだから、その流れを完成させて、接続と連携を強くして、互換性を良くする」。
このファイルは、**どの工程が・何を読んで・何を出し・次の工程がそのどこを読むか**だけを決める。各工程の中身の決まりは、右の「正本」。決まりはスキル（`~/.agents/skills/`）、商品の事実と完成品は `~/Desktop/claude code/newec_harness/<商品名>/`（設計図 `00_はじめに読む_設計図.md`）。旧ハーネス（`~/.claude/skills/`・Obsidian・`~/Claude Code/`・`~/Desktop/アーカイブ/`）は使わない（`~/.agents/skills/README.md`）。

## 1. 線（この順。戻らない）

| 工程 | 何をする | 入力（前の工程のどれを読むか） | 出す物（商品フォルダ） | だれが決める | 正本 |
|---|---|---|---|---|---|
| **0 リサーチ** | 商品を1つ確定する（全件列挙 → 同一商品の実証 → 80点以上の1商品＋参入パック） | Hookd の538社・台帳 | 参入パック（レポート）。入口 B（Seiyo が商品を渡す）なら、渡された物 | Seiyo「この商品で行く」 | `ec-research`（`~/.agents/skills/ec-research/SKILL.md`）・[entry.md](entry.md) |
| **0b 仕入れ先（Discord）** | ①#general に「ありますか・いくらですか」を送る → ②返事（見積もりの画像）を読んで原価を記録 → ③「この商品で行く」になったら、**サーバーに商品のチャンネルを作る**（ほかの商品のチャンネルと同じ形。以後その商品の連絡はそこ） | 参入パックの仕入れ先 URL（0）。もう聞いてある物は送らない | `00_入口.md`（仕入れの表・原価）・`scripts/discord_channels.json` にチャンネル | Seiyo（買うかどうか・交渉の2回目） | [supplier.md](supplier.md)（1・2・3・**1b**）・`scripts/supplier_discord.mjs` |
| **1 商品理解** | 調査員5人＋検証役で A〜G → H 根本原因 → I 仕組みの細部 → J アングルごとの台本の材料 → **K ペルソナ（アングル × 相手。つなぎ方の試写・広告分析つき）** → `05`・`06_原稿/` の空の表 | `00_入口.md`（商品・仕入れ先・競合の URL）。**A は商品ページの FAQ・説明書・仕入れ先・競合ページ・レビューから、使い方（部位・相手ごとの分岐）・お手入れ（洗い方・交換・寿命）・同梱・使えない人まで埋める** | `01_商品理解の基盤/`（00・A〜G・H・I・`J_…/<アングル>.md`・**`K_ペルソナ/<アングル>_<呼び名>.md`＋`_一覧.md`**）・`05_原稿の決まり.md`・`06_原稿/`（台帳・使った物の記録・依頼票/） | Seiyo（E の他にないもの・F・H を1つに） | [product-foundation.md](product-foundation.md)（A・J・**K**）・[root-cause.md](root-cause.md)・`templates/product-foundation/prompts.md`・`templates/persona.md` |
| **2 お金** | 損益分岐・目標 CPA・予算 | `00_入口.md` の原価・売値（0b・0） | `02_損益分岐.md`・`03_広告の数字（目標・予算）.md` | Seiyo（売値・残したい利益・月の上限） | 基盤 0-4・1章・`templates/product/` |
| **3 初日の設計** | 構成の型・pack・アングルの順・着地・Meta の値 → **「動画の依頼」の表（pack × アングル × ペルソナ × 段階 × 映像の型 × 本数）** → 本数だけ依頼票 | `F`（段階×悩み）・`J`・**`K_ペルソナ/_一覧.md`**・02・03 | `04_初日の出稿設計.md`・`06_原稿/依頼票/<pack>_<番号>_<アングル>_<段階>_<型>.md`（**ペルソナの行つき**） | Seiyo（承認。Meta は停止で作る） | 基盤 2-0・4B・4C・`templates/01-pack-split.md`・`templates/vsl-request.md` |
| **4a 台本** | 票1枚につき1本。`vsl-script` の読む物のとおり：商品を読む → 相手の理解シート（J・K を写す）→ `台本の決まり.md`（伝える事 a〜h と質。最後に「くっそ分かりやすく書き直す」1周と自分の見直し）＋寄せ方の1枚 → 台本。**人に見せる試写はしない**（2026-10-21） | 票・`J` のページ・**`K` のページ**・05・06 の記録 | 票の「納める場所」に `台本.md`・`理解メモ.md`・**`相手の理解シート.md`**・`相手.md`（引き継ぎ票・分け方の表つき）。K の「台本で深めた差分」に追記。票に「台本ずみ」 | Seiyo（台本・1文目） | `vsl-script`（SKILL.md の読む順・`商品を読む.md` 11・`相手を1人に決める.md` 0章・`寄せ方/ZackDFilms寄り.md` 第3.5版・`templates/相手役の試写.md`） |
| **4b 映像** | 票の映像の型で作る（ZackDFilms／スケルトン／権威実写／クレイ物語／ZackD POV）。絵コンテ → 承認 → 声（ElevenLabs V4）→ 絵 → 編集 → 検品 | 台本（文言は変えない）・票 | `07_納品/VSL/<pack>/<票>/`（mp4・原稿）。票に「映像ずみ」 | Seiyo（絵コンテ・最終承認） | [video-formats.md](video-formats.md)「今の4つの型」・`zackd-ad`・[storyboard-approval.md](storyboard-approval.md) |
| **4c 記事** | 同じ回で必ず。文字起こし → 引き継ぎ票から「見終わった人の状態」→ 形（普通／リスティクル／ランキング／日本版アンケート）→ 移植表 → 入り → 組む → 画像（Codex）→ 審査 PASS → 仕上がりの検査 | 台本の引き継ぎ票・分け方の表（4a）・映像（4b）・`00`・`01`・`02` | `07_納品/記事/<名前>/`（`index.html`・移植表・決めた値・審査）。票に「記事ずみ」 | Seiyo（公開） | [article.md](article.md)・`article/README.md`・`article/05 記事を作る.md`「一回で作る道」・`bakuro-copy`／`listicle-copy`／`ranking-copy`／`quiz-jp-copy` |
| **4d 店（PDP）** | 記事の「残った疑い」を買う所で閉じる商品ページ。店の設計（来た人・型・見た目の方向・変数42個・絵・3つの面）→ 空の型を埋める → 機械の検査 → 審査 PASS → Seiyo の「いいね」→ 非公開テーマ | 記事の移植表の「見終わった人の状態」（4c）・**`00`・`A`・`02`・`05`（商品の事実）・`K`（客の資料）** | `08_店/店の設計.md`・`08_店/01_<商品>_店_<型>_v1/`（`index.html`・`店の印.json`・`決めた値.md`）。票に「店ずみ」 | Seiyo（いいね・公開） | [pdp.md](pdp.md)・`pdp-tsukuru`（`references/harness-map.md` で読み替え） |
| **4e 静止画・ネイティブ** | pack の中の静止系（10種類の型）・ネイティブ広告 | `01`（A〜H）・05・06 | `06_原稿/` → `07_納品/Static Ads/`・`Native Ads/` | Seiyo（承認） | [static-formats.md](static-formats.md)・`ec-static-ads`・`ec-native-ads` |
| **5 出稿・運用** | Meta に停止で作る → 承認で配信 → 毎日・毎週の判定（止める・予算・疲れ・診断・来週何本・記事の点検・テストの段） | 04・02・03・07（完成品）・数字（fetch.py） | 判断の1行・`03_実績の台帳.md`・`tests.json`・運用ボード | Seiyo（Meta を実際に変える指示。夜の案の承認） | [adops-foundation.md](adops-foundation.md)・[ops-board.md](ops-board.md)・`scripts/fetch.py`・`analyze.py` |
| **6 UI** | 承認・納品・数字を見る画面。今は前のダッシュボード（`~/newec-dashboard/`）。**新しい UI（`zerogridcompany-cell/zerogrid-dashboard-ui`。画面だけ・仮データ）に渡す形は決めた：`scripts/ui_export.py` が `products/<id>/ui/*.json` に写す。まだ繋いでいない** | 商品フォルダ・`products/<id>/`（plan・profile・tests・requests・log・metrics）・仕入れ先の写し・ec-cs の state | `products/<id>/ui/*.json`・`products/_ui/*.json`（UI の定数と同じ名前） | Seiyo | [ui.md](ui.md)・[ops-board.md](ops-board.md)・`~/newec-dashboard/README.md`（前の UI） |

## 2. 互換性（工程をまたいで、同じ物を2回作らない・同じ事実を2か所に書かない）

| 事実・物 | 正本（1か所） | 読む工程 |
|---|---|---|
| 商品の事実（仕組み・仕様・使い方の分岐・お手入れ・同梱・使えない人） | `01_商品理解の基盤/A_商品の事実.md` | 1（J-5・K-2）・4a（商品を読む 3）・4c・**4d（店の変数）**・4e |
| 売値・セット・原価・保証の日数 | `00_入口.md`・`02_損益分岐.md`・`store-legal.md` | 2・4c・4d・5 |
| 根本原因・仕組みの歩み | `H_根本原因.md`・`I_仕組みの細部.md` | 1（J-3・K-7）・4a・4c・4e |
| アングル（困り事の入口） | `F`（悩みの行）＝`J_…/<アングル>.md` のページ名 | 3・4a・K |
| **相手（ペルソナ）：今、何のせいだと思っているか／今している事／口ぐせ／こわい事／こうなりたい／効いている入口** | **`K_ペルソナ/<アングル>_<呼び名>.md`**（台本は写して深め、差分を戻す） | 3（依頼の表）・**4a（相手の理解シート）**・4c（見終わった人の状態の相手）・**4d（見た目の方向の客の資料）** |
| 動画1本の依頼（pack・アングル・ペルソナ・段階・型・着地・納める場所・状態） | `06_原稿/依頼票/<票>.md` | 4a・4b・4c・4d（票の状態に台本ずみ → 映像ずみ → 記事ずみ → 店ずみ） |
| 動画と記事の受け渡し（15の心の声の受け持ち・最後の問い・約束した事） | 台本の引き継ぎ票（`vsl-script/references/記事と分ける.md` 5章）＋分け方の表 | 4c（`15の対応表.md` 2章で写す）・4d（店直行は `VSLの塗り.md`） |
| 記事と店の受け渡し（見終わった人の状態・残った疑い） | 記事の移植表（4c） | 4d（店の設計 1・2） |
| 広告→記事→店で同じでなければならない数字（評価と件数・配送日数・値段・保証日数） | `00`・`02`・`store-legal.md`。作った値は各工程の `決めた値.md`（前の作業フォルダでは古い名前 `テスト用に決めた値.md`） | 4c・4d・5 |
| もう使った物（書き出し・たとえ・型） | `06_原稿/台本の台帳.md`・`使った物の記録.md` | 4a（毎回変える物） |
| 仕入れ先とのやりとり | Discord の商品チャンネル（`scripts/discord_channels.json`）・`00_入口.md` の仕入れの表 | 0b・5（注文・発送） |

## 3. 各工程の入口（「〜して」と言われたら）
| 言われた事 | 開く所 |
|---|---|
| 商品を探して | `ec-research` → [entry.md](entry.md) A |
| この商品でやる | [entry.md](entry.md) B → [supplier.md](supplier.md) |
| 仕入れ先に聞いて／返事来た？／商品のチャンネルを作って | [supplier.md](supplier.md) 1・2・**1b** |
| 商品理解を作って／ペルソナを作って／使い方と洗い方を調べて | [product-foundation.md](product-foundation.md)（A・J・**K**） |
| 初日の構成／pack を分けて／このアングルで VSL を何本 | 基盤 4B → `templates/01-pack-split.md` → `templates/vsl-request.md` |
| この票で台本を書いて | `vsl-script`（票を渡す） |
| 映像にして | [video-formats.md](video-formats.md) |
| 記事を作って | [article.md](article.md) |
| 店を作って／PDP／商品ページ | [pdp.md](pdp.md) |
| 静止画／ネイティブ | [static-formats.md](static-formats.md)／`ec-native-ads` |
| 止める？予算は？来週何本？ | [adops-foundation.md](adops-foundation.md) 14章の型 |

## 4. まだつながっていない所（2026-10-19）
- **新しい UI**（`zerogridcompany-cell/zerogrid-dashboard-ui`）：10/19 夜に読めた（この Mac の写し `~/zerogrid-dashboard-ui/`）。画面だけで、仮データの形は `HANDOFF.md`。うちの出す形との対応と変換の道具は [ui.md](ui.md)（`scripts/ui_export.py`）。**繋ぐのは Seiyo と最後に**（売上・実利益・Clarity の来た人% はその時に取る）
- **店の土台**：10/19 夜に友だちが pdp-tsukuru の中へ入れた（`pdp-tsukuru/references/土台.md`。検査の道具も全部）。4d は `新規.sh` から通しで動く（この Mac で確かめた。[pdp.md](pdp.md)）
- 工程1の K は、決まりとひな形を入れた所。新ワンドライ・新針マットには、まだ K が無い（次の台本の前に作る）
