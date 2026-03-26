from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def _windows_program_roots() -> list[Path]:
    roots: list[Path] = []
    for key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        v = os.environ.get(key, "").strip()
        if v:
            roots.append(Path(v))
    return roots


def _windows_java_candidates() -> list[Path]:
    patterns = (
        "Eclipse Adoptium/*/bin/java.exe",
        "Java/*/bin/java.exe",
        "Microsoft/jdk-*/bin/java.exe",
        "Amazon Corretto/*/bin/java.exe",
        "Zulu/*/bin/java.exe",
    )
    found: list[Path] = []
    for root in _windows_program_roots():
        if not root.is_dir():
            continue
        for pat in patterns:
            found.extend(root.glob(pat))
    # 新しめのパスを先に試す（名前の逆順でざっくり）
    return sorted({p.resolve() for p in found if p.is_file()}, key=str, reverse=True)


def find_java_executable() -> Path | None:
    """PATH / JAVA_HOME / 一般的なインストール先から java を解決する。"""
    w = shutil.which("java")
    if w:
        return Path(w).resolve()

    jh = os.environ.get("JAVA_HOME", "").strip()
    if jh:
        for name in ("java.exe", "java"):
            p = Path(jh) / "bin" / name
            if p.is_file():
                return p.resolve()

    if sys.platform == "win32":
        for p in _windows_java_candidates():
            return p

    return None


def prepare_java_environment() -> Path | None:
    """
    GUI から起動した exe などで PATH が短い場合に、検出した Java の bin を PATH の先頭へ足す。
    opendataloader-pdf が子プロセスで java を起動するため必須になりうる。
    """
    exe = find_java_executable()
    if exe is None:
        return None
    bin_dir = str(exe.parent)
    path = os.environ.get("PATH", "")
    parts = path.split(os.pathsep) if path else []
    if bin_dir.lower() not in {x.lower() for x in parts if x}:
        os.environ["PATH"] = bin_dir + (os.pathsep + path if path else "")

    home = exe.parent.parent
    if home.is_dir() and not os.environ.get("JAVA_HOME"):
        os.environ["JAVA_HOME"] = str(home.resolve())

    return exe


def check_java() -> tuple[bool, str]:
    exe = prepare_java_environment()
    if exe is None:
        return (
            False,
            "Java が見つかりません。次のいずれかを行ってください。\n"
            "・JDK 11 以上をインストールする（例: https://adoptium.net/ ）\n"
            "・環境変数 JAVA_HOME を JDK のルートに設定する\n"
            "・java.exe が PATH に通るようにする\n"
            "※エクスプローラーから起動した exe は PATH が短くなることがあります。",
        )
    try:
        r = subprocess.run(
            [str(exe), "-version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        msg = (r.stderr or r.stdout or "").strip()
        line = msg.splitlines()[0] if msg else "Java を検出しました。"
        return True, line
    except Exception as e:
        return False, f"Java の実行確認に失敗しました: {e}"
