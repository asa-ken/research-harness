#!/usr/bin/env python3
"""init_case.py - 調査案件のディレクトリ雛形を作る。

usage: python3 scripts/init_case.py research/<case_name> ["調査対象名"]
"""
from __future__ import annotations

import os
import sys
from datetime import date

SKEL = {
    "sources.json": "[]\n",
    "ledger.jsonl": "",
    "report.md": None,           # assets からコピー
    "requests/needed_sources.md": """# 情報提供依頼一覧

Claudeが到達できなかった資料です。提供いただけると調査精度が上がります。

""",
    "improvements/inbox.jsonl": "",
    "improvements/decision_log.md": "# 改善 採否ログ\n\n",
    "improvements/case_terms.txt": "__SEED_TARGET__",  # main()でtargetを自動シード
    "search_log.jsonl": "",  # 飽和判定の根拠。1行1回の探索試行を記録する
    "reverify_log.jsonl": "",  # 原典再アクセスの検証台帳。収集直後に1行ずつ記録する
}

SCOPE_TMPL = """# 調査スコープ

- 対象: {target}
- 起票日: {today}
- 問い（何を判断したいか）:
- 期間軸:
- 深度: サマリ / 標準 / 深掘り
- 鮮度基準（既定）: 24 ヶ月より古い情報は警告（トレンドの速い論点では追加論点ごとに短く上書きする）
- 既存の持ち物（ユーザ提供済み資料）:

## 初期仮説

| ID | 仮説 | 崩壊条件 | 優先度 |
|---|---|---|---|
| H1 |  |  | H |
| H2 |  |  | M |

## 採用した問い（references/questions.md からID選択。仮説を立てた後に選ぶ）

| ID | 問い | 選んだ理由（どの仮説に効くか） |
|---|---|---|
| Q-R4 | この仮説が間違っていたと分かるのは、どの数字がどうなったときか | 必須 |

選ばなかった問いはレポートに列挙しない（スコープ宣言で一括処理）。

## 必要証拠リスト（何が分かれば結論が変わるか）

重要度: **C**=Critical（これが無いと結論が出ない） / N=Normal（精度が落ちる）
状態: 未取得 / 取得済(E-xxxx) / 非公表 / 調査不可 / 未特定(N-xx)

| ID | 証拠要件 | 重要度 | 想定ソース | 状態 |
|---|---|---|---|---|
| N-01 |  | C |  | 未取得 |

**Critical項目が未取得のまま残っている場合、ゲートBはFAILする（B22）。**
取得できなかった場合は、[非公表]または[調査不可]としてレポート本文で
扱うか、重要度をNに落とす判断を明示すること。

**Critical判定は案件ごとにここで決める。** 外部の判定基準（他業種向けSkillの
固定リスト等）を持ち込まない。「これが無いと結論が変わるか」だけで判断する。

### Critical項目を「未特定」で閉じる場合

探索を尽くしても見つからない場合は `[未特定|対象:N-xx]` とし、`search_log.jsonl`に
飽和の記録を残す（`references/workflow.md`「飽和基準」参照）。
「未探索（手を付けていない）」と「未特定（尽くしたが分からなかった）」は別物であり、
探索ログの裏付けなしに未特定と書くことはできない。

## 追加論点（納品後の追加質問はここに1ブロックずつ足す）

初回調査の後に来た追加の問い（「〜は優位か」「〜は本当か」等）は、
調べ始める前にここへ1ブロック追記する。ブロックが埋まっていないと
ゲートQ（run_gate.py --gate Q）がWARN/FAILする。

**深掘りの前に、評価軸とトレンドを一緒に調べる。** 「この分野で優劣は何を基準に
語られているか」を複数ソースで調べると、「今なぜその基準が重視されるのか」という
背景（トレンド）も同じ調査で分かる。そこから鮮度基準（何ヶ月より古いと危ないか）も決める。

<!-- 追加論点ブロックの様式（コピーして使う）
### 追加論点 N: <問いを一行で>
- 決定的証拠: <この問いの結論を左右する証拠。1件以上>
- 評価軸（「優位・競争力・技術力・先行」型の問いのときのみ）:
    - <軸1> … 出所: <どのソースで、この軸が重要と分かったか>
    - <軸2> … 出所: <...>
    - <軸3> … 出所: <...>
  ※軸は記憶で先に固定せず、軸を探す調査をしてから書く。
  ※出所の無い軸ばかりが並ぶときは「他に軸はないか、外の情報源で確かめたか」を問い直す合図。
- 発言の一次確認（検証対象が「誰かの発言」のときのみ）:
    - <誰の発言> → 出所: <動画の該当箇所/登壇資料/IR など一次情報の場所>
- 鮮度基準: この論点では <N> ヶ月より古い情報は警告。理由: <トレンドの動く速さ>
  ※この論点のための証拠には、台帳で topic:<この論点の番号> を付けると、
    その証拠だけこの鮮度基準で判定される（付けなければ案件既定の基準）。
-->

"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "(未記入)"
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for sub in ["raw", "raw_text", "figures", "checks", "requests", "improvements"]:
        os.makedirs(os.path.join(case_dir, sub), exist_ok=True)

    for rel, content in SKEL.items():
        path = os.path.join(case_dir, rel)
        if os.path.exists(path):
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if content == "__SEED_TARGET__":
            # 対象企業名を汎用性ゲート(T1固有名詞テスト)の除外語として自動シードする。
            # 空欄のまま放置されがちなファイルなので、手を付けなくても最低限機能するようにする。
            content = ("# この案件の固有名詞を1行1語（汎用性ゲートT1で使う）\n"
                      "# 起票時に対象名を自動シード済み。セグメント名・子会社名等を追記すること\n")
            if target and target != "(未記入)":
                content += target + "\n"
        elif content is None:
            src = os.path.join(skill_dir, "assets", "report_skeleton.md")
            content = open(src, encoding="utf-8").read() if os.path.exists(src) else "# レポート\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    scope = os.path.join(case_dir, "scope.md")
    if not os.path.exists(scope):
        with open(scope, "w", encoding="utf-8") as fh:
            fh.write(SCOPE_TMPL.format(target=target, today=date.today().isoformat()))

    print(f"作成: {case_dir}")
    print("次: scope.md を埋めてユーザ合意(G0) → ソース登録 → capture_source.py")


if __name__ == "__main__":
    main()
