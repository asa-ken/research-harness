#!/usr/bin/env python3
"""extract_claims.py - レポートの主張と、その根拠引用を突き合わせ表に出す。

チェックA/Bは「引用が原文にあるか」「数値が一致するか」までしか見ない。
『引用は本物だが、その引用はその主張を支持していない』という逸脱は、
意味の判断を要するため機械では塞げない。

そこでこのスクリプトは判定せず、独立レビュー用の材料だけを作る。
レビューする人（またはレポートを書いていない別セッションのClaude）が、
主張と引用を1件ずつ見比べて 支持/不支持/判断不能 を付ける。

このスクリプトは外部通信をしない。生成した表を新しいチャットに貼るだけで足りる
（貼り付け用の依頼文も一緒に出力する）。

usage: python3 scripts/extract_claims.py <case_dir>
出力: <case_dir>/checks/claims_review.md
"""
from __future__ import annotations

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    case_path, read_text, load_ledger, iter_report_units, parse_tags, TAG_RE,
    evidence_text,
)


def collect(case_dir):
    """レポート・図からE-ID付きの主張を抽出する。check_c_claims_review.py からも使う。"""
    evidence = {r.get("eid"): r for _, r in load_ledger(case_dir) if r.get("eid")}
    rows = []
    for path in [case_path(case_dir, "report.md")] + \
            sorted(glob.glob(case_path(case_dir, "figures", "*.md"))):
        if not os.path.exists(path):
            continue
        name = os.path.basename(path)
        for where, unit in iter_report_units(read_text(path), name):
            tags = parse_tags(unit)
            if not tags["eids"]:
                continue
            claim = TAG_RE.sub("", unit).strip()
            for eid in dict.fromkeys(tags["eids"]):
                ev = evidence.get(eid, {})
                rows.append((where, claim, eid, ev.get("claim_type", "?"),
                             evidence_text(case_dir, ev).replace("\n", " ")))
    return rows


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    rows = collect(case_dir)

    out = ["# 主張⇔引用 独立レビュー表", "",
           "レポートを書いた者以外が記入する。引用文だけを読み、",
           "その引用が主張を支持しているかを判断する（原文に戻ってもよい）。", "",
           "判定: `支持` / `不支持` / `部分的` / `判断不能`", "",
           "**不支持・部分的が1件でもあれば、レポートを修正してからGBをやり直す。**", "",
           "| # | 箇所 | 主張 | 根拠 | 種別 | 引用（原文） | 判定 | コメント |",
           "|---|---|---|---|---|---|---|---|"]
    for i, (where, claim, eid, ctype, quote) in enumerate(rows, 1):
        c = claim.replace("|", "\\|")[:80]
        q = quote.replace("|", "\\|")[:120]
        out.append(f"| {i} | {where} | {c} | {eid} | {ctype} | {q} |  |  |")
    out += ["", f"（{len(rows)}件）", "",
            "## 別セッションに貼るときの依頼文", "",
            "```",
            "この表の各行について、引用文が主張を支持しているかを判定してください。",
            "レポート全体の文脈や、書き手の意図は考慮しないでください。",
            "引用文だけを読んで、支持 / 部分的 / 不支持 / 判断不能 のいずれかを付け、",
            "不支持・部分的の場合は理由を書いてください。",
            "一般常識や業界知識で補って「支持」としないでください。",
            "引用に書かれていないことは、書かれていないと扱います。",
            "```", "",
            "「このレポートは正しいですか」とは聞かないこと。",
            "全体の妥当性を問うと、もっともらしさで判断されてしまう。", "",
            "## 記入時の着眼点", "",
            "- 主語・対象が入れ替わっていないか（別セグメント、別会社、別製品）",
            "- 主張の向きが引用と逆になっていないか（肯定/否定）",
            "- 単一時点の引用で、変化や傾向を語っていないか",
            "- 会社予想・第三者見解を、事実として書いていないか",
            "- 引用の一部だけを切り出して、条件や留保を落としていないか"]

    path = case_path(case_dir, "checks", "claims_review.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"{len(rows)}件の主張を抽出 → {path}")
    print("→ レポートを書いていない別セッションのClaude、またはユーザ自身が判定する")


if __name__ == "__main__":
    main()
