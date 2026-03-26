from __future__ import annotations

from pathlib import Path

import opendataloader_pdf

# Windows のコマンドライン長制限回避のための分割サイズ（必要なら調整）
_DEFAULT_CHUNK = 64


def convert_pdf_paths(
    pdf_paths: list[Path],
    output_dir: Path,
    *,
    chunk_size: int | None = None,
) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if not pdf_paths:
        return
    paths = [str(p.resolve()) for p in pdf_paths]
    size = chunk_size or _DEFAULT_CHUNK
    if len(paths) <= size:
        opendataloader_pdf.convert(
            input_path=paths,
            output_dir=str(output_dir),
            format="markdown",
            quiet=True,
        )
        return
    for i in range(0, len(paths), size):
        batch = paths[i : i + size]
        opendataloader_pdf.convert(
            input_path=batch,
            output_dir=str(output_dir),
            format="markdown",
            quiet=True,
        )
