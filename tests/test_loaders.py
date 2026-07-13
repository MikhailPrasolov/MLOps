"""Тесты загрузчиков данных."""

from pathlib import Path
import pandas as pd
from src.loaders import load_customers, load_orders, load_top_n_sales


DATA_DIR = Path("data")


def test_load_customers():
    df = load_customers()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_orders():
    df = load_orders()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_top_n_sales():
    df = load_top_n_sales()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
