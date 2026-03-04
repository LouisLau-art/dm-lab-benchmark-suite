from __future__ import annotations

import json
from pathlib import Path
from string import Template
from typing import Any

import altair as alt
import pandas as pd

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    st = None

ARTIFACT_CANDIDATES = ["artifacts_full", "artifacts"]


def _inject_style(theme_mode: str) -> None:
    if theme_mode == "Dark":
        palette = {
            "bg0": "#0b1324",
            "bg1": "#101a31",
            "ink": "#e8eefc",
            "muted": "#a4b3cf",
            "card": "rgba(16, 31, 58, 0.9)",
            "hero0": "#152847",
            "hero1": "#0f1d36",
            "hero_border": "rgba(148, 181, 255, 0.28)",
            "sidebar0": "#101b32",
            "sidebar1": "#0d1629",
            "sidebar_border": "rgba(148, 181, 255, 0.2)",
        }
    else:
        palette = {
            "bg0": "#f4f6fb",
            "bg1": "#eef2ff",
            "ink": "#10243e",
            "muted": "#5c6b82",
            "card": "rgba(255, 255, 255, 0.88)",
            "hero0": "#ffffff",
            "hero1": "#f4fbff",
            "hero_border": "rgba(16, 36, 62, 0.08)",
            "sidebar0": "#ffffff",
            "sidebar1": "#f3f8ff",
            "sidebar_border": "rgba(16, 36, 62, 0.08)",
        }

    css_template = Template(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

          :root {
            --bg-0: $bg0;
            --bg-1: $bg1;
            --ink: $ink;
            --muted: $muted;
            --card: $card;
            --accent: #0077b6;
            --accent-2: #00a6fb;
            --ok: #2a9d8f;
            --warn: #e9c46a;
            --bad: #e76f51;
          }

          [data-testid="stAppViewContainer"] {
            background:
              radial-gradient(circle at 8% 2%, rgba(0, 166, 251, 0.14), transparent 34%),
              radial-gradient(circle at 92% 8%, rgba(0, 119, 182, 0.16), transparent 35%),
              linear-gradient(180deg, var(--bg-1), var(--bg-0));
          }

          [data-testid="stSidebar"] {
            background: linear-gradient(180deg, $sidebar0, $sidebar1);
            border-right: 1px solid $sidebar_border;
          }

          .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
          }

          h1, h2, h3 {
            font-family: 'Sora', sans-serif !important;
            color: var(--ink) !important;
            letter-spacing: -0.02em;
          }

          p, li, [data-testid="stMarkdownContainer"] {
            font-family: 'IBM Plex Sans', sans-serif !important;
            color: var(--ink);
          }

          .hero {
            background: linear-gradient(130deg, $hero0 10%, $hero1 92%);
            border: 1px solid $hero_border;
            border-radius: 20px;
            padding: 1.1rem 1.35rem;
            box-shadow: 0 10px 28px rgba(16, 36, 62, 0.18);
            margin-bottom: 1rem;
          }

          .hero-kpi {
            margin-top: 0.55rem;
            display: inline-block;
            background: rgba(0, 166, 251, 0.12);
            color: var(--ink);
            font-weight: 600;
            padding: 0.28rem 0.68rem;
            border-radius: 999px;
            font-size: 0.86rem;
          }

          .metric-card {
            background: var(--card);
            border: 1px solid rgba(16, 36, 62, 0.07);
            border-radius: 16px;
            padding: 0.7rem 0.85rem;
            box-shadow: 0 4px 16px rgba(16, 36, 62, 0.06);
          }

          .pill {
            border-radius: 999px;
            font-size: 0.76rem;
            padding: 0.14rem 0.58rem;
            font-weight: 600;
            display: inline-block;
          }

          .pill-ok { background: rgba(42, 157, 143, 0.16); color: #18564f; }
          .pill-warn { background: rgba(233, 196, 106, 0.2); color: #7a5600; }
          .pill-bad { background: rgba(231, 111, 81, 0.18); color: #6e2e1f; }

          .muted {
            color: var(--muted);
            font-size: 0.9rem;
          }

          [data-testid="stMetricValue"],
          [data-testid="stMetricDelta"] {
            color: var(--ink) !important;
          }
        </style>
        """
    )
    st.markdown(
        css_template.substitute(**palette),
        unsafe_allow_html=True,
    )


def _available_artifact_dirs() -> list[Path]:
    dirs: list[Path] = []
    for candidate in ARTIFACT_CANDIDATES:
        path = Path(candidate)
        if (path / "summary.json").exists():
            dirs.append(path)
    return dirs


def load_summary(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_metrics(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["task", "metric", "value"])
    return pd.read_csv(path)


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _normalize_metric(task: str, metric_name: str, value: float) -> float:
    if task in {"classification", "anomaly"}:
        return _clamp(value, 0.0, 1.0)
    if task == "clustering" and metric_name == "silhouette":
        return _clamp((value + 1.0) / 2.0, 0.0, 1.0)
    if task == "association" and metric_name == "lift":
        return _clamp(value / 10.0, 0.0, 1.0)
    if metric_name == "davies_bouldin":
        return _clamp(1.0 / (1.0 + value), 0.0, 1.0)
    return _clamp(value, 0.0, 1.0)


def _primary_metric(task: str, metrics: dict[str, Any]) -> tuple[str, float, float]:
    preferred = {
        "classification": "f1",
        "clustering": "silhouette",
        "association": "lift",
        "anomaly": "pr_auc",
    }
    metric_name = preferred.get(task, next(iter(metrics.keys())))
    metric_value = float(metrics.get(metric_name, 0.0))
    normalized = _normalize_metric(task, metric_name, metric_value)
    return metric_name, metric_value, normalized


def _grade_label(score: float) -> tuple[str, str]:
    if score >= 0.85:
        return "Strong", "pill-ok"
    if score >= 0.65:
        return "Watch", "pill-warn"
    return "Risk", "pill-bad"


def _task_hint(task: str) -> str:
    hints = {
        "classification": "Watch precision/recall balance and mention threshold tuning in Q&A.",
        "clustering": "Silhouette high + DB low is your key cluster-quality argument.",
        "association": "Lift is the headline metric; connect to market-basket story.",
        "anomaly": "PR-AUC and Recall@k are the right narrative under class imbalance.",
    }
    return hints.get(task, "")


def _presentation_script(summary: dict[str, dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for task, metrics in summary.items():
        name, value, norm = _primary_metric(task, metrics)
        level, _ = _grade_label(norm)
        lines.append(
            f"{task.title()}: primary metric {name}={value:.4f}, readiness={level}."
        )
    return lines


def render() -> None:
    if st is None:
        return

    st.set_page_config(
        page_title="DM-Lab Presentation Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    available = _available_artifact_dirs()
    if not available:
        st.error("No artifacts found. Run: `./scripts/dev.sh run` first.")
        return

    with st.sidebar:
        st.header("Display")
        theme_mode = st.radio("Dashboard theme", options=["Light", "Dark"], index=0)
        st.divider()
        st.header("Run Source")
        selected = st.selectbox(
            "Artifact directory",
            options=[p.as_posix() for p in available],
            index=0,
            help="Choose quick or full run artifacts for the dashboard.",
        )
        summary_path = Path(selected) / "summary.json"
        metrics_path = Path(selected) / "metrics.csv"
        st.caption(f"Using: `{summary_path}`")

    _inject_style(theme_mode)

    if theme_mode == "Dark":
        chart_colors = ["#6ec5ff", "#48b2ff", "#56d7bc", "#ffb88a"]
        chart_text = "#dce8ff"
    else:
        chart_colors = ["#0077b6", "#00a6fb", "#2a9d8f", "#ff7f51"]
        chart_text = "#10243e"

    summary = load_summary(summary_path)
    metrics_df = load_metrics(metrics_path)

    if not summary:
        st.warning("Selected artifact directory has no summary data.")
        return

    cards: list[dict[str, Any]] = []
    for task, metrics in summary.items():
        metric_name, metric_value, normalized = _primary_metric(task, metrics)
        cards.append(
            {
                "task": task,
                "primary_metric": metric_name,
                "value": metric_value,
                "normalized": normalized,
                "score_pct": round(normalized * 100, 2),
            }
        )

    card_df = pd.DataFrame(cards)
    overall = float(card_df["normalized"].mean()) if not card_df.empty else 0.0
    overall_label, overall_css = _grade_label(overall)

    st.markdown(
        f"""
        <div class="hero">
          <h1 style="margin:0;">DM-Lab Presentation Dashboard</h1>
          <p class="muted" style="margin:0.45rem 0 0.2rem 0;">
            Course demo panel for classification, clustering,
            association mining, and anomaly detection.
          </p>
          <span class="hero-kpi">Overall readiness: {overall*100:.1f}%</span>
          <span class="pill {overall_css}" style="margin-left:0.5rem;">{overall_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(4)
    for idx, row in enumerate(cards):
        with columns[idx % 4]:
            level, level_css = _grade_label(float(row["normalized"]))
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                row["task"].title(),
                f"{row['value']:.4f}",
                delta=f"{row['primary_metric']} · {row['score_pct']:.1f}%",
            )
            st.markdown(
                f"<span class='pill {level_css}'>{level}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    tab_overview, tab_task, tab_script = st.tabs(
        ["Overview", "Task Explorer", "Demo Script"]
    )

    with tab_overview:
        left, right = st.columns([1.6, 1.0])
        with left:
            chart = (
                alt.Chart(card_df)
                .mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10)
                .encode(
                    x=alt.X("task:N", sort=list(card_df["task"])),
                    y=alt.Y(
                        "score_pct:Q",
                        title="Normalized Score (%)",
                        scale=alt.Scale(domain=[0, 100]),
                    ),
                    color=alt.Color(
                        "task:N",
                        scale=alt.Scale(
                            range=chart_colors
                        ),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip("task:N"),
                        alt.Tooltip("primary_metric:N", title="Metric"),
                        alt.Tooltip("value:Q", format=".4f", title="Value"),
                        alt.Tooltip("score_pct:Q", format=".2f", title="Normalized (%)"),
                    ],
                )
                .configure_axis(labelColor=chart_text, titleColor=chart_text)
                .configure_title(color=chart_text)
                .configure_view(stroke=None)
                .properties(height=300)
            )
            st.altair_chart(chart, use_container_width=True)

            if not metrics_df.empty:
                st.subheader("Raw Metrics")
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        with right:
            st.subheader("Presentation Readiness")
            st.markdown(
                "- Show **quick vs full** results difference.\n"
                "- Explain one **good metric** and one **risk metric** per task.\n"
                "- Use the report draft for your speaking flow."
            )
            st.subheader("Talk Track Tips")
            st.markdown(
                "- Start from project constraints (local-first, reproducible, AI-built).\n"
                "- Then show dashboard + 1 chart + 1 failure case.\n"
                "- Close with next-step ablation plan."
            )

    with tab_task:
        selected_task = st.selectbox(
            "Select task",
            options=list(summary.keys()),
            index=0,
        )
        task_metrics = summary[selected_task]

        st.markdown(f"### {selected_task.title()}")
        st.caption(_task_hint(selected_task))

        detail_rows = []
        for metric_name, metric_value in task_metrics.items():
            normalized = _normalize_metric(
                selected_task,
                metric_name,
                float(metric_value) if isinstance(metric_value, (int, float)) else 0.0,
            )
            detail_rows.append(
                {
                    "metric": metric_name,
                    "value": metric_value,
                    "normalized_score": round(normalized * 100, 2),
                }
            )
        detail_df = pd.DataFrame(detail_rows)
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

        for _, metric_row in detail_df.iterrows():
            score = float(metric_row["normalized_score"]) / 100.0
            level, level_css = _grade_label(score)
            st.markdown(
                f"**{metric_row['metric']}** · {metric_row['value']} "
                f"<span class='pill {level_css}'>{level}</span>",
                unsafe_allow_html=True,
            )
            st.progress(score)

    with tab_script:
        st.subheader("Auto Demo Script")
        for line in _presentation_script(summary):
            st.markdown(f"- {line}")

        report_path = Path("reports/final_report.md")
        if report_path.exists():
            with st.expander("Open auto-generated final report", expanded=False):
                st.markdown(report_path.read_text(encoding="utf-8"))


if st is not None:
    render()
