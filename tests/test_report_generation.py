from pathlib import Path

from dm_lab.report.io import write_final_report


def test_write_final_report_fills_required_sections(tmp_path: Path) -> None:
    results = {
        "classification": {
            "f1": 0.7,
            "roc_auc": 0.9,
            "precision": 0.72,
            "recall": 0.68,
        },
        "clustering": {
            "silhouette": 0.4,
            "davies_bouldin": 1.1,
        },
        "association": {
            "support": 0.02,
            "confidence": 0.5,
            "lift": 2.1,
            "rule_count": 12,
        },
        "anomaly": {
            "pr_auc": 0.21,
            "f1": 0.3,
            "recall_at_k": 0.4,
        },
    }

    canonical_path = tmp_path / "reports" / "final_report.md"
    output_path = write_final_report(
        results,
        output_dir=tmp_path / "artifacts",
        seed=42,
        quick=True,
        canonical_path=canonical_path,
    )

    content = output_path.read_text(encoding="utf-8")
    assert "## Method Comparison" in content
    assert "## Ablation Study" in content
    assert "## Error Analysis" in content
    assert "[Describe project objective" not in content
    assert canonical_path.exists()
