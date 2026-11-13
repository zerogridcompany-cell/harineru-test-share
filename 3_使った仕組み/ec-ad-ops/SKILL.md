---
name: ec-ad-ops
description: ECブランドのMeta広告運用の基盤。商品が決まったら、商品理解の基盤（工程1）→ 損益分岐と広告の数字 → 初日の出稿設計（構成・pack・アングル・着地）→ 毎日・毎週の判定（止める・予算・疲れ・診断・来週何本）を、全商品共通の「広告運用ルールの基盤」で毎回同じ形で出す。成果物②〜④（記事・記事の指示書・動画の台本）と運用ボードもここ。「商品が決まった」「初日の構成」「pack作って」「どのアングルから」「来週何本」「止める？」「スケールしていい？」「ROAS落ちた原因」「着地どっちがいい」で使う。作るスキル：動画の台本は vsl-script、記事は references/article の仕組み（bakuro-copy・listicle-copy・ranking-copy・quiz-jp-copy）、店（PDP・商品ページ）は pdp-tsukuru、動画の型 v1（3D図解）は zackd-ad、静止画は ec-static-ads、ネイティブ広告は ec-native-ads（動画の v2〜v10 と権威VSL の作り方はこのスキルの references）。通しの流れは references/flow.md。
---

# ec-ad-ops — 広告運用の基盤

このスキルは手順と出す形だけを持つ。**判断のルールはすべて [references/adops-foundation.md](references/adops-foundation.md)（広告運用ルールの基盤・全商品共通の正本）**。商品ごとの数字は `newec_harness/<商品名>/` の 02・03 から毎回読み、ここに書かない。

## 鉄則

1. **広告の判断は基盤だけで出す。** 答えは「今の数字 → 基盤の番号 → やること → 次に見る日」の1行（基盤 0-2・14章）。基盤に無い場面は自分で埋めず、Seiyo に出して基盤に足す。
2. **決めたことには基盤の番号と根拠の格を付ける**（基盤 0-3）。根拠が無い数字は置かない。
3. **実データは参考。** 全商品の試したことと結果は `newec_harness/03_実績の台帳.md` にためて、判断の横に添える。1つの商品の結果ではルールを変えない（基盤 15-3）。
4. **Meta・Shopify への書き込みは Seiyo の指示がある時だけ。** 作る時は停止（PAUSED）で作り、配信は承認の後。
5. **出す形は毎回テンプレートどおり。** 章の順と表の列を変えない。

## 工程（商品が決まったら、この順）

**通しの流れ（0 リサーチ → 0b 仕入れ先と商品チャンネル → 1 商品理解〈A〜K〉→ 2 お金 → 3 設計と依頼票 → 4a 台本 → 4b 映像 → 4c 記事 → 4d 店 → 4e 静止画 → 5 運用 → 6 UI）と、工程をまたぐ互換性の表は [references/flow.md](references/flow.md)**（2026-10-19）。

**（2026-10-19）14段の台本の型（2026-10-08 に外へ出した物）は、`references/_archive/台本の作り方_20261008/` に写してある（旧の `~/Desktop/アーカイブ/` は使わない）。下の行で指している所は、Seiyo が 14段・物語型・直球型を名指しした時だけ。動画の台本の正本は `vsl-script`。**

**（2026-10-11 Seiyo「このアングルで VSL を何本お願いします、みたいな依頼が、ちゃんと飛ぶ流れに」）動画（VSL）の流れを1本につないだ：商品理解（F・J）→ pack分け（「動画の依頼」の表）→ 依頼票（[templates/vsl-request.md](templates/vsl-request.md)）→ 台本（`vsl-script` スキル。動画の台本の正本）→ 映像（票の映像の型の決まり）。下の表で 14段（アーカイブ）を指している所は、Seiyo が 14段・物語型・直球型を名指しした時だけ使う。指定が無い動画は、依頼票 → `vsl-script`。**

| 工程 | やること | 正本 | 出すもの |
|---|---|---|---|
| 0 | 入口：A リサーチエージェント（ec-research）に探させる／B Seiyo が商品を渡す。**仕入れ先に聞き、「この商品で行く」になったら Discord に商品のチャンネルを作る**（2026-10-19） | [entry.md](references/entry.md)・[supplier.md](references/supplier.md) 1b | `newec_harness/<商品名>/00_入口.md`（ひな形：templates/product/）・`scripts/discord_channels.json` |
| 1 | 商品理解の基盤（調査員5人＋検証役）。**最後に、根本原因を1つ決めて書く**（2026-10-07 Seiyo 指定）。**その後、アングルごとの台本の材料（J）を、アングル1つに1枚作る。`05_原稿の決まり.md` と `06_原稿/` の空の表も置く**（2026-10-11 Seiyo 指定。台本の工程では調べさせないため）。**その後、K ペルソナ（アングル × 相手、1人1枚。何のせいだと思っているか〈つなぎ方の試写つき〉・こうなりたい・広告分析・この人への売り方）を作る。A は使い方（部位・相手ごとの分岐）・お手入れ（洗い方・交換・寿命）・同梱・使えない人まで埋める**（2026-10-19 Seiyo 指定） | [product-foundation.md](references/product-foundation.md)（J は末尾の「J アングルごとの台本の材料」）・**[root-cause.md](references/root-cause.md)（ルーツの探し方）** | `newec_harness/<商品名>/01_商品理解の基盤/`（A〜G と `H_根本原因.md`。**2026-10-11 から `J_アングルごとの台本の材料/<アングル>.md` も**）。次の工程3は、F・J・**K** を入力にする |
| 2 | 損益分岐と広告の数字 | 基盤 0-4・1章 | `02_損益分岐.md`・`03_広告の数字（目標・予算）.md`（ひな形：templates/product/） |
| 3 | 初日の出稿設計（構成の型・アングルの順番・pack・着地・Meta の設定値） | 基盤 2-0・4B・10-1・11章、構成の型：[meta-structures.md](references/meta-structures.md) | [templates/01-pack-split.md](templates/01-pack-split.md) の形 → Seiyo の承認 → 停止で作る。**動画は、同じひな形の「動画の依頼」の表 → 表の本数だけ VSL の依頼票（[templates/vsl-request.md](templates/vsl-request.md)）を `<商品名>/06_原稿/依頼票/` に作る**（2026-10-11。アングルと段階は F の表と J のページから） |
| 4 | **動画（VSL）は「依頼票（`06_原稿/依頼票/`）→ `vsl-script` スキル（台本）→ 票の映像の型の決まり（映像。[video-formats.md](references/video-formats.md) の「今の4つの型」の表）→ 票の『納める場所』に納品」。動画の台本は `vsl-script` が正本**（2026-10-11 Seiyo 指定。票が無い動画は、先に工程3の表と票を作る。票の状態に「台本ずみ」「映像ずみ」「記事ずみ」と日付を足していく。**映像の後、同じ回で飛び先の記事を作る**＝[article.md](references/article.md)・`video-formats.md` の「動画の次は、必ず記事」。VSL のビジュアルは記事に使わない〈2026-10-12〉）。静止画の文字・本文・見出し・記事は、今までどおり下の creative-foundation.md と pack-scripts.md。<br>原稿：pack ごとに4本の原稿（静止画の文字・動画の台本・本文3案・見出し・法令の確認）。記事は ②③。**（ここから先の 14段は、Seiyo が 14段・物語型・直球型を名指しした時）動画の台本（VSL）は、先に `H_根本原因.md` を読み、[vsl-script-design.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-design.md) の14段で書く（第4版。Seiyo 合格の原稿 [vsl-script-example.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-example.md) と並べて）。4〜5分。ヴィランは1つ、説明書の引用と試験の数字は入れない。1本ずつ書いて Seiyo に見せ、答えをもらってから次。書いた後に同じファイルの7章の点検（22問）を通す**（2026-10-07 Seiyo 指定。前からの決まりとぶつかる所は vsl-script-design.md の9章） | **[creative-foundation.md](references/creative-foundation.md)（原稿の基盤・正本）**・**[root-cause.md](references/root-cause.md)**・**[vsl-script-design.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-design.md)**・**[vsl-script-example.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-example.md)**・[script-checklist.md](references/script-checklist.md)・商品の `05_原稿の決まり.md` | [templates/pack-scripts.md](templates/pack-scripts.md) の形で `<商品名>/06_原稿/` に保存。**記事は [article.md](references/article.md) の「先に読む」の道で作る**（型ごとのスキル。流れは flow.md の 4c）。承認の後に制作（動画は Seiyo が選んだ型で作る：[video-formats.md](references/video-formats.md)〈10種類・Remotion で編集〉。権威VSL の細かい決まりは authority-vsl-production.md、静止画は 2-9） |
| 4d | **店（PDP・商品ページ）**：記事の次に、記事の「残った疑い」を買う所で閉じる商品ページを `pdp-tsukuru` で作る。商品の事実は `00`・`A`・`02`、客は `K` から（`pdp-tsukuru/references/harness-map.md`）。土台 `_土台_記事の飛び先.md` は友だちから取るまで無い（2026-10-19） | [pdp.md](references/pdp.md) | `<商品名>/08_店/`（店の設計・`index.html`・印）。票に「店ずみ」。非公開テーマは「いいね」の後 |
| 5 | 毎日・毎週の運用（止める・予算・疲れ・診断・来週何本・記事の点検）。**テストの段を `tests.json` に書く**（基盤 4C-8：分析日・夜の「明日の運用の案」・新しい広告を作った時に必ず更新。2026-10-07） | 基盤 4C・5〜10章・12章 | 判断の1行と、運用ボード、`~/newec-dashboard/products/<商品>/tests.json` |

## 何を聞かれたら、どこを読むか

| 依頼 | 読む | 出す形 |
|---|---|---|
| 商品を探して／この商品でやる | entry.md | 00_入口.md |
| 仕入れ先に聞いて／原価いくら？／返事来た？ | [supplier.md](references/supplier.md) | Discord に送る・返事を読む → 00_入口.md の仕入れ |
| 初日の構成・どのアングルから・pack を分けて | 基盤 1章 → 2-0 → **4B-0b（全部の広告の中身を読んで ①入口②軸③着地 を書き出す）** → 4B → 11章 | templates/01-pack-split.md（中身の表と、疲れの準備の表つき） |
| 原稿を作って | creative-foundation.md → script-checklist.md（動画の台本は、下の「VSL を作って」の行。2026-10-11） | templates/pack-scripts.md |
| 根本原因（ルーツ）を決めて／本当の原因は何？／なぜ今までの対策は効かない？ | [root-cause.md](references/root-cause.md)（商品の 01 の A〜G を読んでから） | `<商品名>/01_商品理解の基盤/H_根本原因.md`（root-cause.md の9章の形） |
| VSL を作って／この pack の動画を／このアングルで VSL を◯本（2026-10-11） | その商品の `04_初日の出稿設計.md` の「動画の依頼」の表 → `06_原稿/依頼票/` の票（無ければ [templates/vsl-request.md](templates/vsl-request.md) で作る。アングルのページ〈J〉が無ければ、先に product-foundation.md の J）→ `vsl-script` スキルに票を渡す（台本）→ 票の映像の型の決まり（[video-formats.md](references/video-formats.md) の「今の4つの型」の表） | 票1枚につき：台本（票の「納める場所」に `台本.md`・`理解メモ.md`・`相手.md`）→ 映像（票の「納める場所」）。票の状態に日付を足す |
| VSL・動画の台本を書いて／台本を直して（**14段・物語型・直球型を名指しされた時。指定が無ければ、上の行＝`vsl-script`**。2026-10-11） | その商品の `H_根本原因.md`（無ければ root-cause.md で先に作る）→ [vsl-script-design.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-design.md)（14段・4〜5分・回数・点検。第4版）と [vsl-script-example.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-example.md)（合格の見本）→ script-checklist.md | 原稿の頭に「根本原因・ヴィラン・名指しの絵・仕組みの名前」の1行ずつ。本文は14段の順のナレーション（引用・試験の数字なし）。字数と長さ（1秒6.6字）。1本ずつ出す。原稿の外に「足りない事実」 |
| 静止画を作って／static ads | [static-formats.md](references/static-formats.md)（2.5章の表のとおり商品フォルダを読む → 型を選ぶ → Codex で画像 → 見出しと本文〈原稿の基盤 6章〉）。入口のスキルは `ec-static-ads` | `<商品名>/06_原稿/` に型の id つきの原稿 → 承認後に `07_納品/Static Ads/<pack>/`（画像・ヘッドライン.txt・本文.txt） |
| ネイティブ広告を作って | `ec-native-ads` スキル（2026-10-07。native-ads を複製し、商品理解の入口をハーネスに付け替えた版。読む所の対応は、そのスキルの `references/harness-map.md`）。その商品の `H_根本原因.md` が先 | `<商品名>/06_原稿/native_<pack>_<日付>.md` → 承認後に `07_納品/Native Ads/<pack>/` |
| 記事を作って／記事の依頼（ダッシュボード） | [article.md](references/article.md) の「先に読む」→ `references/article/05 記事を作る.md` の一回で作る道（型は `_VSLから型を選ぶ.md` で決め、`bakuro-copy`・`listicle-copy`・`ranking-copy`・`quiz-jp-copy` で作る） | `<商品名>/07_納品/記事/<名前>/`（html・content.json・納品メモ） |
| 店を作って／PDP／商品ページを作って／記事の飛び先の店（2026-10-19） | [pdp.md](references/pdp.md) → `pdp-tsukuru`（読み替えは `references/harness-map.md`） | `<商品名>/08_店/`。「いいね」の後に非公開テーマ |
| ペルソナを作って／この商品のアングルを全部出して／相手を深めて | [product-foundation.md](references/product-foundation.md) の K（ひな形 `templates/persona.md`・指示 `templates/product-foundation/prompts.md` の K） | `<商品名>/01_商品理解の基盤/K_ペルソナ/<アングル>_<呼び名>.md`＋`_一覧.md` |
| 商品のチャンネルを作って／Discord で（商品名）に送って | [supplier.md](references/supplier.md) 1b・1 | `scripts/supplier_discord.mjs channel create`・`send --channel <名前>` |
| 使い方・洗い方を調べて | [product-foundation.md](references/product-foundation.md) の A（A-3〜A-6） | `A_商品の事実.md` の 3〜4・7 |
| ダッシュボードの依頼を見て／依頼に対応して | `~/newec-dashboard/products/<商品>/requests.json`（決まりは `~/newec-dashboard/README.md` の「Claude に頼む」） | `state` が「依頼」のものを読む → 案を `reply` に書いて「対応中」→ 基盤とスキルどおりに作業 → 結果を `reply` に書いて「済み」（行は消さない） |
| 来週何本 | 基盤 1章 → 4章 → 4B | 「来週＝◯pack・◯本（言い換え◯・新しい層◯）」＋型ごとの消化の割合（4章⑦） |
| 次に何をテストする？／フックテスト・型（形式）のテスト | 基盤 **4C（テストの順番：入口 → 形式 → フック → 本文・見出し → 音）** → 4章⑥（フック替え）・4B-7（pack の中の4本） | 「今の段 → 進む条件に当たるか → 次に作る物」。`tests.json` を更新（4C-8） |
| 止める？・予算・疲れ・記事の点検 | 基盤 14章の型 | 判断の1行 |
| 疲れてきた？・次の pack の準備は？ | 基盤 6-6〜6-9・4-c | 入口ごとの疲れの比 → 準備の合図 → 準備する pack と出す日（templates/01-pack-split.md の「疲れの準備」の表） |
| ROAS が落ちた | 基盤 7章 → `scripts/fetch.py`・`scripts/analyze.py` | [templates/diagnosis.md](templates/diagnosis.md) |
| 記事か商品ページ直行か | 基盤 10-1・10-3 | Q 番号と理由、または着地テストの設計 |
| 特商法・返金ポリシー・規約・配送・プライバシーを作って／保証の書き方を直して | [store-legal.md](references/store-legal.md)（返金保証は30日・15日使用後が決まった形。全部の場所で同じことを言う） | templates/store-legal/ の5つの文書（ストアへの書き込みは指示がある時だけ） |
| 新しい広告アカウント | 基盤 11-4（ウォームアップ） | 準備〜4週目の表 |
| 広告の一覧を見せて | [ops-board.md](references/ops-board.md) | 運用ボード（Artifact） |

## 答える前に読み直すもの
運用の質問（どの pack を回す・何本作る・いつ再開など）に答える前に、基盤と、その商品の 02・03・初日の出稿設計・運用ボードを読み直し、決まっている計画をそのまま答える。計画を変える提案は、理由（新しい実データ・Seiyo の新しい指定）がある時だけ「計画は◯◯、変えるなら理由は△△」と分けて出す（2026-10-02 Seiyo「なんで毎回意見変えるん？」）。

## 数字の取り方
- 取得：`scripts/fetch.py <brand> <期間A開始> <期間A終了> <期間B開始> <期間B終了>`（読み取りのみ）。出力は `~/ec-ads/<brand>-<作業名>-<日付>/raw/`
- 計算：`scripts/analyze.py <作業フォルダ>`
- 基盤が求める数字（ピクセルの購入件数・新しく届いた人数など）の取得の接続は別途（2026-10-03 Seiyo「接続は後で」）

## 制作の決まり（運用の外。正本だけ示す）
- **実写の画（絵コンテ・話し手・悩みの場面・手元）は、リアルに見せる型で作る**（2026-10-07 Seiyo 指定）：[realistic-image.md](references/realistic-image.md)（スマホで撮った1枚として書く7つ・共通の枠・場面ごとの注意・点検）。権威VSL・動画の型 v2・実写の静止画に当てる
- **声は必ず ElevenLabs の V4（`eleven_v4`）**（2026-10-07 Seiyo「今後も絶対 V4。本当にナチュラル」）。どの型の動画でも同じ。ほかのモデル（v2・v3・turbo など）に落とさない。V4 が使えない時は止めて Seiyo に言う
- **動画（VSL）は、依頼票 → `vsl-script`（台本）→ 映像の型の決まり**（2026-10-11 Seiyo 指定。上の工程 3・4）。映像の型と寄せ方は、今の4つ（ZackDFilms・スケルトン・権威実写・クレイ物語）で固定：[video-formats.md](references/video-formats.md) の「今の4つの型」。下の 14段・物語型・直球型は、Seiyo が名指しした時
- **VSL の台本は、根本原因を1つ決めてから、14段の型で書く。4〜5分**（2026-10-07 Seiyo 合格）：[root-cause.md](references/root-cause.md)（ルーツの探し方）→ [vsl-script-design.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-design.md)（第4版。段ごとの決まり・回数・点検）→ 見本 [vsl-script-example.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/vsl-script-example.md)（針マット A 第12版）。ヴィラン1つ・引用と試験の数字なし・「今なら間に合う」2回・Why us・「〜の人へ」1つ・「20秒ください」。1本ずつ書いて見せる。Seiyo が下の物語型・直球型を指定した時も、原因の段は同じ根本原因を使う
- **話し手のいるVSLは2つの型を持ち、動画ごとに選ぶ**（2026-10-04 Seiyo 指定）：[vsl-types.md](references/vsl-types.md)（物語型と直球型の選び方、型で変わる決まりの表）。どちらにするかは Seiyo が決め、指定が無ければ聞く
- **静止画広告は、10種類の型（st01〜st10）から選び、型を変えてテストする。作る前に商品フォルダを読み、画像＋見出し＋本文を1組で出す。画像は Codex で作る**（2026-10-07 Seiyo 合格「はい最高」「もう完璧」）：[static-formats.md](references/static-formats.md)（st01 実体化〜st10 メッセージ画面の10種類・テストでの使い方・Codex の呼び方・止められた時の言い換え・点検）
- **実写の VSL は、リアルの型の手順で作る**（2026-10-07 Seiyo 合格「よすぎ。実写のVSLのハーネスこれベースでアップデートして」）：[live-action-vsl.md](references/live-action-vsl.md)（14段の台本 → リアルの型の画像〈Codex〉→ 声 → HeyGen の口パク → Wan 2.7 で動画化〈`scripts/i2v_real.py`〉→ 組み立て → 検品。全部カラー。話し手は画面いっぱい・襟元にピンマイク。見本は `~/ec-ads/hagashi-authority-vsl-20261007/`）。Seiyo の指定が無ければ、話し手が映る実写の VSL はこの手順
- 物語型（今までの権威VSL）：[authority-vsl-production.md](references/authority-vsl-production.md)（声・テンポ・口パク〈基本は HeyGen〉・画・音・検品・納品）
- 直球型（約3分30秒）：原稿は [templates/vsl-direct.md](~/.agents/skills/ec-ad-ops/references/_archive/台本の作り方_20261008/1_VSLの台本の型（14段）/直球型の台本のひな形_vsl-direct.md)、編集は `scripts/vsl_direct.py`（字幕の箱・重ねる効果・ブレのつなぎ・色地のカード・点検 `tl.check()`）
- 作る前と納品前のチェック：[script-checklist.md](references/script-checklist.md)（Seiyo の指摘は直したらその場で足す）
- 動画の納品は成果物④のページの形。新しく作った素材は `register_assets.py` で素材庫に登録してから納品
- 参考動画から学んだこと（知識ノート。決まりではない）：[2026-10-04 ARCO 権威VSL](references/knowledge/2026-10-04-arco-authority-vsl.md)（3分30秒・160カットを測った、台本の段と秒数・言葉の種類ごとの画の当て方・字幕と重ねる効果の実測。今の決まりと逆を向く6点は、型ごとの決まりとして vsl-types.md に分けた）

## ダッシュボード（広告ルーム）
**新しい UI（`zerogridcompany-cell/zerogrid-dashboard-ui`。2026-10-19）**：画面がどのデータを待っているかと、うちのどのファイルがそれを持っているかは [ui.md](references/ui.md)。`scripts/ui_export.py` が `products/<id>/ui/*.json` に写す（繋ぐのはまだ）。`profile.json`・`tests.json`・ログを書く時は ui.md 5章の欄も埋める。下は前のダッシュボード（今も使う）。

`~/newec-dashboard/`（http://localhost:4318。画面とデータの決まりは `README.md`）。動画の型の承認（[video-formats.md](references/video-formats.md)）・記事の依頼（[article.md](references/article.md)：`plan.json` の `article_drafts`）・広告と pack と記事の色の判定（基盤 14B）はここで見る。メタ・ショッピファイへは書き込まない（メタは読み取りだけ）。カードの「作り直す」「型を変えて作る」「着地を変える」「直しを頼む」から Seiyo が頼んだことは `products/<商品>/requests.json` に入る（2026-10-06）。広告・記事・動画の作業を始める前に、`state` が「依頼」のものが無いか読む。矢印のつなぎ替え（着地を変える）・新しい記事の内容の案（その依頼の `outline`）・絵コンテの素材の差し替え（`products/<商品>/sb-swaps.json`。動画を作る前に必ず当てる）も同じ README に決まりがある。

### 運用はダッシュボードに残す（2026-10-07 Seiyo 指定「このダッシュボードを使って運用してほしい。1日ログに、何を見て・どう判断して・何をしたかを残す」）
- 広告の運用で何かを見た・判断した・した時は、毎回 `node ~/newec-dashboard/scripts/adroom.mjs log --product <id> --kind <judge|wait|make|ask|fix> --title … --saw <見た数字> --why <だからこう判断した> --did <したこと> --rule <基盤の番号> --shot "<画面>::<説明>"` で記録する。**待った時も「待つ」と理由を書く**（待ちが基本）。
- その日の終わりに `adroom.mjs summary`（見たこと → だから → したこと、次に見る日・承認してほしいこと）。
- 毎晩 21:00 に「明日の運用の案」を作り（`adroom.mjs plan`）、Seiyo がログで「はい」と押した案だけを、押された時に実際に適用する（メタの変更を含む。これが Seiyo の指示にあたる：2026-10-07）。案に無い事は適用しない。
- 商品の追加（一覧の「＋」）と「今日の運用」は、ダッシュボードが裏で Claude を走らせる。指示文は `~/newec-dashboard/harness/`。決まりは `~/newec-dashboard/README.md` の「ハーネスとのつなぎ」。

## 運用ボード（Artifact の型）
「広告の一覧を出して」「配信前の広告を並べて」→ [ops-board.md](references/ops-board.md) の型（広告マネージャの形のタブ、pack・作成済み／未作成・種類で絞り込み、広告名から詳細へ）。ひな形：templates/ops-board/。新しい商品は別の Artifact、同じ商品は同じ URL に data を差し替える。

## 使うのをやめた資料
`references/_旧/`（9/30 までの運用ルール・pack の作り方・着地・診断・根拠の付け方）。中身は基盤に移した。前のハーネス（`EC/`）の `判定.md`・`出稿.md` なども使わない。
