from dm_lab.cli import main


def test_cli_run_returns_zero_exit_code(tmp_path) -> None:
    code = main(
        [
            "run",
            "--output-dir",
            str(tmp_path),
            "--config",
            "configs/default.yaml",
            "--quick",
        ]
    )
    assert code == 0
    assert (tmp_path / "summary.json").exists()
