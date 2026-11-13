# 取り込み元（2026-10-12）

この `ec/構造/`・`ec/wiki/`・`ec/決めたこと.md` は、https://github.com/tokunaritakakura-code/advertorial-harness（d7b7934・2026-10-12）の `vault/ec/` をそのまま写した物。Seiyo「記事のスキルをハーネスに組み込んで。今後は動画を作るたびに記事をどうするか毎回考える」。

| 取り込んだ物 | 置いた場所 |
|---|---|
| `claude-skills/`（quiz-jp-copy・kata-tsukuru・bakuro-copy・ranking-copy・website-copy・fukikae） | `~/.agents/skills/<名前>/` |
| `claude-code/`（ec-harness の検査・kata-tsukuru の runs・team-room の引き継ぎ資料・adv-kata） | `~/Claude Code/` |
| `examples/`（作った見本3本＋SASAE で殻にした「パッドの敵」） | `~/Claude Code/advertorial-harness-examples/` |
| `claude-hooks/kiji-guard.py` | `~/.claude/hooks/kiji-guard.py`（settings.json の PreToolUse Bash・PostToolUse Write|Edit） |
| 道具用の Python（Playwright・Pillow・numpy・OpenCV） | `~/.agents/skills/_env/venv/bin/python`（`python3` に無い時はこれで打つ） |

Seiyo のハーネスからの入口は `~/.agents/skills/ec-ad-ops/references/article.md`（記事の作り方）と `video-formats.md`（動画の後に記事）。SASAE で作った実例は `~/ec-ads/sasae-article-20261012/`。

# 取り込み（2026-10-20）: advertorial-automation 6884358・pdp-tsukuru c906a23

友だちの最新版に合わせた。元は `~/ec-ads/_gh/advertorial-automation`（2566010 の後の 237e6ba・e809ba0・af6a82a・d91ab5c・6884358）と `~/ec-ads/_gh/pdp-tsukuru`（afb72a3 の後の cd2e066〜c906a23）。3方向でまぜ、パスはうちの書き方にし、Seiyo の決まり（`ec-ad-ops/references/article.md`）の行は消さずに残した。食い違う所は Seiyo の決まりを取った。入れる前の元は `~/ec-ads/_gh/_控え_20261020/`（`~/.agents/skills/` からの同じ相対パス）。

| 入れた物 | 置いた場所 | 中身 |
|---|---|---|
| 記事の型を VSL ごとに選び分ける（237e6ba） | `型/_VSLから型を選ぶ.md`・`05 記事を作る.md` 手順2・`決めたこと.md` | 普通の中を3つ（物語型・権威の暴露・調査暴露型）に分け、VSL の線で選ぶ |
| 物語型・調査暴露型の段の芯（新規） | `型/A03 派生 物語型記事/_分解.md`・`型/A03 派生 調査暴露型記事/_分解.md` | 段の表。生の段・画像は友だちの手元（うちには無い）と書いた |
| 声と研究を本物から取る（237e6ba） | `05 記事を作る.md` 手順5・`型/_仕掛けの棚.md` の H | 声は原文のまま4本以上。友だちの `voc.py` はうちに無いので `voc` スキルか共通 Chrome で取る |
| 題の型（6884358。新規） | `型/_題の型.md`・`役/編集長.md` 関門10・`05` 手順9 | 題の関門・型・声の決まり |
| 残った疑いの重さ（d91ab5c） | `型/_買うまでの15の事.md`「残った疑いの重さと答え方」・`05` 手順3・5c・5④・`役/編集長.md` 関門11・`tools/article/記事の検査.py` 6d・7・8・`adv-kata/新規.sh` の表 | 重さ1は値段の段より前の本文で答え切る。FAQ と「〜によります」で済ませない |
| 審査の箱の店の分かれ道（e809ba0・af6a82a） | `tools/article/審査を回す.py` | `店の印.json` があれば pdp-tsukuru の `店の検査を回す.py` と `ストア担当の審査.md` の2節を使う。絵の一覧（16枚を1枚に）・`絵と説明の一覧.tsv`・`照らし合わせ_<回>.txt` も束に入れる。img/ を直した回も「直した」と数える |
| 値段の段の道具（237e6ba） | `tools/article/kata-tsukuru/値段の段を組む.py` | 送料無料がセールの間だけの時の書き方・内訳・3年の比べの直し。「星」の出し分けと顔写真なしはうちのまま |
| 4スキルの SKILL.md（6884358） | `bakuro-copy`・`listicle-copy`・`quiz-jp-copy`・`ranking-copy` | C3 の書き方。C5（VSL のビジュアルを使わない）はそのまま（C4 は 2026-10-20 に外した） |
| 名前替え「テスト用に決めた値.md」→「決めた値.md」 | 記事の文書・スキル全部。道具（`審査を回す.py`・`引き継ぎの検査.py`・`記事の仕上がり検査.py`）は両方の名前を受ける | 前の作業フォルダ（立ち仕事マットの記事など）はそのまま通る |
| pdp-tsukuru c906a23 | `~/.agents/skills/pdp-tsukuru/` | 店だけの審査の箱 `scripts/審査を回す.py`・`絵を置く.py`・`往復とカート.mjs`・`照らし合わせの指示文.md`・`直しの記録.md`・`見本/`。SKILL.md は友だちの新しい形に、うちの読み替えを入れ直した（`references/harness-map.md` 5章） |
| VSL→記事の受け渡しに重さ | `vsl-script/references/記事と分ける.md` 5章・`15の対応表.md` 2-3 | 引き継ぎ票に秒と「残した疑いと重さの候補」の1行。約束した事と最後の問いは重さ1で、票の ⑭ に入れない |

入れなかった物と理由:

| 物 | 理由 |
|---|---|
| `skill-creator/check-undug.py`・`team-room/isolation.mjs` | うちのハーネスに無い部分（部屋・skill-creator の友だち版） |
| 決めたことの CS の行（返金・倉庫・Telegram・arukoto-cs）13行 | 友だちの店の CS の決め。記事・店の仕組みに関係しない。うちの CS は `ec-cs` スキル |
| 決めたことの「advertorial-automation を公開にする」「店の部分は上げない」 | 友だちの GitHub の扱い。うちは commit・push を本人の指示の時だけにしている |
| 審査の決まりの「Claude が決めた専門家の名前と生成した顔は落とさない」 | 友だちの元の文のまま（2026-10-20 に戻した。pdp-tsukuru の `ストア担当の審査.md` も元の行） |
| 審査の箱の「部屋が止まった時に出し直す」（team-room の room.db を読む） | うちは部屋を立てず、回ごとに新しいサブエージェントに頼む |
| `founder-adv` スキル・`voc-research` の道具・`fedotoff-200`・`kokochi-4hon` の生の資料 | 友だちの手元だけにある。文書には「うちには無い。〜で代える」と書いた |
