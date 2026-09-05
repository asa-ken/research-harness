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
