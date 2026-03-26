#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv が見つかりません。https://docs.astral.sh/uv/ を参照してください。"
}

uv sync --extra dev

uv run pyinstaller `
    --noconfirm `
    --clean `
    --onedir `
    --windowed `
    --name pdf2md `
    --collect-all customtkinter `
    --collect-all opendataloader_pdf `
    packaging_entry.py

Write-Host "出力: dist\pdf2md\pdf2md.exe（Java 11+ は別途 PATH に必要です）"
