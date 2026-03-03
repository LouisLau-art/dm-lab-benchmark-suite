# DM-Lab Benchmark Suite Design

## 1. Project Goal

Build a lightweight, reproducible local data-mining project for group assessment, with AI completing most implementation work.

Core scope covers four tasks:
- Classification
- Clustering
- Association Rule Mining
- Anomaly Detection

## 2. Constraints and Principles

- Local-first only (no cloud dependency in main workflow).
- Keep engineering simple, but keep experiments non-trivial.
- AI-friendly stack and automation-first workflow.
- Package install priority: `pacman > uv > pip`.
- Public GitHub repository for sharing and collaboration.

## 3. Architecture

Single Python repository, minimal layers:

- `src/dm_lab/data/`
  - dataset download, validation, preprocessing
- `src/dm_lab/tasks/`
  - `classification.py`
  - `clustering.py`
  - `association.py`
  - `anomaly.py`
- `src/dm_lab/eval/`
  - metrics, cross-task summary, simple statistical comparison
- `src/dm_lab/report/`
  - tables/figures/markdown report generator
- `app/`
  - Streamlit result dashboard (view-only, no heavy training)
- `configs/`
  - YAML experiment configs and random seeds
- `tests/`
  - unit/integration/reproducibility checks

No database service, no microservices, no Docker as default requirement.

## 4. Data and Task Plan

Default dataset mapping:

- Classification: Adult Income (OpenML/UCI mirror)
- Clustering: Wholesale Customers
- Association: Online Retail transactions
- Anomaly: Credit Card Fraud

Each task has one backup dataset to avoid source availability issues.

## 5. Experiment Design

- Unified split policy and random seed control.
- Baseline + stronger model per task.
- Fixed metric set per task:
  - Classification: F1, ROC-AUC, Precision/Recall
  - Clustering: Silhouette, Davies-Bouldin
  - Association: Support, Confidence, Lift
  - Anomaly: PR-AUC, Recall@k, F1
- Include ablation/error analysis to support higher grading.

## 6. Data Flow

1. `run` command loads config
2. Download/validate datasets
3. Preprocess and feature-transform
4. Run task pipeline
5. Compute metrics + plots
6. Export report artifacts
7. Streamlit reads generated artifacts for demo

## 7. Error Handling Strategy

- Dataset fetch failure: fallback mirror and clear actionable message.
- Missing columns/schema mismatch: hard fail with expected-vs-actual diff.
- Model training runtime error: isolate per task, continue others, mark failure in summary.
- Reproducibility drift: seed-check test fails CI.

## 8. Testing Strategy

- Unit tests for preprocessing, metric calculators, and config parsing.
- Integration tests for one small smoke run per task.
- Reproducibility test for deterministic outputs under fixed seed.
- CI runs fast test subset; full experiments remain local/manual.

## 9. Deliverables

- Public GitHub repo with reproducible commands.
- Source code for four task pipelines.
- Auto-generated experiment report (markdown + figures).
- Lightweight Streamlit UI for result exploration.
- Final presentation materials based on exported results.

## 10. Success Criteria

- One-command local run produces complete artifacts.
- All four tasks execute end-to-end with metrics and plots.
- Report includes method comparison, ablation, and error analysis.
- Demo can be completed locally within course presentation time.

