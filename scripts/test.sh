#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required but not installed."
  echo "Install it first, then rerun this script."
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  uv venv
fi

# shellcheck source=/dev/null
source .venv/bin/activate
uv pip install -e .[dev]

ruff check src tests app
pytest -q

echo "All checks passed."
