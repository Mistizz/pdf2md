from __future__ import annotations

import queue
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from pdf2md import __version__
from pdf2md.runner import validate_and_run
from pdf2md.ui.fonts import apply_windows_dpi_awareness, ui_font


def run_app() -> None:
    apply_windows_dpi_awareness()
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = Pdf2MdApp()
    app.mainloop()


class Pdf2MdApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self._f = ui_font(13)
        self._f_small = ui_font(11)
        self._f_btn = ui_font(13)

        self._input_mode: str = "folder"
        self._input_files: list[Path] = []

        self.title(f"PDF → Markdown 一括変換 v{__version__}")
        self.geometry("760x620")
        self.minsize(640, 480)

        self._log_queue: queue.Queue[str] = queue.Queue()
        self._worker: threading.Thread | None = None
        self._job_ok: bool | None = None

        self._build()
        self.after(150, self._drain_log_queue)

    def _build(self) -> None:
        pad = {"padx": 12, "pady": 6}
        kw = {"font": self._f}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(
            self,
            text="入力（フォルダを再帰検索、または PDF を直接 1 件以上選択）",
            **kw,
        ).grid(row=0, column=0, sticky="w", **pad)
        row_in = ctk.CTkFrame(self, fg_color="transparent")
        row_in.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 4))
        row_in.grid_columnconfigure(0, weight=1)
        self.input_var = tk.StringVar()
        self.input_entry = ctk.CTkEntry(row_in, textvariable=self.input_var, font=self._f)
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        btn_in = ctk.CTkFrame(row_in, fg_color="transparent")
        btn_in.grid(row=0, column=1)
        self._btn_pdf = ctk.CTkButton(
            btn_in,
            text="PDF…",
            width=72,
            command=self._browse_pdfs,
            font=self._f_btn,
        )
        self._btn_pdf.pack(side="left", padx=(0, 6))
        self._btn_folder = ctk.CTkButton(
            btn_in,
            text="フォルダ…",
            width=88,
            command=self._browse_folder,
            font=self._f_btn,
        )
        self._btn_folder.pack(side="left")

        ctk.CTkLabel(self, text="出力フォルダ", **kw).grid(row=2, column=0, sticky="w", **pad)
        row_out = ctk.CTkFrame(self, fg_color="transparent")
        row_out.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 4))
        row_out.grid_columnconfigure(0, weight=1)
        self.output_var = tk.StringVar()
        self.output_entry = ctk.CTkEntry(row_out, textvariable=self.output_var, font=self._f)
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(
            row_out,
            text="参照…",
            width=88,
            command=self._browse_output,
            font=self._f_btn,
        ).grid(row=0, column=1)

        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkLabel(mode_frame, text="出力モード", **kw).pack(anchor="w")
        self.merge_var = tk.StringVar(value="separate")
        self._radio_separate = ctk.CTkRadioButton(
            mode_frame,
            text="PDF ごとに .md を出力",
            variable=self.merge_var,
            value="separate",
            font=self._f,
        )
        self._radio_separate.pack(anchor="w", pady=2)
        self._radio_merge = ctk.CTkRadioButton(
            mode_frame,
            text="1 つの combined.md に結合（一時ファイルは成功後に削除）",
            variable=self.merge_var,
            value="merge",
            font=self._f,
        )
        self._radio_merge.pack(anchor="w", pady=2)

        self.status_var = tk.StringVar(value="準備完了")
        ctk.CTkLabel(self, textvariable=self.status_var, **kw).grid(
            row=5, column=0, sticky="w", padx=12, pady=(4, 0)
        )

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.grid(row=6, column=0, sticky="ew", padx=12, pady=(4, 8))
        self.progress.grid_remove()
        self.progress.stop()

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(row=7, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.run_btn = ctk.CTkButton(
            btn_row,
            text="変換を実行",
            command=self._on_run,
            font=self._f_btn,
        )
        self.run_btn.pack(side="left")

        ctk.CTkLabel(self, text="ログ", **kw).grid(row=8, column=0, sticky="w", padx=12, pady=(0, 0))
        self.log_box = ctk.CTkTextbox(self, wrap="word", font=self._f)
        self.log_box.grid(row=9, column=0, sticky="nsew", padx=12, pady=(4, 12))
        self.grid_rowconfigure(9, weight=1)

        foot = ctk.CTkLabel(
            self,
            text=(
                "Java 11+ が必要です（PATH または JAVA_HOME）。"
                "処理はローカルのみ（外部 API は使用しません）。"
            ),
            text_color="gray",
            font=self._f_small,
        )
        foot.grid(row=10, column=0, sticky="w", padx=12, pady=(0, 10))

    def _browse_folder(self) -> None:
        p = filedialog.askdirectory(title="入力フォルダを選択")
        if p:
            self._input_mode = "folder"
            self._input_files = []
            self.input_var.set(p)

    def _browse_pdfs(self) -> None:
        files = filedialog.askopenfilenames(
            title="PDF を選択（Ctrl で複数選択可）",
            filetypes=[("PDF", "*.pdf"), ("すべてのファイル", "*.*")],
        )
        if files:
            self._input_mode = "files"
            self._input_files = [Path(f) for f in files]
            n = len(self._input_files)
            self.input_var.set(f"PDF {n} 件を選択")

    def _browse_output(self) -> None:
        p = filedialog.askdirectory(title="出力フォルダを選択")
        if p:
            self.output_var.set(p)

    def _set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.run_btn.configure(state=state)
        self.input_entry.configure(state=state)
        self.output_entry.configure(state=state)
        self._btn_folder.configure(state=state)
        self._btn_pdf.configure(state=state)
        self._radio_separate.configure(state=state)
        self._radio_merge.configure(state=state)
        if busy:
            self.progress.grid()
            self.progress.start()
            self.status_var.set("変換中…（完了までお待ちください）")
        else:
            self.progress.stop()
            self.progress.grid_remove()
            self.status_var.set("準備完了")

    def _append_log(self, line: str) -> None:
        self.log_box.insert("end", line + "\n")
        self.log_box.see("end")

    def _drain_log_queue(self) -> None:
        try:
            while True:
                line = self._log_queue.get_nowait()
                self._append_log(line)
        except queue.Empty:
            pass
        self.after(150, self._drain_log_queue)

    def _on_run(self) -> None:
        if self._worker and self._worker.is_alive():
            messagebox.showinfo("実行中", "すでに変換が実行されています。")
            return
        out = self.output_var.get().strip()
        if not out:
            messagebox.showerror("入力エラー", "出力フォルダを指定してください。")
            return

        merge_mode = self.merge_var.get() == "merge"
        self.log_box.delete("1.0", "end")
        self._set_busy(True)

        def work() -> None:
            def log(msg: str) -> None:
                self._log_queue.put(msg)

            ok = False
            try:
                if self._input_mode == "files":
                    if not self._input_files:
                        raise ValueError("「PDF…」でファイルを選択してください。")
                    validate_and_run(
                        Path(out),
                        input_pdfs=list(self._input_files),
                        merge_mode=merge_mode,
                        log=log,
                    )
                else:
                    inp = self.input_var.get().strip()
                    if not inp or (
                        inp.startswith("PDF ") and "件を選択" in inp
                    ):
                        raise ValueError(
                            "「フォルダ…」でフォルダを選ぶか、フォルダパスを入力してください。"
                        )
                    input_path = Path(inp)
                    if not input_path.is_dir():
                        raise FileNotFoundError(f"入力フォルダが存在しません: {input_path}")
                    validate_and_run(
                        Path(out),
                        input_dir=input_path,
                        merge_mode=merge_mode,
                        log=log,
                    )
                log("--- 正常終了 ---")
                ok = True
            except Exception as e:
                log(f"エラー: {e}")
                log(traceback.format_exc())
            finally:
                self._job_ok = ok

        self._job_ok = None
        self._worker = threading.Thread(target=work, daemon=True)
        self._worker.start()
        self.after(300, self._watch_worker)

    def _watch_worker(self) -> None:
        if self._worker and self._worker.is_alive():
            self.after(300, self._watch_worker)
            return
        self.after(80, self._finish_job)

    def _finish_job(self) -> None:
        try:
            while True:
                line = self._log_queue.get_nowait()
                self._append_log(line)
        except queue.Empty:
            pass
        self._set_busy(False)
        if self._job_ok is True:
            messagebox.showinfo("完了", "変換が完了しました。")
        elif self._job_ok is False:
            messagebox.showerror(
                "エラー",
                "変換中にエラーが発生しました。ログを確認してください。",
            )
