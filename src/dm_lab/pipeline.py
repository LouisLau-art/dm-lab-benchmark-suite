from __future__ import annotations

from pathlib import Path

from dm_lab.report.io import (
    write_final_report,
    write_json_summary,
    write_markdown_summary,
    write_metrics_table,
)
from dm_lab.tasks.anomaly import run_anomaly
from dm_lab.tasks.association import run_association
from dm_lab.tasks.classification import run_classification
from dm_lab.tasks.clustering import run_clustering

RUNNERS = {
    "classification": run_classification,
    "clustering": run_clustering,
    "association": run_association,
    "anomaly": run_anomaly,
}


def run_all_tasks(
    output_dir: str | Path,
    seed: int,
    selected_tasks: list[str] | None = None,
    quick: bool = True,
    canonical_report_path: str | Path | None = None,
) -> dict[str, dict]:
    ordered_tasks = selected_tasks or ["classification", "clustering", "association", "anomaly"]

    results: dict[str, dict] = {}
    for task in ordered_tasks:
        runner = RUNNERS[task]
        if task == "association":
            results[task] = runner(quick=quick)
        else:
            results[task] = runner(random_state=seed, quick=quick)

    output_path = Path(output_dir)
    write_json_summary(results, output_path)
    write_markdown_summary(results, output_path)
    write_metrics_table(results, output_path)
    write_final_report(
        results,
        output_dir=output_path,
        seed=seed,
        quick=quick,
        canonical_path=Path(canonical_report_path) if canonical_report_path else None,
    )

    return results
