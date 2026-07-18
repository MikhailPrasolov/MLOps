"""Шаг 3: топ-городов, типов занятости, senior-уровней.

Запуск:
    python analytics/03_geo_seniority.py
"""
from __future__ import annotations

import sys
from collections import Counter
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


# Канонические теги (lowercase)
CITY_TAGS = {
    "#москва": "Москва",
    "#мск": "Москва",
    "#спб": "СПб",
    "#питер": "СПб",
    "#санкт": "СПб",
    "#санктпетербург": "СПб",
    "#нн": "Нижний Новгород",
    "#нижнийновгород": "Нижний Новгород",
    "#нино": "Нижний Новгород",
    "#екб": "Екатеринбург",
    "#екатеринбург": "Екатеринбург",
    "#казань": "Казань",
    "#kazan": "Казань",
    "#самара": "Самара",
    "#ростов": "Ростов-на-Дону",
    "#омск": "Омск",
    "#чебоксары": "Чебоксары",
    "#сарат": "Саратов",
    "#минск": "Минск",
    "#одесса": "Одесса",
    "#харьков": "Харьков",
    "#тельавив": "Тель-Авив",
    "#амстердам": "Амстердам",
    "#берлин": "Берлин",
    "#кипр": "Кипр",
    "#израиль": "Израиль",
    "#украина": "Украина",
    "#удаленка": "Удалённо",
    "#удаленно": "Удалённо",
    "#удаленной": "Удалённо",
    "#remote": "Remote",
    "#офис": "Офис",
    "#office": "Офис",
    "#anywhere": "Anywhere",
    "#hot": "Горячая",
    "#срочно": "Срочно",
    "#горячаявакансия": "Горячая",
    "#работавминске": "Минск",
    "#работаваналитике": "Все",
    "#работавgamedev": "GameDev",
    "#vacancyinmoscow": "Москва",
    "#msk": "Москва",
}

TYPE_TAGS = {
    "#fulltime": "Full-time",
    "#фуллтайм": "Full-time",
    "#фултайм": "Full-time",
    "#частичнаязанятость": "Part-time",
    "#частичноудаленка": "Part-time удалённо",
    "#частичноудаленно": "Part-time удалённо",
    "#подработка": "Part-time",
    "#проектнаяработа": "Project",
    "#проектная_занятость": "Project",
    "#офис": "Office",
    "#удаленка": "Remote",
    "#удаленно": "Remote",
    "#remote": "Remote",
    "#office_or_remote": "Office/Remote",
}

SENIORITY_TAGS = {
    "#junior": "Junior",
    "#младший": "Junior",
    "#младшийаналитик": "Junior",
    "#джуниор": "Junior",
    "#безопыта": "Junior (без опыта)",
    "#middle": "Middle",
    "#мидл": "Middle",
    "#mid": "Middle",
    "#senoir": "Senior",
    "#senior": "Senior",
    "#lead_analyst": "Lead",
    "#leadanalytics": "Lead",
    "#ведущийаналитик": "Lead",
    "#ведущий_аналитик": "Lead",
    "#ведущийсистемныйаналитик": "Lead",
    "#ведущийпродуктовыйаналитик": "Lead",
    "#руководительbi": "Lead",
    "#руководителя": "Lead",
    "#руководительпроектов": "Lead",
    "#глававебаналитики": "Head",
    "#head": "Head",
    "#headofsocial": "Head",
    "#cto": "Head",
    "#техническийдиректор": "Head",
    "#эксперт": "Senior",
    "#senior_analyst": "Senior",
    "#seniorаналитик": "Senior",
}

ROLE_TAGS = {
    "#аналитик": "Аналитик (общее)",
    "#analyst": "Аналитик (общее)",
    "#dataаналитик": "Data-аналитик",
    "#dataanalyst": "Data-аналитик",
    "#датааналитик": "Data-аналитик",
    "#data_science": "Data Science",
    "#datascientist": "Data Scientist",
    "#datascience": "Data Science",
    "#data_scientest": "Data Scientist",
    "#machinelearning": "ML",
    "#ml": "ML",
    "#productanalyst": "Product Analyst",
    "#продуктовый_аналитик": "Product Analyst",
    "#продуктовыйаналитик": "Product Analyst",
    "#продуктовый": "Product Analyst",
    "#продуктоваяаналитика": "Product Analyst",
    "#продуктовая_аналитика": "Product Analyst",
    "#product_analyst": "Product Analyst",
    "#productmanager": "Product Manager",
    "#вебаналитик": "Web-аналитик",
    "#webаналитик": "Web-аналитик",
    "#web_analyst": "Web-аналитик",
    "#webanalyst": "Web-аналитик",
    "#веб_аналитика": "Web-аналитик",
    "#web_аналитика": "Web-аналитик",
    "#аналитик_трафика": "Web-аналитик",
    "#traffic_analyst": "Web-аналитик",
    "#bi": "BI",
    "#analystbi": "BI",
    "#аналитикbi": "BI",
    "#аналитик1с": "1С-аналитик",
    "#аналитик_1с": "1С-аналитик",
    "#аналитикpython": "Python-аналитик",
    "#аналитик_на_python": "Python-аналитик",
    "#системныйаналитик": "Системный аналитик",
    "#systemsanalyst": "Системный аналитик",
    "#cистемныйанализ": "Системный аналитик",
    "#sa": "Системный аналитик",
    "#бизнесаналитик": "Бизнес-аналитик",
    "#бизнесаналитика": "Бизнес-аналитик",
    "#бизнессаналитик": "Бизнес-аналитик",
    "#businessanalist": "Бизнес-аналитик",
    "#маркетинговый_аналитик": "Маркетинг-аналитик",
    "#маркетинганалитика": "Маркетинг-аналитик",
    "#маркетологаналитик": "Маркетинг-аналитик",
    "#smmаналитик": "SMM-аналитик",
    "#smm": "SMM-аналитик",
    "#финансовоемоделирование": "Финансовый аналитик",
    "#salesanalyst": "Sales-аналитик",
    "#аналитик_продаж": "Sales-аналитик",
    "#аналитик_отдела_продаж": "Sales-аналитик",
    "#аналитикданных": "Data-аналитик",
    "#рисканалитик": "Risk-аналитик",
    "#risk_analyst": "Risk-аналитик",
    "#antifraud": "Anti-fraud",
    "#aml": "Anti-fraud",
    "#информационныйаналитик": "BI",
    "#бизнесаналитики": "Бизнес-аналитик",
    "#аналитикпродукта": "Product Analyst",
    "#аналитик_питер": "Аналитик (общее)",
    "#marketinganalist": "Маркетинг-аналитик",
    "#маркетинговыйаналитик": "Маркетинг-аналитик",
    "#gameаналитик": "Game-аналитик",
    "#gamedev": "Game-аналитик",
    "#работавgamedev": "GameDev",
    "#аналитик_трафика": "Web-аналитик",
    "#dataинжиниринг": "Data Engineer",
    "#data_инжиниринг": "Data Engineer",
    "#uxanalyst": "UX-аналитик",
    "#growth": "Growth-аналитик",
    "#cmo": "Growth-аналитик",
    "#cro": "Growth-аналитик",
    "#headofsocial": "Head of SMM",
    "#teamleader": "Lead",
    "#productmanager": "Product Manager",
    "#businessdevelopment": "BD",
    "#businessdevelopmentmanager": "BD",
    "#продакт": "Product Manager",
}


def _tags_in(raw_tags: str, mapping: dict) -> Counter:
    """Подсчитывает упоминания тегов из raw_tags по маппингу mapping."""
    out: Counter = Counter()
    if not isinstance(raw_tags, str):
        return out
    for raw in raw_tags.split(";"):
        tag = raw.strip().lower()
        if tag in mapping:
            out[mapping[tag]] += 1
    return out


def main() -> int:
    df = pd.read_csv(CSV)
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("ГЕОГРАФИЯ, ТИП ЗАНЯТОСТИ, SENIORITY, РОЛЬ")
    lines.append("=" * 70)
    lines.append(f"Всего вакансий: {len(df):,}")
    lines.append("")

    # 1. Топ-городов
    lines.append("## Топ-25 городов/стран (по тегам)")
    city_counter = Counter()
    for raw in df["tags"].fillna(""):
        city_counter.update(_tags_in(raw, CITY_TAGS))
    total_tagged_cities = sum(city_counter.values())
    lines.append(f"Сумма тегов-городов: {total_tagged_cities} (вакансия может иметь несколько)")
    lines.append(f"Без тега города: {len(df) - total_tagged_cities:,} ({100 * (len(df) - total_tagged_cities) / len(df):.1f}%)")
    for city, n in city_counter.most_common(25):
        pct = n / len(df) * 100
        bar = "#" * min(n // 20, 60)
        lines.append(f"  {n:5d}  {city:25s}  ({pct:5.1f}%)  {bar}")
    lines.append("")

    # 2. Тип занятости
    lines.append("## Тип занятости")
    type_counter = Counter()
    for raw in df["tags"].fillna(""):
        type_counter.update(_tags_in(raw, TYPE_TAGS))
    for t, n in type_counter.most_common():
        pct = n / len(df) * 100
        lines.append(f"  {n:5d}  {t:30s}  ({pct:5.1f}%)")
    lines.append("")

    # 3. Seniority
    lines.append("## Seniority (junior / middle / senior / lead / head)")
    sen_counter = Counter()
    for raw in df["tags"].fillna(""):
        sen_counter.update(_tags_in(raw, SENIORITY_TAGS))
    n_with_sen = sum(sen_counter.values())
    lines.append(f"С тегом уровня: {n_with_sen:,} ({100 * n_with_sen / len(df):.1f}%)")
    for s, n in sen_counter.most_common():
        pct = n / len(df) * 100
        lines.append(f"  {n:5d}  {s:15s}  ({pct:5.1f}%)")
    lines.append("")

    # 4. Роль аналитика
    lines.append("## Роль (тип аналитика)")
    role_counter = Counter()
    for raw in df["tags"].fillna(""):
        role_counter.update(_tags_in(raw, ROLE_TAGS))
    n_with_role = sum(role_counter.values())
    lines.append(f"С тегом роли: {n_with_role:,} ({100 * n_with_role / len(df):.1f}%)")
    lines.append("(вакансия может иметь несколько ролей, например #dataаналитик + #bi)")
    for r, n in role_counter.most_common():
        pct = n / len(df) * 100
        lines.append(f"  {n:5d}  {r:30s}  ({pct:5.1f}%)")
    lines.append("")

    # Сохранить
    out = _HERE / "03_geo_seniority.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    # ===== ГРАФИКИ =====

    # Bar: топ-городов (вертикальный)
    top_cities = city_counter.most_common(15)
    fig, ax = plt.subplots(figsize=(10, 6))
    names = [c[0] for c in top_cities]
    counts = [c[1] for c in top_cities]
    ax.barh(range(len(names))[::-1], counts, color="steelblue", edgecolor="black")
    ax.set_yticks(range(len(names))[::-1])
    ax.set_yticklabels(names)
    ax.set_xlabel("Число вакансий")
    ax.set_title("Топ-15 городов по тегам вакансий (2016–2026)")
    ax.grid(axis="x", alpha=0.3)
    for i, n in enumerate(counts):
        ax.text(n + max(counts) * 0.01, len(names) - 1 - i, str(n), va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "top_cities.png", dpi=100)
    plt.close(fig)

    # Pie: тип занятости
    fig, ax = plt.subplots(figsize=(8, 8))
    top_types = type_counter.most_common(5)
    other_n = sum(type_counter.values()) - sum(n for _, n in top_types)
    labels = [t[0] for t in top_types] + (["Other"] if other_n > 0 else [])
    sizes = [t[1] for t in top_types] + ([other_n] if other_n > 0 else [])
    colors = ["steelblue", "darkorange", "seagreen", "crimson", "mediumpurple", "gray"]
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors[:len(sizes)], startangle=90)
    ax.set_title("Тип занятости (по тегам)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "employment_type_pie.png", dpi=100)
    plt.close(fig)

    # Bar: seniority
    fig, ax = plt.subplots(figsize=(10, 4))
    sen_top = sen_counter.most_common(6)
    names = [s[0] for s in sen_top]
    counts = [s[1] for s in sen_top]
    colors_map = {"Junior": "lightgreen", "Junior (без опыта)": "lightgreen",
                  "Middle": "steelblue", "Senior": "darkorange",
                  "Lead": "crimson", "Head": "purple"}
    colors = [colors_map.get(n, "gray") for n in names]
    ax.bar(names, counts, color=colors, edgecolor="black")
    ax.set_ylabel("Число вакансий")
    ax.set_title("Seniority distribution (по тегам)")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.3)
    for x, n in enumerate(counts):
        ax.text(x, n + max(counts) * 0.01, str(n), ha="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "seniority_distribution.png", dpi=100)
    plt.close(fig)

    # Bar: role (top 15)
    top_roles = role_counter.most_common(15)
    fig, ax = plt.subplots(figsize=(10, 7))
    names = [r[0] for r in top_roles]
    counts = [r[1] for r in top_roles]
    ax.barh(range(len(names))[::-1], counts, color="seagreen", edgecolor="black")
    ax.set_yticks(range(len(names))[::-1])
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Число вакансий")
    ax.set_title("Топ-15 ролей аналитика (по тегам)")
    ax.grid(axis="x", alpha=0.3)
    for i, n in enumerate(counts):
        ax.text(n + max(counts) * 0.01, len(names) - 1 - i, str(n), va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "top_roles.png", dpi=100)
    plt.close(fig)

    print(f"[OK] {out}")
    print(f"[OK] 4 plots → {FIG_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())