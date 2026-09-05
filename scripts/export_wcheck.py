#!/usr/bin/env python3
"""export_wcheck.py - C-1/C-2/C-3 相当のWチェック結果を証拠ごとに集約し、Excel出力する

設計方針（重要）: 状態は固定語彙（問題なし/懸念あり/問題あり/未実施）のみを使い、
Claudeが自由記述で判定を書き込むことはしない。理由文も、各チェックが実際に出力した
メッセージをそのまま転記する（新たな文章をここで作らない）。

自由記述を許すと、詳細な理由文ほど「もっともらしく見える」ため、
中身が伴わない記述で検証を通過できてしまう（過去の性悪説監査で判明した抜け穴と同型）。
固定語彙＋機械生成の理由文に限定することで、この経路を塞ぐ。

対応関係:
  C-1 記述→原文整合 … checks/claims_review.md の判定列（GC＝独立レビューの結果）
  C-2 原文→原典整合 … reverify_log.jsonl の outcome（原典再アクセスの結果）
  C-3 文脈整合      … check_a_source_ledger.py の A15/A16/A18/A19/A20/A21（今回の実行結果）

usage: python3 scripts/export_wcheck.py <case_dir> [--out path.xlsx] [--no-xlsx]
出力: <case_dir>/checks/wcheck_summary.jsonl（常に生成、機械ファイル）
      <case_dir>/checks/wcheck_summary.xlsx（--no-xlsx で省略可）
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import case_path, read_text, load_ledger, load_reverify_log  # noqa: E402
import check_a_source_ledger as check_a  # noqa: E402

# 固定語彙。この4値以外を使わない。
NO_ISSUE = "問題なし"
CONCERN = "懸念あり"
ISSUE = "問題あり"
NOT_DONE = "未実施"

C3_CODES = {"A15", "A16", "A17", "A18", "A19", "A20", "A21"}

C2_OUTCOME_MAP = {
    "match": NO_ISSUE,
    "context_reversed": CONCERN,
    "hallucination": ISSUE,
    "unreachable": NOT_DONE,
}
C1_VERDICT_MAP = {
    "支持": NO_ISSUE,
    "判断不能": CONCERN,
    "部分的": CONCERN,
    "不支持": ISSUE,
}


def collect_c3(case_dir):
    """A15〜A21の直近実行結果から、証拠ごとの文脈整合状態を機械的に集約する。

    check_a.run() は毎回スクリプトが実際に判定した結果を返す。
    ここでの分類はその結果を読むだけで、新たな判断を行わない。
    """
    res = check_a.run(case_dir)
    by_eid = {}
    for f in res.findings:
        if f.code not in C3_CODES:
            continue
        eid = f.where
        entry = by_eid.setdefault(eid, {"level": None, "reasons": []})
        entry["reasons"].append(f.line())
        if f.level == "FAIL":
            entry["level"] = "FAIL"
        elif f.level == "WARN" and entry["level"] != "FAIL":
            entry["level"] = "WARN"

    out = {}
    for eid, entry in by_eid.items():
        status = ISSUE if entry["level"] == "FAIL" else CONCERN
        out[eid] = (status, " / ".join(entry["reasons"]))
    return out


def collect_c2(case_dir):
    """reverify_log.jsonl の outcome を固定語彙にマッピングする。"""
    out = {}
    for row in load_reverify_log(case_dir):
        eid = row.get("eid")
        if not eid:
            continue
        outcome = row.get("outcome", "")
        status = C2_OUTCOME_MAP.get(outcome)
        if status is None:
            continue
        # detailは原典再アクセスを行った者が記録した確認内容。ここで新たに作文しない。
        out[eid] = (status, str(row.get("detail", "")))
    return out


ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")


def collect_c1(case_dir):
    """claims_review.md（GCの結果）から、証拠ごとの記述整合状態を読む。

    根拠列に書かれたE-IDへ判定を割り当てる。1つのE-IDが複数行で参照されている
    場合は、最も厳しい判定（不支持 > 部分的 = 判断不能 > 支持）を採用する。
    """
    text = read_text(case_path(case_dir, "checks", "claims_review.md"))
    if not text:
        return {}
    severity_order = {NO_ISSUE: 0, CONCERN: 1, ISSUE: 2}
    out = {}
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if not m or not re.match(r"^\d+$", m.group(1)):
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) < 6:
            continue
        eid = cells[2].strip()
        if not re.match(r"^E-\d{4}$", eid):
            continue
        verdict = cells[-2] if len(cells) >= 2 else ""
        comment = cells[-1] if cells else ""
        status = C1_VERDICT_MAP.get(verdict)
        if status is None:
            continue
        if eid not in out or severity_order[status] > severity_order[out[eid][0]]:
            out[eid] = (status, comment)
    return out


def build_summary(case_dir):
    evidence = {r.get("eid"): r for _, r in load_ledger(case_dir) if r.get("eid")}
    c1 = collect_c1(case_dir)
    c2 = collect_c2(case_dir)
    c3 = collect_c3(case_dir)

    rows = []
    for eid, ev in sorted(evidence.items()):
        s1, r1 = c1.get(eid, (NOT_DONE, ""))
        s2, r2 = c2.get(eid, (NOT_DONE, ""))
        s3, r3 = c3.get(eid, (NO_ISSUE, "A15〜A21で指摘なし"))
        rows.append({
            "eid": eid, "source_id": ev.get("source_id", ""),
            "subject": ev.get("subject", ""), "fact": ev.get("fact", ""),
            "claim_type": ev.get("claim_type", ""), "confidence": ev.get("confidence", ""),
            "tags": ",".join(ev.get("tags", []) or []),
            "c1_status": s1, "c1_reason": r1,
            "c2_status": s2, "c2_reason": r2,
            "c3_status": s3, "c3_reason": r3,
        })
    return rows


def write_jsonl_summary(case_dir, rows):
    path = case_path(case_dir, "checks", "wcheck_summary.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return path


def export_xlsx(case_dir, rows, out_path):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        print("openpyxl未導入のためExcel出力をスキップします。"
              "pip install openpyxl --break-system-packages")
        return None

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Wチェック結果"

    headers = ["EID", "Source", "Subject", "Fact", "種別", "確信度", "タグ",
               "C-1判定", "C-1理由(GC)", "C-2判定", "C-2理由(原典再アクセス)",
               "C-3判定", "C-3理由(文脈整合チェック)"]
    ws.append(headers)
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = header_fill
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    status_fill = {
        ISSUE: PatternFill(start_color="F8CBAD", end_color="F8CBAD", fill_type="solid"),
        CONCERN: PatternFill(start_color="FFE699", end_color="FFE699", fill_type="solid"),
        NO_ISSUE: PatternFill(start_color="C6E0B4", end_color="C6E0B4", fill_type="solid"),
        NOT_DONE: PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
    }

    for r in rows:
        row = [r["eid"], r["source_id"], r["subject"], r["fact"], r["claim_type"],
               r["confidence"], r["tags"],
               r["c1_status"], r["c1_reason"],
               r["c2_status"], r["c2_reason"],
               r["c3_status"], r["c3_reason"]]
        ws.append(row)
        excel_row = ws.max_row
        for col_idx, status_key in ((8, "c1_status"), (10, "c2_status"), (12, "c3_status")):
            fill = status_fill.get(r[status_key])
            if fill:
                ws.cell(row=excel_row, column=col_idx).fill = fill
        for c in ws[excel_row]:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    widths = [8, 8, 16, 30, 8, 8, 16, 10, 34, 10, 34, 10, 34]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    ws.freeze_panes = "A2"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)
    return out_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    no_xlsx = "--no-xlsx" in sys.argv
    out_path = None
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    elif not no_xlsx:
        out_path = case_path(case_dir, "checks", "wcheck_summary.xlsx")

    rows = build_summary(case_dir)
    jsonl_path = write_jsonl_summary(case_dir, rows)
    print(f"{len(rows)}件を集約 → {jsonl_path}")

    counts = {}
    for r in rows:
        for k in ("c1_status", "c2_status", "c3_status"):
            counts[(k, r[k])] = counts.get((k, r[k]), 0) + 1
    for dim in ("c1_status", "c2_status", "c3_status"):
        line = " / ".join(f"{v}:{counts.get((dim, v), 0)}"
                          for v in (NO_ISSUE, CONCERN, ISSUE, NOT_DONE))
        print(f"  {dim}: {line}")

    if out_path:
        path = export_xlsx(case_dir, rows, out_path)
        if path:
            print(f"→ Excel: {path}")


if __name__ == "__main__":
    main()
