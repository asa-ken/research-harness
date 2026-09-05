#!/usr/bin/env python3
"""check_a_source_ledger.py - Wチェック① ソース ⇔ 証拠台帳

「引用が本当に原文に存在するか」を文字列一致で検証する。
ここを通らない記述は、以降どれだけ整合していても根拠を持たない。

usage: python3 scripts/check_a_source_ledger.py <case_dir>
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    CheckResult, case_path, read_text, load_ledger, load_sources,
    sha256_text, norm, number_variants, print_and_exit, flexible_find, nfkc,
    load_reverify_log, resolve_anchor, ANCHOR_MAX_LEN,
)
from check_b_ledger_report import parse_necessity_items  # noqa: E402

REQUIRED = ["eid", "source_id", "claim_type", "anchor_head", "anchor_tail",
            "fact", "basis_date", "confidence"]
CLAIM_TYPES = {"fact", "negative", "forecast", "opinion"}
LOW_TIERS = {"T5", "T6"}


# 主張の種類ごとに、どのTierのソースなら根拠になるか。
# 例: 市場規模やシェアを発行体自身の資料(T2)だけで語ると、会社の自称を事実として書くことになる。
TIER_POLICY = {
    "財務.実績": {"allow": {"T1", "T2"}, "level": "FAIL",
                  "why": "実績値は法定開示か発行体一次資料で取る"},
    "財務.健全性": {"allow": {"T1", "T2"}, "level": "FAIL",
                    "why": "財務の健全性は法定開示で確認する"},
    "市場環境": {"allow": {"T1", "T3", "T4"}, "level": "WARN",
                 "why": "市場規模・成長率を発行体の自称に依存させない（T3公的統計で裏を取る）"},
    "競争環境": {"allow": {"T1", "T3", "T4"}, "level": "WARN",
                 "why": "シェアの出所と定義を第三者統計で確認する"},
    "財務.株価指標": {"allow": {"T4", "T1"}, "level": "WARN",
                      "why": "株価指標は市場データから取る"},
}

# 引用の周辺にあると意味が変わりうる語。引用がこれらを含まずに切られていたら、
# 留保や条件を落としている可能性がある。
# 意味を反転・限定しうる語だけを対象にする。
# 「なお」「一方」のような弱い接続詞は日本語の開示文書で頻出し、
# 入れると警告が飽和して読まれなくなるため除外した。
HEDGE_RE = re.compile(
    r"ただし|但し|除いて|除く|除き|限り|場合を除|を控除|遡及|組替|"
    r"変更後|変更前|暫定|速報値|一過性|特殊要因|except|however|excluding")
SENT_END_RE = re.compile(r"[。．\.]\s*$|」\s*$|であります$|ます$")
SENT_START_OK_RE = re.compile(r"(?:^|[。．\n】）\)」]\s*)$")


def check_source_fit(res, loc, ev, src):
    """調査項目に対して、ソースの種別が適切かを見る。"""
    tier = str(src.get("source_class", "")).upper()
    if not tier:
        return
    for tag in (ev.get("tags") or []):
        policy = TIER_POLICY.get(tag)
        if not policy:
            continue
        if tier not in policy["allow"]:
            note = ev.get("note", "")
            if substantive_ack(note, re.compile(r"出所|代替なし")):
                continue  # 制約を認識した上での採用は許容（実質的な説明があれば）
            res.add("A17", policy["level"], loc,
                    f"『{tag}』の根拠が{tier}ソース（推奨: {'/'.join(sorted(policy['allow']))}）",
                    policy["why"] + "。やむを得ず使う場合はnoteに出所と限界を"
                    f"{SUBSTANTIVE_MIN_LEN}字以上で具体的に書く（単語だけでは通らない）")


def check_quote_context(res, loc, ev, raw, offsets=None, quote=None):
    """引用の切り出し範囲を検査する。

    引用が原文に存在しても、直前直後の留保・条件を落として切り出せば、
    意味は変わる。前後の窓を見て、落とした可能性を機械的に指摘する。
    新形式では台帳に原文が無いため、解決済みの範囲から読み出した文字列を受け取る。
    """
    cs, ce = offsets if offsets else (ev.get("char_start"), ev.get("char_end"))
    if cs is None or ce is None or not raw:
        return
    if quote is None:
        quote = raw[cs:ce]
    if not quote:
        return

    before = raw[max(0, cs - 100):cs]
    after = raw[ce:ce + 100]

    # 文の途中で切っていないか
    # 財務諸表の表形式データ（「売上高 267,908 / 402,009」等）は句点で終わらないのが
    # 通例。実データ検証で正常な引用が大量にWARNになったため、表形式は対象外とする。
    is_tabular = bool(re.search(r"\d[\d,]*\s*[/／|]\s*\d|\d[\d,]{4,}\s+\S+\s+\d[\d,]{4,}",
                                quote)
                      # 「売上高 1,755,000百万円 48.4% 営業利益 432,000百万円」のように
                      # 数値＋単位＋比率が複数回並ぶ業績予想表の形式も対象に含める
                      or len(re.findall(r"\d[\d,]*(?:\.\d+)?\s*(?:百万円|億円|%|％)", quote)) >= 3)
    if not is_tabular:
        if not SENT_END_RE.search(quote.strip()):
            res.add("A18", "WARN", loc, "引用が文末で終わっていない（文の途中で切っている）",
                    "条件節や結論部を落としていないか確認する")
        if before and not re.search(r"[。．\n】）\)」　]\s*$", before):
            res.add("A18", "WARN", loc, "引用が文頭から始まっていない（文の途中から切っている）",
                    f"直前: ...{before[-20:]}")

    # 前後に留保・条件があり、引用がそれを含んでいない
    for label, window in (("直前", before), ("直後", after)):
        hits = set(HEDGE_RE.findall(window)) - set(HEDGE_RE.findall(quote))
        if hits:
            res.add("A18", "WARN", loc,
                    f"{label}に留保・条件語がある（引用に含まれていない）: {'、'.join(sorted(hits))}",
                    "文脈を切り取って意味を変えていないか確認する")

    # ページ境界をまたいでいないか（PDF抽出のマーカー）
    if "<<<PAGE" in raw[cs:ce]:
        res.add("A18", "WARN", loc, "引用がページ境界をまたいでいる",
                "抽出時のヘッダ・フッタが混入していないか確認する")


EXPLICIT_PERIOD_RE = re.compile(
    r"(\d{2,4}\s*年\s*\d{1,2}\s*月期|FY\s*\d{2,4}|\d{4}年度|第\d四半期|[1-4]Q)")


def check_period(res, loc, period, quote, note, ev, src):
    """value.period の裏付けを段階的に確認する。

    法定開示は『当連結会計年度』と書き、期を明示しないことが多い。
    毎回noteを要求すると摩擦が大きいので、文書全体の対象期を
    sources.json の period_context に一度だけ宣言する運用を許す。
    危険なのは『引用に別の期が明示されているのに、別の期を記録している』ケースなので、
    そこだけをFAILにする。
    """
    hay_q = norm(quote)
    digits = re.findall(r"\d+", nfkc(period))
    if digits and all(d in hay_q for d in digits):
        return
    bdt = str(ev.get("basis_datetime", "") or "")
    if digits and bdt and all(d in norm(bdt) for d in digits):
        return
    ctx = str(src.get("period_context", "") or "")
    if ctx and (norm(period) in norm(ctx) or norm(ctx) in norm(period)):
        return
    if substantive_ack(note, re.compile(r"期|年度|FY|四半期")):
        return

    # 文書の対象期が宣言済みで、それと違う期を記録している場合。
    # 引用が「前連結会計年度」等の相対表現なら正当なので警告に留める。
    if ctx:
        forward = (ev.get("claim_type") == "forecast"
                   or re.search(r"次期|来期|翌連結会計年度|翌事業年度|見込|予想|計画", quote))
        if forward or re.search(r"前連結会計年度|前事業年度|前期|前年|前四半期|過去", quote):
            res.add("A16", "WARN", loc,
                    f"引用が相対表現（前期・次期等）で、value.period『{period}』を機械判定できない",
                    f"文書の対象期は『{ctx}』。noteに期の根拠を書くこと")
        else:
            res.add("A16", "FAIL", loc,
                    f"文書の対象期『{ctx}』と value.period『{period}』が食い違う", quote[:40])
        return

    explicit = EXPLICIT_PERIOD_RE.findall(quote)
    if explicit and not any(norm(period) in norm(e) or norm(e) in norm(period)
                            for e in explicit):
        res.add("A16", "FAIL", loc,
                f"引用には『{explicit[0]}』とあるのに value.period が『{period}』",
                "期の取り違えは前期比較を壊す")
    else:
        res.add("A16", "WARN", loc,
                f"value.period『{period}』の根拠が引用から特定できない",
                "sources.json の period_context に文書の対象期を宣言するか、noteに書く")


# 取引所の引け時刻（現地時間）。UTCオフセットから市場を推定する。
CLOSE_BY_OFFSET = {
    "+09:00": ("東証", 15, 30),   # 2024年11月以降は15:30引け
    "-04:00": ("米国市場", 16, 0),  # EDT
    "-05:00": ("米国市場", 16, 0),  # EST
}
PRICE_WORD = re.compile(r"株価|終値|時価総額|PER|PBR|PSR|EV/EBITDA|利回り|EPS|BPS")


# 前提条件・算定基礎を示す見出し語。開示文書では冒頭〜前段にまとまることが多い。
# 局所窓(A18)では拾えない「離れた場所にある前提」を検出するために、文書全体から探す。
PREMISE_RE = re.compile(
    r"前提条件|前提として|算定の基礎|算定にあたっての前提|試算の前提|業績予想の前提|"
    r"注記事項|key assumptions?|forward-looking statements|unless otherwise (?:stated|noted)")
PREMISE_ACK_RE = re.compile(r"前提|算定|assumption")


def check_premise_zone(res, loc, ev, raw, resolved_offsets):
    """引用が文書の後半にあり、冒頭側に前提条件の記載がある場合に指摘する。

    局所窓(check_quote_context)は引用のすぐ前後しか見ないため、
    『前提は冒頭、根拠は後半』という開示文書によくある配置を検出できない。
    これは文書全体を走査することで補う。
    """
    if not raw or not resolved_offsets:
        return
    cs, _ = resolved_offsets
    if cs is None:
        return

    doc_len = len(raw)
    preamble_end = min(2000, max(500, int(doc_len * 0.15)))
    if cs < preamble_end:
        return  # 引用自体が前提ゾーン内にあるので対象外

    preamble = raw[:preamble_end]
    m = PREMISE_RE.search(preamble)
    if not m:
        return

    note = ev.get("note", "")
    if substantive_ack(note, PREMISE_ACK_RE):
        return  # 前提を確認済みと実質的な記述がnoteに残っている

    res.add("A19", "WARN", loc,
            "文書冒頭側に前提条件の記載があるが、引用は離れた位置（後半）にある",
            f"冒頭付近『{preamble[max(0,m.start()-10):m.end()+20].strip()}』"
            f"を確認し、矛盾が無ければnoteに確認内容を{SUBSTANTIVE_MIN_LEN}字以上で書くこと")


# 連結/単体・累計/単四半期など、集計範囲を示す語。
SCOPE_TERMS = {
    "連結": r"連結", "単体": r"(?<!連)単体|個別財務諸表",
    "累計": r"累計", "単四半期": r"第[1-4１-４]四半期(?!累計)|単独の四半期",
}

# キーワードを含むだけの空文言（「期」「前提」等の単語1つだけ）でFAILを
# 黙らせられないようにする最低文字数。「なぜそう判断したか」を書かせる意図。
SUBSTANTIVE_MIN_LEN = 15


def substantive_ack(note: str, pattern) -> bool:
    """noteが該当パターンを含み、かつ空文言でない実質的な記述かを見る。

    以前は pattern.search(note) だけで判定しており、note="期" のような
    単語1つでFAILを黙らせられた。最低文字数を課すことで、
    「キーワードを置くだけ」を防ぐ（完全な意味検証ではないが、ゼロ努力は防げる）。
    """
    return bool(note) and bool(pattern.search(note)) and len(note.strip()) >= SUBSTANTIVE_MIN_LEN


def check_scope_consistency(res, loc, ev, quote, raw=None, offsets=None):
    """value.basis_scope（連結/単体など）が引用と矛盾していないかを見る。

    『主体の同一性』のうち、法人・集計範囲の取り違えを検出する。
    セグメント名の取り違えはB19（レポート側）で扱うため、ここではscopeのみ。
    """
    val = ev.get("value")
    if not isinstance(val, dict):
        return
    scope = str(val.get("basis_scope", "") or "")
    if not scope:
        return
    scope_key = None
    for key in SCOPE_TERMS:
        if key in scope:
            scope_key = key
            break
    if not scope_key:
        return
    pattern = SCOPE_TERMS[scope_key]
    # 連結/単体の区分も、表ヘッダや文書冒頭で一度宣言されるのが通例。
    # 引用文字列だけでなく、原文中の引用位置より手前も探索範囲に含める。
    search_zone = quote
    if raw and offsets and offsets[0] is not None:
        search_zone = raw[max(0, offsets[0] - 1500):offsets[1] or offsets[0]]
    if not re.search(pattern, search_zone):
        # 反対のスコープが明示されていれば矛盾、そうでなければ「未確認」に留める
        opposite = {"連結": "単体", "単体": "連結",
                   "累計": "単四半期", "単四半期": "累計"}.get(scope_key)
        if opposite and re.search(SCOPE_TERMS.get(opposite, ""), search_zone):
            res.add("A20", "FAIL", loc,
                    f"value.basis_scope『{scope}』だが引用は『{opposite}』の数値",
                    "連結/単体・累計/単四半期の取り違えは値そのものを誤らせる")
        else:
            res.add("A20", "WARN", loc,
                    f"value.basis_scope『{scope}』が引用中で確認できない",
                    "引用に区分の記載が無い場合は、文書冒頭の適用範囲（連結/単体）を確認しnoteに書く")


PERIOD_TOKEN_RE = re.compile(r"\d{2,4}年\d{1,2}月期|FY\s?\d{2,4}|第[1-4１-４]四半期")
SUMMARY_ACK_RE = re.compile(r"要約表|ファクトシート|ハイライト|5期推移|組替|遡及修正|統合報告書")


def check_granularity(res, loc, ev, quote):
    """複数期の数値が並ぶ引用（＝要約表由来の疑い）で、confidenceが高いままかを見る。

    evidence.mdの運用ルール（要約表からの引用はconfidenceを1段下げ、noteに明記）が
    実際に守られているかは、これまで検証されていなかった。
    """
    periods = set(PERIOD_TOKEN_RE.findall(quote))
    if len(periods) < 2:
        return  # 単一期の引用は対象外
    note = ev.get("note", "")
    if substantive_ack(note, SUMMARY_ACK_RE):
        return  # 要約表であることを実質的に認識し、対応済み
    if ev.get("confidence") == "高":
        res.add("A21", "WARN", loc,
                f"複数期({len(periods)}期分)が並ぶ引用でconfidenceが高いまま",
                "複数期の比較表（要約表・ファクトシート等）から取った場合、"
                "会計基準変更や遡及修正で過去値が原資料と食い違うことがある。"
                f"原資料で裏を取ったか、noteに要約表由来である旨を{SUBSTANTIVE_MIN_LEN}字以上で"
                "明記してconfidenceを1段下げる")


def check_close_price(res, loc, ev, src, bdt, text, note):
    """株価系の証拠が終値ベースかを検証する。

    ザラ場値・PTS・リアルタイム値は日中に動くため、後から再現できない。
    調査の再現性を担保するには終値に固定する必要がある。
    """
    if not PRICE_WORD.search(text):
        return
    if re.search(r"リアルタイム|ザラ場|ザラバ|PTS|気配|現在値", note):
        res.add("A13", "FAIL", loc,
                "終値以外の値（リアルタイム・ザラ場・PTS・気配）は採用しない",
                "場中なら前営業日の終値を使う")
        return
    if not re.search(r"終値", note + text):
        res.add("A13", "FAIL", loc,
                "株価は終値ベースであること（ザラ場値・PTS・リアルタイム値は不可）",
                "noteに『終値』と、当日引け後か前営業日かを明記する")
        return

    m = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})\s*([+-]\d{2}:\d{2})?", bdt)
    if not m:
        return
    y, mo, d, hh, mi = (int(m.group(i)) for i in range(1, 6))
    offset = m.group(6) or "+09:00"
    venue, ch, cm = CLOSE_BY_OFFSET.get(offset, (None, None, None))
    if venue and (hh, mi) < (ch, cm):
        res.add("A13", "FAIL", loc,
                f"basis_datetimeが{venue}の引け({ch}:{cm:02d})より前で、終値になり得ない",
                f"basis_datetime={bdt}。場中なら前営業日の終値を使う")

    try:
        from datetime import date
        dt = date(y, mo, d)
    except ValueError:
        return
    if dt.weekday() >= 5:
        res.add("A14", "WARN", loc,
                "basis_datetimeが土日。前営業日の終値か確認すること", bdt)

    ret = str(src.get("retrieved_at", ""))
    if ret and ret[:10] and ret[:10] < bdt[:10]:
        res.add("A13", "FAIL", loc,
                "取得日より後の日付の終値になっている（存在し得ない）",
                f"retrieved_at={ret[:10]} / basis={bdt[:10]}")


def run(case_dir: str) -> CheckResult:
    res = CheckResult("チェックA: ソース⇔台帳")
    sources, source_list = load_sources(case_dir)
    rows = load_ledger(case_dir)
    if not rows:
        res.add("A00", "FAIL", "ledger.jsonl", "台帳が空、または存在しない")
        return res

    seen_eids = set()
    used_sources = set()
    text_cache = {}
    today = datetime.now()

    # A00b: capture_source.py が検出した改竄フラグを、ここで初めて強制する。
    # 従来はターミナルへの[ALERT]表示のみで、ゲートは素通りしていた。
    for src in source_list:
        sid = src.get("source_id", "?")
        if src.get("raw_sha256_previous"):
            res.add("A22", "FAIL", sid,
                    "原本ファイルが登録後に差し替えられている（--forceで承認済み）",
                    "意図した更新なら checks/exceptions.md に理由を記録し、"
                    "sources.jsonから raw_sha256_previous を削除して解消する")
        if src.get("text_sha256_tampered"):
            res.add("A22", "FAIL", sid,
                    "raw_textが登録後に手動編集されている",
                    "capture_source.py --force で再抽出するか、編集が正当なら "
                    "checks/exceptions.md に記録して text_sha256_tampered を解消する")

    for lineno, ev in rows:
        loc = f"ledger.jsonl:L{lineno}"
        if "__parse_error__" in ev:
            res.add("A07", "FAIL", loc, "JSON解析エラー", ev["__parse_error__"])
            continue
        eid = ev.get("eid", "(no-eid)")
        loc = f"{eid}"

        missing = [k for k in REQUIRED if not ev.get(k)]
        if missing:
            res.add("A07", "FAIL", loc, "必須フィールド欠落", ",".join(missing))
        if eid in seen_eids:
            res.add("A07", "FAIL", loc, "E-IDが重複している")
        seen_eids.add(eid)
        if ev.get("claim_type") not in CLAIM_TYPES:
            res.add("A07", "FAIL", loc, "claim_typeが不正",
                    str(ev.get("claim_type")))

        sid = ev.get("source_id")
        src = sources.get(sid)
        if not src:
            res.add("A04", "FAIL", loc, "source_idがsources.jsonに存在しない", str(sid))
            continue
        used_sources.add(sid)

        rt_path = case_path(case_dir, "raw_text", f"{sid}.txt")
        if sid not in text_cache:
            text_cache[sid] = read_text(rt_path, default="")
        raw = text_cache[sid]
        if not raw:
            res.add("A04", "FAIL", loc, "raw_textが存在しない（原文未保存）", rt_path)
            continue

        recorded = src.get("text_sha256")
        if recorded and recorded != sha256_text(raw):
            res.add("A05", "FAIL", loc,
                    "抽出テキストのSHA256が記録と不一致（原文が差し替わっている）", sid)

        # A01/A02/A03: 識別語(anchor)から原文中の範囲を解決し、実在を確認する。
        # 台帳には原文を転記せず、開始・終了の目印だけを記録する設計のため、
        # ここで原文から実際の引用文を読み出す（転記ミスの経路自体を無くす）。
        head = ev.get("anchor_head", "")
        tail = ev.get("anchor_tail", "")
        quote = ""
        resolved_offsets = None
        if not head or not tail:
            res.add("A07", "FAIL", loc,
                    "anchor_head / anchor_tail が未設定（証拠の位置を特定できない）")
        else:
            if len(head) > ANCHOR_MAX_LEN or len(tail) > ANCHOR_MAX_LEN:
                res.add("A01", "FAIL", loc,
                        f"識別語が長すぎる（各{ANCHOR_MAX_LEN}字以内）。"
                        "識別語は位置の索引であり、原文の再現ではない",
                        f"head={len(head)}字 tail={len(tail)}字")
            status, fs, fe, text = resolve_anchor(raw, head, tail, ev.get("char_start"))
            if status == "no_head":
                res.add("A01", "FAIL", loc,
                        "anchor_headが原文に存在しない（記憶からの記述の可能性）", head[:30])
            elif status == "no_tail":
                res.add("A01", "FAIL", loc,
                        "anchor_headの後にanchor_tailが見つからない（範囲を特定できない）",
                        f"head={head[:20]} tail={tail[:20]}")
            elif status == "ambiguous":
                res.add("A02", "WARN", loc,
                        "識別語が複数箇所に一致し範囲を一意に決められない。"
                        "char_startを指定するか、より特徴的な識別語を選ぶ", head[:30])
            else:
                quote = text
                resolved_offsets = (fs, fe)
                cs, ce = ev.get("char_start"), ev.get("char_end")
                if cs is not None and ce is not None and (cs, ce) != (fs, fe):
                    res.add("A03", "FAIL", loc,
                            "記録された位置と識別語から解決した位置が一致しない",
                            f"記録={cs}:{ce} 解決={fs}:{fe}")

        # A08: value.number が引用内に見当たらない
        val = ev.get("value")
        if isinstance(val, dict) and val.get("number") is not None and quote:
            hay = norm(quote)
            if not any(norm(v) in hay for v in number_variants(val["number"])):
                res.add("A08", "FAIL", loc,
                        "value.numberに相当する数字が引用内に無い",
                        f"number={val['number']} quote={quote[:30]}")

        # A15/A16: 単位と期は引用で裏付けられているか
        if isinstance(val, dict) and quote:
            hay_q = norm(quote)
            note = ev.get("note", "")
            unit = str(val.get("unit", "") or "")
            if unit and unit not in {"倍", "%", "％"}:
                # 単位は表のヘッダに一度だけ書かれ、各行には無いのが開示文書の通例
                # （例:「（単位：百万円）」）。引用文字列だけを見ると正しい引用まで
                # FAILになるため、原文中の引用位置より手前も探索範囲に含める。
                unit_found = norm(unit) in hay_q
                if not unit_found and resolved_offsets and resolved_offsets[0] is not None:
                    header_zone = raw[max(0, resolved_offsets[0] - 1500):resolved_offsets[0]]
                    unit_found = norm(unit) in norm(header_zone)
                if not unit_found and not substantive_ack(
                        note, re.compile(r"換算|単位|割戻")):
                    res.add("A15", "FAIL", loc,
                            f"value.unit『{unit}』が引用にも原文の直前1500字にも無い",
                            "単位の取り違えは桁違いの誤りを生む。"
                            f"換算した場合はnoteに根拠を{SUBSTANTIVE_MIN_LEN}字以上で明記")
            period = str(val.get("period", "") or "")
            if period:
                check_period(res, loc, period, quote, note, ev, src)

        check_source_fit(res, loc, ev, src)
        check_quote_context(res, loc, ev, raw, resolved_offsets, quote)
        check_premise_zone(res, loc, ev, raw, resolved_offsets)
        check_scope_consistency(res, loc, ev, quote, raw, resolved_offsets)
        check_granularity(res, loc, ev, quote)

        tier = str(src.get("source_class", "")).upper()
        if tier in LOW_TIERS and ev.get("confidence") == "高":
            res.add("A09", "WARN", loc, f"{tier}ソースだがconfidence:高", sid)
        if tier == "T6" and ev.get("confidence") != "低":
            res.add("A09", "WARN", loc, "T6ソースはconfidence:低固定", sid)

        bd = str(ev.get("basis_date", ""))
        m = re.match(r"(\d{4})-(\d{2})", bd)
        if m:
            months = (today.year - int(m.group(1))) * 12 + (today.month - int(m.group(2)))
            if months >= 18:
                res.add("A10", "WARN", loc, f"基準日が{months}ヶ月前（陳腐化の懸念）", bd)
        elif ev.get("basis_date"):
            res.add("A07", "WARN", loc, "basis_dateがYYYY-MM-DD形式でない", bd)

        # A11/A12: 市場データ（株価・株価指標）の時点整合
        tags = ev.get("tags", []) or []
        if any("株価指標" in t for t in tags) or str(src.get("source_class", "")).upper() == "T4":
            bdt = str(ev.get("basis_datetime", ""))
            if not re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", bdt):
                res.add("A11", "FAIL", loc,
                        "株価・株価指標の証拠には basis_datetime（時刻まで）が必要",
                        "ザラ場値と終値は別物であり、日付だけでは時点が特定できない")
            text = f"{ev.get('fact','')} {ev.get('quote','')}"
            note = ev.get("note", "")
            if re.search(r"PER|PBR|PSR|EV/EBITDA|利回り|EPS|BPS", text):
                if not re.search(r"コンセンサス|実績", note):
                    if "会社予想" in note:
                        res.add("A12", "FAIL", loc,
                                "会社予想ベースの指標は採用基準外",
                                "採用するのはコンセンサス予想と実績のみ。"
                                "会社予想しか無い場合は[調査不可]としてコンセンサスを依頼する")
                    else:
                        res.add("A12", "FAIL", loc,
                                "株価指標のnoteに基準（コンセンサス予想/実績）と対象期が無い",
                                "同じ予想PERでも会社予想とコンセンサスでは値が変わる")

            # A13/A14: 株価は終値ベース
            check_close_price(res, loc, ev, src, bdt, text, note)

        if ev.get("claim_type") == "negative" and not ev.get("fact"):
            res.add("A07", "FAIL", loc, "negative証拠は探索範囲をfactに明記すること")

    # A23〜A25: 原典再アクセス（収集直後に実施する検証台帳との整合）
    # Critical項目に紐づく証拠は、収集直後に再アクセスして原典が
    # 実在するかを確認する設計になっている（納品直前にまとめて行うと、
    # 検証できないリンクが積み上がる問題を避けるため）。
    reverify_rows = {r.get("eid"): r for r in load_reverify_log(case_dir) if r.get("eid")}
    critical_eids = set()
    for it in parse_necessity_items(case_dir):
        if it["importance"].upper().startswith("C"):
            m = re.search(r"取得済\((E-\d{4})\)", it["state"])
            if m:
                critical_eids.add(m.group(1))

    for eid in critical_eids:
        loc = eid
        rv = reverify_rows.get(eid)
        if not rv:
            res.add("A23", "FAIL", loc,
                    "Critical項目の証拠だが、原典再アクセスの記録(reverify_log.jsonl)が無い",
                    "収集直後に原典へ再アクセスし、結果を記録すること。"
                    "納品直前にまとめて行わない（検証待ちの積み上がりを防ぐため）")
            continue
        outcome = rv.get("outcome", "")
        ev = next((r for _, r in load_ledger(case_dir) if r.get("eid") == eid), None)
        note = (ev or {}).get("note", "") if ev else ""

        if outcome == "hallucination":
            res.add("A24", "FAIL", loc,
                    "原典再アクセスで『原文が原典に存在しない』と判定された証拠が"
                    "台帳に残っている", rv.get("detail", "") +
                    " / 記述を削除し、正しい出典を探し直すこと（検証台帳には記録を残す）")
        elif outcome == "context_reversed":
            if not (note and re.search(r"例外|条件", note) and len(note.strip()) >= SUBSTANTIVE_MIN_LEN):
                res.add("A25", "FAIL", loc,
                        "原典再アクセスで文脈により意味が反転すると判定されたが、"
                        "台帳のnoteに例外規定が反映されていない",
                        rv.get("detail", "") + f" / noteに例外・条件を{SUBSTANTIVE_MIN_LEN}字以上で明記")
        # outcome == "match" は正常。"unreachable" は[調査不可]側で扱うためここでは問わない

        # A26: 再アクセスが著しく遅い（収集直後の原則から外れている兆候）
        rv_at = str(rv.get("reverified_at", ""))
        src_id = (ev or {}).get("source_id") if ev else None
        collected_at = str((sources.get(src_id) or {}).get("retrieved_at", "")) if src_id else ""
        if rv_at and collected_at:
            try:
                from datetime import datetime as _dt
                d1 = _dt.fromisoformat(collected_at.replace("Z", "+00:00"))
                d2 = _dt.fromisoformat(rv_at.replace("Z", "+00:00"))
                if abs((d2 - d1).total_seconds()) > 48 * 3600:
                    res.add("A26", "WARN", loc,
                            "原典再アクセスが収集から48時間以上経ってから行われている",
                            f"収集:{collected_at} 再アクセス:{rv_at} / "
                            "収集直後に行う設計。納品直前の一括検証は避ける")
            except ValueError:
                pass

    # 逆方向: 登録したソースが使われているか
    for src in source_list:
        sid = src.get("source_id")
        if sid and sid not in used_sources and not src.get("unused_reason"):
            if src.get("needs_user_provision"):
                res.add("A06", "WARN", f"{sid}", "未提供のため証拠なし（依頼中）",
                        str(src.get("request_id", "")))
            else:
                res.add("A06", "WARN", f"{sid}",
                        "登録済みだが証拠が1件も無い（読み落としの可能性）",
                        "使わないなら unused_reason を記入")
    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    print_and_exit([run(case_dir)], "ゲートA: ソース⇔台帳", case_dir, "A")


if __name__ == "__main__":
    main()
