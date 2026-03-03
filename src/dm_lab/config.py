from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_CONFIG: dict = {
    "seed": 42,
    "quick_mode": True,
    "tasks": ["classification", "clustering", "association", "anomaly"],
    "output_dir": "artifacts",
}


def load_config(path: str | Path | None) -> dict:
    if path is None:
        return DEFAULT_CONFIG.copy()

    cfg_path = Path(path)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    config = DEFAULT_CONFIG.copy()
    config.update(loaded)

    if "seed" not in config:
        raise ValueError("seed is required")
    if not isinstance(config["seed"], int):
        raise ValueError("seed must be an integer")

    return config
