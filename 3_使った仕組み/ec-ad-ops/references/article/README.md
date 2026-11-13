# 記事の仕組み（advertorial-automation の写し・仮ハーネス 2026-10-16）

読む人: VSL の飛び先の記事を作る Claude と、それを確かめる Seiyo。
読む時: 記事を1本作る前。この仕組みを本物へ入れるか決める前。
読まなくていい条件: 着地が商品ページで、記事を作らないと決まっている時。

## 1. これは何か

友だちの仕組み（リポジトリ advertorial-automation。写しは `/Users/seiyo/ec-ads/_repos/advertorial-automation/`）を、この仮ハーネスに入れた物。
VSL を1本受けて、見終わった人に何が残っているかを書き、記事の形を「普通（権威の暴露・物語）」「リスティクル」「ランキング」の3つから1つ選び、買うまでの15の事を全部入れて書き、機械の検査と編集長の審査を合格まで回して、`index.html` を作る。

友だちの物は Obsidian・`~/Claude Code/`・Dia のブラウザ・ChatGPT の画像の MCP・審査の部屋（サーバー）で動いていた。ここでは次のように替えた。

| 元 | ここ |
|---|---|
| Obsidian の Vault（`ec/構造/…`・`ec/決めたこと.md`） | この `article/` フォルダ。**Obsidian は使わない** |
| `~/Claude Code/ec-harness/`・`adv-kata/`・旧 `~/.claude/skills/kata-tsukuru/scripts/`（どれも旧。新では `tools/article/`） | `/Users/seiyo/.agents/skills/ec-ad-ops/tools/article/` |
| `~/.agents/skills/<スキル>/` | `/Users/seiyo/.agents/skills/<スキル>/` |
| Dia（`dia`・`dia-agent`） | 共通 Chrome（surasura。下の4） |
| ChatGPT の画像の MCP（chatgpt-image） | Codex の image_gen（下の5）。MCP は入れない |
| 審査の部屋（team-room・`http://127.0.0.1:3200`） | 回ごとに新しいサブエージェント（`審査の回し方.md`） |
| 友だちの「買うまでの15の事」 | 言い方は、うちの vsl-script の `15の心の声` が正。対応は `15の対応表.md` |
| 友だちの決め（`決めたこと.md`） | そのまま写した。ただし、うちの決め `ec-ad-ops/references/article.md` が上（VSL のビジュアルを記事に使わない・画像は Codex・公開は Seiyo の指示の時だけ） |

## 2. 何がどこにあるか

`A` = `/Users/seiyo/.agents/skills/ec-ad-ops/references/article`

| 置き場 | 中身 | 元の場所 |
|---|---|---|
| `A/05 記事を作る.md` | 手順の正本。「VSL 動画の飛び先の記事を一回で作る道」1〜10。手順2はうちの引き継ぎ票を読むように直した | Vault `ec/構造/ハーネス/` |
| `A/15の対応表.md` | 友だちの15の事と、うちの15の心の声の対応。見終わった人の状態を票のどこから写すか | 新しく作った |
| `A/審査の回し方.md` | 編集長の審査の回し方（部屋の代わり） | 新しく作った |
| `A/役/編集長.md`・`記事ライター.md`・`ファネル責任者.md` | 審査の関門と作る役の決まり。編集長に 4-2（うちの決めが上）を足した | Vault `ec/構造/ハーネス/役/` |
| `A/型/_VSLから型を選ぶ.md` | 3つの形のどれにするかの決め方 | Vault `ec/構造/型/` |
| `A/型/_買うまでの15の事.md` | 15の事・塗り・見終わった人の状態・好奇心の穴のつなぎ | 同 |
| `A/型/_仕掛けの棚.md`・`_必ず入れる物.md`・`_見た目の手本.md`・`_記事の作り方.md`・`_一覧.md`・`_使った構造.md`・`_骨組み.tsv` | 記事の部品と型の棚 | 同 |
| `A/型/T09…T65`・`A01 メラオ型記事/` | 型ごとの `_分解.md`（棚の `_一覧.md` から全部つながっているので T47〜T65 も入れた） | 同 |
| `A/型/記事の型の木.canvas`・`買うまでの構造.canvas` | 手順から指されている図（JSON。Obsidian では開かない。中の文を読む） | 同 |
| `A/02-記事（アドバトリアル）/型_*.md` | 型ごとの「ブロックの詳細」（頭の段の作り方など。手順4で読む） | Vault `ec/構造/Funnel/…/コンポーネント/` |
| `A/クイズファネル/LINEで回す.md` | クイズを LINE で回す手順 | Vault `ec/構造/Funnel/…/クイズファネル/` |
| `A/playbooks/advertorial.md`・`native-ads.md` | 書く時の関門（1〜32） | Vault `ec/wiki/ads-brain/playbooks/` |
| `A/決めたこと.md`・`A/毎日の制作/_直しの台帳.md` | 友だちの本人の決めと直しの台帳（頭に読み替えの注意を足した） | Vault `ec/` |
| `A/VSL structure/` | 買うまでの項目の実測・VSL の例の索引 | Vault `ec/構造/VSL structure/` |
| `A/_実行契約.md`・`00 組織図.md`・`09 学ぶ.md` | 手順から指されている元の仕組みの説明（部屋や契約の話は読むだけ） | Vault `ec/構造/ハーネス/` |
| `A/資料/記事の最終確認_ひな形.md` | 最後の確かめの表（記事のフォルダへ写して使う） | `~/Claude Code/team-room/引き継ぎ/VSL記事リサーチ_資料/` |
| `A/資料/形式別/_形式と記事の構造.md` | 形式ごとの記事の構造 | 同 |
| `A/資料/針マット/ここちドライの手本/` | 見た目の手本（共通点.md・欄のCSS.html・adv05/08.html） | 同 |
| `A/資料/草むしり椅子/` | 友だちが試しで作った3本（記事1が「普通」の形の固定の参考） | リポジトリの `example/` |
| `A/型の資料/runs/` | 型の資料（bakuro-native・bakuro-static・listicle-native・ranking-static の `型.md`・木） | `~/Claude Code/kata-tsukuru/runs/` |
| `…/skills/` | bakuro-copy・ranking-copy・listicle-copy（新）・quiz-jp-copy・kata-tsukuru・vsl-sagasu（新）。うちの今の版との違いは `skills/差分.md` | `~/.agents/skills/` |
| `…/tools/article/` | 記事の検査.py・記事の仕上がり検査.py・画像の置き方.py・動きの検査.py・審査を回す.py・割り付け検査.py・検査契約.py・config/ | `~/Claude Code/ec-harness/` |
| `…/tools/article/adv-kata/` | 新規.sh（殻と移植表のひな形）・measure.py（参考を数える）・殻の元.html | `~/Claude Code/adv-kata/` |
| `…/tools/article/kata-tsukuru/` | 参考を保存する.py・リンクから辿る.py・値段の段を組む.py（値段の段・コメント欄）・幅の検査.py・素材を貯める.py・木を組む.py・goal.py・skill-creator/（goal.py が使う検査3本） | `~/.agents/skills/kata-tsukuru/scripts/` |

## 3. 1本を端まで作る（この環境で）

正本は `A/05 記事を作る.md` の「一回で作る道」。ここは、どの道具をどう呼ぶかの早見。`PY` = `~/.agents/skills/_env/venv/bin/python`、`TA` = `/Users/seiyo/.agents/skills/ec-ad-ops/tools/article`。

作り始める前に、うちの決め `ec-ad-ops/references/article.md`（鉄則・15の心の声と引き継ぎ票）を読む。作業の置き場は `newec_harness/<商品名>/06_原稿/記事/<記事の名前>/`（承認の前）。納品は `newec_harness/<商品名>/07_納品/記事/<記事の名前>/`、公開は Seiyo の OK の後（2026-10-19 に本物へ入れた。前の試しの置き場は仮ハーネスの `記事テスト/`）。

| # | やる事 | 道具・読む物 |
|---|---|---|
| 1 | VSL を文字起こしする（正本） | `whisper-cli -m ~/.cache/whisper/ggml-large-v3-turbo.bin -l ja -mc 0 <音声>`。コマは ffmpeg で16枚を1枚に |
| 2 | 台本の引き継ぎ票と文字起こしから「見終わった人の状態」を写し、普通・リスティクル・ランキングを決める | 票の決まり `vsl-script/references/記事と分ける.md` 5章、写し方 `A/15の対応表.md` 2章、決め方 `A/型/_VSLから型を選ぶ.md` |
| 3 | 移植表を書く（参考を段に分け、ビジュアルとコピーを分けて書く。塗り・状態・型の候補・穴のつなぎの表を頭に。15はうちの言葉） | 殻とひな形 `bash $TA/adv-kata/新規.sh <型> <商品> <角度> [<置き場>]`。新しい参考は `PY $TA/kata-tsukuru/参考を保存する.py "<URL>" <記事>/参考/`、数えるのは `PY $TA/adv-kata/measure.py "<URL>" <出力.md>`。通るまで `PY $TA/記事の検査.py <移植表.md>`。最後に `A/型/_必ず入れる物.md` を足す |
| 4 | 入り（最初の画面）を作る | `A/02-記事（アドバトリアル）/型_<型>.md` の頭のブロックの作り方 |
| 5 | 数字・権威・声を埋める。作った値は `決めた値.md` に書き、noindex | 友だちの決め（`05 記事を作る.md` の手順5） |
| 6 | ページを組む（字はうちの店の商品ページと同じ。値段の段とコメント欄は道具で） | `PY $TA/kata-tsukuru/値段の段を組む.py <入力.json> -o 値段の段.html`、`… --出す コメント欄 -o コメント欄.html`。手本 `A/資料/針マット/ここちドライの手本/` |
| 7 | 画像を作る（参考の同じ場所の画像を添付して、人と商品をうちの物に） | 下の5。動く素材は `PY $TA/kata-tsukuru/素材を貯める.py 探す …` から |
| 8 | 画像の置き方と動きの検査 | 記事のフォルダに `画像の置き方の引数.txt`（1行目に参考の URL、2行目から引数）を書き、`PY $TA/画像の置き方.py <参考> index.html <引数…>`。動く物は `PY $TA/動きの検査.py index.html <参考の動画…> --見比べ 見比べ_動き.jpg` |
| 9 | 編集長の審査を合格まで | `A/審査の回し方.md` |
| 10 | 仕上がりの検査と幅の確かめ → 最終確認の表 → 本人に5行 | `PY $TA/記事の仕上がり検査.py <記事のフォルダ>`、`PY $TA/kata-tsukuru/幅の検査.py index.html`、`A/資料/記事の最終確認_ひな形.md` を写して全行 |

形ごとのスキル（`…/skills/`）: 普通は `bakuro-copy`、リスティクルは `listicle-copy`、ランキングは `ranking-copy`、日本版アンケート型は `quiz-jp-copy`、型が棚に無ければ `kata-tsukuru`、勝っている VSL を探すのは `vsl-sagasu`。仮ハーネスのスキルは `~/.claude/skills` に入っていないので、使う時は `…/skills/<名前>/SKILL.md` を読んでそのとおりにする。

## 4. ブラウザ（共通 Chrome）

ブラウザは surasura の共通 Chrome だけを使う（プロファイル `~/.claude/task-fleet/chrome-profile`、CDP `http://127.0.0.1:9222`）。

- Python: `from playwright.sync_api import sync_playwright` → `b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")` → `pg = b.contexts[0].new_page()` → 終わったら `pg.close()`（自分のタブだけ。Chrome は落とさない）
- Node: `~/.agents/skills/surasura/scripts/connect.mjs` の `connect()` か `getOrCreateTab(<サイト>)`
- 9222 が無い時は `bash ~/.agents/skills/surasura/scripts/chrome.sh` で立てる。ほかのサイトのタブ（ほかの会話の作業）には触らない。新しいプロファイルは作らない
- `画像の置き方.py`（既定の幅）と `リンクから辿る.py` は、この形で共通 Chrome に繋ぐように直した。繋がらない時は headless の Chromium で同じ事をする。自分のファイルを測るだけの `幅の検査.py`・`参考を保存する.py`・`画像の置き方.py --幅 390` は、元のまま手元の headless の Chromium を使う
- GetHookd は共通 Chrome にログインしている時だけ使える（2026-10-16 はログアウトしていた。ログイン用のタブを1枚開いてある）。使えない時は gethookd の MCP（`search_ads` など）

## 5. 画像（Codex の image_gen）

ChatGPT の画像の MCP は入れない。同じ物を Codex の CLI で直に呼ぶ（友だちの MCP も中で Codex を呼んでいるだけ）。

```bash
cd <記事のフォルダ>/img
printf '%s' "<指示の文。大きさは『横長3:2』『正方形』『縦長3:4』と言葉で。画像の中の日本語はそのまま全部書く。添付の1枚目の構図のまま、人物を日本人に、商品を添付2の本物に替える、など>" \
  | /Users/seiyo/.local/bin/codex exec --skip-git-repo-check --sandbox workspace-write -i <参考の同じ場所の画像> -i <うちの商品の本物の写真>
```

- 文は必ず標準入力で渡す（`-i` は後ろの文までファイル名として飲みこむ）
- 書き先は今いるフォルダ（`workspace-write`）。できた物は `~/.codex/generated_images/` にも残る
- 同時に回すのは、1つのエージェントにつき3枚まで。裏のエージェントからは絶対パスで呼ぶ
- 商品が写る絵は、作る前に `商品の形.md` に本物の形の表を書き、1枚ごとに本物と並べて合わせる（違えば使わない）
- VSL の絵・場面・登場人物は使わない。頭の絵は、記事の参考の同じ段の構図だけから作る
- 動く物の「AI で作る」面は、止まりの絵を Codex で作り、`higgsfield`（いちばん安い動画のモデル）で動かす。お金がかかる生成は先に Seiyo に聞く

## 6. 試した結果（2026-10-16）

友だちの例の記事（`A/資料/草むしり椅子/` の3本）を `/tmp` に写して、道具を全部動かした。

| 道具 | 何で試したか | 結果 |
|---|---|---|
| 記事の検査.py | 3本の移植表と index.html | 3本とも終了コード0「通った」 |
| 記事の仕上がり検査.py | 3本の記事のフォルダ | 3本とも0「通った」 |
| 画像の置き方.py | 3本（記事1は `--幅 390`、記事2・3は既定の幅＝共通 Chrome） | 3本とも0（17／20／20枚が参考と一致）。記事3の参考の本番ページ（innoglam）を共通 Chrome で測り直すと37枚に増えていて1（ずれ）。参考を固定する作りが要る事が分かった |
| 動きの検査.py | 記事3の動画4本（参考の代わりに同じ動画を渡した。他社の参考の動画はリポジトリに無い） | 0（4本とも一致・見比べの1枚を4枚書いた） |
| 割り付け検査.py | 小さな見本の割り付けと反論台帳 | 0「通った」 |
| 審査を回す.py ＋ 編集長のサブエージェント | 記事1の写し（元の審査を消して1回目から） | 束を作って4 → 新しいサブエージェントが判定（約7分）→ `--書く` で FAIL・26件（決定を変える17・書き方9）・終了コード1 → 直さずにもう一度出すと「index.html が変わっていない」で2（関門が効いた）。友だちの部屋では6回目に合格した記事が、うちの決めでは落ちた: 作った医者の名前と顔（三浦 浩一 医師）・画像が ChatGPT の MCP・VSL の場面（孫と土・庭がきれいになったね）の写し・題が動画の最後の問いを受けていない・引き継ぎ票と15行の表が無い、など。うちの決めを編集長に渡せている証拠 |
| adv-kata/measure.py | 記事1の index.html（file://） | 0（節15・太字37） |
| adv-kata/新規.sh | A01・草むしり椅子・試し（置き場は /tmp） | 0。移植表のひな形と殻ができた（bash 3.2 で題の字が化けるのを直した） |
| 幅の検査.py | 3本 | 3本とも0（1280・390 とも、はみ出し0・抜け0・行末の1〜2字落ち0） |
| 値段の段を組む.py | 記事1の入力（値段の段・コメント欄） | どちらも0（HTML を書いた） |
| 参考を保存する.py | `https://roostys.co/pages/feather-loss` | 0（段50・画像40枚・1280と390の画面） |
| リンクから辿る.py | 同じ URL・米国・2本まで（共通 Chrome） | 0（2本・どちらも30日以上）。共通 Chrome は日本語の画面なので、日本語の「ライブラリID」「掲載開始日」も読むように直した |
| 素材を貯める.py | /tmp の素材庫に1本入れて探す | 入れる0・探す0（1件） |
| goal.py・木を組む.py | 試しの型（終わった後に消した） | init 0・木を組む 0・check 1（箱が×なので正しい）・show 0 |

## 7. ここに無い物と、写さなかった物

| 無い物 | 理由・代わり |
|---|---|
| Obsidian・`install.sh`・フック（決めたこと.md を会話に入れる・md の書式検査） | 言われたとおり入れない。決めは手順の中で読む |
| 審査の部屋（team-room）・判断の層（OpenRouter の JEV）・Telegram | 部屋は回ごとのサブエージェントに替えた。ずれの3つの分けは編集長が自分でする |
| ChatGPT の画像の MCP | Codex を直に呼ぶ（上の5） |
| Dia・`dia`・`dia-agent`・友だちの surasura と browser のスキル | 共通 Chrome（上の4） |
| 実行の契約（`lib/ec_contract.py`・`--context`・`--config`） | 写していない。`検査契約.py` は `--context` が無ければ検査だけ回すように直した |
| `週の勝ち負け.py`・`ec-harness/lib/` の残り・`agent_team/` | 記事の手順に要らない（広告の週の判定と部屋の物） |
| 友だちのブランドの資料（`アルコット/`・`ここちドライ/` の 08 記事・反論台帳・`~/Desktop/ec/`） | 人の物。リポジトリにも無い。手順の中で指されていても読み飛ばす |
| 他社の参考の写し（各記事の `参考/` など） | リポジトリに無い。`参考を保存する.py` で取り直す（各記事の `参考を取り直す.md` に URL） |
| quiz-jp の型の正本（`runs/quiz-jp/`） | リポジトリに無い。本物の `~/.agents/skills/ec-ad-ops/references/article/型の資料/runs/quiz-jp/` を読むだけ |
| vsl-sagasu の夜の自動（launchd・`--permission-mode bypassPermissions`）・Telegram・台本係 | 入れていない。入れるかは Seiyo が決める（`skills/差分.md`） |

## 8. 本物へ入れた（2026-10-19）

Seiyo「旧ハーネスは消す。新ハーネスに組み込む」で、`article/` → `~/.agents/skills/ec-ad-ops/references/article/`、`skills/` → `~/.agents/skills/<名前>/`、`tools/article/` → `~/.agents/skills/ec-ad-ops/tools/article/` に入れ、中のパスを全部書きかえた。Python は `~/.agents/skills/_env/venv/bin/python`（旧 `~/Claude Code/venv` の代わり）。友だちの Obsidian・`~/Claude Code/`・`~/Desktop/ec/` にしか無い物（型の `_分解.md` が指す参考の動画、`video-common` の検査）は、この Mac に無いので読み飛ばす。
