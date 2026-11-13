# 新ハーネス（`~/.agents/skills/`）の地図 — 2026-10-19

Seiyo「俺らが使うハーネスは新ハーネスだけ。旧ハーネスを参照している箇所は新ハーネス内に組み込む。旧は最後に消す」。
このフォルダが**唯一の決まりの置き場**。商品の事実と完成品は `~/Desktop/claude code/newec_harness/<商品名>/`（設計図 `00_はじめに読む_設計図.md`）。通しの流れは **`ec-ad-ops/references/flow.md`**。

## 1. 工程と、使うスキル
| 工程 | スキル（このフォルダの中） | 入口 |
|---|---|---|
| 0 リサーチ | `ec-research`（全件列挙・同一商品・80点）。`dropshipping-product-research` は参考 | `ec-research/SKILL.md` |
| 0b 仕入れ先・Discord | `ec-ad-ops`（`references/supplier.md`・`scripts/supplier_discord.mjs`・`scripts/discord_channels.json`） | supplier.md |
| 1 商品理解（A〜G・H・I・J・**K ペルソナ**） | `ec-ad-ops`（`references/product-foundation.md`・`root-cause.md`・`templates/product-foundation/prompts.md`・`templates/persona.md`） | product-foundation.md |
| 2 お金・3 初日の設計・依頼票 | `ec-ad-ops`（`references/adops-foundation.md`・`templates/01-pack-split.md`・`templates/vsl-request.md`） | SKILL.md の工程表 |
| 4a 台本 | `vsl-script`（台本の決まり 1枚・寄せ方の分かれ道・ZackDFilms寄り 第4版。試写なし。2026-10-21） | `vsl-script/SKILL.md` |
| 4b 映像 | `ec-ad-ops/references/video-formats.md`・`zackd-ad`・`ec-vsl`（参考VSLの日本語化）・`higgsfield-*`（絵と動画の生成） | video-formats.md |
| 4c 記事 | `ec-ad-ops/references/article.md` → `references/article/`（友だちの仕組みの写し）・`bakuro-copy`・`listicle-copy`・`ranking-copy`・`quiz-jp-copy`・`kata-tsukuru`・`vsl-sagasu`。本物の声のリサーチは `voc`。道具は `ec-ad-ops/tools/article/` | article.md |
| 4d 店（PDP） | `pdp-tsukuru`（友だちのスキル。読み替えは `references/harness-map.md`）・`website`（公開ページの完コピ → Shopify）・`ec-ad-ops/references/pdp.md` | pdp.md |
| 4e 静止画・ネイティブ・メール | `ec-static-ads`・`ec-native-ads`・`ec-email` | 各 SKILL.md |
| 5 運用 | `ec-ad-ops`（基盤 4C〜14章・`scripts/fetch.py`・`analyze.py`）・`ad-funnel`（数字の取得。fetch.py が使う） | adops-foundation.md |
| 6 UI | 前のダッシュボード `~/newec-dashboard/`（`ec-ad-ops/references/ops-board.md`）。新しい UI（`zerogrid-dashboard-ui`）に渡す形は `ec-ad-ops/references/ui.md`・`scripts/ui_export.py`（繋ぐのはまだ。下の 4） | ui.md・ops-board.md |
| 足回り | `surasura`（統一ブラウザ CDP 9222。`scripts/connect.mjs`・`chrome.sh`・`node_modules/playwright-core`。`ec-ad-ops/scripts/node_modules` と `advertorial/scripts/node_modules` は、ここへの相対リンク）。写しは `ec-ad-ops/scripts/lib/browser/`。`_env/venv`（道具用 Python 3.12：playwright・OpenCV・Pillow） | — |
| その他 | `mitame`・`kankopi`（UI の認識合わせ・完コピ）・`natural-japanese`・`i-have-adhd`・`vault`（鍵）・`dream`・`gstack` | — |

## 2. 旧ハーネスから写した物（2026-10-19。どこから → どこへ）
| 旧の場所 | 新の場所 | 中身 |
|---|---|---|
| `~/.claude/skills/<名前>`（リンク22本の実体） | `~/.agents/skills/<名前>/`（実体に） | ad-factory・advertorial・dream・dropshipping-product-research・ec-email・ec-harness・ec-native-ads・ec-research・ec-static-ads・ec-vsl・gstack・i-have-adhd・kankopi・mitame・native-ads・natural-japanese・surasura・teire・vault・website |
| `~/landing-page-skill/landing-page`・`voc` | `landing-page/`・`voc/` | 記事 LP（英語型） |
| `~/.claude/skills/ad-funnel` | `ad-funnel/` | 数字の取得（fetch.py・ops-board が使う） |
| 仮ハーネス `~/ec-ads/harness-draft-20261015-zackd/skills/*` | `bakuro-copy/`・`ranking-copy/`・`listicle-copy/`・`quiz-jp-copy/`・`kata-tsukuru/`・`vsl-sagasu/`（`~/.claude/skills` の古い版より新しい。差分は `kata-tsukuru/_仮ハーネスとの差分_20261016.md`） | 記事の形ごとのスキル |
| 仮ハーネス `ec-ad-ops/references/article/`・`tools/article/`・`ec-ad-ops/references/article.md` | `ec-ad-ops/references/article/`・`ec-ad-ops/tools/article/`・`article.md`（本物 10/18 と合流） | 記事の仕組み（友だちの advertorial-automation の写し） |
| 仮ハーネス `vsl-script/` | `vsl-script/`（10/19 午前に入れずみ） | 台本の決まり 第3.5版 |
| 仮ハーネス `研究/結果`・`試写の較正`・`台本/書き起こし.md`・`失敗の台帳.md`・`変えた所.md` | `vsl-script/研究/` | 台本の記録 |
| `~/Desktop/アーカイブ/台本の作り方_20261008/`・`動画ルール_20261010_…` | `ec-ad-ops/references/_archive/` | 14段の台本の型（名指しの時だけ）・前の映像の決まり |
| `~/Claude Code/kata-tsukuru/runs/quiz-jp/`・`advertorial-harness-examples/日本版_アンケート型_…`・`team-room/引き継ぎ/…/クイズ_日本/` | `ec-ad-ops/references/article/型の資料/runs/quiz-jp/`・`article/資料/実例/`・`article/資料/クイズ_日本/` | 記事の型の正本と実例 |
| `~/Claude Code/kata-tsukuru/runs/較正_記事/`・`team-room/引き継ぎ/…/日本の見本/` | `ec-ad-ops/references/article/型の資料/runs/較正_記事/`・`…/runs/quiz-jp/日本の見本/` | 審査役の較正の見本（本人の判定つき）・BODY-VO の実物（本文・HTML・画面・広告）。10/19 夕方に追加で写した |
| `~/Claude Code/venv`（Playwright・OpenCV） | `_env/venv`（`_env/setup_venv.sh` で作り直せる） | 道具用 Python |
| Obsidian `ec/構造/ハーネス/_取り込み元_advertorial-harness.md`・`EC攻略まとめ.md`・`EC/Konvert Native Ads講座/原文アーカイブ/` | `article/`・`ec-research/references/knowledge/obsidian/` | 読む資料 |
| `~/.claude/skills/surasura/scripts/connect.mjs`・`chrome.sh` | `surasura/scripts/`（実体）＋ `ec-ad-ops/scripts/lib/browser/`（写し） | 統一ブラウザの足回り |
| GitHub `tokunaritakakura-code/pdp-tsukuru`（c906a23・10/20。前は afb72a3） | `pdp-tsukuru/` | 店を作るスキル（新）。土台・検査の道具・ストア担当の審査・店だけの審査の箱が全部入った版。うちの読み替えは `references/harness-map.md` 5章 |
| `~/.claude/skills/ec-cs` | `ec-cs/`（10/19 夜。リンクでなく実体だったので一度目に漏れていた） | お問い合わせ（CS）のハーネス。surasura の import を新へ |
| `~/.claude/skills/fukikae/scripts/01_transcribe.sh` | `ec-ad-ops/scripts/transcribe_whisper.sh` | whisper-cli で文字起こし（1本だけの道具） |

パスの書きかえ：新ハーネスの中の `.md`・`.py`・`.mjs`・`.sh`・`.json` 約290ファイルで、旧の場所（`~/.claude/skills/`・`~/landing-page-skill/`・`~/Desktop/アーカイブ/`・`~/Claude Code/`・Obsidian・仮ハーネス）を新の場所に替えた。残っているのは、歴史として書いてある行（「元は〜」）と、友だちの環境にしか無い物（下の 3）だけ。

## 3-0. 旧ハーネスと仮ハーネスは片付けた（2026-10-20 Seiyo「仮ハーネスと昔のハーネスを消したい」）
- **`~/.claude/skills/` は全部、ここ（`~/.agents/skills/`）へのリンクになった**（43本。`synced/` は Claude のアプリが入れる物なので触っていない）。Claude Code はここのスキルを読む。前は ec-ad-ops・vsl-script・zackd-ad・higgsfield-* だけがリンクで、残りは旧の実体を読んでいた（pdp-tsukuru・listicle-copy・vsl-sagasu は読まれていなかった）
- ゴミ箱へ移した（`~/.Trash/旧ハーネス_20261020/`。空にするまで戻せる。約11GB）：旧 `~/.claude/skills/` の実体28件・`~/landing-page-skill/`・`~/Desktop/アーカイブ/台本の作り方_20261008/`・`動画ルール_20261010_…`・`~/Claude Code/`（全部）・`~/ec-ads/vsl-rules-draft-20261014/`・`~/ec-ads/_repos/`・仮ハーネス `~/ec-ads/harness-draft-20261015-zackd/`
- 消す前に確かめた事：台本のスキル（vsl-script）は仮ハーネスの最新（第3.5版）＋10/19 の K の読み方。映像の決まりは 17・18章に加え、仮ハーネスの通し試作の直しと道具を 18-6・`質感847/通し/` に入れた。旧の実体との差は、意図した更新とパスの書き換えだけ
- 直した依存：`~/.claude/hooks/kiji-guard.py`（runs の場所）・`~/seiyo-skills/sync.sh`（新ハーネスから写す。控え `sync.sh.bak-20261020`）・`質感847/通し/tools/pipe.py`（Python）・`article/型/_記事の作り方.md`
- 残る旧の名前：vsl-sagasu の Telegram（`~/Claude Code/毎日の制作`。元から無く未対応）、文書の中の「元は〜」の歴史の行。Obsidian の `ec/` は触っていない

## 3-1. 使っていないスキルを片付けた（2026-10-20 Seiyo「今の流れで使わないものは全部削除して」）
ゴミ箱 `~/.Trash/使わないスキル_20261020/` へ移した（空にするまで戻せる）：ad-factory・advertorial・dropshipping-product-research・ec-harness・landing-page・native-ads・teire・higgsfield-*（generate 以外の8本）。流れの文書（ec-ad-ops の SKILL.md・article.md・video-formats.md・creative-foundation.md）から landing-page の道を外した。残したのは、流れの中で使う物と、CLAUDE.md・設定が使う物（surasura・vault・dream・mitame・kankopi・natural-japanese・i-have-adhd〈プラグイン〉・gstack〈Codex の決まりが参照〉・voc〈記事の本物の声〉・website〈店を非公開テーマに置く〉・ec-vsl・ec-email・ec-cs・ad-funnel・higgsfield-generate〈動画・静止画が参照〉）

## 3. 旧を消す前に知っておく事（2026-10-19 に書いた。上の 3-0 で片付けた）
- **消してよい（新に写した）**：`~/.claude/skills/`（ただし `ec-ad-ops`・`vsl-script`・`zackd-ad`・`higgsfield-*` は新へのリンクなので、リンクだけ消える）・`~/landing-page-skill/`・`~/Desktop/アーカイブ/台本の作り方_20261008/`・`動画ルール_20261010_…`・`~/Claude Code/venv`・`~/Claude Code/kata-tsukuru`・`advertorial-harness-examples`・`team-room`・`~/ec-ads/vsl-rules-draft-20261014/`・`~/ec-ads/_repos/`
- **仮ハーネス `~/ec-ads/harness-draft-20261015-zackd/`**：決まりと記事の仕組みは新へ入れた。残っているのは 台本の実例（`原稿/`）・まとめの HTML（`まとめ/`）・研究の動画（`研究/` 4GB）・映像テスト・記事テスト・`_本物の前の版_*`（入れる前の控え）。記録として置いておく（消すなら Seiyo の判断）
- **消してはいけない（新ハーネスの外にあるが、使っている物）**：`~/Desktop/claude code/newec_harness/`（商品の事実と完成品）・`~/newec-dashboard/`（前の UI。新 UI に替えるまで）・`~/ec-ads/<商品>-<作業>-<日付>/`（作業の原本）・`~/ec-ads/supplier-discord/`（Discord の送受信の記録）・**`~/.claude/task-fleet/chrome-profile`（統一ブラウザのプロファイル。Discord・Meta・Shopify のログインが入っている。`~/.claude` を丸ごと消すと消える）**・`~/.cache/whisper/`・`~/.claude.json`（MCP の設定）
- **友だちの環境にしか無く、この Mac に無い物**：`06 店を作る.md`・`店の木_ワンドライ×ここちドライ.html`（読み物。無くてよい）、vsl-sagasu の Telegram（`~/Claude Code/毎日の制作/telegram.py`。未対応のまま）、team-room（友だちの審査の部屋）。**pdp-tsukuru の土台と検査の道具は 10/19 夜に友だちがリポジトリへ入れたので、もう無い物ではない**
- Obsidian は、決まりの置き場としては使わない。`teire`（Vault の点検）と `dream`（memory の整理）だけが Obsidian・`~/.claude` を見る（旧のまま。消すなら一緒に）

## 4. まだつながっていない所
- **新しい UI**（`zerogridcompany-cell/zerogrid-dashboard-ui`）：Seiyo の GitHub（seiyomiyazono）では 404（非公開か別の名前）。読めたら、工程6の出す形を UI に合わせる（`ec-ad-ops/references/flow.md` 4）
- **K ペルソナ**は決まりとひな形まで。新ワンドライ・新針マットの K は未作成（次の台本の前に作る）
- **店（4d）**：土台と道具がそろったので通しで動く（`新規.sh` → 仕上がり検査 → lint → 面の数字 をこの Mac で確かめた）。まだ本物の店は1つも作っていない
- **UI（6）**：新しい UI の仮データの形に写す道具（`ec-ad-ops/scripts/ui_export.py`）と対応表（`references/ui.md`）はできた。繋ぐのは最後に Seiyo と
- **旧 `~/.claude/skills` にあって新に無い物**：`synced/`（Anthropic のスキルの写し。うちの物ではない）・`website-copy/scripts`（`website/scripts` と同じ4本。写していない）

## 5. 記録
- 変えた所（仮ハーネスからの続き）：`vsl-script/研究/変えた所_仮ハーネス.md` 36〜40
- 失敗の台帳（2回で昇格）：`vsl-script/研究/失敗の台帳.md`
- 入れる前の本物：`~/ec-ads/harness-draft-20261015-zackd/_本物の前の版_20261019/`（vsl-script・ec-ad-ops・zackd-ad）
