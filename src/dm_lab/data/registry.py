DATASET_REGISTRY = {
    "classification": {
        "name": "adult_income",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    },
    "clustering": {
        "name": "wholesale_customers",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00292/Wholesale%20customers%20data.csv",
    },
    "association": {
        "name": "online_retail",
        "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx",
    },
    "anomaly": {
        "name": "credit_card_fraud",
        "url": "https://www.openml.org/data/get_csv/1673544/phpKo8OWT",
    },
}


def get_dataset_spec(task: str) -> dict:
    if task not in DATASET_REGISTRY:
        raise KeyError(f"Unknown task: {task}")
    return DATASET_REGISTRY[task]
