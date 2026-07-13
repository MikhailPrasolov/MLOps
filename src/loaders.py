"""Функции загрузки данных."""

import pandas as pd
from pathlib import Path


def load_customers(path: str | Path = "data/customers.csv") -> pd.DataFrame:
    """Загрузить данные клиентов."""
    return pd.read_csv(path)


def load_orders(path: str | Path = "data/orders.csv") -> pd.DataFrame:
    """Загрузить данные заказов."""
    return pd.read_csv(path, parse_dates=["order_date"])


def load_top_n_sales(path: str | Path = "data/Top_N_Sales.csv") -> pd.DataFrame:
    """Загрузить детальные продажи (разделитель `;`)."""
    return pd.read_csv(
        path,
        sep=";",
        parse_dates=["TrDte"],
        dayfirst=True,
    )


def load_all() -> dict[str, pd.DataFrame]:
    """Загрузить все датасеты проекта."""
    return {
        "customers": load_customers(),
        "orders": load_orders(),
        "sales": load_top_n_sales(),
    }
