# research-harness

`equity-research-harness` Skill 本体と、その調査案件データを置くリポジトリ。

ローカルファイルアクセスの無い環境（Chromebook 等）からでも、このリポジトリを
clone すれば検査スクリプトと案件データの両方が揃い、調査を進められる。

## 構成

```
SKILL.md                Skill 本体の入口
scripts/                判定ロジック（検査はここでしか行わない）
references/             フェーズ別手順・証拠台帳の規則・ステータス語彙など
assets/                 スキーマとテンプレート
tests/run_tests.py      網羅テスト（157件）
improvements/           Skill 自身の自己改善記録（I-101〜）

research/<case-slug>/   案件データ。case_dir 構造そのまま
                         raw/ raw_text/ ledger.jsonl sources.json
                         report.md figures/ checks/ requests/ improvements/

docs/ci-design.md              CI配管の設計書（なぜこう作ったか）
docs/git-migration-design.md   Git化の設計書と構成変更の経緯
.github/workflows/             skill-tests.yml / case-verify.yml
```

**Skill と案件を同じリポジトリに置いている理由**は `docs/ci-design.md` の判断1を参照。
要点は、案件と検査コードが同じコミットに紐づくことで
「どのバージョンの検査を通したか」が特定できるようになること。

## 使い方

```bash
git clone https://github.com/asa-ken/research-harness.git
cd research-harness

python3 scripts/init_case.py research/<case> "対象名"
# raw/ にソース原本を置き、sources.json に登録してから
python3 scripts/capture_source.py research/<case>
python3 scripts/build_ledger.py  research/<case>
python3 scripts/run_gate.py      research/<case> --gate A
python3 scripts/run_gate.py      research/<case> --gate B
python3 scripts/extract_claims.py research/<case>   # → checks/claims_review.md を新しいチャットに貼ってGC判定
python3 scripts/verify_gate.py   research/<case> --gate B
```

## 自動検証（GitHub Actions）

Claude の自己申告に依存せず、GitHub 側で機械的に検査を走らせて結果を記録する。
設計意図・前提・検証できる範囲は `docs/ci-design.md` を参照。

| ワークフロー | 動くとき | 内容 |
|---|---|---|
| `skill-tests.yml` | `scripts/**` `tests/**` の変更、PR、手動 | `tests/run_tests.py`（157件） |
| `case-verify.yml` | `research/**` の変更、PR、手動 | 各案件に `run_gate --gate all` → `verify_gate --gate B` |

`case-verify.yml` は検査失敗時も打ち切らず全案件を実行し、1件でも失敗すれば
ワークフロー全体を失敗にする。案件が1つも無い場合は「検査対象なし」で正常終了する。

**テスト件数について**: 157件目は openpyxl に依存する Excel 実ファイル検証。
未導入の環境では `[SKIP]` されて 156/156 と表示されるが、これは失敗ではない。
CI では openpyxl を導入して件数を固定している。
