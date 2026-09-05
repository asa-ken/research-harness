#!/usr/bin/env python3
"""capture_source.py - 保存済み原本からテキストを抽出し、ハッシュを記録する。

このスクリプトはネットワークから取得しない。取得はClaude(web_fetch)またはユーザが行い、
raw/ に置かれた実体だけを扱う。「取得したつもり」の情報が台帳に入る経路を構造的に断つため。

usage: python3 scripts/capture_source.py <case_dir> [--force]
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness_lib import (  # noqa: E402
    case_path, read_json, write_json, read_text, sha256_text, now_iso,
)


def file_digest(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

TEXT_EXT = {".txt", ".md", ".csv", ".tsv", ".json", ".xml"}
HTML_EXT = {".html", ".htm"}


def html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</(p|div|tr|li|h[1-6]|table)>", "\n", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    import html as htmlmod
    html = htmlmod.unescape(html)
    html = re.sub(r"[ \t\u00a0]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def pdf_to_text(path: str):
    """pdfplumber → pypdf の順で試す。両方無ければ理由を返す。"""
    try:
        import pdfplumber  # type: ignore
        pages = []
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                pages.append(f"\n<<<PAGE {i}>>>\n" + (page.extract_text() or ""))
        return "".join(pages), None
    except ImportError:
        pass
    except Exception as exc:
        return None, f"pdfplumber失敗: {exc}"
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(path)
        pages = [f"\n<<<PAGE {i}>>>\n" + (p.extract_text() or "")
                 for i, p in enumerate(reader.pages, 1)]
        return "".join(pages), None
    except ImportError:
        return None, "PDF抽出ライブラリ未導入 (pip install pdfplumber)"
    except Exception as exc:
        return None, f"pypdf失敗: {exc}"


def extract(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_EXT:
        return read_text(path), None
    if ext in HTML_EXT:
        return html_to_text(read_text(path)), None
    if ext == ".pdf":
        return pdf_to_text(path)
    return None, f"未対応の拡張子 {ext}（テキスト化して再投入）"


REQUEST_HEADER = """# 情報提供依頼一覧

Claudeが到達できなかった資料です。提供いただけると調査精度が上がります。
提供不要と判断された場合は該当箇所を `[調査不可]` のまま進めます。

"""


def draft_request(src, req_id):
    return f"""### {req_id} [優先度:{src.get('priority', 'M')}] [状態:未提供]
- 欲しいもの: {src.get('title', '(タイトル未記入)')} ({src.get('source_id')})
- なぜ必要: {src.get('intended_use', '(用途未記入 - 記入すること)')}
- 無い場合の影響: (記入すること)
- 代替案: (記入すること)
- 提供方法: PDFをチャットに添付、またはテキスト貼り付け
- 障壁コード: {src.get('barrier_code', 'FETCH_FAIL')}
- 参考URL: {src.get('url_or_path', '')}

"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    case_dir = sys.argv[1]
    force = "--force" in sys.argv

    raw_text_dir = case_path(case_dir, "raw_text")
    os.makedirs(raw_text_dir, exist_ok=True)
    os.makedirs(case_path(case_dir, "requests"), exist_ok=True)

    sources = read_json(case_path(case_dir, "sources.json"), default=[])
    if isinstance(sources, dict):
        sources = sources.get("sources", [])
    if not sources:
        print("sources.json が空です。ソース登録から始めてください。")
        sys.exit(2)

    req_path = case_path(case_dir, "requests", "needed_sources.md")
    req_text = read_text(req_path, default=REQUEST_HEADER)
    existing_reqs = set(re.findall(r"### (R-\d{3})", req_text))
    next_req = max([int(r.split("-")[1]) for r in existing_reqs], default=0) + 1

    ok = miss = skipped = 0
    for src in sources:
        sid = src.get("source_id")
        if not sid:
            print("[WARN] source_id の無いエントリをスキップ")
            continue
        local = src.get("local_path")
        if local and not os.path.isabs(local):
            local = case_path(case_dir, local)
        out_path = os.path.join(raw_text_dir, f"{sid}.txt")

        if not local or not os.path.exists(local):
            src["needs_user_provision"] = True
            src.setdefault("barrier_code", "FETCH_FAIL")
            if not src.get("request_id"):
                rid = f"R-{next_req:03d}"
                next_req += 1
                src["request_id"] = rid
                req_text += draft_request(src, rid)
                print(f"[REQUEST] {sid}: 原本なし → 依頼 {rid} を起票")
            miss += 1
            continue

        # 原本のハッシュは初回に確定させ、以後は上書きせず照合だけ行う。
        # 自動で取り直すと、原本を差し替えても検出できなくなる。
        raw_digest = file_digest(local)
        if src.get("raw_sha256") and src["raw_sha256"] != raw_digest:
            print(f"[ALERT] {sid}: 原本が初回登録時と異なります（差し替えの疑い）")
            src["raw_sha256_previous"] = src["raw_sha256"]
            if not force:
                print("         --force を付けて意図的な更新であることを明示してください")
                miss += 1
                continue
        src.setdefault("raw_sha256", raw_digest)
        if force:
            src["raw_sha256"] = raw_digest

        if os.path.exists(out_path) and not force:
            text = read_text(out_path)
            current = sha256_text(text)
            if src.get("text_sha256") and src["text_sha256"] != current:
                print(f"[ALERT] {sid}: raw_text が登録後に編集されています")
                src["text_sha256_tampered"] = current
            else:
                src["text_sha256"] = current
            src["char_count"] = len(text)
            skipped += 1
            print(f"[SKIP] {sid}: 抽出済み ({len(text)}字)  --force で再抽出")
            continue

        text, err = extract(local)
        if text is None:
            src["extract_error"] = err
            src["needs_user_provision"] = True
            src.setdefault("barrier_code", "LANG")
            print(f"[FAIL] {sid}: {err}")
            miss += 1
            continue
        if len(text.strip()) < 50:
            src["extract_error"] = "抽出結果が極端に短い（画像PDFの可能性）"
            src["needs_user_provision"] = True
            src.setdefault("barrier_code", "LANG")
            print(f"[FAIL] {sid}: 抽出結果が短すぎます（OCRまたはテキスト提供が必要）")
            miss += 1
            continue

        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        src["text_sha256"] = sha256_text(text)
        src["char_count"] = len(text)
        src["extracted_at"] = now_iso()
        src.pop("extract_error", None)
        src["needs_user_provision"] = False
        ok += 1
        print(f"[OK] {sid}: {len(text)}字 → raw_text/{sid}.txt")

    write_json(case_path(case_dir, "sources.json"), sources)
    with open(req_path, "w", encoding="utf-8") as fh:
        fh.write(req_text)

    print(f"\n抽出成功 {ok} / 既存 {skipped} / 要提供 {miss}")
    if miss:
        print(f"→ 依頼一覧: {req_path}（まとめてユーザに提示すること）")


if __name__ == "__main__":
    main()
