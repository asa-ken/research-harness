"""harness_lib.py - 企業調査ハーネス共通ライブラリ

判定ロジックはすべてここと各チェックスクリプトに置く。
Claudeの自己申告ではなく、機械的に反証可能な形で検査することが目的。
"""
from __future__ import annotations

import json
import hashlib
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

CATEGORIES = [
    "ビジネスモデル", "財務.実績", "財務.株価指標", "財務.健全性",
    "市場環境", "競争環境", "技術", "ガバナンス", "リスク", "株主還元",
]

STATUS_TOKENS = ["非公表", "未調査", "調査不可", "推定", "未特定"]

# 必要証拠リストの項目IDへの参照。scope.mdのN-xx形式に対応。
ITEM_ID_RE = re.compile(r"N-\d{2,}")
BARRIER_CODES = ["PAYWALL", "LOGIN", "PRICED_DB", "FETCH_FAIL", "NOTFOUND", "LANG"]
TIERS = ["T1", "T2", "T3", "T4", "T5", "T6"]

EID_RE = re.compile(r"E-\d{4}")
REQ_RE = re.compile(r"R-\d{3}")
TAG_RE = re.compile(r"\[([^\[\]]*)\]")


# ---------------------------------------------------------------- findings
@dataclass
class Finding:
    code: str
    level: str          # FAIL / WARN / INFO
    where: str
    message: str
    detail: str = ""

    def line(self) -> str:
        d = f" | {self.detail}" if self.detail else ""
        return f"[{self.level}] {self.code} @ {self.where}: {self.message}{d}"


@dataclass
class CheckResult:
    name: str
    findings: list = field(default_factory=list)

    def add(self, code, level, where, message, detail=""):
        self.findings.append(Finding(code, level, where, message, detail))

    @property
    def fails(self):
        return [f for f in self.findings if f.level == "FAIL"]

    @property
    def warns(self):
        return [f for f in self.findings if f.level == "WARN"]

    @property
    def passed(self) -> bool:
        return not self.fails

    def to_markdown(self) -> str:
        out = [f"### {self.name}: {'PASS' if self.passed else 'FAIL'} "
               f"(FAIL {len(self.fails)} / WARN {len(self.warns)})", ""]
        if not self.findings:
            out.append("- 指摘なし")
        for f in self.findings:
            out.append(f"- {f.line()}")
        out.append("")
        return "\n".join(out)


# ---------------------------------------------------------------- io
def case_path(case_dir: str, *parts) -> str:
    return os.path.join(case_dir, *parts)


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def read_jsonl(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for i, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw or raw.startswith("//") or raw.startswith("#"):
                continue
            try:
                rows.append((i, json.loads(raw)))
            except json.JSONDecodeError as exc:
                rows.append((i, {"__parse_error__": str(exc), "__raw__": raw[:120]}))
    return rows


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_text(path, default=""):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def load_sources(case_dir):
    """sources.json は list でも {"sources":[...]} でも受ける。"""
    obj = read_json(case_path(case_dir, "sources.json"), default=[])
    if isinstance(obj, dict):
        obj = obj.get("sources", [])
    return {s.get("source_id"): s for s in obj if isinstance(s, dict)}, obj


def load_ledger(case_dir):
    return read_jsonl(case_path(case_dir, "ledger.jsonl"))


def load_search_log(case_dir):
    """探索ログを読む。1行=1回の探索試行。

    フィールド: item(必要証拠リストのID) / route(T1〜T6) / query(検索文字列) /
    stage(collection|reverify, 省略時collection) / timestamp / new_subjects / new_facts
    """
    rows = []
    for _, row in read_jsonl(case_path(case_dir, "search_log.jsonl")):
        if "__parse_error__" in row:
            continue
        row.setdefault("stage", "collection")
        rows.append(row)
    return rows


def load_reverify_log(case_dir):
    """検証台帳（原典再アクセスの記録）を読む。1行=1回の再アクセス試行。

    フィールド: eid / url / reverified_at / outcome(match|hallucination|
    context_reversed|unreachable) / detail
    """
    rows = []
    for _, row in read_jsonl(case_path(case_dir, "reverify_log.jsonl")):
        if "__parse_error__" in row:
            continue
        rows.append(row)
    return rows


def saturation_status(case_dir, item_id):
    """指定した必要証拠リストID(N-xx)について、飽和条件を満たしているかを判定する。

    条件（ユーザ定義）: 直近3件が経路(route)もクエリ(query)も互いに異なり、
    その3件全てで新規対象・新規事実が0件であること。これは打ち切りを許可する
    最低条件であり、それ以前に新規が出ていた事実を無視するものではない
    （直近3件だけを見るのは『最後に十分探した証拠』を要求するため）。

    返り値: (ok: bool, detail: str)
    """
    rows = [r for r in load_search_log(case_dir)
            if r.get("item") == item_id and r.get("stage", "collection") == "collection"]
    if len(rows) < 3:
        return False, f"探索ログのエントリが{len(rows)}件しかない（3件以上必要）"

    def _ts(r):
        return str(r.get("timestamp", ""))
    rows.sort(key=_ts)
    last3 = rows[-3:]

    routes = [r.get("route", "") for r in last3]
    queries = [r.get("query", "") for r in last3]
    if len(set(routes)) < 3:
        return False, f"直近3件の経路が重複している: {routes}"
    if len(set(queries)) < 3:
        return False, f"直近3件のクエリが重複している（経路を分けても同一クエリではV38の兆候）: {queries}"
    nonzero = [r for r in last3
              if int(r.get("new_subjects", 0) or 0) or int(r.get("new_facts", 0) or 0)]
    if nonzero:
        return False, f"直近3件のうち新規0件でないものがある: {nonzero}"
    return True, f"直近3件（経路:{routes} / クエリ:{len(set(queries))}種）で新規0件を確認"


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- normalize
def nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s or "")


def norm(s: str) -> str:
    """比較用の正規化。全半角統一・空白/カンマ/記号ゆれを除去。

    原文一致の判定は「表記ゆれで落ちる」と運用が止まり、
    「緩すぎる」と検査にならない。ここでは意味を変えない差だけを潰す。
    """
    s = nfkc(s)
    s = s.replace("\u3000", " ")
    s = re.sub(r"[,\s\u00a0]", "", s)
    s = s.replace("△", "-").replace("▲", "-").replace("−", "-").replace("—", "-")
    return s


NEGATION_RE = re.compile(
    r"存在しない|存在せず|見られない|認められない|ではない|ではありません|"
    r"していない|しておらず|無い|ない。|なかった|不要|皆無|生じていない")
COMPARISON_RE = re.compile(
    r"増加|減少|増収|減収|増益|減益|上回|下回|拡大|縮小|改善|悪化|伸び|落ち込|"
    r"前年比|前期比|前年同期比|YoY|QoQ|横ばい|回復|鈍化|加速")

NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")
# 単位・スケールが後続する数値は「厳格照合対象」とみなす
STRICT_SUFFIX = re.compile(
    r"^(?:%|％|兆|億|万|千|百万|十億|円|ドル|USD|JPY|株|台|件|人|社|倍|pt|bp|"
    r"ポイント|期|年|月|日|四半期|Q)")


def extract_numbers(text: str):
    """(raw, normalized_value_str, strict) のリストを返す。"""
    t = nfkc(text)
    # タグ内部（[E-0001] や [推定|...]）は照合対象外
    t = TAG_RE.sub(" ", t)
    # ISO日付・時刻はメタ情報であり数値主張ではない
    t = re.sub(r"\d{4}-\d{2}-\d{2}(?:T[\d:+\-]+)?", " ", t)
    # 識別子に付随する数字を除去
    t = re.sub(r"[ESRFHIG]-\d+", " ", t)
    t = t.replace(",", "")
    out = []
    for m in NUM_RE.finditer(t):
        raw = m.group(0)
        tail = t[m.end():m.end() + 6]
        digits = raw.lstrip("-").replace(".", "")
        strict = bool(STRICT_SUFFIX.match(tail)) or len(digits) >= 3 or "." in raw
        out.append((raw, raw, strict))
    return out


def flexible_find(raw: str, quote: str):
    """引用を原文から探す。返り値は (status, start, end)。

    PDF抽出は文中に改行を入れるため、画面上は連続した一文でも原文では分断される。
    完全一致だけを要求すると正しい引用が大量にFAILし、機構が使われなくなる。
    そこで「空白・改行だけの差」は許容し、それ以外の改変とは区別する。
      exact   : 完全一致
      spacing : 空白・改行のみが異なる（許容、位置は自動補正）
      norm    : 全角半角やカンマの差も含む（要確認）
      missing : 見つからない（記憶からの記述の疑い）
    """
    if not quote:
        return ("missing", None, None)
    idx = raw.find(quote)
    if idx >= 0:
        return ("exact", idx, idx + len(quote))
    core = re.sub(r"\s+", "", quote)
    if core:
        pattern = r"\s*".join(re.escape(ch) for ch in core)
        m = re.search(pattern, raw)
        if m:
            return ("spacing", m.start(), m.end())
    if norm(quote) and norm(quote) in norm(raw):
        return ("norm", None, None)
    return ("missing", None, None)


ANCHOR_MAX_LEN = 40


def resolve_anchor(raw: str, head: str, tail: str, hint_start=None):
    """識別語(anchor_head/tail)から原文中の範囲を解決する。

    台帳には原文を転記せず、開始・終了の短い目印だけを記録する設計。
    実際の引用文はここで原文から読み出す。返り値は (status, start, end, text)。
      ok        : 一意に解決できた
      ambiguous : headが複数箇所に一致し、hint_startでも絞れない
      no_head   : headが原文に無い
      no_tail   : headの後にtailが見つからない
    """
    if not raw or not head or not tail:
        return ("no_head", None, None, "")

    starts = []
    idx = raw.find(head)
    while idx >= 0:
        starts.append(idx)
        idx = raw.find(head, idx + 1)
        if len(starts) > 50:
            break
    if not starts:
        # 空白・改行の差を許容して再探索（PDF抽出対策）
        st, s0, s1 = flexible_find(raw, head)
        if st in ("exact", "spacing") and s0 is not None:
            starts = [s0]
        else:
            return ("no_head", None, None, "")

    if hint_start is not None and len(starts) > 1:
        starts.sort(key=lambda s: abs(s - hint_start))
        starts = starts[:1]
    elif len(starts) > 1:
        # tailが直後に見つかる候補だけに絞れば一意になることがある
        viable = []
        for s in starts:
            t = raw.find(tail, s + len(head))
            if t >= 0:
                viable.append((s, t))
        if len(viable) == 1:
            s, t = viable[0]
            return ("ok", s, t + len(tail), raw[s:t + len(tail)])
        if not viable:
            return ("no_tail", None, None, "")
        return ("ambiguous", None, None, "")

    s = starts[0]
    t = raw.find(tail, s + len(head))
    if t < 0:
        st, t0, t1 = flexible_find(raw[s:], tail)
        if st in ("exact", "spacing") and t0 is not None:
            return ("ok", s, s + t1, raw[s:s + t1])
        return ("no_tail", None, None, "")
    return ("ok", s, t + len(tail), raw[s:t + len(tail)])


def evidence_text(case_dir, ev):
    """証拠が指す原文を読み出す。台帳のquote代わりに使う。"""
    raw = read_text(case_path(case_dir, "raw_text", f"{ev.get('source_id')}.txt"))
    status, s, e, text = resolve_anchor(
        raw, ev.get("anchor_head", ""), ev.get("anchor_tail", ""),
        ev.get("char_start"))
    return text if status == "ok" else ""


def number_variants(value):
    """value.number を照合用の複数表記に展開する。"""
    variants = set()
    try:
        f = float(value)
    except (TypeError, ValueError):
        return {str(value)}
    variants.add(str(value))
    variants.add(repr(f))
    if f == int(f):
        variants.add(str(int(f)))
        variants.add(f"{int(f)}.0")
    else:
        variants.add(f"{f}")
    return {v for v in variants if v}


def haystack_for_evidence(ev: dict, case_dir=None) -> str:
    """数値照合に使う証拠側の文字列。

    原文は台帳に転記されていないため、case_dirが与えられれば識別語から読み出す。
    原文は原語・原表記のままなので、'25年3月期' のような正規化表現は
    アナリストが書く fact 側にしか存在しない。両方を対象にする。
    """
    src_text = evidence_text(case_dir, ev) if case_dir else ""
    parts = [src_text, ev.get("fact", ""), ev.get("basis_date", ""),
             ev.get("note", "")]
    v = ev.get("value")
    if isinstance(v, dict):
        parts.append(json.dumps(v, ensure_ascii=False))
        if "number" in v:
            parts.extend(number_variants(v["number"]))
    return norm(" ".join(str(p) for p in parts))


# ---------------------------------------------------------------- report parse
FENCE_RE = re.compile(r"^\s*```")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:\-\|]+\|\s*$")


def iter_report_units(text: str, source_name: str):
    """レポートを検査単位に分解する。

    - コードブロック / mermaid は除外（図の描画コードは別途データ表で検証する）
    - 見出し行は除外
    - 表は1行=1単位、本文は句点で分割

    **意図的に「検査除外ブロック」機能は持たない。** 過去に
    <!-- no-check -->〜<!-- /no-check --> という複数行除外機構があったが、
    これは任意の主張・数値をチェックから丸ごと隠せる抜け穴だった
    （B02〜B17・S01〜S12すべてが素通りする）。正当な用途として想定していた
    「証跡コメントの除外」は、単一行HTMLコメントの除外だけで十分満たせるため、
    複数行ブロックは廃止した。除外が必要になった場合は、なぜ検査対象外にすべきかを
    個別のチェックコード側で判断する（一括の抜け道を作らない）。
    """
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue  # 証跡コメント等のメタ行は主張ではない（単一行のみ）
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith(">"):
            # 引用ブロックも主張を書ける場所なので検査対象に含める
            stripped = stripped.lstrip("> ").strip()
            if not stripped:
                continue
        if TABLE_SEP_RE.match(line):
            continue
        where = f"{source_name}:L{lineno}"
        if stripped.startswith("|"):
            yield where, stripped
            continue
        for part in re.split(r"(?<=。)|(?<=\n)", stripped):
            part = part.strip()
            if part:
                yield where, part


def parse_tags(unit: str):
    """[...] タグを抽出して種別ごとに分類する。"""
    tags = {"eids": [], "calc": [], "infer": [], "status": [], "raw": []}
    for m in TAG_RE.finditer(unit):
        # 表セル内では | が \| とエスケープされるため戻す
        body = m.group(1).strip().replace("\\|", "|")
        tags["raw"].append(body)
        if body.startswith("計算"):
            tags["calc"].append(body)
        elif body.startswith("推定"):
            tags["infer"].append(body)
        elif any(body.startswith(s) for s in STATUS_TOKENS):
            tags["status"].append(body)
        for eid in EID_RE.findall(body):
            tags["eids"].append(eid)
    return tags

def exception_eids(case_dir):
    """checks/exceptions.md に理由付きで記録されたE-IDの集合を返す。

    A28/A29（レポート採用証拠の遡及再アクセス要求）の個別解除に使う。
    単にE-IDを並べるだけの空解除を防ぐため、E-IDと同じ行に実質的な理由
    （10字以上の記述）がある行だけを有効な解除とみなす。
    """
    text = read_text(case_path(case_dir, "checks", "exceptions.md")) or ""
    exempted = set()
    for line in text.splitlines():
        eids = EID_RE.findall(line)
        if not eids:
            continue
        # E-ID表記を除いた残りを理由とみなし、実質的な長さがあるかを見る
        reason = EID_RE.sub("", line).strip(" \t|-—:：、,")
        if len(reason) >= 10:
            exempted.update(eids)
    return exempted


def referenced_eids(report_text: str, fig_texts=None):
    """レポート本文と図表の根拠欄で実際に引用されているE-IDの集合を返す。

    「結論に使われた証拠」の機械的な定義。check_b の孤立証拠判定(B07)と、
    check_a の遡及再アクセス要求(A28/A29)が同じ定義を共有するために切り出した。

    - 本文: iter_report_units で検査単位に分解し、[...] タグ内のE-IDを拾う
      （地の文にE-IDを裸で書いても parse_tags は拾わないが、無出典の数値は
       別途 B02/B03 がFAILさせるため、引用を外す逃げ道は塞がれている）
    - 図表: データ表の根拠欄などにE-IDが直接書かれるため、テキスト全体から
      EID_RE で拾う

    fig_texts は figures/*.md の内容のリスト（省略可）。
    """
    refs = set()
    for _where, unit in iter_report_units(report_text, "report.md"):
        for eid in parse_tags(unit)["eids"]:
            refs.add(eid)
    for ft in (fig_texts or []):
        for eid in EID_RE.findall(ft):
            refs.add(eid)
    return refs


def safe_eval_arith(expr: str):
    """四則演算のみを評価する。任意コード実行を避けるためASTで検証する。"""
    import ast
    allowed = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
               ast.USub, ast.UAdd, ast.Mod)
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            return None
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            return None
    try:
        return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, {})
    except Exception:
        return None


def render_findings(results, title, case_dir, gate_label):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    body = [f"# {title}", "", f"- case: `{case_dir}`", f"- 実行: {now_iso()}", ""]
    total_fail = sum(len(r.fails) for r in results)
    total_warn = sum(len(r.warns) for r in results)
    body.append(f"## 判定: **{'PASS' if total_fail == 0 else 'FAIL'}** "
                f"(FAIL {total_fail} / WARN {total_warn})")
    body.append("")
    for r in results:
        body.append(r.to_markdown())
    md = "\n".join(body)
    outdir = case_path(case_dir, "checks")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"gate_{gate_label}_{ts}.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(md)
    return path, total_fail, total_warn


RECEIPT_LINE_RE = re.compile(r"^\s*<!--\s*gate:\w+\s+\w+\s+receipt=[0-9a-f]+\s*-->\s*$",
                             re.MULTILINE)


def file_sha(path):
    """ファイルのハッシュ。証跡コメント行は除外して計算する。

    証跡をレポートに書き込むとハッシュが変わる、という自己矛盾を避けるため。
    除外するのは証跡行そのものだけなので、本文の改変は従来どおり検出できる。
    """
    if not os.path.exists(path):
        return None
    text = RECEIPT_LINE_RE.sub("", read_text(path))
    return sha256_text(text)


def figures_sha(case_dir):
    """figures/*.md をまとめて1つのハッシュにする。

    以前は report.md / ledger.jsonl / sources.json しか証跡に含めておらず、
    ゲート通過後に図のデータを書き換えても検出できなかった。
    """
    import glob as _glob
    paths = sorted(_glob.glob(case_path(case_dir, "figures", "*.md")))
    if not paths:
        return None
    combined = "\x00".join(f"{os.path.basename(p)}:{read_text(p)}" for p in paths)
    return sha256_text(combined)


def write_receipt(case_dir, gate_label, verdict, fails, warns):
    """ゲートを実際に実行した証跡を残す。

    「PASSしました」という自己申告と、実際に走らせた結果を区別できるようにする。
    対象ファイルのハッシュを含めるため、ゲート後にレポートを書き換えれば検出できる。
    """
    targets = {
        "report.md": file_sha(case_path(case_dir, "report.md")),
        "ledger.jsonl": file_sha(case_path(case_dir, "ledger.jsonl")),
        "sources.json": file_sha(case_path(case_dir, "sources.json")),
        "figures/": figures_sha(case_dir),
    }
    receipt = {"gate": gate_label, "verdict": verdict, "executed_at": now_iso(),
               "fails": fails, "warns": warns, "files": targets}
    body = json.dumps(receipt, ensure_ascii=False, sort_keys=True)
    receipt["receipt_id"] = sha256_text(body)[:16]
    write_json(case_path(case_dir, "checks", f"receipt_{gate_label}.json"), receipt)
    return receipt


def print_and_exit(results, title, case_dir, gate_label):
    path, fails, warns = render_findings(results, title, case_dir, gate_label)
    for r in results:
        print(r.to_markdown())
    verdict = "PASS" if fails == 0 else "FAIL"
    receipt = write_receipt(case_dir, gate_label, verdict, fails, warns)
    print(f"→ レポート: {path}")
    print(f"→ 判定: {verdict} (FAIL {fails} / WARN {warns})")
    print(f"→ 実行証跡: receipt_{gate_label}.json  id={receipt['receipt_id']}")
    if verdict == "PASS":
        print(f"   レポート冒頭に記載する行: "
              f"<!-- gate:{gate_label} {verdict} receipt={receipt['receipt_id']} -->")
    sys.exit(0 if fails == 0 else 1)
