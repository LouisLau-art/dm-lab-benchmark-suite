from dm_lab.tasks.classification import run_classification


def test_classification_returns_metrics_dict() -> None:
    result = run_classification(random_state=42, quick=True)
    assert {"f1", "roc_auc", "precision", "recall"} <= set(result.keys())
    assert 0 <= result["f1"] <= 1
    assert 0 <= result["roc_auc"] <= 1
