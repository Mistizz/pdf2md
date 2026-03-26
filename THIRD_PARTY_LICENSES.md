# サードパーティライセンス

本リポジトリの**このツール自身のソースコード**は [LICENSE](./LICENSE)（MIT）です。  
以下は **依存ライブラリ**および**ビルドツール**のライセンス概要です。正確な条文は各公式配布物を参照してください。

## 実行時依存（`pyproject.toml` の `dependencies`）

| 名称 | ライセンス（参考） | 参照 |
|------|-------------------|------|
| [opendataloader-pdf](https://pypi.org/project/opendataloader-pdf/) | **Apache License 2.0** | [GitHub / LICENSE](https://github.com/opendataloader-project/opendataloader-pdf/blob/main/LICENSE) |
| [customtkinter](https://pypi.org/project/customtkinter/) | **MIT License** | [GitHub / LICENSE](https://github.com/TomSchimansky/CustomTkinter/blob/master/LICENSE)（PyPI の Classifiers と異なる場合はリポジトリを優先） |
| [darkdetect](https://pypi.org/project/darkdetect/)（customtkinter 依存） | **MIT License** | [GitHub](https://github.com/albertosottile/darkdetect) |
| [packaging](https://pypi.org/project/packaging/)（customtkinter 依存） | **Apache-2.0** および **BSD-2-Clause**（デュアル） | [プロジェクト](https://github.com/pypa/packaging) |

### Apache License 2.0（opendataloader-pdf）について

`opendataloader-pdf` のホイールには Java ラッパー等が含まれます。**バイナリや再配布物に同パッケージを同梱する場合**は、Apache 2.0 の条件（著作権表示・ライセンス文の同梱・特許条項等）に従う必要があります。詳細は上記リンク先の全文を確認してください。

## 開発・ビルド依存（`optional-dependencies.dev`）

| 名称 | ライセンス（参考） | 参照 |
|------|-------------------|------|
| [PyInstaller](https://pypi.org/project/pyinstaller/) | **GPL-2.0-or-later** 等（ブートローダ例外・一部 Apache-2.0/MIT 領域あり） | [公式 License ドキュメント](https://pyinstaller.org/en/stable/license.html)、[COPYING.txt](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt) |

PyInstaller の**ブートローダ例外**により、PyInstaller で生成した実行ファイルの再配布については公式ドキュメントの説明が適用されます。自前で PyInstaller を改変して配布する場合は GPL 上の扱いが変わることがあるため、COPYING.txt を確認してください。

### PyInstaller が間接的に取り込むもの（例）

ビルド時に解決される依存には次のようなものがあります（必要に応じ `uv tree` や各 PyPI ページで確認）。

- [pyinstaller-hooks-contrib](https://github.com/pyinstaller/pyinstaller-hooks-contrib)（GPL-2.0-or-later 等）
- [altgraph](https://pypi.org/project/altgraph/)（MIT）
- [pefile](https://pypi.org/project/pefile/)（MIT）
- [setuptools](https://pypi.org/project/setuptools/)（MIT）
- [pywin32-ctypes](https://pypi.org/project/pywin32-ctypes/)（BSD-3-Clause）

## 標準ライブラリ・ランタイム

- **Python** は [PSF License](https://docs.python.org/3/license.html) 等（バージョンに依存）。
- **Tk / Tcl** は配布形態に応じたライセンス（PyInstaller 同梱時はバンドル構成に依存）。

## 免責

上表は便宜のための要約であり、法的助言ではありません。再配布や商用利用の前に、各ライセンス全文とご利用環境に合わせて判断してください。
