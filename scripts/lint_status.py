#!/usr/bin/env python3
"""lint_status.py - ステータス語彙の検査

「不明」で済ませると次アクションの情報が失われる。
4分類（非公表/未調査/調査不可/推定）とその成立条件を機械的に強制する。

usage: python3 scripts/lint_status.py <case_dir> [target.md ...]
"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    CheckResult, case_path, read_text, iter_report_units, parse_tags,
    BARRIER_CODES, print_and_exit, EID_RE, REQ_RE, load_ledger,
    ITEM_ID_RE, saturation_status,
)

VAGUE = [
    "不明", "情報なし", "情報が見つかり", "確認できず", "確認できませんでした",
    "見つかりませんでした", "定かではない", "定かでない", "詳細不明", "データなし",
    "N/A", "不詳", "判然としない", "はっきりしない", "明確でない", "明らかでない",
    "よく分からない", "把握できていない", "特定できない",
]


def check_unit(res, where, unit, evidence=None, case_dir=None):
    tags = parse_tags(unit)
    bodies = tags["status"] + tags["infer"]

    for body in bodies:
        head = body.split("|")[0].strip()
        attrs = [a.strip() for a in body.split("|")[1:]]
        joined = "|".join(attrs)

        if head == "非公表":
            if not EID_RE.search(joined):
                res.add("S01", "FAIL", where,
                        "[非公表]に確認証拠E-IDが無い（探した場所の証拠が必要）", body[:60])
            elif evidence is not None:
                for eid in EID_RE.findall(joined):
                    ev = evidence.get(eid)
                    if ev is None:
                        # 台帳に存在しないE-IDを書けば、以前はS01もS12も
                        # 素通りしていた（ev=Noneでelifが偽になり判定自体が起きない）。
                        # 存在確認を独立させ、この抜け穴を塞ぐ。
                        res.add("S13", "FAIL", where,
                                f"[非公表]の確認証拠 {eid} が台帳(ledger.jsonl)に存在しない",
                                "実在しないE-IDを書いて検証を回避することはできない")
                    elif ev.get("claim_type") != "negative":
                        res.add("S12", "FAIL", where,
                                f"[非公表]の確認証拠 {eid} が claim_type:negative でない",
                                "『探したが記載が無い』ことの証拠でなければ非公表の根拠にならない")
            if "代替" not in joined:
                res.add("S02", "WARN", where, "[非公表]に代替アプローチの記載が無い", body[:60])
            else:
                alt_text = re.search(r"代替:?([^|]*)", joined)
                if alt_text and len(alt_text.group(1).strip()) < 4:
                    res.add("S02", "WARN", where,
                            "[非公表]の代替アプローチが短すぎ、具体性が無い可能性", body[:60])
        elif head == "未調査":
            next_m = re.search(r"次(?:アクション)?:?([^|]*)", joined)
            if not next_m:
                res.add("S03", "FAIL", where, "[未調査]に次アクションが無い", body[:60])
            elif len(next_m.group(1).strip()) < 4:
                # 「次:確認」のような1〜2文字の空文言でS03を黙らせられないようにする。
                # 完全な意味検証ではないが、ゼロ努力の埋め草は防ぐ。
                res.add("S03", "WARN", where,
                        "[未調査]の次アクションが短すぎ、具体性が無い可能性", body[:60])
            if not re.search(r"優先:[HML]", joined) and "意図的" not in joined:
                res.add("S04", "FAIL", where, "[未調査]に優先度(H/M/L)が無い", body[:60])
        elif head == "調査不可":
            if not any(code in joined for code in BARRIER_CODES):
                res.add("S05", "FAIL", where,
                        f"[調査不可]に障壁コードが無い（{'/'.join(BARRIER_CODES)}）", body[:60])
            if not REQ_RE.search(joined):
                res.add("S06", "FAIL", where, "[調査不可]に依頼ID(R-xxx)が無い", body[:60])
        elif head == "推定":
            if not EID_RE.search(joined):
                res.add("S07", "FAIL", where, "[推定]に根拠E-IDが無い", body[:60])
            if "確信度" not in joined:
                res.add("S08", "FAIL", where, "[推定]に確信度が無い", body[:60])
            if "反証" not in joined:
                res.add("S09", "FAIL", where, "[推定]に反証条件が無い", body[:60])
        elif head == "未特定":
            item_m = ITEM_ID_RE.search(joined)
            if not item_m:
                res.add("S14", "FAIL", where,
                        "[未特定]に必要証拠リストの項目ID(N-xx)が無い", body[:60])
            elif case_dir:
                ok, detail = saturation_status(case_dir, item_m.group(0))
                if not ok:
                    res.add("S14", "FAIL", where,
                            f"[未特定]の飽和条件を満たしていない（項目{item_m.group(0)}）",
                            detail + "。search_log.jsonlに直近3件の探索記録が要る"
                            "（経路・クエリとも3件とも異なり、全て新規0件）")

    # 素の曖昧語（タグ外）
    naked = re.sub(r"\[[^\[\]]*\]", "", unit)
    for word in VAGUE:
        if word in naked:
            res.add("S10", "FAIL", where,
                    f"曖昧語『{word}』が使われている（4分類に置き換えること）", naked[:60])
            break


def run(case_dir: str, targets=None) -> CheckResult:
    res = CheckResult("ステータスLint")
    evidence = {r.get("eid"): r for _, r in load_ledger(case_dir) if r.get("eid")}
    files = targets or ([case_path(case_dir, "report.md")]
                        + sorted(glob.glob(case_path(case_dir, "figures", "*.md"))))
    req_text = read_text(case_path(case_dir, "requests", "needed_sources.md"))
    known_reqs = set(REQ_RE.findall(req_text))

    found_any = False
    for path in files:
        if not os.path.exists(path):
            res.add("S00", "WARN", path, "対象ファイルが存在しない")
            continue
        found_any = True
        text = read_text(path)
        name = os.path.basename(path)
        for where, unit in iter_report_units(text, name):
            check_unit(res, where, unit, evidence, case_dir)
            for rid in REQ_RE.findall(unit):
                if rid not in known_reqs:
                    res.add("S11", "FAIL", where,
                            f"依頼ID {rid} が needed_sources.md に存在しない")
    if not found_any:
        res.add("S00", "FAIL", case_dir, "検査対象のmdが1つも無い")
    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    targets = sys.argv[2:] or None
    print_and_exit([run(case_dir, targets)], "ステータスLint", case_dir, "status")


if __name__ == "__main__":
    main()
