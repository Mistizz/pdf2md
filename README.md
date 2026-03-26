# pdf2md

フォルダ内の PDF、または任意に選んだ複数 PDF をまとめて Markdown に変換するデスクトップツールです。変換エンジンは [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf)（ローカル実行）、GUI は [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) です。外部 API は使用しません。

## 必要環境

- **Python 3.10+**
- **Java 11+**
- **Windows** を主に想定（他 OS では未検証の可能性あり）

## JDK（Java 11 以上）のインストール

本ツールの変換処理に **JDK または JRE の 11 以上**が必要です（「Java」と表記されている場合も、実体は多くの場合 **JDK** パッケージで問題ありません）。

### Windows での例

1. **インストーラで入れる（おすすめ）**
   - [Eclipse Temurin（Adoptium）](https://adoptium.net/) から **LTS（例: 17 または 21）** の Windows 用 **JDK** をダウンロードし、インストールします。
   - または [Microsoft Build of OpenJDK](https://learn.microsoft.com/en-us/java/openjdk/download) から **11 以上**を選び、インストールします。
2. **動作確認**（新しいコマンドプロンプトまたは PowerShell で）:

   ```powershell
   java -version
   ```

   `11` 以上のバージョンが表示されれば OK です。

うまく認識されない場合は、環境変数 **`JAVA_HOME`** に JDK のインストール先（例: `C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot`）を設定してみてください。詳細は各配布元のドキュメントに従ってください。

### パッケージマネージャの例（任意）

[winget](https://learn.microsoft.com/ja-jp/windows/package-manager/winget/) が使える場合の例です（パッケージ名は環境により異なることがあります）。

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

## リリースからのダウンロード（Windows）

ビルド済みの配布物は [GitHub Releases](https://github.com/Mistizz/pdf2md/releases) から入手できます。

1. 使いたい **Release** を開き、添付されている **Windows 用 ZIP**（例: `pdf2md-0.1.0-windows.zip`）をダウンロードします。
2. ZIP を展開します。中に **`pdf2md`** フォルダが入っています。
3. **`pdf2md\pdf2md.exe`** を実行します。

**注意:** 利用 PC には **Java 11+** が必要です。入れ方は上記の **JDK（Java 11 以上）のインストール** を参照してください。`pdf2md` フォルダは **`_internal` などと一緒に**そのまま置いた状態で使ってください（exe だけを別フォルダへ移すと動かない場合があります）。

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

成果物は `dist\pdf2md\` フォルダ一式です。**フォルダごと**配布し、利用者 PC には **Java 11+** が必要です。

## ライセンス

- 本リポジトリの**オリジナルコード**: [MIT License](./LICENSE)
- **依存ライブラリ**: [THIRD_PARTY_LICENSES.md](./THIRD_PARTY_LICENSES.md) を参照してください。特に **opendataloader-pdf（Apache 2.0）** および **PyInstaller でビルドした成果物**の再配布条件は、各公式ライセンスに従ってください。

## 謝辞

- [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf) プロジェクト
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
