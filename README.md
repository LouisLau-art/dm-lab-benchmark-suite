# DM-Lab Benchmark Suite

[![CI](https://github.com/LouisLau-art/dm-lab-benchmark-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/LouisLau-art/dm-lab-benchmark-suite/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)

Local-first data mining benchmark project for course group work.

## Scope

- Classification
- Clustering
- Association Rule Mining
- Anomaly Detection

## Quick Start

```bash
# Preferred policy: pacman > uv > pip
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
```

## One-Command Scripts

Linux/macOS:

```bash
./scripts/dev.sh setup   # create env + install deps
./scripts/dev.sh run     # run benchmark (quick mode)
./scripts/dev.sh run --full   # run benchmark with real datasets
./scripts/dev.sh ui      # launch streamlit dashboard
./scripts/dev.sh all     # run benchmark then open dashboard
./scripts/test.sh        # ruff + pytest
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 setup
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 run
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 run --full
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 ui
powershell -ExecutionPolicy Bypass -File .\scripts\dev.ps1 all
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

Run full benchmark:

```bash
python -m dm_lab run --config configs/default.yaml
```

Run full benchmark with real datasets (non-quick mode):

```bash
python -m dm_lab run --full --config configs/default.yaml
```

Run a single task:

```bash
python -m dm_lab run --task classification --quick
```

Launch dashboard:

```bash
streamlit run app/Home.py
```

## Artifacts

Each run writes:

- `artifacts/summary.json`
- `artifacts/summary.md`
- `artifacts/metrics.csv`

## Reproducibility

- Fixed seed in `configs/default.yaml`
- Deterministic runners in `src/dm_lab/tasks/`
- CI runs lint + tests on each push/PR

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
