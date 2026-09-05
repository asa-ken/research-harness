#!/usr/bin/env python3
"""check_freshness.py - 情報の鮮度チェック（公開日ベース）

古い情報だけで結論を出すと、最新のトレンドとそぐわない物差しで分析してしまう
（実運用の教訓: キオクシアが電力効率を語る背景はデータセンター急拡大という
「今」の事情。古い情報ではこの潮目を外し、時代遅れの物差し=容量密度で測った）。

各証拠が属するソースの published_at（公開日）を、scope.md の鮮度基準と照合する。

F01: 証拠が属するソースに published_at（公開日）が無い。
     → 鮮度を判断できない。公開日の記録を必須にする。
F02: 公開日が鮮度基準より古い。
     → 最新トレンドとそぐわない情報で分析している兆候。

鮮度基準の決め方（証拠ごとに、以下の順で1つ選ぶ）:
  1. 証拠に topic:N（追加論点Nのための証拠、の印）があり、その追加論点ブロックに
     「鮮度基準: M ヶ月」が書かれていれば、それを使う（論点別基準）。
  2. 無ければ scope.md 冒頭「鮮度基準（既定）: N ヶ月」を使う（案件全体の既定）。
  3. どちらも無ければ 24ヶ月。

  topic を付けない証拠は従来通り案件既定で判定されるので、既存案件はそのまま動く。
  トレンドの速い論点だけ、その論点の証拠に topic:N を付けて短い基準で締める。

段階導入: 当面 WARN。定着したら F02 を FAIL に上げる。

起点日: basis_datetime か、無ければ本日。「基準日から見て何ヶ月前の情報か」で判断。

usage: python3 scripts/check_freshness.py <case_dir>
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    CheckResult, case_path, read_text, load_ledger, load_sources, print_and_exit,
)

DEFAULT_MONTHS = 24


def parse_default_months(scope_text):
    """scope.md 冒頭の『鮮度基準（既定）: N ヶ月』から月数を読む。無ければ既定値。"""
    if not scope_text:
        return DEFAULT_MONTHS
    m = re.search(r"鮮度基準（既定）[:：]\s*(\d+)\s*ヶ月", scope_text)
    return int(m.group(1)) if m else DEFAULT_MONTHS


def parse_topic_months(scope_text):
    """追加論点ブロックごとの鮮度基準を読む。

    「### 追加論点 N: ...」で始まる各ブロック内の「鮮度基準: M ヶ月」を拾い、
    {論点番号N(int): 月数M(int)} を返す。番号の無いブロックや基準の無いブロックは含めない。
    証拠側の topic:N がこの番号と対応する。
    """
    out = {}
    if not scope_text:
        return out
    m = re.search(r"^##\s*追加論点.*$", scope_text, re.MULTILINE)
    if not m:
        return out
    section = scope_text[m.end():]
    nxt = re.search(r"^##\s", section, re.MULTILINE)
    if nxt:
        section = section[:nxt.start()]
    section = re.sub(r"<!--.*?-->", "", section, flags=re.DOTALL)
    for bm in re.finditer(r"^###\s+追加論点\s*(\d+)\s*[:：](.*?)(?=^###\s|\Z)",
                          section, re.MULTILINE | re.DOTALL):
        num = int(bm.group(1))
        body = bm.group(0)
        fm = re.search(r"鮮度基準[:：]\s*(?:この論点では\s*)?(\d+)\s*ヶ月", body)
        if fm:
            out[num] = int(fm.group(1))
    return out


def parse_date(s):
    """YYYY-MM-DD / YYYY-MM / YYYY を date に。失敗は None。"""
    if not s:
        return None
    s = str(s).strip()[:10]
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def months_between(older, newer):
    return (newer.year - older.year) * 12 + (newer.month - older.month)


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックF: 情報の鮮度(公開日)")
    scope = read_text(case_path(case_dir, "scope.md")) or ""
    default_months = parse_default_months(scope)
    topic_months = parse_topic_months(scope)
    sources, _ = load_sources(case_dir)

    for _lineno, ev in load_ledger(case_dir):
        eid = ev.get("eid")
        if not eid:
            continue
        sid = ev.get("source_id")
        src = sources.get(sid, {})
        pub = parse_date(src.get("published_at"))
        loc = eid

        # この証拠に適用する鮮度基準を決める。
        # 証拠に topic:N があり、その論点に基準があれば論点別基準。無ければ案件既定。
        topic = ev.get("topic")
        limit_months = default_months
        basis_label = "案件既定"
        if topic is not None:
            try:
                tnum = int(topic)
            except (ValueError, TypeError):
                tnum = None
            if tnum is not None and tnum in topic_months:
                limit_months = topic_months[tnum]
                basis_label = f"追加論点{tnum}"

        if pub is None:
            res.add("F01", "WARN", loc,
                    f"証拠のソース({sid})に公開日(published_at)が無く、鮮度を判断できない",
                    "sources.json に published_at（YYYY-MM-DD）を記録する")
            continue

        # 起点: 基準日 basis_datetime か basis_date、無ければ本日
        base = parse_date(ev.get("basis_datetime") or ev.get("basis_date")) or date.today()
        age = months_between(pub, base)
        if age > limit_months:
            res.add("F02", "WARN", loc,
                    f"公開日 {pub.isoformat()} は基準より約{age}ヶ月前で、"
                    f"鮮度基準({basis_label}: {limit_months}ヶ月)より古い。"
                    f"最新トレンドとそぐわない情報で分析している可能性",
                    "より新しいソースを探すか、この論点のトレンドが本当に安定しているかを"
                    "確認する。安定しているなら鮮度基準を明示的に緩める")
    return res


if __name__ == "__main__":
    print_and_exit([run(sys.argv[1])], "チェックF 実行結果",
                   sys.argv[1] if len(sys.argv) > 1 else ".", "F")
