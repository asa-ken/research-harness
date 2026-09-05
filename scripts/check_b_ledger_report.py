#!/usr/bin/env python3
"""check_b_ledger_report.py - Wチェック② 証拠台帳 ⇔ レポート／図表

両方向を見る:
  - 「調べていないのに書いた」= 無出典文・数値不一致 (B02/B03)
  - 「調べたのに書き忘れた」= 孤立証拠・章欠落 (B07/B08)

usage: python3 scripts/check_b_ledger_report.py <case_dir>
"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    CATEGORIES, CheckResult, case_path, read_text, load_ledger,
    iter_report_units, parse_tags, extract_numbers, haystack_for_evidence,
    norm, safe_eval_arith, print_and_exit, EID_RE, TAG_RE,
    NEGATION_RE, COMPARISON_RE, evidence_text,
)

CALC_TOL = 0.005  # 0.5%
FORECAST_WORDS = ["予想", "ガイダンス", "見通し", "計画", "目標", "会社計画", "想定"]
ASSERTION_WORDS = ["である", "だ。", "している", "した", "増加", "減少", "拡大", "縮小",
                   "首位", "最大", "唯一", "上回", "下回", "優れ", "盤石", "圧倒的",
                   "確実", "劣位", "強み", "弱み", "できる", "見込"]

# 最上級・排他の主張。「出典さえ付いていれば通る」状態だったが、
# これらは『比較対象の全体を調べた』ことを前提とする主張であり、
# 個別の数値証拠だけでは支持できない（B21で扱う）。
SUPERLATIVE_WORDS = ["唯一", "最大", "最小", "最高", "最多", "最速", "最も", "首位",
                     "トップ", "No.1", "ナンバーワン", "圧倒的", "他に無い", "他にない",
                     "独占", "寡占", "世界初", "国内初", "業界初", "随一"]
# 最上級を支持しうる証拠側の表現。順位・シェア・比較の根拠が原文にあるか。
SUPERLATIVE_EVIDENCE_RE = re.compile(
    r"最大|最多|最高|最小|唯一|首位|第1位|第一位|1位|シェア|占有率|順位|ランキング|"
    r"上位|独占|寡占|initial|first|largest|leading|only")
REQUIRED_FIGURES = ["F-01", "F-02", "F-03", "F-04"]


# 語の同定に使う「特徴的な語」。助詞や一般語を拾わないよう長さで絞る。
TERM_RE = re.compile(r"[ァ-ヴー]{3,}|[一-龥]{2,}|[A-Za-z][A-Za-z0-9\-]{2,}")
STOPWORDS = {
    "当社", "同社", "会社", "当該", "今期", "前期", "今回", "以上", "以下", "場合",
    "可能性", "影響", "状況", "結果", "内容", "実施", "推移", "増加", "減少", "拡大",
    "縮小", "改善", "悪化", "見通", "見込", "報告", "確認", "記載", "情報", "調査",
    "分析", "検証", "仮説", "証拠", "指標", "水準", "傾向", "要因", "背景", "課題",
    "対応", "方針", "計画", "予想", "実績", "全体", "一部", "主要", "重要", "中心",
    # 実データ検証で誤検出の主因となった、財務文書に遍在する一般語・単位語。
    # これらは「別の箇所にある」ことに意味が無く、取り違えの兆候にならない。
    "百万円", "億円", "千円", "売上", "売上高", "利益", "営業利益", "経常利益",
    "総資産", "純資産", "負債", "資産", "説明", "記載", "前期", "当期", "通期",
    "四半期", "当第", "前年", "同期", "期末", "比率", "増加", "減少", "セグメント",
    "連結", "単体", "会社", "当社", "グループ", "事業", "業績", "決算", "開示",
    "情報", "通信", "需要", "製品", "顧客", "市場", "地域", "国内", "海外",
}


def check_terms(res, where, naked, tags, evidence, corpus, case_dir=None):
    """主張に出てくる固有の語が、引用した証拠の中にあるかを見る。

    レポートはパラフレーズが原則なので、語が一致しないこと自体は普通にある。
    だが『その語が原文コーパスのどこかには存在するのに、引用した箇所には無い』場合は、
    別の箇所を指す語を、無関係な引用に紐づけている疑いが強い（セグメントの取り違え等）。
    この非対称性だけを見ることで、パラフレーズによる誤検出を避ける。
    """
    cited = [evidence[e] for e in tags["eids"] if e in evidence]
    if not cited or not corpus:
        return
    quotes = " ".join(evidence_text(case_dir, e) for e in cited)
    suspects = []
    for term in set(TERM_RE.findall(naked)):
        if term in STOPWORDS or term in quotes:
            continue
        if term in corpus:
            suspects.append(term)
    # 双方向の不一致: 主張にしかない語と、引用にしかない語が同時に存在する場合、
    # 主語や対象がすり替わっている疑いが強い（デバイス⇔産業機器 のような取り違え）。
    claim_terms = {t for t in TERM_RE.findall(naked)
                   if t not in STOPWORDS and t not in quotes}
    quote_terms = {t for t in TERM_RE.findall(quotes)
                   if t not in STOPWORDS and t not in naked}
    # 表形式の引用（数値の羅列）は、本文の散文と語彙が一致しないのが当然。
    # 実データ検証でほぼ全行が発火したため、対象外とする。
    quotes_tabular = len(re.findall(r"\d[\d,]{4,}", quotes)) >= 3
    if claim_terms and quote_terms and not quotes_tabular:
        pair = f"主張のみ:{'、'.join(sorted(claim_terms)[:3])} / " \
               f"引用のみ:{'、'.join(sorted(quote_terms)[:3])}"
        res.add("B17", "WARN", where,
                "主張と引用で、指している対象が食い違っている可能性", pair)

    if suspects:
        res.add("B16", "WARN", where,
                f"主張中の語が引用に無く、原文の別の箇所にある: {'、'.join(sorted(suspects)[:4])}",
                "引用の取り違え（別セグメント・別期・別主体）の疑い。"
                "正しい箇所を引用しているか確認する")


def check_superlative(res, where, naked, tags, evidence, case_dir=None):
    """最上級・排他の主張が、その最上級を述べた証拠を持っているかを見る。

    「唯一・最大・首位」等は、個別の数値ではなく『比較対象の全体を調べた』
    ことを前提とする主張。自社の売上高が書かれた引用だけでは、
    それが業界最大であることの根拠にならない。

    これまでASSERTION_WORDSに語彙は存在したが、用途はB02（無出典文の検出）
    のみだった。つまり出典さえ付いていれば最上級は無検証で通っていた。
    """
    hits = [w for w in SUPERLATIVE_WORDS if w in naked]
    if not hits:
        return
    if tags["infer"]:
        return  # [推定]として書かれていれば、根拠と確信度はS07-S09が別途検査する

    cited = [evidence[e] for e in tags["eids"] if e in evidence]
    if not cited:
        return  # 無出典はB02が扱う

    quotes = " ".join(evidence_text(case_dir, e) for e in cited)
    if SUPERLATIVE_EVIDENCE_RE.search(quotes):
        return

    res.add("B21", "FAIL", where,
            f"最上級・排他の主張『{hits[0]}』だが、引用に順位・シェア等の根拠が無い",
            "最上級は比較対象の全体を調べた証拠が要る。"
            "第三者統計(T3)で裏を取るか、[推定|根拠:...|確信度:...|反証:...]に落とす")


def check_subject(res, where, naked, tags, evidence, all_subjects):
    """台帳に明示された主体（subject）と、レポートの主張の主体が一致するかを見る。

    B16/B17は自由語彙からの推測なので精度が低い。この検査は、証拠登録時に
    著者自身が明記した subject という統制語彙を使うため、より確度が高い。
    ただし ev['subject'] が空の証拠には適用されない（opt-in）。
    """
    cited = [(e, evidence[e]) for e in tags["eids"] if e in evidence]
    for eid, ev in cited:
        subject = str(ev.get("subject", "") or "").strip()
        if not subject:
            continue
        if subject in naked:
            continue
        others = [s for s in all_subjects if s and s != subject and s in naked]
        if others:
            res.add("B19", "FAIL", where,
                    f"{eid}の主体は『{subject}』だが、主張には別の主体『{others[0]}』が"
                    "使われている", "セグメント・子会社・製品の取り違えの疑い")


def parse_necessity_items(case_dir):
    """scope.mdの必要証拠リストを解析する。check_a/check_b両方から使う。

    テーブル形式: | ID | 証拠要件 | 重要度 | 想定ソース | 状態 |
    返り値: [{"id":"N-01","requirement":"...","importance":"C","state":"..."}]
    """
    text = read_text(case_path(case_dir, "scope.md"))
    if not text:
        return []
    items = []
    in_table = False
    for line in text.splitlines():
        s = line.strip()
        if "必要証拠リスト" in s:
            in_table = True
            continue
        if in_table and s.startswith("##"):
            break
        if not in_table or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5 or re.match(r"^[\s:\-]+$", cells[0]):
            continue
        if cells[0] in ("ID", ""):
            continue
        items.append({"id": cells[0], "requirement": cells[1],
                      "importance": cells[2], "source": cells[3], "state": cells[4]})
    return items


def load_evidence(case_dir):
    ev = {}
    for _, row in load_ledger(case_dir):
        if row.get("eid"):
            ev[row["eid"]] = row
    return ev


def figure_rows(path):
    """図ファイルのデータ表から (行番号, セル配列, ヘッダ) を返す。"""
    header = None
    for lineno, line in enumerate(read_text(path).splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if re.match(r"^[\s:\-\|]+$", s.strip("|")):
            continue
        if header is None:
            header = cells
            continue
        yield lineno, cells, header


def check_numbers(res, where, unit, tags, evidence, case_dir=None):
    """文中の数値が、引用したE-IDの証拠内に存在するかを照合する。"""
    cited = [evidence[e] for e in tags["eids"] if e in evidence]
    if not cited:
        return
    hay = " ".join(haystack_for_evidence(e, case_dir) for e in cited)
    for raw, val, strict in extract_numbers(unit):
        if norm(val) in hay:
            continue
        if tags["calc"] or tags["infer"]:
            continue  # 計算値・推定値は B04 / B05 側で扱う
        level = "FAIL" if strict else "WARN"
        res.add("B03", level, where,
                f"数値 {raw} が引用証拠内に見当たらない",
                "引用元を確認するか[推定]/[計算]に落とすこと")


def check_calc(res, where, unit, tags, evidence):
    for body in tags["calc"]:
        m = re.search(r"式\s*[:：]\s*(.+)$", body)
        if not m:
            res.add("B04", "FAIL", where, "[計算]に式が無い", body[:60])
            continue
        expr = m.group(1).strip()
        subst = expr
        missing = []
        for eid in EID_RE.findall(expr):
            ev = evidence.get(eid)
            num = (ev or {}).get("value", {}).get("number") if ev else None
            if num is None:
                missing.append(eid)
            else:
                subst = subst.replace(eid, str(num))
        if missing:
            res.add("B04", "WARN", where,
                    f"式中のE-IDに数値が無く再計算できない: {','.join(missing)}")
            continue
        subst = re.sub(r"[A-Za-z_]", "", subst) if re.search(r"[A-Za-z]", subst) else subst
        result = safe_eval_arith(subst)
        if result is None:
            res.add("B04", "WARN", where, "式を再計算できない（記号を含む）", expr[:50])
            continue
        nums = [float(v) for _, v, _ in extract_numbers(unit)]
        if not nums:
            continue
        if not any(abs(n - result) <= max(abs(result) * CALC_TOL, 1e-9) for n in nums):
            res.add("B04", "FAIL", where,
                    f"再計算値 {result:.6g} が本文の数値と一致しない",
                    f"式: {expr} / 本文: {nums}")


def check_semantics(res, where, naked, tags, evidence, case_dir=None):
    """引用と主張の向きが合っているかを、限定的だが機械的に検査する。

    意味の一致は完全には検証できないが、「引用に否定が無いのに否定を主張する」
    「単一時点の証拠で変化を主張する」という2つの典型的な逸脱は形で捕まえられる。
    """
    cited = [evidence[e] for e in tags["eids"] if e in evidence]
    if not cited:
        return
    # 判定には原文（quote）だけを使う。fact はClaudeが書いた正規化文なので、
    # そこに比較表現や否定が入っていると、自分の記述で自分を承認することになる。
    quotes = " ".join(evidence_text(case_dir, e) for e in cited)

    # B13: 否定の主張には、引用側にも否定の裏付けが要る
    if NEGATION_RE.search(naked) and not tags["infer"] and not tags["status"]:
        if not NEGATION_RE.search(quotes) and not any(
                e.get("claim_type") == "negative" for e in cited):
            res.add("B13", "FAIL", where,
                    "否定の主張だが、引用側に否定の裏付けが無い",
                    "引用と逆向きの主張になっていないか確認。"
                    "『記載が無い』ことを言うなら claim_type:negative の証拠を使う")

    # B14: 変化の主張には2時点の証拠が要る
    if COMPARISON_RE.search(naked) and not tags["calc"] and not tags["infer"]:
        periods = {str((e.get("value") or {}).get("period", "")) for e in cited}
        periods.discard("")
        if len(cited) < 2 and len(periods) < 2:
            # 「前期比」だけでなく「前連結会計年度比」等の開示文書の定型表現、
            # および「N%増/減」のような比率表現も、引用自体が比較を含む証拠として認める
            comparative_quote = (
                COMPARISON_RE.search(quotes)
                or re.search(r"前[連結事業]*[会計]*年度比|前年同[月期四半期]+比", quotes)
                or re.search(r"\d+(?:\.\d+)?\s*(?:%|％|ポイント|pt)\s*(?:増|減)", quotes)
            )
            if not comparative_quote:
                res.add("B14", "FAIL", where,
                        "変化・比較の主張だが、証拠が1時点しかない",
                        "比較には2期分のE-IDか[計算]タグが要る")


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックB: 台帳⇔レポート")
    evidence = load_evidence(case_dir)
    if not evidence:
        res.add("B00", "FAIL", "ledger.jsonl", "台帳が空")
        return res

    report_path = case_path(case_dir, "report.md")
    fig_paths = sorted(glob.glob(case_path(case_dir, "figures", "*.md")))
    if not os.path.exists(report_path):
        res.add("B00", "FAIL", "report.md", "レポートが存在しない")
        return res

    referenced = set()
    all_subjects = {str(e.get("subject", "") or "").strip() for e in evidence.values()}
    report_text = read_text(report_path)
    corpus = " ".join(read_text(p) for p in
                      sorted(glob.glob(case_path(case_dir, "raw_text", "*.txt"))))

    # ---- 本文
    # B02の例外判定に使う文脈情報。iter_report_unitsは見出しを除外するため、
    # 行番号から現在のセクションを引けるマップを別途作る。
    section_at_line = {}
    _cur = ""
    for _ln, _line in enumerate(report_text.splitlines(), 1):
        if _line.strip().startswith("#"):
            _cur = _line.strip("# ").strip()
        section_at_line[_ln] = _cur

    current_section = ""
    prev_unit_had_evidence = False
    for where, unit in iter_report_units(report_text, "report.md"):
        _m = re.search(r":L(\d+)$", where)
        _sec = section_at_line.get(int(_m.group(1)), "") if _m else ""
        if _sec != current_section:
            # 節が変われば根拠の文脈は切れる
            prev_unit_had_evidence = False
        current_section = _sec
        tags = parse_tags(unit)
        for eid in tags["eids"]:
            referenced.add(eid)
            if eid not in evidence:
                res.add("B01", "FAIL", where, f"参照 {eid} が台帳に存在しない")

        has_any_tag = bool(tags["eids"] or tags["calc"] or tags["infer"] or tags["status"])
        naked = TAG_RE.sub(" ", unit)
        nums = [n for n in extract_numbers(unit) if n[2]]
        assertive = any(w in naked for w in ASSERTION_WORDS)

        # 実データ検証で判明した、出典を持ち得ない正当な記述の類型を除外する。
        # これらをFAILにすると、レポートに必須の構成要素が書けなくなる。
        #  1) 冒頭のメタ情報行（調査基準日・使用ソース等）
        #  2) 直前の行が根拠付きで、その解釈・含意を述べる文
        #  3) 仮説表・ソース一覧のように、セル内にE-IDを列挙する表
        #  4) 「本調査の限界」節のように、調査自体について述べる記述
        is_meta_line = bool(re.match(
            r"^\s*[-*]?\s*(調査基準日|調査範囲|使用ソース|ゲート結果|本調査|"
            r"次の確認タイミング|監視すべき指標)", naked.strip()))
        is_eid_table_row = (unit.strip().startswith("|")
                            and len(EID_RE.findall(unit)) >= 1)
        in_limitations = "限界" in current_section or "付録" in current_section
        is_interpretation = (prev_unit_had_evidence
                             and not nums
                             and bool(re.match(r"^\s*\*{0,2}(ただし|なお|つまり|これは|"
                                               r"一方|逆に|裏返せば|したがって|以上より)",
                                               naked.strip())))

        exempt = (is_meta_line or is_eid_table_row or in_limitations
                  or is_interpretation)

        if not has_any_tag and not exempt and (nums or (assertive and len(naked) > 12)):
            res.add("B02", "FAIL", where, "出典の無い記述",
                    naked[:60])

        check_numbers(res, where, unit, tags, evidence, case_dir)
        check_calc(res, where, unit, tags, evidence)
        check_semantics(res, where, naked, tags, evidence, case_dir)
        check_terms(res, where, naked, tags, evidence, corpus, case_dir)
        check_subject(res, where, naked, tags, evidence, all_subjects)
        check_superlative(res, where, naked, tags, evidence, case_dir)
        # 根拠の文脈は段落単位で継続する。同一段落内で一度でも根拠が示されていれば、
        # それに続く解釈・含意の文は文脈上の根拠を持つとみなす。
        # （文単位でリセットすると、根拠文→補足文→解釈文の並びで解釈文が孤立する）
        if has_any_tag:
            prev_unit_had_evidence = True
        elif nums:
            # 新たな数値を持ち出す文は、独立した主張なので文脈を引き継がせない
            prev_unit_had_evidence = False

        for body in tags["infer"]:
            joined = "|".join(body.split("|")[1:])
            if not (EID_RE.search(joined) and "確信度" in joined and "反証" in joined):
                res.add("B05", "FAIL", where,
                        "[推定]に根拠E-ID/確信度/反証条件のいずれかが欠落", body[:60])

        for eid in tags["eids"]:
            ev = evidence.get(eid)
            if ev and ev.get("claim_type") == "forecast":
                if not any(w in naked for w in FORECAST_WORDS):
                    res.add("B09", "FAIL", where,
                            f"{eid}は会社予想だが、予想と明示せず断定している", naked[:50])
            if ev and ev.get("claim_type") == "opinion" and not tags["infer"]:
                res.add("B09", "WARN", where,
                        f"{eid}は第三者見解。事実として扱っていないか確認", naked[:50])

    # ---- 図表
    for path in fig_paths:
        name = os.path.basename(path)
        has_basis_col = False
        for lineno, cells, header in figure_rows(path):
            idx = next((i for i, h in enumerate(header) if "根拠" in h), None)
            if idx is None:
                continue
            has_basis_col = True
            basis = cells[idx] if idx < len(cells) else ""
            where = f"{name}:L{lineno}"
            if not basis or basis in {"-", "—"}:
                res.add("B06", "FAIL", where, "データ表に根拠の無い行がある",
                        " | ".join(cells)[:60])
                continue
            if "推定" in basis:
                continue
            eids = EID_RE.findall(basis)
            if not eids:
                res.add("B06", "FAIL", where, "根拠欄にE-IDも[推定]も無い", basis[:40])
            for eid in eids:
                referenced.add(eid)
                if eid not in evidence:
                    res.add("B01", "FAIL", where, f"参照 {eid} が台帳に存在しない")
        if not has_basis_col:
            res.add("B06", "WARN", name, "根拠列を持つデータ表が見つからない")

    if not fig_paths:
        res.add("B06", "FAIL", "figures/", "図解が1つも無い（最小セットF-01〜F-04を作成）")

    # ---- 逆方向: 取りこぼし
    orphans = [e for e in evidence if e not in referenced]
    if orphans:
        res.add("B07", "WARN", "ledger.jsonl",
                f"レポート・図のどちらにも使われていない証拠が{len(orphans)}件",
                ",".join(sorted(orphans)[:12]))

    # ---- 章の欠落（見出しに名前を書くだけでは満たされない）
    used_tags = set()
    for eid in referenced:
        for t in (evidence.get(eid, {}).get("tags") or []):
            used_tags.add(t)
    status_covered = set()
    for cat in CATEGORIES:
        for m in re.finditer(re.escape(cat), report_text):
            window = report_text[m.start():m.start() + 200]
            if re.search(r"\[(非公表|未調査|調査不可)", window):
                status_covered.add(cat)
                break
    for cat in CATEGORIES:
        if cat not in used_tags and cat not in status_covered:
            res.add("B08", "WARN", "report.md",
                    f"カテゴリ『{cat}』に、使用された証拠もステータス記述も無い",
                    "調査対象外なら[未調査|意図的|理由:～]と明示すること")

    # B20: 複数カテゴリ名を1行に並べ、共有の1個のステータスで一括処理していないか。
    # B08は「カテゴリ名の直後200字にステータスがあるか」しか見ないため、
    # カテゴリ名を列挙して末尾に1個だけ理由を書けば、個別の吟味なしに全部を
    # 黙らせられる。これは技術的にはB08を通るが、質の低下を招く典型パターン。
    cat_pattern = "|".join(re.escape(c) for c in CATEGORIES)
    for m in re.finditer(rf"(?:(?:{cat_pattern})\s*[/／、,]\s*){{2,}}(?:{cat_pattern})",
                         report_text):
        window = report_text[m.end():m.end() + 100]
        if re.search(r"\[(非公表|未調査|調査不可)", window):
            names = re.findall(cat_pattern, m.group(0))
            res.add("B20", "WARN", "report.md",
                    f"{len(names)}カテゴリを1つの理由で一括スキップしている",
                    f"対象: {'、'.join(names)}。個別の理由が本当に共通か確認する"
                    "（B08は形式上は通るが、実質的な吟味を伴わない一括処理になりやすい）")

    # ---- B18: scope.mdで採用した問いが、レポートで扱われているか
    scope_text = read_text(case_path(case_dir, "scope.md"))
    if scope_text:
        adopted = set(re.findall(r"Q-[A-Z]+\d+", scope_text))
        combined = report_text + " ".join(read_text(p) for p in fig_paths)
        # 問いIDが直接書かれていなくても、証拠タグかステータス記述で扱われていればよい
        unanswered = [q for q in sorted(adopted) if q not in combined]
        if unanswered:
            res.add("B18", "WARN", "scope.md",
                    f"採用した問いのうち、レポートで参照されていないものが{len(unanswered)}件",
                    ",".join(unanswered[:8]) +
                    " / 扱わなかったなら[未調査|意図的]と明示するか、問いIDを本文に残す")

    # ---- B22: 必要証拠リストのCritical項目が未解決のまま残っていないか
    # scope.md の必要証拠リストは、これまでどのスクリプトからも検証されておらず、
    # 「結論を左右する項目が未取得のまま」でもゲートBは通っていた。
    items = parse_necessity_items(case_dir)
    unresolved_critical = []
    for it in items:
        if it["importance"].upper().startswith("C"):
            resolved = (EID_RE.search(it["state"])
                        or re.search(r"非公表|調査不可|取得済|未特定", it["state"]))
            if not resolved:
                unresolved_critical.append(f"{it['id']}:{it['requirement'][:25]}({it['state']})")
    if unresolved_critical:
        res.add("B22", "FAIL", "scope.md",
                f"必要証拠リストのCritical項目が{len(unresolved_critical)}件未解決",
                "; ".join(unresolved_critical[:4]) +
                " / 取得するか、[非公表]・[調査不可]・[未特定]としてレポートで扱うか、"
                "重要度をNに落とす判断を明示する")

    # ---- B15: 最小図解セット
    present = {os.path.basename(p)[:4] for p in fig_paths}
    missing_figs = [f for f in REQUIRED_FIGURES if f not in present]
    if fig_paths and missing_figs:
        res.add("B15", "FAIL", "figures/",
                f"最小図解セットが不足: {','.join(missing_figs)}",
                "F-01収益分解 / F-02競合マップ / F-03時系列 / F-04仮説ツリー は必須")
    if fig_paths and "F-05" not in present:
        res.add("B15", "WARN", "figures/", "F-05（リスク・感応度）が無い")

    # ---- 引用の量
    quotes = re.findall(r"[「\"]([^「」\"]{20,})[」\"]", report_text)
    for q in quotes:
        if len(q) > 60:
            res.add("B10", "WARN", "report.md", "直接引用が長い（パラフレーズを優先）",
                    q[:40])
    src_of_quote = {}
    for q in quotes:
        for eid, ev in evidence.items():
            if norm(q) and norm(q) in norm(evidence_text(case_dir, ev)):
                sid = ev.get("source_id")
                src_of_quote[sid] = src_of_quote.get(sid, 0) + 1
    for sid, n in src_of_quote.items():
        if n > 1:
            res.add("B10", "WARN", "report.md",
                    f"同一ソース {sid} から{n}回直接引用している（1回までに）")
    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    print_and_exit([run(case_dir)], "ゲートB: 台帳⇔レポート", case_dir, "B")


if __name__ == "__main__":
    main()
