#!/usr/bin/env python3
"""build_ledger.py - 証拠台帳の整形。E-ID採番とオフセット補完を行う。

引用が原文に見つからない場合は、ここでは修正せず印を残す（check_a でFAILさせる）。
自動で近いものに寄せると、誤った引用が通ってしまうため。

usage: python3 scripts/build_ledger.py <case_dir>
"""
from __future__ import annotations

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    case_path, read_text, read_jsonl, write_jsonl, load_sources, now_iso, norm,
    resolve_anchor,
)


def find_offsets(haystack: str, needle: str):
    """完全一致を優先し、無ければ正規化後の一致で位置を推定する。"""
    if not needle:
        return []
    hits = []
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx < 0:
            break
        hits.append(idx)
        start = idx + 1
        if len(hits) > 5:
            break
    return hits


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    ledger_path = case_path(case_dir, "ledger.jsonl")
    rows = read_jsonl(ledger_path)
    if not rows:
        print("ledger.jsonl が空です。")
        sys.exit(2)

    sources, _ = load_sources(case_dir)
    used = {r.get("eid") for _, r in rows if r.get("eid")}
    counter = 0

    def next_eid():
        nonlocal counter
        while True:
            counter += 1
            cand = f"E-{counter:04d}"
            if cand not in used:
                used.add(cand)
                return cand

    text_cache = {}
    out = []
    issues = 0
    for lineno, row in rows:
        if "__parse_error__" in row:
            print(f"[FAIL] L{lineno}: JSON解析エラー {row['__parse_error__']}")
            issues += 1
            out.append(row)
            continue
        if not row.get("eid"):
            row["eid"] = next_eid()
            print(f"[ID] L{lineno}: {row['eid']} を採番")

        sid = row.get("source_id")
        if sid not in text_cache:
            text_cache[sid] = read_text(case_path(case_dir, "raw_text", f"{sid}.txt"))
        raw = text_cache[sid]
        head, tail = row.get("anchor_head", ""), row.get("anchor_tail", "")

        if not raw:
            row["_offset_status"] = "NO_RAW_TEXT"
            print(f"[WARN] {row['eid']}: raw_text/{sid}.txt が無い")
            issues += 1
        elif not head or not tail:
            row["_offset_status"] = "NO_ANCHOR"
            print(f"[FAIL] {row['eid']}: anchor_head / anchor_tail が未設定")
            issues += 1
        else:
            status, fs, fe, text = resolve_anchor(raw, head, tail, row.get("char_start"))
            if status == "ok":
                row["char_start"], row["char_end"] = fs, fe
                row["_offset_status"] = "OK"
                row["_resolved_len"] = fe - fs
            else:
                row["_offset_status"] = status.upper()
                label = {"no_head": "anchor_headが原文に無い",
                         "no_tail": "anchor_tailが見つからない",
                         "ambiguous": "識別語が複数箇所に一致（char_startで絞る）"}
                print(f"[FAIL] {row['eid']}: {label.get(status, status)}")
                issues += 1
        row.setdefault("registered_at", now_iso())
        out.append(row)

    if os.path.exists(ledger_path):
        shutil.copy(ledger_path, ledger_path + ".bak")
    out.sort(key=lambda r: r.get("eid", "E-9999"))
    write_jsonl(ledger_path, out)
    print(f"\n{len(out)}件を整形。要確認 {issues}件。バックアップ: ledger.jsonl.bak")
    print("→ 次: python3 scripts/run_gate.py <case_dir> --gate A")


if __name__ == "__main__":
    main()
