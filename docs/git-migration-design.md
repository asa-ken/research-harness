# 設計書: equity-research-harness の Git 化

## 背景・目的

現行の `equity-research-harness` Skill は、案件ディレクトリ（`research/<case>/`）を
ローカルファイルシステム上に置く前提で作られている。

Ken の作業環境は Chromebook（Claude Desktop アプリなし、Cowork のローカルファイル
アクセス機能も使えない）。そこで、案件ディレクトリの実体を **GitHubリポジトリ** に置き、
ブラウザからの Claude.ai チャット（コード実行機能）が clone して動かす構成に変える。

**目標**: 現行スクリプト群（ゲートA/B、台帳構築、改善ゲート等）の判定ロジックは
一切変更しない。変えるのは「ファイルがどこにあるか」と「取得・反映の手順」だけ。

---

## 変更しないもの（重要）

- `scripts/harness_lib.py` 以下の全チェックロジック（A01〜A16, B01〜B17, S01〜S12）
- 案件ディレクトリの内部構造（`raw/`, `raw_text/`, `ledger.jsonl`, `sources.json`,
  `report.md`, `figures/`, `checks/`, `requests/`, `improvements/`）
- ゲートの実行証跡（`checks/receipt_*.json`）と `verify_gate.py` の検証方式
- **外部通信をしないという制約は維持する**。`tests/run_tests.py` の静的検査
  （`urllib.request` / `requests` / `socket` / `api.anthropic.com` 等の禁止）に、
  Git操作で新たに使うコマンド（`git`, `gh` CLI呼び出し）が引っかからないよう、
  検査対象を「Pythonの直接ネットワーク呼び出し」に限定するか判断が必要（後述）

---

## リポジトリ構成（新規）

```
<owner>/equity-research-cases/          ← Ken個人のプライベートリポジトリ（新規作成）
  skill/                                ← equity-research-harness の scripts/ references/ assets/ を格納
    scripts/...
    references/...
    assets/...
    tests/...
  research/
    <case-slug>/                        ← 案件ごと。既存のcase_dir構造そのまま
      raw/
      raw_text/
      figures/
      checks/
      requests/
      improvements/
      sources.json
      ledger.jsonl
      report.md
      scope.md
  README.md
```

**skill/ をリポジトリに同梱する理由**: チャット側が毎回 Skill 本体を持っているとは限らない
（Skillはユーザーのclaude.ai設定に紐づく）。clone一発でスクリプトも案件データも揃うほうが、
「今日はどのSkillバージョンで動いたか」が commit 単位で追跡できて安全。

Skill本体を更新したら `skill/` にコピーしてコミットする運用とし、
`skill/VERSION` のような1行ファイルでバージョンを持たせる（Skill側のSKILL.mdの内容と
乖離していないか、たまに突き合わせる）。

---

## フローの変更点

### 現行（ローカル前提）
```
init_case.py → (ユーザがファイル配置) → capture_source.py → build_ledger.py
→ run_gate.py --gate A → (レポート起草) → run_gate.py --gate B
→ extract_claims.py → (人/別セッションが判定) → verify_gate.py
```

### Git化後
```
1. [チャット] リポジトリをclone
     git clone https://github.com/<owner>/equity-research-cases.git /tmp/work
2. [チャット] skill/scripts を使い、既存フローをそのまま実行
     python3 skill/scripts/init_case.py research/<case> "対象名"
     ... (ソース配置、capture_source.py、build_ledger.py、run_gate.py 等 現行と同一)
3. [チャット] 変更をコミット（詳細は「書き込みの扱い」参照）
4. [人] GC工程: claims_review.md を新しいチャットに貼って判定
     → 判定結果を report.md や claims_review.md に反映
5. [チャット] 最終コミット・プッシュ
```

**現行スクリプトのCLIインターフェースは一切変えない。** 変わるのは
「案件ディレクトリの起点が `/tmp/work/research/<case>` になる」ことだけ。

---

## 書き込み（コミット・プッシュ）の扱い ★最優先・実装着手前に必ず検証

**方針は確定: 案B（書き込みまで自動化）を採用する。**
チャットで「cloneして進めて」と依頼するだけで、調査・ゲート実行・コミット・
プッシュまで自動で完結させる。GitHubのweb UIを手動で開く工程は無くす。

案A（プル専用・手動コミット）は不採用。参考として下部の「不採用案（参考）」に残す。

### 案Bの最優先タスク: トークンの安全な受け渡し方式

**これはCodeが実装に入る前に、着手時点で最初に検証すること。** 現時点で確証を
持って言えるのはここまで:

- GitHub Personal Access Token は **fine-grained、対象リポジトリ1つに限定、
  Contents: Read and write のみ** のスコープで発行する
- トークンを **チャットの本文に直接貼る運用は避ける**（チャット履歴に平文で残るため）
- Claude.ai には「接続（Connectors）」の仕組みがあり、GitHub連携がそこで完結できる
  可能性が高いが、以下は**未検証・要確認**:
  - Connectors経由のGitHub認証で、`git push` に使える形の資格情報が
    チャット実行環境（コード実行機能）側に渡るか
  - Web版とモバイルアプリ版で、Connectorsの挙動・認証フローが同一か
    （**Kenの主な利用シーンはPC=Chromebookのブラウザだが、スマホからの
    利用も想定するため、両方で同じ手順になるかは必ず確認すること**）
  - コード実行環境からの外向き通信で `git push`（ネットワーク上はHTTPS経由の
    git操作）が許可されているか。現状確認できているのは `github.com` /
    `codeload.github.com` への読み取り系アクセスのみで、書き込み系
    （認証付きpush）が同条件で通るとは限らない

この検証が終わるまでは、**フォールバックとして「プル専用＋手動コミット」の
手順（旧・案A、下部に残した内容）をそのまま使える**ようにしておく。
つまり実装は「まず案Aの手順で動くことを確認 → トークン受け渡し方式が
固まり次第、コミット・プッシュ部分だけ差し替えて自動化する」という
2段階で進めるのが安全。

> **2026-08-24 追記（一部解決）**: **Claude Code on the web** のセッションでは、
> PAT不要で解決した。セッション自体がリポジトリごとにスコープされたpush用の
> 資格情報（`GITHUB_TOKEN` / `GIT_ASKPASS` によるプロキシ型認証）を最初から
> 持っており、Kenが手動でPATを発行・貼り付ける必要はない。実際にこの経路で
> `git push` が通ることを確認済み（下記「実装状況」参照）。
>
> ただし**これはKenが実際に使う想定の経路（claude.aiのチャット＋コード実行機能、
> Chromebookのブラウザ／モバイルアプリ）とは別のプロダクト**。Claude Code on the web
> でのpush成功をもって、claude.aiチャット側の書き込みが同様に通ると断定はできない。
> 特にモバイルアプリでの動作は未確認のまま残っている。

### 案Bが完成した場合の運用（確定後の姿）

```
①PCでもスマホでも、Claude.aiのチャットを開く
②「このリポジトリをcloneして案件を進めて」と依頼
③チャットが調査・ゲート実行・コミット・プッシュまで自動で行う
④GCだけ新しいチャットに貼って判定（Git化と無関係、常に手動）
⑤判定結果を元のチャットに戻す → 自動で反映・コミット
```

トークン漏洩・誤プッシュのリスクは残るため、**対象リポジトリを他の用途と
共有しない**（このハーネス専用の小さいリポジトリに閉じる）ことをスコープ限定の
代替防御とする。

---

### 不採用案（参考）: プル専用フォールバック

トークン検証が終わるまでの暫定手順、または最終的に案Bが技術的に困難と判明した
場合のフォールバックとして残す。

- チャット側のコード実行環境は `git clone`（読み取り）のみ行う
- 生成物（ledger.jsonl, report.md, checks/, requests/ の更新等）は
  チャットの `present_files` / ダウンロード機能で都度Kenに渡す
- Kenが手元でGitHubのweb UI（Chromebookのブラウザで十分）にドラッグ&ドロップ、
  または `github.dev`（VSCode for the Web、ブラウザだけで動く）でコミット
- チャットセッションはGitHub認証情報を一切持たない（安全だが手動コミットが残る）

---

## capture_source.py の変更点

現行は `local_path` に相対パスを想定しており、そのままGit化後の構成でも動くはず
（cloneしたルートからの相対パスであれば無変更で通る）。確認事項:

- [ ] `raw/` に置いたPDF等がGit管理下で正しくバイナリとして扱われるか
      （`.gitattributes` で `raw/**/*.pdf binary` 等の指定が要るか確認）
- [ ] リポジトリサイズの上限（GitHubは単一ファイル100MB上限、リポジトリ全体は
      ソフト上限あり）。有報PDF等は数MB程度が通例なので通常は問題ないはずだが、
      案件数が増えたときの累積サイズは要監視

---

## verify_gate.py / receipt の扱い

現行の受領証跡（`checks/receipt_*.json`、ファイルハッシュ埋め込み）は
**Git化後もそのまま機能する**。むしろGitのcommitハッシュと二重の証跡になり、
改竄検知はより強固になる。

追加検討: `receipt_*.json` に、生成時点の **git commit hash** も併記するか。
（`git rev-parse HEAD` を受領証跡に足すだけの小さな変更。任意）

---

## GitHub連携の技術的な注意点（Codeが実装時に確認すること）

1. **既存のネットワーク許可ドメイン**: このSkillのbashツールは
   `github.com`, `codeload.github.com` へのアクセスが許可されている
   （このチャット環境で確認済み）。ただし**Claude Code側の実行環境で
   同様の許可があるかは別途確認が必要**。環境ごとにネットワーク設定が異なりうる
2. `git clone` に認証が要るプライベートリポジトリの場合、案Aでは
   読み取り専用の認証手段（Deploy Key の read-only、または
   fine-grained PAT の Contents: Read のみ）を検討する
3. **`tests/run_tests.py` の静的検査**（外部通信禁止）は、Git化後は
   「スクリプト自体はネットワークに触れない」という制約はそのまま維持しつつ、
   「clone/pushはSkillの外側（チャット環境・Kenの操作）の責務」と明確に分離する。
   スクリプト本体に `git` コマンド呼び出しを埋め込まないこと
   （＝オーケストレーションはSkillの外、判定ロジックはSkillの中、という境界を保つ）

---

## GCワークフローへの影響

前段のやり取りで確認した通り、GitHub化はGCの自動化そのものには寄与しない
（独立性の問題であってファイル所在の問題ではないため）。変わるのは受け渡し経路のみ:

```
現行: claims_review.md をダウンロード → 新しいチャットに貼る
Git化後: claims_review.md をコミット → GitHub上で内容を確認しつつ、
         同じ内容を新しいチャットに貼る（コミットは記録のため、判定はやはり手動）
```

---

## 移行手順（Codeへの依頼として渡せる粒度）

1. GitHubに新規プライベートリポジトリを作成（`equity-research-cases` 等）
2. 現行Skillの `scripts/`, `references/`, `assets/`, `tests/` を `skill/` 配下にコピー
3. 案Aの書き込みフロー（プル専用）で、1案件分をエンドツーエンドで動かして検証
   - clone → init_case.py → capture_source.py → build_ledger.py
   - run_gate.py --gate A/B → 生成物をダウンロード → 手動でweb UIからコミット
4. `.gitattributes` の要否を確認（PDF等バイナリの扱い）
5. `tests/run_tests.py` をGit化後の構成でも実行し、64件全成功を確認
   （このテストスイート自体はファイルパスに依存しないので、Skillのディレクトリを
   どこに置いても動くはず。念のため確認）
6. 動作確認が取れたら、`references/independent-review.md` と `SKILL.md` に
   「Git運用時の手順」を追記（このドキュメントの内容を反映する形で）

---

## Codeへの申し送り事項（未決定・要判断）

- [ ] **最優先**: トークンの安全な受け渡し方式（Connectors経由か、他の手段か）を検証する。
      PCブラウザとスマホアプリで同じ手順になるかを必ず両方で確認する
- [ ] コード実行環境から `git push`（認証付き）が技術的に通るか確認する
      （読み取り系のgithub.comアクセスとは別に検証が要る）
- [ ] リポジトリ名・可視性（プライベート・専用リポジトリ前提で書いたが確認）
- [ ] `skill/VERSION` のようなバージョン管理をどこまで作り込むか（過剰実装を避ける）

## 移行手順の優先順位（更新）

1. トークン受け渡し方式の検証（最優先タスク、上記参照）
2. 検証が終わるまでは「不採用案（参考）」の手順で1案件分をエンドツーエンドに動かし、
   ロジック面（clone・ゲート実行・生成物の中身）に問題が無いことを先に確認
3. トークン方式が固まり次第、コミット・プッシュだけを自動化に差し替える
4. `tests/run_tests.py` をGit化後の構成でも実行し、64件全成功を確認
5. 動作確認が取れたら、`references/independent-review.md` と `SKILL.md` に
   Git運用時の手順（案B確定後の姿）を追記する

この設計書はロジックの変更を含まない、純粋な「置き場所と受け渡し手順」の設計。
既存の64件のテストが通ることを、移行完了の判定基準とする。

---

## 実装状況（2026-08-23 更新）

移行手順 1〜5 のうち、**このセッションで実施できる範囲**を完了した:

- リポジトリ構成を作成（`skill/` に Skill 本体をコピー、`research/` を新設）
- `skill/tests/run_tests.py` を新しい配置で実行し、**64/64 成功**を確認
  （パス非依存の実装のため無変更で動作）
- 「不採用案（参考）: プル専用フォールバック」の手順で、スモークテスト案件
  （`_smoketest`、コミットはしていない）を使い
  `init_case.py → capture_source.py → build_ledger.py → run_gate.py --gate A（PASS）
  → run_gate.py --gate B（図解未作成のため意図通りFAIL）→ verify_gate.py（レポート
  改変を正しく検知）` のエンドツーエンドを確認。判定ロジックは無変更で機能した
- `.gitattributes` を追加（`raw/` 配下のバイナリ・改行コードの扱い）
- `tests/run_tests.py` の `FORBIDDEN` 静的検査は `skill/scripts/*.py` のみを
  スキャンする実装であることを確認済み。git/gh 呼び出しをスクリプト側に
  埋め込まない限り、検査対象の変更は不要（設計書の想定通り、無変更で成立）

**このセッションでは検証できなかったもの**（Kenの実環境が必要なため）:

- トークンの安全な受け渡し方式（Connectors経由か等）。Claude.aiのConnectors設定や
  モバイルアプリの挙動は、このセッション（Claude Code側の実行環境）からは
  確認できない
- コード実行環境（claude.aiのチャット側）から認証付き `git push` が通るかどうか。
  これも claude.ai 側チャットでの実地確認が必要
- リポジトリの可視性（Private化されているか）はGitHub側の設定確認が必要

したがって現状は「案A（プル専用）で動作確認済み、案Bへの切替は要検証」の段階。
`README.md` には現時点で確認済みの手順（案A相当）のみを記載した。

---

## 構成変更（2026-09-05）: Skill 本体を別リポジトリへ分離

> **2026-09-06 追記: この分割は同日に取り消し、1リポジトリへ再統合した。**
> 経緯と理由は末尾の「構成変更（2026-09-06）: 1リポジトリへ再統合」を参照。
> 分割していた期間は約1日で、その間に実案件は1件も作成されていない。
> 以下はその分割時点の記録として残す。

Skill 本体を `asa-ken/research-harness` に独立させたため、このリポジトリの
`skill/` は削除した。役割はこうなる:

| リポジトリ | 中身 |
|---|---|
| `asa-ken/research-harness` | Skill 本体（29ファイル、テスト156件） |
| `asa-ken/stock-research` | 案件データ（`research/<case-slug>/`） |

**この設計書の「skill/ をリポジトリに同梱する理由」は、この変更で一部無効になる。**
同梱の狙いは「clone一発で揃う」ことと「どの Skill バージョンで動かしたかが
commit 単位で追える」ことだったが、2リポジトリに分けたことで:

- clone は2回必要になった（実務上の負担は小さい）
- **バージョン追跡性は弱まった**。案件の commit を見ても、そのとき使った
  Skill のバージョンは分からない

補う場合は、この設計書が任意項目として挙げていた
「`receipt_*.json` に生成時点の git commit hash を併記する」を、
`research-harness` 側の commit hash に対して行うのが素直。未実装。

---

## 実装状況（2026-08-24 更新）

Ken からアップロードされた更新版 Skill（個別企業特化への範囲明確化とボトルネック
分析の統合、判定ロジックは無変更）を `skill/` に全置換で反映した。手順は
`c534c256-codehandoff.md` の指示どおり: 26ファイルの過不足確認 →
`skill/tests/run_tests.py` で **64/64 成功**を確認 → コミット。
`scripts/context_check.py` の混入は無し。

同ハンドオフに記載の通り、**トークン受け渡し方式は Claude Code on the web に
限っては解決した**（PAT不要、セッションのプロキシ型認証で `git push` が通る。
上記「案Bの最優先タスク」の追記を参照）。ただし claude.ai チャット（Kenが実際に
使う経路）での挙動、特にモバイルアプリでの確認は依然として未実施。
これは前回セッションでKenに伝えた区別（Claude Code on the web ≠ claude.aiチャット）
と同じ内容で、ハンドオフ側の「未解決事項」にも同じ論点が残されている。

---

## 構成変更（2026-09-06）: 1リポジトリへ再統合

**決定**: 2026-09-05 の2リポジトリ分割を取り消し、`asa-ken/research-harness` に
Skill 本体と案件（`research/`）を統合する。このファイル自体も、統合に伴い
`stock-research` から `research-harness/docs/` へ移した。

### なぜ分割したのか（2026-09-05 の経緯）

分割は**積極的な設計判断ではなかった**。Claude Code 側とチャット側で別々に話が進み、
`skill/` が両リポジトリに重複して二重管理になった（`stock-research` 側が旧版:
26ファイル・テスト64件、`research-harness` 側が新版: 29ファイル・テスト157件）。
「重複を解消したい」という要請に対し、`stock-research` から `skill/` を削除して
役割を分ける形で処理したのが分割の実体である。

### なぜ統合するのか

1. **追跡性の問題が構造的に解消する。** 分割時に「バージョン追跡性が弱まった」と
   上に記録したとおり、案件の commit を見てもそのとき使った Skill のバージョンが
   特定できなかった。これは配管（`docs/ci-design.md`）の目的と正面から衝突する。
   配管が証明しようとしているのは「レポートが本当に検査を通ったか」だが、
   **検査したスクリプトのバージョンが特定できなければ証明は不完全**になる。
   後から「あの時点の検査に穴があった」と判明したとき、影響範囲を追えない。
   同一リポジトリなら案件と検査コードが同じコミットに紐づくため、この問題は消える。
   補償策として挙げていた「receipt に commit hash を併記」も不要になる。
2. **分割の理由が既に消えている。** `skill/` の重複とバージョン乖離は解消済みで、
   分割を維持する理由が残っていない。
3. **Skill と案件を分けておきたい意向が無い**ことを確認した（2026-09-06）。

### 検討して採らなかった案

分割を維持したまま `case-verify.yml` を `stock-research` 側に置き、CI 内で
`research-harness` を clone する案。**採らない理由**: 「どのバージョンを clone したか」が
再び曖昧になり、追跡性の問題が形を変えて残るため。

### 統合後の構成

```
asa-ken/research-harness/
  SKILL.md / scripts/ / references/ / assets/ / tests/   Skill 本体
  improvements/                                          Skill 自身の自己改善記録
  research/<case-slug>/                                  案件データ
  docs/ci-design.md                                      CI配管の設計書
  docs/git-migration-design.md                           このファイル
  .github/workflows/                                     skill-tests.yml / case-verify.yml
  .gitattributes                                         raw/ 配下のバイナリ・改行コードの扱い
```

`asa-ken/stock-research` は統合により役割を失う。扱いは Ken の判断を待つ。
