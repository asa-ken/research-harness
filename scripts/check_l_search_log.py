#!/usr/bin/env python3
"""check_l_search_log.py - 探索ログの多様性検査（V37/V38相当）

飽和を宣言するための「経路もクエリも異なる3件」という条件は、
S14（lint_status.py）が個々の宣言時に検証する。
このスクリプトはそれとは別に、探索ログ全体を走査し、
「経路は分けたが実質同じ検索だった」という兆候を早期に発見する。

L01 (V38相当): 同一項目・同一ステージ内で、経路(route)が異なるのに
               クエリ(query)が完全一致している組がある。
               経路を分けたことになっているが、同じ検索を繰り返しただけの兆候。
L02 (V37相当): 独立再検証(stage=reverify)のクエリが、収集時(stage=collection)の
               クエリと完全一致している。多様性が確保されていない。
               reverifyステージが存在しない案件では該当なし（該当機構は未実装）。

usage: python3 scripts/check_l_search_log.py <case_dir>
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import CheckResult, load_search_log, print_and_exit  # noqa: E402


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックL: 探索ログの多様性(V37/V38相当)")
    rows = load_search_log(case_dir)
    if not rows:
        res.add("L00", "WARN", "search_log.jsonl", "探索ログが空。飽和判定の根拠が残せない")
        return res

    by_item_stage = defaultdict(list)
    for r in rows:
        by_item_stage[(r.get("item", "?"), r.get("stage", "collection"))].append(r)

    # L01: 同一項目・同一ステージで、経路は違うがクエリが完全一致
    for (item, stage), group in by_item_stage.items():
        seen = {}
        for r in group:
            q = r.get("query", "")
            route = r.get("route", "")
            if not q:
                continue
            if q in seen and seen[q] != route:
                res.add("L01", "WARN", f"{item}/{stage}",
                        f"経路『{seen[q]}』と『{route}』でクエリが完全一致: 『{q}』",
                        "経路を分けたことになっているが、同じ検索の繰り返しの疑い。"
                        "経路ごとに異なる検索語・サイト指定を使うこと")
            seen.setdefault(q, route)

    # L02: 独立再検証のクエリが収集時と完全一致
    items = {r.get("item", "?") for r in rows}
    for item in items:
        collection_queries = {r.get("query", "") for r in rows
                              if r.get("item") == item and r.get("stage", "collection") == "collection"}
        for r in rows:
            if r.get("item") != item or r.get("stage") != "reverify":
                continue
            q = r.get("query", "")
            if q and q in collection_queries:
                res.add("L02", "FAIL", item,
                        f"独立再検証のクエリが収集時と完全一致: 『{q}』",
                        "再検証は収集時と異なるクエリで行う。多様性が確保されていない")

    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    print_and_exit([run(case_dir)], "ゲートL: 探索ログの多様性", case_dir, "L")


if __name__ == "__main__":
    main()
