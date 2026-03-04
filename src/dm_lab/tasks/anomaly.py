from __future__ import annotations

import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, f1_score
from sklearn.model_selection import train_test_split


def _make_anomaly_dataset(random_state: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(random_state)
    normal = rng.normal(loc=0.0, scale=1.0, size=(2800, 8))
    anomalies = rng.normal(loc=4.0, scale=1.2, size=(120, 8))

    x = np.vstack([normal, anomalies])
    y = np.concatenate([np.zeros(len(normal), dtype=int), np.ones(len(anomalies), dtype=int)])
    return x, y


def _load_real_anomaly_dataset(
    random_state: int, max_rows: int = 50_000
) -> tuple[np.ndarray, np.ndarray]:
    frame = fetch_openml(name="creditcard", version=1, as_frame=True, parser="auto")
    x_df = frame.data.apply(lambda col: col.astype(float))
    y_series = frame.target.astype(int)

    if len(x_df) > max_rows:
        x_df, _, y_series, _ = train_test_split(
            x_df,
            y_series,
            train_size=max_rows,
            stratify=y_series,
            random_state=random_state,
        )

    return x_df.to_numpy(dtype=float), y_series.to_numpy(dtype=int)


def run_anomaly(random_state: int = 42, quick: bool = True) -> dict:
    try:
        x, y = (
            _make_anomaly_dataset(random_state)
            if quick
            else _load_real_anomaly_dataset(random_state=random_state)
        )
    except Exception:
        x, y = _make_anomaly_dataset(random_state)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=random_state, stratify=y
    )

    model = IsolationForest(contamination=0.04, random_state=random_state)
    model.fit(x_train[y_train == 0])

    scores = -model.score_samples(x_test)
    pr_auc = average_precision_score(y_test, scores)

    anomaly_ratio = max(y_test.mean(), 0.01)
    threshold = np.quantile(scores, 1 - anomaly_ratio)
    y_pred = (scores >= threshold).astype(int)

    k = max(int(np.sum(y_test == 1)), 1)
    top_idx = np.argsort(scores)[-k:]
    recall_at_k = float(np.sum(y_test[top_idx] == 1) / k)

    return {
        "pr_auc": round(float(pr_auc), 6),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 6),
        "recall_at_k": round(float(recall_at_k), 6),
    }
