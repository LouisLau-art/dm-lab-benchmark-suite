# DM-Lab Benchmark Suite Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local-first, reproducible data mining benchmark project with four tasks (classification, clustering, association, anomaly), auto-reporting, and a lightweight Streamlit result UI.

**Architecture:** Single Python repo with modular pipelines in `src/dm_lab`, config-driven runs from `configs/*.yaml`, generated artifacts in `artifacts/`, and a read-only Streamlit app in `app/` for presentation. Keep infra minimal and prioritize reproducibility and grading-oriented evaluation.

**Tech Stack:** Python 3.12+, pandas, numpy, scikit-learn, mlxtend, imbalanced-learn, matplotlib, seaborn, streamlit, pyyaml, pytest, ruff.

---

### Task 1: Bootstrap Project and CLI Skeleton

**Files:**
- Create: `/root/data-mining/pyproject.toml`
- Create: `/root/data-mining/src/dm_lab/__init__.py`
- Create: `/root/data-mining/src/dm_lab/cli.py`
- Create: `/root/data-mining/src/dm_lab/__main__.py`
- Create: `/root/data-mining/tests/test_cli_smoke.py`
- Create: `/root/data-mining/.gitignore`

**Step 1: Write the failing test**

```python
# tests/test_cli_smoke.py
from dm_lab.cli import build_parser

def test_cli_has_run_command():
    parser = build_parser()
    subcommands = parser._subparsers._group_actions[0].choices
    assert "run" in subcommands
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli_smoke.py -v`  
Expected: FAIL with import/module error.

**Step 3: Write minimal implementation**

```python
# src/dm_lab/cli.py
import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dm-lab")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("run")
    return parser
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli_smoke.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add pyproject.toml src/dm_lab tests/test_cli_smoke.py .gitignore
git commit -m "chore: bootstrap dm-lab package and CLI skeleton"
```

### Task 2: Config Loader and Validation

**Files:**
- Create: `/root/data-mining/configs/default.yaml`
- Create: `/root/data-mining/src/dm_lab/config.py`
- Create: `/root/data-mining/tests/test_config.py`

**Step 1: Write the failing test**

```python
from dm_lab.config import load_config

def test_load_config_reads_seed():
    cfg = load_config("configs/default.yaml")
    assert cfg["seed"] == 42
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`  
Expected: FAIL with `ModuleNotFoundError` or missing function.

**Step 3: Write minimal implementation**

```python
# src/dm_lab/config.py
import yaml

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if "seed" not in cfg:
        raise ValueError("seed is required")
    return cfg
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add configs/default.yaml src/dm_lab/config.py tests/test_config.py
git commit -m "feat: add config loader with seed validation"
```

### Task 3: Dataset Registry and Local Caching

**Files:**
- Create: `/root/data-mining/src/dm_lab/data/registry.py`
- Create: `/root/data-mining/src/dm_lab/data/io.py`
- Create: `/root/data-mining/tests/test_data_registry.py`
- Create: `/root/data-mining/data/.gitkeep`

**Step 1: Write the failing test**

```python
from dm_lab.data.registry import get_dataset_spec

def test_registry_contains_classification_dataset():
    spec = get_dataset_spec("classification")
    assert "name" in spec and "url" in spec
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_registry.py -v`  
Expected: FAIL because module/function does not exist.

**Step 3: Write minimal implementation**

```python
# src/dm_lab/data/registry.py
DATASET_REGISTRY = {
    "classification": {"name": "adult_income", "url": "https://..."},
    "clustering": {"name": "wholesale_customers", "url": "https://..."},
    "association": {"name": "online_retail", "url": "https://..."},
    "anomaly": {"name": "credit_card_fraud", "url": "https://..."},
}

def get_dataset_spec(task: str) -> dict:
    return DATASET_REGISTRY[task]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_registry.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/data tests/test_data_registry.py data/.gitkeep
git commit -m "feat: add dataset registry and cache skeleton"
```

### Task 4: Classification Pipeline

**Files:**
- Create: `/root/data-mining/src/dm_lab/tasks/classification.py`
- Create: `/root/data-mining/tests/test_classification.py`

**Step 1: Write the failing test**

```python
from dm_lab.tasks.classification import run_classification

def test_classification_returns_metrics_dict():
    result = run_classification(random_state=42)
    assert {"f1", "roc_auc", "precision", "recall"} <= set(result.keys())
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_classification.py -v`  
Expected: FAIL because function is missing.

**Step 3: Write minimal implementation**

```python
def run_classification(random_state: int = 42) -> dict:
    # Use sklearn built-in dataset for deterministic smoke pipeline.
    return {"f1": 0.0, "roc_auc": 0.0, "precision": 0.0, "recall": 0.0}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_classification.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/tasks/classification.py tests/test_classification.py
git commit -m "feat: add classification pipeline contract"
```

### Task 5: Clustering Pipeline

**Files:**
- Create: `/root/data-mining/src/dm_lab/tasks/clustering.py`
- Create: `/root/data-mining/tests/test_clustering.py`

**Step 1: Write the failing test**

```python
from dm_lab.tasks.clustering import run_clustering

def test_clustering_returns_quality_metrics():
    result = run_clustering(random_state=42)
    assert {"silhouette", "davies_bouldin"} <= set(result.keys())
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_clustering.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def run_clustering(random_state: int = 42) -> dict:
    return {"silhouette": 0.0, "davies_bouldin": 0.0}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_clustering.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/tasks/clustering.py tests/test_clustering.py
git commit -m "feat: add clustering pipeline contract"
```

### Task 6: Association Rule Pipeline

**Files:**
- Create: `/root/data-mining/src/dm_lab/tasks/association.py`
- Create: `/root/data-mining/tests/test_association.py`

**Step 1: Write the failing test**

```python
from dm_lab.tasks.association import run_association

def test_association_returns_rule_metrics():
    result = run_association()
    assert {"support", "confidence", "lift"} <= set(result.keys())
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_association.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def run_association() -> dict:
    return {"support": 0.0, "confidence": 0.0, "lift": 0.0}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_association.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/tasks/association.py tests/test_association.py
git commit -m "feat: add association pipeline contract"
```

### Task 7: Anomaly Detection Pipeline

**Files:**
- Create: `/root/data-mining/src/dm_lab/tasks/anomaly.py`
- Create: `/root/data-mining/tests/test_anomaly.py`

**Step 1: Write the failing test**

```python
from dm_lab.tasks.anomaly import run_anomaly

def test_anomaly_returns_core_metrics():
    result = run_anomaly(random_state=42)
    assert {"pr_auc", "f1", "recall_at_k"} <= set(result.keys())
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_anomaly.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def run_anomaly(random_state: int = 42) -> dict:
    return {"pr_auc": 0.0, "f1": 0.0, "recall_at_k": 0.0}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_anomaly.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/tasks/anomaly.py tests/test_anomaly.py
git commit -m "feat: add anomaly pipeline contract"
```

### Task 8: Unified Runner and Artifact Writer

**Files:**
- Create: `/root/data-mining/src/dm_lab/pipeline.py`
- Create: `/root/data-mining/src/dm_lab/report/io.py`
- Create: `/root/data-mining/tests/test_pipeline_smoke.py`

**Step 1: Write the failing test**

```python
from dm_lab.pipeline import run_all_tasks

def test_run_all_tasks_returns_four_sections(tmp_path):
    result = run_all_tasks(output_dir=tmp_path, seed=42)
    assert {"classification", "clustering", "association", "anomaly"} <= set(result.keys())
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_pipeline_smoke.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def run_all_tasks(output_dir, seed: int) -> dict:
    return {
        "classification": {},
        "clustering": {},
        "association": {},
        "anomaly": {},
    }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_pipeline_smoke.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/pipeline.py src/dm_lab/report/io.py tests/test_pipeline_smoke.py
git commit -m "feat: add unified runner and artifact contract"
```

### Task 9: CLI `run` Command Integration

**Files:**
- Modify: `/root/data-mining/src/dm_lab/cli.py`
- Create: `/root/data-mining/tests/test_cli_run.py`

**Step 1: Write the failing test**

```python
from dm_lab.cli import main

def test_cli_run_returns_zero_exit_code(tmp_path):
    code = main(["run", "--output-dir", str(tmp_path), "--config", "configs/default.yaml"])
    assert code == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli_run.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        return 0
    return 1
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli_run.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/cli.py tests/test_cli_run.py
git commit -m "feat: wire CLI run command"
```

### Task 10: Streamlit Result Dashboard (Read-Only)

**Files:**
- Create: `/root/data-mining/app/Home.py`
- Create: `/root/data-mining/tests/test_dashboard_import.py`

**Step 1: Write the failing test**

```python
def test_streamlit_home_module_imports():
    import importlib
    mod = importlib.import_module("app.Home")
    assert mod is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_dashboard_import.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
# app/Home.py
import streamlit as st

st.title("DM-Lab Benchmark Suite")
st.write("Result dashboard (read-only).")
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_dashboard_import.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add app/Home.py tests/test_dashboard_import.py
git commit -m "feat: add lightweight streamlit dashboard"
```

### Task 11: Reproducibility and Smoke E2E Test

**Files:**
- Create: `/root/data-mining/tests/test_reproducibility.py`
- Modify: `/root/data-mining/src/dm_lab/pipeline.py`

**Step 1: Write the failing test**

```python
from dm_lab.pipeline import run_all_tasks

def test_same_seed_produces_same_summary(tmp_path):
    a = run_all_tasks(output_dir=tmp_path / "a", seed=42)
    b = run_all_tasks(output_dir=tmp_path / "b", seed=42)
    assert a == b
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_reproducibility.py -v`  
Expected: FAIL due to non-deterministic or missing implementation.

**Step 3: Write minimal implementation**

```python
# Ensure task functions accept/use seed and deterministic paths.
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_reproducibility.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/dm_lab/pipeline.py tests/test_reproducibility.py
git commit -m "test: enforce reproducibility with fixed seed"
```

### Task 12: CI Workflow and Quality Gate

**Files:**
- Create: `/root/data-mining/.github/workflows/ci.yml`
- Create: `/root/data-mining/README.md`

**Step 1: Write the failing test/check**

Run: `ruff check src tests`  
Expected: FAIL until workflow/tooling is configured.

**Step 2: Run test to verify it fails**

Run: `pytest -q`  
Expected: FAIL if previous wiring incomplete.

**Step 3: Write minimal implementation**

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e .[dev]
      - run: ruff check src tests
      - run: pytest -q
```

**Step 4: Run test to verify it passes**

Run: `ruff check src tests && pytest -q`  
Expected: PASS.

**Step 5: Commit**

```bash
git add .github/workflows/ci.yml README.md
git commit -m "ci: add lint and test workflow"
```

### Task 13: Final Report Template and Demo Commands

**Files:**
- Create: `/root/data-mining/reports/final_report.md`
- Modify: `/root/data-mining/README.md`

**Step 1: Write the failing check**

Run: `rg -n "Method Comparison|Ablation|Error Analysis" reports/final_report.md`  
Expected: FAIL because template not created yet.

**Step 2: Run test to verify it fails**

Run: `rg -n "python -m dm_lab run|streamlit run app/Home.py" README.md`  
Expected: FAIL if commands missing.

**Step 3: Write minimal implementation**

```markdown
# Final Report
## Method Comparison
## Ablation Study
## Error Analysis
## Conclusion
```

**Step 4: Run test to verify it passes**

Run:  
- `rg -n "Method Comparison|Ablation|Error Analysis" reports/final_report.md`  
- `rg -n "python -m dm_lab run|streamlit run app/Home.py" README.md`  
Expected: PASS.

**Step 5: Commit**

```bash
git add reports/final_report.md README.md
git commit -m "docs: add final report template and demo commands"
```

---

## Environment and Package Policy (Mandatory)

Install in this order:

1. `pacman` for system/runtime packages first
2. `uv` for Python dependency/env management second
3. `pip` only when previous options are unavailable

Suggested bootstrap commands:

```bash
# system packages first
sudo pacman -S --needed python python-pip python-virtualenv

# python env with uv
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
```

