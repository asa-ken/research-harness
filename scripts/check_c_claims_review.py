#!/usr/bin/env python3
"""check_c_claims_review.py - ゲートC: 独立レビュー(GC)が実施されたことの検証

extract_claims.py は表を作るだけで、判定が埋まったかは誰も確認していなかった。
このスクリプトは claims_review.md の判定列が埋まっているか、
不支持・部分的が残っていないかを機械的に確認する。

usage: python3 scripts/check_c_claims_review.py <case_dir>
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import CheckResult, case_path, read_text, print_and_exit  # noqa: E402
from extract_claims import collect  # noqa: E402

VALID = {"支持", "部分的", "不支持", "判断不能"}
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")


def parse_table(text):
    rows = []
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) < 6 or not re.match(r"^\d+$", m.group(1)):
            continue
        rows.append(cells)
    return rows


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックC: 独立レビュー(GC)の実施確認")
    expected = collect(case_dir)
    path = case_path(case_dir, "checks", "claims_review.md")
    text = read_text(path)

    if not text:
        if len(expected) == 0:
            res.add("C00", "WARN", case_dir, "E-ID付きの主張が無く、GC対象自体が無い")
        elif len(expected) < 5:
            res.add("C00", "WARN", case_dir,
                    f"claims_review.mdが未生成（対象{len(expected)}件、小規模のため見送りも可）",
                    "省略する場合はレポートの「本調査の限界」に未実施と明記すること")
        else:
            res.add("C00", "FAIL", case_dir,
                    f"claims_review.mdが未生成（対象{len(expected)}件）",
                    "extract_claims.py を実行し、独立レビューを行うこと")
        return res

    rows = parse_table(text)
    if not rows:
        res.add("C00", "FAIL", path, "claims_review.mdに表の行が1件も解析できない",
                "手動編集でMarkdown表の形式が崩れていないか確認する")
        return res

    if len(rows) < len(expected):
        res.add("C04", "WARN", path,
                f"表の行数({len(rows)})が現在のレポートの主張数({len(expected)})より少ない",
                "レポート更新後にextract_claims.pyを再実行していない可能性")

    unresolved = []
    unreviewed = []
    weak = []
    comments = []
    verdicts = []
    for cells in rows:
        idx = len(cells) - 2  # 末尾から2列目が「判定」（最後は「コメント」）
        verdict = cells[idx] if 0 <= idx < len(cells) else ""
        comment = cells[-1] if cells else ""
        where = f"{path}:#{cells[0] if cells else '?'}"
        if not verdict or verdict not in VALID:
            unreviewed.append(where)
        elif verdict in ("不支持", "部分的"):
            unresolved.append((where, cells[1] if len(cells) > 1 else ""))
        elif verdict == "判断不能":
            weak.append(where)
        verdicts.append(verdict)
        comments.append(comment.strip())

    if unreviewed:
        res.add("C01", "FAIL", path,
                f"判定が未記入の行が{len(unreviewed)}件",
                "全行の判定列を埋めてから納品する")
    if unresolved:
        res.add("C02", "FAIL", path,
                f"不支持・部分的の判定が{len(unresolved)}件残っている",
                "レポートを修正しゲートBからやり直す。解消後にclaims_review.mdも更新すること")
    if weak:
        res.add("C03", "WARN", path,
                f"判断不能が{len(weak)}件（証拠が主張に対して弱い）",
                "証拠を取り直すか、主張を弱める")

    # C05/C06: ラバースタンプ（機械的に「支持」を連発しただけ）の兆候を検出する。
    # 完全な意味検証は不可能だが、以下の統計的な形跡は実際の吟味が
    # 行われなかった可能性を示唆する。あくまで兆候であり、確定的な判定ではない。
    judged = [v for v in verdicts if v in VALID]
    if len(judged) >= 5:
        support_ratio = judged.count("支持") / len(judged)
        if support_ratio == 1.0:
            res.add("C05", "WARN", path,
                    f"{len(judged)}件全てが『支持』——多数の主張のうち"
                    "1件も疑義が無いのは、実質的な吟味が行われていない兆候の可能性",
                    "本当に全て支持できるか、独立した視点で見直したか確認する")
        nonempty_comments = [c for c in comments if c]
        if len(nonempty_comments) >= 5:
            most_common = max(set(nonempty_comments), key=nonempty_comments.count)
            dup_ratio = nonempty_comments.count(most_common) / len(nonempty_comments)
            if dup_ratio >= 0.6:
                res.add("C06", "WARN", path,
                        f"コメントの{dup_ratio:.0%}が同一文言『{most_common[:30]}』——"
                        "コピー&ペーストによる形式的記入の兆候の可能性",
                        "各行を個別に検討したコメントになっているか確認する")

    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    print_and_exit([run(case_dir)], "ゲートC: 独立レビュー確認", case_dir, "C")


if __name__ == "__main__":
    main()
