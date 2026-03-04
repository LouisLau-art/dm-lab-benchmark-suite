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


def download_with_fallback(
    urls: list[str], destination: str | Path, timeout: int = 30
) -> tuple[Path, str]:
    destination_path = Path(destination)
    if destination_path.exists():
        return destination_path, "cache"

    errors: list[str] = []
    for url in urls:
        try:
            path = download_file(url, destination_path, timeout=timeout)
            return path, url
        except Exception as exc:  # pragma: no cover
            errors.append(f"{url}: {exc}")

    raise RuntimeError("All download URLs failed:\n" + "\n".join(errors))
