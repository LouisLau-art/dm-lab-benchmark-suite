from __future__ import annotations

from typing import Any


def flatten_results(results: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task, metrics in results.items():
        for metric_name, value in metrics.items():
            rows.append({"task": task, "metric": metric_name, "value": value})
    return rows
