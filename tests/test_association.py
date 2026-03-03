from dm_lab.tasks.association import run_association


def test_association_returns_rule_metrics() -> None:
    result = run_association(quick=True)
    assert {"support", "confidence", "lift", "rule_count"} <= set(result.keys())
    assert result["support"] >= 0
    assert result["confidence"] >= 0
    assert result["lift"] >= 0
