from __future__ import annotations

from pathlib import Path


def ordered_md_pairs(pdfs: list[Path], work_dir: Path) -> list[tuple[Path, Path]]:
    """Return (source_pdf, md_path) in deterministic order; append unmatched .md files last."""
    work_dir = work_dir.resolve()
    used_md: set[Path] = set()
    pairs: list[tuple[Path, Path]] = []
    for pdf in pdfs:
        md = work_dir / f"{pdf.stem}.md"
        if md.is_file():
            pairs.append((pdf, md))
            used_md.add(md.resolve())
    for md in sorted(work_dir.glob("*.md"), key=lambda p: str(p).lower()):
        rp = md.resolve()
        if rp in used_md:
            continue
        pseudo = md.with_suffix(".pdf")
        pairs.append((pseudo, md))
    return pairs


def merge_to_combined(
    input_root: Path,
    pdfs: list[Path],
    work_dir: Path,
    output_file: Path,
) -> None:
    input_root = input_root.resolve()
    pairs = ordered_md_pairs(pdfs, work_dir)
    if not pairs:
        raise FileNotFoundError(
            f"結合用の Markdown が見つかりません: {work_dir}"
        )
    chunks: list[str] = []
    for pdf, md in pairs:
        if pdf.suffix.lower() == ".pdf":
            try:
                label = str(pdf.resolve().relative_to(input_root))
            except ValueError:
                label = pdf.name
        else:
            label = md.name
        body = md.read_text(encoding="utf-8", errors="replace").strip()
        chunks.append(f"---\n\n# 元: {label}\n\n{body}\n")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
