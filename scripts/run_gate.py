#!/usr/bin/env python3
"""run_gate.py - ゲートを実行して合否を出す。

Claudeはここで出た結果だけを合否として扱う。自己申告での通過を認めない。

usage:
  python3 scripts/run_gate.py <case_dir> --gate A     # P2完了時
  python3 scripts/run_gate.py <case_dir> --gate B     # P4完了時
  python3 scripts/run_gate.py <case_dir> --gate all
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_a_source_ledger as check_a  # noqa: E402
import check_b_ledger_report as check_b  # noqa: E402
import check_c_claims_review as check_c  # noqa: E402
import check_l_search_log as check_l  # noqa: E402
import lint_status  # noqa: E402
from harness_lib import print_and_exit  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    gate = "all"
    if "--gate" in sys.argv:
        gate = sys.argv[sys.argv.index("--gate") + 1].upper()
    if not os.path.isdir(case_dir):
        print(f"ディレクトリが無い: {case_dir}")
        sys.exit(2)

    results = []
    if gate in ("A", "ALL"):
        results.append(check_a.run(case_dir))
        results.append(check_l.run(case_dir))
    if gate in ("B", "ALL"):
        results.append(lint_status.run(case_dir))
        results.append(check_b.run(case_dir))
    if gate in ("C", "ALL"):
        results.append(check_c.run(case_dir))
    if gate == "L":
        results.append(check_l.run(case_dir))

    if not results:
        print(f"未知のゲート: {gate}")
        sys.exit(2)
    print_and_exit(results, f"ゲート{gate} 実行結果", case_dir, gate)


if __name__ == "__main__":
    main()
