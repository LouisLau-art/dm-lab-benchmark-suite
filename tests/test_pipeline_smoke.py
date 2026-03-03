from dm_lab.pipeline import run_all_tasks


def test_run_all_tasks_returns_four_sections(tmp_path) -> None:
    result = run_all_tasks(output_dir=tmp_path, seed=42, quick=True)
    assert {"classification", "clustering", "association", "anomaly"} <= set(result.keys())
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "metrics.csv").exists()
