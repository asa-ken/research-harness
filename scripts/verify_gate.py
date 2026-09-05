#!/usr/bin/env python3
"""verify_gate.py - ゲートが実際に実行され、その後ファイルが改変されていないかを確認する。

Claudeの「チェックを通しました」という報告を、受け取った側が独立に検証するための道具。
納品されたレポートのハッシュが、ゲート実行時のハッシュと一致するかを見る。

usage: python3 scripts/verify_gate.py <case_dir> [--gate B]
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import case_path, read_json, read_text, file_sha, figures_sha  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    gate = sys.argv[sys.argv.index("--gate") + 1].upper() if "--gate" in sys.argv else "B"

    receipt = read_json(case_path(case_dir, "checks", f"receipt_{gate}.json"))
    if not receipt:
        print(f"[NG] ゲート{gate}の実行証跡がありません。チェックは実行されていません。")
        sys.exit(1)

    problems = []
    if receipt.get("verdict") != "PASS":
        problems.append(f"証跡の判定が {receipt.get('verdict')} です"
                        f"（FAIL {receipt.get('fails')}件）")
    for name, recorded in (receipt.get("files") or {}).items():
        if name == "figures/":
            current = figures_sha(case_dir)
        else:
            current = file_sha(case_path(case_dir, name))
        if recorded and current != recorded:
            problems.append(f"{name} がゲート実行後に変更されています")
        elif recorded and current is None:
            problems.append(f"{name} が見つかりません（削除された可能性）")

    embedded = re.search(r"<!--\s*gate:(\w+)\s+(\w+)\s+receipt=([0-9a-f]+)\s*-->",
                         read_text(case_path(case_dir, "report.md")))
    if embedded and embedded.group(3) != receipt.get("receipt_id"):
        problems.append("レポートに書かれた証跡IDが実際の証跡と一致しません")

    print(f"ゲート{gate} 実行日時: {receipt.get('executed_at')}")
    print(f"証跡ID: {receipt.get('receipt_id')}  判定: {receipt.get('verdict')}"
          f" (FAIL {receipt.get('fails')} / WARN {receipt.get('warns')})")
    if problems:
        for p in problems:
            print(f"[NG] {p}")
        sys.exit(1)
    print("[OK] ゲートは実行済みで、その後ファイルは変更されていません。")


if __name__ == "__main__":
    main()
