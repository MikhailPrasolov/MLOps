"""Функции очистки и предобработки данных."""

import pandas as pd
import numpy as np


def summary(df: pd.DataFrame) -> pd.DataFrame:
    """Вывести сводку по датасету: типы, пропуски, уникальные значения."""
    return pd.DataFrame({
        "dtype": df.dtypes,
        "non_null": df.count(),
        "null_pct": (df.isnull().sum() / len(df) * 100).round(2),
        "n_unique": df.nunique(),
    })


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Удалить дубликаты."""
    return df.drop_duplicates(subset=subset)


def fill_missing(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    """Заполнить или удалить пропуски."""
    if strategy == "drop":
        return df.dropna()
    elif strategy == "ffill":
        return df.ffill()
    elif strategy == "bfill":
        return df.bfill()
    elif strategy == "zero":
        return df.fillna(0)
    else:
        return df
