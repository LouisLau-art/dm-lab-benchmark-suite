from dm_lab.tasks.anomaly import run_anomaly


def test_anomaly_returns_core_metrics() -> None:
    result = run_anomaly(random_state=42, quick=True)
    assert {"pr_auc", "f1", "recall_at_k"} <= set(result.keys())
    assert 0 <= result["pr_auc"] <= 1
    assert 0 <= result["f1"] <= 1
