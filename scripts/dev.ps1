Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param(
  [ValidateSet("setup", "run", "ui", "all")]
  [string]$Mode = "all",
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$ExtraArgs
)

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

switch ($Mode) {
  "setup" {
    Write-Host "Environment is ready at .venv"
  }
  "run" {
    python -m dm_lab run --config configs/default.yaml --quick @ExtraArgs
  }
  "ui" {
    streamlit run app/Home.py @ExtraArgs
  }
  "all" {
    python -m dm_lab run --config configs/default.yaml --quick
    streamlit run app/Home.py @ExtraArgs
  }
}
