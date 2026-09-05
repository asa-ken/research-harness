#!/usr/bin/env python3
"""improve_gate.py - 改善候補の汎用性ゲート

調査後の会話から拾った改善案を、そのままSKILL.mdに書くと
「その案件に効くが他案件では雑音になるルール」が溜まる（過学習）。
5テストで機械的にふるいにかける。

usage: python3 scripts/improve_gate.py <case_dir> [--skill <skill_dir>]

入力: <case_dir>/improvements/inbox.jsonl
      <case_dir>/improvements/case_terms.txt  (任意: この案件の固有名詞を1行1語)
出力: <case_dir>/improvements/gate_result.md
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import case_path, read_text, read_jsonl, now_iso  # noqa: E402

SKILL_LINE_BUDGET = 500
TICKER_RE = re.compile(r"\b[A-Z]{2,5}\b")
JP_CODE_RE = re.compile(r"(?<!\d)[1-9]\d{3}(?!\d)")
YEARMON_RE = re.compile(r"(19|20)\d{2}年|\bFY\d{2}\b|\b[1-4]Q\b")
CORP_RE = re.compile(r"株式会社|ホールディングス|\b(Inc|Corp|Corporation|Ltd|LLC|PLC)\b")

GENERIC_ALLOW = {"AI", "API", "PDF", "IR", "GAAP", "IFRS", "SEC", "TAM", "SAM",
                 "KPI", "ROE", "ROIC", "PER", "PBR", "EPS", "CAPEX", "YOY", "QOQ",
                 "OK", "NG", "T1", "T2", "T3", "T4", "T5", "T6"}


def bigrams(s: str):
    s = re.sub(r"\s+", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def jaccard(a: str, b: str) -> float:
    A, B = bigrams(a), bigrams(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def t1_proper_nouns(cand, case_terms):
    """固有名詞テスト: 特定銘柄・企業・時期に依存していないか。"""
    text = f"{cand.get('proposal','')} {cand.get('failure_mode','')}"
    hits = []
    for tok in TICKER_RE.findall(text):
        if tok not in GENERIC_ALLOW:
            hits.append(f"ティッカー様の語:{tok}")
    hits += [f"証券コード様の数字:{m}" for m in JP_CODE_RE.findall(text)]
    hits += [f"時期指定:{m.group(0)}" for m in YEARMON_RE.finditer(text)]
    if CORP_RE.search(text):
        hits.append("法人格を含む社名")
    for term in case_terms:
        if term and term in text:
            hits.append(f"案件固有語:{term}")
    return (not hits), hits


def t2_counterexamples(cand):
    ev = cand.get("scope_evidence") or []
    ok = isinstance(ev, list) and len(ev) >= 2
    return ok, [] if ok else ["異なる市場/業種での適用例が2件未満"]


def t3_root_cause(cand):
    fm = (cand.get("failure_mode") or "").strip()
    prop = (cand.get("proposal") or "").strip()
    notes = []
    if len(fm) < 10:
        notes.append("failure_modeが未記入または短すぎる（症状ではなく機構の欠陥を書く）")
    if re.match(r"^(次回|今回|この|本件)", prop):
        notes.append("proposalが単発の指示になっている")
    if fm and prop and jaccard(fm, prop) > 0.85:
        notes.append("failure_modeとproposalが同義（原因分析が無い）")
    return (not notes), notes


def t4_dup_conflict(cand, corpus_lines):
    prop = cand.get("proposal", "")
    notes = []
    best = (0.0, "")
    for line in corpus_lines:
        score = jaccard(prop, line)
        if score > best[0]:
            best = (score, line)
    if best[0] >= 0.60:
        notes.append(f"既存記述と重複の疑い(類似度{best[0]:.2f}): {best[1][:60]}")
    neg = re.search(r"(しない|禁止|避ける|不要)", prop)
    if neg and best[0] >= 0.40:
        notes.append("既存ルールと矛盾する可能性（否定形＋高類似）")
    return (not notes), notes


CORRECTNESS_EVIDENCE_RE = re.compile(
    r"誤り|間違い|誤検出|誤った|誤記|事実と異な|不正確|取り違え|矛盾|誤読|"
    r"incorrect|wrong|error|mismatch")


def t_severity_honesty(cand):
    """severity:correctness の自己申告に、裏付けとなる記述があるかを見る。

    severityはPROMOTE可否を左右する（correctnessなら再発を待たず即PROMOTE）。
    しかし誰でも書ける自己申告なので、規律を回避する手段になりうる。
    ここでは『誤りを示す語がobservationに無いのにcorrectnessを名乗る』ケースだけを拾う。
    完全な検証はできない（意味理解が要るため）ので、これは弱いヒューリスティックであり、
    最終的には decision_log.md への記録を人が確認することが前提。
    """
    if cand.get("severity") != "correctness":
        return True, []
    observation = cand.get("observation", "") or ""
    failure_mode = cand.get("failure_mode", "") or ""
    if CORRECTNESS_EVIDENCE_RE.search(observation + failure_mode):
        return True, []
    return False, ["severity:correctness だが、誤りを示す記述がobservation/failure_modeに無い"]


def t5_cost(cand, skill_lines):
    notes = []
    target = cand.get("target_file", "")
    added = len(cand.get("proposal", "").splitlines()) or 1
    if target.endswith("SKILL.md") and skill_lines + added > SKILL_LINE_BUDGET:
        notes.append(f"SKILL.md行数予算超過({skill_lines}+{added} > {SKILL_LINE_BUDGET})")
    if int(cand.get("added_steps", 0) or 0) >= 2:
        notes.append("追加ワークフローステップが2以上（referencesへ／機械化を検討）")
    if len(cand.get("proposal", "")) > 400:
        notes.append("proposalが長い（1ルール1文に分割）")
    return (not notes), notes


def verdict_for(cand, case_terms, corpus_lines, skill_lines):
    tests = {
        "T1固有名詞": t1_proper_nouns(cand, case_terms),
        "T2反例": t2_counterexamples(cand),
        "T3根本原因": t3_root_cause(cand),
        "T4重複矛盾": t4_dup_conflict(cand, corpus_lines),
        "T5コスト": t5_cost(cand, skill_lines),
        "T6severity": t_severity_honesty(cand),
    }
    failed = [k for k, (ok, _) in tests.items() if not ok]
    severity = cand.get("severity", "")
    recurrence = int(cand.get("recurrence", 1) or 1)
    severity_verified = tests["T6severity"][0]

    if failed and failed != ["T6severity"]:
        verdict = "REJECT" if "T1固有名詞" in failed or "T2反例" in failed else "REVISE"
    elif severity == "correctness" and severity_verified:
        verdict = "PROMOTE"      # 誤情報が出た欠陥は再発を待たない
    elif severity == "correctness" and not severity_verified:
        # 裏付けの無いcorrectness自己申告は、通常の再発待ちルートに落とす
        # （即時昇格の特権だけを剥奪し、REJECTはしない）
        verdict = "PROMOTE" if recurrence >= 2 else "HOLD"
    elif recurrence >= 2:
        verdict = "PROMOTE"
    else:
        verdict = "HOLD"         # 汎用性は満たすが再発待ち
    return verdict, tests


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if "--skill" in sys.argv:
        skill_dir = sys.argv[sys.argv.index("--skill") + 1]

    inbox = case_path(case_dir, "improvements", "inbox.jsonl")
    rows = read_jsonl(inbox)
    if not rows:
        print(f"改善候補がありません: {inbox}")
        sys.exit(2)

    case_terms = [t.strip() for t in
                  read_text(case_path(case_dir, "improvements", "case_terms.txt")).splitlines()
                  if t.strip() and not t.startswith("#")]

    skill_md = os.path.join(skill_dir, "SKILL.md")
    skill_text = read_text(skill_md)
    skill_lines = len(skill_text.splitlines())
    corpus_lines = [l.strip() for l in skill_text.splitlines() if len(l.strip()) > 20]
    for sub in ("references", "assets"):
        for ref in glob.glob(os.path.join(skill_dir, sub, "*.md")):
            corpus_lines += [l.strip() for l in read_text(ref).splitlines()
                             if len(l.strip()) > 20]

    out = [f"# 汎用性ゲート結果", "", f"- 実行: {now_iso()}",
           f"- SKILL.md 行数: {skill_lines} / 予算 {SKILL_LINE_BUDGET}", ""]
    counts = {}
    for lineno, cand in rows:
        if "__parse_error__" in cand:
            out.append(f"## L{lineno}: JSON解析エラー\n")
            continue
        verdict, tests = verdict_for(cand, case_terms, corpus_lines, skill_lines)
        counts[verdict] = counts.get(verdict, 0) + 1
        out.append(f"## {cand.get('id','(no-id)')} → **{verdict}**")
        out.append(f"- 失敗モード: {cand.get('failure_mode','')}")
        out.append(f"- 提案: {cand.get('proposal','')}")
        out.append(f"- 反映先候補: {cand.get('target_file','')} / "
                   f"再発回数: {cand.get('recurrence',1)} / severity: {cand.get('severity','-')}")
        for name, (ok, notes) in tests.items():
            mark = "pass" if ok else "FAIL"
            out.append(f"  - {name}: {mark}" + ("" if ok else " — " + "; ".join(notes)))
        if verdict == "PROMOTE":
            out.append("  - → 反映してよい。機械化できるならスクリプトのチェック項目を第一候補にする")
        elif verdict == "HOLD":
            out.append("  - → 汎用性は満たすが再発待ち(recurrence>=2で昇格)。inboxに残す")
        else:
            out.append("  - → 上記を直して再提出。却下も decision_log.md に記録すること")
        out.append("")

    path = case_path(case_dir, "improvements", "gate_result.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print("\n".join(out))
    print(f"→ 保存: {path}")
    print("→ 集計: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
