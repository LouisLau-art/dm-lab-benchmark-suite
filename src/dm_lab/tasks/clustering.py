from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

from dm_lab.data.io import download_file
from dm_lab.data.registry import get_dataset_spec


def _quick_dataset(random_state: int) -> pd.DataFrame:
    x, _ = make_blobs(n_samples=900, centers=4, n_features=6, random_state=random_state)
    return pd.DataFrame(x)


def _real_dataset() -> pd.DataFrame:
    spec = get_dataset_spec("clustering")
    path = download_file(spec["url"], "data/wholesale_customers.csv")
    df = pd.read_csv(path)
    drop_cols = [c for c in ["Channel", "Region"] if c in df.columns]
    return df.drop(columns=drop_cols, errors="ignore")


def run_clustering(random_state: int = 42, quick: bool = True) -> dict:
    try:
        df = _quick_dataset(random_state) if quick else _real_dataset()
    except Exception:
        df = _quick_dataset(random_state)

    x = StandardScaler().fit_transform(df)
    model = KMeans(n_clusters=4, n_init=20, random_state=random_state)
    labels = model.fit_predict(x)

    return {
        "silhouette": round(float(silhouette_score(x, labels)), 6),
        "davies_bouldin": round(float(davies_bouldin_score(x, labels)), 6),
    }
