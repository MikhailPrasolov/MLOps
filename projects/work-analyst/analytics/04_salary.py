"""Шаг 4: зарплатная вилка (regex извлечение ₽ / тыс ₽ / $).

Запуск:
    python analytics/04_salary.py
"""
from __future__ import annotations

import re
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


# Строгий паттерн с ОБЯЗАТЕЛЬНЫМ контекстом:
#   - рядом должно быть слово-маркер ("зарплат", "salary", "compensation", "оклад",
#     "₽", "$", "руб", "USD", "EUR") ИЛИ "тыс/к" единица
#   - иначе это телефон/ID/дата, не зарплата
RE_SALARY_CONTEXT = re.compile(
    r"(?:зарплат|salary|compensation|оклад|ЗП|доход|wage|₽|\$|€|руб\.?|rub|USD|EUR)",
    re.IGNORECASE,
)

# Паттерн числа: 1-7 цифр (с пробелами), возможно с разделителями
RE_NUMBER = re.compile(r"\b(\d{1,3}(?:[\s\u00a0]?\d{3})*|\d{1,7})\b")

# Диапазон зарплат (₽/мес) — разумные пределы для русскоязычного чата 2016-2026
SALARY_MIN = 15_000    # ниже — не зарплата
SALARY_MAX = 1_500_000  # выше — выброс (директора/CEO выбросы)

# Конвертация в рубли
USD_TO_RUB_2024 = 90
EUR_TO_RUB_2024 = 100


def _norm_num(s: str) -> int:
    return int(s.replace(" ", "").replace("\u00a0", ""))


def _has_currency_marker(text: str) -> tuple[bool, str]:
    """Возвращает (has_marker, currency_hint).

    True если в тексте есть явный маркер валюты (₽/$/€/руб/USD/EUR)
    или слово ЗП/зарплата/salary.
    """
    low = text.lower()
    if "₽" in text or "руб" in low or "rub" in low:
        return True, "RUB"
    if "$" in text or "usd" in low:
        return True, "USD"
    if "€" in text or "eur" in low:
        return True, "EUR"
    if any(w in low for w in ("зарплат", "salary", "compensation", "оклад", " зп ", "доход")):
        return True, "RUB"  # по умолчанию для русского чата
    return False, ""


def parse_salary(text: str) -> tuple[int | None, int | None, str]:
    """Возвращает (salary_from, salary_to, currency).

    Стратегия:
    1. Найти маркер (₽/$/€/руб/зарплата/...)
    2. В окне ±80 символов от маркера найти первое валидное число
    3. Если есть "X–Y" / "X-Y" / "от X до Y" → две границы
    4. Иначе одна граница
    5. Применяем unit (тыс = *1000, к = *1000)
    6. Фильтр по диапазону [SALARY_MIN, SALARY_MAX]
    """
    if not isinstance(text, str):
        return (None, None, "")

    # 1. Поиск маркера
    m_ctx = RE_SALARY_CONTEXT.search(text)
    if not m_ctx:
        return (None, None, "")
    currency = m_ctx.group(0).lower().replace(".", "")
    if currency in ("₽", "руб", "rub"):
        currency = "RUB"
    elif currency in ("$", "usd"):
        currency = "USD"
    elif currency in ("€", "eur"):
        currency = "EUR"
    elif currency in ("зарплат", "salary", "compensation", "оклад", "зп", "доход"):
        currency = "RUB"
    else:
        currency = "RUB"

    # 2. Окно вокруг маркера
    win_start = max(0, m_ctx.start() - 80)
    win_end = min(len(text), m_ctx.end() + 80)
    window = text[win_start:win_end]

    # 3. Ищем диапазон или одиночное число
    # "от X до Y", "X–Y", "X-Y", "от X", "до X", "X тыс", "Xк"
    RE_RANGE_V2 = re.compile(
        r"(?:от\s*)?(?P<a>\d{2,3}(?:[\s\u00a0]?\d{3})*|\d{4,7})"
        r"\s*[–—\-]\s*(?:до\s*)?(?P<b>\d{2,3}(?:[\s\u00a0]?\d{3})*|\d{4,7})"
        r"|(?:от\s*|до\s*)?(?P<single>\d{2,3}(?:[\s\u00a0]?\d{3})*|\d{4,7})"
        r"\s*(?P<unit>тыс\.?|тысяч|к|k|₽|руб\.?|рублей|rub|USD|\$|EUR|€)?"
    )
    m = RE_RANGE_V2.search(window)
    if not m:
        return (None, None, "")

    def _to_int(s: str | None) -> int | None:
        if s is None:
            return None
        try:
            return _norm_num(s)
        except ValueError:
            return None

    a = _to_int(m.group("a"))
    b = _to_int(m.group("b"))
    single = _to_int(m.group("single"))
    unit = (m.group("unit") or "").lower().replace(".", "")

    if a is not None and b is not None:
        salary_from, salary_to = a, b
    elif single is not None:
        salary_from, salary_to = single, single
    else:
        return (None, None, "")

    # unit multiplier
    if unit in ("тыс", "тысяч", "к", "k"):
        salary_from *= 1000
        salary_to *= 1000

    # Convert to RUB
    if currency == "USD":
        salary_from = int(salary_from * USD_TO_RUB_2024)
        salary_to = int(salary_to * USD_TO_RUB_2024)
    elif currency == "EUR":
        salary_from = int(salary_from * EUR_TO_RUB_2024)
        salary_to = int(salary_to * EUR_TO_RUB_2024)

    # Filter по разумному диапазону (₽/мес)
    def _in_range(v: int) -> int | None:
        return v if SALARY_MIN <= v <= SALARY_MAX else None

    return (_in_range(salary_from), _in_range(salary_to), currency)


def main() -> int:
    df = pd.read_csv(CSV)
    print(f"[INFO] Parsing salaries for {len(df):,} vacancies...")

    parsed = df["text"].apply(parse_salary)
    df["salary_from"] = parsed.apply(lambda t: t[0])
    df["salary_to"] = parsed.apply(lambda t: t[1])
    df["currency"] = parsed.apply(lambda t: t[2])

    has_from = df["salary_from"].notna()
    has_to = df["salary_to"].notna()
    has_any = has_from | has_to

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("ЗАРПЛАТНАЯ ВИЛКА")
    lines.append("=" * 70)
    lines.append(f"Вакансий всего: {len(df):,}")
    lines.append(f"С хотя бы одной границей зарплаты: {has_any.sum():,} "
                 f"({100 * has_any.sum() / len(df):.1f}%)")
    lines.append(f"  - только salary_from: {has_from.sum() - (has_from & has_to).sum():,}")
    lines.append(f"  - только salary_to: {has_to.sum() - (has_from & has_to).sum():,}")
    lines.append(f"  - обе границы: {(has_from & has_to).sum():,}")
    lines.append("")

    # По валютам
    lines.append("## По валютам")
    cur_counts = df.loc[has_any, "currency"].value_counts()
    for cur, n in cur_counts.items():
        lines.append(f"  {cur or '(unknown)':10s}  {n:5d}")
    lines.append("")

    # Статистики только для RUB
    rub = df.loc[(df["currency"] == "RUB") & has_any].copy()
    if len(rub) > 0:
        lines.append("## RUB: статистики")
        lines.append(f"Вакансий с зарплатой в RUB: {len(rub):,}")
        lines.append("")
        lines.append("### salary_from")
        sf = rub["salary_from"].dropna()
        lines.append(f"  count={len(sf)}, "
                    f"min={sf.min():,}, "
                    f"median={sf.median():,.0f}, "
                    f"mean={sf.mean():,.0f}, "
                    f"p90={sf.quantile(0.9):,.0f}, "
                    f"max={sf.max():,}")
        lines.append("")
        lines.append("### salary_to")
        st = rub["salary_to"].dropna()
        lines.append(f"  count={len(st)}, "
                    f"min={st.min():,}, "
                    f"median={st.median():,.0f}, "
                    f"mean={st.mean():,.0f}, "
                    f"p90={st.quantile(0.9):,.0f}, "
                    f"max={st.max():,}")
        lines.append("")
        lines.append("### midpoint = (from + to) / 2")
        mid = ((rub["salary_from"].fillna(0) + rub["salary_to"].fillna(0)) / 2)
        mid = mid[mid > 0]
        lines.append(f"  count={len(mid)}, "
                    f"min={mid.min():,}, "
                    f"median={mid.median():,.0f}, "
                    f"mean={mid.mean():,.0f}, "
                    f"p10={mid.quantile(0.1):,.0f}, "
                    f"p90={mid.quantile(0.9):,.0f}, "
                    f"max={mid.max():,}")
        lines.append("")

        # По годам (тренд)
        rub["date"] = pd.to_datetime(rub["date"], errors="coerce", utc=True)
        rub["year"] = rub["date"].dt.year
        rub_year = rub.dropna(subset=["year"])
        # Медиана midpoint по году (только вакансии с обеими границами или одной)
        rub_year_mid = rub_year.copy()
        rub_year_mid["mid"] = (rub_year_mid["salary_from"].fillna(0)
                                + rub_year_mid["salary_to"].fillna(0)) / 2
        rub_year_mid = rub_year_mid[rub_year_mid["mid"] > 0]

        lines.append("## Медиана midpoint по годам (RUB, ₽/мес)")
        by_year_sal = rub_year_mid.groupby("year")["mid"].agg(["median", "count"])
        for year, row in by_year_sal.iterrows():
            if row["count"] >= 3:
                lines.append(f"  {year}: median={row['median']:>10,.0f} ₽  "
                            f"(n={int(row['count'])})")
        lines.append("")

        # Топ-высокооплачиваемые (для sanity)
        lines.append("## Топ-10 вакансий по median (RUB, ₽/мес)")
        rub["mid"] = (rub["salary_from"].fillna(0) + rub["salary_to"].fillna(0)) / 2
        top10 = rub.nlargest(10, "mid")[["date", "author", "salary_from", "salary_to", "mid"]]
        for _, row in top10.iterrows():
            d = row["date"]
            dstr = d.strftime("%Y-%m-%d") if pd.notna(d) else "?"
            lines.append(f"  {dstr}  from={row['salary_from']:>10,}  "
                        f"to={row['salary_to']:>10,}  mid={int(row['mid']):>10,}  "
                        f"author={row['author']!s:.40s}")

    # Сохранить CSV с распарсенными зарплатами в data/processed/
    data_dir = _ROOT / "data" / "processed"
    data_dir.mkdir(parents=True, exist_ok=True)
    out_csv = data_dir / "vacancies_with_salary.csv"
    keep_cols = ["date", "author", "salary_from", "salary_to", "currency", "tags", "text"]
    df[keep_cols].to_csv(out_csv, index=False, encoding="utf-8")
    lines.append(f"")
    lines.append(f"Расширенный CSV (с зарплатами): {out_csv}")

    out = _HERE / "04_salary.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    # ===== ГРАФИКИ =====
    if len(rub) > 0:
        # Histogram salary_from
        sf = rub["salary_from"].dropna()
        sf_clean = sf[(sf >= 30_000) & (sf <= 1_000_000)]  # отсекаем выбросы
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(sf_clean, bins=50, color="steelblue", edgecolor="black")
        ax.set_title(f"Распределение salary_from (RUB, {len(sf_clean):,} вакансий, отсечено выбросов)")
        ax.set_xlabel("Зарплата от, ₽/мес")
        ax.set_ylabel("Число вакансий")
        ax.grid(axis="y", alpha=0.3)
        ax.axvline(sf_clean.median(), color="red", linestyle="--", label=f"median={sf_clean.median():,.0f}")
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIG_DIR / "salary_from_distribution.png", dpi=100)
        plt.close(fig)

        # Histogram midpoint
        mid = ((rub["salary_from"].fillna(0) + rub["salary_to"].fillna(0)) / 2)
        mid = mid[(mid > 0) & (mid <= 1_000_000)]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(mid, bins=50, color="seagreen", edgecolor="black")
        ax.set_title(f"Распределение midpoint (RUB, {len(mid):,} вакансий)")
        ax.set_xlabel("Зарплата midpoint, ₽/мес")
        ax.set_ylabel("Число вакансий")
        ax.grid(axis="y", alpha=0.3)
        ax.axvline(mid.median(), color="red", linestyle="--", label=f"median={mid.median():,.0f}")
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIG_DIR / "salary_midpoint_distribution.png", dpi=100)
        plt.close(fig)

        # Тренд по годам
        rub_year_mid["year"] = rub_year_mid["year"].astype(int)
        by_year_sal = rub_year_mid.groupby("year")["mid"].agg(["median", "count"])
        by_year_sal = by_year_sal[by_year_sal["count"] >= 3]
        if len(by_year_sal) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(by_year_sal.index, by_year_sal["median"],
                    marker="o", color="darkred", linewidth=2)
            ax.set_title("Медиана зарплаты (RUB, midpoint) по годам")
            ax.set_xlabel("Год")
            ax.set_ylabel("Медиана midpoint, ₽/мес")
            ax.grid(alpha=0.3)
            for x, y in zip(by_year_sal.index, by_year_sal["median"]):
                ax.text(x, y + 5000, f"{y:,.0f}", ha="center", fontsize=9)
            fig.tight_layout()
            fig.savefig(FIG_DIR / "salary_median_by_year.png", dpi=100)
            plt.close(fig)

        # Boxplot по ролям (топ-5)
        rub["role"] = rub["tags"].fillna("").str.lower().apply(_detect_role)
        top_roles_for_plot = rub["role"].value_counts().head(5).index.tolist()
        rub_top = rub[rub["role"].isin(top_roles_for_plot)].copy()
        rub_top["mid"] = (rub_top["salary_from"].fillna(0)
                          + rub_top["salary_to"].fillna(0)) / 2
        rub_top = rub_top[(rub_top["mid"] > 30_000) & (rub_top["mid"] <= 1_000_000)]
        if len(rub_top) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            data = [rub_top[rub_top["role"] == r]["mid"].values
                    for r in top_roles_for_plot]
            ax.boxplot(data, labels=top_roles_for_plot, vert=True, patch_artist=True)
            ax.set_title("Распределение midpoint по ролям (топ-5)")
            ax.set_ylabel("Зарплата midpoint, ₽/мес")
            ax.tick_params(axis="x", rotation=15)
            ax.grid(axis="y", alpha=0.3)
            fig.tight_layout()
            fig.savefig(FIG_DIR / "salary_by_role_boxplot.png", dpi=100)
            plt.close(fig)

    print(f"[OK] {out}")
    print(f"[OK] vacancies_with_salary.csv")
    print(f"[OK] 4 plots → {FIG_DIR}/")
    return 0


ROLE_KEYWORDS = [
    ("Data Scientist", ["#datascientist", "#data_science", "#data_scientest", "#machinelearning"]),
    ("Data-аналитик", ["#dataаналитик", "#dataanalyst", "#аналитикданных"]),
    ("Product Analyst", ["#productanalyst", "#продуктовыйаналитик", "#product_analyst",
                          "#продуктоваяаналитика", "#продуктовый_аналитик", "#аналитикпродукта"]),
    ("Системный аналитик", ["#системныйаналитик", "#systemsanalyst", "#cистемныйанализ", "#sa"]),
    ("Web-аналитик", ["#вебаналитик", "#webаналитик", "#web_analyst", "#webanalyst",
                       "#веб_аналитика", "#web_аналитика", "#аналитик_трафика",
                       "#traffic_analyst"]),
    ("BI", ["#bi", "#analystbi", "#аналитикbi"]),
    ("Бизнес-аналитик", ["#бизнесаналитик", "#бизнессаналитик", "#бизнесаналитика",
                          "#businessanalist"]),
    ("Маркетинг-аналитик", ["#маркетинговыйаналитик", "#маркетинганалитика",
                              "#маркетологаналитик"]),
]


def _detect_role(tags_str: str) -> str:
    low = tags_str
    for name, kws in ROLE_KEYWORDS:
        for kw in kws:
            if kw in low:
                return name
    return ""


if __name__ == "__main__":
    sys.exit(main())