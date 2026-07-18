"""Шаг 2: тренды по годам и месяцам (2016-2026).

Запуск:
    python analytics/02_time_trends.py

Сохраняет:
    analytics/figures/vacancies_by_year.png  + .txt
    analytics/figures/vacancies_by_month.png
    analytics/figures/year_over_year_growth.png
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
CSV = _ROOT / "data" / "processed" / "vacancies.csv"
FIG_DIR = _HERE / "figures"
FIG_DIR.mkdir(exist_ok=True)


def main() -> int:
    df = pd.read_csv(CSV, parse_dates=["date"], date_format="ISO8601")
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year
    df["ym"] = df["date"].dt.to_period("M")

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("ВРЕМЕННЫЕ ТРЕНДЫ VACANCIES")
    lines.append("=" * 70)
    lines.append(f"Всего вакансий с валидной датой: {len(df):,}")
    lines.append(f"Диапазон: {df['date'].min().date()} — {df['date'].max().date()}")
    lines.append("")

    # 1. По годам
    by_year = df.groupby("year").size().sort_index()
    lines.append("## По годам")
    for year, n in by_year.items():
        bar = "#" * min(n // 20, 60)
        lines.append(f"  {year}  {n:5d}  {bar}")
    lines.append("")

    # Plot: vacancies by year
    fig, ax = plt.subplots(figsize=(10, 5))
    by_year.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
    ax.set_title(f"Вакансии по годам ({int(df['date'].dt.year.min())}–{int(df['date'].dt.year.max())})")
    ax.set_xlabel("Год")
    ax.set_ylabel("Число вакансий")
    ax.grid(axis="y", alpha=0.3)
    for x, n in enumerate(by_year.values):
        ax.text(x, n + max(by_year.values) * 0.01, str(n),
                ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "vacancies_by_year.png", dpi=100)
    plt.close(fig)

    # 2. Год-к-году (YoY growth)
    lines.append("## Год-к-году (YoY growth)")
    prev = None
    for year, n in by_year.items():
        if prev is not None and prev > 0:
            pct = (n - prev) / prev * 100
            sign = "+" if pct >= 0 else ""
            lines.append(f"  {year}: {n:5d}  ({sign}{pct:.1f}% vs {year-1})")
        else:
            lines.append(f"  {year}: {n:5d}  (baseline)")
        prev = n
    lines.append("")

    # Plot YoY
    yoy = by_year.pct_change() * 100
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["green" if (v or 0) >= 0 else "red" for v in yoy.values]
    yoy.plot(kind="bar", ax=ax, color=colors, edgecolor="black")
    ax.set_title("YoY growth (% change vs previous year)")
    ax.set_xlabel("Год")
    ax.set_ylabel("Изменение, %")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "year_over_year_growth.png", dpi=100)
    plt.close(fig)

    # 3. По месяцам (последние 24)
    by_month = df.groupby("ym").size().sort_index()
    last_24 = by_month.tail(24)
    lines.append("## Последние 24 месяца")
    for period, n in last_24.items():
        lines.append(f"  {period}  {n:5d}")
    lines.append("")

    # Plot последние 24
    fig, ax = plt.subplots(figsize=(12, 5))
    last_24.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
    ax.set_title("Вакансии по месяцам (последние 24)")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Число вакансий")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "vacancies_by_month_last24.png", dpi=100)
    plt.close(fig)

    # 4. Полный ряд по месяцам (тонкий line plot)
    fig, ax = plt.subplots(figsize=(14, 5))
    by_month.plot(kind="line", ax=ax, color="steelblue", linewidth=1)
    ax.set_title("Вакансии по месяцам (вся история, 2016–2026)")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Число вакансий")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "vacancies_by_month_full.png", dpi=100)
    plt.close(fig)

    # 5. Скользящее среднее (тренд)
    rolling = by_month.rolling(window=6).mean()
    fig, ax = plt.subplots(figsize=(14, 5))
    by_month.plot(kind="line", ax=ax, color="lightsteelblue",
                  linewidth=1, label="Monthly")
    rolling.plot(kind="line", ax=ax, color="darkred",
                 linewidth=2, label="6-month MA")
    ax.set_title("Тренд вакансий: месячные значения + скользящее среднее 6 мес")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Число вакансий")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "vacancies_trend_ma6.png", dpi=100)
    plt.close(fig)

    # Сохранить вывод
    out = _HERE / "02_time_trends.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] {out}")
    print(f"[OK] 4 plots → {FIG_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())