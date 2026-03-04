from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from dm_lab.eval.summary import flatten_results


def write_json_summary(results: dict[str, dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return summary_path


def write_markdown_summary(results: dict[str, dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# DM-Lab Results", ""]
    for task, metrics in results.items():
        lines.append(f"## {task.title()}")
        for key, value in metrics.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    markdown_path = output_dir / "summary.md"
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return markdown_path


def write_metrics_table(results: dict[str, dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(flatten_results(results))
    table_path = output_dir / "metrics.csv"
    df.to_csv(table_path, index=False)
    return table_path


def _fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def _primary_metric(task: str, metrics: dict[str, Any]) -> tuple[str, float]:
    mapping = {
        "classification": "f1",
        "clustering": "silhouette",
        "association": "lift",
        "anomaly": "pr_auc",
    }
    metric_name = mapping.get(task)
    if metric_name and metric_name in metrics:
        return metric_name, float(metrics[metric_name])

    # Fallback for unexpected task metrics.
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            return key, float(value)
    return "n/a", 0.0


def _build_method_comparison(results: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "## Method Comparison",
        "",
        "| Task | Primary Metric | Score | Notes |",
        "| --- | --- | ---: | --- |",
    ]

    ranking: list[tuple[str, str, float]] = []
    for task, metrics in results.items():
        metric_name, score = _primary_metric(task, metrics)
        notes = ", ".join(f"{k}={_fmt(v)}" for k, v in metrics.items())
        lines.append(f"| {task} | {metric_name} | {score:.6f} | {notes} |")
        ranking.append((task, metric_name, score))

    ranking.sort(key=lambda item: item[2], reverse=True)
    lines.extend(["", "### Metric Ranking", ""])
    for idx, (task, metric_name, score) in enumerate(ranking, start=1):
        lines.append(f"{idx}. `{task}` by `{metric_name}` = `{score:.6f}`")

    lines.append("")
    return lines


def _build_ablation_study(results: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "## Ablation Study",
        "",
        "This section is auto-generated as a lightweight proxy analysis from current metrics.",
        "",
    ]

    cls = results.get("classification", {})
    if {"precision", "recall"} <= set(cls.keys()):
        gap = abs(float(cls["precision"]) - float(cls["recall"]))
        lines.append(
            f"- Classification threshold sensitivity: |precision-recall| = `{gap:.6f}`. "
            "Consider threshold tuning or class weighting ablation."
        )

    clu = results.get("clustering", {})
    if {"silhouette", "davies_bouldin"} <= set(clu.keys()):
        sil = float(clu["silhouette"])
        db = float(clu["davies_bouldin"])
        lines.append(
            f"- Clustering configuration sensitivity: silhouette `{sil:.6f}`, "
            f"davies-bouldin `{db:.6f}`. Run k-value ablation (e.g., k=3..8)."
        )

    assoc = results.get("association", {})
    if {"support", "confidence", "lift"} <= set(assoc.keys()):
        lines.append(
            "- Association rule threshold sensitivity: "
            f"support `{_fmt(assoc['support'])}`, "
            f"confidence `{_fmt(assoc['confidence'])}`, "
            f"lift `{_fmt(assoc['lift'])}`. "
            "Ablate `min_support` and `min_confidence` to balance rule volume and quality."
        )

    ano = results.get("anomaly", {})
    if {"pr_auc", "recall_at_k"} <= set(ano.keys()):
        lines.append(
            "- Anomaly threshold sensitivity: "
            f"pr_auc `{_fmt(ano['pr_auc'])}`, recall_at_k `{_fmt(ano['recall_at_k'])}`. "
            "Ablate contamination ratio / top-k threshold."
        )

    if lines[-1] == "":
        lines.append("- No ablation hints available for current task outputs.")
    lines.append("")
    return lines


def _build_error_analysis(results: dict[str, dict[str, Any]]) -> list[str]:
    lines = ["## Error Analysis", ""]
    findings: list[str] = []

    cls = results.get("classification", {})
    if cls and float(cls.get("f1", 1.0)) < 0.75:
        findings.append(
            f"- Classification underfitting risk (`f1={_fmt(cls.get('f1'))}`). "
            "Check feature encoding and class imbalance handling."
        )

    clu = results.get("clustering", {})
    if clu and float(clu.get("silhouette", 1.0)) < 0.45:
        findings.append(
            f"- Clustering separability is modest (`silhouette={_fmt(clu.get('silhouette'))}`). "
            "Consider feature scaling variants and alternate cluster count."
        )

    assoc = results.get("association", {})
    if assoc and int(assoc.get("rule_count", 0)) == 0:
        findings.append(
            "- Association produced no rules. "
            "Lower support/confidence or improve transaction density."
        )

    ano = results.get("anomaly", {})
    if ano and float(ano.get("pr_auc", 1.0)) < 0.3:
        findings.append(
            f"- Anomaly detection remains challenging (`pr_auc={_fmt(ano.get('pr_auc'))}`). "
            "Tune contamination/threshold and inspect feature drift."
        )

    if not findings:
        lines.append("- No major metric-level failure detected in this run.")
    else:
        lines.extend(findings)

    lines.extend(
        [
            "",
            "### Recommended Next Checks",
            "",
            "1. Re-run with a different seed to verify stability.",
            "2. Compare quick vs full mode deltas per task.",
            "3. Inspect top error cases for classification/anomaly tasks.",
            "",
        ]
    )
    return lines


def write_final_report(
    results: dict[str, dict[str, Any]],
    output_dir: Path,
    seed: int,
    quick: bool,
    canonical_path: Path | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    mode = "quick" if quick else "full"

    lines: list[str] = [
        "# Final Report",
        "",
        "## Project Overview",
        "",
        "This report is auto-generated from DM-Lab benchmark outputs.",
        f"- Run mode: `{mode}`",
        f"- Seed: `{seed}`",
        f"- Tasks: {', '.join(results.keys())}",
        "",
        "## Datasets and Preprocessing",
        "",
        "- Classification: tabular features with mixed-type preprocessing.",
        "- Clustering: standardized numerical features and KMeans baseline.",
        "- Association: transaction basket encoding and rule mining.",
        "- Anomaly: unsupervised isolation-based scoring with thresholding.",
        "",
    ]

    lines.extend(_build_method_comparison(results))
    lines.extend(_build_ablation_study(results))
    lines.extend(_build_error_analysis(results))
    lines.extend(
        [
            "## Conclusion",
            "",
            "The current run produced a complete baseline across four data-mining tasks. "
            "Use this report as the base for presentation, "
            "then append screenshots/plots from artifacts.",
            "",
        ]
    )

    output_path = output_dir / "final_report.md"
    report_text = "\n".join(lines)
    output_path.write_text(report_text, encoding="utf-8")

    if canonical_path is not None:
        canonical_path.parent.mkdir(parents=True, exist_ok=True)
        canonical_path.write_text(report_text, encoding="utf-8")

    return output_path
