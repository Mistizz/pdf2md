"""Windows などで日本語 UI が変なフォントに落ちないよう、明示的な UI フォントを選ぶ。"""

from __future__ import annotations

import sys
import tkinter.font as tkfont

import customtkinter as ctk


def pick_ui_family() -> str:
    if sys.platform != "win32":
        return "Segoe UI"
    try:
        families = set(tkfont.families())
    except Exception:
        families = set()
    for name in ("Yu Gothic UI", "Meiryo UI", "Yu Gothic", "Meiryo", "Segoe UI", "MS Gothic"):
        if name in families:
            return name
    return "Segoe UI"


def ui_font(size: int, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=pick_ui_family(), size=size, weight=weight)


def apply_windows_dpi_awareness() -> None:
    """高 DPI でフォントが潰れる・化ける場合の緩和（Tk ウィンドウ生成前に呼ぶ）。"""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        # 2 = PROCESS_PER_MONITOR_DPI_AWARE
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            import ctypes

            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
