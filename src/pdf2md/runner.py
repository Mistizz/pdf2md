from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

from pdf2md.convert_runner import convert_pdf_paths
from pdf2md.discover import discover_pdfs, stem_collision_warnings
from pdf2md.java_check import check_java
from pdf2md.merge import merge_to_combined

LogFn = Callable[[str], None]


def _noop_log(_: str) -> None:
    pass


def validate_and_run(
    input_dir: Path,
    output_dir: Path,
    *,
    merge_mode: bool,
    log: LogFn | None = None,
) -> None:
    log = log or _noop_log
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.is_dir():
        raise FileNotFoundError(f"入力フォルダが存在しません: {input_dir}")

    ok, java_msg = check_java()
    if not ok:
        raise RuntimeError(java_msg)
    log(f"Java: {java_msg}")

    pdfs = discover_pdfs(input_dir)
    if not pdfs:
        raise ValueError("PDF が 1 件も見つかりません（再帰検索済み）。")

    for w in stem_collision_warnings(pdfs):
        log(f"警告: {w}")

    log(f"対象 PDF: {len(pdfs)} 件")

    if merge_mode:
        parts = output_dir / "_parts"
        if parts.exists():
            shutil.rmtree(parts)
        parts.mkdir(parents=True, exist_ok=True)
        log(f"変換出力（一時）: {parts}")
        convert_pdf_paths(pdfs, parts)
        combined = output_dir / "combined.md"
        merge_to_combined(input_dir, pdfs, parts, combined)
        log(f"結合完了: {combined}")
        shutil.rmtree(parts)
        log("一時フォルダ _parts を削除しました。")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        log(f"出力先: {output_dir}")
        convert_pdf_paths(pdfs, output_dir)
        log("変換が完了しました。")
