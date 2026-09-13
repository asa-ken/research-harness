# equity-research-harness 更新パッケージ（2026-09-10）

このzipは更新済みのスキル本体一式です（案件データ research/ は含みません）。
プラグインの配置先へ中身を上書き、またはGitHubリポジトリへコミットしてください。

## 変更点
1. SKILL.md
   - レポート出力時に「証拠台帳Excel」を毎回同時出力することを必須化。
   - レポートは版番号つきで発行する命名規則を定義（初回 v1、出力都度 +1）。
     命名: <base>_report_v{N}.md ／ <base>_evidence_ledger_v{N}.xlsx（同じNを共有）。
   - ツール表に publish_report.py を追加、export_wcheck.py の位置づけを更新。
2. scripts/publish_report.py（新規）
   - レポートを版番号つきで発行し、証拠台帳Excelを同名版で同時出力する発行エントリ。
   - 版番号は <case_dir>/outputs/ の既存 <base>_report_v*.md の最大+1。
   - ゲート対象の report.md 自体は変更しない（ゲートB刻印は無効化されない）。
   - usage: python3 scripts/publish_report.py <case_dir> [--name BASE] [--verify]
3. scripts/export_wcheck.py
   - 「引用原文(復元)」列を追加（アンカーからraw_textの該当箇所を復元して表示）。
4. scripts/check_a_source_ledger.py
   - A18の「文境界の指摘（引用が文の途中で始まる/終わる）」を既定オフ化。
     アンカーは位置索引で文の途中を指すのが通常のためノイズになっていた。
     留保・条件語の脱落検知（意味を変える切り取りの防御）は従来どおり維持。
     文境界チェックを戻したい場合は環境変数 ERH_A18_SENTENCE=1 を立てる。

## 適用方法（どちらか）
- プラグイン直接更新: このzipの中身を既存スキルフォルダへ上書きコピー。
- GitHub反映: リポジトリへ上記ファイルをコミット（SKILL.md / scripts/*.py と本CHANGES.md）。
