from dm_lab.data.registry import get_dataset_spec


def test_registry_contains_classification_dataset() -> None:
    spec = get_dataset_spec("classification")
    assert "name" in spec and "url" in spec
