from dm_lab.config import load_config


def test_load_config_reads_seed() -> None:
    cfg = load_config("configs/default.yaml")
    assert cfg["seed"] == 42
