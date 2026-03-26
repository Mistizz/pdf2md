from __future__ import annotations

from collections import defaultdict
from pathlib import Path


def discover_pdfs(root: Path) -> list[Path]:
    root = root.resolve()
    if not root.is_dir():
        return []
    out: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() == ".pdf":
            out.append(p)
    return sorted(out, key=lambda x: str(x).lower())


def stem_collision_warnings(pdfs: list[Path]) -> list[str]:
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for p in pdfs:
        by_stem[p.stem.lower()].append(p)
    warnings: list[str] = []
    for stem, paths in sorted(by_stem.items()):
        if len(paths) > 1:
            names = ", ".join(str(x) for x in paths[:5])
            more = f" … 他 {len(paths) - 5} 件" if len(paths) > 5 else ""
            warnings.append(
                f"同じファイル名（拡張子除く）が複数あります。「{stem}」: {names}{more}。"
                "出力 Markdown のファイル名が衝突すると上書きされる可能性があります。"
            )
    return warnings
