from dm_lab.tasks.clustering import run_clustering


def test_clustering_returns_quality_metrics() -> None:
    result = run_clustering(random_state=42, quick=True)
    assert {"silhouette", "davies_bouldin"} <= set(result.keys())
    assert -1 <= result["silhouette"] <= 1
    assert result["davies_bouldin"] >= 0


def test_clustering_full_mode_uses_real_loader(monkeypatch) -> None:
    called = {"real": False}

    def fake_real_loader():
        import pandas as pd

        called["real"] = True
        return pd.DataFrame(
            {
                "fresh": [1, 2, 3, 4, 5, 6],
                "milk": [6, 5, 4, 3, 2, 1],
                "grocery": [3, 3, 3, 7, 7, 7],
            }
        )

    monkeypatch.setattr("dm_lab.tasks.clustering._real_dataset", fake_real_loader)
    result = run_clustering(random_state=42, quick=False)
    assert called["real"] is True
    assert {"silhouette", "davies_bouldin"} <= set(result.keys())
