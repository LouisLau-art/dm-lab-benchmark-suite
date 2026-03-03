from __future__ import annotations

import json
from pathlib import Path

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    st = None


def load_summary(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def render() -> None:
    if st is None:
        return

    st.set_page_config(page_title="DM-Lab Benchmark", layout="wide")
    st.title("DM-Lab Benchmark Suite")
    st.caption("Local-first data mining benchmark dashboard")

    summary = load_summary(Path("artifacts/summary.json"))
    if not summary:
        st.info("No artifacts yet. Run: python -m dm_lab run")
        return

    for task, metrics in summary.items():
        st.subheader(task.title())
        st.json(metrics)


if st is not None:
    render()
