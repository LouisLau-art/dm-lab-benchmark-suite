from dm_lab.tasks.classification import run_classification


def test_classification_returns_metrics_dict() -> None:
    result = run_classification(random_state=42, quick=True)
    assert {"f1", "roc_auc", "precision", "recall"} <= set(result.keys())
    assert 0 <= result["f1"] <= 1
    assert 0 <= result["roc_auc"] <= 1


def test_classification_full_mode_uses_real_loader(monkeypatch) -> None:
    called = {"real": False}

    def fake_real_loader():
        import pandas as pd

        called["real"] = True
        x = pd.DataFrame(
            {
                "age": [20, 32, 28, 44, 36, 31],
                "hours-per-week": [40, 50, 35, 60, 45, 42],
                "workclass": ["Private", "Self", "Private", "Gov", "Private", "Self"],
            }
        )
        y = pd.Series([0, 1, 0, 1, 1, 0])
        return x, y

    monkeypatch.setattr("dm_lab.tasks.classification._adult_dataset", fake_real_loader)
    result = run_classification(random_state=42, quick=False)
    assert called["real"] is True
    assert {"f1", "roc_auc", "precision", "recall"} <= set(result.keys())
