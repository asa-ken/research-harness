#!/usr/bin/env python3
"""check_q_micro_scope.py - 追加質問（追加論点）の準備チェック

初回調査には P0（スコープ確定）とゲートがあるが、納品後の追加質問には
準備をやり直す仕組みが無く、軸分解もソース一次特定も飛ばして走ってしまう
（実運用でI-101/I-102/I-103として表面化）。ここを埋める軽量ゲート。

scope.md の「## 追加論点」以下に置かれた各ブロックを検査する:

Q01: 論点（問い）が一行で書かれているか。空ならブロック不成立。
Q02: 決定的証拠が1件以上あるか。
Q03: 「優位・競争力・技術力・先行」型の問いなのに評価軸が2件未満。
     → 軸を分解せずに走っている兆候。
Q04: 評価軸に出所が1つも無い。
     → 記憶だけで軸を並べ、外の情報源で確かめていない兆候。
        出所の有無は減点でなく「他に軸はないか」という気づきの合図として出す。
Q05: 検証対象が「発言」なのに一次確認の記入が無い。
     → 要約だけで発言を検証する経路（I-102）。
Q06: 鮮度基準（何ヶ月より古いと危ないか）が書かれていない。
     → トレンドの速さを踏まえた鮮度判断をしていない兆候。

段階導入: すべて当面 WARN（出すが進める）。運用が定着したら FAIL に上げる。

usage: python3 scripts/check_q_micro_scope.py <case_dir>
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import CheckResult, case_path, read_text, print_and_exit  # noqa: E402

# 「優位性を問う」問いの手がかり語。取りこぼしはClaudeの明示指定で補う前提。
SUPERIORITY_RE = re.compile(r"優位|優れ|競争力|技術力|先行|勝|強い|上回|リード|ベスト|最強|トップ")
# 「発言」を検証している手がかり語。
STATEMENT_RE = re.compile(r"発言|語っ|述べ|コメント|インタビュー|会見|登壇|CEO|CTO|社長|会長|経営陣|幹部")


def split_blocks(scope_text):
    """scope.mdの「## 追加論点」以下を、### で始まる追加論点ブロックに分割する。"""
    if not scope_text:
        return []
    # 「## 追加論点」セクションの本文を取り出す
    m = re.search(r"^##\s*追加論点.*$", scope_text, re.MULTILINE)
    if not m:
        return []
    section = scope_text[m.end():]
    # 次の「## 」で終わる（あれば）
    nxt = re.search(r"^##\s", section, re.MULTILINE)
    if nxt:
        section = section[:nxt.start()]
    # コメント例（<!-- ... -->）は検査対象から除く
    section = re.sub(r"<!--.*?-->", "", section, flags=re.DOTALL)
    # ### で始まる各ブロック
    blocks = []
    for bm in re.finditer(r"^###\s+(.*?)(?=^###\s|\Z)", section, re.MULTILINE | re.DOTALL):
        blocks.append(bm.group(0).strip())
    return blocks


def block_title(block):
    first = block.splitlines()[0] if block else ""
    return re.sub(r"^###\s*", "", first).strip()


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックQ: 追加論点の準備(I-101/102/103)")
    scope = read_text(case_path(case_dir, "scope.md")) or ""
    blocks = split_blocks(scope)

    if not blocks:
        # 追加論点が無い案件（初回のみ）は該当なし。無音で正常終了。
        return res

    for block in blocks:
        title = block_title(block) or "(無題)"
        loc = f"追加論点: {title[:30]}"
        body = block.lower()

        # Q01 論点が一行で書かれているか
        if not title or title == "(無題)" or title.startswith("追加論点 n"):
            res.add("Q01", "WARN", loc,
                    "追加論点の問いが一行で書かれていない",
                    "### 追加論点 N: <問いを一行で> の形で論点を記入する")

        # Q02 決定的証拠が1件以上
        if "決定的証拠" not in block or re.search(r"決定的証拠:\s*$", block, re.MULTILINE):
            res.add("Q02", "WARN", loc,
                    "この問いの結論を左右する決定的証拠が記入されていない",
                    "決定的証拠を1件以上書く")

        is_superiority = bool(SUPERIORITY_RE.search(title))
        is_statement = bool(STATEMENT_RE.search(block))

        # 評価軸の行を抽出（「… 出所:」の形を想定した箇条書き）
        axis_lines = re.findall(r"^\s*[-*]\s*(.+?)…\s*出所[:：](.*)$", block, re.MULTILINE)
        # 出所を伴わない軸行（… が無い箇条書き。評価軸セクション内）
        axis_section = ""
        am = re.search(r"評価軸.*?:(.*?)(?=^-\s|\Z)", block, re.MULTILINE | re.DOTALL)
        if am:
            axis_section = am.group(1)
        axis_bullets = re.findall(r"^\s*[-*]\s*\S", axis_section, re.MULTILINE)

        if is_superiority:
            # Q03 優位性の問いなのに軸が2件未満
            if len(axis_bullets) < 2:
                res.add("Q03", "WARN", loc,
                        "『優位・競争力・技術力・先行』型の問いだが、評価軸が2件未満。"
                        "単一の視点に偏り、優劣を測る物差しの全体像を取りこぼす兆候",
                        "深掘り前に『この分野で優劣は何を基準に語られているか』を複数ソースで"
                        "調べ、評価軸を2件以上に分解してから数値を集める")
            # Q04 出所が1つも無い（気づきの合図として）
            elif not axis_lines:
                res.add("Q04", "WARN", loc,
                        "評価軸に出所が1つも無い。記憶だけで軸を並べている可能性があり、"
                        "他に見落としている軸があるかもしれない",
                        "各軸を『どのソースで重要と分かったか』で確認する。"
                        "外の情報源で軸の全体像を確かめ、抜けが無いか問い直す")

        # Q05 発言の検証なのに一次確認が無い
        if is_statement and "一次確認" not in block:
            res.add("Q05", "WARN", loc,
                    "検証対象に『発言』が含まれるが、発言そのものの一次確認（動画の該当箇所・"
                    "登壇資料・IR等）が記入されていない。要約だけで発言を検証する兆候",
                    "発言の指標・主語・数値を一次ソースで確定してから組み立てる。"
                    "一次特定できない場合は『発言主旨は未確認』と明示する")

        # Q06 鮮度基準が書かれていない
        if "鮮度基準" not in block:
            res.add("Q06", "WARN", loc,
                    "鮮度基準（何ヶ月より古い情報は警告か）が記入されていない。"
                    "トレンドの速い分野では古い情報が最新の潮目とそぐわず、誤った物差しを選ぶ",
                    "評価軸を調べる際に分かる『トレンドの動く速さ』から、"
                    "この論点の鮮度基準（何ヶ月）を決めて記入する")

    return res


if __name__ == "__main__":
    print_and_exit([run(sys.argv[1])], "チェックQ 実行結果",
                   sys.argv[1] if len(sys.argv) > 1 else ".", "Q")
