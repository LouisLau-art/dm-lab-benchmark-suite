from __future__ import annotations

from pathlib import Path

import requests


def ensure_dir(path: str | Path) -> Path:
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def download_file(url: str, destination: str | Path, timeout: int = 30) -> Path:
    destination_path = Path(destination)
    if destination_path.exists():
        return destination_path

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    destination_path.write_bytes(response.content)
    return destination_path
