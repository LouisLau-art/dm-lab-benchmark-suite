from __future__ import annotations

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


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


def _mine_rules(transactions: list[list[str]]) -> pd.DataFrame:
    encoder = TransactionEncoder()
    encoded = encoder.fit(transactions).transform(transactions)
    basket = pd.DataFrame(encoded, columns=encoder.columns_)

    frequent_itemsets = apriori(basket, min_support=0.2, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.4)
    return rules


def run_association(quick: bool = True) -> dict:
    _ = quick
    rules = _mine_rules(_quick_transactions())

    if rules.empty:
        return {"support": 0.0, "confidence": 0.0, "lift": 0.0, "rule_count": 0}

    best = rules.sort_values(["lift", "confidence"], ascending=False).iloc[0]

    return {
        "support": round(float(best["support"]), 6),
        "confidence": round(float(best["confidence"]), 6),
        "lift": round(float(best["lift"]), 6),
        "rule_count": int(len(rules)),
    }
