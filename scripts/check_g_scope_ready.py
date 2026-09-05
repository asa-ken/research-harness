#!/usr/bin/env python3
"""check_g_scope_ready.py - 調査に入る前の入口チェック（I-104）

「何を調べるべきか」のリスト（必要証拠リスト）が空欄・雛形のまま次工程へ
進むと、『重要な証拠が未取得なら止める』という後段の安全装置ごと無効になる
（実運用でI-104として表面化）。ここを入口で塞ぐ。

G01: 必要証拠リストに、中身のある行が1つも無い（雛形の空行しかない）。
     → 何を調べるかが未定のまま進んでいる。
G02: 重要度Critical(C)の行が1つも無い。
     → 結論を左右する証拠が1つも定義されておらず、後段のC検査が空回りする。
G03: 問い（何を判断したいか）が未記入。
     → 何のための調査か決まっていない。

段階導入の例外: G01/G02/G03 はいずれも FAIL（入口で止める）。
ここは「準備の骨組みが無い」という致命的な欠落なので、警告では意味がない。
ただしClaudeが縮退運用を明示宣言した場合のみ、後述の運用ルールに従う。

usage: python3 scripts/check_g_scope_ready.py <case_dir>
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import CheckResult, case_path, read_text, print_and_exit  # noqa: E402


def parse_evidence_rows(scope_text):
    """必要証拠リストの表から、中身のある行を取り出す。

    戻り値: [(id, 要件, 重要度, 想定ソース, 状態), ...]
    雛形の空行（要件が空）は除く。
    """
    if not scope_text:
        return []
    m = re.search(r"##\s*必要証拠リスト.*$", scope_text, re.MULTILINE)
    if not m:
        return []
    section = scope_text[m.end():]
    nxt = re.search(r"^##\s", section, re.MULTILINE)
    if nxt:
        section = section[:nxt.start()]

    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        # ヘッダ行と区切り行を除く
        if cells[0] in ("ID", "") or set(cells[0]) <= set("-: "):
            continue
        _id, req = cells[0], cells[1]
        # 要件が空＝雛形の空行。中身のある行だけ拾う。
        if not req:
            continue
        rows.append(tuple(cells[:5]))
    return rows


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックG: 調査入口の準備(I-104)")
    scope = read_text(case_path(case_dir, "scope.md")) or ""

    # G03 問いが未記入
    qm = re.search(r"問い（何を判断したいか）[:：](.*)$", scope, re.MULTILINE)
    if not qm or not qm.group(1).strip():
        res.add("G03", "FAIL", "scope.md",
                "問い（何を判断したいか）が未記入。何のための調査か決まっていない",
                "『問い（何を判断したいか）:』の後に、判断したいことを一行で書く")

    rows = parse_evidence_rows(scope)

    # G01 中身のある行が1つも無い
    if not rows:
        res.add("G01", "FAIL", "scope.md",
                "必要証拠リストに中身のある行が1つも無い（雛形の空行のみ）。"
                "何を調べるかが未定のまま。この状態では後段の『重要証拠が未取得なら止める』"
                "検査ごと無効になる",
                "結論を左右する証拠を、証拠要件・重要度・想定ソースを埋めて登録する")
        return res

    # G02 Critical行が1つも無い
    has_critical = any(len(r) >= 3 and r[2].upper().startswith("C") for r in rows)
    if not has_critical:
        res.add("G02", "FAIL", "scope.md",
                "重要度Critical(C)の証拠要件が1つも無い。結論を左右する証拠が未定義で、"
                "後段のCritical網羅チェックが空回りする",
                "結論の決め手になる証拠を最低1件、重要度Cで登録する")

    return res


if __name__ == "__main__":
    print_and_exit([run(sys.argv[1])], "チェックG 実行結果",
                   sys.argv[1] if len(sys.argv) > 1 else ".", "G")
