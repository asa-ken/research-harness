#!/usr/bin/env python3
"""publish_report.py - レポートを「版番号つき」で発行し、証拠台帳Excelも必ず同時に出す。

命名規則（レポート出力都度、整数で1つ上げる）:
  初回= v1。以降、出力のたびに +1。
  - レポート : <base>_report_v{N}.md
  - 証拠台帳 : <base>_evidence_ledger_v{N}.xlsx   （同じ N を共有）
  <base> は既定で案件ディレクトリ名（--name で上書き可）。
  版番号 N は <case_dir>/outputs/ にある既存 <base>_report_v*.md の最大番号 + 1。

  ゲート対象の作業ファイルは従来どおり report.md（固定名）。本スクリプトはそれを
  版番号つきの名前でコピーして発行するだけで、report.md 自体は変更しない
  （＝ゲートB刻印は無効化されない）。

必ず証拠台帳Excelも出す:
  内部で export_wcheck.py を実行し、生成された checks/wcheck_summary.xlsx を
  版番号つきの名前でコピーする。レポート単体を出してExcelを出し忘れることを防ぐ。

usage:
  python3 scripts/publish_report.py <case_dir> [--name BASE] [--verify]
出力（すべて <case_dir>/outputs/ 配下）:
  <base>_report_v{N}.md
  <base>_evidence_ledger_v{N}.xlsx
標準出力に、発行した2ファイルのパスと版番号 N を表示する。
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def next_version(outputs_dir: str, base: str) -> int:
    """outputs/ 内の <base>_report_v{N}.md を走査し、最大 N + 1 を返す。無ければ 1。"""
    pat = re.compile(rf"^{re.escape(base)}_report_v(\d+)\.md$")
    hi = 0
    if os.path.isdir(outputs_dir):
        for name in os.listdir(outputs_dir):
            m = pat.match(name)
            if m:
                hi = max(hi, int(m.group(1)))
    return hi + 1


def main() -> int:
    args = [a for a in sys.argv[1:]]
    if not args:
        print("usage: python3 scripts/publish_report.py <case_dir> [--name BASE] [--verify]")
        return 2
    case_dir = args[0]
    base = None
    do_verify = "--verify" in args
    if "--name" in args:
        i = args.index("--name")
        base = args[i + 1] if i + 1 < len(args) else None
    if not base:
        base = os.path.basename(os.path.normpath(case_dir))

    report = os.path.join(case_dir, "report.md")
    if not os.path.isfile(report):
        print(f"[エラー] レポートが見つからない: {report}")
        return 1

    # 任意: 発行前に改ざん検知（ゲートB）を確認する
    if do_verify:
        r = subprocess.run([sys.executable, os.path.join(HERE, "verify_gate.py"),
                            case_dir, "--gate", "B"], capture_output=True, text=True)
        print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(verify出力なし)")

    # 証拠台帳Excel（必須・毎回）を生成
    subprocess.run([sys.executable, os.path.join(HERE, "export_wcheck.py"), case_dir],
                   check=False)
    xlsx_src = os.path.join(case_dir, "checks", "wcheck_summary.xlsx")

    outputs_dir = os.path.join(case_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    n = next_version(outputs_dir, base)

    report_out = os.path.join(outputs_dir, f"{base}_report_v{n}.md")
    shutil.copyfile(report, report_out)

    ledger_out = None
    if os.path.isfile(xlsx_src):
        ledger_out = os.path.join(outputs_dir, f"{base}_evidence_ledger_v{n}.xlsx")
        shutil.copyfile(xlsx_src, ledger_out)
    else:
        print("[警告] 証拠台帳Excelが生成されていない（export_wcheckを確認）")

    print(f"版番号: v{n}")
    print(f"レポート : {report_out}")
    if ledger_out:
        print(f"証拠台帳 : {ledger_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
