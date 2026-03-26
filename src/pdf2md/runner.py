from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable

from pdf2md.convert_runner import convert_pdf_paths
from pdf2md.discover import (
    discover_pdfs,
    normalize_pdf_paths,
    stem_collision_warnings,
)
from pdf2md.java_check import check_java
from pdf2md.merge import merge_to_combined

LogFn = Callable[[str], None]


def _noop_log(_: str) -> None:
    pass


def _merge_input_root_for_explicit_pdfs(pdfs: list[Path]) -> Path:
    """結合時の # 元: 相対パス用。共通祖先が取れなければ先頭ファイルの親へ。"""
    if not pdfs:
        return Path.cwd()
    resolved = [p.resolve() for p in pdfs]
    try:
        common = os.path.commonpath([str(p) for p in resolved])
        return Path(common)
    except ValueError:
        return resolved[0].parent


def validate_and_run(
    output_dir: Path,
    *,
    input_dir: Path | None = None,
    input_pdfs: list[Path] | None = None,
    merge_mode: bool = False,
    log: LogFn | None = None,
) -> None:
    log = log or _noop_log
    output_dir = Path(output_dir)

    has_dir = input_dir is not None
    has_files = input_pdfs is not None and len(input_pdfs) > 0
    if has_dir == has_files:
        raise ValueError(
            "入力は「フォルダ（input_dir）」または「PDF リスト（input_pdfs）」のどちらか一方だけ指定してください。"
        )

    ok, java_msg = check_java()
    if not ok:
        raise RuntimeError(java_msg)
    log(f"Java: {java_msg}")

    merge_root: Path
    if input_dir is not None:
        input_dir = Path(input_dir)
        if not input_dir.is_dir():
            raise FileNotFoundError(f"入力フォルダが存在しません: {input_dir}")
        pdfs = discover_pdfs(input_dir)
        merge_root = input_dir.resolve()
        if not pdfs:
            raise ValueError("PDF が 1 件も見つかりません（再帰検索済み）。")
    else:
        pdfs = normalize_pdf_paths(list(input_pdfs or []))
        merge_root = _merge_input_root_for_explicit_pdfs(pdfs)
        if not pdfs:
            raise ValueError("有効な PDF ファイルがありません。")

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
        merge_to_combined(merge_root, pdfs, parts, combined)
        log(f"結合完了: {combined}")
        shutil.rmtree(parts)
        log("一時フォルダ _parts を削除しました。")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        log(f"出力先: {output_dir}")
        convert_pdf_paths(pdfs, output_dir)
        log("変換が完了しました。")
