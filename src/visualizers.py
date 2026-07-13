"""Утилиты для визуализации."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def set_style():
    """Глобальные настройки стиля графиков."""
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 120


def plot_distribution(
    df: pd.DataFrame,
    column: str,
    bins: int = 30,
    title: str | None = None,
) -> plt.Figure:
    """Гистограмма + KDE для одной колонки."""
    fig, ax = plt.subplots()
    sns.histplot(df[column].dropna(), bins=bins, kde=True, ax=ax)
    ax.set_title(title or f"Distribution of {column}")
    ax.set_xlabel(column)
    return fig


def plot_correlation_matrix(
    df: pd.DataFrame,
    title: str = "Correlation Matrix",
    figsize: tuple[int, int] = (10, 8),
) -> plt.Figure:
    """Тепловая карта корреляций."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        df.select_dtypes(include="number").corr(),
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        square=True,
        ax=ax,
    )
    ax.set_title(title)
    return fig
