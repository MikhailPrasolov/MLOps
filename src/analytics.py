"""Аналитические утилиты: EDA, когорты, RFM и др."""

import pandas as pd
import numpy as np


def describe_all(df: pd.DataFrame) -> pd.DataFrame:
    """Расширенное описание числовых колонок."""
    return df.describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).T


def top_n(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Топ-N значений в колонке."""
    return (
        df[column]
        .value_counts()
        .head(n)
        .reset_index()
        .rename(columns={"index": column, column: "count"})
    )
