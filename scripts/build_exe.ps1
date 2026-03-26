#Requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv not found. See https://docs.astral.sh/uv/"
}

$stagingRoot = "dist\_pyi_staging"
$finalDir = "dist\pdf2md"
$builtDir = Join-Path $stagingRoot "pdf2md"

if (Test-Path $stagingRoot) {
    Remove-Item -LiteralPath $stagingRoot -Recurse -Force
}

uv sync --extra dev

uv run pyinstaller `
    --noconfirm `
    --clean `
    --onedir `
    --windowed `
    --name pdf2md `
    --distpath $stagingRoot `
    --workpath build `
    --collect-all customtkinter `
    --collect-all opendataloader_pdf `
    packaging_entry.py

if (-not (Test-Path (Join-Path $builtDir "pdf2md.exe"))) {
    Write-Error "Build output missing: $builtDir\pdf2md.exe"
}

if (Test-Path $finalDir) {
    try {
        Remove-Item -LiteralPath $finalDir -Recurse -Force
    } catch {
        $p = (Resolve-Path $builtDir).Path
        Write-Warning "Could not remove $finalDir (file in use?). Quit pdf2md.exe, close Explorer on that folder, then:"
        Write-Warning "  Remove-Item -Recurse -Force '$finalDir'"
        Write-Warning "  Move-Item '$builtDir' '$finalDir'"
        Write-Warning "Fresh build is here (distribute this folder as-is): $p"
        exit 0
    }
}

New-Item -ItemType Directory -Path "dist" -Force | Out-Null
Move-Item -LiteralPath $builtDir -Destination $finalDir
Remove-Item -LiteralPath $stagingRoot -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "OK: dist\pdf2md\pdf2md.exe (Java 11+ on PATH or JAVA_HOME)"
