from __future__ import annotations

import json
from pathlib import Path

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
