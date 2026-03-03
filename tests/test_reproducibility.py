from dm_lab.pipeline import run_all_tasks


def test_same_seed_produces_same_summary(tmp_path) -> None:
    a = run_all_tasks(output_dir=tmp_path / "a", seed=42, quick=True)
    b = run_all_tasks(output_dir=tmp_path / "b", seed=42, quick=True)
    assert a == b
