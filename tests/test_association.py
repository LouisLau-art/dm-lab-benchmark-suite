from dm_lab.tasks.association import run_association


def test_association_returns_rule_metrics() -> None:
    result = run_association(quick=True)
    assert {"support", "confidence", "lift", "rule_count"} <= set(result.keys())
    assert result["support"] >= 0
    assert result["confidence"] >= 0
    assert result["lift"] >= 0


def test_association_full_mode_uses_real_loader(monkeypatch) -> None:
    called = {"real": False}

    def fake_real_loader() -> list[list[str]]:
        called["real"] = True
        return [["milk", "bread"], ["milk", "diaper"], ["bread", "diaper"]]

    monkeypatch.setattr("dm_lab.tasks.association._load_real_transactions", fake_real_loader)
    result = run_association(quick=False)
    assert called["real"] is True
    assert {"support", "confidence", "lift", "rule_count"} <= set(result.keys())
