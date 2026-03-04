from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

from dm_lab.data.io import download_file
from dm_lab.data.registry import get_dataset_spec


def _quick_transactions() -> list[list[str]]:
    return [
        ["milk", "bread", "butter"],
        ["beer", "diaper", "milk"],
        ["bread", "butter"],
        ["beer", "diaper"],
        ["milk", "diaper", "beer", "cola"],
        ["bread", "milk", "diaper", "beer"],
        ["bread", "milk", "diaper", "cola"],
        ["milk", "bread"],
        ["butter", "bread", "jam"],
        ["jam", "bread", "milk"],
    ]


def _load_real_transactions(max_rows: int = 50_000) -> list[list[str]]:
    spec = get_dataset_spec("association")
    candidates: list[tuple[str, Path, str]] = [
        (spec["url"], Path("data/online_retail.xlsx"), "xlsx")
    ]
    fallback_urls = spec.get("fallback_urls", [])
    if fallback_urls:
        candidates.append((fallback_urls[0], Path("data/groceries.csv"), "csv"))

    errors: list[str] = []
    for url, destination, source_type in candidates:
        try:
            if not url:
                continue
            path = download_file(url, destination, timeout=45)
            if source_type == "xlsx":
                return _load_online_retail_transactions(path, max_rows=max_rows)
            return _load_grocery_lines(path)
        except Exception as exc:
            errors.append(f"{url}: {exc}")

    raise RuntimeError("Failed to load association dataset:\n" + "\n".join(errors))


def _load_online_retail_transactions(path: Path, max_rows: int) -> list[list[str]]:
    df = pd.read_excel(path, nrows=max_rows, engine="openpyxl")
    required = {"InvoiceNo", "Description"}
    if not required.issubset(df.columns):
        raise ValueError(f"Online Retail schema mismatch: missing {required - set(df.columns)}")

    if "Quantity" in df.columns:
        df = df[df["Quantity"] > 0]

    cleaned = (
        df.dropna(subset=["InvoiceNo", "Description"])
        .assign(Description=lambda d: d["Description"].astype(str).str.strip().str.lower())
        .query("Description != ''")
    )

    baskets = (
        cleaned.groupby("InvoiceNo")["Description"]
        .apply(lambda series: sorted(set(series.tolist())))
        .tolist()
    )
    return [basket for basket in baskets if len(basket) >= 2]


def _load_grocery_lines(path: Path) -> list[list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    transactions: list[list[str]] = []
    for raw in lines:
        items = [item.strip().lower() for item in raw.split(",") if item.strip()]
        if len(items) >= 2:
            transactions.append(items)
    return transactions


def _shrink_transactions(
    transactions: list[list[str]],
    max_transactions: int,
    top_items: int,
) -> list[list[str]]:
    limited = transactions[:max_transactions]
    frequency = Counter(item for basket in limited for item in set(basket))
    keep = {item for item, _ in frequency.most_common(top_items)}

    reduced: list[list[str]] = []
    for basket in limited:
        filtered = sorted({item for item in basket if item in keep})
        if len(filtered) >= 2:
            reduced.append(filtered)
    return reduced


def _mine_rules(
    transactions: list[list[str]],
    min_support: float,
    min_confidence: float,
    max_len: int | None = None,
) -> pd.DataFrame:
    encoder = TransactionEncoder()
    encoded = encoder.fit(transactions).transform(transactions)
    basket = pd.DataFrame(encoded, columns=encoder.columns_)

    frequent_itemsets = fpgrowth(
        basket,
        min_support=min_support,
        use_colnames=True,
        max_len=max_len,
    )
    if frequent_itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence,
    )
    return rules


def run_association(quick: bool = True) -> dict:
    try:
        transactions = _quick_transactions() if quick else _load_real_transactions()
    except Exception:
        transactions = _quick_transactions()

    if quick:
        working_transactions = transactions
        min_support = 0.2
        min_confidence = 0.4
        max_len = None
    else:
        working_transactions = _shrink_transactions(
            transactions,
            max_transactions=10_000,
            top_items=50,
        )
        min_support = 0.02
        min_confidence = 0.2
        max_len = 3

    rules = _mine_rules(
        working_transactions,
        min_support=min_support,
        min_confidence=min_confidence,
        max_len=max_len,
    )

    if rules.empty:
        return {"support": 0.0, "confidence": 0.0, "lift": 0.0, "rule_count": 0}

    best = rules.sort_values(["lift", "confidence"], ascending=False).iloc[0]

    return {
        "support": round(float(best["support"]), 6),
        "confidence": round(float(best["confidence"]), 6),
        "lift": round(float(best["lift"]), 6),
        "rule_count": int(len(rules)),
    }
