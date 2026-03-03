import importlib


def test_streamlit_home_module_imports() -> None:
    module = importlib.import_module("app.Home")
    assert module is not None
