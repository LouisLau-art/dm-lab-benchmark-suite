from dm_lab.tasks.clustering import run_clustering


def test_clustering_returns_quality_metrics() -> None:
    result = run_clustering(random_state=42, quick=True)
    assert {"silhouette", "davies_bouldin"} <= set(result.keys())
    assert -1 <= result["silhouette"] <= 1
    assert result["davies_bouldin"] >= 0
