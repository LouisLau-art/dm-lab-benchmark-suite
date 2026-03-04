from dm_lab.tasks.anomaly import run_anomaly


def test_anomaly_returns_core_metrics() -> None:
    result = run_anomaly(random_state=42, quick=True)
    assert {"pr_auc", "f1", "recall_at_k"} <= set(result.keys())
    assert 0 <= result["pr_auc"] <= 1
    assert 0 <= result["f1"] <= 1


def test_anomaly_full_mode_uses_real_loader(monkeypatch) -> None:
    called = {"real": False}

    def fake_real_loader(random_state: int) -> tuple:
        import numpy as np

        _ = random_state
        called["real"] = True
        normal = np.zeros((100, 4))
        anomalies = np.ones((20, 4)) * 3
        x = np.vstack([normal, anomalies])
        y = np.concatenate([np.zeros(100, dtype=int), np.ones(20, dtype=int)])
        return x, y

    monkeypatch.setattr("dm_lab.tasks.anomaly._load_real_anomaly_dataset", fake_real_loader)
    result = run_anomaly(random_state=42, quick=False)
    assert called["real"] is True
    assert {"pr_auc", "f1", "recall_at_k"} <= set(result.keys())
