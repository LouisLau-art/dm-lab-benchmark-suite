# DM-Lab Benchmark Suite

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

Run full benchmark:

```bash
python -m dm_lab run --config configs/default.yaml
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
