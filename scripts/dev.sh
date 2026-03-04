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
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

MODE="${1:-all}"
if [[ $# -gt 0 ]]; then
  shift
fi
EXTRA_ARGS=("$@")

case "$MODE" in
  setup)
    echo "Environment is ready at .venv"
    ;;
  run)
    python -m dm_lab run --config configs/default.yaml "${EXTRA_ARGS[@]}"
    ;;
  ui)
    streamlit run app/Home.py --server.headless true "${EXTRA_ARGS[@]}"
    ;;
  all)
    python -m dm_lab run --config configs/default.yaml "${EXTRA_ARGS[@]}"
    streamlit run app/Home.py --server.headless true
    ;;
  *)
    echo "Usage: ./scripts/dev.sh [setup|run|ui|all] [extra args]"
    exit 1
    ;;
esac
