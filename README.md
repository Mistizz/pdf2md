# pdf2md

フォルダ内の PDF、または任意に選んだ複数 PDF をまとめて Markdown に変換するデスクトップツールです。変換エンジンは [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf)（ローカル実行）、GUI は [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) です。外部 API は使用しません。

## 必要環境

- **Python 3.10+**
- **Java 11+**（JDK または JRE。`PATH` に `java` があるか、`JAVA_HOME` が JDK ルートを指すこと）
- **Windows** を主に想定（他 OS では未検証の可能性あり）

## セットアップ

[uv](https://docs.astral.sh/uv/) を推奨します。

```bash
git clone https://github.com/Mistizz/pdf2md.git
cd pdf2md
uv sync
```

## 使い方（ソースから起動）

```bash
uv run python -m pdf2md
```

- **入力**
  - **フォルダ…**: その配下の `.pdf` を再帰的に検索します。フォルダパスを手入力しても構いません。
  - **PDF…**: 1 件または複数（Ctrl＋クリック等）を直接選びます。
- **出力フォルダ**: 変換結果の出力先です。
- **出力モード**
  - PDF ごとに `.md` を出力
  - または `combined.md` 1 ファイルに結合（成功後、作業用 `_parts` は削除）

## Windows 用 exe のビルド

開発用依存を入れたうえで PyInstaller を実行します。

```powershell
.\scripts\build_exe.ps1
```

または:

```powershell
uv sync --extra dev
uv run pyinstaller --noconfirm --clean --onedir --windowed --name pdf2md `
  --collect-all customtkinter --collect-all opendataloader_pdf packaging_entry.py
```

成果物は `dist\pdf2md\` フォルダ一式です。**フォルダごと**配布し、利用者 PC には **Java 11+**（`PATH` または `JAVA_HOME`）が必要です。

## 公開前チェック（実施済みの観点）

リポジトリを public にする前に、次を確認しました。

| 項目 | 結果 |
|------|------|
| ソース内の秘密情報（API キー、パスワード等） | `src/` 内に該当なし |
| `.gitignore` | `dist/`、`build/`、`.venv`、`pdf2md.spec`、`.cursor/` を除外 |
| 個人パスのハードコード | なし |
| `pyproject.toml` の作者メール | 未記載（汎用のまま） |

**ご自身でも確認してほしい点**

- **`git log`** の作者名・メールが公開して問題ないか（GitHub の `noreply` メール等）。
- **配布 zip** に `dist/` やローカルパス入りの設定ファイルを混ぜていないか。
- **商用・社内規程**で追加のライセンス表記や承認が必要か。

## ライセンス

- 本リポジトリの**オリジナルコード**: [MIT License](./LICENSE)
- **依存ライブラリ**: [THIRD_PARTY_LICENSES.md](./THIRD_PARTY_LICENSES.md) を参照してください。特に **opendataloader-pdf（Apache 2.0）** および **PyInstaller でビルドした成果物**の再配布条件は、各公式ライセンスに従ってください。

## 謝辞

- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) プロジェクト
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
