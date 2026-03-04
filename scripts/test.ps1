Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RootDir

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Error "uv is required but not installed."
}

if (-not (Test-Path ".venv")) {
  uv venv
}

. .\.venv\Scripts\Activate.ps1
uv pip install -e ".[dev]"

ruff check src tests app
pytest -q

Write-Host "All checks passed."
